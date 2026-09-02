"""Full-spectral BTD high-resolution line U-Net with line-gated mask refinement."""

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
        (6, 13),   # ABI 7 - ABI 14 shortwave / longwave window
        (7, 9),    # ABI 8 - ABI 10 water-vapor contrast
        (7, 12),   # ABI 8 - ABI 13 upper-water-vapor / clean-window
        (8, 13),   # ABI 9 - ABI 14 mid-water-vapor / longwave
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


class UpFuseBlock(nn.Module):
    """Upsample decoder features and fuse them with an encoder skip."""

    def __init__(self, in_channels: int, skip_channels: int, out_channels: int) -> None:
        super().__init__()
        self.skip_gate = nn.Sequential(
            nn.Conv2d(skip_channels, skip_channels, kernel_size=1, bias=True),
            nn.Sigmoid(),
        )
        self.fuse = nn.Sequential(
            ConvNormAct(in_channels + skip_channels, out_channels),
            ResidualBlock(out_channels, out_channels),
        )

    def forward(self, inputs: Tensor, skip: Tensor) -> Tensor:
        upsampled = F.interpolate(inputs, size=skip.shape[-2:], mode="bilinear", align_corners=False)
        gated_skip = skip * self.skip_gate(skip)
        return self.fuse(torch.cat((upsampled, gated_skip), dim=1))


class DilatedContext(nn.Module):
    """Multi-dilation context at the coarsest scale without candidate-owned postprocessing."""

    def __init__(self, channels: int) -> None:
        super().__init__()
        self.d1 = ResidualBlock(channels, channels, dilation=1)
        self.d2 = ResidualBlock(channels, channels, dilation=2)
        self.d4 = ResidualBlock(channels, channels, dilation=4)
        self.project = ConvNormAct(channels * 3, channels, kernel_size=1)

    def forward(self, inputs: Tensor) -> Tensor:
        return self.project(torch.cat((self.d1(inputs), self.d2(inputs), self.d4(inputs)), dim=1))


class MultiScaleSkipFusion(nn.Module):
    """Fuse full-resolution decoder output with projected lower-scale decoder context and stem features."""

    def __init__(self, base_channels: int) -> None:
        super().__init__()
        self.dec1_project = ConvNormAct(base_channels * 2, base_channels, kernel_size=1)
        self.dec2_project = ConvNormAct(base_channels * 4, base_channels, kernel_size=1)
        self.stem_gate = nn.Sequential(nn.Conv2d(base_channels, base_channels, kernel_size=1, bias=True), nn.Sigmoid())
        self.dec0_gate = nn.Sequential(nn.Conv2d(base_channels, base_channels, kernel_size=1, bias=True), nn.Sigmoid())
        self.dec1_gate = nn.Sequential(nn.Conv2d(base_channels, base_channels, kernel_size=1, bias=True), nn.Sigmoid())
        self.dec2_gate = nn.Sequential(nn.Conv2d(base_channels, base_channels, kernel_size=1, bias=True), nn.Sigmoid())
        self.fuse = nn.Sequential(
            ConvNormAct(base_channels * 4, base_channels * 2),
            ResidualBlock(base_channels * 2, base_channels * 2),
            ConvNormAct(base_channels * 2, base_channels),
            ResidualBlock(base_channels, base_channels),
        )

    def forward(self, dec0: Tensor, dec1: Tensor, dec2: Tensor, stem: Tensor) -> Tensor:
        target_size = dec0.shape[-2:]
        dec1_full = self.dec1_project(F.interpolate(dec1, size=target_size, mode="bilinear", align_corners=False))
        dec2_full = self.dec2_project(F.interpolate(dec2, size=target_size, mode="bilinear", align_corners=False))
        gated = torch.cat(
            (
                dec0 * self.dec0_gate(dec0),
                dec1_full * self.dec1_gate(dec1_full),
                dec2_full * self.dec2_gate(dec2_full),
                stem * self.stem_gate(stem),
            ),
            dim=1,
        )
        return self.fuse(gated)


class HighResolutionLineRefiner(nn.Module):
    """Full-resolution refinement path aimed at preserving thin contrail evidence."""

    def __init__(self, channels: int) -> None:
        super().__init__()
        self.local = ConvNormAct(channels, channels)
        self.dilated2 = ConvNormAct(channels, channels, dilation=2)
        self.dilated4 = ConvNormAct(channels, channels, dilation=4)
        self.project = nn.Sequential(
            ConvNormAct(channels * 3, channels),
            ResidualBlock(channels, channels),
        )

    def forward(self, inputs: Tensor) -> Tensor:
        return self.project(torch.cat((self.local(inputs), self.dilated2(inputs), self.dilated4(inputs)), dim=1))


class LineGatedMaskRefiner(nn.Module):
    """Use a supervised centerline-proposal branch as differentiable attention for mask logits."""

    def __init__(self, channels: int) -> None:
        super().__init__()
        self.line_refiner = HighResolutionLineRefiner(channels)
        self.centerline_head = nn.Conv2d(channels, 1, kernel_size=1)
        self.mask_refiner = nn.Sequential(
            ResidualBlock(channels, channels),
            ConvNormAct(channels, channels),
        )
        self.mask_fuse = nn.Sequential(
            ConvNormAct(channels * 3, channels),
            ResidualBlock(channels, channels),
        )
        self.mask_head = nn.Conv2d(channels, 1, kernel_size=1)

    def forward(self, inputs: Tensor) -> dict[str, Tensor]:
        line_features = self.line_refiner(inputs)
        centerline_logits = self.centerline_head(line_features)
        line_attention = torch.sigmoid(centerline_logits)
        mask_features = self.mask_refiner(inputs)
        gated_mask_features = mask_features * (0.5 + line_attention)
        gated_line_features = line_features * (0.5 + line_attention)
        fused = self.mask_fuse(torch.cat((inputs, gated_mask_features, gated_line_features), dim=1))
        return {
            "mask_logits": self.mask_head(fused),
            "centerline_logits": centerline_logits,
        }


class FullSpectralBTDHighResolutionLineGatedMaskUNet(nn.Module):
    """High-resolution U-Net decoder with centerline-supervised line attention for mask refinement."""

    def __init__(self) -> None:
        super().__init__()
        self.front_end = NormalizedBTDFrontEnd(learned_channels=16)
        base = 48
        self.stem = nn.Sequential(
            ConvNormAct(self.front_end.out_channels, base),
            ResidualBlock(base, base),
        )
        self.enc1 = ResidualBlock(base, base)
        self.down1 = nn.Sequential(nn.MaxPool2d(2), ResidualBlock(base, base * 2))
        self.down2 = nn.Sequential(nn.MaxPool2d(2), ResidualBlock(base * 2, base * 4))
        self.down3 = nn.Sequential(nn.MaxPool2d(2), ResidualBlock(base * 4, base * 8))
        self.context = DilatedContext(base * 8)
        self.up2 = UpFuseBlock(base * 8, base * 4, base * 4)
        self.up1 = UpFuseBlock(base * 4, base * 2, base * 2)
        self.up0 = UpFuseBlock(base * 2, base, base)
        self.multi_scale_fusion = MultiScaleSkipFusion(base)
        self.line_gated_head = LineGatedMaskRefiner(base)

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
        fused = self.multi_scale_fusion(dec0, dec1, dec2, stem)
        return self.line_gated_head(fused)


def _validate_centerline_auxiliary_output(output_spec: dict[str, object]) -> None:
    auxiliary_outputs = output_spec.get("auxiliary_outputs")
    expected = [{"target": "centerline", "name": "centerline_logits", "shape": [1, 256, 256]}]
    if auxiliary_outputs != expected:
        raise ValueError(
            "abi057_fullspectral_btd_hrline_unet_line_gated_mask_refiner_cldice_centerline_aux_v1 requires "
            "exactly one trusted centerline auxiliary output named centerline_logits"
        )


def build_model(input_spec: dict[str, object], output_spec: dict[str, object]) -> nn.Module:
    """Build the model for the Harness-supplied ABI contract."""

    if input_spec.get("mode") != "abi_16ch" or input_spec.get("shape") != [16, 256, 256]:
        raise ValueError(
            "abi057_fullspectral_btd_hrline_unet_line_gated_mask_refiner_cldice_centerline_aux_v1 requires "
            "abi_16ch [16, 256, 256] input"
        )
    if output_spec.get("form") != "mask_logits" or output_spec.get("shape") != [1, 256, 256]:
        raise ValueError(
            "abi057_fullspectral_btd_hrline_unet_line_gated_mask_refiner_cldice_centerline_aux_v1 requires "
            "mask_logits [1, 256, 256] primary output"
        )
    _validate_centerline_auxiliary_output(output_spec)
    return FullSpectralBTDHighResolutionLineGatedMaskUNet()
