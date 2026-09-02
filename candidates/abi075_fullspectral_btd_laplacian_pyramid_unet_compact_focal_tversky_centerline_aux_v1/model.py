"""Full-spectral BTD Laplacian-pyramid U-Net for ABI contrail segmentation."""

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


class LaplacianBandBlock(nn.Module):
    """Mix multi-scale bandpass feature bands without output-threshold or filter logic."""

    def __init__(self, channels: int) -> None:
        super().__init__()
        self.raw_branch = ResidualBlock(channels, channels)
        self.narrow_branch = ConvNormAct(channels, channels)
        self.mid_branch = ConvNormAct(channels, channels)
        self.broad_branch = ConvNormAct(channels, channels, dilation=2)
        self.band_logits = nn.Conv2d(channels * 4, 4, kernel_size=1, bias=True)
        self.project = nn.Sequential(
            ConvNormAct(channels * 2, channels, kernel_size=1),
            ResidualBlock(channels, channels),
        )

    def forward(self, inputs: Tensor) -> Tensor:
        smooth5 = _smooth(inputs, 5)
        smooth13 = _smooth(inputs, 13)
        smooth31 = _smooth(inputs, 31)
        narrow = inputs - smooth5
        mid = smooth5 - smooth13
        broad = smooth13 - smooth31
        branches = (
            self.raw_branch(inputs),
            self.narrow_branch(narrow),
            self.mid_branch(mid),
            self.broad_branch(broad),
        )
        weights = torch.softmax(self.band_logits(torch.cat((inputs, narrow, mid, broad), dim=1)), dim=1).unsqueeze(2)
        mixed = (torch.stack(branches, dim=1) * weights).sum(dim=1)
        return self.project(torch.cat((inputs, mixed), dim=1))


class LaplacianStem(nn.Module):
    """Project spectral features and expose narrow, middle, and broad bandpass evidence early."""

    def __init__(self, in_channels: int, out_channels: int) -> None:
        super().__init__()
        self.raw_project = ConvNormAct(in_channels, out_channels, kernel_size=1)
        self.narrow_project = ConvNormAct(in_channels, out_channels, kernel_size=1)
        self.mid_project = ConvNormAct(in_channels, out_channels, kernel_size=1)
        self.context_project = ConvNormAct(in_channels, out_channels, kernel_size=1)
        self.fuse = nn.Sequential(
            ConvNormAct(out_channels * 4, out_channels),
            LaplacianBandBlock(out_channels),
        )

    def forward(self, inputs: Tensor) -> Tensor:
        smooth5 = _smooth(inputs, 5)
        smooth13 = _smooth(inputs, 13)
        smooth31 = _smooth(inputs, 31)
        narrow = inputs - smooth5
        mid = smooth5 - smooth13
        broad_context = smooth31
        return self.fuse(
            torch.cat(
                (
                    self.raw_project(inputs),
                    self.narrow_project(narrow),
                    self.mid_project(mid),
                    self.context_project(broad_context),
                ),
                dim=1,
            )
        )


class DownBlock(nn.Module):
    """Downsample and refine one encoder scale with Laplacian band mixing."""

    def __init__(self, in_channels: int, out_channels: int) -> None:
        super().__init__()
        self.block = nn.Sequential(
            nn.MaxPool2d(2),
            ResidualBlock(in_channels, out_channels),
            LaplacianBandBlock(out_channels),
        )

    def forward(self, inputs: Tensor) -> Tensor:
        return self.block(inputs)


class UpBlock(nn.Module):
    """Upsample decoder features and fuse skips without learned suppressive output gating."""

    def __init__(self, in_channels: int, skip_channels: int, out_channels: int) -> None:
        super().__init__()
        self.skip_project = ConvNormAct(skip_channels, skip_channels, kernel_size=1)
        self.fuse = nn.Sequential(
            ConvNormAct(in_channels + skip_channels, out_channels),
            ResidualBlock(out_channels, out_channels),
            LaplacianBandBlock(out_channels),
        )

    def forward(self, inputs: Tensor, skip: Tensor) -> Tensor:
        upsampled = F.interpolate(inputs, size=skip.shape[-2:], mode="bilinear", align_corners=False)
        return self.fuse(torch.cat((upsampled, self.skip_project(skip)), dim=1))


class LaplacianContext(nn.Module):
    """Dilated bottleneck context followed by multi-band feature mixing."""

    def __init__(self, channels: int) -> None:
        super().__init__()
        self.d1 = ResidualBlock(channels, channels, dilation=1)
        self.d2 = ResidualBlock(channels, channels, dilation=2)
        self.d4 = ResidualBlock(channels, channels, dilation=4)
        self.project = nn.Sequential(
            ConvNormAct(channels * 3, channels, kernel_size=1),
            LaplacianBandBlock(channels),
        )

    def forward(self, inputs: Tensor) -> Tensor:
        return self.project(torch.cat((self.d1(inputs), self.d2(inputs), self.d4(inputs)), dim=1))


class LaplacianPyramidFusion(nn.Module):
    """Fuse decoder scales with explicit Laplacian-band evidence at full resolution."""

    def __init__(self, base_channels: int) -> None:
        super().__init__()
        self.dec1_project = ConvNormAct(base_channels * 2, base_channels, kernel_size=1)
        self.dec2_project = ConvNormAct(base_channels * 4, base_channels, kernel_size=1)
        self.stem_project = ConvNormAct(base_channels, base_channels, kernel_size=1)
        self.fuse = nn.Sequential(
            ConvNormAct(base_channels * 7, base_channels * 2),
            ResidualBlock(base_channels * 2, base_channels * 2),
            ConvNormAct(base_channels * 2, base_channels),
            LaplacianBandBlock(base_channels),
        )

    def forward(self, dec0: Tensor, dec1: Tensor, dec2: Tensor, stem: Tensor) -> Tensor:
        target_size = dec0.shape[-2:]
        dec1_full = self.dec1_project(F.interpolate(dec1, size=target_size, mode="bilinear", align_corners=False))
        dec2_full = self.dec2_project(F.interpolate(dec2, size=target_size, mode="bilinear", align_corners=False))
        stem_full = self.stem_project(stem)
        smooth5 = _smooth(dec0, 5)
        smooth13 = _smooth(dec0, 13)
        smooth31 = _smooth(dec0, 31)
        narrow = dec0 - smooth5
        mid = smooth5 - smooth13
        broad = smooth13 - smooth31
        return self.fuse(torch.cat((dec0, narrow, mid, broad, dec1_full, dec2_full, stem_full), dim=1))


class FullSpectralBTDLaplacianPyramidUNet(nn.Module):
    """U-Net with ABI spectral BTD features and multi-scale bandpass feature fusion."""

    def __init__(self) -> None:
        super().__init__()
        self.front_end = NormalizedBTDFrontEnd(learned_channels=16)
        base = 32
        self.stem = LaplacianStem(self.front_end.out_channels, base)
        self.enc1 = nn.Sequential(ResidualBlock(base, base), LaplacianBandBlock(base))
        self.down1 = DownBlock(base, base * 2)
        self.down2 = DownBlock(base * 2, base * 4)
        self.down3 = DownBlock(base * 4, base * 8)
        self.context = LaplacianContext(base * 8)
        self.up2 = UpBlock(base * 8, base * 4, base * 4)
        self.up1 = UpBlock(base * 4, base * 2, base * 2)
        self.up0 = UpBlock(base * 2, base, base)
        self.pyramid_fusion = LaplacianPyramidFusion(base)
        self.mask_head = nn.Conv2d(base, 1, kernel_size=1)
        self.centerline_head = nn.Conv2d(base, 1, kernel_size=1)

    def forward(self, inputs: Tensor) -> dict[str, Tensor]:
        features = self.front_end(inputs)
        stem = self.stem(features)
        enc1 = self.enc1(stem)
        enc2 = self.down1(enc1)
        enc3 = self.down2(enc2)
        enc4 = self.down3(enc3)
        context = self.context(enc4)
        dec2 = self.up2(context, enc3)
        dec1 = self.up1(dec2, enc2)
        dec0 = self.up0(dec1, enc1)
        refined = self.pyramid_fusion(dec0, dec1, dec2, stem)
        return {
            "mask_logits": self.mask_head(refined),
            "centerline_logits": self.centerline_head(refined),
        }


def _validate_centerline_auxiliary_output(output_spec: dict[str, object]) -> None:
    auxiliary_outputs = output_spec.get("auxiliary_outputs")
    expected = [{"target": "centerline", "name": "centerline_logits", "shape": [1, 256, 256]}]
    if auxiliary_outputs != expected:
        raise ValueError(
            "abi075_fullspectral_btd_laplacian_pyramid_unet_compact_focal_tversky_centerline_aux_v1 requires "
            "exactly one trusted centerline auxiliary output named centerline_logits"
        )


def build_model(input_spec: dict[str, object], output_spec: dict[str, object]) -> nn.Module:
    """Build the model for the Harness-supplied ABI contract."""

    if input_spec.get("mode") != "abi_16ch" or input_spec.get("shape") != [16, 256, 256]:
        raise ValueError(
            "abi075_fullspectral_btd_laplacian_pyramid_unet_compact_focal_tversky_centerline_aux_v1 requires "
            "abi_16ch [16, 256, 256] input"
        )
    if output_spec.get("form") != "mask_logits" or output_spec.get("shape") != [1, 256, 256]:
        raise ValueError(
            "abi075_fullspectral_btd_laplacian_pyramid_unet_compact_focal_tversky_centerline_aux_v1 requires "
            "mask_logits [1, 256, 256] primary output"
        )
    _validate_centerline_auxiliary_output(output_spec)
    return FullSpectralBTDLaplacianPyramidUNet()
