"""Compact spectral/SZA-regime MoE with decoder-integrated line memory for ABI contrails."""

from __future__ import annotations

import torch
import torch.nn.functional as F
from torch import Tensor, nn


CANDIDATE_ID = "abi301_fullspectral_btd_sza_compact_moe_decoder_line_memory_unet_bce_dice_line_centerline_aux_v1"


def _group_count(channels: int) -> int:
    for groups in (8, 6, 5, 4, 3, 2, 1):
        if channels % groups == 0:
            return groups
    return 1


def _bounded(inputs: Tensor, *, limit: float = 12.0) -> Tensor:
    return torch.clamp(torch.nan_to_num(inputs, nan=0.0, posinf=limit, neginf=-limit), -limit, limit)


def _smooth(inputs: Tensor, kernel_size: int) -> Tensor:
    return F.avg_pool2d(inputs, kernel_size=kernel_size, stride=1, padding=kernel_size // 2, count_include_pad=False)


class ABIBTDSZAFrontEnd(nn.Module):
    """Normalize provider-approved ABI+SZA and append approved-channel BTDs."""

    _ABI_MEANS = (
        0.1572, 0.1281, 0.1566, 0.0268, 0.0883, 0.0753,
        279.45, 233.17, 241.06, 248.44, 267.58, 250.28, 269.32, 268.23, 265.94, 255.61,
    )
    _ABI_SCALES = (
        0.36, 0.34, 0.36, 0.16, 0.23, 0.18,
        42.0, 20.0, 25.0, 29.0, 43.0, 28.0, 44.0, 44.0, 43.0, 35.0,
    )
    _BTD_PAIRS = ((12, 13), (13, 14), (12, 14), (10, 13), (6, 13), (7, 9), (7, 12), (8, 13))
    _BTD_SCALE = 20.0

    def __init__(self, learned_channels: int = 8) -> None:
        super().__init__()
        self.register_buffer("abi_means", torch.tensor(self._ABI_MEANS, dtype=torch.float32).view(1, 16, 1, 1))
        self.register_buffer("abi_scales", torch.tensor(self._ABI_SCALES, dtype=torch.float32).view(1, 16, 1, 1))
        self.learned_mixer = nn.Sequential(nn.Conv2d(17, learned_channels, kernel_size=1), nn.GELU())
        self.out_channels = 16 + len(self._BTD_PAIRS) + 2 + learned_channels

    def forward(self, inputs: Tensor) -> Tensor:
        if inputs.ndim != 4 or inputs.shape[1] != 17:
            raise ValueError(f"expected [N, 17, H, W] ABI+SZA tensor, got {tuple(inputs.shape)}")
        abi = inputs[:, :16]
        sza = torch.nan_to_num(inputs[:, 16:17], nan=90.0, posinf=180.0, neginf=0.0).clamp(0.0, 180.0)
        normalized = _bounded((abi - self.abi_means) / self.abi_scales, limit=6.0)
        btd = _bounded(
            torch.cat([(abi[:, a:a + 1] - abi[:, b:b + 1]) / self._BTD_SCALE for a, b in self._BTD_PAIRS], dim=1),
            limit=6.0,
        )
        sza_scaled = (sza - 90.0) / 90.0
        sza_cosine = torch.cos(torch.deg2rad(sza))
        learned = _bounded(self.learned_mixer(torch.cat((normalized, sza_scaled), dim=1)), limit=6.0)
        return torch.cat((normalized, btd, sza_scaled, sza_cosine, learned), dim=1)


class ConvNormAct(nn.Module):
    def __init__(self, in_channels: int, out_channels: int, *, kernel_size: int = 3, stride: int = 1, dilation: int = 1) -> None:
        super().__init__()
        padding = dilation * (kernel_size // 2)
        self.block = nn.Sequential(
            nn.Conv2d(in_channels, out_channels, kernel_size=kernel_size, stride=stride, padding=padding, dilation=dilation, bias=False),
            nn.GroupNorm(_group_count(out_channels), out_channels),
            nn.GELU(),
        )

    def forward(self, inputs: Tensor) -> Tensor:
        return _bounded(self.block(inputs))


class ResidualBlock(nn.Module):
    def __init__(self, in_channels: int, out_channels: int, *, dilation: int = 1) -> None:
        super().__init__()
        self.conv1 = ConvNormAct(in_channels, out_channels, dilation=dilation)
        self.conv2 = nn.Sequential(
            nn.Conv2d(out_channels, out_channels, kernel_size=3, padding=1, bias=False),
            nn.GroupNorm(_group_count(out_channels), out_channels),
        )
        self.skip = nn.Identity() if in_channels == out_channels else nn.Conv2d(in_channels, out_channels, kernel_size=1, bias=False)
        self.act = nn.GELU()

    def forward(self, inputs: Tensor) -> Tensor:
        return _bounded(self.act(self.conv2(self.conv1(inputs)) + self.skip(inputs)))


class DetailStem(nn.Module):
    """Cheap high-resolution signed-detail evidence from approved features."""

    def __init__(self, in_channels: int, out_channels: int) -> None:
        super().__init__()
        self.raw = ConvNormAct(in_channels, out_channels, kernel_size=1)
        self.detail = ConvNormAct(in_channels * 2, out_channels, kernel_size=1)
        self.project = ResidualBlock(out_channels * 2, out_channels)

    def forward(self, features: Tensor) -> Tensor:
        detail = features - _smooth(features, 7)
        signed = torch.cat((F.relu(detail), F.relu(-detail)), dim=1)
        return self.project(torch.cat((self.raw(features), self.detail(signed)), dim=1))


class DepthwiseExpert(nn.Module):
    """One bounded lightweight expert used inside compact regime MoE blocks."""

    def __init__(self, channels: int, *, mode: str) -> None:
        super().__init__()
        hidden = max(channels // 2, 8)
        if mode == "local":
            self.block = nn.Sequential(
                ConvNormAct(channels, hidden, kernel_size=1),
                nn.Conv2d(hidden, hidden, kernel_size=3, padding=1, groups=hidden, bias=False),
                nn.Conv2d(hidden, channels, kernel_size=1, bias=False),
                nn.GroupNorm(_group_count(channels), channels),
                nn.GELU(),
            )
        elif mode == "dilated":
            self.block = nn.Sequential(
                ConvNormAct(channels, hidden, kernel_size=1),
                nn.Conv2d(hidden, hidden, kernel_size=3, padding=2, dilation=2, groups=hidden, bias=False),
                nn.Conv2d(hidden, channels, kernel_size=1, bias=False),
                nn.GroupNorm(_group_count(channels), channels),
                nn.GELU(),
            )
        elif mode == "line":
            self.block = nn.Sequential(
                ConvNormAct(channels, hidden, kernel_size=1),
                nn.Conv2d(hidden, hidden, kernel_size=(1, 9), padding=(0, 4), groups=hidden, bias=False),
                nn.Conv2d(hidden, hidden, kernel_size=(9, 1), padding=(4, 0), groups=hidden, bias=False),
                nn.Conv2d(hidden, channels, kernel_size=1, bias=False),
                nn.GroupNorm(_group_count(channels), channels),
                nn.GELU(),
            )
        else:
            raise ValueError(f"unknown expert mode {mode!r}")

    def forward(self, inputs: Tensor) -> Tensor:
        return _bounded(self.block(inputs))


class CompactRegimeMoEBlock(nn.Module):
    """Softly gate compact local/context/line experts from approved features."""

    def __init__(self, channels: int) -> None:
        super().__init__()
        gate_channels = max(channels // 4, 8)
        self.gate = nn.Sequential(
            nn.GroupNorm(_group_count(channels), channels),
            nn.Conv2d(channels, gate_channels, kernel_size=1),
            nn.GELU(),
            nn.Conv2d(gate_channels, 3, kernel_size=1),
        )
        self.experts = nn.ModuleList(
            (DepthwiseExpert(channels, mode="local"), DepthwiseExpert(channels, mode="dilated"), DepthwiseExpert(channels, mode="line"))
        )
        self.project = nn.Sequential(ConvNormAct(channels * 2, channels, kernel_size=1), ResidualBlock(channels, channels))
        self.scale = nn.Parameter(torch.tensor(0.15))

    def forward(self, inputs: Tensor) -> Tensor:
        weights = torch.softmax(self.gate(inputs), dim=1)
        expert_outputs = torch.stack([expert(inputs) for expert in self.experts], dim=1)
        mixed = (expert_outputs * weights.unsqueeze(2)).sum(dim=1)
        fused = self.project(torch.cat((inputs, mixed), dim=1))
        return _bounded(inputs + torch.tanh(self.scale) * fused)


class EncoderStage(nn.Module):
    def __init__(self, in_channels: int, out_channels: int) -> None:
        super().__init__()
        self.block = nn.Sequential(
            ConvNormAct(in_channels, out_channels, stride=2),
            ResidualBlock(out_channels, out_channels),
            CompactRegimeMoEBlock(out_channels),
        )

    def forward(self, inputs: Tensor) -> Tensor:
        return self.block(inputs)


class DirectionalLineMemoryBlock(nn.Module):
    """Architecture-internal multi-orientation line memory.

    This block is used inside decoder stages, before final logits are formed, so
    line continuity can shape region evidence rather than being appended as a
    conservative post-decoder head. It is differentiable model logic over
    provider-approved features, not postprocessing or threshold selection.
    """

    def __init__(self, channels: int) -> None:
        super().__init__()
        self.branches = nn.ModuleList((
            self._branch(channels, kernel_size=(1, 11), padding=(0, 5)),
            self._branch(channels, kernel_size=(11, 1), padding=(5, 0)),
            self._branch(channels, kernel_size=(7, 7), padding=(3, 3)),
            self._branch(channels, kernel_size=(5, 5), padding=(4, 4), dilation=(2, 2)),
        ))
        self.branch_logits = nn.ModuleList(nn.Conv2d(channels, 1, kernel_size=1) for _ in range(4))
        self.project = nn.Sequential(ConvNormAct(channels * 4, channels, kernel_size=1), ResidualBlock(channels, channels))
        self.agreement_project = ConvNormAct(1, channels, kernel_size=1)
        self.gate = nn.Sequential(
            ConvNormAct(channels * 3, channels, kernel_size=1),
            nn.Conv2d(channels, channels, kernel_size=1),
            nn.Sigmoid(),
        )
        self.scale = nn.Parameter(torch.tensor(0.12))

    @staticmethod
    def _branch(
        channels: int,
        *,
        kernel_size: tuple[int, int],
        padding: tuple[int, int],
        dilation: tuple[int, int] = (1, 1),
    ) -> nn.Module:
        return nn.Sequential(
            ConvNormAct(channels, channels, kernel_size=1),
            nn.Conv2d(channels, channels, kernel_size=kernel_size, padding=padding, dilation=dilation, groups=channels, bias=False),
            nn.Conv2d(channels, channels, kernel_size=1, bias=False),
            nn.GroupNorm(_group_count(channels), channels),
            nn.GELU(),
        )

    def forward(self, inputs: Tensor) -> Tensor:
        directional = [_bounded(branch(inputs)) for branch in self.branches]
        fused = self.project(torch.cat(directional, dim=1))
        logits = torch.cat([head(branch) for head, branch in zip(self.branch_logits, directional)], dim=1)
        mean_logits = logits.mean(dim=1, keepdim=True)
        disagreement = torch.mean(torch.abs(logits - mean_logits), dim=1, keepdim=True)
        agreement = 1.0 - torch.tanh(disagreement)
        agreement_features = self.agreement_project(agreement)
        gate = self.gate(torch.cat((inputs, fused, agreement_features), dim=1))
        memory = gate * fused + 0.20 * agreement_features
        return _bounded(inputs + torch.tanh(self.scale) * memory)


class EncoderStage(nn.Module):
    def __init__(self, in_channels: int, out_channels: int) -> None:
        super().__init__()
        self.block = nn.Sequential(
            ConvNormAct(in_channels, out_channels, stride=2),
            ResidualBlock(out_channels, out_channels),
            CompactRegimeMoEBlock(out_channels),
        )

    def forward(self, inputs: Tensor) -> Tensor:
        return self.block(inputs)


class DecoderStage(nn.Module):
    def __init__(self, in_channels: int, skip_channels: int, out_channels: int, *, use_moe: bool, use_line_memory: bool) -> None:
        super().__init__()
        self.skip_project = ConvNormAct(skip_channels, out_channels, kernel_size=1)
        layers: list[nn.Module] = [ConvNormAct(in_channels + out_channels, out_channels), ResidualBlock(out_channels, out_channels)]
        if use_moe:
            layers.append(CompactRegimeMoEBlock(out_channels))
        if use_line_memory:
            layers.append(DirectionalLineMemoryBlock(out_channels))
        self.fuse = nn.Sequential(*layers)

    def forward(self, inputs: Tensor, skip: Tensor) -> Tensor:
        upsampled = F.interpolate(inputs, size=skip.shape[-2:], mode="bilinear", align_corners=False)
        return self.fuse(torch.cat((upsampled, self.skip_project(skip)), dim=1))


class DecoderLineMemoryHead(nn.Module):
    """Final logits from decoder-integrated line-memory features."""

    def __init__(self, channels: int) -> None:
        super().__init__()
        self.pre_context = ResidualBlock(channels, channels)
        self.line_memory = DirectionalLineMemoryBlock(channels)
        self.detail_context = ResidualBlock(channels, channels)
        self.fuse = nn.Sequential(ConvNormAct(channels * 3, channels), ResidualBlock(channels, channels))
        self.mask_head = nn.Conv2d(channels, 1, kernel_size=1)
        self.line_head = nn.Conv2d(channels, 1, kernel_size=1)
        self.centerline_head = nn.Conv2d(channels, 1, kernel_size=1)

    def forward(self, features: Tensor) -> dict[str, Tensor]:
        local = self.pre_context(features)
        line_features = self.line_memory(local)
        detail = self.detail_context(features - _smooth(features, 5))
        fused = self.fuse(torch.cat((local, line_features, detail), dim=1))
        line_logits = self.line_head(line_features)
        centerline_logits = self.centerline_head(fused)
        mask_logits = self.mask_head(fused) + 0.04 * torch.tanh(line_logits) + 0.02 * torch.tanh(centerline_logits)
        return {"mask_logits": mask_logits, "line_logits": line_logits, "centerline_logits": centerline_logits}


class CompactMoEDecoderLineMemoryUNet(nn.Module):
    """Resource-aware ABI+SZA compact MoE U-Net with decoder-integrated line memory."""

    def __init__(self) -> None:
        super().__init__()
        self.front_end = ABIBTDSZAFrontEnd(learned_channels=8)
        base = 24
        self.stem = nn.Sequential(ConvNormAct(self.front_end.out_channels, base), ResidualBlock(base, base))
        self.detail = DetailStem(self.front_end.out_channels, base)
        self.enc1 = EncoderStage(base, 32)
        self.enc2 = EncoderStage(32, 56)
        self.enc3 = EncoderStage(56, 88)
        self.bottleneck = nn.Sequential(ResidualBlock(88, 104), CompactRegimeMoEBlock(104), ResidualBlock(104, 104, dilation=2))
        self.up2 = DecoderStage(104, 56, 64, use_moe=True, use_line_memory=True)
        self.up1 = DecoderStage(64, 32, 40, use_moe=False, use_line_memory=True)
        self.up0 = DecoderStage(40, base, 32, use_moe=False, use_line_memory=True)
        self.final_fuse = nn.Sequential(ConvNormAct(32 + base + base, 32), ResidualBlock(32, 32), DirectionalLineMemoryBlock(32), ResidualBlock(32, 32))
        self.head = DecoderLineMemoryHead(32)

    def forward(self, inputs: Tensor) -> dict[str, Tensor]:
        features = self.front_end(inputs)
        stem = self.stem(features)
        detail = self.detail(features)
        enc1 = self.enc1(stem)
        enc2 = self.enc2(enc1)
        enc3 = self.enc3(enc2)
        bottleneck = self.bottleneck(enc3)
        dec2 = self.up2(bottleneck, enc2)
        dec1 = self.up1(dec2, enc1)
        dec0 = self.up0(dec1, stem)
        fused = self.final_fuse(torch.cat((dec0, stem, detail), dim=1))
        return self.head(fused)


def _validate_auxiliary_outputs(output_spec: dict[str, object]) -> None:
    expected = [
        {"target": "line", "name": "line_logits", "shape": [1, 256, 256]},
        {"target": "centerline", "name": "centerline_logits", "shape": [1, 256, 256]},
    ]
    if output_spec.get("auxiliary_outputs") != expected:
        raise ValueError(f"{CANDIDATE_ID} requires trusted line_logits and centerline_logits auxiliary outputs")


def build_model(input_spec: dict[str, object], output_spec: dict[str, object]) -> nn.Module:
    """Build the model for the Harness-supplied ABI+SZA contract."""

    if input_spec.get("mode") != "abi_16ch_plus_sza" or input_spec.get("shape") != [17, 256, 256]:
        raise ValueError(f"{CANDIDATE_ID} requires abi_16ch_plus_sza [17, 256, 256] input")
    if input_spec.get("source_channel_indices") not in (None, list(range(16)) + [18]):
        raise ValueError(f"{CANDIDATE_ID} received an unexpected source-channel contract")
    if output_spec.get("form") != "mask_logits" or output_spec.get("shape") != [1, 256, 256]:
        raise ValueError(f"{CANDIDATE_ID} requires mask_logits [1, 256, 256] primary output")
    _validate_auxiliary_outputs(output_spec)
    return CompactMoEDecoderLineMemoryUNet()
