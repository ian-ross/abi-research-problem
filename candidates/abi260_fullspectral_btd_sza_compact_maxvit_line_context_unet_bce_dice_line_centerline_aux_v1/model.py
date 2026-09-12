"""Compact MaxViT-style line-context U-Net for full-spectral ABI+SZA inputs."""

from __future__ import annotations

import math

import torch
import torch.nn.functional as F
from torch import Tensor, nn


CANDIDATE_ID = "abi260_fullspectral_btd_sza_compact_maxvit_line_context_unet_bce_dice_line_centerline_aux_v1"


def _finite_feature(inputs: Tensor, *, limit: float, nan: float = 0.0) -> Tensor:
    """Map non-finite candidate-visible feature values to bounded neutral values."""

    return torch.nan_to_num(inputs, nan=nan, posinf=limit, neginf=-limit).clamp(-limit, limit)


def _bounded(inputs: Tensor, *, limit: float = 12.0) -> Tensor:
    """Bound internal activations without hiding non-finite parameter failures."""

    return torch.clamp(inputs, min=-limit, max=limit)


def _group_count(channels: int) -> int:
    for groups in (8, 6, 5, 4, 3, 2, 1):
        if channels % groups == 0:
            return groups
    return 1


def _smooth(inputs: Tensor, kernel_size: int) -> Tensor:
    return F.avg_pool2d(inputs, kernel_size=kernel_size, stride=1, padding=kernel_size // 2, count_include_pad=False)


class SingleFrameFeatureBuilder(nn.Module):
    """Build normalized ABI+SZA, approved-channel BTD, and learned channel features."""

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
    """Convolution, GroupNorm, GELU, and bounded activations."""

    def __init__(self, in_channels: int, out_channels: int, *, kernel_size: int = 3, dilation: int = 1) -> None:
        super().__init__()
        padding = dilation * (kernel_size // 2)
        self.block = nn.Sequential(
            nn.Conv2d(in_channels, out_channels, kernel_size=kernel_size, padding=padding, dilation=dilation, bias=False),
            nn.GroupNorm(_group_count(out_channels), out_channels),
            nn.GELU(),
        )

    def forward(self, inputs: Tensor) -> Tensor:
        return _bounded(self.block(inputs))


class ResidualBlock(nn.Module):
    """Compact residual convolution block."""

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
        return _bounded(self.act(_bounded(self.conv2(self.conv1(inputs)) + self.skip(inputs))))


class SignedDetailStem(nn.Module):
    """Expose signed local detail and broader ABI context as learned features."""

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
        return self.fuse(
            torch.cat(
                (
                    self.raw(inputs),
                    self.local_pos(F.relu(local_detail)),
                    self.local_neg(F.relu(-local_detail)),
                    self.mid_pos(F.relu(mid_detail)),
                    self.context(broad),
                ),
                dim=1,
            )
        )


class MBConvBlock(nn.Module):
    """Small MBConv-style local context block used before attention."""

    def __init__(self, channels: int, *, expansion: int = 2) -> None:
        super().__init__()
        hidden = channels * expansion
        squeeze = max(channels // 4, 8)
        self.expand = ConvNormAct(channels, hidden, kernel_size=1)
        self.depthwise = nn.Sequential(
            nn.Conv2d(hidden, hidden, kernel_size=5, padding=2, groups=hidden, bias=False),
            nn.GroupNorm(_group_count(hidden), hidden),
            nn.GELU(),
        )
        self.se_reduce = nn.Conv2d(hidden, squeeze, kernel_size=1)
        self.se_expand = nn.Conv2d(squeeze, hidden, kernel_size=1)
        self.project = nn.Sequential(
            nn.Conv2d(hidden, channels, kernel_size=1, bias=False),
            nn.GroupNorm(_group_count(channels), channels),
        )
        self.scale = nn.Parameter(torch.tensor(0.2))
        self.act = nn.GELU()

    def forward(self, inputs: Tensor) -> Tensor:
        hidden = _bounded(self.depthwise(self.expand(inputs)))
        gate = torch.sigmoid(self.se_expand(F.gelu(self.se_reduce(F.adaptive_avg_pool2d(hidden, 1)))))
        projected = self.project(hidden * gate)
        return _bounded(inputs + torch.tanh(self.scale) * self.act(projected))


class TokenAttention(nn.Module):
    """Multi-head attention over already-partitioned image tokens."""

    def __init__(self, channels: int, *, num_heads: int = 4, mlp_ratio: int = 2) -> None:
        super().__init__()
        if channels % num_heads != 0:
            raise ValueError(f"channels={channels} must be divisible by num_heads={num_heads}")
        self.channels = channels
        self.num_heads = num_heads
        self.head_dim = channels // num_heads
        self.scale = 1.0 / math.sqrt(float(self.head_dim))
        self.norm1 = nn.LayerNorm(channels)
        self.qkv = nn.Linear(channels, channels * 3, bias=False)
        self.proj = nn.Linear(channels, channels)
        self.norm2 = nn.LayerNorm(channels)
        hidden = channels * mlp_ratio
        self.mlp = nn.Sequential(nn.Linear(channels, hidden), nn.GELU(), nn.Linear(hidden, channels))
        self.attn_gamma = nn.Parameter(torch.full((channels,), 0.08))
        self.mlp_gamma = nn.Parameter(torch.full((channels,), 0.08))

    def forward(self, tokens: Tensor) -> Tensor:
        normalized = self.norm1(tokens)
        qkv = self.qkv(normalized).view(tokens.shape[0], tokens.shape[1], 3, self.num_heads, self.head_dim)
        q, k, v = qkv.permute(2, 0, 3, 1, 4).unbind(0)
        attention = torch.softmax((q @ k.transpose(-2, -1)) * self.scale, dim=-1)
        attended = (attention @ v).transpose(1, 2).reshape(tokens.shape[0], tokens.shape[1], self.channels)
        tokens = tokens + self.proj(attended) * self.attn_gamma.view(1, 1, -1)
        return tokens + self.mlp(self.norm2(tokens)) * self.mlp_gamma.view(1, 1, -1)


class WindowAttentionBlock(nn.Module):
    """Local window attention for MaxViT-style short-range context."""

    def __init__(self, channels: int, *, window_size: int = 8, num_heads: int = 4) -> None:
        super().__init__()
        self.channels = channels
        self.window_size = window_size
        self.attention = TokenAttention(channels, num_heads=num_heads)

    def _partition(self, inputs: Tensor) -> Tensor:
        batch, channels, height, width = inputs.shape
        window = self.window_size
        if height % window != 0 or width % window != 0:
            raise ValueError(f"feature map {(height, width)} is not divisible by window size {window}")
        return (
            inputs.view(batch, channels, height // window, window, width // window, window)
            .permute(0, 2, 4, 3, 5, 1)
            .reshape(-1, window * window, channels)
        )

    def _merge(self, tokens: Tensor, *, batch: int, height: int, width: int) -> Tensor:
        window = self.window_size
        return (
            tokens.view(batch, height // window, width // window, window, window, self.channels)
            .permute(0, 5, 1, 3, 2, 4)
            .reshape(batch, self.channels, height, width)
        )

    def forward(self, inputs: Tensor) -> Tensor:
        batch, _, height, width = inputs.shape
        tokens = self._partition(inputs)
        return _bounded(self._merge(self.attention(tokens), batch=batch, height=height, width=width))


class GridAttentionBlock(nn.Module):
    """Sparse global grid attention: tokens sharing a window-relative position attend globally."""

    def __init__(self, channels: int, *, grid_size: int = 8, num_heads: int = 4) -> None:
        super().__init__()
        self.channels = channels
        self.grid_size = grid_size
        self.attention = TokenAttention(channels, num_heads=num_heads)

    def _partition(self, inputs: Tensor) -> Tensor:
        batch, channels, height, width = inputs.shape
        grid = self.grid_size
        if height % grid != 0 or width % grid != 0:
            raise ValueError(f"feature map {(height, width)} is not divisible by grid size {grid}")
        return (
            inputs.view(batch, channels, height // grid, grid, width // grid, grid)
            .permute(0, 3, 5, 2, 4, 1)
            .reshape(batch * grid * grid, (height // grid) * (width // grid), channels)
        )

    def _merge(self, tokens: Tensor, *, batch: int, height: int, width: int) -> Tensor:
        grid = self.grid_size
        return (
            tokens.view(batch, grid, grid, height // grid, width // grid, self.channels)
            .permute(0, 5, 3, 1, 4, 2)
            .reshape(batch, self.channels, height, width)
        )

    def forward(self, inputs: Tensor) -> Tensor:
        batch, _, height, width = inputs.shape
        tokens = self._partition(inputs)
        return _bounded(self._merge(self.attention(tokens), batch=batch, height=height, width=width))


class MaxViTStage(nn.Module):
    """Downsampled MBConv + local-window + global-grid attention stage."""

    def __init__(self, in_channels: int, out_channels: int, *, num_heads: int) -> None:
        super().__init__()
        self.down = nn.MaxPool2d(2)
        self.project = ResidualBlock(in_channels, out_channels)
        self.mbconv = MBConvBlock(out_channels)
        self.window = WindowAttentionBlock(out_channels, window_size=8, num_heads=num_heads)
        self.grid = GridAttentionBlock(out_channels, grid_size=8, num_heads=num_heads)
        self.refine = ResidualBlock(out_channels, out_channels)

    def forward(self, inputs: Tensor) -> Tensor:
        features = self.project(self.down(inputs))
        features = self.mbconv(features)
        features = self.window(features)
        features = self.grid(features)
        return self.refine(features)


class OrientedLineContext(nn.Module):
    """Differentiable anisotropic context for thin-line decoder continuity."""

    def __init__(self, channels: int) -> None:
        super().__init__()
        self.horizontal = nn.Sequential(
            nn.Conv2d(channels, channels, kernel_size=(1, 13), padding=(0, 6), groups=channels, bias=False),
            nn.GroupNorm(_group_count(channels), channels),
            nn.GELU(),
        )
        self.vertical = nn.Sequential(
            nn.Conv2d(channels, channels, kernel_size=(13, 1), padding=(6, 0), groups=channels, bias=False),
            nn.GroupNorm(_group_count(channels), channels),
            nn.GELU(),
        )
        self.diag2 = ConvNormAct(channels, channels, dilation=2)
        self.diag3 = ConvNormAct(channels, channels, dilation=3)
        self.project = nn.Sequential(ConvNormAct(channels * 5, channels, kernel_size=1), ResidualBlock(channels, channels))
        self.gate = nn.Sequential(ConvNormAct(channels * 2, channels, kernel_size=1), nn.Conv2d(channels, channels, kernel_size=1), nn.Sigmoid())

    def forward(self, inputs: Tensor) -> Tensor:
        context = self.project(
            torch.cat(
                (inputs, _bounded(self.horizontal(inputs)), _bounded(self.vertical(inputs)), self.diag2(inputs), self.diag3(inputs)),
                dim=1,
            )
        )
        gate = self.gate(torch.cat((inputs, context), dim=1))
        return _bounded(inputs + gate * context)


class PyramidMaxViTContext(nn.Module):
    """Bottleneck context using sparse attention and ASPP-style dilation."""

    def __init__(self, channels: int, *, num_heads: int) -> None:
        super().__init__()
        branch = max(channels // 4, 24)
        self.mbconv = MBConvBlock(channels)
        self.window = WindowAttentionBlock(channels, window_size=8, num_heads=num_heads)
        self.grid = GridAttentionBlock(channels, grid_size=8, num_heads=num_heads)
        self.branch1 = ConvNormAct(channels, branch, kernel_size=1)
        self.branch2 = ConvNormAct(channels, branch, dilation=2)
        self.branch4 = ConvNormAct(channels, branch, dilation=4)
        self.branch8 = ConvNormAct(channels, branch, dilation=8)
        self.image_pool = nn.Sequential(nn.AdaptiveAvgPool2d(1), ConvNormAct(channels, branch, kernel_size=1))
        self.project = nn.Sequential(ConvNormAct(branch * 5, channels, kernel_size=1), ResidualBlock(channels, channels))

    def forward(self, inputs: Tensor) -> Tensor:
        attended = self.grid(self.window(self.mbconv(inputs)))
        pooled = F.interpolate(self.image_pool(attended), size=attended.shape[-2:], mode="bilinear", align_corners=False)
        return self.project(torch.cat((self.branch1(attended), self.branch2(attended), self.branch4(attended), self.branch8(attended), pooled), dim=1))


class DecoderFuse(nn.Module):
    """Upsample and fuse encoder skips with line-aware decoder refinement."""

    def __init__(self, in_channels: int, skip_channels: int, out_channels: int, *, use_grid: bool = False) -> None:
        super().__init__()
        self.input_project = ConvNormAct(in_channels, out_channels, kernel_size=1)
        self.skip_project = ConvNormAct(skip_channels, out_channels, kernel_size=1)
        blocks: list[nn.Module] = [ConvNormAct(out_channels * 2, out_channels), ResidualBlock(out_channels, out_channels), OrientedLineContext(out_channels)]
        if use_grid:
            blocks.extend([WindowAttentionBlock(out_channels, window_size=8, num_heads=4), GridAttentionBlock(out_channels, grid_size=8, num_heads=4)])
        self.fuse = nn.Sequential(*blocks)

    def forward(self, inputs: Tensor, skip: Tensor) -> Tensor:
        upsampled = F.interpolate(inputs, size=skip.shape[-2:], mode="bilinear", align_corners=False)
        return self.fuse(torch.cat((self.input_project(upsampled), self.skip_project(skip)), dim=1))


class LineCalibratedHead(nn.Module):
    """Feature-level recall/line-evidence fusion head; no thresholding or postprocessing."""

    def __init__(self, channels: int) -> None:
        super().__init__()
        self.recall_features = nn.Sequential(ConvNormAct(channels, channels, dilation=2), ResidualBlock(channels, channels))
        self.line_features = nn.Sequential(OrientedLineContext(channels), ResidualBlock(channels, channels))
        self.fuse_gate = nn.Sequential(
            ConvNormAct(channels * 4, channels, kernel_size=1),
            nn.Conv2d(channels, channels, kernel_size=1),
            nn.Sigmoid(),
        )
        self.fuse = nn.Sequential(ConvNormAct(channels * 3, channels), ResidualBlock(channels, channels))
        self.mask_head = nn.Conv2d(channels, 1, kernel_size=1)
        self.line_head = nn.Conv2d(channels, 1, kernel_size=1)
        self.centerline_head = nn.Conv2d(channels, 1, kernel_size=1)

    def forward(self, features: Tensor) -> dict[str, Tensor]:
        recall = self.recall_features(features)
        line = self.line_features(features)
        gate = self.fuse_gate(torch.cat((features, recall, line, torch.abs(recall - line)), dim=1))
        fused = self.fuse(torch.cat((features, gate * recall, (1.0 - gate) * line), dim=1))
        return {
            "mask_logits": self.mask_head(fused),
            "line_logits": self.line_head(line),
            "centerline_logits": self.centerline_head(fused),
        }


class CompactMaxViTLineContextUNet(nn.Module):
    """Compact MaxViT-style U-Net with line-context decoder for contrail masks."""

    def __init__(self) -> None:
        super().__init__()
        base = 24
        self.features = SingleFrameFeatureBuilder(learned_channels=12)
        self.stem = SignedDetailStem(self.features.out_channels, base)
        self.scale0 = nn.Sequential(ResidualBlock(base, base), MBConvBlock(base), OrientedLineContext(base))
        self.down1 = MaxViTStage(base, base * 2, num_heads=4)
        self.down2 = MaxViTStage(base * 2, base * 4, num_heads=4)
        self.down3 = MaxViTStage(base * 4, base * 6, num_heads=6)
        self.context = PyramidMaxViTContext(base * 6, num_heads=6)
        self.up2 = DecoderFuse(base * 6, base * 4, base * 4, use_grid=True)
        self.up1 = DecoderFuse(base * 4, base * 2, base * 2)
        self.up0 = DecoderFuse(base * 2, base, base)
        self.highres_detail = SignedDetailStem(self.features.out_channels, base)
        self.refine = nn.Sequential(
            ConvNormAct(base * 3, base),
            ResidualBlock(base, base),
            OrientedLineContext(base),
            ResidualBlock(base, base),
        )
        self.head = LineCalibratedHead(base)

    def forward(self, inputs: Tensor) -> dict[str, Tensor]:
        features = self.features(inputs)
        stem = self.stem(features)
        scale0 = self.scale0(stem)
        scale1 = self.down1(scale0)
        scale2 = self.down2(scale1)
        scale3 = self.down3(scale2)
        context = self.context(scale3)
        dec2 = self.up2(context, scale2)
        dec1 = self.up1(dec2, scale1)
        dec0 = self.up0(dec1, scale0)
        detail = self.highres_detail(features)
        refined = self.refine(torch.cat((dec0, detail, stem), dim=1))
        return self.head(refined)


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
    return CompactMaxViTLineContextUNet()
