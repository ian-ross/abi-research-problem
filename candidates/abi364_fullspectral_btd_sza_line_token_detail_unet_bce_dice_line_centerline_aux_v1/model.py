"""Full-spectral BTD+SZA U-Net with a low-rank line-token detail decoder."""

from __future__ import annotations

import torch
import torch.nn.functional as F
from torch import Tensor, nn


CANDIDATE_ID = "abi364_fullspectral_btd_sza_line_token_detail_unet_bce_dice_line_centerline_aux_v1"


class NormalizedBTDSZAFrontEnd(nn.Module):
    """Build normalized ABI, approved-channel BTD, SZA, and learned features."""

    _CHANNEL_MEANS = (
        0.1572, 0.1281, 0.1566, 0.0268, 0.0883, 0.0753,
        279.45, 233.17, 241.06, 248.44, 267.58, 250.28, 269.32, 268.23, 265.94, 255.61,
    )
    _CHANNEL_SCALES = (
        0.36, 0.34, 0.36, 0.16, 0.23, 0.18,
        42.0, 20.0, 25.0, 29.0, 43.0, 28.0, 44.0, 44.0, 43.0, 35.0,
    )
    _BTD_PAIRS = ((12, 13), (13, 14), (12, 14), (10, 13), (6, 13), (7, 9), (7, 12), (8, 13))
    _BTD_SCALE = 20.0

    def __init__(self, learned_channels: int = 16) -> None:
        super().__init__()
        self.register_buffer("channel_means", torch.tensor(self._CHANNEL_MEANS).view(1, 16, 1, 1))
        self.register_buffer("channel_scales", torch.tensor(self._CHANNEL_SCALES).view(1, 16, 1, 1))
        self.learned_mixer = nn.Sequential(nn.Conv2d(17, learned_channels, 1), nn.GELU())
        self.out_channels = 16 + len(self._BTD_PAIRS) + 2 + learned_channels

    def forward(self, inputs: Tensor) -> Tensor:
        if inputs.ndim != 4 or inputs.shape[1] != 17:
            raise ValueError(f"expected [N, 17, H, W] ABI+SZA tensor, got {tuple(inputs.shape)}")
        abi = inputs[:, :16]
        sza = torch.clamp(inputs[:, 16:17], 0.0, 180.0)
        normalized = (abi - self.channel_means) / self.channel_scales
        btd = torch.cat([(abi[:, a : a + 1] - abi[:, b : b + 1]) / self._BTD_SCALE for a, b in self._BTD_PAIRS], dim=1)
        sza_scaled = (sza - 90.0) / 90.0
        sza_cosine = torch.cos(torch.deg2rad(sza))
        learned = self.learned_mixer(torch.cat((normalized, sza_scaled), dim=1))
        return torch.cat((normalized, btd, sza_scaled, sza_cosine, learned), dim=1)


def _group_count(channels: int) -> int:
    for groups in (8, 5, 4, 2, 1):
        if channels % groups == 0:
            return groups
    return 1


def _smooth(inputs: Tensor, kernel_size: int) -> Tensor:
    return F.avg_pool2d(inputs, kernel_size=kernel_size, stride=1, padding=kernel_size // 2, count_include_pad=False)


class ConvNormAct(nn.Module):
    def __init__(self, in_channels: int, out_channels: int, *, kernel_size: int = 3, dilation: int = 1) -> None:
        super().__init__()
        padding = dilation * (kernel_size // 2)
        self.block = nn.Sequential(
            nn.Conv2d(in_channels, out_channels, kernel_size, padding=padding, dilation=dilation, bias=False),
            nn.GroupNorm(_group_count(out_channels), out_channels),
            nn.GELU(),
        )

    def forward(self, inputs: Tensor) -> Tensor:
        return self.block(inputs)


class ResidualBlock(nn.Module):
    def __init__(self, in_channels: int, out_channels: int, *, dilation: int = 1) -> None:
        super().__init__()
        self.conv1 = ConvNormAct(in_channels, out_channels, dilation=dilation)
        self.conv2 = nn.Sequential(
            nn.Conv2d(out_channels, out_channels, 3, padding=1, bias=False),
            nn.GroupNorm(_group_count(out_channels), out_channels),
        )
        self.skip = nn.Identity() if in_channels == out_channels else nn.Conv2d(in_channels, out_channels, 1, bias=False)
        self.act = nn.GELU()

    def forward(self, inputs: Tensor) -> Tensor:
        return self.act(self.conv2(self.conv1(inputs)) + self.skip(inputs))


class SignedDetailStem(nn.Module):
    """Expose local signed detail and broad context without target transforms."""

    def __init__(self, in_channels: int, out_channels: int) -> None:
        super().__init__()
        self.raw = ConvNormAct(in_channels, out_channels, kernel_size=1)
        self.fine_pos = ConvNormAct(in_channels, out_channels, kernel_size=1)
        self.fine_neg = ConvNormAct(in_channels, out_channels, kernel_size=1)
        self.context = ConvNormAct(in_channels, out_channels, kernel_size=1)
        self.fuse = nn.Sequential(ConvNormAct(out_channels * 4, out_channels), ResidualBlock(out_channels, out_channels))

    def forward(self, inputs: Tensor) -> Tensor:
        fine = inputs - _smooth(inputs, 7)
        broad = _smooth(inputs, 31)
        return self.fuse(torch.cat((self.raw(inputs), self.fine_pos(F.relu(fine)), self.fine_neg(F.relu(-fine)), self.context(broad)), dim=1))


class EncoderDown(nn.Module):
    def __init__(self, in_channels: int, out_channels: int) -> None:
        super().__init__()
        self.block = nn.Sequential(nn.MaxPool2d(2), ResidualBlock(in_channels, out_channels), ResidualBlock(out_channels, out_channels))

    def forward(self, inputs: Tensor) -> Tensor:
        return self.block(inputs)


class ASPPContext(nn.Module):
    def __init__(self, in_channels: int, out_channels: int) -> None:
        super().__init__()
        branch = out_channels // 4
        self.branch1 = ConvNormAct(in_channels, branch, kernel_size=1)
        self.branch2 = ConvNormAct(in_channels, branch, dilation=2)
        self.branch4 = ConvNormAct(in_channels, branch, dilation=4)
        self.branch8 = ConvNormAct(in_channels, branch, dilation=8)
        self.project = nn.Sequential(ConvNormAct(branch * 4, out_channels, kernel_size=1), ResidualBlock(out_channels, out_channels))

    def forward(self, inputs: Tensor) -> Tensor:
        return self.project(torch.cat((self.branch1(inputs), self.branch2(inputs), self.branch4(inputs), self.branch8(inputs)), dim=1))


class DecoderFuse(nn.Module):
    def __init__(self, in_channels: int, skip_channels: int, out_channels: int) -> None:
        super().__init__()
        self.input_project = ConvNormAct(in_channels, out_channels, kernel_size=1)
        self.skip_project = ConvNormAct(skip_channels, out_channels, kernel_size=1)
        self.fuse = nn.Sequential(ConvNormAct(out_channels * 2, out_channels), ResidualBlock(out_channels, out_channels))

    def forward(self, inputs: Tensor, skip: Tensor) -> Tensor:
        upsampled = F.interpolate(inputs, size=skip.shape[-2:], mode="bilinear", align_corners=False)
        return self.fuse(torch.cat((self.input_project(upsampled), self.skip_project(skip)), dim=1))


class LocalStripContext(nn.Module):
    """Depthwise horizontal/vertical strip evidence used only as model features."""

    def __init__(self, channels: int, width: int = 31) -> None:
        super().__init__()
        pad = width // 2
        self.horizontal = nn.Sequential(
            nn.Conv2d(channels, channels, kernel_size=(1, width), padding=(0, pad), groups=channels, bias=False),
            nn.Conv2d(channels, channels, 1, bias=False),
            nn.GroupNorm(_group_count(channels), channels),
            nn.GELU(),
        )
        self.vertical = nn.Sequential(
            nn.Conv2d(channels, channels, kernel_size=(width, 1), padding=(pad, 0), groups=channels, bias=False),
            nn.Conv2d(channels, channels, 1, bias=False),
            nn.GroupNorm(_group_count(channels), channels),
            nn.GELU(),
        )
        self.fuse = nn.Sequential(ConvNormAct(channels * 3, channels), ResidualBlock(channels, channels))

    def forward(self, inputs: Tensor) -> Tensor:
        detail = inputs - _smooth(inputs, 7)
        return self.fuse(torch.cat((inputs, self.horizontal(detail), self.vertical(detail)), dim=1))


class LineTokenDetailBridge(nn.Module):
    """Fuse cross-scale decoder detail with row/column line tokens before logits."""

    def __init__(self, channels: int) -> None:
        super().__init__()
        self.cross_scale = nn.Sequential(ConvNormAct(channels * 4, channels), ResidualBlock(channels, channels))
        self.strip_context = LocalStripContext(channels)
        self.token_project = nn.Sequential(ConvNormAct(channels * 3, channels), ResidualBlock(channels, channels))
        self.detail_project = nn.Sequential(ConvNormAct(channels * 2, channels), ResidualBlock(channels, channels))
        self.agreement = nn.Sequential(ConvNormAct(channels * 3, channels), nn.Conv2d(channels, 1, 1))
        self.output_refine = nn.Sequential(ConvNormAct(channels * 4, channels), ResidualBlock(channels, channels))

    def forward(self, dec0: Tensor, detail: Tensor, dec1_full: Tensor, dec2_full: Tensor) -> tuple[Tensor, Tensor, Tensor]:
        fused = self.cross_scale(torch.cat((dec0, detail, dec1_full, dec2_full), dim=1))
        row_token = fused.mean(dim=3, keepdim=True).expand_as(fused)
        col_token = fused.mean(dim=2, keepdim=True).expand_as(fused)
        line_tokens = self.token_project(torch.cat((self.strip_context(fused), row_token, col_token), dim=1))
        signed_detail = detail - _smooth(detail, 15)
        detail_support = self.detail_project(torch.cat((detail, signed_detail), dim=1))
        agree = torch.sigmoid(self.agreement(torch.cat((fused, line_tokens, detail_support), dim=1)))
        refined = self.output_refine(torch.cat((fused, agree * line_tokens, agree * detail_support, line_tokens * detail_support), dim=1))
        return refined, line_tokens, detail_support


class BoundedAgreementHead(nn.Module):
    """Convert region/detail/line evidence to trusted logits without thresholds."""

    def __init__(self, channels: int) -> None:
        super().__init__()
        self.region_refine = nn.Sequential(ConvNormAct(channels, channels), ResidualBlock(channels, channels))
        self.support_refine = nn.Sequential(ConvNormAct(channels * 3, channels), ResidualBlock(channels, channels))
        self.region_head = nn.Conv2d(channels, 1, 1)
        self.delta_head = nn.Conv2d(channels, 1, 1)
        self.delta_gate = nn.Sequential(ConvNormAct(channels * 3, channels), nn.Conv2d(channels, 1, 1))
        self.line_head = nn.Conv2d(channels, 1, 1)
        self.centerline_head = nn.Conv2d(channels, 1, 1)

    def forward(self, features: Tensor, line_tokens: Tensor, detail_support: Tensor) -> dict[str, Tensor]:
        region = self.region_refine(features)
        support = self.support_refine(torch.cat((features, line_tokens, detail_support), dim=1))
        region_logits = self.region_head(region)
        delta = 1.1 * torch.tanh(self.delta_head(support))
        gate = torch.sigmoid(self.delta_gate(torch.cat((region, line_tokens, detail_support), dim=1)))
        return {
            "mask_logits": region_logits + gate * delta,
            "line_logits": self.line_head(line_tokens),
            "centerline_logits": self.centerline_head(support),
        }


class FullSpectralBTDSZALineTokenDetailUNet(nn.Module):
    def __init__(self) -> None:
        super().__init__()
        self.front_end = NormalizedBTDSZAFrontEnd(learned_channels=16)
        base = 36
        self.stem = SignedDetailStem(self.front_end.out_channels, base)
        self.enc0 = ResidualBlock(base, base)
        self.enc1 = EncoderDown(base, base * 2)
        self.enc2 = EncoderDown(base * 2, base * 4)
        self.enc3 = EncoderDown(base * 4, base * 8)
        self.context = ASPPContext(base * 8, base * 8)
        self.up2 = DecoderFuse(base * 8, base * 4, base * 4)
        self.up1 = DecoderFuse(base * 4, base * 2, base * 2)
        self.up0 = DecoderFuse(base * 2, base, base)
        self.highres_detail = SignedDetailStem(self.front_end.out_channels, base)
        self.dec1_project = ConvNormAct(base * 2, base, kernel_size=1)
        self.dec2_project = ConvNormAct(base * 4, base, kernel_size=1)
        self.bridge = LineTokenDetailBridge(base)
        self.head = BoundedAgreementHead(base)

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
        dec1_full = F.interpolate(self.dec1_project(dec1), size=dec0.shape[-2:], mode="bilinear", align_corners=False)
        dec2_full = F.interpolate(self.dec2_project(dec2), size=dec0.shape[-2:], mode="bilinear", align_corners=False)
        refined, line_tokens, detail_support = self.bridge(dec0, detail, dec1_full, dec2_full)
        return self.head(refined, line_tokens, detail_support)


def _validate_auxiliary_outputs(output_spec: dict[str, object]) -> None:
    expected = [
        {"target": "line", "name": "line_logits", "shape": [1, 256, 256]},
        {"target": "centerline", "name": "centerline_logits", "shape": [1, 256, 256]},
    ]
    if output_spec.get("auxiliary_outputs") != expected:
        raise ValueError(f"{CANDIDATE_ID} requires trusted line_logits and centerline_logits auxiliary outputs")


def build_model(input_spec: dict[str, object], output_spec: dict[str, object]) -> nn.Module:
    """Build the model for the Harness-supplied ABI contract."""

    if input_spec.get("mode") != "abi_16ch_plus_sza" or input_spec.get("shape") != [17, 256, 256]:
        raise ValueError(f"{CANDIDATE_ID} requires abi_16ch_plus_sza [17, 256, 256] input")
    if output_spec.get("form") != "mask_logits" or output_spec.get("shape") != [1, 256, 256]:
        raise ValueError(f"{CANDIDATE_ID} requires mask_logits [1, 256, 256] primary output")
    _validate_auxiliary_outputs(output_spec)
    return FullSpectralBTDSZALineTokenDetailUNet()
