"""Ultra-stable full-spectral BTD ConvNeXt-style U-Net repair for ABI contrail segmentation."""

from __future__ import annotations

import torch
import torch.nn.functional as F
from torch import Tensor, nn


class NormalizedBTDFrontEnd(nn.Module):
    """Build bounded normalized ABI channels and deterministic thermal-difference features."""

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
        self.out_channels = 16 + len(self._BTD_PAIRS)

    def forward(self, inputs: Tensor) -> Tensor:
        if inputs.ndim != 4 or inputs.shape[1] != 16:
            raise ValueError(f"expected [N, 16, H, W] ABI tensor, got {tuple(inputs.shape)}")
        normalized = _bounded((inputs - self.channel_means) / self.channel_scales, limit=6.0)
        btd_planes = _bounded(
            torch.cat(
                [
                    (inputs[:, a : a + 1, :, :] - inputs[:, b : b + 1, :, :]) / self._BTD_SCALE
                    for a, b in self._BTD_PAIRS
                ],
                dim=1,
            ),
            limit=6.0,
        )
        return torch.cat((normalized, btd_planes), dim=1)


def _group_count(channels: int) -> int:
    for groups in (8, 6, 4, 3, 2, 1):
        if channels % groups == 0:
            return groups
    return 1


def _bounded(inputs: Tensor, limit: float = 12.0) -> Tensor:
    """Clamp internal activations to keep the repair focused on finite ConvNeXt evidence."""

    return torch.clamp(inputs, min=-limit, max=limit)


class ConvNormAct(nn.Module):
    """Convolution, GroupNorm, and GELU activation for stable small-batch training."""

    def __init__(self, in_channels: int, out_channels: int, *, kernel_size: int = 3, stride: int = 1) -> None:
        super().__init__()
        self.block = nn.Sequential(
            nn.Conv2d(
                in_channels,
                out_channels,
                kernel_size=kernel_size,
                stride=stride,
                padding=kernel_size // 2,
                bias=False,
            ),
            nn.GroupNorm(_group_count(out_channels), out_channels),
            nn.GELU(),
        )

    def forward(self, inputs: Tensor) -> Tensor:
        return _bounded(self.block(inputs))


class ConvNeXtBlock(nn.Module):
    """Small-batch-safe ConvNeXt-style residual block with bounded depthwise context."""

    def __init__(self, channels: int, *, kernel_size: int = 7, expansion: int = 3) -> None:
        super().__init__()
        hidden_channels = channels * expansion
        self.depthwise = nn.Conv2d(
            channels,
            channels,
            kernel_size=kernel_size,
            padding=kernel_size // 2,
            groups=channels,
            bias=True,
        )
        self.norm = nn.GroupNorm(_group_count(channels), channels)
        self.pointwise = nn.Sequential(
            nn.Conv2d(channels, hidden_channels, kernel_size=1, bias=True),
            nn.GELU(),
            nn.Conv2d(hidden_channels, channels, kernel_size=1, bias=True),
        )
        self.gamma = nn.Parameter(torch.full((1, channels, 1, 1), 1.0e-4))

    def forward(self, inputs: Tensor) -> Tensor:
        residual = _bounded(self.pointwise(self.norm(self.depthwise(inputs))))
        return _bounded(inputs + self.gamma * residual)


class ConvNeXtStage(nn.Module):
    """Projection followed by repeated ConvNeXt blocks."""

    def __init__(self, in_channels: int, out_channels: int, *, depth: int) -> None:
        super().__init__()
        self.project = ConvNormAct(in_channels, out_channels, kernel_size=1)
        self.blocks = nn.Sequential(*[ConvNeXtBlock(out_channels) for _ in range(depth)])

    def forward(self, inputs: Tensor) -> Tensor:
        return self.blocks(self.project(inputs))


class DownsampleStage(nn.Module):
    """Halve resolution, increase channels, and apply ConvNeXt context blocks."""

    def __init__(self, in_channels: int, out_channels: int, *, depth: int) -> None:
        super().__init__()
        self.down = ConvNormAct(in_channels, out_channels, kernel_size=3, stride=2)
        self.blocks = nn.Sequential(*[ConvNeXtBlock(out_channels) for _ in range(depth)])

    def forward(self, inputs: Tensor) -> Tensor:
        return self.blocks(self.down(inputs))


class AtrousConvNeXtContext(nn.Module):
    """Low-resolution context block using depthwise large kernels and dilated convolutions."""

    def __init__(self, channels: int) -> None:
        super().__init__()
        self.local = ConvNeXtBlock(channels)
        self.dilated2 = nn.Sequential(
            nn.Conv2d(channels, channels, kernel_size=3, padding=2, dilation=2, groups=channels, bias=True),
            nn.GroupNorm(_group_count(channels), channels),
            nn.GELU(),
            nn.Conv2d(channels, channels, kernel_size=1, bias=True),
        )
        self.dilated4 = nn.Sequential(
            nn.Conv2d(channels, channels, kernel_size=3, padding=4, dilation=4, groups=channels, bias=True),
            nn.GroupNorm(_group_count(channels), channels),
            nn.GELU(),
            nn.Conv2d(channels, channels, kernel_size=1, bias=True),
        )
        self.project = ConvNormAct(channels * 3, channels, kernel_size=1)
        self.refine = nn.Sequential(ConvNeXtBlock(channels), ConvNeXtBlock(channels))

    def forward(self, inputs: Tensor) -> Tensor:
        dilated2 = _bounded(self.dilated2(inputs))
        dilated4 = _bounded(self.dilated4(inputs))
        fused = self.project(torch.cat((self.local(inputs), dilated2, dilated4), dim=1))
        return self.refine(fused)


class UpFuseStage(nn.Module):
    """Upsample decoder features, concatenate a skip, and refine without multiplicative gating."""

    def __init__(self, in_channels: int, skip_channels: int, out_channels: int, *, depth: int) -> None:
        super().__init__()
        self.fuse = ConvNormAct(in_channels + skip_channels, out_channels, kernel_size=1)
        self.blocks = nn.Sequential(*[ConvNeXtBlock(out_channels) for _ in range(depth)])

    def forward(self, inputs: Tensor, skip: Tensor) -> Tensor:
        upsampled = F.interpolate(inputs, size=skip.shape[-2:], mode="bilinear", align_corners=False)
        return self.blocks(self.fuse(torch.cat((upsampled, skip), dim=1)))


class HighResolutionRefiner(nn.Module):
    """Final high-resolution context/detail refinement before primary and auxiliary logits."""

    def __init__(self, channels: int) -> None:
        super().__init__()
        self.detail = nn.Sequential(
            nn.Conv2d(channels, channels, kernel_size=3, padding=1, groups=channels, bias=True),
            nn.GroupNorm(_group_count(channels), channels),
            nn.GELU(),
            nn.Conv2d(channels, channels, kernel_size=1, bias=True),
        )
        self.context = nn.Sequential(
            nn.AvgPool2d(kernel_size=9, stride=1, padding=4, count_include_pad=False),
            ConvNeXtBlock(channels, kernel_size=7),
        )
        self.project = nn.Sequential(
            ConvNormAct(channels * 3, channels, kernel_size=1),
            ConvNeXtBlock(channels),
        )

    def forward(self, inputs: Tensor, stem: Tensor) -> Tensor:
        detail = _bounded(self.detail(inputs))
        context = self.context(inputs)
        return self.project(torch.cat((_bounded(inputs + stem), detail, context), dim=1))


class UltraStableFullSpectralBTDConvNeXtUNet(nn.Module):
    """ConvNeXt-style U-Net with deterministic BTD features and centerline auxiliary output."""

    def __init__(self) -> None:
        super().__init__()
        self.front_end = NormalizedBTDFrontEnd()
        base = 48
        self.stem = ConvNeXtStage(self.front_end.out_channels, base, depth=2)
        self.down1 = DownsampleStage(base, base * 2, depth=2)
        self.down2 = DownsampleStage(base * 2, base * 4, depth=3)
        self.down3 = DownsampleStage(base * 4, base * 8, depth=3)
        self.context = AtrousConvNeXtContext(base * 8)
        self.up2 = UpFuseStage(base * 8, base * 4, base * 4, depth=2)
        self.up1 = UpFuseStage(base * 4, base * 2, base * 2, depth=2)
        self.up0 = UpFuseStage(base * 2, base, base, depth=2)
        self.refiner = HighResolutionRefiner(base)
        self.mask_head = nn.Conv2d(base, 1, kernel_size=1)
        self.centerline_head = nn.Conv2d(base, 1, kernel_size=1)

    def forward(self, inputs: Tensor) -> dict[str, Tensor]:
        features = self.front_end(inputs)
        stem = self.stem(features)
        enc2 = self.down1(stem)
        enc3 = self.down2(enc2)
        enc4 = self.down3(enc3)
        context = self.context(enc4)
        dec2 = self.up2(context, enc3)
        dec1 = self.up1(dec2, enc2)
        dec0 = self.up0(dec1, stem)
        refined = self.refiner(dec0, stem)
        return {
            "mask_logits": self.mask_head(refined),
            "centerline_logits": self.centerline_head(refined),
        }


def _validate_centerline_auxiliary_output(output_spec: dict[str, object]) -> None:
    auxiliary_outputs = output_spec.get("auxiliary_outputs")
    expected = [{"target": "centerline", "name": "centerline_logits", "shape": [1, 256, 256]}]
    if auxiliary_outputs != expected:
        raise ValueError(
            "abi102_fullspectral_btd_convnext_unet_ultrastable_focal_tversky_centerline_aux_v1 requires "
            "exactly one trusted centerline auxiliary output named centerline_logits"
        )


def build_model(input_spec: dict[str, object], output_spec: dict[str, object]) -> nn.Module:
    """Build the model for the Harness-supplied ABI contract."""

    if input_spec.get("mode") != "abi_16ch" or input_spec.get("shape") != [16, 256, 256]:
        raise ValueError(
            "abi102_fullspectral_btd_convnext_unet_ultrastable_focal_tversky_centerline_aux_v1 requires "
            "abi_16ch [16, 256, 256] input"
        )
    if output_spec.get("form") != "mask_logits" or output_spec.get("shape") != [1, 256, 256]:
        raise ValueError(
            "abi102_fullspectral_btd_convnext_unet_ultrastable_focal_tversky_centerline_aux_v1 requires "
            "mask_logits [1, 256, 256] primary output"
        )
    _validate_centerline_auxiliary_output(output_spec)
    return UltraStableFullSpectralBTDConvNeXtUNet()
