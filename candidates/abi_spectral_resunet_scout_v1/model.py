"""Spectral residual U-Net family scout for GOES ABI Contrail Segmentation."""

from __future__ import annotations

import torch
from torch import Tensor, nn

from abi_contrail.model_support import Conv1x1ChannelMixer


class SpectralFrontEnd(nn.Module):
    """Combine normalized ABI channels, explicit thermal BTDs, and learned mixtures."""

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
    _RAW_CHANNEL_INDICES = (3, 4, 6, 10, 12, 13)
    _BTD_PAIRS = ((10, 13), (12, 14), (13, 14), (7, 9), (6, 13))

    def __init__(self) -> None:
        super().__init__()
        means = torch.tensor(self._CHANNEL_MEANS, dtype=torch.float32).view(1, 16, 1, 1)
        scales = torch.tensor(self._CHANNEL_SCALES, dtype=torch.float32).view(1, 16, 1, 1)
        self.register_buffer("channel_means", means)
        self.register_buffer("channel_scales", scales)
        self.learned_mixer = Conv1x1ChannelMixer(
            16,
            16,
            activation=nn.SiLU(inplace=True),
        )
        self.out_channels = len(self._RAW_CHANNEL_INDICES) + len(self._BTD_PAIRS) + 16

    def forward(self, inputs: Tensor) -> Tensor:
        normalized = (inputs - self.channel_means) / self.channel_scales
        selected = normalized[:, self._RAW_CHANNEL_INDICES, :, :]
        btd_features = [
            (inputs[:, minuend : minuend + 1] - inputs[:, subtrahend : subtrahend + 1]) / 10.0
            for minuend, subtrahend in self._BTD_PAIRS
        ]
        learned = self.learned_mixer(normalized)
        return torch.cat((selected, *btd_features, learned), dim=1)


class ResidualBlock(nn.Module):
    """Two-convolution residual block with batch-size-insensitive normalization."""

    def __init__(self, in_channels: int, out_channels: int, *, dilation: int = 1) -> None:
        super().__init__()
        self.body = nn.Sequential(
            nn.Conv2d(
                in_channels,
                out_channels,
                kernel_size=3,
                padding=dilation,
                dilation=dilation,
                bias=False,
            ),
            nn.GroupNorm(8, out_channels),
            nn.SiLU(inplace=True),
            nn.Conv2d(
                out_channels,
                out_channels,
                kernel_size=3,
                padding=dilation,
                dilation=dilation,
                bias=False,
            ),
            nn.GroupNorm(8, out_channels),
        )
        self.shortcut = (
            nn.Identity()
            if in_channels == out_channels
            else nn.Conv2d(in_channels, out_channels, kernel_size=1, bias=False)
        )
        self.activation = nn.SiLU(inplace=True)

    def forward(self, inputs: Tensor) -> Tensor:
        return self.activation(self.body(inputs) + self.shortcut(inputs))


class MultiScaleContext(nn.Module):
    """Preserve local detail while adding bounded dilated context at 1/8 scale."""

    def __init__(self, channels: int = 192) -> None:
        super().__init__()
        branch_channels = channels // 3
        self.branches = nn.ModuleList(
            [
                nn.Sequential(
                    nn.Conv2d(
                        channels,
                        branch_channels,
                        kernel_size=3,
                        padding=dilation,
                        dilation=dilation,
                        bias=False,
                    ),
                    nn.GroupNorm(8, branch_channels),
                    nn.SiLU(inplace=True),
                )
                for dilation in (1, 2, 4)
            ]
        )
        self.fuse = ResidualBlock(channels, channels)

    def forward(self, inputs: Tensor) -> Tensor:
        return self.fuse(torch.cat([branch(inputs) for branch in self.branches], dim=1))


class UpBlock(nn.Module):
    """Bilinear decoder stage with a high-resolution encoder skip."""

    def __init__(self, in_channels: int, skip_channels: int) -> None:
        super().__init__()
        self.upsample = nn.Upsample(scale_factor=2, mode="bilinear", align_corners=False)
        self.reduce = nn.Conv2d(in_channels, skip_channels, kernel_size=1, bias=False)
        self.refine = ResidualBlock(skip_channels * 2, skip_channels)

    def forward(self, inputs: Tensor, skip: Tensor) -> Tensor:
        upsampled = self.reduce(self.upsample(inputs))
        return self.refine(torch.cat((upsampled, skip), dim=1))


class ABISpectralResidualUNet(nn.Module):
    """Compact residual encoder-decoder with explicit ABI spectral evidence."""

    def __init__(self) -> None:
        super().__init__()
        self.spectral_front_end = SpectralFrontEnd()
        self.encoder_1 = ResidualBlock(self.spectral_front_end.out_channels, 32)
        self.encoder_2 = ResidualBlock(32, 64)
        self.encoder_3 = ResidualBlock(64, 128)
        self.pool = nn.MaxPool2d(kernel_size=2, stride=2)
        self.bottleneck = nn.Sequential(
            ResidualBlock(128, 192),
            MultiScaleContext(192),
        )
        self.decoder_3 = UpBlock(192, 128)
        self.decoder_2 = UpBlock(128, 64)
        self.decoder_1 = UpBlock(64, 32)
        self.mask_head = nn.Conv2d(32, 1, kernel_size=1)

    def forward(self, inputs: Tensor) -> Tensor:
        spectral = self.spectral_front_end(inputs)
        encoder_1 = self.encoder_1(spectral)
        encoder_2 = self.encoder_2(self.pool(encoder_1))
        encoder_3 = self.encoder_3(self.pool(encoder_2))
        bottleneck = self.bottleneck(self.pool(encoder_3))
        decoded = self.decoder_3(bottleneck, encoder_3)
        decoded = self.decoder_2(decoded, encoder_2)
        decoded = self.decoder_1(decoded, encoder_1)
        return self.mask_head(decoded)


def build_model(input_spec, output_spec):
    """Build the model for the Harness-supplied ABI contract."""

    if input_spec.get("mode") != "abi_16ch":
        raise ValueError("abi_spectral_resunet_scout_v1 requires abi_16ch input")
    if input_spec.get("shape") != [16, 256, 256]:
        raise ValueError("abi_spectral_resunet_scout_v1 requires [16, 256, 256] input")
    if output_spec.get("form") != "mask_logits":
        raise ValueError("abi_spectral_resunet_scout_v1 produces mask_logits output")
    if output_spec.get("shape") != [1, 256, 256]:
        raise ValueError("abi_spectral_resunet_scout_v1 requires [1, 256, 256] output")
    return ABISpectralResidualUNet()
