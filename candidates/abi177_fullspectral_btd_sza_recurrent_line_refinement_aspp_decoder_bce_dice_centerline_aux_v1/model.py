"""Full-spectral BTD+SZA recurrent line-refinement ASPP decoder for ABI contrail segmentation."""

from __future__ import annotations

import torch
import torch.nn.functional as F
from torch import Tensor, nn


CANDIDATE_ID = "abi177_fullspectral_btd_sza_recurrent_line_refinement_aspp_decoder_bce_dice_centerline_aux_v1"


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
        self.anchor_channels = 10 + len(self._BTD_PAIRS) + 2

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

    def anchor_features(self, features: Tensor) -> Tensor:
        """Select thermal ABI channels, BTD planes, and SZA features from the approved front end."""

        thermal = features[:, 6:16, :, :]
        btd = features[:, 16:24, :, :]
        sza = features[:, 24:26, :, :]
        return torch.cat((thermal, btd, sza), dim=1)


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
    """Fuse encoder/decoder scales plus thermal support at mask resolution."""

    def __init__(self, base_channels: int) -> None:
        super().__init__()
        branch = 16
        self.enc0_project = ConvNormAct(base_channels, branch, kernel_size=1)
        self.enc1_project = ConvNormAct(base_channels * 2, branch, kernel_size=1)
        self.enc2_project = ConvNormAct(base_channels * 4, branch, kernel_size=1)
        self.context_project = ConvNormAct(base_channels * 8, branch, kernel_size=1)
        self.dec2_project = ConvNormAct(base_channels * 4, branch, kernel_size=1)
        self.dec1_project = ConvNormAct(base_channels * 2, branch, kernel_size=1)
        self.dec0_project = ConvNormAct(base_channels, branch, kernel_size=1)
        self.support_project = ConvNormAct(base_channels, branch, kernel_size=1)
        self.fuse = nn.Sequential(
            ConvNormAct(branch * 8, base_channels),
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
        enc0: Tensor,
        enc1: Tensor,
        enc2: Tensor,
        context: Tensor,
        dec2: Tensor,
        dec1: Tensor,
        dec0: Tensor,
        support: Tensor,
    ) -> Tensor:
        size = dec0.shape[-2:]
        branches = (
            self.enc0_project(enc0),
            self.enc1_project(self._resize(enc1, size)),
            self.enc2_project(self._resize(enc2, size)),
            self.context_project(self._resize(context, size)),
            self.dec2_project(self._resize(dec2, size)),
            self.dec1_project(self._resize(dec1, size)),
            self.dec0_project(dec0),
            self.support_project(support),
        )
        return self.fuse(torch.cat(branches, dim=1))


class ThermalAnchorSupport(nn.Module):
    """Compact thermal/BTD/SZA support branch derived only from approved channels."""

    def __init__(self, in_channels: int, out_channels: int) -> None:
        super().__init__()
        hidden = 24
        self.stem = nn.Sequential(
            ConvNormAct(in_channels, hidden, kernel_size=1),
            ResidualBlock(hidden, hidden),
        )
        self.down1 = EncoderDown(hidden, hidden * 2)
        self.down2 = EncoderDown(hidden * 2, hidden * 4)
        self.context = ASPPContext(hidden * 4, hidden * 4)
        self.up1 = DecoderFuse(hidden * 4, hidden * 2, hidden * 2)
        self.up0 = DecoderFuse(hidden * 2, hidden, hidden)
        self.project = nn.Sequential(
            ConvNormAct(hidden, out_channels),
            ResidualBlock(out_channels, out_channels),
        )

    def forward(self, anchor_features: Tensor) -> Tensor:
        stem = self.stem(anchor_features)
        low1 = self.down1(stem)
        low2 = self.down2(low1)
        context = self.context(low2)
        up1 = self.up1(context, low1)
        up0 = self.up0(up1, stem)
        return self.project(up0)


class RecurrentLineRefinement(nn.Module):
    """Shared additive recurrent feature refinement from line and thermal support evidence."""

    def __init__(self, channels: int, *, steps: int = 3) -> None:
        super().__init__()
        self.steps = steps
        self.state_project = ConvNormAct(channels, channels, kernel_size=1)
        self.support_project = ConvNormAct(channels, channels, kernel_size=1)
        self.horizontal = nn.Sequential(
            nn.Conv2d(channels, channels, kernel_size=(1, 19), padding=(0, 9), bias=False),
            nn.GroupNorm(_group_count(channels), channels),
            nn.GELU(),
        )
        self.vertical = nn.Sequential(
            nn.Conv2d(channels, channels, kernel_size=(19, 1), padding=(9, 0), bias=False),
            nn.GroupNorm(_group_count(channels), channels),
            nn.GELU(),
        )
        self.diagonal_local = ConvNormAct(channels, channels, dilation=2)
        self.update = nn.Sequential(
            ConvNormAct(channels * 6, channels),
            nn.Conv2d(channels, channels, kernel_size=3, padding=1, bias=False),
            nn.GroupNorm(_group_count(channels), channels),
        )
        self.output = nn.Sequential(
            ResidualBlock(channels, channels),
            ConvNormAct(channels, channels),
        )

    def forward(self, inputs: Tensor, support: Tensor) -> Tensor:
        state = self.state_project(inputs)
        support_features = self.support_project(support)
        for _ in range(self.steps):
            horizontal = self.horizontal(state)
            vertical = self.vertical(state)
            diagonal = self.diagonal_local(state)
            broad = _smooth(state, 17)
            update = self.update(torch.cat((state, support_features, horizontal, vertical, diagonal, broad), dim=1))
            state = state + 0.25 * torch.tanh(update)
        return self.output(state)


class FullSpectralBTDSZARecurrentLineRefinementASPPDecoder(nn.Module):
    """ASPP decoder with thermal anchor support and recurrent line refinement."""

    def __init__(self) -> None:
        super().__init__()
        self.front_end = NormalizedBTDSZAFrontEnd(learned_channels=16)
        base = 40
        self.stem = nn.Sequential(
            ConvNormAct(self.front_end.out_channels, base, kernel_size=1),
            ResidualBlock(base, base),
        )
        self.enc0 = ResidualBlock(base, base)
        self.enc1 = EncoderDown(base, base * 2)
        self.enc2 = EncoderDown(base * 2, base * 4)
        self.enc3 = EncoderDown(base * 4, base * 8)
        self.context = ASPPContext(base * 8, base * 8)
        self.up2 = DecoderFuse(base * 8, base * 4, base * 4)
        self.up1 = DecoderFuse(base * 4, base * 2, base * 2)
        self.up0 = DecoderFuse(base * 2, base, base)
        self.thermal_anchor = ThermalAnchorSupport(self.front_end.anchor_channels, base)
        self.fullscale_fusion = FullScaleSkipFusion(base)
        self.refine = RecurrentLineRefinement(base, steps=3)
        self.mask_head = nn.Conv2d(base, 1, kernel_size=1)
        self.centerline_head = nn.Conv2d(base, 1, kernel_size=1)

    def forward(self, inputs: Tensor) -> dict[str, Tensor]:
        features = self.front_end(inputs)
        anchor = self.thermal_anchor(self.front_end.anchor_features(features))
        stem = self.stem(features)
        enc0 = self.enc0(stem)
        enc1 = self.enc1(enc0)
        enc2 = self.enc2(enc1)
        enc3 = self.enc3(enc2)
        context = self.context(enc3)
        dec2 = self.up2(context, enc2)
        dec1 = self.up1(dec2, enc1)
        dec0 = self.up0(dec1, enc0)
        fullscale = self.fullscale_fusion(
            enc0=enc0,
            enc1=enc1,
            enc2=enc2,
            context=context,
            dec2=dec2,
            dec1=dec1,
            dec0=dec0,
            support=anchor,
        )
        refined = self.refine(fullscale, anchor)
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

    if input_spec.get("mode") != "abi_16ch_plus_sza" or input_spec.get("shape") != [17, 256, 256]:
        raise ValueError(f"{CANDIDATE_ID} requires abi_16ch_plus_sza [17, 256, 256] input")
    if output_spec.get("form") != "mask_logits" or output_spec.get("shape") != [1, 256, 256]:
        raise ValueError(f"{CANDIDATE_ID} requires mask_logits [1, 256, 256] primary output")
    _validate_centerline_auxiliary_output(output_spec)
    return FullSpectralBTDSZARecurrentLineRefinementASPPDecoder()
