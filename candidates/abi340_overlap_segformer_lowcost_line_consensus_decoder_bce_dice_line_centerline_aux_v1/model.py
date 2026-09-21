"""Low-cost overlap SegFormer line-consensus decoder for ABI+SZA contrail segmentation."""

from __future__ import annotations

import math

import torch
import torch.nn.functional as F
from torch import Tensor, nn


CANDIDATE_ID = "abi340_overlap_segformer_lowcost_line_consensus_decoder_bce_dice_line_centerline_aux_v1"


def _group_count(channels: int) -> int:
    for groups in (8, 6, 5, 4, 3, 2, 1):
        if channels % groups == 0:
            return groups
    return 1


def _finite_feature(inputs: Tensor, *, limit: float, nan: float = 0.0) -> Tensor:
    """Map non-finite candidate-visible feature values to bounded neutral values."""

    return torch.nan_to_num(inputs, nan=nan, posinf=limit, neginf=-limit).clamp(-limit, limit)


def _bounded(inputs: Tensor, *, limit: float = 12.0) -> Tensor:
    """Bound activations while leaving parameter non-finiteness visible to the Harness."""

    return torch.clamp(inputs, min=-limit, max=limit)


def _smooth(inputs: Tensor, kernel_size: int) -> Tensor:
    return F.avg_pool2d(inputs, kernel_size=kernel_size, stride=1, padding=kernel_size // 2, count_include_pad=False)


class ABIBTDSZAFrontEnd(nn.Module):
    """Build finite normalized ABI, ABI-channel BTD, SZA, and learned channel features."""

    _ABI_MEANS = (
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
    _ABI_SCALES = (
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

    def __init__(self, learned_channels: int = 12) -> None:
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
        normalized = _finite_feature((abi - self.abi_means) / self.abi_scales, limit=6.0)
        btd = _finite_feature(
            torch.cat([(abi[:, a : a + 1] - abi[:, b : b + 1]) / self._BTD_SCALE for a, b in self._BTD_PAIRS], dim=1),
            limit=6.0,
        )
        sza_scaled = (sza - 90.0) / 90.0
        sza_cosine = torch.cos(torch.deg2rad(sza))
        learned = _bounded(self.learned_mixer(torch.cat((normalized, sza_scaled), dim=1)))
        return torch.cat((normalized, btd, sza_scaled, sza_cosine, learned), dim=1)


class ConvNormAct(nn.Module):
    """Convolution, GroupNorm, GELU, and bounded activation."""

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
    """Small residual convolution block for local detail."""

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


class SignedDetailBridge(nn.Module):
    """High-resolution signed-detail evidence path for thin contrail edges."""

    def __init__(self, in_channels: int, out_channels: int) -> None:
        super().__init__()
        self.raw = ConvNormAct(in_channels, out_channels, kernel_size=1)
        self.local_pos = ConvNormAct(in_channels, out_channels, kernel_size=1)
        self.local_neg = ConvNormAct(in_channels, out_channels, kernel_size=1)
        self.mid_pos = ConvNormAct(in_channels, out_channels, kernel_size=1)
        self.mid_neg = ConvNormAct(in_channels, out_channels, kernel_size=1)
        self.project = nn.Sequential(ConvNormAct(out_channels * 5, out_channels), ResidualBlock(out_channels, out_channels))

    def forward(self, features: Tensor) -> Tensor:
        local = features - _smooth(features, 7)
        mid = features - _smooth(features, 15)
        return self.project(
            torch.cat(
                (
                    self.raw(features),
                    self.local_pos(F.relu(local)),
                    self.local_neg(F.relu(-local)),
                    self.mid_pos(F.relu(mid)),
                    self.mid_neg(F.relu(-mid)),
                ),
                dim=1,
            )
        )


class OverlapPatchEmbed(nn.Module):
    """SegFormer-like overlapped patch embedding using only convolutional model logic."""

    def __init__(self, in_channels: int, out_channels: int, *, kernel_size: int, stride: int) -> None:
        super().__init__()
        self.proj = nn.Conv2d(in_channels, out_channels, kernel_size=kernel_size, stride=stride, padding=kernel_size // 2, bias=False)
        self.norm = nn.GroupNorm(_group_count(out_channels), out_channels)
        self.act = nn.GELU()

    def forward(self, inputs: Tensor) -> Tensor:
        return _bounded(self.act(self.norm(self.proj(inputs))))


class EfficientSelfAttention(nn.Module):
    """Spatial-reduction self-attention over provider-approved feature tensors."""

    def __init__(self, channels: int, *, num_heads: int, sr_ratio: int) -> None:
        super().__init__()
        if channels % num_heads != 0:
            raise ValueError(f"channels={channels} must be divisible by num_heads={num_heads}")
        self.channels = channels
        self.num_heads = num_heads
        self.head_dim = channels // num_heads
        self.scale = 1.0 / math.sqrt(float(self.head_dim))
        self.norm = nn.GroupNorm(_group_count(channels), channels)
        self.q = nn.Conv2d(channels, channels, kernel_size=1, bias=False)
        self.kv = nn.Conv2d(channels, channels * 2, kernel_size=1, bias=False)
        self.sr_ratio = sr_ratio
        self.sr = nn.Conv2d(channels, channels, kernel_size=sr_ratio, stride=sr_ratio, groups=channels, bias=False) if sr_ratio > 1 else nn.Identity()
        self.sr_norm = nn.GroupNorm(_group_count(channels), channels)
        self.proj = nn.Conv2d(channels, channels, kernel_size=1, bias=False)
        self.gamma = nn.Parameter(torch.tensor(0.10))

    def forward(self, inputs: Tensor) -> Tensor:
        batch, channels, height, width = inputs.shape
        normed = self.norm(inputs)
        q = self.q(normed).flatten(2).transpose(1, 2).reshape(batch, height * width, self.num_heads, self.head_dim)
        q = q.permute(0, 2, 1, 3)
        reduced = self.sr(normed)
        reduced = self.sr_norm(reduced)
        kv = self.kv(reduced).flatten(2).transpose(1, 2)
        kv = kv.reshape(batch, kv.shape[1], 2, self.num_heads, self.head_dim).permute(2, 0, 3, 1, 4)
        key, value = kv.unbind(0)
        attention = torch.softmax((q @ key.transpose(-2, -1)) * self.scale, dim=-1)
        attended = (attention @ value).transpose(1, 2).reshape(batch, height * width, channels)
        attended = attended.transpose(1, 2).reshape(batch, channels, height, width)
        return _bounded(inputs + torch.tanh(self.gamma) * self.proj(attended))


class MixFeedForward(nn.Module):
    """SegFormer Mix-FFN with depthwise spatial mixing."""

    def __init__(self, channels: int, *, expansion: int = 3) -> None:
        super().__init__()
        hidden = channels * expansion
        self.norm = nn.GroupNorm(_group_count(channels), channels)
        self.expand = nn.Conv2d(channels, hidden, kernel_size=1, bias=False)
        self.depthwise = nn.Conv2d(hidden, hidden, kernel_size=3, padding=1, groups=hidden, bias=False)
        self.project = nn.Conv2d(hidden, channels, kernel_size=1, bias=False)
        self.gamma = nn.Parameter(torch.tensor(0.10))

    def forward(self, inputs: Tensor) -> Tensor:
        hidden = F.gelu(self.expand(self.norm(inputs)))
        hidden = F.gelu(self.depthwise(hidden))
        return _bounded(inputs + torch.tanh(self.gamma) * self.project(hidden))


class SegFormerBlock(nn.Module):
    """Overlap-attention block for compact ABI context modeling."""

    def __init__(self, channels: int, *, num_heads: int, sr_ratio: int) -> None:
        super().__init__()
        self.attn = EfficientSelfAttention(channels, num_heads=num_heads, sr_ratio=sr_ratio)
        self.ffn = MixFeedForward(channels)

    def forward(self, inputs: Tensor) -> Tensor:
        return self.ffn(self.attn(inputs))


class SegFormerStage(nn.Module):
    """Downsample then apply a small number of efficient attention blocks."""

    def __init__(self, in_channels: int, out_channels: int, *, kernel_size: int, stride: int, num_heads: int, sr_ratio: int, depth: int) -> None:
        super().__init__()
        blocks: list[nn.Module] = [OverlapPatchEmbed(in_channels, out_channels, kernel_size=kernel_size, stride=stride)]
        blocks.extend(SegFormerBlock(out_channels, num_heads=num_heads, sr_ratio=sr_ratio) for _ in range(depth))
        self.stage = nn.Sequential(*blocks)

    def forward(self, inputs: Tensor) -> Tensor:
        return self.stage(inputs)


class OrientedLineContext(nn.Module):
    """Learned horizontal/vertical/diagonal context; architecture only, not postprocessing."""

    def __init__(self, channels: int) -> None:
        super().__init__()
        self.horizontal = nn.Sequential(
            nn.Conv2d(channels, channels, kernel_size=(1, 11), padding=(0, 5), groups=channels, bias=False),
            nn.Conv2d(channels, channels, kernel_size=1, bias=False),
            nn.GroupNorm(_group_count(channels), channels),
            nn.GELU(),
        )
        self.vertical = nn.Sequential(
            nn.Conv2d(channels, channels, kernel_size=(11, 1), padding=(5, 0), groups=channels, bias=False),
            nn.Conv2d(channels, channels, kernel_size=1, bias=False),
            nn.GroupNorm(_group_count(channels), channels),
            nn.GELU(),
        )
        self.diag = nn.Sequential(
            nn.Conv2d(channels, channels, kernel_size=3, padding=2, dilation=2, groups=channels, bias=False),
            nn.Conv2d(channels, channels, kernel_size=1, bias=False),
            nn.GroupNorm(_group_count(channels), channels),
            nn.GELU(),
        )
        self.fuse = nn.Sequential(ConvNormAct(channels * 4, channels, kernel_size=1), ResidualBlock(channels, channels))
        self.scale = nn.Parameter(torch.tensor(0.20))

    def forward(self, inputs: Tensor) -> Tensor:
        support = self.fuse(torch.cat((inputs, self.horizontal(inputs), self.vertical(inputs), self.diag(inputs)), dim=1))
        return _bounded(inputs + torch.tanh(self.scale) * support)


class SegFormerLineDecoder(nn.Module):
    """All-MLP-style multi-scale fusion with high-resolution line/detail refinement."""

    def __init__(self, channels: tuple[int, int, int, int], detail_channels: int, out_channels: int = 48) -> None:
        super().__init__()
        c0, c1, c2, c3 = channels
        self.p0 = ConvNormAct(c0, out_channels, kernel_size=1)
        self.p1 = ConvNormAct(c1, out_channels, kernel_size=1)
        self.p2 = ConvNormAct(c2, out_channels, kernel_size=1)
        self.p3 = ConvNormAct(c3, out_channels, kernel_size=1)
        self.fuse128 = nn.Sequential(ConvNormAct(out_channels * 4, out_channels), ResidualBlock(out_channels, out_channels), OrientedLineContext(out_channels))
        self.detail_project = ConvNormAct(detail_channels, out_channels, kernel_size=1)
        self.fuse256 = nn.Sequential(
            ConvNormAct(out_channels * 3, out_channels),
            ResidualBlock(out_channels, out_channels),
            OrientedLineContext(out_channels),
            ResidualBlock(out_channels, out_channels),
        )

    def forward(self, e0: Tensor, e1: Tensor, e2: Tensor, e3: Tensor, stem256: Tensor, detail256: Tensor) -> Tensor:
        target128 = e0.shape[-2:]
        fused128 = self.fuse128(
            torch.cat(
                (
                    self.p0(e0),
                    F.interpolate(self.p1(e1), size=target128, mode="bilinear", align_corners=False),
                    F.interpolate(self.p2(e2), size=target128, mode="bilinear", align_corners=False),
                    F.interpolate(self.p3(e3), size=target128, mode="bilinear", align_corners=False),
                ),
                dim=1,
            )
        )
        fused256 = F.interpolate(fused128, size=stem256.shape[-2:], mode="bilinear", align_corners=False)
        return self.fuse256(torch.cat((fused256, self.detail_project(detail256), self.detail_project(stem256)), dim=1))


class ConnectivityPreservingLineConsensusHead(nn.Module):
    """Low-cost line-consensus logit head for overlap-attention features.

    The head keeps ABI-262s resource-efficient overlap SegFormer encoder and
    replaces broad evidence raising with a compact strip-consensus path. It
    creates separate coverage and line-continuity logits, then adds only bounded
    residual support when high-resolution decoder features, oriented strip
    context, and learned centerline evidence agree. This is architecture logic
    only: no thresholding, morphology, postprocessing, Artifact Filtering, or
    candidate-owned target construction.
    """

    def __init__(self, channels: int) -> None:
        super().__init__()
        self.coverage_path = nn.Sequential(ResidualBlock(channels, channels), ConvNormAct(channels, channels, dilation=2))
        self.line_context = OrientedLineContext(channels)
        self.local_detail = nn.Sequential(
            ConvNormAct(channels, channels, kernel_size=1),
            nn.Conv2d(channels, channels, kernel_size=3, padding=1, groups=channels, bias=False),
            nn.GroupNorm(_group_count(channels), channels),
            nn.GELU(),
        )
        self.consensus_gate = nn.Sequential(
            ConvNormAct(channels * 5, channels, kernel_size=1),
            ResidualBlock(channels, channels),
            nn.Conv2d(channels, channels, kernel_size=1),
            nn.Sigmoid(),
        )
        self.coverage_fuse = nn.Sequential(ConvNormAct(channels * 3, channels), ResidualBlock(channels, channels))
        self.mask_base = nn.Conv2d(channels, 1, kernel_size=1)
        self.coverage_logits = nn.Conv2d(channels, 1, kernel_size=1)
        self.line_logits = nn.Conv2d(channels, 1, kernel_size=1)
        self.centerline_logits = nn.Conv2d(channels, 1, kernel_size=1)

    def forward(self, features: Tensor) -> dict[str, Tensor]:
        coverage = self.coverage_path(features)
        line = self.line_context(features)
        detail = _bounded(self.local_detail(features))
        disagreement = torch.abs(coverage - line)
        gate = self.consensus_gate(torch.cat((features, coverage, line, detail, disagreement), dim=1))
        fused = self.coverage_fuse(torch.cat((features, coverage, gate * line + (1.0 - gate) * detail), dim=1))
        base_logits = self.mask_base(fused)
        coverage_logits = self.coverage_logits(coverage)
        line_logits = self.line_logits(line)
        centerline_logits = self.centerline_logits(gate * line + detail)
        positive_support = torch.tanh(coverage_logits) * torch.sigmoid(line_logits)
        continuity_support = torch.tanh(line_logits) * torch.sigmoid(centerline_logits)
        mask_logits = base_logits + 0.14 * positive_support + 0.10 * continuity_support
        return {
            "mask_logits": mask_logits,
            "line_logits": line_logits,
            "centerline_logits": centerline_logits,
        }


class OverlapSegFormerLineDecoder(nn.Module):
    """Compact SegFormer-like encoder plus line-aware high-resolution decoder."""

    def __init__(self) -> None:
        super().__init__()
        self.front_end = ABIBTDSZAFrontEnd(learned_channels=12)
        base = 32
        self.detail = SignedDetailBridge(self.front_end.out_channels, base)
        self.stem = nn.Sequential(ConvNormAct(self.front_end.out_channels, base), ResidualBlock(base, base))
        self.stage0 = SegFormerStage(base, 32, kernel_size=7, stride=2, num_heads=2, sr_ratio=8, depth=1)
        self.stage1 = SegFormerStage(32, 64, kernel_size=3, stride=2, num_heads=4, sr_ratio=4, depth=1)
        self.stage2 = SegFormerStage(64, 96, kernel_size=3, stride=2, num_heads=4, sr_ratio=2, depth=1)
        self.stage3 = SegFormerStage(96, 160, kernel_size=3, stride=2, num_heads=5, sr_ratio=1, depth=2)
        self.decoder = SegFormerLineDecoder((32, 64, 96, 160), detail_channels=base, out_channels=48)
        self.head = ConnectivityPreservingLineConsensusHead(48)

    def forward(self, inputs: Tensor) -> dict[str, Tensor]:
        features = self.front_end(inputs)
        stem = self.stem(features)
        detail = self.detail(features)
        enc0 = self.stage0(stem)
        enc1 = self.stage1(enc0)
        enc2 = self.stage2(enc1)
        enc3 = self.stage3(enc2)
        decoded = self.decoder(enc0, enc1, enc2, enc3, stem, detail)
        return self.head(decoded)


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
    return OverlapSegFormerLineDecoder()
