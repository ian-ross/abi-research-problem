"""Full-spectral BTD multi-resolution line-HRNet scout for ABI contrail segmentation."""

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
        kernel_size: int = 3,
        dilation: int = 1,
        groups: int = 1,
    ) -> None:
        super().__init__()
        padding = dilation * (kernel_size // 2)
        self.block = nn.Sequential(
            nn.Conv2d(
                in_channels,
                out_channels,
                kernel_size=kernel_size,
                padding=padding,
                dilation=dilation,
                groups=groups,
                bias=False,
            ),
            nn.GroupNorm(_group_count(out_channels), out_channels),
            nn.GELU(),
        )

    def forward(self, inputs: Tensor) -> Tensor:
        return self.block(inputs)


class ResidualBlock(nn.Module):
    """Residual convolution block used at each resolution."""

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


class SeparableAsymmetricConv(nn.Module):
    """Depthwise asymmetric line filter followed by pointwise mixing."""

    def __init__(self, channels: int, *, kernel_size: tuple[int, int]) -> None:
        super().__init__()
        padding = (kernel_size[0] // 2, kernel_size[1] // 2)
        self.block = nn.Sequential(
            nn.Conv2d(channels, channels, kernel_size=kernel_size, padding=padding, groups=channels, bias=False),
            nn.Conv2d(channels, channels, kernel_size=1, bias=False),
            nn.GroupNorm(_group_count(channels), channels),
            nn.GELU(),
        )

    def forward(self, inputs: Tensor) -> Tensor:
        return self.block(inputs)


class LineContextBlock(nn.Module):
    """Low-capacity oriented context that avoids hard thresholding or postprocessing."""

    def __init__(self, channels: int) -> None:
        super().__init__()
        self.local = ResidualBlock(channels, channels)
        self.horizontal = SeparableAsymmetricConv(channels, kernel_size=(1, 15))
        self.vertical = SeparableAsymmetricConv(channels, kernel_size=(15, 1))
        self.dilated = nn.Sequential(
            ConvNormAct(channels, channels, dilation=2),
            ConvNormAct(channels, channels, dilation=4),
        )
        self.gate = nn.Sequential(
            ConvNormAct(channels * 4, channels, kernel_size=1),
            nn.Conv2d(channels, channels, kernel_size=1, bias=True),
            nn.Sigmoid(),
        )
        self.project = nn.Sequential(
            ConvNormAct(channels * 4, channels, kernel_size=1),
            ResidualBlock(channels, channels),
        )

    def forward(self, inputs: Tensor) -> Tensor:
        detail = inputs - _smooth(inputs, 9)
        branches = torch.cat((self.local(inputs), self.horizontal(detail), self.vertical(detail), self.dilated(inputs)), dim=1)
        gate = self.gate(branches)
        fused = self.project(branches)
        return inputs + fused * (0.5 + gate)


class MultiResolutionFusionStage(nn.Module):
    """Repeatedly exchange high-resolution line detail with coarser cloud context."""

    def __init__(self, high_channels: int, mid_channels: int, low_channels: int) -> None:
        super().__init__()
        self.high_line = LineContextBlock(high_channels)
        self.mid_context = ResidualBlock(mid_channels, mid_channels, dilation=2)
        self.low_context = nn.Sequential(
            ResidualBlock(low_channels, low_channels, dilation=2),
            ResidualBlock(low_channels, low_channels, dilation=4),
        )
        self.high_from_mid = ConvNormAct(mid_channels, high_channels, kernel_size=1)
        self.high_from_low = ConvNormAct(low_channels, high_channels, kernel_size=1)
        self.mid_from_high = ConvNormAct(high_channels, mid_channels, kernel_size=1)
        self.mid_from_low = ConvNormAct(low_channels, mid_channels, kernel_size=1)
        self.low_from_high = ConvNormAct(high_channels, low_channels, kernel_size=1)
        self.low_from_mid = ConvNormAct(mid_channels, low_channels, kernel_size=1)
        self.high_fuse = ResidualBlock(high_channels * 3, high_channels)
        self.mid_fuse = ResidualBlock(mid_channels * 3, mid_channels)
        self.low_fuse = ResidualBlock(low_channels * 3, low_channels)

    def forward(self, high: Tensor, mid: Tensor, low: Tensor) -> tuple[Tensor, Tensor, Tensor]:
        high_base = self.high_line(high)
        mid_base = self.mid_context(mid)
        low_base = self.low_context(low)

        high_size = high_base.shape[-2:]
        mid_size = mid_base.shape[-2:]
        low_size = low_base.shape[-2:]

        high_next = self.high_fuse(
            torch.cat(
                (
                    high_base,
                    F.interpolate(self.high_from_mid(mid_base), size=high_size, mode="bilinear", align_corners=False),
                    F.interpolate(self.high_from_low(low_base), size=high_size, mode="bilinear", align_corners=False),
                ),
                dim=1,
            )
        )
        mid_next = self.mid_fuse(
            torch.cat(
                (
                    mid_base,
                    F.adaptive_avg_pool2d(self.mid_from_high(high_base), mid_size),
                    F.interpolate(self.mid_from_low(low_base), size=mid_size, mode="bilinear", align_corners=False),
                ),
                dim=1,
            )
        )
        low_next = self.low_fuse(
            torch.cat(
                (
                    low_base,
                    F.adaptive_avg_pool2d(self.low_from_high(high_base), low_size),
                    F.adaptive_avg_pool2d(self.low_from_mid(mid_base), low_size),
                ),
                dim=1,
            )
        )
        return high_next, mid_next, low_next


class MultiResolutionLineHead(nn.Module):
    """Fuse HRNet-style branches into mask and centerline evidence features."""

    def __init__(self, high_channels: int, mid_channels: int, low_channels: int) -> None:
        super().__init__()
        self.mid_project = ConvNormAct(mid_channels, high_channels, kernel_size=1)
        self.low_project = ConvNormAct(low_channels, high_channels, kernel_size=1)
        self.detail_project = ConvNormAct(high_channels, high_channels, kernel_size=1)
        self.line_refine = LineContextBlock(high_channels)
        self.project = nn.Sequential(
            ConvNormAct(high_channels * 4, high_channels * 2),
            ResidualBlock(high_channels * 2, high_channels),
            LineContextBlock(high_channels),
        )

    def forward(self, high: Tensor, mid: Tensor, low: Tensor) -> Tensor:
        high_size = high.shape[-2:]
        mid_full = F.interpolate(self.mid_project(mid), size=high_size, mode="bilinear", align_corners=False)
        low_full = F.interpolate(self.low_project(low), size=high_size, mode="bilinear", align_corners=False)
        detail = self.detail_project(high - _smooth(high, 9))
        line = self.line_refine(high)
        return self.project(torch.cat((high, mid_full, low_full, detail + line), dim=1))


class FullSpectralBTDMultiresolutionLineHRNet(nn.Module):
    """Parallel multi-resolution network for thin-line ABI contrail segmentation."""

    def __init__(self) -> None:
        super().__init__()
        self.front_end = NormalizedBTDFrontEnd(learned_channels=16)
        base = 32
        self.stem = nn.Sequential(
            ConvNormAct(self.front_end.out_channels, base, kernel_size=1),
            ResidualBlock(base, base),
            LineContextBlock(base),
        )
        self.make_mid = nn.Sequential(nn.MaxPool2d(2), ResidualBlock(base, base * 2))
        self.make_low = nn.Sequential(nn.MaxPool2d(2), ResidualBlock(base * 2, base * 4))
        self.stage1 = MultiResolutionFusionStage(base, base * 2, base * 4)
        self.stage2 = MultiResolutionFusionStage(base, base * 2, base * 4)
        self.stage3 = MultiResolutionFusionStage(base, base * 2, base * 4)
        self.head_features = MultiResolutionLineHead(base, base * 2, base * 4)
        self.mask_head = nn.Conv2d(base, 1, kernel_size=1)
        self.centerline_head = nn.Conv2d(base, 1, kernel_size=1)

    def forward(self, inputs: Tensor) -> dict[str, Tensor]:
        features = self.front_end(inputs)
        high = self.stem(features)
        mid = self.make_mid(high)
        low = self.make_low(mid)
        high, mid, low = self.stage1(high, mid, low)
        high, mid, low = self.stage2(high, mid, low)
        high, mid, low = self.stage3(high, mid, low)
        refined = self.head_features(high, mid, low)
        return {
            "mask_logits": self.mask_head(refined),
            "centerline_logits": self.centerline_head(refined),
        }


def _validate_centerline_auxiliary_output(output_spec: dict[str, object]) -> None:
    auxiliary_outputs = output_spec.get("auxiliary_outputs")
    expected = [{"target": "centerline", "name": "centerline_logits", "shape": [1, 256, 256]}]
    if auxiliary_outputs != expected:
        raise ValueError(
            "abi084_fullspectral_btd_multiresolution_line_hrnet_focal_tversky_centerline_aux_v1 requires "
            "exactly one trusted centerline auxiliary output named centerline_logits"
        )


def build_model(input_spec: dict[str, object], output_spec: dict[str, object]) -> nn.Module:
    """Build the model for the Harness-supplied ABI contract."""

    if input_spec.get("mode") != "abi_16ch" or input_spec.get("shape") != [16, 256, 256]:
        raise ValueError(
            "abi084_fullspectral_btd_multiresolution_line_hrnet_focal_tversky_centerline_aux_v1 requires "
            "abi_16ch [16, 256, 256] input"
        )
    if output_spec.get("form") != "mask_logits" or output_spec.get("shape") != [1, 256, 256]:
        raise ValueError(
            "abi084_fullspectral_btd_multiresolution_line_hrnet_focal_tversky_centerline_aux_v1 requires "
            "mask_logits [1, 256, 256] primary output"
        )
    _validate_centerline_auxiliary_output(output_spec)
    return FullSpectralBTDMultiresolutionLineHRNet()
