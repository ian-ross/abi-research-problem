"""Full-spectral BTD+SZA signed-detail full-scale skip ASPP decoder for ABI contrail segmentation."""

from __future__ import annotations

import torch
import torch.nn.functional as F
from torch import Tensor, nn


CANDIDATE_ID = "abi183_fullspectral_btd_sza_signed_detail_fullscale_skip_aspp_lineaux_bce_dice_centerline_aux_v1"


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
        # Raw normalized ABI channels + thermal BTD planes + normalized SZA + cos(SZA) + learned mixture.
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


class SignedDetailContextStem(nn.Module):
    """Project raw context plus signed local/mid-scale detail anomalies without postprocessing."""

    def __init__(self, in_channels: int, out_channels: int) -> None:
        super().__init__()
        self.raw_project = ConvNormAct(in_channels, out_channels, kernel_size=1)
        self.local_positive_project = ConvNormAct(in_channels, out_channels, kernel_size=1)
        self.local_negative_project = ConvNormAct(in_channels, out_channels, kernel_size=1)
        self.mid_positive_project = ConvNormAct(in_channels, out_channels, kernel_size=1)
        self.mid_negative_project = ConvNormAct(in_channels, out_channels, kernel_size=1)
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
                    self.local_positive_project(F.relu(local_detail)),
                    self.local_negative_project(F.relu(-local_detail)),
                    self.mid_positive_project(F.relu(mid_detail)),
                    self.mid_negative_project(F.relu(-mid_detail)),
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


class FullScaleSkipFusion(nn.Module):
    """Fuse all encoder/decoder scales at mask resolution without candidate-owned postprocessing."""

    def __init__(self, base_channels: int) -> None:
        super().__init__()
        branch = 16
        self.stem_project = ConvNormAct(base_channels, branch, kernel_size=1)
        self.enc0_project = ConvNormAct(base_channels, branch, kernel_size=1)
        self.enc1_project = ConvNormAct(base_channels * 2, branch, kernel_size=1)
        self.enc2_project = ConvNormAct(base_channels * 4, branch, kernel_size=1)
        self.enc3_project = ConvNormAct(base_channels * 8, branch, kernel_size=1)
        self.context_project = ConvNormAct(base_channels * 8, branch, kernel_size=1)
        self.dec2_project = ConvNormAct(base_channels * 4, branch, kernel_size=1)
        self.dec1_project = ConvNormAct(base_channels * 2, branch, kernel_size=1)
        self.dec0_project = ConvNormAct(base_channels, branch, kernel_size=1)
        self.detail_project = ConvNormAct(base_channels, branch, kernel_size=1)
        self.fuse = nn.Sequential(
            ConvNormAct(branch * 10, base_channels),
            ResidualBlock(base_channels, base_channels),
        )

    @staticmethod
    def _resize(inputs: Tensor, size: tuple[int, int]) -> Tensor:
        if inputs.shape[-2:] == size:
            return inputs
        return F.interpolate(inputs, size=size, mode="bilinear", align_corners=False)

    def forward(
        self,
        *,
        stem: Tensor,
        enc0: Tensor,
        enc1: Tensor,
        enc2: Tensor,
        enc3: Tensor,
        context: Tensor,
        dec2: Tensor,
        dec1: Tensor,
        dec0: Tensor,
        detail: Tensor,
    ) -> Tensor:
        size = dec0.shape[-2:]
        branches = (
            self.stem_project(stem),
            self.enc0_project(enc0),
            self.enc1_project(self._resize(enc1, size)),
            self.enc2_project(self._resize(enc2, size)),
            self.enc3_project(self._resize(enc3, size)),
            self.context_project(self._resize(context, size)),
            self.dec2_project(self._resize(dec2, size)),
            self.dec1_project(self._resize(dec1, size)),
            self.dec0_project(dec0),
            self.detail_project(detail),
        )
        return self.fuse(torch.cat(branches, dim=1))


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


class FullSpectralBTDSZASignedDetailFullScaleSkipASPPDecoder(nn.Module):
    """ASPP decoder with signed high-resolution detail streams, full-scale skip aggregation, and Solar Geometry Input."""

    def __init__(self) -> None:
        super().__init__()
        self.front_end = NormalizedBTDSZAFrontEnd(learned_channels=16)
        base = 40
        self.stem = SignedDetailContextStem(self.front_end.out_channels, base)
        self.enc0 = ResidualBlock(base, base)
        self.enc1 = EncoderDown(base, base * 2)
        self.enc2 = EncoderDown(base * 2, base * 4)
        self.enc3 = EncoderDown(base * 4, base * 8)
        self.context = ASPPContext(base * 8, base * 8)
        self.up2 = DecoderFuse(base * 8, base * 4, base * 4)
        self.up1 = DecoderFuse(base * 4, base * 2, base * 2)
        self.up0 = DecoderFuse(base * 2, base, base)
        self.highres_detail = SignedDetailContextStem(self.front_end.out_channels, base)
        self.fullscale_fusion = FullScaleSkipFusion(base)
        self.final_project = nn.Sequential(
            ConvNormAct(base * 4, base),
            ResidualBlock(base, base),
        )
        self.refine = LineAwareRefinement(base)
        self.mask_head = nn.Conv2d(base, 1, kernel_size=1)
        self.line_head = nn.Conv2d(base, 1, kernel_size=1)
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
        fullscale = self.fullscale_fusion(
            stem=stem,
            enc0=enc0,
            enc1=enc1,
            enc2=enc2,
            enc3=enc3,
            context=context,
            dec2=dec2,
            dec1=dec1,
            dec0=dec0,
            detail=detail,
        )
        fused = self.final_project(torch.cat((dec0, detail, stem, fullscale), dim=1))
        refined = self.refine(fused)
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
    return FullSpectralBTDSZASignedDetailFullScaleSkipASPPDecoder()
