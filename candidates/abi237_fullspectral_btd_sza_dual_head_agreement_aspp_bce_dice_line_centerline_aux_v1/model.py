"""Full-spectral BTD+SZA ASPP U-Net with internal dual-head agreement fusion."""

from __future__ import annotations

import torch
import torch.nn.functional as F
from torch import Tensor, nn


CANDIDATE_ID = "abi237_fullspectral_btd_sza_dual_head_agreement_aspp_bce_dice_line_centerline_aux_v1"


class NormalizedBTDSZAFrontEnd(nn.Module):
    """Build normalized ABI, brightness-temperature-difference, SZA, and learned features."""

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
    for groups in (8, 6, 5, 4, 3, 2, 1):
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
        self.conv2 = nn.Sequential(nn.Conv2d(out_channels, out_channels, 3, padding=1, bias=False), nn.GroupNorm(_group_count(out_channels), out_channels))
        self.skip = nn.Identity() if in_channels == out_channels else nn.Conv2d(in_channels, out_channels, 1, bias=False)
        self.act = nn.GELU()

    def forward(self, inputs: Tensor) -> Tensor:
        return self.act(self.conv2(self.conv1(inputs)) + self.skip(inputs))


class SignedDetailContextStem(nn.Module):
    """Project local detail and broad context without candidate-owned filtering."""

    def __init__(self, in_channels: int, out_channels: int) -> None:
        super().__init__()
        self.raw = ConvNormAct(in_channels, out_channels, kernel_size=1)
        self.local_pos = ConvNormAct(in_channels, out_channels, kernel_size=1)
        self.local_neg = ConvNormAct(in_channels, out_channels, kernel_size=1)
        self.mid_pos = ConvNormAct(in_channels, out_channels, kernel_size=1)
        self.context = ConvNormAct(in_channels, out_channels, kernel_size=1)
        self.fuse = nn.Sequential(ConvNormAct(out_channels * 5, out_channels), ResidualBlock(out_channels, out_channels))

    def forward(self, inputs: Tensor) -> Tensor:
        local_detail = inputs - _smooth(inputs, 7)
        mid_detail = inputs - _smooth(inputs, 15)
        broad = _smooth(inputs, 31)
        return self.fuse(torch.cat((self.raw(inputs), self.local_pos(F.relu(local_detail)), self.local_neg(F.relu(-local_detail)), self.mid_pos(F.relu(mid_detail)), self.context(broad)), dim=1))


class EncoderDown(nn.Module):
    def __init__(self, in_channels: int, out_channels: int) -> None:
        super().__init__()
        self.block = nn.Sequential(nn.MaxPool2d(2), ResidualBlock(in_channels, out_channels), ResidualBlock(out_channels, out_channels))

    def forward(self, inputs: Tensor) -> Tensor:
        return self.block(inputs)


class ASPPContext(nn.Module):
    def __init__(self, in_channels: int, out_channels: int) -> None:
        super().__init__()
        branch = out_channels // 2
        self.branch1 = ConvNormAct(in_channels, branch, kernel_size=1)
        self.branch2 = ConvNormAct(in_channels, branch, dilation=2)
        self.branch4 = ConvNormAct(in_channels, branch, dilation=4)
        self.branch8 = ConvNormAct(in_channels, branch, dilation=8)
        self.image_pool = nn.Sequential(nn.AdaptiveAvgPool2d(1), ConvNormAct(in_channels, branch, kernel_size=1))
        self.project = nn.Sequential(ConvNormAct(branch * 5, out_channels, kernel_size=1), ResidualBlock(out_channels, out_channels))

    def forward(self, inputs: Tensor) -> Tensor:
        pooled = F.interpolate(self.image_pool(inputs), size=inputs.shape[-2:], mode="bilinear", align_corners=False)
        return self.project(torch.cat((self.branch1(inputs), self.branch2(inputs), self.branch4(inputs), self.branch8(inputs), pooled), dim=1))


class DecoderFuse(nn.Module):
    def __init__(self, in_channels: int, skip_channels: int, out_channels: int) -> None:
        super().__init__()
        self.input_project = ConvNormAct(in_channels, out_channels, kernel_size=1)
        self.skip_project = ConvNormAct(skip_channels, out_channels, kernel_size=1)
        self.fuse = nn.Sequential(ConvNormAct(out_channels * 2, out_channels), ResidualBlock(out_channels, out_channels))

    def forward(self, inputs: Tensor, skip: Tensor) -> Tensor:
        upsampled = F.interpolate(inputs, size=skip.shape[-2:], mode="bilinear", align_corners=False)
        return self.fuse(torch.cat((self.input_project(upsampled), self.skip_project(skip)), dim=1))


class FullScaleFusion(nn.Module):
    def __init__(self, base_channels: int) -> None:
        super().__init__()
        branch = 16
        self.projects = nn.ModuleList([
            ConvNormAct(base_channels, branch, kernel_size=1), ConvNormAct(base_channels, branch, kernel_size=1),
            ConvNormAct(base_channels * 2, branch, kernel_size=1), ConvNormAct(base_channels * 4, branch, kernel_size=1),
            ConvNormAct(base_channels * 8, branch, kernel_size=1), ConvNormAct(base_channels * 8, branch, kernel_size=1),
            ConvNormAct(base_channels * 4, branch, kernel_size=1), ConvNormAct(base_channels * 2, branch, kernel_size=1),
            ConvNormAct(base_channels, branch, kernel_size=1), ConvNormAct(base_channels, branch, kernel_size=1),
        ])
        self.fuse = nn.Sequential(ConvNormAct(branch * 10, base_channels), ResidualBlock(base_channels, base_channels))

    @staticmethod
    def _resize(inputs: Tensor, size: tuple[int, int]) -> Tensor:
        return inputs if inputs.shape[-2:] == size else F.interpolate(inputs, size=size, mode="bilinear", align_corners=False)

    def forward(self, tensors: tuple[Tensor, ...]) -> Tensor:
        size = tensors[-2].shape[-2:]
        projected = [project(self._resize(tensor, size)) for project, tensor in zip(self.projects, tensors)]
        return self.fuse(torch.cat(projected, dim=1))


class LineAwareRefinement(nn.Module):
    def __init__(self, channels: int) -> None:
        super().__init__()
        self.detail = ConvNormAct(channels, channels)
        self.horizontal = nn.Sequential(nn.Conv2d(channels, channels, kernel_size=(1, 15), padding=(0, 7), bias=False), nn.GroupNorm(_group_count(channels), channels), nn.GELU())
        self.vertical = nn.Sequential(nn.Conv2d(channels, channels, kernel_size=(15, 1), padding=(7, 0), bias=False), nn.GroupNorm(_group_count(channels), channels), nn.GELU())
        self.project = nn.Sequential(ConvNormAct(channels * 4, channels), ResidualBlock(channels, channels))

    def forward(self, inputs: Tensor) -> Tensor:
        detail = self.detail(inputs - _smooth(inputs, 7))
        return self.project(torch.cat((inputs, detail, self.horizontal(inputs), self.vertical(inputs)), dim=1))


class DualHeadAgreementFusion(nn.Module):
    """Fuse recall-oriented and precision-oriented features without thresholding."""

    def __init__(self, channels: int) -> None:
        super().__init__()
        self.recall_branch = nn.Sequential(ConvNormAct(channels * 4, channels), ResidualBlock(channels, channels))
        self.precision_branch = LineAwareRefinement(channels)
        self.agreement_gate = nn.Sequential(ConvNormAct(channels * 4, channels, kernel_size=1), nn.Conv2d(channels, channels, 1), nn.Sigmoid())
        self.fused_project = nn.Sequential(ConvNormAct(channels * 4, channels), ResidualBlock(channels, channels))
        self.mask_head = nn.Conv2d(channels, 1, 1)
        self.recall_logit = nn.Conv2d(channels, 1, 1)
        self.precision_logit = nn.Conv2d(channels, 1, 1)
        self.line_head = nn.Conv2d(channels, 1, 1)
        self.centerline_head = nn.Conv2d(channels, 1, 1)

    def forward(self, decoder: Tensor, detail: Tensor, stem: Tensor, fullscale: Tensor) -> dict[str, Tensor]:
        recall = self.recall_branch(torch.cat((decoder, detail, stem, fullscale), dim=1))
        precision = self.precision_branch(fullscale)
        difference = torch.abs(recall - precision)
        agreement = self.agreement_gate(torch.cat((recall, precision, difference, detail), dim=1))
        fused = agreement * (0.5 * (recall + precision)) + (1.0 - agreement) * recall
        refined = self.fused_project(torch.cat((fused, recall, precision, fullscale), dim=1))
        mask_logits = self.mask_head(refined) + 0.15 * self.recall_logit(recall) + 0.10 * self.precision_logit(precision)
        return {"mask_logits": mask_logits, "line_logits": self.line_head(precision), "centerline_logits": self.centerline_head(refined)}


class FullSpectralBTDSZADualHeadAgreementASPP(nn.Module):
    def __init__(self) -> None:
        super().__init__()
        self.front_end = NormalizedBTDSZAFrontEnd(learned_channels=16)
        base = 36
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
        self.fullscale = FullScaleFusion(base)
        self.decoder_project = nn.Sequential(ConvNormAct(base * 4, base), ResidualBlock(base, base))
        self.agreement_head = DualHeadAgreementFusion(base)

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
        fullscale = self.fullscale((stem, enc0, enc1, enc2, enc3, context, dec2, dec1, dec0, detail))
        decoder = self.decoder_project(torch.cat((dec0, detail, stem, fullscale), dim=1))
        return self.agreement_head(decoder, detail, stem, fullscale)


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
    return FullSpectralBTDSZADualHeadAgreementASPP()
