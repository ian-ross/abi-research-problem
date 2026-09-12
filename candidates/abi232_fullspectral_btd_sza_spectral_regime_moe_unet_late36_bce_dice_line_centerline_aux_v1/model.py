"""Spectral/SZA-regime gated mixture-of-experts U-Net for ABI contrails."""

from __future__ import annotations

import torch
import torch.nn.functional as F
from torch import Tensor, nn


CANDIDATE_ID = "abi232_fullspectral_btd_sza_spectral_regime_moe_unet_late36_bce_dice_line_centerline_aux_v1"


class NormalizedBTDSZAFrontEnd(nn.Module):
    """Build finite normalized ABI, thermal-difference, SZA, and learned features."""

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
    # Zero-based provider-approved ABI channel pairs. These are channel-derived BTD features.
    _BTD_PAIRS = (
        (12, 13),
        (13, 14),
        (12, 14),
        (10, 13),
        (6, 13),
        (7, 9),
        (7, 12),
        (8, 13),
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


class ConvNormAct(nn.Module):
    """Convolution, GroupNorm, and GELU for stable small-batch training."""

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
    """Compact residual block."""

    def __init__(self, in_channels: int, out_channels: int, *, dilation: int = 1) -> None:
        super().__init__()
        self.conv1 = ConvNormAct(in_channels, out_channels, dilation=dilation)
        self.conv2 = nn.Sequential(
            nn.Conv2d(out_channels, out_channels, kernel_size=3, padding=1, bias=False),
            nn.GroupNorm(_group_count(out_channels), out_channels),
        )
        self.skip = nn.Identity() if in_channels == out_channels else nn.Conv2d(in_channels, out_channels, 1, bias=False)
        self.act = nn.GELU()

    def forward(self, inputs: Tensor) -> Tensor:
        return self.act(self.conv2(self.conv1(inputs)) + self.skip(inputs))


class EncoderDown(nn.Module):
    """Downsample by two and encode."""

    def __init__(self, in_channels: int, out_channels: int) -> None:
        super().__init__()
        self.block = nn.Sequential(
            nn.MaxPool2d(2),
            ResidualBlock(in_channels, out_channels),
            ResidualBlock(out_channels, out_channels),
        )

    def forward(self, inputs: Tensor) -> Tensor:
        return self.block(inputs)


class DecoderFuse(nn.Module):
    """Upsample and fuse with a skip feature."""

    def __init__(self, in_channels: int, skip_channels: int, out_channels: int) -> None:
        super().__init__()
        self.project = nn.Sequential(
            ConvNormAct(in_channels + skip_channels, out_channels),
            ResidualBlock(out_channels, out_channels),
        )

    def forward(self, inputs: Tensor, skip: Tensor) -> Tensor:
        upsampled = F.interpolate(inputs, size=skip.shape[-2:], mode="bilinear", align_corners=False)
        return self.project(torch.cat((upsampled, skip), dim=1))


class ASPPContext(nn.Module):
    """Lightweight ASPP context at the bottleneck."""

    def __init__(self, in_channels: int, out_channels: int) -> None:
        super().__init__()
        branch_channels = out_channels // 4
        self.local = ConvNormAct(in_channels, branch_channels, kernel_size=1)
        self.dilated2 = ConvNormAct(in_channels, branch_channels, dilation=2)
        self.dilated4 = ConvNormAct(in_channels, branch_channels, dilation=4)
        self.dilated8 = ConvNormAct(in_channels, branch_channels, dilation=8)
        self.project = nn.Sequential(
            ConvNormAct(branch_channels * 4, out_channels, kernel_size=1),
            ResidualBlock(out_channels, out_channels),
        )

    def forward(self, inputs: Tensor) -> Tensor:
        return self.project(
            torch.cat(
                (
                    self.local(inputs),
                    self.dilated2(inputs),
                    self.dilated4(inputs),
                    self.dilated8(inputs),
                ),
                dim=1,
            )
        )


class SpectralRegimeMoEStem(nn.Module):
    """Learn soft spectral/SZA regime gates over three feature experts.

    Gates are inferred only from provider-approved ABI/SZA-derived tensors. They do not
    use Dataset Source identity, scene identity, coordinates, paths, or postprocessing.
    """

    def __init__(self, in_channels: int, out_channels: int, experts: int = 3) -> None:
        super().__init__()
        self.experts = nn.ModuleList(
            (
                nn.Sequential(ConvNormAct(in_channels, out_channels, kernel_size=1), ResidualBlock(out_channels, out_channels)),
                nn.Sequential(ConvNormAct(in_channels, out_channels, kernel_size=3), ResidualBlock(out_channels, out_channels)),
                nn.Sequential(ConvNormAct(in_channels, out_channels, kernel_size=5), ResidualBlock(out_channels, out_channels, dilation=2)),
            )
        )
        self.global_gate = nn.Sequential(
            nn.AdaptiveAvgPool2d(1),
            nn.Flatten(),
            nn.Linear(in_channels, max(12, in_channels // 2)),
            nn.GELU(),
            nn.Linear(max(12, in_channels // 2), experts),
        )
        self.spatial_gate = nn.Conv2d(in_channels, experts, kernel_size=1, bias=True)
        self.fuse = ResidualBlock(out_channels, out_channels)

    def forward(self, features: Tensor) -> Tensor:
        global_logits = self.global_gate(features).view(features.shape[0], len(self.experts), 1, 1)
        spatial_logits = self.spatial_gate(features)
        gates = torch.softmax(global_logits + spatial_logits, dim=1)
        expert_features = torch.stack([expert(features) for expert in self.experts], dim=1)
        mixed = (expert_features * gates.unsqueeze(2)).sum(dim=1)
        return self.fuse(mixed)


class DetailBridge(nn.Module):
    """High-resolution local/mid-scale signed-detail bridge."""

    def __init__(self, in_channels: int, out_channels: int) -> None:
        super().__init__()
        self.raw = ConvNormAct(in_channels, out_channels, kernel_size=1)
        self.local_pos = ConvNormAct(in_channels, out_channels, kernel_size=1)
        self.local_neg = ConvNormAct(in_channels, out_channels, kernel_size=1)
        self.mid_pos = ConvNormAct(in_channels, out_channels, kernel_size=1)
        self.mid_neg = ConvNormAct(in_channels, out_channels, kernel_size=1)
        self.project = nn.Sequential(ConvNormAct(out_channels * 5, out_channels), ResidualBlock(out_channels, out_channels))

    def forward(self, features: Tensor) -> Tensor:
        local = F.avg_pool2d(features, kernel_size=7, stride=1, padding=3, count_include_pad=False)
        mid = F.avg_pool2d(features, kernel_size=15, stride=1, padding=7, count_include_pad=False)
        local_detail = features - local
        mid_detail = features - mid
        return self.project(
            torch.cat(
                (
                    self.raw(features),
                    self.local_pos(F.relu(local_detail)),
                    self.local_neg(F.relu(-local_detail)),
                    self.mid_pos(F.relu(mid_detail)),
                    self.mid_neg(F.relu(-mid_detail)),
                ),
                dim=1,
            )
        )


class RegimeAwareFusion(nn.Module):
    """Fuse decoder, detail, and regime-gated evidence before prediction heads."""

    def __init__(self, channels: int) -> None:
        super().__init__()
        self.gate = nn.Sequential(
            ConvNormAct(channels * 3, channels, kernel_size=1),
            nn.Conv2d(channels, channels, kernel_size=1),
            nn.Sigmoid(),
        )
        self.project = nn.Sequential(ConvNormAct(channels * 3, channels), ResidualBlock(channels, channels))

    def forward(self, decoded: Tensor, detail: Tensor, stem: Tensor) -> Tensor:
        support = torch.cat((decoded, detail, stem), dim=1)
        gate = self.gate(support)
        calibrated = decoded + gate * detail + (1.0 - gate) * stem
        return self.project(torch.cat((calibrated, detail, stem), dim=1))


class SpectralRegimeMoEUNet(nn.Module):
    """Compact single-frame spectral/SZA-regime MoE encoder-decoder."""

    def __init__(self) -> None:
        super().__init__()
        self.front_end = NormalizedBTDSZAFrontEnd(learned_channels=16)
        base = 32
        self.stem = SpectralRegimeMoEStem(self.front_end.out_channels, base)
        self.enc0 = ResidualBlock(base, base)
        self.enc1 = EncoderDown(base, base * 2)
        self.enc2 = EncoderDown(base * 2, base * 3)
        self.enc3 = EncoderDown(base * 3, base * 4)
        self.context = ASPPContext(base * 4, base * 4)
        self.up2 = DecoderFuse(base * 4, base * 3, base * 3)
        self.up1 = DecoderFuse(base * 3, base * 2, base * 2)
        self.up0 = DecoderFuse(base * 2, base, base)
        self.detail = DetailBridge(self.front_end.out_channels, base)
        self.fusion = RegimeAwareFusion(base)
        self.refine = nn.Sequential(ResidualBlock(base, base), ConvNormAct(base, base))
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
        detail = self.detail(features)
        fused = self.fusion(dec0, detail, stem)
        refined = self.refine(fused)
        return {
            "mask_logits": self.mask_head(refined),
            "line_logits": self.line_head(refined),
            "centerline_logits": self.centerline_head(refined),
        }


def _validate_auxiliary_outputs(output_spec: dict[str, object]) -> None:
    expected = [
        {"target": "line", "name": "line_logits", "shape": [1, 256, 256]},
        {"target": "centerline", "name": "centerline_logits", "shape": [1, 256, 256]},
    ]
    if output_spec.get("auxiliary_outputs") != expected:
        raise ValueError(f"{CANDIDATE_ID} requires trusted line_logits and centerline_logits auxiliary outputs")


def build_model(input_spec: dict[str, object], output_spec: dict[str, object]) -> nn.Module:
    """Build the Harness-facing model."""

    if input_spec.get("mode") != "abi_16ch_plus_sza" or input_spec.get("shape") != [17, 256, 256]:
        raise ValueError(f"{CANDIDATE_ID} requires abi_16ch_plus_sza [17, 256, 256] input")
    if output_spec.get("form") != "mask_logits" or output_spec.get("shape") != [1, 256, 256]:
        raise ValueError(f"{CANDIDATE_ID} requires mask_logits [1, 256, 256] primary output")
    _validate_auxiliary_outputs(output_spec)
    return SpectralRegimeMoEUNet()
