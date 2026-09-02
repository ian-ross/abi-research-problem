"""Full-spectral BTD ASPP/detail decoder for ABI contrail segmentation."""

from __future__ import annotations

import torch
import torch.nn.functional as F
from torch import Tensor, nn


CANDIDATE_ID = "abi121_fullspectral_btd_aspp_detail_decoder_focal_tversky_centerline_aux_v1"


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
    """Residual block used for encoder, decoder, and refinement features."""

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


class DetailContextStem(nn.Module):
    """Project raw, high-frequency detail, and broad cloud context without postprocessing."""

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
        local = _smooth(inputs, 9)
        broad = _smooth(inputs, 25)
        detail = inputs - local
        return self.fuse(
            torch.cat(
                (
                    self.raw_project(inputs),
                    self.detail_project(detail),
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


class ASPPContext(nn.Module):
    """Atrous pyramid plus image-level context at the coarsest encoder scale."""

    def __init__(self, in_channels: int, out_channels: int) -> None:
        super().__init__()
        branch = out_channels // 2
        self.branch1 = ConvNormAct(in_channels, branch, kernel_size=1)
        self.branch2 = ConvNormAct(in_channels, branch, dilation=2)
        self.branch4 = ConvNormAct(in_channels, branch, dilation=4)
        self.branch8 = ConvNormAct(in_channels, branch, dilation=8)
        self.image_pool = nn.Sequential(
            nn.AdaptiveAvgPool2d(1),
            ConvNormAct(in_channels, branch, kernel_size=1),
        )
        self.project = nn.Sequential(
            ConvNormAct(branch * 5, out_channels, kernel_size=1),
            ResidualBlock(out_channels, out_channels),
        )

    def forward(self, inputs: Tensor) -> Tensor:
        pooled = F.interpolate(self.image_pool(inputs), size=inputs.shape[-2:], mode="bilinear", align_corners=False)
        return self.project(
            torch.cat((self.branch1(inputs), self.branch2(inputs), self.branch4(inputs), self.branch8(inputs), pooled), dim=1)
        )


class DecoderFuse(nn.Module):
    """Upsample decoder features and merge with a projected encoder skip."""

    def __init__(self, in_channels: int, skip_channels: int, out_channels: int) -> None:
        super().__init__()
        self.input_project = ConvNormAct(in_channels, out_channels, kernel_size=1)
        self.skip_project = ConvNormAct(skip_channels, out_channels, kernel_size=1)
        self.fuse = nn.Sequential(
            ConvNormAct(out_channels * 2, out_channels),
            ResidualBlock(out_channels, out_channels),
        )

    def forward(self, inputs: Tensor, skip: Tensor) -> Tensor:
        upsampled = F.interpolate(inputs, size=skip.shape[-2:], mode="bilinear", align_corners=False)
        return self.fuse(torch.cat((self.input_project(upsampled), self.skip_project(skip)), dim=1))


class LineAwareRefinement(nn.Module):
    """Final learned feature refinement using horizontal/vertical context and local detail."""

    def __init__(self, channels: int) -> None:
        super().__init__()
        self.detail_project = ConvNormAct(channels, channels)
        self.horizontal = nn.Sequential(
            nn.Conv2d(channels, channels, kernel_size=(1, 15), padding=(0, 7), bias=False),
            nn.GroupNorm(_group_count(channels), channels),
            nn.GELU(),
        )
        self.vertical = nn.Sequential(
            nn.Conv2d(channels, channels, kernel_size=(15, 1), padding=(7, 0), bias=False),
            nn.GroupNorm(_group_count(channels), channels),
            nn.GELU(),
        )
        self.gate = nn.Sequential(
            ConvNormAct(channels * 4, channels, kernel_size=1),
            nn.Conv2d(channels, channels, kernel_size=1, bias=True),
            nn.Sigmoid(),
        )
        self.project = nn.Sequential(
            ConvNormAct(channels * 4, channels),
            ResidualBlock(channels, channels),
        )

    def forward(self, inputs: Tensor) -> Tensor:
        detail = self.detail_project(inputs - _smooth(inputs, 7))
        horizontal = self.horizontal(inputs)
        vertical = self.vertical(inputs)
        context = _smooth(inputs, 17)
        gate = self.gate(torch.cat((inputs, detail, horizontal, vertical), dim=1))
        calibrated = inputs * (0.75 + 0.5 * gate)
        return self.project(torch.cat((calibrated, detail, horizontal, context), dim=1))


class FullSpectralBTDASPPDetailDecoder(nn.Module):
    """ASPP encoder-decoder retaining high-resolution BTD/detail evidence."""

    def __init__(self) -> None:
        super().__init__()
        self.front_end = NormalizedBTDFrontEnd(learned_channels=16)
        base = 40
        self.stem = DetailContextStem(self.front_end.out_channels, base)
        self.enc0 = ResidualBlock(base, base)
        self.enc1 = EncoderDown(base, base * 2)
        self.enc2 = EncoderDown(base * 2, base * 4)
        self.enc3 = EncoderDown(base * 4, base * 8)
        self.context = ASPPContext(base * 8, base * 8)
        self.up2 = DecoderFuse(base * 8, base * 4, base * 4)
        self.up1 = DecoderFuse(base * 4, base * 2, base * 2)
        self.up0 = DecoderFuse(base * 2, base, base)
        self.highres_detail = DetailContextStem(self.front_end.out_channels, base)
        self.final_project = nn.Sequential(
            ConvNormAct(base * 3, base),
            ResidualBlock(base, base),
        )
        self.refine = LineAwareRefinement(base)
        self.mask_head = nn.Conv2d(base, 1, kernel_size=1)
        self.centerline_head = nn.Conv2d(base, 1, kernel_size=1)

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
        detail = self.highres_detail(features)
        fused = self.final_project(torch.cat((dec0, detail, stem), dim=1))
        refined = self.refine(fused)
        return {
            "mask_logits": self.mask_head(refined),
            "centerline_logits": self.centerline_head(refined),
        }


def _validate_centerline_auxiliary_output(output_spec: dict[str, object]) -> None:
    auxiliary_outputs = output_spec.get("auxiliary_outputs")
    expected = [{"target": "centerline", "name": "centerline_logits", "shape": [1, 256, 256]}]
    if auxiliary_outputs != expected:
        raise ValueError(f"{CANDIDATE_ID} requires exactly one trusted centerline auxiliary output named centerline_logits")


def build_model(input_spec: dict[str, object], output_spec: dict[str, object]) -> nn.Module:
    """Build the model for the Harness-supplied ABI contract."""

    if input_spec.get("mode") != "abi_16ch" or input_spec.get("shape") != [16, 256, 256]:
        raise ValueError(f"{CANDIDATE_ID} requires abi_16ch [16, 256, 256] input")
    if output_spec.get("form") != "mask_logits" or output_spec.get("shape") != [1, 256, 256]:
        raise ValueError(f"{CANDIDATE_ID} requires mask_logits [1, 256, 256] primary output")
    _validate_centerline_auxiliary_output(output_spec)
    return FullSpectralBTDASPPDetailDecoder()
