"""Full-spectral BTD frequency-gated line U-Net with centerline-guided focal-Tversky head."""

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


class FrequencySplitStem(nn.Module):
    """Separate local line contrast from broad cloud context before encoding."""

    def __init__(self, in_channels: int, out_channels: int) -> None:
        super().__init__()
        self.raw_project = ConvNormAct(in_channels, out_channels, kernel_size=1)
        self.detail_project = ConvNormAct(in_channels, out_channels, kernel_size=1)
        self.context_project = ConvNormAct(in_channels, out_channels, kernel_size=1)
        self.fuse = nn.Sequential(
            ConvNormAct(out_channels * 3, out_channels),
            ResidualBlock(out_channels, out_channels),
        )

    def forward(self, inputs: Tensor) -> Tensor:
        local_smooth = _smooth(inputs, 9)
        broad_smooth = _smooth(inputs, 25)
        detail = inputs - local_smooth
        return self.fuse(
            torch.cat(
                (
                    self.raw_project(inputs),
                    self.detail_project(detail),
                    self.context_project(broad_smooth),
                ),
                dim=1,
            )
        )


class UpFuseBlock(nn.Module):
    """Upsample decoder features and fuse them with a low-frequency-gated skip."""

    def __init__(self, in_channels: int, skip_channels: int, out_channels: int) -> None:
        super().__init__()
        self.skip_gate = nn.Sequential(
            nn.Conv2d(skip_channels * 2, skip_channels, kernel_size=1, bias=True),
            nn.Sigmoid(),
        )
        self.fuse = nn.Sequential(
            ConvNormAct(in_channels + skip_channels, out_channels),
            ResidualBlock(out_channels, out_channels),
        )

    def forward(self, inputs: Tensor, skip: Tensor) -> Tensor:
        upsampled = F.interpolate(inputs, size=skip.shape[-2:], mode="bilinear", align_corners=False)
        skip_context = _smooth(skip, 9)
        gated_skip = skip * (0.5 + self.skip_gate(torch.cat((skip, skip_context), dim=1)))
        return self.fuse(torch.cat((upsampled, gated_skip), dim=1))


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


class AsymmetricConvNormAct(nn.Module):
    """Asymmetric convolution, GroupNorm, and GELU for direction-specific line context."""

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
                bias=False,
            ),
            nn.GroupNorm(_group_count(channels), channels),
            nn.GELU(),
        )

    def forward(self, inputs: Tensor) -> Tensor:
        return self.block(inputs)


class FrequencyLineRefiner(nn.Module):
    """Refine logits from high-frequency detail, oriented context, and smooth gates."""

    def __init__(self, channels: int) -> None:
        super().__init__()
        self.detail_project = ConvNormAct(channels, channels)
        self.horizontal = nn.Sequential(
            AsymmetricConvNormAct(channels, kernel_size=(1, 13)),
            ResidualBlock(channels, channels),
        )
        self.vertical = nn.Sequential(
            AsymmetricConvNormAct(channels, kernel_size=(13, 1)),
            ResidualBlock(channels, channels),
        )
        self.broad = nn.Sequential(
            ConvNormAct(channels, channels, dilation=2),
            ConvNormAct(channels, channels, dilation=4),
        )
        self.orientation_logits = nn.Conv2d(channels * 3, 3, kernel_size=1, bias=True)
        self.smooth_gate = nn.Sequential(
            ConvNormAct(channels * 2, channels, kernel_size=1),
            nn.Conv2d(channels, channels, kernel_size=1, bias=True),
            nn.Sigmoid(),
        )
        self.project = nn.Sequential(
            ConvNormAct(channels * 3, channels),
            ResidualBlock(channels, channels),
        )

    def forward(self, inputs: Tensor) -> Tensor:
        detail = self.detail_project(inputs - _smooth(inputs, 9))
        branches = (self.horizontal(detail), self.vertical(detail), self.broad(inputs))
        branch_stack = torch.stack(branches, dim=1)
        weights = torch.softmax(self.orientation_logits(torch.cat(branches, dim=1)), dim=1).unsqueeze(2)
        oriented = (branch_stack * weights).sum(dim=1)
        smooth_context = _smooth(inputs, 17)
        gate = self.smooth_gate(torch.cat((inputs, smooth_context), dim=1))
        gated = inputs * (0.5 + gate)
        return self.project(torch.cat((gated, detail, oriented), dim=1))


class FrequencyPyramidFusion(nn.Module):
    """Fuse decoder features with explicit high/low spatial-frequency evidence."""

    def __init__(self, base_channels: int) -> None:
        super().__init__()
        self.dec1_project = ConvNormAct(base_channels * 2, base_channels, kernel_size=1)
        self.dec2_project = ConvNormAct(base_channels * 4, base_channels, kernel_size=1)
        self.stem_project = ConvNormAct(base_channels, base_channels, kernel_size=1)
        self.fuse = nn.Sequential(
            ConvNormAct(base_channels * 6, base_channels * 2),
            ResidualBlock(base_channels * 2, base_channels * 2),
            ConvNormAct(base_channels * 2, base_channels),
            ResidualBlock(base_channels, base_channels),
        )
        self.refiner = FrequencyLineRefiner(base_channels)

    def forward(self, dec0: Tensor, dec1: Tensor, dec2: Tensor, stem: Tensor) -> Tensor:
        target_size = dec0.shape[-2:]
        dec1_full = self.dec1_project(F.interpolate(dec1, size=target_size, mode="bilinear", align_corners=False))
        dec2_full = self.dec2_project(F.interpolate(dec2, size=target_size, mode="bilinear", align_corners=False))
        stem_full = self.stem_project(stem)
        detail = dec0 - _smooth(dec0, 9)
        local_smooth = _smooth(dec0, 9)
        broad_smooth = _smooth(dec0, 25)
        fused = self.fuse(torch.cat((dec0, detail, local_smooth, broad_smooth, dec1_full, dec2_full), dim=1))
        return self.refiner(fused + stem_full)


class CenterlineGuidedMaskHead(nn.Module):
    """Predict mask logits with a small centerline-guided additive residual.

    ABI-069's subtractive confidence suppressor reduced useful continuity. This
    head is intentionally less suppressive: the direct mask logit remains the
    primary path, while a bounded residual can add or remove evidence only where
    the jointly trained centerline branch finds line-like support. It is ordinary
    differentiable model architecture, not thresholding, postprocessing, target
    derivation, metric logic, or an Artifact Filter.
    """

    def __init__(self, channels: int) -> None:
        super().__init__()
        self.direct_logits = nn.Conv2d(channels, 1, kernel_size=1)
        self.centerline_logits = nn.Conv2d(channels, 1, kernel_size=1)
        self.residual_features = nn.Sequential(
            ConvNormAct(channels * 3, channels),
            ResidualBlock(channels, channels),
            ConvNormAct(channels, channels),
        )
        self.residual_logits = nn.Conv2d(channels, 1, kernel_size=1)
        nn.init.zeros_(self.residual_logits.weight)
        nn.init.zeros_(self.residual_logits.bias)

    def forward(self, inputs: Tensor) -> tuple[Tensor, Tensor]:
        detail = inputs - _smooth(inputs, 9)
        smooth_context = _smooth(inputs, 25)
        residual_features = self.residual_features(torch.cat((inputs, detail, smooth_context), dim=1))
        centerline_logits = self.centerline_logits(inputs)
        centerline_gate = torch.sigmoid(centerline_logits)
        bounded_residual = 0.20 * torch.tanh(self.residual_logits(residual_features)) * centerline_gate
        return self.direct_logits(inputs) + bounded_residual, centerline_logits


class FullSpectralBTDFrequencyGatedCenterlineGuidedUNet(nn.Module):
    """Frequency-gated U-Net preserving ABI-068 with a centerline-guided mask head."""

    def __init__(self) -> None:
        super().__init__()
        self.front_end = NormalizedBTDFrontEnd(learned_channels=16)
        base = 44
        self.stem = FrequencySplitStem(self.front_end.out_channels, base)
        self.enc1 = ResidualBlock(base, base)
        self.down1 = nn.Sequential(nn.MaxPool2d(2), ResidualBlock(base, base * 2))
        self.down2 = nn.Sequential(nn.MaxPool2d(2), ResidualBlock(base * 2, base * 4))
        self.down3 = nn.Sequential(nn.MaxPool2d(2), ResidualBlock(base * 4, base * 8))
        self.context = DilatedContext(base * 8)
        self.up2 = UpFuseBlock(base * 8, base * 4, base * 4)
        self.up1 = UpFuseBlock(base * 4, base * 2, base * 2)
        self.up0 = UpFuseBlock(base * 2, base, base)
        self.frequency_fusion = FrequencyPyramidFusion(base)
        self.mask_head = CenterlineGuidedMaskHead(base)

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
        refined = self.frequency_fusion(dec0, dec1, dec2, stem)
        mask_logits, centerline_logits = self.mask_head(refined)
        return {
            "mask_logits": mask_logits,
            "centerline_logits": centerline_logits,
        }


def _validate_centerline_auxiliary_output(output_spec: dict[str, object]) -> None:
    auxiliary_outputs = output_spec.get("auxiliary_outputs")
    expected = [{"target": "centerline", "name": "centerline_logits", "shape": [1, 256, 256]}]
    if auxiliary_outputs != expected:
        raise ValueError(
            "abi070_fullspectral_btd_frequency_gated_line_unet_centerline_guided_focal_tversky_v1 requires "
            "exactly one trusted centerline auxiliary output named centerline_logits"
        )


def build_model(input_spec: dict[str, object], output_spec: dict[str, object]) -> nn.Module:
    """Build the model for the Harness-supplied ABI contract."""

    if input_spec.get("mode") != "abi_16ch" or input_spec.get("shape") != [16, 256, 256]:
        raise ValueError(
            "abi070_fullspectral_btd_frequency_gated_line_unet_centerline_guided_focal_tversky_v1 requires "
            "abi_16ch [16, 256, 256] input"
        )
    if output_spec.get("form") != "mask_logits" or output_spec.get("shape") != [1, 256, 256]:
        raise ValueError(
            "abi070_fullspectral_btd_frequency_gated_line_unet_centerline_guided_focal_tversky_v1 requires "
            "mask_logits [1, 256, 256] primary output"
        )
    _validate_centerline_auxiliary_output(output_spec)
    return FullSpectralBTDFrequencyGatedCenterlineGuidedUNet()
