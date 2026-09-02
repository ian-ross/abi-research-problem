"""Dual-stream spectral-gate line U-Net for GOES ABI contrail segmentation."""

from __future__ import annotations

import torch
import torch.nn.functional as F
from torch import Tensor, nn


class SpectralBTDInputs(nn.Module):
    """Normalize approved ABI channels and build deterministic thermal BTD planes."""

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

    def __init__(self) -> None:
        super().__init__()
        self.register_buffer(
            "channel_means",
            torch.tensor(self._CHANNEL_MEANS, dtype=torch.float32).view(1, 16, 1, 1),
        )
        self.register_buffer(
            "channel_scales",
            torch.tensor(self._CHANNEL_SCALES, dtype=torch.float32).view(1, 16, 1, 1),
        )

    def forward(self, inputs: Tensor) -> tuple[Tensor, Tensor, Tensor]:
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
        reflective = normalized[:, :6, :, :]
        thermal = normalized[:, 6:, :, :]
        return reflective, thermal, btd_planes


def _group_count(channels: int) -> int:
    for groups in (8, 6, 4, 3, 2, 1):
        if channels % groups == 0:
            return groups
    return 1


def _smooth(inputs: Tensor, kernel_size: int) -> Tensor:
    padding = kernel_size // 2
    return F.avg_pool2d(inputs, kernel_size=kernel_size, stride=1, padding=padding, count_include_pad=False)


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
    """Residual block with GroupNorm for small batches."""

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


class AsymmetricConvNormAct(nn.Module):
    """Asymmetric convolution for horizontal or vertical line context."""

    def __init__(self, channels: int, *, kernel_size: tuple[int, int], dilation: tuple[int, int] = (1, 1)) -> None:
        super().__init__()
        padding = (
            dilation[0] * (kernel_size[0] // 2),
            dilation[1] * (kernel_size[1] // 2),
        )
        self.block = nn.Sequential(
            nn.Conv2d(
                channels,
                channels,
                kernel_size=kernel_size,
                padding=padding,
                dilation=dilation,
                bias=False,
            ),
            nn.GroupNorm(_group_count(channels), channels),
            nn.GELU(),
        )

    def forward(self, inputs: Tensor) -> Tensor:
        return self.block(inputs)


class SpectralGateStem(nn.Module):
    """Separate reflective, thermal, and BTD streams before bounded cross-stream fusion."""

    def __init__(self, out_channels: int) -> None:
        super().__init__()
        self.reflective_stem = nn.Sequential(ConvNormAct(6, out_channels), ResidualBlock(out_channels, out_channels))
        self.thermal_stem = nn.Sequential(ConvNormAct(10, out_channels), ResidualBlock(out_channels, out_channels))
        self.btd_stem = nn.Sequential(ConvNormAct(8, out_channels), ResidualBlock(out_channels, out_channels))
        self.reflective_gate = nn.Sequential(
            ConvNormAct(out_channels * 2, out_channels, kernel_size=1),
            nn.Conv2d(out_channels, out_channels, kernel_size=1, bias=True),
            nn.Sigmoid(),
        )
        self.thermal_gate = nn.Sequential(
            ConvNormAct(out_channels * 2, out_channels, kernel_size=1),
            nn.Conv2d(out_channels, out_channels, kernel_size=1, bias=True),
            nn.Sigmoid(),
        )
        self.btd_gate = nn.Sequential(
            ConvNormAct(out_channels * 2, out_channels, kernel_size=1),
            nn.Conv2d(out_channels, out_channels, kernel_size=1, bias=True),
            nn.Sigmoid(),
        )
        self.fuse = nn.Sequential(
            ConvNormAct(out_channels * 4, out_channels),
            ResidualBlock(out_channels, out_channels),
        )

    def forward(self, reflective: Tensor, thermal: Tensor, btd: Tensor) -> Tensor:
        refl = self.reflective_stem(reflective)
        therm = self.thermal_stem(thermal)
        btd_features = self.btd_stem(btd)
        refl_gate = self.reflective_gate(torch.cat((therm, btd_features), dim=1))
        therm_gate = self.thermal_gate(torch.cat((refl, btd_features), dim=1))
        btd_gate = self.btd_gate(torch.cat((refl, therm), dim=1))
        gated_refl = refl * (0.5 + refl_gate)
        gated_therm = therm * (0.5 + therm_gate)
        gated_btd = btd_features * (0.5 + btd_gate)
        agreement = gated_refl * torch.sigmoid(gated_therm + gated_btd)
        return self.fuse(torch.cat((gated_refl, gated_therm, gated_btd, agreement), dim=1))


class UpFuseBlock(nn.Module):
    """Upsample decoder features and fuse them with a low-frequency-gated skip."""

    def __init__(self, in_channels: int, skip_channels: int, out_channels: int) -> None:
        super().__init__()
        self.skip_gate = nn.Sequential(
            nn.Conv2d(skip_channels * 2, skip_channels, kernel_size=1, bias=True),
            nn.Sigmoid(),
        )
        self.fuse = nn.Sequential(
            ConvNormAct(in_channels + skip_channels, out_channels),
            ResidualBlock(out_channels, out_channels),
        )

    def forward(self, inputs: Tensor, skip: Tensor) -> Tensor:
        upsampled = F.interpolate(inputs, size=skip.shape[-2:], mode="bilinear", align_corners=False)
        skip_context = _smooth(skip, 9)
        gated_skip = skip * (0.5 + self.skip_gate(torch.cat((skip, skip_context), dim=1)))
        return self.fuse(torch.cat((upsampled, gated_skip), dim=1))


class DilatedLineContext(nn.Module):
    """Coarse-scale context with dilated and asymmetric line branches."""

    def __init__(self, channels: int) -> None:
        super().__init__()
        self.local = ResidualBlock(channels, channels, dilation=1)
        self.dilated = ResidualBlock(channels, channels, dilation=3)
        self.horizontal = AsymmetricConvNormAct(channels, kernel_size=(1, 15))
        self.vertical = AsymmetricConvNormAct(channels, kernel_size=(15, 1))
        self.project = nn.Sequential(
            ConvNormAct(channels * 4, channels, kernel_size=1),
            ResidualBlock(channels, channels),
        )

    def forward(self, inputs: Tensor) -> Tensor:
        return self.project(
            torch.cat((self.local(inputs), self.dilated(inputs), self.horizontal(inputs), self.vertical(inputs)), dim=1)
        )


class FullResolutionLineConsensus(nn.Module):
    """Fuse multi-scale decoder features with local detail and oriented line evidence."""

    def __init__(self, base_channels: int) -> None:
        super().__init__()
        self.dec1_project = ConvNormAct(base_channels * 2, base_channels, kernel_size=1)
        self.dec2_project = ConvNormAct(base_channels * 4, base_channels, kernel_size=1)
        self.context_project = ConvNormAct(base_channels * 8, base_channels, kernel_size=1)
        self.pre_fuse = nn.Sequential(
            ConvNormAct(base_channels * 5, base_channels * 2),
            ResidualBlock(base_channels * 2, base_channels * 2),
            ConvNormAct(base_channels * 2, base_channels),
        )
        self.horizontal = AsymmetricConvNormAct(base_channels, kernel_size=(1, 17))
        self.vertical = AsymmetricConvNormAct(base_channels, kernel_size=(17, 1))
        self.broad = nn.Sequential(ConvNormAct(base_channels, base_channels, dilation=2), ConvNormAct(base_channels, base_channels, dilation=4))
        self.orientation_logits = nn.Conv2d(base_channels * 3, 3, kernel_size=1, bias=True)
        self.output = nn.Sequential(
            ConvNormAct(base_channels * 4, base_channels),
            ResidualBlock(base_channels, base_channels),
        )

    def forward(self, dec0: Tensor, dec1: Tensor, dec2: Tensor, context: Tensor) -> Tensor:
        target_size = dec0.shape[-2:]
        dec1_full = self.dec1_project(F.interpolate(dec1, size=target_size, mode="bilinear", align_corners=False))
        dec2_full = self.dec2_project(F.interpolate(dec2, size=target_size, mode="bilinear", align_corners=False))
        context_full = self.context_project(F.interpolate(context, size=target_size, mode="bilinear", align_corners=False))
        detail = dec0 - _smooth(dec0, 9)
        smooth_context = _smooth(dec0, 21)
        fused = self.pre_fuse(torch.cat((dec0, detail, smooth_context, dec1_full, dec2_full), dim=1))
        branches = (self.horizontal(fused), self.vertical(fused), self.broad(fused + context_full))
        branch_stack = torch.stack(branches, dim=1)
        weights = torch.softmax(self.orientation_logits(torch.cat(branches, dim=1)), dim=1).unsqueeze(2)
        oriented = (branch_stack * weights).sum(dim=1)
        return self.output(torch.cat((fused, detail, context_full, oriented), dim=1))


class FullSpectralBTDDualStreamSpectralGateLineUNet(nn.Module):
    """Dual-stream spectral-gate residual U-Net for thin contrail masks."""

    def __init__(self) -> None:
        super().__init__()
        base = 40
        self.inputs = SpectralBTDInputs()
        self.stem = SpectralGateStem(base)
        self.enc0 = ResidualBlock(base, base)
        self.down1 = nn.Sequential(nn.MaxPool2d(2), ResidualBlock(base, base * 2))
        self.down2 = nn.Sequential(nn.MaxPool2d(2), ResidualBlock(base * 2, base * 4))
        self.down3 = nn.Sequential(nn.MaxPool2d(2), ResidualBlock(base * 4, base * 8))
        self.context = DilatedLineContext(base * 8)
        self.up2 = UpFuseBlock(base * 8, base * 4, base * 4)
        self.up1 = UpFuseBlock(base * 4, base * 2, base * 2)
        self.up0 = UpFuseBlock(base * 2, base, base)
        self.line_consensus = FullResolutionLineConsensus(base)
        self.mask_head = nn.Conv2d(base, 1, kernel_size=1)
        self.centerline_head = nn.Conv2d(base, 1, kernel_size=1)

    def forward(self, inputs: Tensor) -> dict[str, Tensor]:
        reflective, thermal, btd = self.inputs(inputs)
        stem = self.stem(reflective, thermal, btd)
        enc0 = self.enc0(stem)
        enc1 = self.down1(enc0)
        enc2 = self.down2(enc1)
        enc3 = self.down3(enc2)
        context = self.context(enc3)
        dec2 = self.up2(context, enc2)
        dec1 = self.up1(dec2, enc1)
        dec0 = self.up0(dec1, enc0)
        refined = self.line_consensus(dec0, dec1, dec2, context)
        return {
            "mask_logits": self.mask_head(refined),
            "centerline_logits": self.centerline_head(refined),
        }


def _validate_centerline_auxiliary_output(output_spec: dict[str, object]) -> None:
    auxiliary_outputs = output_spec.get("auxiliary_outputs")
    expected = [{"target": "centerline", "name": "centerline_logits", "shape": [1, 256, 256]}]
    if auxiliary_outputs != expected:
        raise ValueError(
            "abi103_fullspectral_btd_dual_stream_spectral_gate_line_unet_focal_tversky_centerline_aux_v1 "
            "requires exactly one trusted centerline auxiliary output named centerline_logits"
        )


def build_model(input_spec: dict[str, object], output_spec: dict[str, object]) -> nn.Module:
    """Build the model for the Harness-supplied ABI contract."""

    if input_spec.get("mode") != "abi_16ch" or input_spec.get("shape") != [16, 256, 256]:
        raise ValueError(
            "abi103_fullspectral_btd_dual_stream_spectral_gate_line_unet_focal_tversky_centerline_aux_v1 "
            "requires abi_16ch [16, 256, 256] input"
        )
    if output_spec.get("form") != "mask_logits" or output_spec.get("shape") != [1, 256, 256]:
        raise ValueError(
            "abi103_fullspectral_btd_dual_stream_spectral_gate_line_unet_focal_tversky_centerline_aux_v1 "
            "requires mask_logits [1, 256, 256] primary output"
        )
    _validate_centerline_auxiliary_output(output_spec)
    return FullSpectralBTDDualStreamSpectralGateLineUNet()
