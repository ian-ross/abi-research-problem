"""Temporal local-correlation center-detail U-Net for provider-owned ABI+SZA clips."""

from __future__ import annotations

import math

import torch
import torch.nn.functional as F
from torch import Tensor, nn


CANDIDATE_ID = "abi296_temporal_local_correlation_center_detail_unet_bce_dice_line_centerline_aux_v1"
TEMPORAL_OFFSETS = [-1, 0, 1]
CHANNELS_PER_FRAME = 17
FRAME_COUNT = 3
INPUT_CHANNELS = CHANNELS_PER_FRAME * FRAME_COUNT


def _finite_feature(inputs: Tensor, *, limit: float, nan: float = 0.0) -> Tensor:
    """Map non-finite candidate-visible feature values to bounded neutral values."""

    return torch.nan_to_num(inputs, nan=nan, posinf=limit, neginf=-limit).clamp(-limit, limit)


def _bounded(inputs: Tensor, *, limit: float = 12.0) -> Tensor:
    """Bound internal activations without hiding non-finite parameter failures."""

    return torch.clamp(inputs, min=-limit, max=limit)


def _smooth(inputs: Tensor, kernel_size: int) -> Tensor:
    return F.avg_pool2d(inputs, kernel_size=kernel_size, stride=1, padding=kernel_size // 2, count_include_pad=False)


def _group_count(channels: int) -> int:
    for groups in (8, 6, 4, 3, 2, 1):
        if channels % groups == 0:
            return groups
    return 1


class TemporalFrameFeatureBuilder(nn.Module):
    """Build finite per-frame ABI+BTD+Solar Geometry Input features."""

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
    # Zero-based ABI channel indices inside each candidate-visible frame.
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
        abi = frame[:, :16]
        sza = frame[:, 16:17]
        normalized = _finite_feature((abi - self.abi_means) / self.abi_scales, limit=6.0)
        btd = _finite_feature(
            torch.cat([(abi[:, a : a + 1] - abi[:, b : b + 1]) / self._BTD_SCALE for a, b in self._BTD_PAIRS], dim=1),
            limit=6.0,
        )
        sza_finite = torch.nan_to_num(sza, nan=90.0, posinf=180.0, neginf=0.0).clamp(0.0, 180.0)
        sza_scaled = (sza_finite - 90.0) / 90.0
        sza_cosine = torch.cos(torch.deg2rad(sza_finite))
        return torch.cat((normalized, btd, sza_scaled, sza_cosine), dim=1)

    def forward(self, inputs: Tensor) -> tuple[Tensor, Tensor, Tensor]:
        if inputs.ndim != 4 or inputs.shape[1] != INPUT_CHANNELS:
            raise ValueError(f"expected [N, {INPUT_CHANNELS}, H, W] temporal ABI+SZA tensor, got {tuple(inputs.shape)}")
        batch, _, height, width = inputs.shape
        frames = inputs.reshape(batch, FRAME_COUNT, CHANNELS_PER_FRAME, height, width)
        previous = self.forward_frame(frames[:, 0])
        center = self.forward_frame(frames[:, 1])
        next_frame = self.forward_frame(frames[:, 2])
        return previous, center, next_frame


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


class SharedFrameStem(nn.Module):
    """Encode each temporal frame with identical weights to avoid source/time shortcuts."""

    def __init__(self, in_channels: int, out_channels: int) -> None:
        super().__init__()
        self.project = nn.Sequential(
            ConvNormAct(in_channels, out_channels, kernel_size=1),
            ResidualBlock(out_channels, out_channels),
        )

    def forward(self, frame_features: Tensor) -> Tensor:
        return self.project(frame_features)


class LocalCorrelationFuse(nn.Module):
    """Small-displacement differentiable matching for previous/next temporal evidence."""

    def __init__(self, channels: int, key_channels: int = 16) -> None:
        super().__init__()
        self.center_key = nn.Conv2d(channels, key_channels, kernel_size=1, bias=False)
        self.neighbor_key = nn.Conv2d(channels, key_channels, kernel_size=1, bias=False)
        self.corr_project = nn.Sequential(
            ConvNormAct(18, channels, kernel_size=1),
            ResidualBlock(channels, channels),
        )
        self.change_project = nn.Sequential(
            ConvNormAct(channels * 4, channels, kernel_size=1),
            ResidualBlock(channels, channels),
        )
        self.reliability = nn.Sequential(
            ConvNormAct(channels * 4, channels, kernel_size=1),
            nn.Conv2d(channels, channels, kernel_size=1),
            nn.Sigmoid(),
        )
        self.fuse = nn.Sequential(
            ConvNormAct(channels * 4, channels, kernel_size=1),
            ResidualBlock(channels, channels),
            ResidualBlock(channels, channels),
        )
        self.scale = 1.0 / math.sqrt(float(key_channels))

    def _local_correlation(self, center: Tensor, neighbor: Tensor) -> Tensor:
        n, _, h, w = center.shape
        center_key = F.normalize(self.center_key(center), dim=1, eps=1.0e-4)
        neighbor_key = F.normalize(self.neighbor_key(neighbor), dim=1, eps=1.0e-4)
        patches = F.unfold(neighbor_key, kernel_size=3, padding=1).view(n, center_key.shape[1], 9, h, w)
        corr = (center_key.unsqueeze(2) * patches).sum(dim=1) * self.scale
        return _bounded(corr, limit=4.0)

    def forward(self, previous: Tensor, center: Tensor, next_frame: Tensor) -> Tensor:
        prev_corr = self._local_correlation(center, previous)
        next_corr = self._local_correlation(center, next_frame)
        corr_features = self.corr_project(torch.cat((prev_corr, next_corr), dim=1))
        previous_delta = center - previous
        next_delta = center - next_frame
        symmetric_delta = previous - next_frame
        change_features = self.change_project(
            torch.cat((previous_delta, next_delta, torch.abs(previous_delta) + torch.abs(next_delta), symmetric_delta), dim=1)
        )
        reliability = self.reliability(torch.cat((center, corr_features, change_features, torch.abs(previous_delta) + torch.abs(next_delta)), dim=1))
        support = reliability * corr_features + (1.0 - reliability) * center
        return self.fuse(torch.cat((center, support, change_features, corr_features), dim=1))


class DirectionalLineContext(nn.Module):
    """Resource-bounded horizontal/vertical/diagonal context for connected thin lines."""

    def __init__(self, channels: int) -> None:
        super().__init__()
        self.horizontal = nn.Sequential(
            nn.Conv2d(channels, channels, kernel_size=(1, 13), padding=(0, 6), groups=channels, bias=False),
            nn.Conv2d(channels, channels, kernel_size=1, bias=False),
            nn.GroupNorm(_group_count(channels), channels),
            nn.GELU(),
        )
        self.vertical = nn.Sequential(
            nn.Conv2d(channels, channels, kernel_size=(13, 1), padding=(6, 0), groups=channels, bias=False),
            nn.Conv2d(channels, channels, kernel_size=1, bias=False),
            nn.GroupNorm(_group_count(channels), channels),
            nn.GELU(),
        )
        self.diagonal = nn.Sequential(
            nn.Conv2d(channels, channels, kernel_size=3, padding=2, dilation=2, groups=channels, bias=False),
            nn.Conv2d(channels, channels, kernel_size=1, bias=False),
            nn.GroupNorm(_group_count(channels), channels),
            nn.GELU(),
        )
        self.project = nn.Sequential(ConvNormAct(channels * 4, channels, kernel_size=1), ResidualBlock(channels, channels))

    def forward(self, inputs: Tensor) -> Tensor:
        return self.project(torch.cat((inputs, self.horizontal(inputs), self.vertical(inputs), self.diagonal(inputs)), dim=1))


class CenterDetailStem(nn.Module):
    """Preserve signed center-frame local detail independent of neighbor support."""

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


class DownBlock(nn.Module):
    def __init__(self, in_channels: int, out_channels: int) -> None:
        super().__init__()
        self.block = nn.Sequential(nn.MaxPool2d(2), ResidualBlock(in_channels, out_channels), ResidualBlock(out_channels, out_channels))

    def forward(self, inputs: Tensor) -> Tensor:
        return self.block(inputs)


class ASPPContext(nn.Module):
    def __init__(self, in_channels: int, out_channels: int) -> None:
        super().__init__()
        branch = out_channels // 4
        self.branch1 = ConvNormAct(in_channels, branch, kernel_size=1)
        self.branch2 = ConvNormAct(in_channels, branch, dilation=2)
        self.branch4 = ConvNormAct(in_channels, branch, dilation=4)
        self.branch8 = ConvNormAct(in_channels, branch, dilation=8)
        self.project = nn.Sequential(ConvNormAct(branch * 4, out_channels, kernel_size=1), ResidualBlock(out_channels, out_channels))

    def forward(self, inputs: Tensor) -> Tensor:
        return self.project(torch.cat((self.branch1(inputs), self.branch2(inputs), self.branch4(inputs), self.branch8(inputs)), dim=1))


class UpFuse(nn.Module):
    def __init__(self, in_channels: int, skip_channels: int, out_channels: int) -> None:
        super().__init__()
        self.input_project = ConvNormAct(in_channels, out_channels, kernel_size=1)
        self.skip_project = ConvNormAct(skip_channels, out_channels, kernel_size=1)
        self.fuse = nn.Sequential(ConvNormAct(out_channels * 2, out_channels), ResidualBlock(out_channels, out_channels))

    def forward(self, inputs: Tensor, skip: Tensor) -> Tensor:
        upsampled = F.interpolate(inputs, size=skip.shape[-2:], mode="bilinear", align_corners=False)
        return self.fuse(torch.cat((self.input_project(upsampled), self.skip_project(skip)), dim=1))


class LocalCorrelationEvidenceHead(nn.Module):
    """Bounded architecture-internal logit support from center detail and temporal correlation."""

    def __init__(self, channels: int) -> None:
        super().__init__()
        self.line_context = DirectionalLineContext(channels)
        self.region_refine = nn.Sequential(ConvNormAct(channels * 2, channels), ResidualBlock(channels, channels))
        self.detail_refine = nn.Sequential(ConvNormAct(channels * 3, channels), ResidualBlock(channels, channels))
        self.support_refine = nn.Sequential(ConvNormAct(channels * 4, channels), ResidualBlock(channels, channels))
        self.support_gate = nn.Sequential(
            ConvNormAct(channels * 5, channels, kernel_size=1),
            nn.Conv2d(channels, 1, kernel_size=1),
            nn.Sigmoid(),
        )
        self.clutter_gate = nn.Sequential(
            ConvNormAct(channels * 4, channels, kernel_size=1),
            nn.Conv2d(channels, 1, kernel_size=1),
            nn.Sigmoid(),
        )
        self.region_head = nn.Conv2d(channels, 1, kernel_size=1)
        self.line_head = nn.Conv2d(channels, 1, kernel_size=1)
        self.detail_head = nn.Conv2d(channels, 1, kernel_size=1)
        self.support_head = nn.Conv2d(channels, 1, kernel_size=1)
        self.centerline_head = nn.Conv2d(channels, 1, kernel_size=1)

    def forward(self, features: Tensor, temporal_support: Tensor, support1: Tensor, support2: Tensor) -> dict[str, Tensor]:
        line_features = self.line_context(features)
        region_features = self.region_refine(torch.cat((features, temporal_support), dim=1))
        signed_detail = features - _smooth(features, 5)
        detail_features = self.detail_refine(torch.cat((features, line_features, signed_detail), dim=1))
        multiscale_support = self.support_refine(torch.cat((temporal_support, line_features, support1, support2), dim=1))
        disagreement = torch.abs(region_features - multiscale_support)
        gate = self.support_gate(torch.cat((features, line_features, region_features, detail_features, multiscale_support), dim=1))
        clutter = self.clutter_gate(torch.cat((disagreement, torch.abs(signed_detail), temporal_support, line_features), dim=1))
        region_logits = self.region_head(region_features)
        line_logits = self.line_head(line_features)
        detail_logits = self.detail_head(detail_features)
        support_logits = self.support_head(multiscale_support)
        uncertainty_band = torch.sigmoid(-0.55 * torch.abs(region_logits))
        recall_support = (
            0.10 * gate * torch.tanh(support_logits)
            + 0.08 * gate * torch.tanh(line_logits)
            + 0.08 * uncertainty_band * gate * (1.0 - clutter) * torch.tanh(detail_logits)
        )
        compact_veto = 0.05 * (1.0 - gate) * clutter * torch.sigmoid(disagreement.mean(dim=1, keepdim=True))
        mask_logits = region_logits + recall_support - compact_veto
        return {
            "mask_logits": _bounded(mask_logits),
            "line_logits": _bounded(line_logits + 0.20 * support_logits),
            "centerline_logits": _bounded(self.centerline_head(detail_features)),
        }


class TemporalLocalCorrelationCenterDetailUNet(nn.Module):
    def __init__(self) -> None:
        super().__init__()
        base = 32
        self.frame_builder = TemporalFrameFeatureBuilder()
        self.frame_stem = SharedFrameStem(self.frame_builder.out_channels, base)
        self.local_correlation = LocalCorrelationFuse(base, key_channels=16)
        self.center_detail = CenterDetailStem(self.frame_builder.out_channels, base)
        self.enc0 = nn.Sequential(ResidualBlock(base * 2, base), ResidualBlock(base, base))
        self.line0 = DirectionalLineContext(base)
        self.enc1 = DownBlock(base, base * 2)
        self.enc2 = DownBlock(base * 2, base * 4)
        self.enc3 = DownBlock(base * 4, base * 8)
        self.context = ASPPContext(base * 8, base * 8)
        self.up2 = UpFuse(base * 8, base * 4, base * 4)
        self.up1 = UpFuse(base * 4, base * 2, base * 2)
        self.up0 = UpFuse(base * 2, base, base)
        self.temporal_support_project = ConvNormAct(base, base, kernel_size=1)
        self.support1_project = ConvNormAct(base * 2, base, kernel_size=1)
        self.support2_project = ConvNormAct(base * 4, base, kernel_size=1)
        self.final_project = nn.Sequential(ConvNormAct(base * 3, base), ResidualBlock(base, base))
        self.head = LocalCorrelationEvidenceHead(base)

    def forward(self, inputs: Tensor) -> dict[str, Tensor]:
        previous_features, center_features, next_features = self.frame_builder(inputs)
        previous = self.frame_stem(previous_features)
        center = self.frame_stem(center_features)
        next_frame = self.frame_stem(next_features)
        temporal = self.local_correlation(previous, center, next_frame)
        center_detail = self.center_detail(center_features)
        enc0 = self.line0(self.enc0(torch.cat((temporal, center_detail), dim=1)))
        enc1 = self.enc1(enc0)
        enc2 = self.enc2(enc1)
        enc3 = self.enc3(enc2)
        context = self.context(enc3)
        dec2 = self.up2(context, enc2)
        dec1 = self.up1(dec2, enc1)
        dec0 = self.up0(dec1, enc0)
        temporal_support = self.temporal_support_project(temporal)
        fullres = self.final_project(torch.cat((dec0, center_detail, temporal_support), dim=1))
        support_size = fullres.shape[-2:]
        support1 = F.interpolate(self.support1_project(dec1), size=support_size, mode="bilinear", align_corners=False)
        support2 = F.interpolate(self.support2_project(dec2), size=support_size, mode="bilinear", align_corners=False)
        return self.head(fullres, temporal_support, support1, support2)


def _validate_auxiliary_outputs(output_spec: dict[str, object]) -> None:
    expected = [
        {"target": "line", "name": "line_logits", "shape": [1, 256, 256]},
        {"target": "centerline", "name": "centerline_logits", "shape": [1, 256, 256]},
    ]
    if output_spec.get("auxiliary_outputs") != expected:
        raise ValueError(f"{CANDIDATE_ID} requires trusted line_logits and centerline_logits auxiliary outputs")


def build_model(input_spec: dict[str, object], output_spec: dict[str, object]) -> nn.Module:
    """Build the model for the Harness-supplied temporal ABI contract."""

    if input_spec.get("mode") != "abi_16ch_plus_sza_temporal" or input_spec.get("shape") != [INPUT_CHANNELS, 256, 256]:
        raise ValueError(f"{CANDIDATE_ID} requires abi_16ch_plus_sza_temporal [{INPUT_CHANNELS}, 256, 256] input")
    if output_spec.get("form") != "mask_logits" or output_spec.get("shape") != [1, 256, 256]:
        raise ValueError(f"{CANDIDATE_ID} requires mask_logits [1, 256, 256] primary output")
    _validate_auxiliary_outputs(output_spec)
    return TemporalLocalCorrelationCenterDetailUNet()
