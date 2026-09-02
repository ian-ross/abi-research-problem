"""Full-spectral BTD context-pyramid agreement U-Net for ABI contrail segmentation."""

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


class ContextPyramidNeck(nn.Module):
    """Blend global patch context and atrous cloud context at the coarsest scale."""

    def __init__(self, channels: int, pyramid_channels: int = 64) -> None:
        super().__init__()
        self.local = nn.Sequential(
            ResidualBlock(channels, channels, dilation=1),
            ResidualBlock(channels, channels, dilation=2),
        )
        self.pool_branches = nn.ModuleList(
            [ConvNormAct(channels, pyramid_channels, kernel_size=1) for _ in (1, 2, 4, 8)]
        )
        self.dilated = nn.ModuleList(
            [
                ResidualBlock(channels, pyramid_channels, dilation=rate)
                for rate in (1, 2, 4, 6)
            ]
        )
        fuse_channels = channels + pyramid_channels * 8
        self.fuse = nn.Sequential(
            ConvNormAct(fuse_channels, channels, kernel_size=1),
            ResidualBlock(channels, channels),
        )

    def forward(self, inputs: Tensor) -> Tensor:
        target_size = inputs.shape[-2:]
        pooled = []
        for bins, branch in zip((1, 2, 4, 8), self.pool_branches):
            context = F.adaptive_avg_pool2d(inputs, output_size=(bins, bins))
            pooled.append(F.interpolate(branch(context), size=target_size, mode="bilinear", align_corners=False))
        dilated = [branch(inputs) for branch in self.dilated]
        return self.fuse(torch.cat((self.local(inputs), *pooled, *dilated), dim=1))


class FPNDecoder(nn.Module):
    """Top-down decoder that emphasizes context-calibrated feature reuse over concatenative skip amplification."""

    def __init__(self, base_channels: int) -> None:
        super().__init__()
        base = base_channels
        self.top_project = ConvNormAct(base * 8, base * 4, kernel_size=1)
        self.lateral2 = ConvNormAct(base * 4, base * 4, kernel_size=1)
        self.lateral1 = ConvNormAct(base * 2, base * 2, kernel_size=1)
        self.lateral0 = ConvNormAct(base, base, kernel_size=1)
        self.refine2 = ResidualBlock(base * 4, base * 4)
        self.refine1 = ResidualBlock(base * 2, base * 2)
        self.refine0 = ResidualBlock(base, base)
        self.reduce2 = ConvNormAct(base * 4, base * 2, kernel_size=1)
        self.reduce1 = ConvNormAct(base * 2, base, kernel_size=1)
        self.pyramid_fuse = nn.Sequential(
            ConvNormAct(base * 4, base * 2),
            ResidualBlock(base * 2, base * 2),
            ConvNormAct(base * 2, base),
            ResidualBlock(base, base),
        )

    def forward(self, enc0: Tensor, enc1: Tensor, enc2: Tensor, neck: Tensor) -> tuple[Tensor, Tensor]:
        p2 = self.refine2(self.top_project(neck) + self.lateral2(enc2))
        p1_from_top = F.interpolate(self.reduce2(p2), size=enc1.shape[-2:], mode="bilinear", align_corners=False)
        p1 = self.refine1(p1_from_top + self.lateral1(enc1))
        p0_from_top = F.interpolate(self.reduce1(p1), size=enc0.shape[-2:], mode="bilinear", align_corners=False)
        p0 = self.refine0(p0_from_top + self.lateral0(enc0))

        p1_full = F.interpolate(self.reduce1(p1), size=p0.shape[-2:], mode="bilinear", align_corners=False)
        p2_full = F.interpolate(self.reduce1(self.reduce2(p2)), size=p0.shape[-2:], mode="bilinear", align_corners=False)
        neck_full = F.interpolate(self.reduce1(self.reduce2(self.top_project(neck))), size=p0.shape[-2:], mode="bilinear", align_corners=False)
        return self.pyramid_fuse(torch.cat((p0, p1_full, p2_full, neck_full), dim=1)), neck_full


class FeatureAgreementCalibrator(nn.Module):
    """Fuse local line evidence with low-resolution patch context before producing logits."""

    def __init__(self, channels: int) -> None:
        super().__init__()
        self.local_project = ResidualBlock(channels, channels)
        self.context_project = nn.Sequential(
            ConvNormAct(channels, channels),
            ResidualBlock(channels, channels),
        )
        self.agreement_gate = nn.Sequential(
            ConvNormAct(channels * 3, channels, kernel_size=1),
            nn.Conv2d(channels, channels, kernel_size=1, bias=True),
            nn.Sigmoid(),
        )
        self.fuse = nn.Sequential(
            ConvNormAct(channels * 2, channels),
            ResidualBlock(channels, channels),
        )

    def forward(self, local_features: Tensor, context_features: Tensor) -> Tensor:
        local = self.local_project(local_features)
        context = self.context_project(context_features)
        gate = self.agreement_gate(torch.cat((local, context, torch.abs(local - context)), dim=1))
        calibrated_local = local * (0.75 + 0.5 * gate)
        calibrated_context = context * (0.25 + 0.25 * (1.0 - gate))
        return self.fuse(torch.cat((calibrated_local, calibrated_context), dim=1))


class FullSpectralBTDContextPyramidAgreementUNet(nn.Module):
    """Context-pyramid FPN/U-Net with feature-agreement calibration for thin contrails."""

    def __init__(self) -> None:
        super().__init__()
        self.front_end = NormalizedBTDFrontEnd(learned_channels=16)
        base = 40
        self.stem = nn.Sequential(
            ConvNormAct(self.front_end.out_channels, base),
            ResidualBlock(base, base),
        )
        self.down1 = DownBlock(base, base * 2)
        self.down2 = DownBlock(base * 2, base * 4)
        self.down3 = DownBlock(base * 4, base * 8)
        self.neck = ContextPyramidNeck(base * 8, pyramid_channels=base)
        self.decoder = FPNDecoder(base)
        self.calibrator = FeatureAgreementCalibrator(base)
        self.mask_head = nn.Conv2d(base, 1, kernel_size=1)
        self.centerline_head = nn.Conv2d(base, 1, kernel_size=1)

    def forward(self, inputs: Tensor) -> dict[str, Tensor]:
        features = self.front_end(inputs)
        enc0 = self.stem(features)
        enc1 = self.down1(enc0)
        enc2 = self.down2(enc1)
        enc3 = self.down3(enc2)
        neck = self.neck(enc3)
        decoded, context_full = self.decoder(enc0, enc1, enc2, neck)
        calibrated = self.calibrator(decoded, context_full)
        return {
            "mask_logits": self.mask_head(calibrated),
            "centerline_logits": self.centerline_head(calibrated),
        }


def _validate_centerline_auxiliary_output(output_spec: dict[str, object]) -> None:
    auxiliary_outputs = output_spec.get("auxiliary_outputs")
    expected = [{"target": "centerline", "name": "centerline_logits", "shape": [1, 256, 256]}]
    if auxiliary_outputs != expected:
        raise ValueError(
            "abi118_fullspectral_btd_context_pyramid_agreement_unet_focal_tversky_centerline_aux_v1 requires "
            "exactly one trusted centerline auxiliary output named centerline_logits"
        )


def build_model(input_spec: dict[str, object], output_spec: dict[str, object]) -> nn.Module:
    """Build the model for the Harness-supplied ABI contract."""

    if input_spec.get("mode") != "abi_16ch" or input_spec.get("shape") != [16, 256, 256]:
        raise ValueError(
            "abi118_fullspectral_btd_context_pyramid_agreement_unet_focal_tversky_centerline_aux_v1 requires "
            "abi_16ch [16, 256, 256] input"
        )
    if output_spec.get("form") != "mask_logits" or output_spec.get("shape") != [1, 256, 256]:
        raise ValueError(
            "abi118_fullspectral_btd_context_pyramid_agreement_unet_focal_tversky_centerline_aux_v1 requires "
            "mask_logits [1, 256, 256] primary output"
        )
    _validate_centerline_auxiliary_output(output_spec)
    return FullSpectralBTDContextPyramidAgreementUNet()
