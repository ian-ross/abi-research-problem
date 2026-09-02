"""Full-spectral BTD+SZA nested-skip U-Net for ABI contrail segmentation."""

from __future__ import annotations

import torch
import torch.nn.functional as F
from torch import Tensor, nn


class NormalizedBTDSZAFrontEnd(nn.Module):
    """Build normalized ABI, thermal-difference, solar-geometry, and learned features."""

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
    # Zero-based candidate-input channel pairs. All use provider-approved ABI channels 1-16.
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

    def __init__(self, learned_channels: int = 16) -> None:
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
        # Raw normalized ABI channels + thermal BTD planes + normalized SZA + cos(SZA) + learned mixture.
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
    for groups in (8, 6, 4, 3, 2, 1):
        if channels % groups == 0:
            return groups
    return 1


def _as_pair(value: int | tuple[int, int]) -> tuple[int, int]:
    if isinstance(value, tuple):
        return value
    return (value, value)


def _smooth(inputs: Tensor, kernel_size: int) -> Tensor:
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
        kernel_pair = _as_pair(kernel_size)
        dilation_pair = _as_pair(dilation)
        padding = (
            dilation_pair[0] * (kernel_pair[0] // 2),
            dilation_pair[1] * (kernel_pair[1] // 2),
        )
        self.block = nn.Sequential(
            nn.Conv2d(
                in_channels,
                out_channels,
                kernel_size=kernel_pair,
                padding=padding,
                dilation=dilation_pair,
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


class DownBlock(nn.Module):
    """Downsample while preserving a residual feature transform."""

    def __init__(self, in_channels: int, out_channels: int) -> None:
        super().__init__()
        self.block = nn.Sequential(
            nn.MaxPool2d(2),
            ResidualBlock(in_channels, out_channels),
            ResidualBlock(out_channels, out_channels),
        )

    def forward(self, inputs: Tensor) -> Tensor:
        return self.block(inputs)


class ASPPContext(nn.Module):
    """Compact atrous context at the coarsest scale."""

    def __init__(self, channels: int) -> None:
        super().__init__()
        branch_channels = channels // 2
        self.d1 = ConvNormAct(channels, branch_channels, kernel_size=1)
        self.d2 = ConvNormAct(channels, branch_channels, dilation=2)
        self.d4 = ConvNormAct(channels, branch_channels, dilation=4)
        self.d6 = ConvNormAct(channels, branch_channels, dilation=6)
        self.project = nn.Sequential(
            ConvNormAct(branch_channels * 4, channels, kernel_size=1),
            ResidualBlock(channels, channels),
        )

    def forward(self, inputs: Tensor) -> Tensor:
        return self.project(torch.cat((self.d1(inputs), self.d2(inputs), self.d4(inputs), self.d6(inputs)), dim=1))


class NestedFuse(nn.Module):
    """Fuse same-depth skip features with upsampled deeper context."""

    def __init__(self, in_channels: int, out_channels: int) -> None:
        super().__init__()
        self.fuse = nn.Sequential(
            ConvNormAct(in_channels, out_channels),
            ResidualBlock(out_channels, out_channels),
        )

    def forward(self, *features: Tensor) -> Tensor:
        target_size = features[0].shape[-2:]
        aligned = [
            feature
            if feature.shape[-2:] == target_size
            else F.interpolate(feature, size=target_size, mode="bilinear", align_corners=False)
            for feature in features
        ]
        return self.fuse(torch.cat(aligned, dim=1))


class MultiDepthEvidenceFusion(nn.Module):
    """Aggregate nested full-resolution nodes and deeper context into final evidence."""

    def __init__(self, base_channels: int) -> None:
        super().__init__()
        self.x1_project = ConvNormAct(base_channels * 2, base_channels, kernel_size=1)
        self.x2_project = ConvNormAct(base_channels * 4, base_channels, kernel_size=1)
        self.x3_project = ConvNormAct(base_channels * 8, base_channels, kernel_size=1)
        self.detail_project = ConvNormAct(base_channels, base_channels)
        self.horizontal = ConvNormAct(base_channels, base_channels, kernel_size=(1, 9))
        self.vertical = ConvNormAct(base_channels, base_channels, kernel_size=(9, 1))
        self.fuse = nn.Sequential(
            ConvNormAct(base_channels * 8, base_channels * 2),
            ResidualBlock(base_channels * 2, base_channels * 2),
            ConvNormAct(base_channels * 2, base_channels),
            ResidualBlock(base_channels, base_channels),
        )
        self.residual_scale = nn.Parameter(torch.tensor(0.1, dtype=torch.float32))

    def forward(
        self,
        x0_1: Tensor,
        x0_2: Tensor,
        x0_3: Tensor,
        x1_2: Tensor,
        x2_1: Tensor,
        x3_context: Tensor,
    ) -> Tensor:
        target_size = x0_3.shape[-2:]
        x1_full = self.x1_project(F.interpolate(x1_2, size=target_size, mode="bilinear", align_corners=False))
        x2_full = self.x2_project(F.interpolate(x2_1, size=target_size, mode="bilinear", align_corners=False))
        x3_full = self.x3_project(F.interpolate(x3_context, size=target_size, mode="bilinear", align_corners=False))
        detail = self.detail_project(x0_3 - _smooth(x0_3, 9))
        horizontal = self.horizontal(detail)
        vertical = self.vertical(detail)
        fused = self.fuse(torch.cat((x0_1, x0_2, x0_3, x1_full, x2_full, x3_full, horizontal, vertical), dim=1))
        return fused + self.residual_scale * detail


class FullSpectralBTDSZANestedSkipUNet(nn.Module):
    """Compact nested-skip U-Net with full-spectral BTD features."""

    def __init__(self) -> None:
        super().__init__()
        self.front_end = NormalizedBTDSZAFrontEnd(learned_channels=16)
        base = 32
        self.stem = nn.Sequential(
            ConvNormAct(self.front_end.out_channels, base),
            ResidualBlock(base, base),
        )
        self.down1 = DownBlock(base, base * 2)
        self.down2 = DownBlock(base * 2, base * 4)
        self.down3 = DownBlock(base * 4, base * 8)
        self.context = ASPPContext(base * 8)

        self.x2_1 = NestedFuse(base * 4 + base * 8, base * 4)
        self.x1_1 = NestedFuse(base * 2 + base * 4, base * 2)
        self.x0_1 = NestedFuse(base + base * 2, base)
        self.x1_2 = NestedFuse(base * 2 + base * 2 + base * 4, base * 2)
        self.x0_2 = NestedFuse(base + base + base * 2, base)
        self.x0_3 = NestedFuse(base + base + base + base * 2, base)
        self.final_fusion = MultiDepthEvidenceFusion(base)
        self.mask_head = nn.Conv2d(base, 1, kernel_size=1)
        self.centerline_head = nn.Conv2d(base, 1, kernel_size=1)

    def forward(self, inputs: Tensor) -> dict[str, Tensor]:
        features = self.front_end(inputs)
        x0_0 = self.stem(features)
        x1_0 = self.down1(x0_0)
        x2_0 = self.down2(x1_0)
        x3_0 = self.down3(x2_0)
        x3_context = self.context(x3_0)

        x2_1 = self.x2_1(x2_0, x3_context)
        x1_1 = self.x1_1(x1_0, x2_0)
        x0_1 = self.x0_1(x0_0, x1_0)
        x1_2 = self.x1_2(x1_0, x1_1, x2_1)
        x0_2 = self.x0_2(x0_0, x0_1, x1_1)
        x0_3 = self.x0_3(x0_0, x0_1, x0_2, x1_2)

        fused = self.final_fusion(x0_1, x0_2, x0_3, x1_2, x2_1, x3_context)
        return {
            "mask_logits": self.mask_head(fused),
            "centerline_logits": self.centerline_head(fused),
        }


def _validate_centerline_auxiliary_output(output_spec: dict[str, object]) -> None:
    auxiliary_outputs = output_spec.get("auxiliary_outputs")
    expected = [{"target": "centerline", "name": "centerline_logits", "shape": [1, 256, 256]}]
    if auxiliary_outputs != expected:
        raise ValueError(
            "abi139_fullspectral_btd_sza_nested_skip_unet_bce_dice_centerline_aux_v1 requires "
            "exactly one trusted centerline auxiliary output named centerline_logits"
        )


def build_model(input_spec: dict[str, object], output_spec: dict[str, object]) -> nn.Module:
    """Build the model for the Harness-supplied ABI contract."""

    if input_spec.get("mode") != "abi_16ch_plus_sza" or input_spec.get("shape") != [17, 256, 256]:
        raise ValueError(
            "abi139_fullspectral_btd_sza_nested_skip_unet_bce_dice_centerline_aux_v1 requires "
            "abi_16ch_plus_sza [17, 256, 256] input"
        )
    if output_spec.get("form") != "mask_logits" or output_spec.get("shape") != [1, 256, 256]:
        raise ValueError(
            "abi139_fullspectral_btd_sza_nested_skip_unet_bce_dice_centerline_aux_v1 requires "
            "mask_logits [1, 256, 256] primary output"
        )
    _validate_centerline_auxiliary_output(output_spec)
    return FullSpectralBTDSZANestedSkipUNet()
