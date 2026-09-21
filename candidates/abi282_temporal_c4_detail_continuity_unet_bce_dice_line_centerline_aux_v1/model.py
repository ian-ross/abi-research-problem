"""Temporal-attention U-Net with C4 detail-continuity head for -1/0/+1 ABI+SZA frames."""

from __future__ import annotations

import torch
import torch.nn.functional as F
from torch import Tensor, nn


CANDIDATE_ID = "abi282_temporal_c4_detail_continuity_unet_bce_dice_line_centerline_aux_v1"
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


class DownBlock(nn.Module):
    """Downsample by two and encode the next scale."""

    def __init__(self, in_channels: int, out_channels: int) -> None:
        super().__init__()
        self.block = nn.Sequential(
            nn.MaxPool2d(2),
            ResidualBlock(in_channels, out_channels),
            ResidualBlock(out_channels, out_channels),
        )

    def forward(self, inputs: Tensor) -> Tensor:
        return self.block(inputs)


class SingleStreamEncoder(nn.Module):
    """Single compact encoder after temporal-attention fusion."""

    def __init__(self, base_channels: int) -> None:
        super().__init__()
        self.stem_refine = ResidualBlock(base_channels, base_channels)
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

    def forward(self, inputs: Tensor) -> Tensor:
        pooled = F.interpolate(self.image_pool(inputs), size=inputs.shape[-2:], mode="bilinear", align_corners=False)
        return self.project(torch.cat((self.branch1(inputs), self.branch2(inputs), self.branch4(inputs), self.branch8(inputs), pooled), dim=1))


class DecoderFuse(nn.Module):
    """Upsample and merge decoder features with one encoder skip scale."""

    def __init__(self, in_channels: int, skip_channels: int, out_channels: int) -> None:
        super().__init__()
        self.input_project = ConvNormAct(in_channels, out_channels, kernel_size=1)
        self.skip_project = ConvNormAct(skip_channels, out_channels, kernel_size=1)
        self.fuse = nn.Sequential(ConvNormAct(out_channels * 2, out_channels), ResidualBlock(out_channels, out_channels))

    def forward(self, inputs: Tensor, skip: Tensor) -> Tensor:
        upsampled = F.interpolate(inputs, size=skip.shape[-2:], mode="bilinear", align_corners=False)
        return self.fuse(torch.cat((self.input_project(upsampled), self.skip_project(skip)), dim=1))


class OrientationSharedStripBlock(nn.Module):
    """Anisotropic strip context shared across C4 rotations."""

    def __init__(self, channels: int) -> None:
        super().__init__()
        self.block = nn.Sequential(
            nn.Conv2d(channels, channels, kernel_size=(1, 17), padding=(0, 8), bias=False),
            nn.GroupNorm(_group_count(channels), channels),
            nn.GELU(),
            ResidualBlock(channels, channels),
        )

    def forward(self, inputs: Tensor) -> Tensor:
        return _bounded(self.block(inputs))


class C4SteerableLineContext(nn.Module):
    """Rotation-shared line context used as architecture-internal continuity evidence."""

    def __init__(self, channels: int) -> None:
        super().__init__()
        self.shared_strip = OrientationSharedStripBlock(channels)
        self.orientation_score = nn.Conv2d(channels, 1, kernel_size=1)
        self.detail = ConvNormAct(channels, channels)
        self.project = nn.Sequential(ConvNormAct(channels * 5, channels), ResidualBlock(channels, channels))

    def forward(self, inputs: Tensor) -> Tensor:
        contexts = []
        for k in range(4):
            rotated = torch.rot90(inputs, k, dims=(-2, -1))
            oriented = self.shared_strip(rotated)
            contexts.append(torch.rot90(oriented, -k, dims=(-2, -1)))
        stacked = torch.stack(contexts, dim=1)
        batch, orientations, channels, height, width = stacked.shape
        scores = self.orientation_score(stacked.flatten(0, 1)).view(batch, orientations, 1, height, width)
        weights = torch.softmax(scores, dim=1)
        weighted = _bounded((stacked * weights).sum(dim=1))
        mean_context = _bounded(stacked.mean(dim=1))
        max_context = _bounded(stacked.amax(dim=1))
        detail = self.detail(inputs - F.avg_pool2d(inputs, kernel_size=7, stride=1, padding=3, count_include_pad=False))
        return self.project(torch.cat((inputs, detail, weighted, mean_context, max_context), dim=1))


class C4DetailContinuityHead(nn.Module):
    """Fuse temporal decoder evidence, center-frame detail, and C4 continuity before logits.

    This head is differentiable architecture only. It uses provider-visible center
    ABI/SZA/BTD features and rotation-shared feature context to organize line
    evidence; it does not threshold, postprocess, define losses/metrics, inspect
    coordinates, or implement Artifact Filters.
    """

    def __init__(self, center_channels: int, base_channels: int) -> None:
        super().__init__()
        self.center_project = nn.Sequential(
            ConvNormAct(center_channels, base_channels, kernel_size=1),
            ResidualBlock(base_channels, base_channels),
        )
        self.pre_context = nn.Sequential(
            ConvNormAct(base_channels * 2, base_channels),
            ResidualBlock(base_channels, base_channels),
        )
        self.line_context = C4SteerableLineContext(base_channels)
        self.continuity_gate = nn.Sequential(
            ConvNormAct(base_channels * 4, base_channels, kernel_size=1),
            nn.Conv2d(base_channels, base_channels, kernel_size=1),
            nn.Sigmoid(),
        )
        self.recall_residual = nn.Sequential(
            ConvNormAct(base_channels * 3, base_channels),
            ResidualBlock(base_channels, base_channels),
            nn.Conv2d(base_channels, 1, kernel_size=1),
            nn.Tanh(),
        )
        self.clutter_veto = nn.Sequential(
            ConvNormAct(base_channels * 3, base_channels, kernel_size=1),
            nn.Conv2d(base_channels, 1, kernel_size=1),
            nn.Sigmoid(),
        )
        self.mask_head = nn.Conv2d(base_channels, 1, kernel_size=1)
        self.line_head = nn.Conv2d(base_channels, 1, kernel_size=1)
        self.centerline_head = nn.Conv2d(base_channels, 1, kernel_size=1)

    def forward(self, refined: Tensor, center_features: Tensor) -> dict[str, Tensor]:
        detail = self.center_project(center_features)
        seed = self.pre_context(torch.cat((refined, detail), dim=1))
        line_context = self.line_context(seed)
        line_disagreement = torch.abs(line_context - detail)
        decoder_disagreement = torch.abs(refined - detail)
        gate = self.continuity_gate(torch.cat((refined, detail, line_context, line_disagreement), dim=1))
        fused = _bounded(gate * line_context + (1.0 - gate) * seed)
        gate_strength = gate.mean(dim=1, keepdim=True)
        recall_delta = self.recall_residual(torch.cat((fused, detail, line_context), dim=1))
        veto = self.clutter_veto(torch.cat((fused, line_disagreement, decoder_disagreement), dim=1))
        mask_logits = self.mask_head(fused) + 0.25 * gate_strength * recall_delta - 0.15 * (1.0 - gate_strength) * veto
        return {
            "mask_logits": mask_logits,
            "line_logits": self.line_head(line_context),
            "centerline_logits": self.centerline_head(fused),
        }


class TemporalC4DetailContinuityUNet(nn.Module):
    """Compact temporal-attention U-Net with C4 detail-continuity logits."""

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
            ResidualBlock(base, base),
            ResidualBlock(base, base),
        )
        self.continuity_head = C4DetailContinuityHead(self.temporal_features.out_channels, base)

    def forward(self, inputs: Tensor) -> dict[str, Tensor]:
        previous, center, next_frame = self.temporal_features(inputs)
        stem = self.temporal_stem(previous, center, next_frame)
        scale0, scale1, scale2, scale3 = self.encoder(stem)
        context = self.context(scale3)
        dec2 = self.up2(context, scale2)
        dec1 = self.up1(dec2, scale1)
        dec0 = self.up0(dec1, scale0)
        refined = self.refine(torch.cat((dec0, scale0), dim=1))
        return self.continuity_head(refined, center)


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
    return TemporalC4DetailContinuityUNet()
