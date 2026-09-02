"""Stable full-spectral BTD large-kernel line-context network for ABI contrail segmentation."""

from __future__ import annotations

import torch
import torch.nn.functional as F
from torch import Tensor, nn


class NormalizedBTDFrontEnd(nn.Module):
    """Build normalized raw, thermal-difference, and learned ABI channel features."""

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
            nn.Conv2d(16, learned_channels, kernel_size=1, bias=True),
            nn.GELU(),
        )
        self.out_channels = 16 + len(self._BTD_PAIRS) + learned_channels

    def forward(self, inputs: Tensor) -> Tensor:
        if inputs.ndim != 4 or inputs.shape[1] != 16:
            raise ValueError(f"expected [N, 16, H, W] ABI tensor, got {tuple(inputs.shape)}")
        normalized = torch.clamp((inputs - self.channel_means) / self.channel_scales, min=-8.0, max=8.0)
        btd_planes = torch.clamp(
            torch.cat(
                [
                    (inputs[:, a : a + 1, :, :] - inputs[:, b : b + 1, :, :]) / self._BTD_SCALE
                    for a, b in self._BTD_PAIRS
                ],
                dim=1,
            ),
            min=-8.0,
            max=8.0,
        )
        learned = self.learned_mixer(normalized)
        return torch.cat((normalized, btd_planes, learned), dim=1)


def _group_count(channels: int) -> int:
    for groups in (8, 6, 4, 3, 2, 1):
        if channels % groups == 0:
            return groups
    return 1


def _pair(value: int | tuple[int, int]) -> tuple[int, int]:
    if isinstance(value, tuple):
        return value
    return (value, value)


class ConvNormAct(nn.Module):
    """Convolution, GroupNorm, and GELU activation for stable small-batch training."""

    def __init__(
        self,
        in_channels: int,
        out_channels: int,
        *,
        kernel_size: int | tuple[int, int] = 3,
        dilation: int | tuple[int, int] = 1,
        groups: int = 1,
    ) -> None:
        super().__init__()
        kernel_pair = _pair(kernel_size)
        dilation_pair = _pair(dilation)
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
                groups=groups,
                bias=False,
            ),
            nn.GroupNorm(_group_count(out_channels), out_channels),
            nn.GELU(),
        )

    def forward(self, inputs: Tensor) -> Tensor:
        return self.block(inputs)


class PointwiseFFN(nn.Module):
    """ConvNeXt-style channel mixing block with bounded residual contribution."""

    def __init__(self, channels: int, expansion: int = 3, residual_scale: float = 0.2) -> None:
        super().__init__()
        hidden = channels * expansion
        self.residual_scale = residual_scale
        self.net = nn.Sequential(
            nn.Conv2d(channels, hidden, kernel_size=1, bias=True),
            nn.GELU(),
            nn.Conv2d(hidden, channels, kernel_size=1, bias=True),
        )

    def forward(self, inputs: Tensor) -> Tensor:
        return inputs + self.residual_scale * self.net(inputs)


class LargeKernelLineBlock(nn.Module):
    """Depthwise large-kernel axial context block for thin linear structure."""

    def __init__(
        self,
        in_channels: int,
        out_channels: int,
        *,
        kernel_size: int = 21,
        residual_scale: float = 0.2,
    ) -> None:
        super().__init__()
        self.residual_scale = residual_scale
        self.project = (
            nn.Identity()
            if in_channels == out_channels
            else ConvNormAct(in_channels, out_channels, kernel_size=1)
        )
        self.local = ConvNormAct(out_channels, out_channels, groups=out_channels)
        self.horizontal = ConvNormAct(
            out_channels,
            out_channels,
            kernel_size=(1, kernel_size),
            groups=out_channels,
        )
        self.vertical = ConvNormAct(
            out_channels,
            out_channels,
            kernel_size=(kernel_size, 1),
            groups=out_channels,
        )
        self.dilated = ConvNormAct(out_channels, out_channels, dilation=3, groups=out_channels)
        self.mix = ConvNormAct(out_channels * 4, out_channels, kernel_size=1)
        self.ffn = PointwiseFFN(out_channels)

    def forward(self, inputs: Tensor) -> Tensor:
        projected = self.project(inputs)
        branches = (
            self.local(projected),
            self.horizontal(projected),
            self.vertical(projected),
            self.dilated(projected),
        )
        mixed = self.mix(torch.cat(branches, dim=1))
        return self.ffn(projected + self.residual_scale * mixed)


class LargeKernelStage(nn.Module):
    """Two line-context blocks at one resolution."""

    def __init__(self, in_channels: int, out_channels: int, *, kernel_size: int = 21) -> None:
        super().__init__()
        self.blocks = nn.Sequential(
            LargeKernelLineBlock(in_channels, out_channels, kernel_size=kernel_size),
            LargeKernelLineBlock(out_channels, out_channels, kernel_size=kernel_size),
        )

    def forward(self, inputs: Tensor) -> Tensor:
        return self.blocks(inputs)


class DownStage(nn.Module):
    """Downsample and apply large-kernel line-context processing."""

    def __init__(self, in_channels: int, out_channels: int, *, kernel_size: int = 21) -> None:
        super().__init__()
        self.net = nn.Sequential(
            nn.MaxPool2d(2),
            LargeKernelStage(in_channels, out_channels, kernel_size=kernel_size),
        )

    def forward(self, inputs: Tensor) -> Tensor:
        return self.net(inputs)


class PyramidLineContext(nn.Module):
    """Low-resolution multi-dilation context without transformer memory cost."""

    def __init__(self, channels: int) -> None:
        super().__init__()
        self.d1 = ConvNormAct(channels, channels, dilation=1, groups=channels)
        self.d3 = ConvNormAct(channels, channels, dilation=3, groups=channels)
        self.d5 = ConvNormAct(channels, channels, dilation=5, groups=channels)
        self.global_project = ConvNormAct(channels, channels, kernel_size=1)
        self.mix = nn.Sequential(
            ConvNormAct(channels * 4, channels, kernel_size=1),
            PointwiseFFN(channels),
        )

    def forward(self, inputs: Tensor) -> Tensor:
        pooled = F.adaptive_avg_pool2d(inputs, output_size=1)
        global_context = F.interpolate(self.global_project(pooled), size=inputs.shape[-2:], mode="bilinear", align_corners=False)
        return self.mix(torch.cat((self.d1(inputs), self.d3(inputs), self.d5(inputs), global_context), dim=1))


class UpLineFuse(nn.Module):
    """Upsample decoder features and fuse with same-resolution encoder context."""

    def __init__(self, in_channels: int, skip_channels: int, out_channels: int, *, kernel_size: int = 15) -> None:
        super().__init__()
        self.skip_project = ConvNormAct(skip_channels, out_channels, kernel_size=1)
        self.up_project = ConvNormAct(in_channels, out_channels, kernel_size=1)
        self.fuse = LargeKernelStage(out_channels * 2, out_channels, kernel_size=kernel_size)

    def forward(self, inputs: Tensor, skip: Tensor) -> Tensor:
        upsampled = F.interpolate(inputs, size=skip.shape[-2:], mode="bilinear", align_corners=False)
        return self.fuse(torch.cat((self.up_project(upsampled), self.skip_project(skip)), dim=1))


class MultiScaleLineHead(nn.Module):
    """Fuse shallow detail with upsampled decoder context before final logits."""

    def __init__(self, base_channels: int) -> None:
        super().__init__()
        self.dec1_project = ConvNormAct(base_channels * 2, base_channels, kernel_size=1)
        self.dec2_project = ConvNormAct(base_channels * 4, base_channels, kernel_size=1)
        self.stem_project = ConvNormAct(base_channels, base_channels, kernel_size=1)
        self.fuse = nn.Sequential(
            ConvNormAct(base_channels * 4, base_channels * 2),
            LargeKernelLineBlock(base_channels * 2, base_channels, kernel_size=15),
            LargeKernelLineBlock(base_channels, base_channels, kernel_size=15),
        )

    def forward(self, dec0: Tensor, dec1: Tensor, dec2: Tensor, stem: Tensor) -> Tensor:
        target_size = dec0.shape[-2:]
        dec1_full = self.dec1_project(F.interpolate(dec1, size=target_size, mode="bilinear", align_corners=False))
        dec2_full = self.dec2_project(F.interpolate(dec2, size=target_size, mode="bilinear", align_corners=False))
        stem_full = self.stem_project(stem)
        return self.fuse(torch.cat((dec0, dec1_full, dec2_full, stem_full), dim=1))


class StableFullSpectralBTDLargeKernelLineContextNet(nn.Module):
    """Residual-scaled large-kernel depthwise line-context encoder-decoder for ABI patches."""

    def __init__(self) -> None:
        super().__init__()
        self.front_end = NormalizedBTDFrontEnd(learned_channels=16)
        base = 48
        self.stem = nn.Sequential(
            ConvNormAct(self.front_end.out_channels, base, kernel_size=1),
            LargeKernelLineBlock(base, base, kernel_size=15),
        )
        self.enc1 = LargeKernelStage(base, base, kernel_size=15)
        self.enc2 = DownStage(base, base * 2, kernel_size=17)
        self.enc3 = DownStage(base * 2, base * 4, kernel_size=19)
        self.enc4 = DownStage(base * 4, base * 8, kernel_size=21)
        self.context = PyramidLineContext(base * 8)
        self.up2 = UpLineFuse(base * 8, base * 4, base * 4, kernel_size=17)
        self.up1 = UpLineFuse(base * 4, base * 2, base * 2, kernel_size=15)
        self.up0 = UpLineFuse(base * 2, base, base, kernel_size=15)
        self.head_features = MultiScaleLineHead(base)
        self.mask_head = nn.Conv2d(base, 1, kernel_size=1)
        self.centerline_head = nn.Conv2d(base, 1, kernel_size=1)

    def forward(self, inputs: Tensor) -> dict[str, Tensor]:
        features = self.front_end(inputs)
        stem = self.stem(features)
        enc1 = self.enc1(stem)
        enc2 = self.enc2(enc1)
        enc3 = self.enc3(enc2)
        enc4 = self.enc4(enc3)
        context = self.context(enc4)
        dec2 = self.up2(context, enc3)
        dec1 = self.up1(dec2, enc2)
        dec0 = self.up0(dec1, enc1)
        refined = self.head_features(dec0, dec1, dec2, stem)
        return {
            "mask_logits": self.mask_head(refined),
            "centerline_logits": self.centerline_head(refined),
        }


def _validate_centerline_auxiliary_output(output_spec: dict[str, object]) -> None:
    auxiliary_outputs = output_spec.get("auxiliary_outputs")
    expected = [{"target": "centerline", "name": "centerline_logits", "shape": [1, 256, 256]}]
    if auxiliary_outputs != expected:
        raise ValueError(
            "abi094_fullspectral_btd_large_kernel_line_context_net_stable_syntax_repair_v1 requires "
            "exactly one trusted centerline auxiliary output named centerline_logits"
        )


def build_model(input_spec: dict[str, object], output_spec: dict[str, object]) -> nn.Module:
    """Build the model for the Harness-supplied ABI contract."""

    if input_spec.get("mode") != "abi_16ch" or input_spec.get("shape") != [16, 256, 256]:
        raise ValueError(
            "abi094_fullspectral_btd_large_kernel_line_context_net_stable_syntax_repair_v1 requires "
            "abi_16ch [16, 256, 256] input"
        )
    if output_spec.get("form") != "mask_logits" or output_spec.get("shape") != [1, 256, 256]:
        raise ValueError(
            "abi094_fullspectral_btd_large_kernel_line_context_net_stable_syntax_repair_v1 requires "
            "mask_logits [1, 256, 256] primary output"
        )
    _validate_centerline_auxiliary_output(output_spec)
    return StableFullSpectralBTDLargeKernelLineContextNet()
