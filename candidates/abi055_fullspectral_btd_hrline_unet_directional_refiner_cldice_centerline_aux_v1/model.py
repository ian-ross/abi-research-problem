"""Full-spectral BTD high-resolution line U-Net with an architecture-level directional continuity refiner."""

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


class AsymmetricConvNormAct(nn.Module):
    """Directional convolution branch for elongated thin-line evidence."""

    def __init__(self, in_channels: int, out_channels: int, *, kernel_size: tuple[int, int]) -> None:
        super().__init__()
        padding = (kernel_size[0] // 2, kernel_size[1] // 2)
        self.block = nn.Sequential(
            nn.Conv2d(in_channels, out_channels, kernel_size=kernel_size, padding=padding, bias=False),
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


class DirectionalContinuityRefiner(nn.Module):
    """Full-resolution architecture path for horizontal and vertical thin-line continuity.

    This replaces the ABI-053/054 isotropic multi-dilation refiner with asymmetric
    1 x K and K x 1 branches plus a learned gate. It remains a model-internal
    feature refiner: it does not threshold, filter, skeletonize, or postprocess masks.
    """

    def __init__(self, channels: int) -> None:
        super().__init__()
        self.local = ConvNormAct(channels, channels)
        self.horizontal7 = AsymmetricConvNormAct(channels, channels, kernel_size=(1, 7))
        self.vertical7 = AsymmetricConvNormAct(channels, channels, kernel_size=(7, 1))
        self.horizontal15 = AsymmetricConvNormAct(channels, channels, kernel_size=(1, 15))
        self.vertical15 = AsymmetricConvNormAct(channels, channels, kernel_size=(15, 1))
        self.direction_project = ConvNormAct(channels * 4, channels, kernel_size=1)
        self.fusion_gate = nn.Sequential(
            ConvNormAct(channels * 2, channels, kernel_size=1),
            nn.Conv2d(channels, channels, kernel_size=1, bias=True),
            nn.Sigmoid(),
        )
        self.output = ResidualBlock(channels, channels)

    def forward(self, inputs: Tensor) -> Tensor:
        local = self.local(inputs)
        directional = self.direction_project(
            torch.cat(
                (
                    self.horizontal7(inputs),
                    self.vertical7(inputs),
                    self.horizontal15(inputs),
                    self.vertical15(inputs),
                ),
                dim=1,
            )
        )
        gate = self.fusion_gate(torch.cat((local, directional), dim=1))
        return self.output(inputs + local + gate * directional)


class FullSpectralBTDHighResolutionDirectionalLineUNet(nn.Module):
    """High-resolution U-Net-style decoder with directional continuity refinement."""

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
        self.full_res_refiner = DirectionalContinuityRefiner(base)
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
        refined = self.full_res_refiner(dec0 + stem)
        return {
            "mask_logits": self.mask_head(refined),
            "centerline_logits": self.centerline_head(refined),
        }


def _validate_centerline_auxiliary_output(output_spec: dict[str, object]) -> None:
    auxiliary_outputs = output_spec.get("auxiliary_outputs")
    expected = [{"target": "centerline", "name": "centerline_logits", "shape": [1, 256, 256]}]
    if auxiliary_outputs != expected:
        raise ValueError(
            "abi055_fullspectral_btd_hrline_unet_directional_refiner_cldice_centerline_aux_v1 requires "
            "exactly one trusted centerline auxiliary output named centerline_logits"
        )


def build_model(input_spec: dict[str, object], output_spec: dict[str, object]) -> nn.Module:
    """Build the model for the Harness-supplied ABI contract."""

    if input_spec.get("mode") != "abi_16ch" or input_spec.get("shape") != [16, 256, 256]:
        raise ValueError(
            "abi055_fullspectral_btd_hrline_unet_directional_refiner_cldice_centerline_aux_v1 requires "
            "abi_16ch [16, 256, 256] input"
        )
    if output_spec.get("form") != "mask_logits" or output_spec.get("shape") != [1, 256, 256]:
        raise ValueError(
            "abi055_fullspectral_btd_hrline_unet_directional_refiner_cldice_centerline_aux_v1 requires "
            "mask_logits [1, 256, 256] primary output"
        )
    _validate_centerline_auxiliary_output(output_spec)
    return FullSpectralBTDHighResolutionDirectionalLineUNet()
