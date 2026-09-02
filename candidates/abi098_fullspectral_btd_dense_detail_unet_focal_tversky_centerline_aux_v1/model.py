"""Full-spectral BTD dense-detail U-Net for ABI contrail segmentation."""

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

    def __init__(
        self,
        in_channels: int,
        out_channels: int,
        *,
        kernel_size: int | tuple[int, int] = 3,
        dilation: int | tuple[int, int] = 1,
        activation: bool = True,
    ) -> None:
        super().__init__()
        if isinstance(kernel_size, tuple):
            if isinstance(dilation, tuple):
                padding = (dilation[0] * (kernel_size[0] // 2), dilation[1] * (kernel_size[1] // 2))
            else:
                padding = (dilation * (kernel_size[0] // 2), dilation * (kernel_size[1] // 2))
        else:
            if isinstance(dilation, tuple):
                padding = (dilation[0] * (kernel_size // 2), dilation[1] * (kernel_size // 2))
            else:
                padding = dilation * (kernel_size // 2)
        layers: list[nn.Module] = [
            nn.Conv2d(
                in_channels,
                out_channels,
                kernel_size=kernel_size,
                padding=padding,
                dilation=dilation,
                bias=False,
            ),
            nn.GroupNorm(_group_count(out_channels), out_channels),
        ]
        if activation:
            layers.append(nn.GELU())
        self.block = nn.Sequential(*layers)

    def forward(self, inputs: Tensor) -> Tensor:
        return self.block(inputs)


class ResidualBlock(nn.Module):
    """Residual convolution block used for projection and post-fusion refinement."""

    def __init__(self, in_channels: int, out_channels: int, *, dilation: int = 1) -> None:
        super().__init__()
        self.conv1 = ConvNormAct(in_channels, out_channels, dilation=dilation)
        self.conv2 = ConvNormAct(out_channels, out_channels, activation=False)
        self.skip = (
            nn.Identity()
            if in_channels == out_channels
            else nn.Conv2d(in_channels, out_channels, kernel_size=1, bias=False)
        )
        self.act = nn.GELU()

    def forward(self, inputs: Tensor) -> Tensor:
        return self.act(self.conv2(self.conv1(inputs)) + self.skip(inputs))


class DenseLayer(nn.Module):
    """One compact dense layer that appends newly learned local evidence."""

    def __init__(self, in_channels: int, growth_rate: int, *, dilation: int = 1) -> None:
        super().__init__()
        self.layer = nn.Sequential(
            ConvNormAct(in_channels, growth_rate * 2, kernel_size=1),
            ConvNormAct(growth_rate * 2, growth_rate, dilation=dilation),
        )

    def forward(self, inputs: Tensor) -> Tensor:
        return torch.cat((inputs, self.layer(inputs)), dim=1)


class DenseBlock(nn.Module):
    """Small DenseNet-style block for feature reuse without a large parameter budget."""

    def __init__(self, in_channels: int, growth_rate: int, layer_count: int) -> None:
        super().__init__()
        channels = in_channels
        layers = []
        for index in range(layer_count):
            dilation = 2 if index % 3 == 2 else 1
            layer = DenseLayer(channels, growth_rate, dilation=dilation)
            layers.append(layer)
            channels += growth_rate
        self.layers = nn.ModuleList(layers)
        self.out_channels = channels

    def forward(self, inputs: Tensor) -> Tensor:
        features = inputs
        for layer in self.layers:
            features = layer(features)
        return features


class DenseStage(nn.Module):
    """Dense block followed by projection to a fixed channel width."""

    def __init__(self, in_channels: int, out_channels: int, growth_rate: int, layer_count: int) -> None:
        super().__init__()
        self.dense = DenseBlock(in_channels, growth_rate, layer_count)
        self.project = nn.Sequential(
            ConvNormAct(self.dense.out_channels, out_channels, kernel_size=1),
            ResidualBlock(out_channels, out_channels),
        )

    def forward(self, inputs: Tensor) -> Tensor:
        return self.project(self.dense(inputs))


class DownStage(nn.Module):
    """Pool to a coarser scale and build dense local context."""

    def __init__(self, in_channels: int, out_channels: int, growth_rate: int, layer_count: int) -> None:
        super().__init__()
        self.stage = nn.Sequential(
            nn.MaxPool2d(2),
            ConvNormAct(in_channels, out_channels, kernel_size=1),
            DenseStage(out_channels, out_channels, growth_rate, layer_count),
        )

    def forward(self, inputs: Tensor) -> Tensor:
        return self.stage(inputs)


class UpDenseFuse(nn.Module):
    """Upsample decoder features and fuse with high-resolution dense skip evidence."""

    def __init__(self, in_channels: int, skip_channels: int, out_channels: int, growth_rate: int) -> None:
        super().__init__()
        self.skip_detail_gate = nn.Sequential(
            ConvNormAct(skip_channels * 2, skip_channels, kernel_size=1),
            nn.Conv2d(skip_channels, skip_channels, kernel_size=1, bias=True),
            nn.Sigmoid(),
        )
        self.pre_project = ConvNormAct(in_channels + skip_channels, out_channels, kernel_size=1)
        self.stage = DenseStage(out_channels, out_channels, growth_rate, layer_count=3)

    def forward(self, inputs: Tensor, skip: Tensor) -> Tensor:
        upsampled = F.interpolate(inputs, size=skip.shape[-2:], mode="bilinear", align_corners=False)
        skip_detail = skip - _smooth(skip, 7)
        gate = self.skip_detail_gate(torch.cat((skip, skip_detail), dim=1))
        gated_skip = skip * (0.75 + 0.5 * gate)
        fused = torch.cat((upsampled, gated_skip), dim=1)
        return self.stage(self.pre_project(fused))


class AtrousDenseContext(nn.Module):
    """Compact multi-dilation context at the coarsest feature scale."""

    def __init__(self, channels: int) -> None:
        super().__init__()
        self.local = ResidualBlock(channels, channels, dilation=1)
        self.mid = ResidualBlock(channels, channels, dilation=2)
        self.wide = ResidualBlock(channels, channels, dilation=4)
        self.project = ConvNormAct(channels * 3, channels, kernel_size=1)

    def forward(self, inputs: Tensor) -> Tensor:
        return self.project(torch.cat((self.local(inputs), self.mid(inputs), self.wide(inputs)), dim=1))


class DenseDetailRefiner(nn.Module):
    """Preserve thin high-frequency lines while using smooth context as a soft gate."""

    def __init__(self, channels: int) -> None:
        super().__init__()
        self.detail_stage = DenseStage(channels * 2, channels, growth_rate=12, layer_count=3)
        self.context_gate = nn.Sequential(
            ConvNormAct(channels * 3, channels, kernel_size=1),
            nn.Conv2d(channels, channels, kernel_size=1, bias=True),
            nn.Sigmoid(),
        )
        self.oriented = nn.Sequential(
            ConvNormAct(channels, channels, kernel_size=(1, 9)),
            ConvNormAct(channels, channels, kernel_size=(9, 1)),
        )
        self.project = nn.Sequential(
            ConvNormAct(channels * 4, channels),
            ResidualBlock(channels, channels),
        )

    def forward(self, inputs: Tensor) -> Tensor:
        detail = inputs - _smooth(inputs, 7)
        local_context = _smooth(inputs, 15)
        dense_detail = self.detail_stage(torch.cat((inputs, detail), dim=1))
        gate = self.context_gate(torch.cat((inputs, dense_detail, local_context), dim=1))
        oriented = self.oriented(dense_detail)
        return self.project(torch.cat((inputs, detail, dense_detail * (0.5 + gate), oriented), dim=1))


class FullSpectralBTDDenseDetailUNet(nn.Module):
    """Dense U-Net that preserves ABI/BTD detail features through shallow dense reuse."""

    def __init__(self) -> None:
        super().__init__()
        self.front_end = NormalizedBTDFrontEnd(learned_channels=16)
        self.stem = nn.Sequential(
            ConvNormAct(self.front_end.out_channels, 32, kernel_size=1),
            ResidualBlock(32, 32),
        )
        self.enc0 = DenseStage(32, 48, growth_rate=12, layer_count=3)
        self.enc1 = DownStage(48, 72, growth_rate=16, layer_count=3)
        self.enc2 = DownStage(72, 112, growth_rate=20, layer_count=4)
        self.enc3 = DownStage(112, 144, growth_rate=24, layer_count=4)
        self.context = AtrousDenseContext(144)
        self.up2 = UpDenseFuse(144, 112, 112, growth_rate=20)
        self.up1 = UpDenseFuse(112, 72, 72, growth_rate=16)
        self.up0 = UpDenseFuse(72, 48, 48, growth_rate=12)
        self.refiner = DenseDetailRefiner(48)
        self.mask_head = nn.Conv2d(48, 1, kernel_size=1)
        self.centerline_head = nn.Conv2d(48, 1, kernel_size=1)

    def forward(self, inputs: Tensor) -> dict[str, Tensor]:
        features = self.front_end(inputs)
        stem = self.stem(features)
        enc0 = self.enc0(stem)
        enc1 = self.enc1(enc0)
        enc2 = self.enc2(enc1)
        enc3 = self.enc3(enc2)
        context = self.context(enc3)
        dec2 = self.up2(context, enc2)
        dec1 = self.up1(dec2, enc1)
        dec0 = self.up0(dec1, enc0)
        refined = self.refiner(dec0)
        return {
            "mask_logits": self.mask_head(refined),
            "centerline_logits": self.centerline_head(refined),
        }


def _validate_centerline_auxiliary_output(output_spec: dict[str, object]) -> None:
    auxiliary_outputs = output_spec.get("auxiliary_outputs")
    expected = [{"target": "centerline", "name": "centerline_logits", "shape": [1, 256, 256]}]
    if auxiliary_outputs != expected:
        raise ValueError(
            "abi098_fullspectral_btd_dense_detail_unet_focal_tversky_centerline_aux_v1 requires "
            "exactly one trusted centerline auxiliary output named centerline_logits"
        )


def build_model(input_spec: dict[str, object], output_spec: dict[str, object]) -> nn.Module:
    """Build the model for the Harness-supplied ABI contract."""

    if input_spec.get("mode") != "abi_16ch" or input_spec.get("shape") != [16, 256, 256]:
        raise ValueError(
            "abi098_fullspectral_btd_dense_detail_unet_focal_tversky_centerline_aux_v1 requires "
            "abi_16ch [16, 256, 256] input"
        )
    if output_spec.get("form") != "mask_logits" or output_spec.get("shape") != [1, 256, 256]:
        raise ValueError(
            "abi098_fullspectral_btd_dense_detail_unet_focal_tversky_centerline_aux_v1 requires "
            "mask_logits [1, 256, 256] primary output"
        )
    _validate_centerline_auxiliary_output(output_spec)
    return FullSpectralBTDDenseDetailUNet()
