"""Temporal persistence/detail line-gate U-Net for provider-owned -1/0/+1 ABI+SZA frames."""

from __future__ import annotations

import torch
import torch.nn.functional as F
from torch import Tensor, nn


CANDIDATE_ID = "abi332_temporal_persistence_detail_line_gate_late36_bce_dice_line_centerline_aux_v1"
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


def _smooth(inputs: Tensor, kernel_size: int) -> Tensor:
    return F.avg_pool2d(inputs, kernel_size=kernel_size, stride=1, padding=kernel_size // 2, count_include_pad=False)


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


class TemporalPersistenceDetailStem(nn.Module):
    """Fuse three frames with cheap persistence and local temporal-difference evidence."""

    def __init__(self, frame_feature_channels: int, out_channels: int) -> None:
        super().__init__()
        self.frame_project = nn.Sequential(
            ConvNormAct(frame_feature_channels, out_channels, kernel_size=1),
            ResidualBlock(out_channels, out_channels),
        )
        self.difference_project = nn.Sequential(
            ConvNormAct(frame_feature_channels * 5, out_channels, kernel_size=1),
            ResidualBlock(out_channels, out_channels),
        )
        self.persistence_gate = nn.Sequential(
            ConvNormAct(out_channels * 4, out_channels, kernel_size=1),
            nn.Conv2d(out_channels, out_channels, kernel_size=1),
            nn.Sigmoid(),
        )
        self.transient_guard = nn.Sequential(
            ConvNormAct(out_channels * 3, out_channels, kernel_size=1),
            nn.Conv2d(out_channels, out_channels, kernel_size=1),
            nn.Sigmoid(),
        )
        self.fuse = nn.Sequential(
            ConvNormAct(out_channels * 4, out_channels, kernel_size=1),
            ResidualBlock(out_channels, out_channels),
            ResidualBlock(out_channels, out_channels),
        )

    def forward(self, previous: Tensor, center: Tensor, next_frame: Tensor) -> Tensor:
        previous_embed = self.frame_project(previous)
        center_embed = self.frame_project(center)
        next_embed = self.frame_project(next_frame)
        neighbor_embed = _bounded(0.5 * (previous_embed + next_embed))

        neighbor_mean = 0.5 * (previous + next_frame)
        temporal_detail = center - neighbor_mean
        difference_features = torch.cat(
            (
                _finite_feature(temporal_detail, limit=8.0),
                _finite_feature(torch.abs(center - previous), limit=8.0),
                _finite_feature(torch.abs(next_frame - center), limit=8.0),
                _finite_feature(torch.abs(next_frame - previous), limit=8.0),
                _finite_feature(torch.abs(temporal_detail) - 0.5 * torch.abs(next_frame - previous), limit=8.0),
            ),
            dim=1,
        )
        difference_embed = self.difference_project(difference_features)
        agreement = _bounded(center_embed - torch.abs(center_embed - neighbor_embed))
        gate_inputs = torch.cat((center_embed, neighbor_embed, difference_embed, agreement), dim=1)
        persistence_gate = self.persistence_gate(gate_inputs)
        transient_guard = self.transient_guard(torch.cat((torch.abs(center_embed - neighbor_embed), difference_embed, agreement), dim=1))
        persistent_center = _bounded(center_embed + persistence_gate * neighbor_embed - 0.20 * transient_guard * torch.abs(difference_embed))
        return self.fuse(torch.cat((persistent_center, center_embed, neighbor_embed, difference_embed), dim=1))


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


class CenterDetailStem(nn.Module):
    """Preserve center-frame signed local detail beside temporal attention features."""

    def __init__(self, in_channels: int, out_channels: int) -> None:
        super().__init__()
        self.raw = ConvNormAct(in_channels, out_channels, kernel_size=1)
        self.positive_detail = ConvNormAct(in_channels, out_channels, kernel_size=1)
        self.negative_detail = ConvNormAct(in_channels, out_channels, kernel_size=1)
        self.context = ConvNormAct(in_channels, out_channels, kernel_size=1)
        self.fuse = nn.Sequential(ConvNormAct(out_channels * 4, out_channels, kernel_size=1), ResidualBlock(out_channels, out_channels))

    def forward(self, center_features: Tensor) -> Tensor:
        detail = center_features - _smooth(center_features, 7)
        context = _smooth(center_features, 31)
        return self.fuse(
            torch.cat((self.raw(center_features), self.positive_detail(F.relu(detail)), self.negative_detail(F.relu(-detail)), self.context(context)), dim=1)
        )


class HighResolutionDirectionalContext(nn.Module):
    """Resource-bounded line context over final decoder evidence."""

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
        self.gate = nn.Sequential(ConvNormAct(channels * 5, channels, kernel_size=1), nn.Conv2d(channels, channels, kernel_size=1), nn.Sigmoid())
        self.project = nn.Sequential(ConvNormAct(channels * 5, channels, kernel_size=1), ResidualBlock(channels, channels))

    def forward(self, inputs: Tensor) -> Tensor:
        local = self.local(inputs)
        horizontal = _bounded(self.horizontal(local))
        vertical = _bounded(self.vertical(local))
        diagonal_near = self.diagonal_near(local)
        diagonal_wide = self.diagonal_wide(local)
        stacked = torch.cat((local, horizontal, vertical, diagonal_near, diagonal_wide), dim=1)
        return _bounded(inputs + self.gate(stacked) * self.project(stacked))


class PersistenceDetailLineGateHead(nn.Module):
    """Bounded line/detail residual head guarded by temporal persistence support.

    This is architecture-internal logit computation only.  It leaves the
    Harness threshold, losses, metrics, and Artifact Filters unchanged.
    """

    def __init__(self, channels: int) -> None:
        super().__init__()
        self.shared = nn.Sequential(ConvNormAct(channels, channels), ResidualBlock(channels, channels))
        self.line_context = HighResolutionDirectionalContext(channels)
        self.detail_project = nn.Sequential(ConvNormAct(channels, channels, kernel_size=1), ResidualBlock(channels, channels))
        self.temporal_project = nn.Sequential(ConvNormAct(channels, channels, kernel_size=1), ResidualBlock(channels, channels))
        self.mask_head = nn.Conv2d(channels, 1, kernel_size=1)
        self.line_head = nn.Conv2d(channels, 1, kernel_size=1)
        self.centerline_head = nn.Conv2d(channels, 1, kernel_size=1)
        self.detail_head = nn.Conv2d(channels, 1, kernel_size=1)
        self.temporal_support_head = nn.Conv2d(channels, 1, kernel_size=1)
        self.evidence_gate = nn.Sequential(
            ConvNormAct(channels * 4 + 5, channels, kernel_size=1),
            nn.Conv2d(channels, 1, kernel_size=1),
            nn.Sigmoid(),
        )
        self.clutter_veto = nn.Sequential(
            ConvNormAct(channels * 3 + 3, channels, kernel_size=1),
            nn.Conv2d(channels, 1, kernel_size=1),
            nn.Sigmoid(),
        )

    def forward(self, decoder_features: Tensor, center_detail: Tensor, temporal_stem: Tensor) -> dict[str, Tensor]:
        shared = self.shared(decoder_features)
        line_features = self.line_context(shared)
        detail_features = self.detail_project(center_detail)
        temporal_features = self.temporal_project(temporal_stem)
        base_mask = self.mask_head(shared)
        line_logits = self.line_head(line_features)
        centerline_logits = self.centerline_head(_bounded(0.5 * (line_features + detail_features)))
        detail_logits = self.detail_head(detail_features)
        temporal_support_logits = self.temporal_support_head(temporal_features)
        mask_probability = torch.sigmoid(base_mask)
        line_probability = torch.sigmoid(line_logits)
        centerline_probability = torch.sigmoid(centerline_logits)
        detail_probability = torch.sigmoid(detail_logits)
        support_probability = torch.sigmoid(temporal_support_logits)
        uncertainty = torch.sigmoid(-0.55 * torch.abs(base_mask))
        gate_inputs = torch.cat(
            (
                shared,
                line_features,
                detail_features,
                temporal_features,
                mask_probability,
                line_probability,
                centerline_probability,
                detail_probability,
                support_probability,
            ),
            dim=1,
        )
        evidence_gate = self.evidence_gate(gate_inputs)
        agreement = line_probability * centerline_probability * detail_probability * support_probability
        positive_evidence = torch.clamp(F.softplus(line_logits + centerline_logits + detail_logits + temporal_support_logits), max=1.20)
        positive_residual = 0.22 * evidence_gate * uncertainty * agreement * positive_evidence
        veto_inputs = torch.cat(
            (
                torch.abs(shared - line_features),
                torch.abs(shared - detail_features),
                torch.abs(shared - temporal_features),
                line_probability,
                detail_probability,
                support_probability,
            ),
            dim=1,
        )
        veto = 0.08 * self.clutter_veto(veto_inputs) * (1.0 - support_probability) * torch.sigmoid(torch.abs(base_mask))
        return {
            "mask_logits": _bounded(base_mask + positive_residual - veto),
            "line_logits": _bounded(line_logits + 0.10 * temporal_support_logits),
            "centerline_logits": _bounded(centerline_logits + 0.10 * detail_logits),
        }


class TemporalPersistenceDetailLineGateUNet(nn.Module):
    """Temporal persistence/detail U-Net with a guarded line-support head."""

    def __init__(self) -> None:
        super().__init__()
        base = 22
        self.temporal_features = TemporalFrameFeatureBuilder()
        self.temporal_stem = TemporalPersistenceDetailStem(self.temporal_features.out_channels, base)
        self.center_detail = CenterDetailStem(self.temporal_features.out_channels, base)
        self.encoder = SingleStreamEncoder(base)
        self.context = ASPPContext(base * 8)
        self.up2 = DecoderFuse(base * 8, base * 4, base * 4)
        self.up1 = DecoderFuse(base * 4, base * 2, base * 2)
        self.up0 = DecoderFuse(base * 2, base, base)
        self.refine = nn.Sequential(
            ConvNormAct(base * 3, base),
            ResidualBlock(base, base),
            ResidualBlock(base, base),
        )
        self.head = PersistenceDetailLineGateHead(base)

    def forward(self, inputs: Tensor) -> dict[str, Tensor]:
        previous, center, next_frame = self.temporal_features(inputs)
        stem = self.temporal_stem(previous, center, next_frame)
        center_detail = self.center_detail(center)
        scale0, scale1, scale2, scale3 = self.encoder(stem)
        context = self.context(scale3)
        dec2 = self.up2(context, scale2)
        dec1 = self.up1(dec2, scale1)
        dec0 = self.up0(dec1, scale0)
        refined = self.refine(torch.cat((dec0, scale0, center_detail), dim=1))
        return self.head(refined, center_detail, stem)


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
    return TemporalPersistenceDetailLineGateUNet()
