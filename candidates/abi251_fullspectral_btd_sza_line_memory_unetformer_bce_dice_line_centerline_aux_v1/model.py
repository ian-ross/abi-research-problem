"""Full-spectral BTD+SZA shifted-window line-memory U-NetFormer scout."""

from __future__ import annotations

import math

import torch
import torch.nn.functional as F
from torch import Tensor, nn


CANDIDATE_ID = "abi251_fullspectral_btd_sza_line_memory_unetformer_bce_dice_line_centerline_aux_v1"


def _finite_feature(inputs: Tensor, *, limit: float, nan: float = 0.0) -> Tensor:
    """Map non-finite candidate-visible feature values to bounded neutral values."""

    return torch.nan_to_num(inputs, nan=nan, posinf=limit, neginf=-limit).clamp(-limit, limit)


def _bounded(inputs: Tensor, *, limit: float = 12.0) -> Tensor:
    """Bound internal activations without hiding non-finite parameter failures."""

    return torch.clamp(inputs, min=-limit, max=limit)


def _group_count(channels: int) -> int:
    for groups in (8, 6, 5, 4, 3, 2, 1):
        if channels % groups == 0:
            return groups
    return 1


def _smooth(inputs: Tensor, kernel_size: int) -> Tensor:
    return F.avg_pool2d(inputs, kernel_size=kernel_size, stride=1, padding=kernel_size // 2, count_include_pad=False)


class SingleFrameFeatureBuilder(nn.Module):
    """Build normalized ABI+SZA, approved-channel BTD, and learned features."""

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
    _BTD_PAIRS = (
        (12, 13),
        (13, 14),
        (12, 14),
        (10, 13),
        (6, 13),
        (7, 9),
        (7, 12),
        (8, 13),
    )
    _BTD_SCALE = 20.0

    def __init__(self, learned_channels: int = 16) -> None:
        super().__init__()
        self.register_buffer("abi_means", torch.tensor(self._ABI_MEANS, dtype=torch.float32).view(1, 16, 1, 1))
        self.register_buffer("abi_scales", torch.tensor(self._ABI_SCALES, dtype=torch.float32).view(1, 16, 1, 1))
        self.learned_mixer = nn.Sequential(nn.Conv2d(17, learned_channels, kernel_size=1), nn.GELU())
        self.out_channels = 16 + len(self._BTD_PAIRS) + 2 + learned_channels

    def forward(self, inputs: Tensor) -> Tensor:
        if inputs.ndim != 4 or inputs.shape[1] != 17:
            raise ValueError(f"expected [N, 17, H, W] ABI+SZA tensor, got {tuple(inputs.shape)}")
        abi = inputs[:, :16]
        sza = torch.nan_to_num(inputs[:, 16:17], nan=90.0, posinf=180.0, neginf=0.0).clamp(0.0, 180.0)
        normalized = _finite_feature((abi - self.abi_means) / self.abi_scales, limit=6.0)
        btd = _finite_feature(
            torch.cat([(abi[:, a : a + 1] - abi[:, b : b + 1]) / self._BTD_SCALE for a, b in self._BTD_PAIRS], dim=1),
            limit=6.0,
        )
        sza_scaled = (sza - 90.0) / 90.0
        sza_cosine = torch.cos(torch.deg2rad(sza))
        learned = _bounded(self.learned_mixer(torch.cat((normalized, sza_scaled), dim=1)))
        return torch.cat((normalized, btd, sza_scaled, sza_cosine, learned), dim=1)


class ConvNormAct(nn.Module):
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


class SignedDetailStem(nn.Module):
    """Expose local signed detail and broad context as learned model features."""

    def __init__(self, in_channels: int, out_channels: int) -> None:
        super().__init__()
        self.raw = ConvNormAct(in_channels, out_channels, kernel_size=1)
        self.local_pos = ConvNormAct(in_channels, out_channels, kernel_size=1)
        self.local_neg = ConvNormAct(in_channels, out_channels, kernel_size=1)
        self.mid_pos = ConvNormAct(in_channels, out_channels, kernel_size=1)
        self.context = ConvNormAct(in_channels, out_channels, kernel_size=1)
        self.fuse = nn.Sequential(ConvNormAct(out_channels * 5, out_channels), ResidualBlock(out_channels, out_channels))

    def forward(self, inputs: Tensor) -> Tensor:
        local_detail = inputs - _smooth(inputs, 7)
        mid_detail = inputs - _smooth(inputs, 15)
        broad = _smooth(inputs, 31)
        return self.fuse(
            torch.cat(
                (
                    self.raw(inputs),
                    self.local_pos(F.relu(local_detail)),
                    self.local_neg(F.relu(-local_detail)),
                    self.mid_pos(F.relu(mid_detail)),
                    self.context(broad),
                ),
                dim=1,
            )
        )


class WindowAttentionBlock(nn.Module):
    """Swin/UNetFormer-style local self-attention with optional shifted windows."""

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
        self.attn_gamma = nn.Parameter(torch.full((channels,), 0.08))
        self.mlp_gamma = nn.Parameter(torch.full((channels,), 0.08))

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


class LineMemoryBlock(nn.Module):
    """Row/column global line-memory context, implemented as differentiable feature logic."""

    def __init__(self, channels: int) -> None:
        super().__init__()
        self.horizontal = nn.Sequential(
            nn.Conv2d(channels, channels, kernel_size=(1, 17), padding=(0, 8), groups=channels, bias=False),
            nn.Conv2d(channels, channels, kernel_size=1, bias=False),
            nn.GroupNorm(_group_count(channels), channels),
            nn.GELU(),
        )
        self.vertical = nn.Sequential(
            nn.Conv2d(channels, channels, kernel_size=(17, 1), padding=(8, 0), groups=channels, bias=False),
            nn.Conv2d(channels, channels, kernel_size=1, bias=False),
            nn.GroupNorm(_group_count(channels), channels),
            nn.GELU(),
        )
        self.row_project = nn.Sequential(
            nn.Conv2d(channels, channels, kernel_size=(9, 1), padding=(4, 0), groups=channels, bias=False),
            nn.Conv2d(channels, channels, kernel_size=1, bias=False),
            nn.GroupNorm(_group_count(channels), channels),
            nn.GELU(),
        )
        self.col_project = nn.Sequential(
            nn.Conv2d(channels, channels, kernel_size=(1, 9), padding=(0, 4), groups=channels, bias=False),
            nn.Conv2d(channels, channels, kernel_size=1, bias=False),
            nn.GroupNorm(_group_count(channels), channels),
            nn.GELU(),
        )
        self.gate = nn.Sequential(ConvNormAct(channels * 5, channels, kernel_size=1), nn.Conv2d(channels, channels, kernel_size=1), nn.Sigmoid())
        self.project = nn.Sequential(ConvNormAct(channels * 5, channels, kernel_size=1), ResidualBlock(channels, channels))
        self.residual_scale = nn.Parameter(torch.tensor(0.15))

    def forward(self, inputs: Tensor) -> Tensor:
        horizontal = self.horizontal(inputs)
        vertical = self.vertical(inputs)
        row_context = self.row_project(inputs.mean(dim=3, keepdim=True)).expand_as(inputs)
        col_context = self.col_project(inputs.mean(dim=2, keepdim=True)).expand_as(inputs)
        broad = _smooth(inputs, 31)
        stacked = torch.cat((inputs, horizontal, vertical, row_context, col_context + broad), dim=1)
        gate = self.gate(stacked)
        memory = self.project(stacked)
        return _bounded(inputs + torch.tanh(self.residual_scale) * gate * memory)


class WindowLineEncoderStage(nn.Module):
    def __init__(self, in_channels: int, out_channels: int, *, num_heads: int) -> None:
        super().__init__()
        self.down = nn.MaxPool2d(2)
        self.project = ResidualBlock(in_channels, out_channels)
        self.window = WindowAttentionBlock(out_channels, window_size=8, num_heads=num_heads, shift_size=4)
        self.line_memory = LineMemoryBlock(out_channels)
        self.refine = ResidualBlock(out_channels, out_channels)

    def forward(self, inputs: Tensor) -> Tensor:
        features = self.project(self.down(inputs))
        features = self.window(features)
        features = self.line_memory(features)
        return self.refine(features)


class PyramidLineWindowContext(nn.Module):
    def __init__(self, channels: int, *, num_heads: int) -> None:
        super().__init__()
        branch = max(channels // 4, 24)
        self.window = WindowAttentionBlock(channels, window_size=8, num_heads=num_heads, shift_size=4)
        self.line_memory = LineMemoryBlock(channels)
        self.branch1 = ConvNormAct(channels, branch, kernel_size=1)
        self.branch2 = ConvNormAct(channels, branch, dilation=2)
        self.branch4 = ConvNormAct(channels, branch, dilation=4)
        self.branch8 = ConvNormAct(channels, branch, dilation=8)
        self.image_pool = nn.Sequential(nn.AdaptiveAvgPool2d(1), ConvNormAct(channels, branch, kernel_size=1))
        self.project = nn.Sequential(ConvNormAct(branch * 5, channels, kernel_size=1), ResidualBlock(channels, channels))

    def forward(self, inputs: Tensor) -> Tensor:
        attended = self.line_memory(self.window(inputs))
        pooled = F.interpolate(self.image_pool(attended), size=attended.shape[-2:], mode="bilinear", align_corners=False)
        return self.project(torch.cat((self.branch1(attended), self.branch2(attended), self.branch4(attended), self.branch8(attended), pooled), dim=1))


class DecoderFuse(nn.Module):
    def __init__(self, in_channels: int, skip_channels: int, out_channels: int, *, use_attention: bool) -> None:
        super().__init__()
        self.input_project = ConvNormAct(in_channels, out_channels, kernel_size=1)
        self.skip_project = ConvNormAct(skip_channels, out_channels, kernel_size=1)
        blocks: list[nn.Module] = [ConvNormAct(out_channels * 2, out_channels), ResidualBlock(out_channels, out_channels), LineMemoryBlock(out_channels)]
        if use_attention:
            blocks.append(WindowAttentionBlock(out_channels, window_size=8, num_heads=4, shift_size=4))
        self.fuse = nn.Sequential(*blocks)

    def forward(self, inputs: Tensor, skip: Tensor) -> Tensor:
        upsampled = F.interpolate(inputs, size=skip.shape[-2:], mode="bilinear", align_corners=False)
        return self.fuse(torch.cat((self.input_project(upsampled), self.skip_project(skip)), dim=1))


class CalibratedLineMemoryHead(nn.Module):
    """Internal feature-fusion head for recall/precision balance at fixed threshold."""

    def __init__(self, channels: int) -> None:
        super().__init__()
        self.recall_features = nn.Sequential(ConvNormAct(channels, channels, dilation=2), ResidualBlock(channels, channels))
        self.precision_features = nn.Sequential(LineMemoryBlock(channels), ResidualBlock(channels, channels))
        self.agreement_gate = nn.Sequential(
            ConvNormAct(channels * 4, channels, kernel_size=1),
            nn.Conv2d(channels, channels, kernel_size=1),
            nn.Sigmoid(),
        )
        self.fuse = nn.Sequential(ConvNormAct(channels * 3, channels), ResidualBlock(channels, channels))
        self.mask_head = nn.Conv2d(channels, 1, kernel_size=1)
        self.line_head = nn.Conv2d(channels, 1, kernel_size=1)
        self.centerline_head = nn.Conv2d(channels, 1, kernel_size=1)

    def forward(self, features: Tensor) -> dict[str, Tensor]:
        recall = self.recall_features(features)
        precision = self.precision_features(features)
        gate = self.agreement_gate(torch.cat((features, recall, precision, torch.abs(recall - precision)), dim=1))
        fused = self.fuse(torch.cat((features, gate * recall, (1.0 - gate) * precision), dim=1))
        return {
            "mask_logits": self.mask_head(fused),
            "line_logits": self.line_head(precision),
            "centerline_logits": self.centerline_head(fused),
        }


class FullSpectralBTDSZALineMemoryUNetFormer(nn.Module):
    def __init__(self) -> None:
        super().__init__()
        base = 32
        self.features = SingleFrameFeatureBuilder(learned_channels=16)
        self.stem = SignedDetailStem(self.features.out_channels, base)
        self.scale0 = nn.Sequential(
            ResidualBlock(base, base),
            WindowAttentionBlock(base, window_size=8, num_heads=4, shift_size=4),
            LineMemoryBlock(base),
        )
        self.down1 = WindowLineEncoderStage(base, base * 2, num_heads=4)
        self.down2 = WindowLineEncoderStage(base * 2, base * 4, num_heads=4)
        self.down3 = WindowLineEncoderStage(base * 4, base * 6, num_heads=6)
        self.context = PyramidLineWindowContext(base * 6, num_heads=6)
        self.up2 = DecoderFuse(base * 6, base * 4, base * 4, use_attention=True)
        self.up1 = DecoderFuse(base * 4, base * 2, base * 2, use_attention=True)
        self.up0 = DecoderFuse(base * 2, base, base, use_attention=False)
        self.highres_detail = SignedDetailStem(self.features.out_channels, base)
        self.final_refine = nn.Sequential(
            ConvNormAct(base * 3, base),
            ResidualBlock(base, base),
            LineMemoryBlock(base),
            WindowAttentionBlock(base, window_size=8, num_heads=4, shift_size=4),
            ResidualBlock(base, base),
        )
        self.head = CalibratedLineMemoryHead(base)

    def forward(self, inputs: Tensor) -> dict[str, Tensor]:
        features = self.features(inputs)
        stem = self.stem(features)
        scale0 = self.scale0(stem)
        scale1 = self.down1(scale0)
        scale2 = self.down2(scale1)
        scale3 = self.down3(scale2)
        context = self.context(scale3)
        dec2 = self.up2(context, scale2)
        dec1 = self.up1(dec2, scale1)
        dec0 = self.up0(dec1, scale0)
        detail = self.highres_detail(features)
        refined = self.final_refine(torch.cat((dec0, detail, stem), dim=1))
        return self.head(refined)


def _validate_auxiliary_outputs(output_spec: dict[str, object]) -> None:
    expected = [
        {"target": "line", "name": "line_logits", "shape": [1, 256, 256]},
        {"target": "centerline", "name": "centerline_logits", "shape": [1, 256, 256]},
    ]
    if output_spec.get("auxiliary_outputs") != expected:
        raise ValueError(f"{CANDIDATE_ID} requires trusted line_logits and centerline_logits auxiliary outputs")


def build_model(input_spec: dict[str, object], output_spec: dict[str, object]) -> nn.Module:
    """Build the model for the Harness-supplied ABI+SZA contract."""

    if input_spec.get("mode") != "abi_16ch_plus_sza" or input_spec.get("shape") != [17, 256, 256]:
        raise ValueError(f"{CANDIDATE_ID} requires abi_16ch_plus_sza [17, 256, 256] input")
    if output_spec.get("form") != "mask_logits" or output_spec.get("shape") != [1, 256, 256]:
        raise ValueError(f"{CANDIDATE_ID} requires mask_logits [1, 256, 256] primary output")
    _validate_auxiliary_outputs(output_spec)
    return FullSpectralBTDSZALineMemoryUNetFormer()
