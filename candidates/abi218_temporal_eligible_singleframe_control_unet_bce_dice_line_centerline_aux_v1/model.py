"""Temporal-eligible single-frame ABI+SZA control U-Net for ABI-217."""

from __future__ import annotations

import torch
import torch.nn.functional as F
from torch import Tensor, nn


CANDIDATE_ID = "abi218_temporal_eligible_singleframe_control_unet_bce_dice_line_centerline_aux_v1"
INPUT_CHANNELS = 17


def _finite_feature(inputs: Tensor, *, limit: float, nan: float = 0.0) -> Tensor:
    """Map non-finite candidate-visible feature values to bounded neutral values."""

    return torch.nan_to_num(inputs, nan=nan, posinf=limit, neginf=-limit).clamp(-limit, limit)


def _bounded(inputs: Tensor, *, limit: float = 12.0) -> Tensor:
    """Bound finite internal activations without hiding non-finite parameter failures."""

    return torch.clamp(inputs, min=-limit, max=limit)


class SingleFrameFeatureBuilder(nn.Module):
    """Normalize provider-supplied ABI+SZA and add finite approved-channel BTD planes."""

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
    # Zero-based ABI indices within the 17-channel candidate-visible frame.
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

    def forward(self, inputs: Tensor) -> Tensor:
        if inputs.ndim != 4 or inputs.shape[1] != INPUT_CHANNELS:
            raise ValueError(f"expected [N, {INPUT_CHANNELS}, H, W] ABI+SZA tensor, got {tuple(inputs.shape)}")
        abi = inputs[:, :16, :, :]
        sza = inputs[:, 16:17, :, :]
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


def _group_count(channels: int) -> int:
    for groups in (8, 6, 4, 3, 2, 1):
        if channels % groups == 0:
            return groups
    return 1


class ConvNormAct(nn.Module):
    """Convolution, GroupNorm, GELU, and bounded activations for stable small-batch training."""

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
    """Compact residual block used in the encoder and decoder."""

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


class SingleFrameEncoder(nn.Module):
    """Compact four-scale encoder matching ABI-217's per-frame encoder width."""

    def __init__(self, in_channels: int, base_channels: int) -> None:
        super().__init__()
        self.stem = nn.Sequential(
            ConvNormAct(in_channels, base_channels),
            ResidualBlock(base_channels, base_channels),
        )
        self.down1 = DownBlock(base_channels, base_channels * 2)
        self.down2 = DownBlock(base_channels * 2, base_channels * 4)
        self.down3 = DownBlock(base_channels * 4, base_channels * 8)

    def forward(self, features: Tensor) -> tuple[Tensor, Tensor, Tensor, Tensor]:
        scale0 = self.stem(features)
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


class TemporalEligibleSingleFrameControlUNet(nn.Module):
    """A compact center-frame ABI+SZA U-Net with Line and Centerline auxiliary heads."""

    def __init__(self) -> None:
        super().__init__()
        base = 24
        self.frame_features = SingleFrameFeatureBuilder()
        self.encoder = SingleFrameEncoder(self.frame_features.out_channels, base)
        self.context = ASPPContext(base * 8)
        self.up2 = DecoderFuse(base * 8, base * 4, base * 4)
        self.up1 = DecoderFuse(base * 4, base * 2, base * 2)
        self.up0 = DecoderFuse(base * 2, base, base)
        self.refine = nn.Sequential(
            ConvNormAct(base * 2, base),
            ResidualBlock(base, base),
            ResidualBlock(base, base),
        )
        self.mask_head = nn.Conv2d(base, 1, kernel_size=1)
        self.line_head = nn.Conv2d(base, 1, kernel_size=1)
        self.centerline_head = nn.Conv2d(base, 1, kernel_size=1)

    def forward(self, inputs: Tensor) -> dict[str, Tensor]:
        features = self.frame_features(inputs)
        scale0, scale1, scale2, scale3 = self.encoder(features)
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
    """Build the model for the Harness-supplied single-frame ABI+SZA contract."""

    if input_spec.get("mode") != "abi_16ch_plus_sza":
        raise ValueError(f"{CANDIDATE_ID} requires abi_16ch_plus_sza input")
    if input_spec.get("shape") != [INPUT_CHANNELS, 256, 256]:
        raise ValueError(f"{CANDIDATE_ID} requires [{INPUT_CHANNELS}, 256, 256] input")
    if output_spec.get("form") != "mask_logits" or output_spec.get("shape") != [1, 256, 256]:
        raise ValueError(f"{CANDIDATE_ID} requires mask_logits [1, 256, 256] primary output")
    _validate_auxiliary_outputs(output_spec)
    return TemporalEligibleSingleFrameControlUNet()
