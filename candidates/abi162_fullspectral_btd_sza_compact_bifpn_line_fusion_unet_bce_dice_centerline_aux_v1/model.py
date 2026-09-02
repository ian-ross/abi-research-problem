"""Compact full-spectral BTD+SZA bidirectional feature-pyramid line-fusion U-Net."""

from __future__ import annotations

import torch
import torch.nn.functional as F
from torch import Tensor, nn


CANDIDATE_ID = "abi162_fullspectral_btd_sza_compact_bifpn_line_fusion_unet_bce_dice_centerline_aux_v1"


class NormalizedBTDSZAFrontEnd(nn.Module):
    """Build bounded normalized ABI, thermal-difference, solar-geometry, and learned features."""

    _CHANNEL_MEANS = (
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
    _CHANNEL_SCALES = (
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

    def __init__(self, learned_channels: int = 8) -> None:
        super().__init__()
        self.register_buffer(
            "channel_means",
            torch.tensor(self._CHANNEL_MEANS, dtype=torch.float32).view(1, 16, 1, 1),
        )
        self.register_buffer(
            "channel_scales",
            torch.tensor(self._CHANNEL_SCALES, dtype=torch.float32).view(1, 16, 1, 1),
        )
        self.learned_mixer = nn.Sequential(
            nn.Conv2d(17, learned_channels, kernel_size=1, bias=True),
            nn.GELU(),
        )
        self.out_channels = 16 + len(self._BTD_PAIRS) + 2 + learned_channels

    def forward(self, inputs: Tensor) -> Tensor:
        if inputs.ndim != 4 or inputs.shape[1] != 17:
            raise ValueError(f"expected [N, 17, H, W] ABI+SZA tensor, got {tuple(inputs.shape)}")
        abi = inputs[:, :16, :, :]
        sza = inputs[:, 16:17, :, :]
        normalized = (abi - self.channel_means) / self.channel_scales
        btd_planes = torch.cat(
            [
                (abi[:, a : a + 1, :, :] - abi[:, b : b + 1, :, :]) / self._BTD_SCALE
                for a, b in self._BTD_PAIRS
            ],
            dim=1,
        )
        sza_clamped = torch.clamp(sza, 0.0, 180.0)
        sza_scaled = (sza_clamped - 90.0) / 90.0
        sza_cosine = torch.cos(torch.deg2rad(sza_clamped))
        learned = self.learned_mixer(torch.cat((normalized, sza_scaled), dim=1))
        return torch.cat((normalized, btd_planes, sza_scaled, sza_cosine, learned), dim=1)


def _group_count(channels: int) -> int:
    for groups in (8, 6, 5, 4, 3, 2, 1):
        if channels % groups == 0:
            return groups
    return 1


def _smooth(inputs: Tensor, kernel_size: int | tuple[int, int]) -> Tensor:
    if isinstance(kernel_size, tuple):
        padding = (kernel_size[0] // 2, kernel_size[1] // 2)
    else:
        padding = kernel_size // 2
    return F.avg_pool2d(inputs, kernel_size=kernel_size, stride=1, padding=padding, count_include_pad=False)


class ConvNormAct(nn.Module):
    """Convolution, GroupNorm, and GELU activation for stable small-batch training."""

    def __init__(
        self,
        in_channels: int,
        out_channels: int,
        *,
        kernel_size: int | tuple[int, int] = 3,
        dilation: int | tuple[int, int] = 1,
    ) -> None:
        super().__init__()
        if isinstance(kernel_size, tuple):
            if isinstance(dilation, tuple):
                padding = (dilation[0] * (kernel_size[0] // 2), dilation[1] * (kernel_size[1] // 2))
            else:
                padding = (dilation * (kernel_size[0] // 2), dilation * (kernel_size[1] // 2))
        else:
            if isinstance(dilation, tuple):
                padding = (dilation[0] * (kernel_size // 2), dilation[1] * (kernel_size // 2))
            else:
                padding = dilation * (kernel_size // 2)
        self.block = nn.Sequential(
            nn.Conv2d(
                in_channels,
                out_channels,
                kernel_size=kernel_size,
                padding=padding,
                dilation=dilation,
                bias=False,
            ),
            nn.GroupNorm(_group_count(out_channels), out_channels),
            nn.GELU(),
        )

    def forward(self, inputs: Tensor) -> Tensor:
        return self.block(inputs)


class ResidualBlock(nn.Module):
    """Residual convolution block used at each image scale."""

    def __init__(self, in_channels: int, out_channels: int, *, dilation: int = 1) -> None:
        super().__init__()
        self.conv1 = ConvNormAct(in_channels, out_channels, dilation=dilation)
        self.conv2 = nn.Sequential(
            nn.Conv2d(out_channels, out_channels, kernel_size=3, padding=1, bias=False),
            nn.GroupNorm(_group_count(out_channels), out_channels),
        )
        self.skip = (
            nn.Identity()
            if in_channels == out_channels
            else nn.Conv2d(in_channels, out_channels, kernel_size=1, bias=False)
        )
        self.act = nn.GELU()

    def forward(self, inputs: Tensor) -> Tensor:
        return self.act(self.conv2(self.conv1(inputs)) + self.skip(inputs))


class LineEvidenceStem(nn.Module):
    """Single high-resolution line-evidence stem with bounded local/oriented support."""

    def __init__(self, in_channels: int, out_channels: int) -> None:
        super().__init__()
        self.raw_project = ConvNormAct(in_channels, out_channels, kernel_size=1)
        self.detail_project = ConvNormAct(in_channels, out_channels, kernel_size=1)
        self.line_project = ConvNormAct(in_channels * 2, out_channels, kernel_size=1)
        self.context_project = ConvNormAct(in_channels, out_channels, kernel_size=1)
        self.fuse = nn.Sequential(
            ConvNormAct(out_channels * 4, out_channels),
            ResidualBlock(out_channels, out_channels),
        )

    def forward(self, inputs: Tensor) -> Tensor:
        local_mean = _smooth(inputs, 7)
        detail = inputs - local_mean
        horizontal = _smooth(inputs, (1, 11)) - local_mean
        vertical = _smooth(inputs, (11, 1)) - local_mean
        context = _smooth(inputs, 21)
        return self.fuse(
            torch.cat(
                (
                    self.raw_project(inputs),
                    self.detail_project(detail),
                    self.line_project(torch.cat((horizontal, vertical), dim=1)),
                    self.context_project(context),
                ),
                dim=1,
            )
        )


class EncoderDown(nn.Module):
    """Downsample by two and encode features at the new scale."""

    def __init__(self, in_channels: int, out_channels: int) -> None:
        super().__init__()
        self.block = nn.Sequential(
            nn.MaxPool2d(2),
            ResidualBlock(in_channels, out_channels),
        )

    def forward(self, inputs: Tensor) -> Tensor:
        return self.block(inputs)


class WeightedFuse(nn.Module):
    """Learn a positive normalized mixture of same-resolution feature tensors."""

    def __init__(self, input_count: int, channels: int) -> None:
        super().__init__()
        self.weights = nn.Parameter(torch.ones(input_count, dtype=torch.float32))
        self.project = ConvNormAct(channels, channels)

    def forward(self, tensors: list[Tensor]) -> Tensor:
        if len(tensors) != self.weights.numel():
            raise ValueError(f"expected {self.weights.numel()} tensors, got {len(tensors)}")
        weights = F.relu(self.weights)
        weights = weights / (weights.sum() + 1e-6)
        fused = torch.zeros_like(tensors[0])
        for index, tensor in enumerate(tensors):
            fused = fused + weights[index] * tensor
        return self.project(fused)


class BiFPNFuse(nn.Module):
    """Narrow bidirectional feature pyramid with top-down and bottom-up fusion."""

    def __init__(self, channels: int) -> None:
        super().__init__()
        self.td2 = WeightedFuse(2, channels)
        self.td1 = WeightedFuse(2, channels)
        self.td0 = WeightedFuse(2, channels)
        self.bu1 = WeightedFuse(2, channels)
        self.bu2 = WeightedFuse(2, channels)
        self.bu3 = WeightedFuse(2, channels)
        self.out0 = WeightedFuse(4, channels)

    def forward(self, p0: Tensor, p1: Tensor, p2: Tensor, p3: Tensor) -> Tensor:
        p2_td = self.td2([p2, F.interpolate(p3, size=p2.shape[-2:], mode="bilinear", align_corners=False)])
        p1_td = self.td1([p1, F.interpolate(p2_td, size=p1.shape[-2:], mode="bilinear", align_corners=False)])
        p0_td = self.td0([p0, F.interpolate(p1_td, size=p0.shape[-2:], mode="bilinear", align_corners=False)])
        p1_bu = self.bu1([p1_td, F.max_pool2d(p0_td, kernel_size=2)])
        p2_bu = self.bu2([p2_td, F.max_pool2d(p1_bu, kernel_size=2)])
        p3_bu = self.bu3([p3, F.max_pool2d(p2_bu, kernel_size=2)])
        target_size = p0_td.shape[-2:]
        return self.out0(
            [
                p0_td,
                F.interpolate(p1_bu, size=target_size, mode="bilinear", align_corners=False),
                F.interpolate(p2_bu, size=target_size, mode="bilinear", align_corners=False),
                F.interpolate(p3_bu, size=target_size, mode="bilinear", align_corners=False),
            ]
        )


class CompactLineHead(nn.Module):
    """Final feature-space line-context refinement for fixed-threshold calibration."""

    def __init__(self, channels: int) -> None:
        super().__init__()
        self.detail = ConvNormAct(channels, channels)
        self.horizontal = ConvNormAct(channels, channels, kernel_size=(1, 9))
        self.vertical = ConvNormAct(channels, channels, kernel_size=(9, 1))
        self.project = nn.Sequential(
            ConvNormAct(channels * 4, channels),
            ResidualBlock(channels, channels),
        )

    def forward(self, inputs: Tensor) -> Tensor:
        detail = self.detail(inputs - _smooth(inputs, 7))
        horizontal = self.horizontal(inputs)
        vertical = self.vertical(inputs)
        context = _smooth(inputs, 15)
        return self.project(torch.cat((inputs, detail, horizontal + vertical, context), dim=1))


class CompactFullSpectralBTDSZABiFPNLineFusionUNet(nn.Module):
    """Compact SZA-aware BTD U-Net with resource-bounded BiFPN context fusion."""

    def __init__(self) -> None:
        super().__init__()
        self.front_end = NormalizedBTDSZAFrontEnd(learned_channels=8)
        base = 32
        pyramid = 64
        self.stem = LineEvidenceStem(self.front_end.out_channels, base)
        self.enc0 = ResidualBlock(base, base)
        self.enc1 = EncoderDown(base, base * 2)
        self.enc2 = EncoderDown(base * 2, base * 4)
        self.enc3 = EncoderDown(base * 4, base * 8)
        self.p0 = ConvNormAct(base, pyramid, kernel_size=1)
        self.p1 = ConvNormAct(base * 2, pyramid, kernel_size=1)
        self.p2 = ConvNormAct(base * 4, pyramid, kernel_size=1)
        self.p3 = ConvNormAct(base * 8, pyramid, kernel_size=1)
        self.bifpn = BiFPNFuse(pyramid)
        self.highres_project = ConvNormAct(base, pyramid, kernel_size=1)
        self.final_fuse = nn.Sequential(
            ConvNormAct(pyramid * 2, pyramid),
            ResidualBlock(pyramid, pyramid),
        )
        self.line_head = CompactLineHead(pyramid)
        self.mask_head = nn.Conv2d(pyramid, 1, kernel_size=1)
        self.centerline_head = nn.Conv2d(pyramid, 1, kernel_size=1)

    def forward(self, inputs: Tensor) -> dict[str, Tensor]:
        features = self.front_end(inputs)
        stem = self.stem(features)
        enc0 = self.enc0(stem)
        enc1 = self.enc1(enc0)
        enc2 = self.enc2(enc1)
        enc3 = self.enc3(enc2)
        pyramid = self.bifpn(self.p0(enc0), self.p1(enc1), self.p2(enc2), self.p3(enc3))
        highres = self.highres_project(enc0)
        refined = self.line_head(self.final_fuse(torch.cat((pyramid, highres), dim=1)))
        return {
            "mask_logits": self.mask_head(refined),
            "centerline_logits": self.centerline_head(refined),
        }


def _validate_centerline_auxiliary_output(output_spec: dict[str, object]) -> None:
    auxiliary_outputs = output_spec.get("auxiliary_outputs")
    expected = [{"target": "centerline", "name": "centerline_logits", "shape": [1, 256, 256]}]
    if auxiliary_outputs != expected:
        raise ValueError(f"{CANDIDATE_ID} requires exactly one trusted centerline auxiliary output named centerline_logits")


def build_model(input_spec: dict[str, object], output_spec: dict[str, object]) -> nn.Module:
    """Build the model for the Harness-supplied ABI contract."""

    if input_spec.get("mode") != "abi_16ch_plus_sza" or input_spec.get("shape") != [17, 256, 256]:
        raise ValueError(f"{CANDIDATE_ID} requires abi_16ch_plus_sza [17, 256, 256] input")
    if output_spec.get("form") != "mask_logits" or output_spec.get("shape") != [1, 256, 256]:
        raise ValueError(f"{CANDIDATE_ID} requires mask_logits [1, 256, 256] primary output")
    _validate_centerline_auxiliary_output(output_spec)
    return CompactFullSpectralBTDSZABiFPNLineFusionUNet()
