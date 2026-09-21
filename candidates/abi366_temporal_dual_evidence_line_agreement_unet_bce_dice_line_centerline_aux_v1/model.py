"""Temporal dual-evidence line-agreement U-Net for provider-owned -1/0/+1 ABI+SZA frames."""

from __future__ import annotations

import torch
import torch.nn.functional as F
from torch import Tensor, nn


CANDIDATE_ID = "abi366_temporal_dual_evidence_line_agreement_unet_bce_dice_line_centerline_aux_v1"
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
    """Build finite per-frame ABI+SZA+BTD features for temporal evidence streams."""

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
    """Compact residual block used in stems, encoders, and decoder."""

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


class TemporalDualEvidenceStem(nn.Module):
    """Create separate center-detail and temporal-change evidence streams."""

    def __init__(self, frame_feature_channels: int, out_channels: int) -> None:
        super().__init__()
        self.center_project = nn.Sequential(
            ConvNormAct(frame_feature_channels, out_channels, kernel_size=1),
            ResidualBlock(out_channels, out_channels),
        )
        self.change_project = nn.Sequential(
            ConvNormAct(frame_feature_channels * 4, out_channels, kernel_size=1),
            ResidualBlock(out_channels, out_channels),
            ResidualBlock(out_channels, out_channels),
        )
        self.initial_agreement = nn.Sequential(
            ConvNormAct(out_channels * 3, out_channels, kernel_size=1),
            nn.Conv2d(out_channels, out_channels, kernel_size=1),
            nn.Sigmoid(),
        )
        self.center_refine = ResidualBlock(out_channels, out_channels)
        self.change_refine = ResidualBlock(out_channels, out_channels)

    def forward(self, previous: Tensor, center: Tensor, next_frame: Tensor) -> tuple[Tensor, Tensor]:
        center_embed = self.center_project(center)
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
        gate = self.initial_agreement(torch.cat((center_embed, change_embed, torch.abs(center_embed - change_embed)), dim=1))
        return self.center_refine(center_embed), self.change_refine(_bounded(gate * change_embed + (1.0 - gate) * center_embed))


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
    """Compact encoder for one evidence stream."""

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


class EvidenceAgreementFuse(nn.Module):
    """Fuse center and change evidence at one scale using architecture-internal agreement."""

    def __init__(self, channels: int) -> None:
        super().__init__()
        self.center_project = ConvNormAct(channels, channels, kernel_size=1)
        self.change_project = ConvNormAct(channels, channels, kernel_size=1)
        self.gate = nn.Sequential(
            ConvNormAct(channels * 3, channels, kernel_size=1),
            nn.Conv2d(channels, channels, kernel_size=1),
            nn.Sigmoid(),
        )
        self.fuse = nn.Sequential(
            ConvNormAct(channels * 3, channels, kernel_size=1),
            ResidualBlock(channels, channels),
        )

    def forward(self, center: Tensor, change: Tensor) -> Tensor:
        center_evidence = self.center_project(center)
        change_evidence = self.change_project(change)
        agreement = self.gate(torch.cat((center_evidence, change_evidence, torch.abs(center_evidence - change_evidence)), dim=1))
        supported_change = _bounded(agreement * change_evidence)
        return self.fuse(torch.cat((center_evidence, supported_change, torch.abs(center_evidence - supported_change)), dim=1))


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


class OrientationLineSupport(nn.Module):
    """Differentiable orientation-aware line evidence for one fused skip scale."""

    def __init__(self, channels: int) -> None:
        super().__init__()
        self.local = ResidualBlock(channels, channels)
        self.horizontal = nn.Sequential(
            nn.Conv2d(channels, channels, kernel_size=(1, 11), padding=(0, 5), groups=channels, bias=False),
            nn.GroupNorm(_group_count(channels), channels),
            nn.GELU(),
            nn.Conv2d(channels, channels, kernel_size=1, bias=False),
        )
        self.vertical = nn.Sequential(
            nn.Conv2d(channels, channels, kernel_size=(11, 1), padding=(5, 0), groups=channels, bias=False),
            nn.GroupNorm(_group_count(channels), channels),
            nn.GELU(),
            nn.Conv2d(channels, channels, kernel_size=1, bias=False),
        )
        self.diagonal_near = ConvNormAct(channels, channels, dilation=2)
        self.diagonal_wide = ConvNormAct(channels, channels, dilation=4)
        self.project = nn.Sequential(ConvNormAct(channels * 5, channels, kernel_size=1), ResidualBlock(channels, channels))

    def forward(self, inputs: Tensor) -> Tensor:
        local = self.local(inputs)
        horizontal = _bounded(self.horizontal(local))
        vertical = _bounded(self.vertical(local))
        diagonal_near = self.diagonal_near(local)
        diagonal_wide = self.diagonal_wide(local)
        return self.project(torch.cat((local, horizontal, vertical, diagonal_near, diagonal_wide), dim=1))


class AgreementLineSupportGate(nn.Module):
    """Inject line support into fused skips under decoder/context agreement."""

    def __init__(self, skip_channels: int, context_channels: int) -> None:
        super().__init__()
        self.line_support = OrientationLineSupport(skip_channels)
        self.context_project = ConvNormAct(context_channels, skip_channels, kernel_size=1)
        self.gate = nn.Sequential(
            ConvNormAct(skip_channels * 3, skip_channels, kernel_size=1),
            nn.Conv2d(skip_channels, skip_channels, kernel_size=1),
            nn.Sigmoid(),
        )
        self.support_refine = ResidualBlock(skip_channels, skip_channels)

    def forward(self, skip: Tensor, context: Tensor) -> Tensor:
        context_up = F.interpolate(context, size=skip.shape[-2:], mode="bilinear", align_corners=False)
        context_embed = self.context_project(context_up)
        line = self.line_support(skip)
        gate = self.gate(torch.cat((skip, line, context_embed), dim=1))
        support = self.support_refine(_bounded(line + context_embed))
        return _bounded(skip + 0.45 * gate * support)


class DecoderFuse(nn.Module):
    """Upsample and merge decoder features with one skip scale."""

    def __init__(self, in_channels: int, skip_channels: int, out_channels: int) -> None:
        super().__init__()
        self.input_project = ConvNormAct(in_channels, out_channels, kernel_size=1)
        self.skip_project = ConvNormAct(skip_channels, out_channels, kernel_size=1)
        self.fuse = nn.Sequential(ConvNormAct(out_channels * 2, out_channels), ResidualBlock(out_channels, out_channels))

    def forward(self, inputs: Tensor, skip: Tensor) -> Tensor:
        upsampled = F.interpolate(inputs, size=skip.shape[-2:], mode="bilinear", align_corners=False)
        return self.fuse(torch.cat((self.input_project(upsampled), self.skip_project(skip)), dim=1))


class BoundedAgreementLogitHead(nn.Module):
    """Fuse compact and recall logits through a bounded learned agreement residual."""

    def __init__(self, channels: int) -> None:
        super().__init__()
        self.compact_head = nn.Conv2d(channels, 1, kernel_size=1)
        self.recall_head = nn.Conv2d(channels, 1, kernel_size=1)
        self.agreement_gate = nn.Sequential(
            ConvNormAct(channels, channels, kernel_size=1),
            nn.Conv2d(channels, 1, kernel_size=1),
            nn.Sigmoid(),
        )

    def forward(self, features: Tensor) -> Tensor:
        compact = self.compact_head(features)
        recall_residual = torch.tanh(self.recall_head(features))
        gate = self.agreement_gate(features)
        return _bounded(compact + 0.6 * gate * recall_residual)


class TemporalDualEvidenceLineAgreementUNet(nn.Module):
    """Dual-evidence temporal U-Net with agreement-gated line-supported decoder skips."""

    def __init__(self) -> None:
        super().__init__()
        base = 20
        self.temporal_features = TemporalFrameFeatureBuilder()
        self.stem = TemporalDualEvidenceStem(self.temporal_features.out_channels, base)
        self.center_encoder = SingleStreamEncoder(base)
        self.change_encoder = SingleStreamEncoder(base)
        self.fuse0 = EvidenceAgreementFuse(base)
        self.fuse1 = EvidenceAgreementFuse(base * 2)
        self.fuse2 = EvidenceAgreementFuse(base * 4)
        self.fuse3 = EvidenceAgreementFuse(base * 8)
        self.context = ASPPContext(base * 8)
        self.support2 = AgreementLineSupportGate(base * 4, base * 8)
        self.support1 = AgreementLineSupportGate(base * 2, base * 4)
        self.support0 = AgreementLineSupportGate(base, base * 2)
        self.up2 = DecoderFuse(base * 8, base * 4, base * 4)
        self.up1 = DecoderFuse(base * 4, base * 2, base * 2)
        self.up0 = DecoderFuse(base * 2, base, base)
        self.refine = nn.Sequential(
            ConvNormAct(base * 2, base),
            ResidualBlock(base, base),
            ResidualBlock(base, base),
        )
        self.mask_head = BoundedAgreementLogitHead(base)
        self.line_head = nn.Conv2d(base, 1, kernel_size=1)
        self.centerline_head = nn.Conv2d(base, 1, kernel_size=1)

    def forward(self, inputs: Tensor) -> dict[str, Tensor]:
        previous, center, next_frame = self.temporal_features(inputs)
        center_stem, change_stem = self.stem(previous, center, next_frame)
        center_scales = self.center_encoder(center_stem)
        change_scales = self.change_encoder(change_stem)
        scale0 = self.fuse0(center_scales[0], change_scales[0])
        scale1 = self.fuse1(center_scales[1], change_scales[1])
        scale2 = self.fuse2(center_scales[2], change_scales[2])
        scale3 = self.fuse3(center_scales[3], change_scales[3])
        context = self.context(scale3)
        scale2_supported = self.support2(scale2, context)
        dec2 = self.up2(context, scale2_supported)
        scale1_supported = self.support1(scale1, dec2)
        dec1 = self.up1(dec2, scale1_supported)
        scale0_supported = self.support0(scale0, dec1)
        dec0 = self.up0(dec1, scale0_supported)
        refined = self.refine(torch.cat((dec0, scale0_supported), dim=1))
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
    return TemporalDualEvidenceLineAgreementUNet()
