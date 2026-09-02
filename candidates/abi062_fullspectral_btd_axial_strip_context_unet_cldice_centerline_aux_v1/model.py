"""Full-spectral BTD axial strip-context U-Net for ABI contrail segmentation."""

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
    for groups in (8, 6, 4, 3, 2, 1):
        if channels % groups == 0:
            return groups
    return 1


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
    """Compact residual block used at each image scale."""

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


class ChannelGate(nn.Module):
    """Patch-context channel gate derived from globally pooled decoder or encoder features."""

    def __init__(self, channels: int, reduction: int = 4) -> None:
        super().__init__()
        hidden = max(channels // reduction, 8)
        self.gate = nn.Sequential(
            nn.AdaptiveAvgPool2d(1),
            nn.Conv2d(channels, hidden, kernel_size=1),
            nn.GELU(),
            nn.Conv2d(hidden, channels, kernel_size=1),
            nn.Sigmoid(),
        )

    def forward(self, inputs: Tensor) -> Tensor:
        return inputs * self.gate(inputs)


class AsymmetricConvNormAct(nn.Module):
    """Asymmetric convolution, GroupNorm, and GELU for strip-wise context."""

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
                groups=_group_count(channels),
                bias=False,
            ),
            nn.GroupNorm(_group_count(channels), channels),
            nn.GELU(),
        )

    def forward(self, inputs: Tensor) -> Tensor:
        return self.block(inputs)


class AxialStripContextBlock(nn.Module):
    """Fuse local features with row, column, and patch-context evidence.

    The strip branches pool over one image axis before applying asymmetric
    convolution, so they provide long linear context without quadratic attention
    memory.  They do not use coordinates, thresholding, or postprocessing.
    """

    def __init__(self, channels: int) -> None:
        super().__init__()
        self.local = ResidualBlock(channels, channels)
        self.horizontal = nn.Sequential(
            AsymmetricConvNormAct(channels, kernel_size=(1, 17)),
            nn.Conv2d(channels, channels, kernel_size=1, bias=False),
            nn.GroupNorm(_group_count(channels), channels),
            nn.GELU(),
        )
        self.vertical = nn.Sequential(
            AsymmetricConvNormAct(channels, kernel_size=(17, 1)),
            nn.Conv2d(channels, channels, kernel_size=1, bias=False),
            nn.GroupNorm(_group_count(channels), channels),
            nn.GELU(),
        )
        self.patch_gate = ChannelGate(channels)
        self.branch_logits = nn.Conv2d(channels * 4, 4, kernel_size=1, bias=True)
        self.project = nn.Sequential(
            ConvNormAct(channels * 2, channels),
            ResidualBlock(channels, channels),
        )

    def forward(self, inputs: Tensor) -> Tensor:
        local = self.local(inputs)
        horizontal_seed = inputs.mean(dim=2, keepdim=True).expand_as(inputs)
        vertical_seed = inputs.mean(dim=3, keepdim=True).expand_as(inputs)
        horizontal = self.horizontal(horizontal_seed)
        vertical = self.vertical(vertical_seed)
        patch = self.patch_gate(inputs)
        branches = (local, horizontal, vertical, patch)
        branch_stack = torch.stack(branches, dim=1)
        weights = torch.softmax(self.branch_logits(torch.cat(branches, dim=1)), dim=1).unsqueeze(2)
        contextual = (branch_stack * weights).sum(dim=1)
        return self.project(torch.cat((inputs, contextual), dim=1))


class DownsampleBlock(nn.Module):
    """Downsample and apply residual plus axial strip context."""

    def __init__(self, in_channels: int, out_channels: int) -> None:
        super().__init__()
        self.block = nn.Sequential(
            nn.MaxPool2d(2),
            ResidualBlock(in_channels, out_channels),
            AxialStripContextBlock(out_channels),
        )

    def forward(self, inputs: Tensor) -> Tensor:
        return self.block(inputs)


class UpStripFuseBlock(nn.Module):
    """Upsample decoder features, attention-gate skips, and add strip context."""

    def __init__(self, in_channels: int, skip_channels: int, out_channels: int) -> None:
        super().__init__()
        self.skip_gate = nn.Sequential(
            nn.Conv2d(skip_channels, skip_channels, kernel_size=1, bias=True),
            nn.Sigmoid(),
        )
        self.fuse = nn.Sequential(
            ConvNormAct(in_channels + skip_channels, out_channels),
            ResidualBlock(out_channels, out_channels),
            AxialStripContextBlock(out_channels),
        )

    def forward(self, inputs: Tensor, skip: Tensor) -> Tensor:
        upsampled = F.interpolate(inputs, size=skip.shape[-2:], mode="bilinear", align_corners=False)
        gated_skip = skip * self.skip_gate(skip)
        return self.fuse(torch.cat((upsampled, gated_skip), dim=1))


class AtrousBottleneck(nn.Module):
    """Compact multi-dilation bottleneck for cloud-scale context."""

    def __init__(self, channels: int) -> None:
        super().__init__()
        self.d1 = ResidualBlock(channels, channels, dilation=1)
        self.d2 = ResidualBlock(channels, channels, dilation=2)
        self.d4 = ResidualBlock(channels, channels, dilation=4)
        self.strip = AxialStripContextBlock(channels)
        self.project = nn.Sequential(
            ConvNormAct(channels * 4, channels),
            ChannelGate(channels),
            ResidualBlock(channels, channels),
        )

    def forward(self, inputs: Tensor) -> Tensor:
        return self.project(torch.cat((self.d1(inputs), self.d2(inputs), self.d4(inputs), self.strip(inputs)), dim=1))


class MultiResolutionHead(nn.Module):
    """Fuse decoder features from three scales before final logit heads."""

    def __init__(self, base_channels: int) -> None:
        super().__init__()
        self.dec1_project = ConvNormAct(base_channels * 2, base_channels, kernel_size=1)
        self.dec2_project = ConvNormAct(base_channels * 4, base_channels, kernel_size=1)
        self.fuse = nn.Sequential(
            ConvNormAct(base_channels * 3, base_channels * 2),
            ResidualBlock(base_channels * 2, base_channels * 2),
            ConvNormAct(base_channels * 2, base_channels),
            AxialStripContextBlock(base_channels),
        )

    def forward(self, dec0: Tensor, dec1: Tensor, dec2: Tensor) -> Tensor:
        target_size = dec0.shape[-2:]
        dec1_full = self.dec1_project(F.interpolate(dec1, size=target_size, mode="bilinear", align_corners=False))
        dec2_full = self.dec2_project(F.interpolate(dec2, size=target_size, mode="bilinear", align_corners=False))
        return self.fuse(torch.cat((dec0, dec1_full, dec2_full), dim=1))


class FullSpectralBTDAxialStripContextUNet(nn.Module):
    """U-Net-like encoder-decoder dominated by axial strip-context blocks."""

    def __init__(self) -> None:
        super().__init__()
        self.front_end = NormalizedBTDFrontEnd(learned_channels=16)
        base = 44
        self.stem = nn.Sequential(
            ConvNormAct(self.front_end.out_channels, base),
            ResidualBlock(base, base),
            AxialStripContextBlock(base),
        )
        self.down1 = DownsampleBlock(base, base * 2)
        self.down2 = DownsampleBlock(base * 2, base * 4)
        self.down3 = DownsampleBlock(base * 4, base * 8)
        self.bottleneck = AtrousBottleneck(base * 8)
        self.up2 = UpStripFuseBlock(base * 8, base * 4, base * 4)
        self.up1 = UpStripFuseBlock(base * 4, base * 2, base * 2)
        self.up0 = UpStripFuseBlock(base * 2, base, base)
        self.head_features = MultiResolutionHead(base)
        self.mask_head = nn.Conv2d(base, 1, kernel_size=1)
        self.centerline_head = nn.Conv2d(base, 1, kernel_size=1)

    def forward(self, inputs: Tensor) -> dict[str, Tensor]:
        features = self.front_end(inputs)
        enc0 = self.stem(features)
        enc1 = self.down1(enc0)
        enc2 = self.down2(enc1)
        enc3 = self.down3(enc2)
        context = self.bottleneck(enc3)
        dec2 = self.up2(context, enc2)
        dec1 = self.up1(dec2, enc1)
        dec0 = self.up0(dec1, enc0)
        features_out = self.head_features(dec0, dec1, dec2)
        return {
            "mask_logits": self.mask_head(features_out),
            "centerline_logits": self.centerline_head(features_out),
        }


def _validate_centerline_auxiliary_output(output_spec: dict[str, object]) -> None:
    auxiliary_outputs = output_spec.get("auxiliary_outputs")
    expected = [{"target": "centerline", "name": "centerline_logits", "shape": [1, 256, 256]}]
    if auxiliary_outputs != expected:
        raise ValueError(
            "abi062_fullspectral_btd_axial_strip_context_unet_cldice_centerline_aux_v1 requires "
            "exactly one trusted centerline auxiliary output named centerline_logits"
        )


def build_model(input_spec: dict[str, object], output_spec: dict[str, object]) -> nn.Module:
    """Build the model for the Harness-supplied ABI contract."""

    if input_spec.get("mode") != "abi_16ch" or input_spec.get("shape") != [16, 256, 256]:
        raise ValueError(
            "abi062_fullspectral_btd_axial_strip_context_unet_cldice_centerline_aux_v1 requires "
            "abi_16ch [16, 256, 256] input"
        )
    if output_spec.get("form") != "mask_logits" or output_spec.get("shape") != [1, 256, 256]:
        raise ValueError(
            "abi062_fullspectral_btd_axial_strip_context_unet_cldice_centerline_aux_v1 requires "
            "mask_logits [1, 256, 256] primary output"
        )
    _validate_centerline_auxiliary_output(output_spec)
    return FullSpectralBTDAxialStripContextUNet()
