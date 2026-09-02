"""Full-spectral BTD+SZA UPerNet directional line-context decoder for ABI contrail segmentation."""

from __future__ import annotations

import torch
import torch.nn.functional as F
from torch import Tensor, nn


CANDIDATE_ID = "abi180_fullspectral_btd_sza_upernet_directional_line_context_bce_dice_line_centerline_aux_v1"


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


class SignedDetailStem(nn.Module):
    """Preserve positive and negative thin-line residual evidence before pyramid encoding."""

    def __init__(self, in_channels: int, out_channels: int) -> None:
        super().__init__()
        self.raw_project = ConvNormAct(in_channels, out_channels, kernel_size=1)
        self.local_positive = ConvNormAct(in_channels, out_channels, kernel_size=1)
        self.local_negative = ConvNormAct(in_channels, out_channels, kernel_size=1)
        self.mid_positive = ConvNormAct(in_channels, out_channels, kernel_size=1)
        self.mid_negative = ConvNormAct(in_channels, out_channels, kernel_size=1)
        self.context_project = ConvNormAct(in_channels, out_channels, kernel_size=1)
        self.fuse = nn.Sequential(
            ConvNormAct(out_channels * 6, out_channels),
            ResidualBlock(out_channels, out_channels),
        )

    def forward(self, inputs: Tensor) -> Tensor:
        local = _smooth(inputs, 7)
        mid = _smooth(inputs, 15)
        broad = _smooth(inputs, 31)
        local_detail = inputs - local
        mid_detail = inputs - mid
        return self.fuse(
            torch.cat(
                (
                    self.raw_project(inputs),
                    self.local_positive(F.relu(local_detail)),
                    self.local_negative(F.relu(-local_detail)),
                    self.mid_positive(F.relu(mid_detail)),
                    self.mid_negative(F.relu(-mid_detail)),
                    self.context_project(broad),
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
            ResidualBlock(out_channels, out_channels),
        )

    def forward(self, inputs: Tensor) -> Tensor:
        return self.block(inputs)


class PyramidPoolingContext(nn.Module):
    """UPerNet-style pyramid pooling at the coarsest feature scale."""

    def __init__(self, in_channels: int, out_channels: int) -> None:
        super().__init__()
        branch = out_channels // 4
        self.local_project = ConvNormAct(in_channels, branch, kernel_size=1)
        self.pool1 = nn.Sequential(nn.AdaptiveAvgPool2d(1), ConvNormAct(in_channels, branch, kernel_size=1))
        self.pool2 = nn.Sequential(nn.AdaptiveAvgPool2d(2), ConvNormAct(in_channels, branch, kernel_size=1))
        self.pool4 = nn.Sequential(nn.AdaptiveAvgPool2d(4), ConvNormAct(in_channels, branch, kernel_size=1))
        self.project = nn.Sequential(
            ConvNormAct(branch * 4, out_channels, kernel_size=1),
            ResidualBlock(out_channels, out_channels),
        )

    @staticmethod
    def _upsample(inputs: Tensor, size: tuple[int, int]) -> Tensor:
        return F.interpolate(inputs, size=size, mode="bilinear", align_corners=False)

    def forward(self, inputs: Tensor) -> Tensor:
        size = inputs.shape[-2:]
        return self.project(
            torch.cat(
                (
                    self.local_project(inputs),
                    self._upsample(self.pool1(inputs), size),
                    self._upsample(self.pool2(inputs), size),
                    self._upsample(self.pool4(inputs), size),
                ),
                dim=1,
            )
        )


class UPerFeaturePyramid(nn.Module):
    """Top-down feature pyramid with high-resolution detail fusion."""

    def __init__(self, base_channels: int, pyramid_channels: int = 64) -> None:
        super().__init__()
        self.lat0 = ConvNormAct(base_channels, pyramid_channels, kernel_size=1)
        self.lat1 = ConvNormAct(base_channels * 2, pyramid_channels, kernel_size=1)
        self.lat2 = ConvNormAct(base_channels * 4, pyramid_channels, kernel_size=1)
        self.lat3 = ConvNormAct(base_channels * 8, pyramid_channels, kernel_size=1)
        self.smooth0 = ResidualBlock(pyramid_channels, pyramid_channels)
        self.smooth1 = ResidualBlock(pyramid_channels, pyramid_channels)
        self.smooth2 = ResidualBlock(pyramid_channels, pyramid_channels)
        self.smooth3 = ResidualBlock(pyramid_channels, pyramid_channels)
        self.detail_project = ConvNormAct(base_channels, pyramid_channels, kernel_size=1)
        self.fuse = nn.Sequential(
            ConvNormAct(pyramid_channels * 5, pyramid_channels),
            ResidualBlock(pyramid_channels, pyramid_channels),
        )

    @staticmethod
    def _resize(inputs: Tensor, size: tuple[int, int]) -> Tensor:
        if inputs.shape[-2:] == size:
            return inputs
        return F.interpolate(inputs, size=size, mode="bilinear", align_corners=False)

    def forward(self, enc0: Tensor, enc1: Tensor, enc2: Tensor, context: Tensor, detail: Tensor) -> Tensor:
        p3 = self.lat3(context)
        p2 = self.lat2(enc2) + self._resize(p3, enc2.shape[-2:])
        p1 = self.lat1(enc1) + self._resize(p2, enc1.shape[-2:])
        p0 = self.lat0(enc0) + self._resize(p1, enc0.shape[-2:])
        p3 = self.smooth3(p3)
        p2 = self.smooth2(p2)
        p1 = self.smooth1(p1)
        p0 = self.smooth0(p0)
        size = enc0.shape[-2:]
        detail_features = self.detail_project(detail)
        return self.fuse(
            torch.cat(
                (
                    p0,
                    self._resize(p1, size),
                    self._resize(p2, size),
                    self._resize(p3, size),
                    detail_features,
                ),
                dim=1,
            )
        )


class FixedDirectionalAverages(nn.Module):
    """Fixed feature-space directional averages for line continuity support."""

    def __init__(self, kernel_size: int = 17) -> None:
        super().__init__()
        if kernel_size % 2 != 1:
            raise ValueError("kernel_size must be odd")
        self.kernel_size = kernel_size
        horizontal = torch.ones(1, 1, 1, kernel_size, dtype=torch.float32) / float(kernel_size)
        vertical = torch.ones(1, 1, kernel_size, 1, dtype=torch.float32) / float(kernel_size)
        diagonal_down = torch.eye(kernel_size, dtype=torch.float32).view(1, 1, kernel_size, kernel_size) / float(kernel_size)
        diagonal_up = torch.flip(diagonal_down, dims=[-1])
        self.register_buffer("horizontal_kernel", horizontal)
        self.register_buffer("vertical_kernel", vertical)
        self.register_buffer("diagonal_down_kernel", diagonal_down)
        self.register_buffer("diagonal_up_kernel", diagonal_up)

    @staticmethod
    def _depthwise_filter(inputs: Tensor, kernel: Tensor, padding: tuple[int, int]) -> Tensor:
        weight = kernel.expand(inputs.shape[1], -1, -1, -1)
        return F.conv2d(inputs, weight, padding=padding, groups=inputs.shape[1])

    def forward(self, inputs: Tensor) -> Tensor:
        radius = self.kernel_size // 2
        horizontal = self._depthwise_filter(inputs, self.horizontal_kernel, (0, radius))
        vertical = self._depthwise_filter(inputs, self.vertical_kernel, (radius, 0))
        diagonal_down = self._depthwise_filter(inputs, self.diagonal_down_kernel, (radius, radius))
        diagonal_up = self._depthwise_filter(inputs, self.diagonal_up_kernel, (radius, radius))
        return torch.cat((horizontal, vertical, diagonal_down, diagonal_up), dim=1)


class DirectionalLineContextRefiner(nn.Module):
    """Non-postprocessing additive line propagation for horizontal, vertical, and diagonal support."""

    def __init__(self, channels: int) -> None:
        super().__init__()
        self.detail = ConvNormAct(channels, channels)
        self.directional_average = FixedDirectionalAverages(kernel_size=17)
        self.directional_project = nn.Sequential(
            ConvNormAct(channels * 4, channels, kernel_size=1),
            ResidualBlock(channels, channels),
        )
        self.broad = ConvNormAct(channels, channels, kernel_size=1)
        self.additive_residual = nn.Sequential(
            ConvNormAct(channels * 3, channels, kernel_size=1),
            nn.Conv2d(channels, channels, kernel_size=1, bias=True),
            nn.Tanh(),
        )
        self.project = nn.Sequential(
            ConvNormAct(channels * 4, channels),
            ResidualBlock(channels, channels),
        )

    def forward(self, inputs: Tensor) -> Tensor:
        detail = self.detail(inputs - _smooth(inputs, 7))
        directional = self.directional_project(self.directional_average(inputs))
        broad = self.broad(_smooth(inputs, 25))
        residual = 0.30 * self.additive_residual(torch.cat((detail, directional, broad), dim=1))
        propagated = inputs + residual
        return self.project(torch.cat((propagated, detail, directional, broad), dim=1))


class FullSpectralBTDSZAUPerNetDirectionalLineContextDecoder(nn.Module):
    """UPerNet pyramid/detail decoder with additive directional line-continuity propagation."""

    def __init__(self) -> None:
        super().__init__()
        self.front_end = NormalizedBTDSZAFrontEnd(learned_channels=16)
        base = 40
        pyramid = 64
        self.stem = SignedDetailStem(self.front_end.out_channels, base)
        self.enc0 = ResidualBlock(base, base)
        self.enc1 = EncoderDown(base, base * 2)
        self.enc2 = EncoderDown(base * 2, base * 4)
        self.enc3 = EncoderDown(base * 4, base * 8)
        self.context = PyramidPoolingContext(base * 8, base * 8)
        self.detail = SignedDetailStem(self.front_end.out_channels, base)
        self.pyramid = UPerFeaturePyramid(base, pyramid_channels=pyramid)
        self.refine = DirectionalLineContextRefiner(pyramid)
        self.mask_head = nn.Conv2d(pyramid, 1, kernel_size=1)
        self.line_head = nn.Conv2d(pyramid, 1, kernel_size=1)
        self.centerline_head = nn.Conv2d(pyramid, 1, kernel_size=1)

    def forward(self, inputs: Tensor) -> dict[str, Tensor]:
        features = self.front_end(inputs)
        stem = self.stem(features)
        enc0 = self.enc0(stem)
        enc1 = self.enc1(enc0)
        enc2 = self.enc2(enc1)
        enc3 = self.enc3(enc2)
        context = self.context(enc3)
        detail = self.detail(features)
        pyramid = self.pyramid(enc0, enc1, enc2, context, detail)
        refined = self.refine(pyramid)
        return {
            "mask_logits": self.mask_head(refined),
            "line_logits": self.line_head(refined),
            "centerline_logits": self.centerline_head(refined),
        }


def _validate_auxiliary_outputs(output_spec: dict[str, object]) -> None:
    auxiliary_outputs = output_spec.get("auxiliary_outputs")
    expected = [
        {"target": "line", "name": "line_logits", "shape": [1, 256, 256]},
        {"target": "centerline", "name": "centerline_logits", "shape": [1, 256, 256]},
    ]
    if auxiliary_outputs != expected:
        raise ValueError(
            f"{CANDIDATE_ID} requires trusted line_logits and centerline_logits auxiliary outputs"
        )


def build_model(input_spec: dict[str, object], output_spec: dict[str, object]) -> nn.Module:
    """Build the model for the Harness-supplied ABI contract."""

    if input_spec.get("mode") != "abi_16ch_plus_sza" or input_spec.get("shape") != [17, 256, 256]:
        raise ValueError(f"{CANDIDATE_ID} requires abi_16ch_plus_sza [17, 256, 256] input")
    if output_spec.get("form") != "mask_logits" or output_spec.get("shape") != [1, 256, 256]:
        raise ValueError(f"{CANDIDATE_ID} requires mask_logits [1, 256, 256] primary output")
    _validate_auxiliary_outputs(output_spec)
    return FullSpectralBTDSZAUPerNetDirectionalLineContextDecoder()
