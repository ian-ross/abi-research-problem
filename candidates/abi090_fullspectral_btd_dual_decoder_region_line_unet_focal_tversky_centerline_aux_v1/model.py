"""Full-spectral BTD dual-decoder region/line U-Net for ABI contrail segmentation."""

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


class DualEvidenceStem(nn.Module):
    """Project raw ABI/BTD features, local line residuals, and broad cloud context."""

    def __init__(self, in_channels: int, out_channels: int) -> None:
        super().__init__()
        self.raw_project = ConvNormAct(in_channels, out_channels, kernel_size=1)
        self.line_project = ConvNormAct(in_channels, out_channels, kernel_size=1)
        self.region_project = ConvNormAct(in_channels, out_channels, kernel_size=1)
        self.fuse = nn.Sequential(
            ConvNormAct(out_channels * 3, out_channels),
            ResidualBlock(out_channels, out_channels),
        )

    def forward(self, inputs: Tensor) -> Tensor:
        local_context = _smooth(inputs, 9)
        broad_context = _smooth(inputs, 25)
        line_detail = inputs - local_context
        return self.fuse(
            torch.cat(
                (
                    self.raw_project(inputs),
                    self.line_project(line_detail),
                    self.region_project(broad_context),
                ),
                dim=1,
            )
        )


class DownBlock(nn.Module):
    """Downsample by two and refine features."""

    def __init__(self, in_channels: int, out_channels: int) -> None:
        super().__init__()
        self.block = nn.Sequential(
            nn.MaxPool2d(2),
            ResidualBlock(in_channels, out_channels),
            ResidualBlock(out_channels, out_channels),
        )

    def forward(self, inputs: Tensor) -> Tensor:
        return self.block(inputs)


class DilatedContext(nn.Module):
    """Multi-dilation context at the coarsest scale."""

    def __init__(self, channels: int) -> None:
        super().__init__()
        self.d1 = ResidualBlock(channels, channels, dilation=1)
        self.d2 = ResidualBlock(channels, channels, dilation=2)
        self.d4 = ResidualBlock(channels, channels, dilation=4)
        self.project = ConvNormAct(channels * 3, channels, kernel_size=1)

    def forward(self, inputs: Tensor) -> Tensor:
        return self.project(torch.cat((self.d1(inputs), self.d2(inputs), self.d4(inputs)), dim=1))


class RegionUpBlock(nn.Module):
    """Upsample context decoder features with a smoothed skip emphasis."""

    def __init__(self, in_channels: int, skip_channels: int, out_channels: int) -> None:
        super().__init__()
        self.skip_project = ConvNormAct(skip_channels * 2, skip_channels, kernel_size=1)
        self.fuse = nn.Sequential(
            ConvNormAct(in_channels + skip_channels, out_channels),
            ResidualBlock(out_channels, out_channels),
        )

    def forward(self, inputs: Tensor, skip: Tensor) -> Tensor:
        upsampled = F.interpolate(inputs, size=skip.shape[-2:], mode="bilinear", align_corners=False)
        region_skip = self.skip_project(torch.cat((skip, _smooth(skip, 17)), dim=1))
        return self.fuse(torch.cat((upsampled, region_skip), dim=1))


class LineUpBlock(nn.Module):
    """Upsample line decoder features with high-frequency skip detail."""

    def __init__(self, in_channels: int, skip_channels: int, out_channels: int) -> None:
        super().__init__()
        self.skip_project = ConvNormAct(skip_channels * 2, skip_channels, kernel_size=1)
        self.fuse = nn.Sequential(
            ConvNormAct(in_channels + skip_channels, out_channels),
            ResidualBlock(out_channels, out_channels),
        )

    def forward(self, inputs: Tensor, skip: Tensor) -> Tensor:
        upsampled = F.interpolate(inputs, size=skip.shape[-2:], mode="bilinear", align_corners=False)
        line_detail = skip - _smooth(skip, 9)
        line_skip = self.skip_project(torch.cat((skip, line_detail), dim=1))
        return self.fuse(torch.cat((upsampled, line_skip), dim=1))


class CrossPathExchange(nn.Module):
    """Exchange region and line features after each decoder scale."""

    def __init__(self, channels: int) -> None:
        super().__init__()
        self.region_from_line = nn.Sequential(
            ConvNormAct(channels * 2, channels, kernel_size=1),
            nn.Conv2d(channels, channels, kernel_size=1, bias=True),
            nn.Sigmoid(),
        )
        self.line_from_region = nn.Sequential(
            ConvNormAct(channels * 2, channels, kernel_size=1),
            nn.Conv2d(channels, channels, kernel_size=1, bias=True),
            nn.Sigmoid(),
        )
        self.region_refine = ResidualBlock(channels, channels)
        self.line_refine = ResidualBlock(channels, channels)

    def forward(self, region: Tensor, line: Tensor) -> tuple[Tensor, Tensor]:
        shared = torch.cat((region, line), dim=1)
        region_gate = self.region_from_line(shared)
        line_gate = self.line_from_region(shared)
        region_next = self.region_refine(region + 0.25 * region_gate * line)
        line_next = self.line_refine(line + 0.25 * line_gate * region)
        return region_next, line_next


class RegionLineFusion(nn.Module):
    """Fuse full-resolution region context and line detail for mask logits."""

    def __init__(self, channels: int) -> None:
        super().__init__()
        self.region_project = nn.Sequential(
            ConvNormAct(channels, channels),
            ResidualBlock(channels, channels),
        )
        self.line_project = nn.Sequential(
            ConvNormAct(channels, channels),
            ResidualBlock(channels, channels),
        )
        self.agreement = nn.Sequential(
            ConvNormAct(channels * 4, channels, kernel_size=1),
            nn.Conv2d(channels, channels, kernel_size=1, bias=True),
            nn.Sigmoid(),
        )
        self.fuse = nn.Sequential(
            ConvNormAct(channels * 3, channels),
            ResidualBlock(channels, channels),
        )

    def forward(self, region: Tensor, line: Tensor, stem: Tensor) -> tuple[Tensor, Tensor]:
        region_features = self.region_project(region + _smooth(stem, 17))
        line_features = self.line_project(line + (stem - _smooth(stem, 9)))
        agreement = self.agreement(
            torch.cat(
                (
                    region_features,
                    line_features,
                    torch.abs(region_features - line_features),
                    region_features * line_features,
                ),
                dim=1,
            )
        )
        balanced = agreement * line_features + (1.0 - agreement) * region_features
        fused = self.fuse(torch.cat((region_features, line_features, balanced), dim=1))
        return fused, line_features


class FullSpectralBTDDualDecoderRegionLineUNet(nn.Module):
    """U-Net with separate region-context and line-detail decoders."""

    def __init__(self) -> None:
        super().__init__()
        self.front_end = NormalizedBTDFrontEnd(learned_channels=16)
        base = 40
        self.stem = DualEvidenceStem(self.front_end.out_channels, base)
        self.enc0 = ResidualBlock(base, base)
        self.down1 = DownBlock(base, base * 2)
        self.down2 = DownBlock(base * 2, base * 4)
        self.down3 = DownBlock(base * 4, base * 8)
        self.context = DilatedContext(base * 8)

        self.region_up2 = RegionUpBlock(base * 8, base * 4, base * 4)
        self.line_up2 = LineUpBlock(base * 8, base * 4, base * 4)
        self.exchange2 = CrossPathExchange(base * 4)
        self.region_up1 = RegionUpBlock(base * 4, base * 2, base * 2)
        self.line_up1 = LineUpBlock(base * 4, base * 2, base * 2)
        self.exchange1 = CrossPathExchange(base * 2)
        self.region_up0 = RegionUpBlock(base * 2, base, base)
        self.line_up0 = LineUpBlock(base * 2, base, base)
        self.exchange0 = CrossPathExchange(base)

        self.fusion = RegionLineFusion(base)
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

        region2 = self.region_up2(context, enc2)
        line2 = self.line_up2(context, enc2)
        region2, line2 = self.exchange2(region2, line2)
        region1 = self.region_up1(region2, enc1)
        line1 = self.line_up1(line2, enc1)
        region1, line1 = self.exchange1(region1, line1)
        region0 = self.region_up0(region1, enc0)
        line0 = self.line_up0(line1, enc0)
        region0, line0 = self.exchange0(region0, line0)

        fused, line_features = self.fusion(region0, line0, stem)
        return {
            "mask_logits": self.mask_head(fused),
            "centerline_logits": self.centerline_head(line_features),
        }


def _validate_centerline_auxiliary_output(output_spec: dict[str, object]) -> None:
    auxiliary_outputs = output_spec.get("auxiliary_outputs")
    expected = [{"target": "centerline", "name": "centerline_logits", "shape": [1, 256, 256]}]
    if auxiliary_outputs != expected:
        raise ValueError(
            "abi090_fullspectral_btd_dual_decoder_region_line_unet_focal_tversky_centerline_aux_v1 requires "
            "exactly one trusted centerline auxiliary output named centerline_logits"
        )


def build_model(input_spec: dict[str, object], output_spec: dict[str, object]) -> nn.Module:
    """Build the model for the Harness-supplied ABI contract."""

    if input_spec.get("mode") != "abi_16ch" or input_spec.get("shape") != [16, 256, 256]:
        raise ValueError(
            "abi090_fullspectral_btd_dual_decoder_region_line_unet_focal_tversky_centerline_aux_v1 requires "
            "abi_16ch [16, 256, 256] input"
        )
    if output_spec.get("form") != "mask_logits" or output_spec.get("shape") != [1, 256, 256]:
        raise ValueError(
            "abi090_fullspectral_btd_dual_decoder_region_line_unet_focal_tversky_centerline_aux_v1 requires "
            "mask_logits [1, 256, 256] primary output"
        )
    _validate_centerline_auxiliary_output(output_spec)
    return FullSpectralBTDDualDecoderRegionLineUNet()
