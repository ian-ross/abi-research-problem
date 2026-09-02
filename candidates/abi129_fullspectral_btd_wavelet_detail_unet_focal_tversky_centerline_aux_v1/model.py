"""Full-spectral BTD wavelet-detail U-Net for ABI contrail segmentation."""

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


def _group_count(channels: int) -> int:
    for groups in (8, 6, 5, 4, 3, 2, 1):
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


class WaveletDetailDownsample(nn.Module):
    """Downsample while retaining fixed high-frequency residual magnitude evidence."""

    def __init__(self, in_channels: int, out_channels: int) -> None:
        super().__init__()
        self.low_project = ConvNormAct(in_channels, out_channels, kernel_size=1)
        self.detail_project = ConvNormAct(in_channels, out_channels, kernel_size=1)
        self.fuse = nn.Sequential(
            ConvNormAct(out_channels * 2, out_channels),
            ResidualBlock(out_channels, out_channels),
        )

    def forward(self, inputs: Tensor) -> Tensor:
        low = F.avg_pool2d(inputs, kernel_size=2, stride=2)
        up_low = F.interpolate(low, size=inputs.shape[-2:], mode="bilinear", align_corners=False)
        detail = F.avg_pool2d(torch.abs(inputs - up_low), kernel_size=2, stride=2)
        return self.fuse(torch.cat((self.low_project(low), self.detail_project(detail)), dim=1))


class WaveletSplitStem(nn.Module):
    """Fuse raw ABI/BTD features with local and broad residual detail at full resolution."""

    def __init__(self, in_channels: int, out_channels: int) -> None:
        super().__init__()
        self.raw_project = ConvNormAct(in_channels, out_channels, kernel_size=1)
        self.local_detail_project = ConvNormAct(in_channels, out_channels, kernel_size=1)
        self.broad_detail_project = ConvNormAct(in_channels, out_channels, kernel_size=1)
        self.context_project = ConvNormAct(in_channels, out_channels, kernel_size=1)
        self.fuse = nn.Sequential(
            ConvNormAct(out_channels * 4, out_channels),
            ResidualBlock(out_channels, out_channels),
        )

    def forward(self, inputs: Tensor) -> Tensor:
        local = _smooth(inputs, 7)
        broad = _smooth(inputs, 21)
        local_detail = inputs - local
        broad_detail = local - broad
        return self.fuse(
            torch.cat(
                (
                    self.raw_project(inputs),
                    self.local_detail_project(local_detail),
                    self.broad_detail_project(broad_detail),
                    self.context_project(broad),
                ),
                dim=1,
            )
        )


class ContextGatedUpFuse(nn.Module):
    """Upsample decoder features and fuse with context-gated, detail-aware skips."""

    def __init__(self, in_channels: int, skip_channels: int, out_channels: int) -> None:
        super().__init__()
        self.skip_detail_project = ConvNormAct(skip_channels, skip_channels, kernel_size=1)
        self.gate = nn.Sequential(
            ConvNormAct(in_channels + skip_channels * 2, skip_channels, kernel_size=1),
            nn.Conv2d(skip_channels, skip_channels, kernel_size=1, bias=True),
            nn.Sigmoid(),
        )
        self.fuse = nn.Sequential(
            ConvNormAct(in_channels + skip_channels * 2, out_channels),
            ResidualBlock(out_channels, out_channels),
        )

    def forward(self, inputs: Tensor, skip: Tensor) -> Tensor:
        upsampled = F.interpolate(inputs, size=skip.shape[-2:], mode="bilinear", align_corners=False)
        skip_context = _smooth(skip, 11)
        skip_detail = self.skip_detail_project(skip - skip_context)
        gate = self.gate(torch.cat((upsampled, skip, skip_context), dim=1))
        gated_skip = skip * (0.75 + 0.5 * gate)
        return self.fuse(torch.cat((upsampled, gated_skip, skip_detail), dim=1))


class DilatedContext(nn.Module):
    """Multi-dilation context at the coarsest scale."""

    def __init__(self, channels: int) -> None:
        super().__init__()
        self.d1 = ResidualBlock(channels, channels, dilation=1)
        self.d2 = ResidualBlock(channels, channels, dilation=2)
        self.d4 = ResidualBlock(channels, channels, dilation=4)
        self.d8 = ResidualBlock(channels, channels, dilation=8)
        self.project = ConvNormAct(channels * 4, channels, kernel_size=1)

    def forward(self, inputs: Tensor) -> Tensor:
        return self.project(torch.cat((self.d1(inputs), self.d2(inputs), self.d4(inputs), self.d8(inputs)), dim=1))


class AsymmetricConvNormAct(nn.Module):
    """Asymmetric convolution, GroupNorm, and GELU for line-oriented context."""

    def __init__(self, channels: int, *, kernel_size: tuple[int, int]) -> None:
        super().__init__()
        padding = (kernel_size[0] // 2, kernel_size[1] // 2)
        self.block = nn.Sequential(
            nn.Conv2d(channels, channels, kernel_size=kernel_size, padding=padding, bias=False),
            nn.GroupNorm(_group_count(channels), channels),
            nn.GELU(),
        )

    def forward(self, inputs: Tensor) -> Tensor:
        return self.block(inputs)


class WaveletLineHead(nn.Module):
    """Line-aware full-resolution fusion over local detail and broad context."""

    def __init__(self, channels: int) -> None:
        super().__init__()
        self.detail_project = ConvNormAct(channels, channels)
        self.context_project = ConvNormAct(channels, channels, kernel_size=1)
        self.horizontal = nn.Sequential(
            AsymmetricConvNormAct(channels, kernel_size=(1, 15)),
            ResidualBlock(channels, channels),
        )
        self.vertical = nn.Sequential(
            AsymmetricConvNormAct(channels, kernel_size=(15, 1)),
            ResidualBlock(channels, channels),
        )
        self.orientation_logits = nn.Conv2d(channels * 2, 2, kernel_size=1, bias=True)
        self.fuse = nn.Sequential(
            ConvNormAct(channels * 4, channels * 2),
            ResidualBlock(channels * 2, channels * 2),
            ConvNormAct(channels * 2, channels),
            ResidualBlock(channels, channels),
        )

    def forward(self, inputs: Tensor) -> Tensor:
        detail = self.detail_project(inputs - _smooth(inputs, 9))
        context = self.context_project(_smooth(inputs, 19))
        horizontal = self.horizontal(detail)
        vertical = self.vertical(detail)
        branch_stack = torch.stack((horizontal, vertical), dim=1)
        weights = torch.softmax(self.orientation_logits(torch.cat((horizontal, vertical), dim=1)), dim=1).unsqueeze(2)
        oriented = (branch_stack * weights).sum(dim=1)
        return self.fuse(torch.cat((inputs, detail, context, oriented), dim=1))


class FullSpectralBTDWaveletDetailUNet(nn.Module):
    """U-Net with BTD spectral features, wavelet-detail downsampling, and line-aware head."""

    def __init__(self) -> None:
        super().__init__()
        self.front_end = NormalizedBTDFrontEnd(learned_channels=16)
        base = 40
        self.stem = WaveletSplitStem(self.front_end.out_channels, base)
        self.enc0 = ResidualBlock(base, base)
        self.down1 = WaveletDetailDownsample(base, base * 2)
        self.down2 = WaveletDetailDownsample(base * 2, base * 4)
        self.down3 = WaveletDetailDownsample(base * 4, base * 8)
        self.context = DilatedContext(base * 8)
        self.up2 = ContextGatedUpFuse(base * 8, base * 4, base * 4)
        self.up1 = ContextGatedUpFuse(base * 4, base * 2, base * 2)
        self.up0 = ContextGatedUpFuse(base * 2, base, base)
        self.line_head = WaveletLineHead(base)
        self.mask_head = nn.Conv2d(base, 1, kernel_size=1)
        self.centerline_head = nn.Conv2d(base, 1, kernel_size=1)

    def forward(self, inputs: Tensor) -> dict[str, Tensor]:
        features = self.front_end(inputs)
        stem = self.stem(features)
        enc0 = self.enc0(stem)
        enc1 = self.down1(enc0)
        enc2 = self.down2(enc1)
        enc3 = self.down3(enc2)
        context = self.context(enc3)
        dec2 = self.up2(context, enc2)
        dec1 = self.up1(dec2, enc1)
        dec0 = self.up0(dec1, enc0)
        refined = self.line_head(dec0)
        return {
            "mask_logits": self.mask_head(refined),
            "centerline_logits": self.centerline_head(refined),
        }


def _validate_centerline_auxiliary_output(output_spec: dict[str, object]) -> None:
    auxiliary_outputs = output_spec.get("auxiliary_outputs")
    expected = [{"target": "centerline", "name": "centerline_logits", "shape": [1, 256, 256]}]
    if auxiliary_outputs != expected:
        raise ValueError(
            "abi129_fullspectral_btd_wavelet_detail_unet_focal_tversky_centerline_aux_v1 requires "
            "exactly one trusted centerline auxiliary output named centerline_logits"
        )


def build_model(input_spec: dict[str, object], output_spec: dict[str, object]) -> nn.Module:
    """Build the model for the Harness-supplied ABI contract."""

    if input_spec.get("mode") != "abi_16ch" or input_spec.get("shape") != [16, 256, 256]:
        raise ValueError(
            "abi129_fullspectral_btd_wavelet_detail_unet_focal_tversky_centerline_aux_v1 requires "
            "abi_16ch [16, 256, 256] input"
        )
    if output_spec.get("form") != "mask_logits" or output_spec.get("shape") != [1, 256, 256]:
        raise ValueError(
            "abi129_fullspectral_btd_wavelet_detail_unet_focal_tversky_centerline_aux_v1 requires "
            "mask_logits [1, 256, 256] primary output"
        )
    _validate_centerline_auxiliary_output(output_spec)
    return FullSpectralBTDWaveletDetailUNet()
