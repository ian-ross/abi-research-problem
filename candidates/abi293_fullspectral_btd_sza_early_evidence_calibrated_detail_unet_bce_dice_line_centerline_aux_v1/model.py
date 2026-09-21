"""Full-spectral BTD+SZA U-Net with early evidence-calibrated detail support."""

from __future__ import annotations

import torch
import torch.nn.functional as F
from torch import Tensor, nn


CANDIDATE_ID = "abi293_fullspectral_btd_sza_early_evidence_calibrated_detail_unet_bce_dice_line_centerline_aux_v1"


def _finite(inputs: Tensor, *, limit: float, nan: float = 0.0) -> Tensor:
    """Bound candidate-visible derived features to keep scouts numerically conservative."""

    return torch.nan_to_num(inputs, nan=nan, posinf=limit, neginf=-limit).clamp(-limit, limit)


class NormalizedBTDSZAFrontEnd(nn.Module):
    """Build normalized ABI, approved-channel BTD, Solar Geometry Input, and learned features."""

    _CHANNEL_MEANS = (
        0.1572, 0.1281, 0.1566, 0.0268, 0.0883, 0.0753,
        279.45, 233.17, 241.06, 248.44, 267.58, 250.28, 269.32, 268.23, 265.94, 255.61,
    )
    _CHANNEL_SCALES = (
        0.36, 0.34, 0.36, 0.16, 0.23, 0.18,
        42.0, 20.0, 25.0, 29.0, 43.0, 28.0, 44.0, 44.0, 43.0, 35.0,
    )
    _BTD_PAIRS = ((12, 13), (13, 14), (12, 14), (10, 13), (6, 13), (7, 9), (7, 12), (8, 13))
    _BTD_SCALE = 20.0

    def __init__(self, learned_channels: int = 16) -> None:
        super().__init__()
        self.register_buffer("channel_means", torch.tensor(self._CHANNEL_MEANS, dtype=torch.float32).view(1, 16, 1, 1))
        self.register_buffer("channel_scales", torch.tensor(self._CHANNEL_SCALES, dtype=torch.float32).view(1, 16, 1, 1))
        self.learned_mixer = nn.Sequential(nn.Conv2d(17, learned_channels, kernel_size=1), nn.GELU())
        self.out_channels = 16 + len(self._BTD_PAIRS) + 2 + learned_channels

    def forward(self, inputs: Tensor) -> Tensor:
        if inputs.ndim != 4 or inputs.shape[1] != 17:
            raise ValueError(f"expected [N, 17, H, W] ABI+SZA tensor, got {tuple(inputs.shape)}")
        abi = inputs[:, :16]
        sza = torch.nan_to_num(inputs[:, 16:17], nan=90.0, posinf=180.0, neginf=0.0).clamp(0.0, 180.0)
        normalized = _finite((abi - self.channel_means) / self.channel_scales, limit=6.0)
        btd = _finite(torch.cat([(abi[:, a : a + 1] - abi[:, b : b + 1]) / self._BTD_SCALE for a, b in self._BTD_PAIRS], dim=1), limit=6.0)
        sza_scaled = (sza - 90.0) / 90.0
        sza_cosine = torch.cos(torch.deg2rad(sza))
        learned = self.learned_mixer(torch.cat((normalized, sza_scaled), dim=1))
        return torch.cat((normalized, btd, sza_scaled, sza_cosine, learned), dim=1)


def _group_count(channels: int) -> int:
    for groups in (8, 6, 5, 4, 3, 2, 1):
        if channels % groups == 0:
            return groups
    return 1


def _smooth(inputs: Tensor, kernel_size: int) -> Tensor:
    return F.avg_pool2d(inputs, kernel_size=kernel_size, stride=1, padding=kernel_size // 2, count_include_pad=False)


def _bounded(inputs: Tensor, *, limit: float = 12.0) -> Tensor:
    return torch.clamp(inputs, min=-limit, max=limit)


class ConvNormAct(nn.Module):
    def __init__(self, in_channels: int, out_channels: int, *, kernel_size: int = 3, dilation: int = 1) -> None:
        super().__init__()
        padding = dilation * (kernel_size // 2)
        self.block = nn.Sequential(
            nn.Conv2d(in_channels, out_channels, kernel_size, padding=padding, dilation=dilation, bias=False),
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


class SignedDetailContextStem(nn.Module):
    """Separate signed local detail from broad context as architecture-internal evidence."""

    def __init__(self, in_channels: int, out_channels: int) -> None:
        super().__init__()
        self.raw = ConvNormAct(in_channels, out_channels, kernel_size=1)
        self.local_pos = ConvNormAct(in_channels, out_channels, kernel_size=1)
        self.local_neg = ConvNormAct(in_channels, out_channels, kernel_size=1)
        self.context = ConvNormAct(in_channels, out_channels, kernel_size=1)
        self.fuse = nn.Sequential(ConvNormAct(out_channels * 4, out_channels), ResidualBlock(out_channels, out_channels))

    def forward(self, inputs: Tensor) -> Tensor:
        detail = inputs - _smooth(inputs, 7)
        broad = _smooth(inputs, 31)
        return self.fuse(torch.cat((self.raw(inputs), self.local_pos(F.relu(detail)), self.local_neg(F.relu(-detail)), self.context(broad)), dim=1))


class SeparableLineContext(nn.Module):
    """Horizontal/vertical separable context for thin-line evidence, used as model features only."""

    def __init__(self, channels: int) -> None:
        super().__init__()
        self.horizontal = nn.Sequential(
            nn.Conv2d(channels, channels, kernel_size=(1, 15), padding=(0, 7), groups=channels, bias=False),
            nn.Conv2d(channels, channels, kernel_size=1, bias=False),
            nn.GroupNorm(_group_count(channels), channels),
            nn.GELU(),
        )
        self.vertical = nn.Sequential(
            nn.Conv2d(channels, channels, kernel_size=(15, 1), padding=(7, 0), groups=channels, bias=False),
            nn.Conv2d(channels, channels, kernel_size=1, bias=False),
            nn.GroupNorm(_group_count(channels), channels),
            nn.GELU(),
        )
        self.project = nn.Sequential(ConvNormAct(channels * 3, channels, kernel_size=1), ResidualBlock(channels, channels))

    def forward(self, inputs: Tensor) -> Tensor:
        return self.project(torch.cat((inputs, self.horizontal(inputs), self.vertical(inputs)), dim=1))


class EvidenceCalibrationBlock(nn.Module):
    """Inject bounded clean detail/line evidence into skip features before decoding."""

    def __init__(self, channels: int) -> None:
        super().__init__()
        self.local = ResidualBlock(channels, channels)
        self.broad = ConvNormAct(channels, channels, dilation=2)
        self.line_context = SeparableLineContext(channels)
        self.detail_project = ConvNormAct(channels * 3, channels, kernel_size=1)
        self.reliability = nn.Sequential(
            ConvNormAct(channels * 4, channels, kernel_size=1),
            nn.Conv2d(channels, channels, kernel_size=1),
            nn.Sigmoid(),
        )
        self.clutter = nn.Sequential(
            ConvNormAct(channels * 3, channels, kernel_size=1),
            nn.Conv2d(channels, channels, kernel_size=1),
            nn.Sigmoid(),
        )

    def forward(self, inputs: Tensor) -> Tensor:
        local = self.local(inputs)
        broad = self.broad(_smooth(inputs, 15))
        detail = inputs - _smooth(inputs, 5)
        line = self.line_context(local)
        reliability = self.reliability(torch.cat((local, broad, line, torch.abs(detail)), dim=1))
        clutter = self.clutter(torch.cat((torch.abs(local - broad), torch.abs(detail), line), dim=1))
        support = self.detail_project(torch.cat((F.relu(detail), line, local), dim=1))
        calibrated = inputs + 0.18 * reliability * torch.tanh(support) - 0.06 * (1.0 - reliability) * clutter * torch.tanh(torch.abs(support))
        return _bounded(calibrated)


class EncoderDown(nn.Module):
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


class DecoderFuse(nn.Module):
    def __init__(self, in_channels: int, skip_channels: int, out_channels: int) -> None:
        super().__init__()
        self.input_project = ConvNormAct(in_channels, out_channels, kernel_size=1)
        self.skip_project = ConvNormAct(skip_channels, out_channels, kernel_size=1)
        self.fuse = nn.Sequential(ConvNormAct(out_channels * 2, out_channels), ResidualBlock(out_channels, out_channels))

    def forward(self, inputs: Tensor, skip: Tensor) -> Tensor:
        upsampled = F.interpolate(inputs, size=skip.shape[-2:], mode="bilinear", align_corners=False)
        return self.fuse(torch.cat((self.input_project(upsampled), self.skip_project(skip)), dim=1))


class CalibratedEvidenceHead(nn.Module):
    """Combine region logits with bounded reliability-gated detail and line evidence."""

    def __init__(self, channels: int) -> None:
        super().__init__()
        self.line_context = SeparableLineContext(channels)
        self.region_refine = nn.Sequential(ConvNormAct(channels * 2, channels), ResidualBlock(channels, channels))
        self.detail_refine = nn.Sequential(ConvNormAct(channels * 3, channels), ResidualBlock(channels, channels))
        self.support_refine = nn.Sequential(ConvNormAct(channels * 4, channels), ResidualBlock(channels, channels))
        self.gate = nn.Sequential(
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
        self.clutter_head = nn.Conv2d(channels, 1, kernel_size=1)
        self.centerline_head = nn.Conv2d(channels, 1, kernel_size=1)

    def forward(self, features: Tensor, support1: Tensor, support2: Tensor, support3: Tensor) -> dict[str, Tensor]:
        line_context = self.line_context(features)
        region_features = self.region_refine(torch.cat((features, line_context), dim=1))
        signed_detail = features - _smooth(features, 5)
        detail_features = self.detail_refine(torch.cat((features, line_context, signed_detail), dim=1))
        multiscale = self.support_refine(torch.cat((line_context, support1, support2, support3), dim=1))
        support_mean = (support1 + support2 + support3) / 3.0
        disagreement = torch.abs(line_context - support_mean)
        gate = self.gate(torch.cat((features, line_context, region_features, detail_features, multiscale), dim=1))
        clutter = self.clutter_gate(torch.cat((region_features, detail_features, disagreement, torch.abs(signed_detail)), dim=1))
        region_logits = self.region_head(region_features)
        line_logits = self.line_head(line_context)
        detail_logits = self.detail_head(detail_features)
        support_logits = self.support_head(multiscale)
        clutter_logits = self.clutter_head(disagreement)
        uncertainty_band = torch.sigmoid(-0.55 * torch.abs(region_logits))
        recall_support = (
            0.10 * gate * torch.tanh(line_logits)
            + 0.08 * gate * torch.tanh(support_logits)
            + 0.10 * uncertainty_band * gate * (1.0 - clutter) * torch.tanh(detail_logits)
        )
        clutter_veto = 0.07 * (1.0 - gate) * clutter * torch.sigmoid(clutter_logits)
        mask_logits = region_logits + recall_support - clutter_veto
        return {
            "mask_logits": _bounded(mask_logits),
            "line_logits": line_logits + 0.25 * support_logits,
            "centerline_logits": self.centerline_head(detail_features),
        }


class EarlyEvidenceCalibratedDetailUNet(nn.Module):
    def __init__(self) -> None:
        super().__init__()
        self.front_end = NormalizedBTDSZAFrontEnd(learned_channels=16)
        base = 40
        self.stem = SignedDetailContextStem(self.front_end.out_channels, base)
        self.enc0 = ResidualBlock(base, base)
        self.cal0 = EvidenceCalibrationBlock(base)
        self.enc1 = EncoderDown(base, base * 2)
        self.cal1 = EvidenceCalibrationBlock(base * 2)
        self.enc2 = EncoderDown(base * 2, base * 4)
        self.cal2 = EvidenceCalibrationBlock(base * 4)
        self.enc3 = EncoderDown(base * 4, base * 8)
        self.context = ASPPContext(base * 8, base * 8)
        self.up2 = DecoderFuse(base * 8, base * 4, base * 4)
        self.up1 = DecoderFuse(base * 4, base * 2, base * 2)
        self.up0 = DecoderFuse(base * 2, base, base)
        self.highres_detail = SignedDetailContextStem(self.front_end.out_channels, base)
        self.highres_cal = EvidenceCalibrationBlock(base)
        self.final_project = nn.Sequential(ConvNormAct(base * 3, base), ResidualBlock(base, base))
        self.support_dec1 = ConvNormAct(base * 2, base, kernel_size=1)
        self.support_dec2 = ConvNormAct(base * 4, base, kernel_size=1)
        self.support_context = ConvNormAct(base * 8, base, kernel_size=1)
        self.head = CalibratedEvidenceHead(base)

    def forward(self, inputs: Tensor) -> dict[str, Tensor]:
        features = self.front_end(inputs)
        stem = self.stem(features)
        enc0 = self.cal0(self.enc0(stem))
        enc1 = self.cal1(self.enc1(enc0))
        enc2 = self.cal2(self.enc2(enc1))
        enc3 = self.enc3(enc2)
        context = self.context(enc3)
        dec2 = self.up2(context, enc2)
        dec1 = self.up1(dec2, enc1)
        dec0 = self.up0(dec1, enc0)
        detail = self.highres_cal(self.highres_detail(features))
        fullres = self.final_project(torch.cat((dec0, detail, stem), dim=1))
        support_size = fullres.shape[-2:]
        support1 = F.interpolate(self.support_dec1(dec1), size=support_size, mode="bilinear", align_corners=False)
        support2 = F.interpolate(self.support_dec2(dec2), size=support_size, mode="bilinear", align_corners=False)
        support3 = F.interpolate(self.support_context(context), size=support_size, mode="bilinear", align_corners=False)
        return self.head(fullres, support1, support2, support3)


def _validate_auxiliary_outputs(output_spec: dict[str, object]) -> None:
    expected = [
        {"target": "line", "name": "line_logits", "shape": [1, 256, 256]},
        {"target": "centerline", "name": "centerline_logits", "shape": [1, 256, 256]},
    ]
    if output_spec.get("auxiliary_outputs") != expected:
        raise ValueError(f"{CANDIDATE_ID} requires trusted line_logits and centerline_logits auxiliary outputs")


def build_model(input_spec: dict[str, object], output_spec: dict[str, object]) -> nn.Module:
    """Build the model for the Harness-supplied ABI contract."""

    if input_spec.get("mode") != "abi_16ch_plus_sza" or input_spec.get("shape") != [17, 256, 256]:
        raise ValueError(f"{CANDIDATE_ID} requires abi_16ch_plus_sza [17, 256, 256] input")
    if output_spec.get("form") != "mask_logits" or output_spec.get("shape") != [1, 256, 256]:
        raise ValueError(f"{CANDIDATE_ID} requires mask_logits [1, 256, 256] primary output")
    _validate_auxiliary_outputs(output_spec)
    return EarlyEvidenceCalibratedDetailUNet()
