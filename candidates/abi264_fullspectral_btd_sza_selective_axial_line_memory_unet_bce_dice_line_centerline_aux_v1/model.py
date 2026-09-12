"""Selective axial line-memory U-Net for ABI+SZA contrail segmentation."""

from __future__ import annotations

import torch
import torch.nn.functional as F
from torch import Tensor, nn


CANDIDATE_ID = "abi264_fullspectral_btd_sza_selective_axial_line_memory_unet_bce_dice_line_centerline_aux_v1"


def _group_count(channels: int) -> int:
    for groups in (8, 6, 5, 4, 3, 2, 1):
        if channels % groups == 0:
            return groups
    return 1


def _bounded(inputs: Tensor, *, limit: float = 12.0) -> Tensor:
    return torch.clamp(inputs, min=-limit, max=limit)


def _finite_feature(inputs: Tensor, *, limit: float, nan: float = 0.0) -> Tensor:
    return torch.nan_to_num(inputs, nan=nan, posinf=limit, neginf=-limit).clamp(-limit, limit)


def _smooth(inputs: Tensor, kernel_size: int) -> Tensor:
    return F.avg_pool2d(inputs, kernel_size=kernel_size, stride=1, padding=kernel_size // 2, count_include_pad=False)


def _prefix_average(values: Tensor, weights: Tensor, *, dim: int) -> Tensor:
    weighted = values * weights
    numerator = torch.cumsum(weighted, dim=dim)
    denominator = torch.cumsum(weights, dim=dim).clamp_min(1.0e-3)
    return numerator / denominator


class ABIBTDSZAFrontEnd(nn.Module):
    """Normalize ABI+SZA and add ABI-channel BTD plus learned channel mixtures."""

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

    def __init__(self, learned_channels: int = 12) -> None:
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
    def __init__(self, in_channels: int, out_channels: int, *, kernel_size: int = 3, stride: int = 1, dilation: int = 1) -> None:
        super().__init__()
        padding = dilation * (kernel_size // 2)
        self.block = nn.Sequential(
            nn.Conv2d(in_channels, out_channels, kernel_size=kernel_size, stride=stride, padding=padding, dilation=dilation, bias=False),
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
        return _bounded(self.act(self.conv2(self.conv1(inputs)) + self.skip(inputs)))


class SignedDetailBridge(nn.Module):
    """High-resolution signed-detail evidence without target or postprocessing logic."""

    def __init__(self, in_channels: int, out_channels: int) -> None:
        super().__init__()
        self.raw = ConvNormAct(in_channels, out_channels, kernel_size=1)
        self.local_pos = ConvNormAct(in_channels, out_channels, kernel_size=1)
        self.local_neg = ConvNormAct(in_channels, out_channels, kernel_size=1)
        self.mid_pos = ConvNormAct(in_channels, out_channels, kernel_size=1)
        self.mid_neg = ConvNormAct(in_channels, out_channels, kernel_size=1)
        self.project = nn.Sequential(ConvNormAct(out_channels * 5, out_channels), ResidualBlock(out_channels, out_channels))

    def forward(self, features: Tensor) -> Tensor:
        local = features - _smooth(features, 7)
        mid = features - _smooth(features, 15)
        return self.project(
            torch.cat(
                (
                    self.raw(features),
                    self.local_pos(F.relu(local)),
                    self.local_neg(F.relu(-local)),
                    self.mid_pos(F.relu(mid)),
                    self.mid_neg(F.relu(-mid)),
                ),
                dim=1,
            )
        )


class SelectiveAxialLineMemory(nn.Module):
    """Differentiable axial state-space-style line memory over feature tensors.

    The block forms learned-gated prefix averages in left/right and up/down directions,
    then fuses those long-line contexts back into the feature map. It is model logic only:
    no thresholding, morphology, target derivation, or Artifact Filter behavior is used.
    """

    def __init__(self, channels: int) -> None:
        super().__init__()
        self.norm = nn.GroupNorm(_group_count(channels), channels)
        self.value = nn.Conv2d(channels, channels, kernel_size=1, bias=False)
        self.gate = nn.Conv2d(channels, channels, kernel_size=1)
        self.local_line = nn.Sequential(
            nn.Conv2d(channels, channels, kernel_size=(1, 9), padding=(0, 4), groups=channels, bias=False),
            nn.Conv2d(channels, channels, kernel_size=(9, 1), padding=(4, 0), groups=channels, bias=False),
            nn.Conv2d(channels, channels, kernel_size=1, bias=False),
            nn.GroupNorm(_group_count(channels), channels),
            nn.GELU(),
        )
        self.fuse = nn.Sequential(ConvNormAct(channels * 6, channels, kernel_size=1), ResidualBlock(channels, channels))
        self.scale = nn.Parameter(torch.tensor(0.15))

    def forward(self, inputs: Tensor) -> Tensor:
        normed = self.norm(inputs)
        values = _bounded(self.value(normed))
        weights = torch.sigmoid(self.gate(normed)).clamp_min(1.0e-3)
        left_to_right = _prefix_average(values, weights, dim=3)
        right_to_left = torch.flip(_prefix_average(torch.flip(values, dims=(3,)), torch.flip(weights, dims=(3,)), dim=3), dims=(3,))
        top_to_bottom = _prefix_average(values, weights, dim=2)
        bottom_to_top = torch.flip(_prefix_average(torch.flip(values, dims=(2,)), torch.flip(weights, dims=(2,)), dim=2), dims=(2,))
        support = self.fuse(torch.cat((inputs, left_to_right, right_to_left, top_to_bottom, bottom_to_top, self.local_line(inputs)), dim=1))
        return _bounded(inputs + torch.tanh(self.scale) * support)


class EncoderStage(nn.Module):
    def __init__(self, in_channels: int, out_channels: int, *, stride: int) -> None:
        super().__init__()
        self.block = nn.Sequential(
            ConvNormAct(in_channels, out_channels, stride=stride),
            ResidualBlock(out_channels, out_channels),
            SelectiveAxialLineMemory(out_channels),
            ResidualBlock(out_channels, out_channels, dilation=2),
        )

    def forward(self, inputs: Tensor) -> Tensor:
        return self.block(inputs)


class DecoderStage(nn.Module):
    def __init__(self, in_channels: int, skip_channels: int, out_channels: int) -> None:
        super().__init__()
        self.skip_project = ConvNormAct(skip_channels, out_channels, kernel_size=1)
        self.fuse = nn.Sequential(
            ConvNormAct(in_channels + out_channels, out_channels),
            ResidualBlock(out_channels, out_channels),
            SelectiveAxialLineMemory(out_channels),
        )

    def forward(self, inputs: Tensor, skip: Tensor) -> Tensor:
        upsampled = F.interpolate(inputs, size=skip.shape[-2:], mode="bilinear", align_corners=False)
        return self.fuse(torch.cat((upsampled, self.skip_project(skip)), dim=1))


class AxialEvidenceHead(nn.Module):
    """Mask, Line, and Centerline heads with bounded architecture-level logit evidence."""

    def __init__(self, channels: int) -> None:
        super().__init__()
        self.line_memory = nn.Sequential(SelectiveAxialLineMemory(channels), ResidualBlock(channels, channels))
        self.recall_path = nn.Sequential(ResidualBlock(channels, channels, dilation=2), ConvNormAct(channels, channels))
        self.agreement = nn.Sequential(
            ConvNormAct(channels * 4, channels, kernel_size=1),
            nn.Conv2d(channels, channels, kernel_size=1),
            nn.Sigmoid(),
        )
        self.fuse = nn.Sequential(ConvNormAct(channels * 3, channels), ResidualBlock(channels, channels))
        self.mask_base = nn.Conv2d(channels, 1, kernel_size=1)
        self.mask_recall = nn.Conv2d(channels, 1, kernel_size=1)
        self.line_head = nn.Conv2d(channels, 1, kernel_size=1)
        self.centerline_head = nn.Conv2d(channels, 1, kernel_size=1)

    def forward(self, features: Tensor) -> dict[str, Tensor]:
        line_features = self.line_memory(features)
        recall_features = self.recall_path(features)
        gate = self.agreement(torch.cat((features, line_features, recall_features, torch.abs(line_features - recall_features)), dim=1))
        fused = self.fuse(torch.cat((features, gate * recall_features, (1.0 - gate) * line_features), dim=1))
        line_logits = self.line_head(line_features)
        return {
            "mask_logits": self.mask_base(fused) + 0.15 * torch.tanh(self.mask_recall(recall_features)) + 0.15 * torch.tanh(line_logits),
            "line_logits": line_logits,
            "centerline_logits": self.centerline_head(fused),
        }


class SelectiveAxialLineMemoryUNet(nn.Module):
    """Compact U-Net with long axial line-memory blocks at multiple scales."""

    def __init__(self) -> None:
        super().__init__()
        self.front_end = ABIBTDSZAFrontEnd(learned_channels=12)
        base = 32
        self.detail = SignedDetailBridge(self.front_end.out_channels, base)
        self.stem = nn.Sequential(ConvNormAct(self.front_end.out_channels, base), ResidualBlock(base, base), SelectiveAxialLineMemory(base))
        self.enc1 = EncoderStage(base, 48, stride=2)
        self.enc2 = EncoderStage(48, 80, stride=2)
        self.enc3 = EncoderStage(80, 128, stride=2)
        self.bottleneck = nn.Sequential(ResidualBlock(128, 160), SelectiveAxialLineMemory(160), ResidualBlock(160, 160, dilation=2))
        self.up2 = DecoderStage(160, 80, 96)
        self.up1 = DecoderStage(96, 48, 64)
        self.up0 = DecoderStage(64, base, 48)
        self.final_fuse = nn.Sequential(
            ConvNormAct(48 + base + base, 48),
            ResidualBlock(48, 48),
            SelectiveAxialLineMemory(48),
            ResidualBlock(48, 48),
        )
        self.head = AxialEvidenceHead(48)

    def forward(self, inputs: Tensor) -> dict[str, Tensor]:
        features = self.front_end(inputs)
        stem = self.stem(features)
        detail = self.detail(features)
        enc1 = self.enc1(stem)
        enc2 = self.enc2(enc1)
        enc3 = self.enc3(enc2)
        bottleneck = self.bottleneck(enc3)
        dec2 = self.up2(bottleneck, enc2)
        dec1 = self.up1(dec2, enc1)
        dec0 = self.up0(dec1, stem)
        fused = self.final_fuse(torch.cat((dec0, stem, detail), dim=1))
        return self.head(fused)


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
    if input_spec.get("source_channel_indices") not in (None, list(range(16)) + [18]):
        raise ValueError(f"{CANDIDATE_ID} received an unexpected source-channel contract")
    if output_spec.get("form") != "mask_logits" or output_spec.get("shape") != [1, 256, 256]:
        raise ValueError(f"{CANDIDATE_ID} requires mask_logits [1, 256, 256] primary output")
    _validate_auxiliary_outputs(output_spec)
    return SelectiveAxialLineMemoryUNet()
