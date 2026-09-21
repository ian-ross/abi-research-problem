"""Temporal-attention U-Net with multi-scale strip-token line mixers."""

from __future__ import annotations

import torch
import torch.nn.functional as F
from torch import Tensor, nn


CANDIDATE_ID = "abi329_temporal_attention_strip_token_line_mixer_unet_bce_dice_line_centerline_aux_v1"
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
    """Build finite per-frame ABI+SZA+BTD features for temporal-attention fusion."""

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
    """Convolution, GroupNorm, GELU, and bounded activations for stable temporal training."""

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
    """Compact residual block used in the encoder, temporal stem, and decoder."""

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


class TemporalAttentionStem(nn.Module):
    """Fuse three temporal frames with lightweight per-pixel temporal attention."""

    def __init__(self, frame_feature_channels: int, out_channels: int) -> None:
        super().__init__()
        self.frame_project = nn.Sequential(
            ConvNormAct(frame_feature_channels, out_channels, kernel_size=1),
            ResidualBlock(out_channels, out_channels),
        )
        self.attention_hidden = ConvNormAct(out_channels * 3, out_channels, kernel_size=1)
        self.attention_logits = nn.Conv2d(out_channels, 1, kernel_size=1)
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
            ResidualBlock(out_channels, out_channels),
        )

    def _frame_attention_logit(self, frame_embed: Tensor, center_embed: Tensor) -> Tensor:
        attention_input = torch.cat((frame_embed, center_embed, torch.abs(frame_embed - center_embed)), dim=1)
        return self.attention_logits(self.attention_hidden(attention_input))

    def forward(self, previous: Tensor, center: Tensor, next_frame: Tensor) -> Tensor:
        previous_embed = self.frame_project(previous)
        center_embed = self.frame_project(center)
        next_embed = self.frame_project(next_frame)

        logits = torch.stack(
            (
                self._frame_attention_logit(previous_embed, center_embed),
                self._frame_attention_logit(center_embed, center_embed),
                self._frame_attention_logit(next_embed, center_embed),
            ),
            dim=1,
        )
        weights = torch.softmax(logits, dim=1)
        stacked_frames = torch.stack((previous_embed, center_embed, next_embed), dim=1)
        attended = _bounded((weights * stacked_frames).sum(dim=1))

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
        center_weight = self.center_gate(torch.cat((center_embed, attended, change_embed), dim=1))
        center_residual = _bounded(center_weight * center_embed + (1.0 - center_weight) * attended)
        return self.fuse(torch.cat((center_residual, attended, change_embed), dim=1))


class StripTokenMixer(nn.Module):
    """Differentiable horizontal/vertical line-token mixing inside the feature hierarchy.

    This is ordinary neural network feature mixing over provider-supplied tensors.
    It does not threshold masks, run morphology, create connected components, or
    implement Artifact Filtering/postprocessing.
    """

    def __init__(self, channels: int, *, strip_size: int = 15) -> None:
        super().__init__()
        pad = strip_size // 2
        self.local = ResidualBlock(channels, channels)
        self.horizontal = nn.Sequential(
            nn.Conv2d(channels, channels, kernel_size=(1, strip_size), padding=(0, pad), groups=channels, bias=False),
            nn.GroupNorm(_group_count(channels), channels),
            nn.GELU(),
            nn.Conv2d(channels, channels, kernel_size=1, bias=False),
        )
        self.vertical = nn.Sequential(
            nn.Conv2d(channels, channels, kernel_size=(strip_size, 1), padding=(pad, 0), groups=channels, bias=False),
            nn.GroupNorm(_group_count(channels), channels),
            nn.GELU(),
            nn.Conv2d(channels, channels, kernel_size=1, bias=False),
        )
        self.global_context = nn.Sequential(nn.AdaptiveAvgPool2d(1), ConvNormAct(channels, channels, kernel_size=1))
        self.gate = nn.Sequential(
            ConvNormAct(channels * 4, channels, kernel_size=1),
            nn.Conv2d(channels, channels, kernel_size=1),
            nn.Sigmoid(),
        )
        self.project = nn.Sequential(ConvNormAct(channels * 4, channels, kernel_size=1), ResidualBlock(channels, channels))

    def forward(self, inputs: Tensor) -> Tensor:
        local = self.local(inputs)
        horizontal = _bounded(self.horizontal(local))
        vertical = _bounded(self.vertical(local))
        pooled = F.interpolate(self.global_context(local), size=local.shape[-2:], mode="bilinear", align_corners=False)
        tokens = torch.cat((local, horizontal, vertical, pooled), dim=1)
        mixed = self.project(tokens)
        gate = self.gate(tokens)
        return _bounded(local + gate * mixed)


class DownBlock(nn.Module):
    """Downsample by two and encode the next scale with strip-token mixing."""

    def __init__(self, in_channels: int, out_channels: int) -> None:
        super().__init__()
        self.block = nn.Sequential(
            nn.MaxPool2d(2),
            ResidualBlock(in_channels, out_channels),
            StripTokenMixer(out_channels, strip_size=11),
        )

    def forward(self, inputs: Tensor) -> Tensor:
        return self.block(inputs)


class SingleStreamEncoder(nn.Module):
    """Single compact encoder after temporal-attention fusion."""

    def __init__(self, base_channels: int) -> None:
        super().__init__()
        self.stem_refine = nn.Sequential(ResidualBlock(base_channels, base_channels), StripTokenMixer(base_channels, strip_size=11))
        self.down1 = DownBlock(base_channels, base_channels * 2)
        self.down2 = DownBlock(base_channels * 2, base_channels * 4)
        self.down3 = DownBlock(base_channels * 4, base_channels * 8)

    def forward(self, features: Tensor) -> tuple[Tensor, Tensor, Tensor, Tensor]:
        scale0 = self.stem_refine(features)
        scale1 = self.down1(scale0)
        scale2 = self.down2(scale1)
        scale3 = self.down3(scale2)
        return scale0, scale1, scale2, scale3


class ASPPContext(nn.Module):
    """Small atrous context block at the bottleneck."""

    def __init__(self, channels: int) -> None:
        super().__init__()
        branch = max(channels // 4, 16)
        self.branch1 = ConvNormAct(channels, branch, kernel_size=1)
        self.branch2 = ConvNormAct(channels, branch, dilation=2)
        self.branch4 = ConvNormAct(channels, branch, dilation=4)
        self.branch8 = ConvNormAct(channels, branch, dilation=8)
        self.image_pool = nn.Sequential(nn.AdaptiveAvgPool2d(1), ConvNormAct(channels, branch, kernel_size=1))
        self.project = nn.Sequential(ConvNormAct(branch * 5, channels, kernel_size=1), ResidualBlock(channels, channels))
        self.strip = StripTokenMixer(channels, strip_size=9)

    def forward(self, inputs: Tensor) -> Tensor:
        pooled = F.interpolate(self.image_pool(inputs), size=inputs.shape[-2:], mode="bilinear", align_corners=False)
        context = self.project(torch.cat((self.branch1(inputs), self.branch2(inputs), self.branch4(inputs), self.branch8(inputs), pooled), dim=1))
        return self.strip(context)


class DecoderFuse(nn.Module):
    """Upsample and merge decoder features with one encoder skip scale."""

    def __init__(self, in_channels: int, skip_channels: int, out_channels: int) -> None:
        super().__init__()
        self.input_project = ConvNormAct(in_channels, out_channels, kernel_size=1)
        self.skip_project = ConvNormAct(skip_channels, out_channels, kernel_size=1)
        self.fuse = nn.Sequential(ConvNormAct(out_channels * 2, out_channels), ResidualBlock(out_channels, out_channels), StripTokenMixer(out_channels, strip_size=11))

    def forward(self, inputs: Tensor, skip: Tensor) -> Tensor:
        upsampled = F.interpolate(inputs, size=skip.shape[-2:], mode="bilinear", align_corners=False)
        return self.fuse(torch.cat((self.input_project(upsampled), self.skip_project(skip)), dim=1))


class ConsensusLogitFloorHead(nn.Module):
    """Bounded consensus head for recall support without thresholding or postprocessing.

    The base region logit keeps ABI-223's compact temporal-attention operating
    point. A small positive residual is added only when learned line,
    centerline, center-detail, and decoder-context evidence agree. A learned
    conflict gate attenuates the lift when detail disagrees with broader context.
    All operations are differentiable architecture logic; there is no mask
    thresholding, morphology, connected-component logic, Artifact Filtering, or
    candidate-owned calibration policy.
    """

    def __init__(self, channels: int) -> None:
        super().__init__()
        self.region_refine = nn.Sequential(ResidualBlock(channels, channels), ConvNormAct(channels, channels, kernel_size=1))
        self.line_refine = nn.Sequential(ConvNormAct(channels * 2, channels), ResidualBlock(channels, channels))
        self.centerline_refine = nn.Sequential(ConvNormAct(channels * 2, channels), ResidualBlock(channels, channels))
        self.detail_refine = nn.Sequential(ConvNormAct(channels * 3, channels), ResidualBlock(channels, channels))
        self.consensus_gate = nn.Sequential(ConvNormAct(channels * 4, channels, kernel_size=1), nn.Conv2d(channels, 1, kernel_size=1), nn.Sigmoid())
        self.conflict_gate = nn.Sequential(ConvNormAct(channels * 3, channels, kernel_size=1), nn.Conv2d(channels, 1, kernel_size=1), nn.Sigmoid())
        self.region_head = nn.Conv2d(channels, 1, kernel_size=1)
        self.line_head = nn.Conv2d(channels, 1, kernel_size=1)
        self.centerline_head = nn.Conv2d(channels, 1, kernel_size=1)
        self.detail_head = nn.Conv2d(channels, 1, kernel_size=1)

    def forward(self, features: Tensor, stem: Tensor) -> dict[str, Tensor]:
        local_detail = _bounded(features - F.avg_pool2d(features, kernel_size=5, stride=1, padding=2, count_include_pad=False))
        stem_detail = _bounded(stem - F.avg_pool2d(stem, kernel_size=7, stride=1, padding=3, count_include_pad=False))
        region_features = self.region_refine(features)
        line_features = self.line_refine(torch.cat((features, local_detail), dim=1))
        centerline_features = self.centerline_refine(torch.cat((features, stem_detail), dim=1))
        detail_features = self.detail_refine(torch.cat((features, local_detail, stem_detail), dim=1))

        region_logits = self.region_head(region_features)
        line_logits = self.line_head(line_features)
        centerline_logits = self.centerline_head(centerline_features)
        detail_logits = self.detail_head(detail_features)

        consensus_gate = self.consensus_gate(torch.cat((region_features, line_features, centerline_features, detail_features), dim=1))
        conflict_gate = self.conflict_gate(torch.cat((torch.abs(region_features - detail_features), local_detail, stem_detail), dim=1))
        positive_consensus = (
            F.relu(torch.tanh(line_logits))
            * F.relu(torch.tanh(centerline_logits))
            * (0.5 + 0.5 * F.relu(torch.tanh(detail_logits)))
        )
        consensus_floor = (1.0 - 0.40 * conflict_gate) * consensus_gate * positive_consensus
        mask_logits = region_logits + 0.18 * consensus_floor
        return {
            "mask_logits": mask_logits,
            "line_logits": line_logits + 0.10 * detail_logits,
            "centerline_logits": centerline_logits + 0.10 * detail_logits,
        }


class TemporalAttentionStripTokenLineMixerUNet(nn.Module):
    """ABI temporal-attention U-Net with multi-scale strip-token line mixing."""

    def __init__(self) -> None:
        super().__init__()
        base = 24
        self.temporal_features = TemporalFrameFeatureBuilder()
        self.temporal_stem = TemporalAttentionStem(self.temporal_features.out_channels, base)
        self.encoder = SingleStreamEncoder(base)
        self.context = ASPPContext(base * 8)
        self.up2 = DecoderFuse(base * 8, base * 4, base * 4)
        self.up1 = DecoderFuse(base * 4, base * 2, base * 2)
        self.up0 = DecoderFuse(base * 2, base, base)
        self.refine = nn.Sequential(
            ConvNormAct(base * 2, base),
            StripTokenMixer(base, strip_size=13),
            ResidualBlock(base, base),
        )
        self.head = ConsensusLogitFloorHead(base)

    def forward(self, inputs: Tensor) -> dict[str, Tensor]:
        previous, center, next_frame = self.temporal_features(inputs)
        stem = self.temporal_stem(previous, center, next_frame)
        scale0, scale1, scale2, scale3 = self.encoder(stem)
        context = self.context(scale3)
        dec2 = self.up2(context, scale2)
        dec1 = self.up1(dec2, scale1)
        dec0 = self.up0(dec1, scale0)
        refined = self.refine(torch.cat((dec0, scale0), dim=1))
        return self.head(refined, scale0)


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
    return TemporalAttentionStripTokenLineMixerUNet()
