"""Full-spectral BTD steerable ridge U-Net for ABI contrail segmentation."""

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


class AsymmetricDepthwiseBranch(nn.Module):
    """Efficient horizontal or vertical line-context branch."""

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
                groups=channels,
                bias=False,
            ),
            nn.Conv2d(channels, channels, kernel_size=1, bias=False),
            nn.GroupNorm(_group_count(channels), channels),
            nn.GELU(),
        )

    def forward(self, inputs: Tensor) -> Tensor:
        return self.block(inputs)


class MaskedDiagonalDepthwiseBranch(nn.Module):
    """Depthwise diagonal line-context branch with trainable weights on one diagonal only."""

    def __init__(self, channels: int, *, kernel_size: int = 15, anti_diagonal: bool = False) -> None:
        super().__init__()
        self.kernel_size = kernel_size
        self.weight = nn.Parameter(torch.empty(channels, 1, kernel_size, kernel_size))
        nn.init.kaiming_normal_(self.weight, nonlinearity="linear")
        mask = torch.zeros(1, 1, kernel_size, kernel_size, dtype=torch.float32)
        positions = range(kernel_size)
        for row in positions:
            col = kernel_size - 1 - row if anti_diagonal else row
            mask[:, :, row, col] = 1.0 / (kernel_size**0.5)
        self.register_buffer("mask", mask)
        self.pointwise = nn.Sequential(
            nn.Conv2d(channels, channels, kernel_size=1, bias=False),
            nn.GroupNorm(_group_count(channels), channels),
            nn.GELU(),
        )

    def forward(self, inputs: Tensor) -> Tensor:
        weight = self.weight * self.mask
        diagonal = F.conv2d(inputs, weight, padding=self.kernel_size // 2, groups=inputs.shape[1])
        return self.pointwise(diagonal)


class SteerableRidgeBlock(nn.Module):
    """Fuse local, horizontal, vertical, and diagonal evidence without output suppression.

    This block is intended to broaden beyond recent post-decoder suppressive/gated heads.
    It keeps a residual feature path and uses learned soft branch mixing among oriented
    line-context features, but it does not threshold, postprocess, artifact-filter, or
    derive targets inside candidate code.
    """

    def __init__(self, channels: int, *, line_kernel: int = 15) -> None:
        super().__init__()
        self.local = ResidualBlock(channels, channels)
        self.horizontal = AsymmetricDepthwiseBranch(channels, kernel_size=(1, line_kernel))
        self.vertical = AsymmetricDepthwiseBranch(channels, kernel_size=(line_kernel, 1))
        self.diagonal_down = MaskedDiagonalDepthwiseBranch(channels, kernel_size=line_kernel, anti_diagonal=False)
        self.diagonal_up = MaskedDiagonalDepthwiseBranch(channels, kernel_size=line_kernel, anti_diagonal=True)
        self.branch_logits = nn.Conv2d(channels * 5, 5, kernel_size=1, bias=True)
        self.project = nn.Sequential(
            ConvNormAct(channels * 3, channels),
            nn.Conv2d(channels, channels, kernel_size=3, padding=1, bias=False),
            nn.GroupNorm(_group_count(channels), channels),
        )
        self.act = nn.GELU()

    def forward(self, inputs: Tensor) -> Tensor:
        detail = inputs - _smooth(inputs, 9)
        branches = (
            self.local(inputs),
            self.horizontal(detail),
            self.vertical(detail),
            self.diagonal_down(detail),
            self.diagonal_up(detail),
        )
        weights = torch.softmax(self.branch_logits(torch.cat(branches, dim=1)), dim=1).unsqueeze(2)
        mixed = (torch.stack(branches, dim=1) * weights).sum(dim=1)
        residual = self.project(torch.cat((inputs, detail, mixed), dim=1))
        return self.act(inputs + residual)


class DownRidgeBlock(nn.Module):
    """Downsample and apply residual plus steerable ridge context."""

    def __init__(self, in_channels: int, out_channels: int) -> None:
        super().__init__()
        self.block = nn.Sequential(
            nn.MaxPool2d(2),
            ResidualBlock(in_channels, out_channels),
            SteerableRidgeBlock(out_channels),
        )

    def forward(self, inputs: Tensor) -> Tensor:
        return self.block(inputs)


class UpRidgeFuseBlock(nn.Module):
    """Upsample decoder features, concatenate the full skip, and refine ridge context."""

    def __init__(self, in_channels: int, skip_channels: int, out_channels: int) -> None:
        super().__init__()
        self.fuse = nn.Sequential(
            ConvNormAct(in_channels + skip_channels, out_channels),
            ResidualBlock(out_channels, out_channels),
            SteerableRidgeBlock(out_channels),
        )

    def forward(self, inputs: Tensor, skip: Tensor) -> Tensor:
        upsampled = F.interpolate(inputs, size=skip.shape[-2:], mode="bilinear", align_corners=False)
        return self.fuse(torch.cat((upsampled, skip), dim=1))


class MultiDilationRidgeBottleneck(nn.Module):
    """Coarse context with atrous and steerable-ridge branches."""

    def __init__(self, channels: int) -> None:
        super().__init__()
        self.d1 = ResidualBlock(channels, channels, dilation=1)
        self.d2 = ResidualBlock(channels, channels, dilation=2)
        self.d4 = ResidualBlock(channels, channels, dilation=4)
        self.ridge = SteerableRidgeBlock(channels, line_kernel=11)
        self.project = nn.Sequential(
            ConvNormAct(channels * 4, channels),
            ResidualBlock(channels, channels),
        )

    def forward(self, inputs: Tensor) -> Tensor:
        return self.project(torch.cat((self.d1(inputs), self.d2(inputs), self.d4(inputs), self.ridge(inputs)), dim=1))


class MultiScaleRidgeHead(nn.Module):
    """Fuse decoder scales, high-frequency residual detail, and stem context before heads."""

    def __init__(self, base_channels: int) -> None:
        super().__init__()
        self.dec1_project = ConvNormAct(base_channels * 2, base_channels, kernel_size=1)
        self.dec2_project = ConvNormAct(base_channels * 4, base_channels, kernel_size=1)
        self.stem_project = ConvNormAct(base_channels, base_channels, kernel_size=1)
        self.fuse = nn.Sequential(
            ConvNormAct(base_channels * 5, base_channels * 2),
            ResidualBlock(base_channels * 2, base_channels * 2),
            ConvNormAct(base_channels * 2, base_channels),
            SteerableRidgeBlock(base_channels),
        )

    def forward(self, dec0: Tensor, dec1: Tensor, dec2: Tensor, stem: Tensor) -> Tensor:
        target_size = dec0.shape[-2:]
        dec1_full = self.dec1_project(F.interpolate(dec1, size=target_size, mode="bilinear", align_corners=False))
        dec2_full = self.dec2_project(F.interpolate(dec2, size=target_size, mode="bilinear", align_corners=False))
        stem_full = self.stem_project(stem)
        detail = dec0 - _smooth(dec0, 9)
        return self.fuse(torch.cat((dec0, detail, dec1_full, dec2_full, stem_full), dim=1))


class FullSpectralBTDSteerableRidgeUNet(nn.Module):
    """U-Net with BTD features and non-suppressive steerable ridge context."""

    def __init__(self) -> None:
        super().__init__()
        self.front_end = NormalizedBTDFrontEnd(learned_channels=16)
        base = 32
        self.stem = nn.Sequential(
            ConvNormAct(self.front_end.out_channels, base),
            ResidualBlock(base, base),
            SteerableRidgeBlock(base),
        )
        self.down1 = DownRidgeBlock(base, base * 2)
        self.down2 = DownRidgeBlock(base * 2, base * 4)
        self.down3 = DownRidgeBlock(base * 4, base * 8)
        self.bottleneck = MultiDilationRidgeBottleneck(base * 8)
        self.up2 = UpRidgeFuseBlock(base * 8, base * 4, base * 4)
        self.up1 = UpRidgeFuseBlock(base * 4, base * 2, base * 2)
        self.up0 = UpRidgeFuseBlock(base * 2, base, base)
        self.head_features = MultiScaleRidgeHead(base)
        self.mask_head = nn.Conv2d(base, 1, kernel_size=1)
        self.centerline_head = nn.Conv2d(base, 1, kernel_size=1)

    def forward(self, inputs: Tensor) -> dict[str, Tensor]:
        features = self.front_end(inputs)
        stem = self.stem(features)
        enc1 = self.down1(stem)
        enc2 = self.down2(enc1)
        enc3 = self.down3(enc2)
        context = self.bottleneck(enc3)
        dec2 = self.up2(context, enc2)
        dec1 = self.up1(dec2, enc1)
        dec0 = self.up0(dec1, stem)
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
            "abi072_fullspectral_btd_steerable_ridge_unet_focal_tversky_centerline_aux_v1 requires "
            "exactly one trusted centerline auxiliary output named centerline_logits"
        )


def build_model(input_spec: dict[str, object], output_spec: dict[str, object]) -> nn.Module:
    """Build the model for the Harness-supplied ABI contract."""

    if input_spec.get("mode") != "abi_16ch" or input_spec.get("shape") != [16, 256, 256]:
        raise ValueError(
            "abi072_fullspectral_btd_steerable_ridge_unet_focal_tversky_centerline_aux_v1 requires "
            "abi_16ch [16, 256, 256] input"
        )
    if output_spec.get("form") != "mask_logits" or output_spec.get("shape") != [1, 256, 256]:
        raise ValueError(
            "abi072_fullspectral_btd_steerable_ridge_unet_focal_tversky_centerline_aux_v1 requires "
            "mask_logits [1, 256, 256] primary output"
        )
    _validate_centerline_auxiliary_output(output_spec)
    return FullSpectralBTDSteerableRidgeUNet()
