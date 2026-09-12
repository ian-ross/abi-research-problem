"""Compact temporal shifted-window-attention U-NetFormer scout for provider-owned ABI+SZA frames."""

from __future__ import annotations

import math

import torch
import torch.nn.functional as F
from torch import Tensor, nn


CANDIDATE_ID = "abi244_temporal_shifted_window_attention_unetformer_bce_dice_line_centerline_aux_v1"
TEMPORAL_OFFSETS = [-1, 0, 1]
CHANNELS_PER_FRAME = 17
FRAME_COUNT = 3
INPUT_CHANNELS = CHANNELS_PER_FRAME * FRAME_COUNT


def _finite_feature(inputs: Tensor, *, limit: float, nan: float = 0.0) -> Tensor:
    """Map non-finite candidate-visible feature values to bounded neutral values."""

    return torch.nan_to_num(inputs, nan=nan, posinf=limit, neginf=-limit).clamp(-limit, limit)


def _bounded(inputs: Tensor, *, limit: float = 12.0) -> Tensor:
    """Bound finite internal activations without hiding non-finite parameter failures."""

    return torch.clamp(inputs, min=-limit, max=limit)


class TemporalFrameFeatureBuilder(nn.Module):
    """Build finite per-frame ABI+SZA+BTD features from candidate-visible channels."""

    _ABI_MEANS = (
        0.1572,
        0.1281,
        0.1566,
        0.0268,
        0.0883,
        0.0753,
        279.45,
        233.17,
        241.06,
        248.44,
        267.58,
        250.28,
        269.32,
        268.23,
        265.94,
        255.61,
    )
    _ABI_SCALES = (
        0.36,
        0.34,
        0.36,
        0.16,
        0.23,
        0.18,
        42.0,
        20.0,
        25.0,
        29.0,
        43.0,
        28.0,
        44.0,
        44.0,
        43.0,
        35.0,
    )
    # Zero-based ABI indices within each 17-channel candidate-visible temporal frame.
    _BTD_PAIRS = (
        (12, 13),  # ABI 13 - ABI 14 clean/longwave window
        (13, 14),  # ABI 14 - ABI 15 longwave/dirty window
        (12, 14),  # ABI 13 - ABI 15 split-window contrast
        (10, 13),  # ABI 11 - ABI 14 cloud-top phase / longwave
        (6, 13),  # ABI 7 - ABI 14 shortwave / longwave window
        (7, 9),  # ABI 8 - ABI 10 water-vapor contrast
        (7, 12),  # ABI 8 - ABI 13 upper-water-vapor / clean-window
        (8, 13),  # ABI 9 - ABI 14 mid-water-vapor / longwave
    )
    _BTD_SCALE = 20.0

    def __init__(self) -> None:
        super().__init__()
        self.register_buffer("abi_means", torch.tensor(self._ABI_MEANS, dtype=torch.float32).view(1, 16, 1, 1))
        self.register_buffer("abi_scales", torch.tensor(self._ABI_SCALES, dtype=torch.float32).view(1, 16, 1, 1))
        self.out_channels = 16 + len(self._BTD_PAIRS) + 2

    def forward_frame(self, frame: Tensor) -> Tensor:
        if frame.ndim != 4 or frame.shape[1] != CHANNELS_PER_FRAME:
            raise ValueError(f"expected [N, {CHANNELS_PER_FRAME}, H, W] ABI+SZA frame, got {tuple(frame.shape)}")
        abi = frame[:, :16, :, :]
        sza = frame[:, 16:17, :, :]
        normalized = _finite_feature((abi - self.abi_means) / self.abi_scales, limit=6.0)
        btd = _finite_feature(
            torch.cat(
                [(abi[:, a : a + 1, :, :] - abi[:, b : b + 1, :, :]) / self._BTD_SCALE for a, b in self._BTD_PAIRS],
                dim=1,
            ),
            limit=6.0,
        )
        sza_finite = torch.nan_to_num(sza, nan=90.0, posinf=180.0, neginf=0.0)
        sza_clamped = torch.clamp(sza_finite, 0.0, 180.0)
        sza_scaled = (sza_clamped - 90.0) / 90.0
        sza_cosine = torch.cos(torch.deg2rad(sza_clamped))
        return torch.cat((normalized, btd, sza_scaled, sza_cosine), dim=1)

    def forward(self, inputs: Tensor) -> tuple[Tensor, Tensor, Tensor]:
        if inputs.ndim != 4 or inputs.shape[1] != INPUT_CHANNELS:
            raise ValueError(f"expected [N, {INPUT_CHANNELS}, H, W] temporal ABI+SZA tensor, got {tuple(inputs.shape)}")
        batch, _, height, width = inputs.shape
        frames = inputs.reshape(batch, FRAME_COUNT, CHANNELS_PER_FRAME, height, width)
        previous = self.forward_frame(frames[:, 0, :, :, :])
        center = self.forward_frame(frames[:, 1, :, :, :])
        next_frame = self.forward_frame(frames[:, 2, :, :, :])
        return previous, center, next_frame


def _group_count(channels: int) -> int:
    for groups in (8, 6, 4, 3, 2, 1):
        if channels % groups == 0:
            return groups
    return 1


class ConvNormAct(nn.Module):
    """Convolution, GroupNorm, GELU, and bounded activations."""

    def __init__(self, in_channels: int, out_channels: int, *, kernel_size: int = 3, dilation: int = 1) -> None:
        super().__init__()
        padding = dilation * (kernel_size // 2)
        self.block = nn.Sequential(
            nn.Conv2d(in_channels, out_channels, kernel_size=kernel_size, padding=padding, dilation=dilation, bias=False),
            nn.GroupNorm(_group_count(out_channels), out_channels),
            nn.GELU(),
        )

    def forward(self, inputs: Tensor) -> Tensor:
        return _bounded(self.block(inputs))


class ResidualBlock(nn.Module):
    """Compact residual convolutional block for stable local features."""

    def __init__(self, in_channels: int, out_channels: int, *, dilation: int = 1) -> None:
        super().__init__()
        self.conv1 = ConvNormAct(in_channels, out_channels, dilation=dilation)
        self.conv2 = nn.Sequential(
            nn.Conv2d(out_channels, out_channels, kernel_size=3, padding=1, bias=False),
            nn.GroupNorm(_group_count(out_channels), out_channels),
        )
        self.skip = nn.Identity() if in_channels == out_channels else nn.Conv2d(in_channels, out_channels, kernel_size=1, bias=False)
        self.act = nn.GELU()

    def forward(self, inputs: Tensor) -> Tensor:
        return _bounded(self.act(_bounded(self.conv2(self.conv1(inputs)) + self.skip(inputs))))


class WindowAttentionBlock(nn.Module):
    """Swin/UNetFormer-style local window self-attention with optional shifted windows."""

    def __init__(
        self,
        channels: int,
        *,
        window_size: int = 8,
        num_heads: int = 4,
        shift_size: int = 0,
        mlp_ratio: int = 2,
    ) -> None:
        super().__init__()
        if channels % num_heads != 0:
            raise ValueError(f"channels={channels} must be divisible by num_heads={num_heads}")
        if not 0 <= shift_size < window_size:
            raise ValueError(f"shift_size={shift_size} must be in [0, {window_size})")
        self.channels = channels
        self.window_size = window_size
        self.shift_size = shift_size
        self.num_heads = num_heads
        self.head_dim = channels // num_heads
        self.scale = 1.0 / math.sqrt(float(self.head_dim))
        self.norm1 = nn.LayerNorm(channels)
        self.qkv = nn.Linear(channels, channels * 3, bias=False)
        self.proj = nn.Linear(channels, channels)
        self.norm2 = nn.LayerNorm(channels)
        hidden = channels * mlp_ratio
        self.mlp = nn.Sequential(nn.Linear(channels, hidden), nn.GELU(), nn.Linear(hidden, channels))
        self.attn_gamma = nn.Parameter(torch.full((channels,), 0.1))
        self.mlp_gamma = nn.Parameter(torch.full((channels,), 0.1))

    def _partition_windows(self, inputs: Tensor) -> Tensor:
        batch, channels, height, width = inputs.shape
        window = self.window_size
        if height % window != 0 or width % window != 0:
            raise ValueError(f"feature map {(height, width)} is not divisible by window size {window}")
        return (
            inputs.view(batch, channels, height // window, window, width // window, window)
            .permute(0, 2, 4, 3, 5, 1)
            .reshape(-1, window * window, channels)
        )

    def _merge_windows(self, windows: Tensor, *, batch: int, height: int, width: int) -> Tensor:
        window = self.window_size
        return (
            windows.view(batch, height // window, width // window, window, window, self.channels)
            .permute(0, 5, 1, 3, 2, 4)
            .reshape(batch, self.channels, height, width)
        )

    def _shift_attention_mask(self, *, height: int, width: int, device: torch.device) -> Tensor | None:
        """Mask cyclic-shift window seams so shifted attention stays local, not wrapped."""

        if self.shift_size == 0:
            return None
        window = self.window_size
        shift = self.shift_size
        region_mask = torch.zeros((1, 1, height, width), device=device)
        h_slices = (slice(0, -window), slice(-window, -shift), slice(-shift, None))
        w_slices = (slice(0, -window), slice(-window, -shift), slice(-shift, None))
        region_id = 0
        for h_slice in h_slices:
            for w_slice in w_slices:
                region_mask[:, :, h_slice, w_slice] = region_id
                region_id += 1
        mask_windows = self._partition_windows(region_mask).view(-1, window * window)
        attention_mask = mask_windows.unsqueeze(1) - mask_windows.unsqueeze(2)
        return attention_mask.masked_fill(attention_mask != 0, -100.0).masked_fill(attention_mask == 0, 0.0)

    def forward(self, inputs: Tensor) -> Tensor:
        batch, _, height, width = inputs.shape
        shifted = inputs
        if self.shift_size:
            shifted = torch.roll(inputs, shifts=(-self.shift_size, -self.shift_size), dims=(2, 3))
        windows = self._partition_windows(shifted)
        normalized = self.norm1(windows)
        qkv = self.qkv(normalized).view(windows.shape[0], windows.shape[1], 3, self.num_heads, self.head_dim)
        q, k, v = qkv.permute(2, 0, 3, 1, 4).unbind(0)
        attention_scores = (q @ k.transpose(-2, -1)) * self.scale
        attention_mask = self._shift_attention_mask(height=height, width=width, device=inputs.device)
        if attention_mask is not None:
            attention_scores = attention_scores.view(batch, -1, self.num_heads, windows.shape[1], windows.shape[1])
            attention_scores = attention_scores + attention_mask.view(1, -1, 1, windows.shape[1], windows.shape[1])
            attention_scores = attention_scores.view(-1, self.num_heads, windows.shape[1], windows.shape[1])
        attention = torch.softmax(attention_scores, dim=-1)
        attended = (attention @ v).transpose(1, 2).reshape(windows.shape[0], windows.shape[1], self.channels)
        windows = windows + self.proj(attended) * self.attn_gamma.view(1, 1, -1)
        windows = windows + self.mlp(self.norm2(windows)) * self.mlp_gamma.view(1, 1, -1)
        merged = self._merge_windows(windows, batch=batch, height=height, width=width)
        if self.shift_size:
            merged = torch.roll(merged, shifts=(self.shift_size, self.shift_size), dims=(2, 3))
        return _bounded(merged)


class TemporalWindowFusionStem(nn.Module):
    """Fuse three provider-owned temporal frames before shifted spatial window attention."""

    def __init__(self, frame_feature_channels: int, out_channels: int) -> None:
        super().__init__()
        self.frame_project = nn.Sequential(
            ConvNormAct(frame_feature_channels, out_channels, kernel_size=1),
            ResidualBlock(out_channels, out_channels),
        )
        self.temporal_logits = nn.Sequential(
            ConvNormAct(out_channels * 3, out_channels, kernel_size=1),
            nn.Conv2d(out_channels, 1, kernel_size=1),
        )
        self.change_project = nn.Sequential(
            ConvNormAct(frame_feature_channels * 4, out_channels, kernel_size=1),
            ResidualBlock(out_channels, out_channels),
        )
        self.center_gate = nn.Sequential(
            ConvNormAct(out_channels * 3, out_channels, kernel_size=1),
            nn.Conv2d(out_channels, out_channels, kernel_size=1),
            nn.Sigmoid(),
        )
        self.fuse = nn.Sequential(
            ConvNormAct(out_channels * 3, out_channels, kernel_size=1),
            ResidualBlock(out_channels, out_channels),
        )
        self.window_refine = WindowAttentionBlock(out_channels, window_size=8, num_heads=4, shift_size=4)

    def _attention_logit(self, frame_embed: Tensor, center_embed: Tensor) -> Tensor:
        return self.temporal_logits(torch.cat((frame_embed, center_embed, torch.abs(frame_embed - center_embed)), dim=1))

    def forward(self, previous: Tensor, center: Tensor, next_frame: Tensor) -> Tensor:
        previous_embed = self.frame_project(previous)
        center_embed = self.frame_project(center)
        next_embed = self.frame_project(next_frame)
        logits = torch.stack(
            (
                self._attention_logit(previous_embed, center_embed),
                self._attention_logit(center_embed, center_embed),
                self._attention_logit(next_embed, center_embed),
            ),
            dim=1,
        )
        weights = torch.softmax(logits, dim=1)
        attended = _bounded((weights * torch.stack((previous_embed, center_embed, next_embed), dim=1)).sum(dim=1))

        neighbor_mean = 0.5 * (previous + next_frame)
        change_features = torch.cat(
            (
                _finite_feature(center - neighbor_mean, limit=8.0),
                _finite_feature(next_frame - previous, limit=8.0),
                _finite_feature(torch.abs(center - previous), limit=8.0),
                _finite_feature(torch.abs(next_frame - center), limit=8.0),
            ),
            dim=1,
        )
        change_embed = self.change_project(change_features)
        gate = self.center_gate(torch.cat((center_embed, attended, change_embed), dim=1))
        center_anchored = _bounded(gate * center_embed + (1.0 - gate) * attended)
        fused = self.fuse(torch.cat((center_anchored, attended, change_embed), dim=1))
        return self.window_refine(fused)


class WindowEncoderStage(nn.Module):
    """Downsample then combine convolutional locality with shifted-window self-attention."""

    def __init__(self, in_channels: int, out_channels: int, *, num_heads: int) -> None:
        super().__init__()
        self.block = nn.Sequential(
            nn.MaxPool2d(2),
            ResidualBlock(in_channels, out_channels),
            WindowAttentionBlock(out_channels, window_size=8, num_heads=num_heads, shift_size=4),
            ResidualBlock(out_channels, out_channels),
        )

    def forward(self, inputs: Tensor) -> Tensor:
        return self.block(inputs)


class WindowUNetFormerEncoder(nn.Module):
    """Compact hierarchical encoder with shifted-window attention stages."""

    def __init__(self, base_channels: int) -> None:
        super().__init__()
        self.scale0 = nn.Sequential(
            ResidualBlock(base_channels, base_channels),
            WindowAttentionBlock(base_channels, window_size=8, num_heads=4, shift_size=4),
        )
        self.down1 = WindowEncoderStage(base_channels, base_channels * 2, num_heads=4)
        self.down2 = WindowEncoderStage(base_channels * 2, base_channels * 4, num_heads=4)
        self.down3 = WindowEncoderStage(base_channels * 4, base_channels * 8, num_heads=6)

    def forward(self, features: Tensor) -> tuple[Tensor, Tensor, Tensor, Tensor]:
        scale0 = self.scale0(features)
        scale1 = self.down1(scale0)
        scale2 = self.down2(scale1)
        scale3 = self.down3(scale2)
        return scale0, scale1, scale2, scale3


class PyramidWindowContext(nn.Module):
    """Bottleneck context mixing shifted-window attention with atrous convolutional context."""

    def __init__(self, channels: int) -> None:
        super().__init__()
        branch = max(channels // 4, 16)
        self.window = WindowAttentionBlock(channels, window_size=8, num_heads=6, shift_size=4)
        self.branch1 = ConvNormAct(channels, branch, kernel_size=1)
        self.branch2 = ConvNormAct(channels, branch, dilation=2)
        self.branch4 = ConvNormAct(channels, branch, dilation=4)
        self.branch8 = ConvNormAct(channels, branch, dilation=8)
        self.image_pool = nn.Sequential(nn.AdaptiveAvgPool2d(1), ConvNormAct(channels, branch, kernel_size=1))
        self.project = nn.Sequential(ConvNormAct(branch * 5, channels, kernel_size=1), ResidualBlock(channels, channels))

    def forward(self, inputs: Tensor) -> Tensor:
        attended = self.window(inputs)
        pooled = F.interpolate(self.image_pool(attended), size=attended.shape[-2:], mode="bilinear", align_corners=False)
        return self.project(torch.cat((self.branch1(attended), self.branch2(attended), self.branch4(attended), self.branch8(attended), pooled), dim=1))


class DecoderFuse(nn.Module):
    """Upsample and merge decoder features with an encoder skip scale."""

    def __init__(self, in_channels: int, skip_channels: int, out_channels: int, *, use_attention: bool) -> None:
        super().__init__()
        self.input_project = ConvNormAct(in_channels, out_channels, kernel_size=1)
        self.skip_project = ConvNormAct(skip_channels, out_channels, kernel_size=1)
        blocks: list[nn.Module] = [ConvNormAct(out_channels * 2, out_channels), ResidualBlock(out_channels, out_channels)]
        if use_attention:
            heads = 4 if out_channels < 192 else 6
            blocks.append(WindowAttentionBlock(out_channels, window_size=8, num_heads=heads, shift_size=4))
        self.fuse = nn.Sequential(*blocks)

    def forward(self, inputs: Tensor, skip: Tensor) -> Tensor:
        upsampled = F.interpolate(inputs, size=skip.shape[-2:], mode="bilinear", align_corners=False)
        return self.fuse(torch.cat((self.input_project(upsampled), self.skip_project(skip)), dim=1))


class TemporalShiftedWindowAttentionUNetFormer(nn.Module):
    """Temporal shifted-window attention encoder-decoder with Line and Centerline auxiliary heads."""

    def __init__(self) -> None:
        super().__init__()
        base = 24
        self.temporal_features = TemporalFrameFeatureBuilder()
        self.temporal_stem = TemporalWindowFusionStem(self.temporal_features.out_channels, base)
        self.encoder = WindowUNetFormerEncoder(base)
        self.context = PyramidWindowContext(base * 8)
        self.up2 = DecoderFuse(base * 8, base * 4, base * 4, use_attention=True)
        self.up1 = DecoderFuse(base * 4, base * 2, base * 2, use_attention=True)
        self.up0 = DecoderFuse(base * 2, base, base, use_attention=False)
        self.refine = nn.Sequential(
            ConvNormAct(base * 2, base),
            ResidualBlock(base, base),
            WindowAttentionBlock(base, window_size=8, num_heads=4, shift_size=4),
            ResidualBlock(base, base),
        )
        self.mask_head = nn.Conv2d(base, 1, kernel_size=1)
        self.line_head = nn.Conv2d(base, 1, kernel_size=1)
        self.centerline_head = nn.Conv2d(base, 1, kernel_size=1)

    def forward(self, inputs: Tensor) -> dict[str, Tensor]:
        previous, center, next_frame = self.temporal_features(inputs)
        stem = self.temporal_stem(previous, center, next_frame)
        scale0, scale1, scale2, scale3 = self.encoder(stem)
        context = self.context(scale3)
        dec2 = self.up2(context, scale2)
        dec1 = self.up1(dec2, scale1)
        dec0 = self.up0(dec1, scale0)
        refined = self.refine(torch.cat((dec0, scale0), dim=1))
        return {
            "mask_logits": self.mask_head(refined),
            "line_logits": self.line_head(refined),
            "centerline_logits": self.centerline_head(refined),
        }


def _validate_auxiliary_outputs(output_spec: dict[str, object]) -> None:
    auxiliary_outputs = output_spec.get("auxiliary_outputs")
    expected = [
        {"target": "line", "name": "line_logits", "shape": [1, 256, 256]},
        {"target": "centerline", "name": "centerline_logits", "shape": [1, 256, 256]},
    ]
    if auxiliary_outputs != expected:
        raise ValueError(f"{CANDIDATE_ID} requires trusted line_logits and centerline_logits auxiliary outputs")


def build_model(input_spec: dict[str, object], output_spec: dict[str, object]) -> nn.Module:
    """Build the model for the Harness-supplied temporal ABI contract."""

    if input_spec.get("mode") != "abi_16ch_plus_sza_temporal":
        raise ValueError(f"{CANDIDATE_ID} requires abi_16ch_plus_sza_temporal input")
    if input_spec.get("shape") != [INPUT_CHANNELS, 256, 256]:
        raise ValueError(f"{CANDIDATE_ID} requires [{INPUT_CHANNELS}, 256, 256] input")
    if input_spec.get("layout") != "channel_stacked_temporal_frames":
        raise ValueError(f"{CANDIDATE_ID} requires channel-stacked temporal input")
    if input_spec.get("base_channels_per_frame") != CHANNELS_PER_FRAME:
        raise ValueError(f"{CANDIDATE_ID} requires {CHANNELS_PER_FRAME} channels per temporal frame")
    offsets = input_spec.get("temporal_frame_offsets", input_spec.get("default_temporal_frame_offsets"))
    if offsets != TEMPORAL_OFFSETS:
        raise ValueError(f"{CANDIDATE_ID} requires temporal frame offsets {TEMPORAL_OFFSETS}")
    if input_spec.get("source_channel_indices_per_frame") not in (None, list(range(16)) + [18]):
        raise ValueError(f"{CANDIDATE_ID} received an unexpected per-frame source-channel contract")
    if output_spec.get("form") != "mask_logits" or output_spec.get("shape") != [1, 256, 256]:
        raise ValueError(f"{CANDIDATE_ID} requires mask_logits [1, 256, 256] primary output")
    _validate_auxiliary_outputs(output_spec)
    return TemporalShiftedWindowAttentionUNetFormer()
