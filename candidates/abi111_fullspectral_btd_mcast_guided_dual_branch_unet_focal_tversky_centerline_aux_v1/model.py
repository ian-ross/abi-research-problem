"""Full-spectral BTD and MCAST-guided dual-branch U-Net for ABI contrail segmentation."""

from __future__ import annotations

import torch
import torch.nn.functional as F
from torch import Tensor, nn


def _group_count(channels: int) -> int:
    for groups in (8, 6, 4, 3, 2, 1):
        if channels % groups == 0:
            return groups
    return 1


def _smooth(inputs: Tensor, kernel_size: int) -> Tensor:
    padding = kernel_size // 2
    return F.avg_pool2d(inputs, kernel_size=kernel_size, stride=1, padding=padding, count_include_pad=False)


class NormalizedBTDFrontEnd(nn.Module):
    """Build normalized raw, thermal-difference, and learned full-ABI channel features."""

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
            nn.Conv2d(16, learned_channels, kernel_size=1, bias=True),
            nn.GELU(),
        )
        self.out_channels = 16 + len(self._BTD_PAIRS) + learned_channels

    def forward(self, inputs: Tensor) -> Tensor:
        if inputs.ndim != 4 or inputs.shape[1] != 16:
            raise ValueError(f"expected [N, 16, H, W] ABI tensor, got {tuple(inputs.shape)}")
        normalized = (inputs - self.channel_means) / self.channel_scales
        btd_planes = torch.cat(
            [
                (inputs[:, a : a + 1, :, :] - inputs[:, b : b + 1, :, :]) / self._BTD_SCALE
                for a, b in self._BTD_PAIRS
            ],
            dim=1,
        )
        learned = self.learned_mixer(normalized)
        return torch.cat((normalized, btd_planes, learned), dim=1)


class MCASTThermalFrontEnd(nn.Module):
    """Derive normalized MCAST-like thermal evidence from approved ABI channels."""

    _MEANS = (274.15866814464114, 275.74145854126134, 3.05802131633268)
    _STDS = (18.369019656652068, 19.497045505465557, 1.8518705027433054)

    def __init__(self) -> None:
        super().__init__()
        self.register_buffer("means", torch.tensor(self._MEANS, dtype=torch.float32).view(1, 3, 1, 1))
        self.register_buffer("stds", torch.tensor(self._STDS, dtype=torch.float32).view(1, 3, 1, 1))
        self.out_channels = 3

    def forward(self, inputs: Tensor) -> Tensor:
        c11 = inputs[:, 10:11]
        c14 = inputs[:, 13:14]
        c13_minus_c15 = inputs[:, 12:13] - inputs[:, 14:15]
        planes = torch.cat((c11, c14, c13_minus_c15), dim=1)
        return (planes - self.means) / self.stds


class ConvNormAct(nn.Module):
    """Convolution, GroupNorm, and GELU activation for stable small-batch training."""

    def __init__(self, in_channels: int, out_channels: int, *, kernel_size: int = 3, dilation: int = 1) -> None:
        super().__init__()
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
        self.skip = nn.Identity() if in_channels == out_channels else nn.Conv2d(in_channels, out_channels, 1, bias=False)
        self.act = nn.GELU()

    def forward(self, inputs: Tensor) -> Tensor:
        return self.act(self.conv2(self.conv1(inputs)) + self.skip(inputs))


class FrequencySplitStem(nn.Module):
    """Separate local line contrast from broad cloud context before spectral encoding."""

    def __init__(self, in_channels: int, out_channels: int) -> None:
        super().__init__()
        self.raw_project = ConvNormAct(in_channels, out_channels, kernel_size=1)
        self.detail_project = ConvNormAct(in_channels, out_channels, kernel_size=1)
        self.context_project = ConvNormAct(in_channels, out_channels, kernel_size=1)
        self.fuse = nn.Sequential(ConvNormAct(out_channels * 3, out_channels), ResidualBlock(out_channels, out_channels))

    def forward(self, inputs: Tensor) -> Tensor:
        local_smooth = _smooth(inputs, 9)
        broad_smooth = _smooth(inputs, 25)
        detail = inputs - local_smooth
        return self.fuse(
            torch.cat(
                (self.raw_project(inputs), self.detail_project(detail), self.context_project(broad_smooth)),
                dim=1,
            )
        )


class MCASTStem(nn.Module):
    """Small branch for robust MCAST-like thermal support features."""

    def __init__(self, out_channels: int) -> None:
        super().__init__()
        self.block = nn.Sequential(
            ConvNormAct(3, out_channels),
            ResidualBlock(out_channels, out_channels),
            ConvNormAct(out_channels, out_channels, kernel_size=1),
        )

    def forward(self, inputs: Tensor) -> Tensor:
        return self.block(inputs)


class GuidedFusion(nn.Module):
    """Fuse spectral/detail features with a conservative MCAST-guidance branch."""

    def __init__(self, channels: int) -> None:
        super().__init__()
        self.mcast_project = ConvNormAct(channels, channels, kernel_size=1)
        self.gate = nn.Sequential(
            nn.Conv2d(channels * 2, channels, kernel_size=1, bias=True),
            nn.Sigmoid(),
        )
        self.fuse = nn.Sequential(
            ConvNormAct(channels * 3, channels),
            ResidualBlock(channels, channels),
        )

    def forward(self, spectral: Tensor, mcast: Tensor) -> Tensor:
        support = self.mcast_project(mcast)
        gate = self.gate(torch.cat((spectral, support), dim=1))
        calibrated = spectral * (0.75 + 0.5 * gate)
        return self.fuse(torch.cat((spectral, calibrated, support), dim=1))


class DualDownBlock(nn.Module):
    """Downsample spectral and MCAST branches, then fuse at the new scale."""

    def __init__(self, in_channels: int, out_channels: int) -> None:
        super().__init__()
        self.spectral_down = nn.Sequential(nn.MaxPool2d(2), ResidualBlock(in_channels, out_channels))
        self.mcast_down = nn.Sequential(nn.MaxPool2d(2), ResidualBlock(in_channels, out_channels))
        self.fusion = GuidedFusion(out_channels)

    def forward(self, spectral: Tensor, mcast: Tensor) -> tuple[Tensor, Tensor, Tensor]:
        spectral_next = self.spectral_down(spectral)
        mcast_next = self.mcast_down(mcast)
        fused = self.fusion(spectral_next, mcast_next)
        return fused, spectral_next, mcast_next


class UpFuseBlock(nn.Module):
    """Upsample decoder features and fuse them with the guided encoder skip."""

    def __init__(self, in_channels: int, skip_channels: int, out_channels: int) -> None:
        super().__init__()
        self.block = nn.Sequential(
            ConvNormAct(in_channels + skip_channels, out_channels),
            ResidualBlock(out_channels, out_channels),
        )

    def forward(self, inputs: Tensor, skip: Tensor) -> Tensor:
        upsampled = F.interpolate(inputs, size=skip.shape[-2:], mode="bilinear", align_corners=False)
        return self.block(torch.cat((upsampled, skip), dim=1))


class DilatedContext(nn.Module):
    """Multi-dilation context at the coarsest scale."""

    def __init__(self, channels: int) -> None:
        super().__init__()
        self.d1 = ResidualBlock(channels, channels, dilation=1)
        self.d2 = ResidualBlock(channels, channels, dilation=2)
        self.d4 = ResidualBlock(channels, channels, dilation=4)
        self.project = ConvNormAct(channels * 3, channels, kernel_size=1)

    def forward(self, inputs: Tensor) -> Tensor:
        return self.project(torch.cat((self.d1(inputs), self.d2(inputs), self.d4(inputs)), dim=1))


class AsymmetricConvNormAct(nn.Module):
    """Asymmetric convolution, GroupNorm, and GELU for direction-specific line context."""

    def __init__(self, channels: int, *, kernel_size: tuple[int, int], dilation: tuple[int, int] = (1, 1)) -> None:
        super().__init__()
        padding = (dilation[0] * (kernel_size[0] // 2), dilation[1] * (kernel_size[1] // 2))
        self.block = nn.Sequential(
            nn.Conv2d(channels, channels, kernel_size=kernel_size, padding=padding, dilation=dilation, bias=False),
            nn.GroupNorm(_group_count(channels), channels),
            nn.GELU(),
        )

    def forward(self, inputs: Tensor) -> Tensor:
        return self.block(inputs)


class MCASTGuidedLineRefiner(nn.Module):
    """Refine decoded features using detail, oriented line context, and MCAST support."""

    def __init__(self, channels: int) -> None:
        super().__init__()
        self.detail_project = ConvNormAct(channels, channels)
        self.horizontal = AsymmetricConvNormAct(channels, kernel_size=(1, 15))
        self.vertical = AsymmetricConvNormAct(channels, kernel_size=(15, 1))
        self.diagonal = nn.Sequential(ConvNormAct(channels, channels, dilation=2), ResidualBlock(channels, channels))
        self.support_gate = nn.Sequential(
            ConvNormAct(channels * 2, channels, kernel_size=1),
            nn.Conv2d(channels, channels, kernel_size=1, bias=True),
            nn.Sigmoid(),
        )
        self.project = nn.Sequential(
            ConvNormAct(channels * 5, channels * 2),
            ResidualBlock(channels * 2, channels * 2),
            ConvNormAct(channels * 2, channels),
            ResidualBlock(channels, channels),
        )

    def forward(self, decoded: Tensor, mcast_support: Tensor) -> Tensor:
        support = F.interpolate(mcast_support, size=decoded.shape[-2:], mode="bilinear", align_corners=False)
        detail = self.detail_project(decoded - _smooth(decoded, 9))
        horiz = self.horizontal(detail)
        vert = self.vertical(detail)
        diag = self.diagonal(decoded)
        gate = self.support_gate(torch.cat((decoded, support), dim=1))
        supported = decoded * (0.75 + 0.5 * gate)
        return self.project(torch.cat((supported, support, detail, horiz, vert + diag), dim=1))


class FullSpectralBTDMCASTGuidedDualBranchUNet(nn.Module):
    """U-Net with full-spectral BTD features calibrated by a MCAST-like thermal branch."""

    def __init__(self) -> None:
        super().__init__()
        base = 40
        self.full_front_end = NormalizedBTDFrontEnd(learned_channels=16)
        self.mcast_front_end = MCASTThermalFrontEnd()
        self.full_stem = FrequencySplitStem(self.full_front_end.out_channels, base)
        self.mcast_stem = MCASTStem(base)
        self.fuse0 = GuidedFusion(base)
        self.down1 = DualDownBlock(base, base * 2)
        self.down2 = DualDownBlock(base * 2, base * 4)
        self.down3 = DualDownBlock(base * 4, base * 8)
        self.context = DilatedContext(base * 8)
        self.up2 = UpFuseBlock(base * 8, base * 4, base * 4)
        self.up1 = UpFuseBlock(base * 4, base * 2, base * 2)
        self.up0 = UpFuseBlock(base * 2, base, base)
        self.mcast_context_project = ConvNormAct(base * 8, base, kernel_size=1)
        self.refiner = MCASTGuidedLineRefiner(base)
        self.mask_head = nn.Conv2d(base, 1, kernel_size=1)
        self.centerline_head = nn.Conv2d(base, 1, kernel_size=1)

    def forward(self, inputs: Tensor) -> dict[str, Tensor]:
        full_features = self.full_front_end(inputs)
        mcast_planes = self.mcast_front_end(inputs)
        spectral0 = self.full_stem(full_features)
        mcast0 = self.mcast_stem(mcast_planes)
        skip0 = self.fuse0(spectral0, mcast0)
        skip1, spectral1, mcast1 = self.down1(skip0, mcast0)
        skip2, spectral2, mcast2 = self.down2(skip1, mcast1)
        skip3, _spectral3, mcast3 = self.down3(skip2, mcast2)
        context = self.context(skip3)
        dec2 = self.up2(context, skip2)
        dec1 = self.up1(dec2, skip1)
        dec0 = self.up0(dec1, skip0)
        mcast_context = self.mcast_context_project(
            F.interpolate(mcast3, size=mcast0.shape[-2:], mode="bilinear", align_corners=False)
        )
        refined = self.refiner(dec0, mcast0 + mcast_context)
        return {"mask_logits": self.mask_head(refined), "centerline_logits": self.centerline_head(refined)}


def _validate_centerline_auxiliary_output(output_spec: dict[str, object]) -> None:
    auxiliary_outputs = output_spec.get("auxiliary_outputs")
    expected = [{"target": "centerline", "name": "centerline_logits", "shape": [1, 256, 256]}]
    if auxiliary_outputs != expected:
        raise ValueError(
            "abi111_fullspectral_btd_mcast_guided_dual_branch_unet_focal_tversky_centerline_aux_v1 "
            "requires exactly one trusted centerline auxiliary output named centerline_logits"
        )


def build_model(input_spec: dict[str, object], output_spec: dict[str, object]) -> nn.Module:
    """Build the model for the Harness-supplied ABI contract."""

    if input_spec.get("mode") != "abi_16ch" or input_spec.get("shape") != [16, 256, 256]:
        raise ValueError(
            "abi111_fullspectral_btd_mcast_guided_dual_branch_unet_focal_tversky_centerline_aux_v1 "
            "requires abi_16ch [16, 256, 256] input"
        )
    if output_spec.get("form") != "mask_logits" or output_spec.get("shape") != [1, 256, 256]:
        raise ValueError(
            "abi111_fullspectral_btd_mcast_guided_dual_branch_unet_focal_tversky_centerline_aux_v1 "
            "requires mask_logits [1, 256, 256] primary output"
        )
    _validate_centerline_auxiliary_output(output_spec)
    return FullSpectralBTDMCASTGuidedDualBranchUNet()
