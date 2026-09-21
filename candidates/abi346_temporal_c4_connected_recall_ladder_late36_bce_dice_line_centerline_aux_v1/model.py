"""Temporal C4 line-state U-Net with a connected-recall ladder logit head."""

from __future__ import annotations

import torch
import torch.nn.functional as F
from torch import Tensor, nn


CANDIDATE_ID = "abi346_temporal_c4_connected_recall_ladder_late36_bce_dice_line_centerline_aux_v1"
TEMPORAL_OFFSETS = [-1, 0, 1]
CHANNELS_PER_FRAME = 17
FRAME_COUNT = 3
INPUT_CHANNELS = CHANNELS_PER_FRAME * FRAME_COUNT


def _finite_feature(inputs: Tensor, *, limit: float, nan: float = 0.0) -> Tensor:
    """Map non-finite candidate-visible feature values to bounded neutral values."""

    return torch.nan_to_num(inputs, nan=nan, posinf=limit, neginf=-limit).clamp(-limit, limit)


def _bounded(inputs: Tensor, *, limit: float = 12.0) -> Tensor:
    """Bound finite internal activations without hiding non-finite parameter failures."""

    return torch.clamp(inputs, min=-limit, max=limit)


class TemporalFrameFeatureBuilder(nn.Module):
    """Build finite per-frame ABI+SZA+BTD features for temporal-attention fusion."""

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
    # Zero-based ABI indices within each 17-channel candidate-visible temporal frame.
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

    def __init__(self) -> None:
        super().__init__()
        self.register_buffer("abi_means", torch.tensor(self._ABI_MEANS, dtype=torch.float32).view(1, 16, 1, 1))
        self.register_buffer("abi_scales", torch.tensor(self._ABI_SCALES, dtype=torch.float32).view(1, 16, 1, 1))
        self.out_channels = 16 + len(self._BTD_PAIRS) + 2

    def forward_frame(self, frame: Tensor) -> Tensor:
        if frame.ndim != 4 or frame.shape[1] != CHANNELS_PER_FRAME:
            raise ValueError(f"expected [N, {CHANNELS_PER_FRAME}, H, W] ABI+SZA frame, got {tuple(frame.shape)}")
        abi = frame[:, :16, :, :]
        sza = frame[:, 16:17, :, :]
        normalized = _finite_feature((abi - self.abi_means) / self.abi_scales, limit=6.0)
        btd = _finite_feature(
            torch.cat(
                [(abi[:, a : a + 1, :, :] - abi[:, b : b + 1, :, :]) / self._BTD_SCALE for a, b in self._BTD_PAIRS],
                dim=1,
            ),
            limit=6.0,
        )
        sza_finite = torch.nan_to_num(sza, nan=90.0, posinf=180.0, neginf=0.0)
        sza_clamped = torch.clamp(sza_finite, 0.0, 180.0)
        sza_scaled = (sza_clamped - 90.0) / 90.0
        sza_cosine = torch.cos(torch.deg2rad(sza_clamped))
        return torch.cat((normalized, btd, sza_scaled, sza_cosine), dim=1)

    def forward(self, inputs: Tensor) -> tuple[Tensor, Tensor, Tensor]:
        if inputs.ndim != 4 or inputs.shape[1] != INPUT_CHANNELS:
            raise ValueError(f"expected [N, {INPUT_CHANNELS}, H, W] temporal ABI+SZA tensor, got {tuple(inputs.shape)}")
        batch, _, height, width = inputs.shape
        frames = inputs.reshape(batch, FRAME_COUNT, CHANNELS_PER_FRAME, height, width)
        previous = self.forward_frame(frames[:, 0, :, :, :])
        center = self.forward_frame(frames[:, 1, :, :, :])
        next_frame = self.forward_frame(frames[:, 2, :, :, :])
        return previous, center, next_frame


def _group_count(channels: int) -> int:
    for groups in (8, 6, 4, 3, 2, 1):
        if channels % groups == 0:
            return groups
    return 1


class ConvNormAct(nn.Module):
    """Convolution, GroupNorm, GELU, and bounded activations for stable temporal training."""

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
    """Compact residual block used in the encoder, temporal stem, and decoder."""

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


class C4OrientationConsensusLineState(nn.Module):
    """Rotation-shared line-state consensus before the temporal encoder pyramid.

    The branch differs from ABI-275/282 post-decoder C4 heads by organizing the
    early temporal line state itself.  It shares one anisotropic strip filter
    across 0/90/180/270-degree rotations, learns an orientation attention map,
    and returns bounded architecture-internal features only; it does not perform
    thresholding, morphology, Artifact Filtering, or postprocessing.
    """

    def __init__(self, channels: int) -> None:
        super().__init__()
        self.local = ResidualBlock(channels, channels)
        self.shared_strip = nn.Sequential(
            nn.Conv2d(channels, channels, kernel_size=(1, 13), padding=(0, 6), groups=channels, bias=False),
            nn.GroupNorm(_group_count(channels), channels),
            nn.GELU(),
            nn.Conv2d(channels, channels, kernel_size=1, bias=False),
        )
        self.orientation_score = nn.Conv2d(channels, 1, kernel_size=1)
        self.consensus_gate = nn.Sequential(
            ConvNormAct(channels * 4, channels, kernel_size=1),
            nn.Conv2d(channels, channels, kernel_size=1),
            nn.Sigmoid(),
        )
        self.project = nn.Sequential(
            ConvNormAct(channels * 5, channels, kernel_size=1),
            ResidualBlock(channels, channels),
        )

    def forward(self, line_seed: Tensor, appearance: Tensor) -> Tensor:
        local = self.local(line_seed)
        oriented = []
        for rotations in range(4):
            rotated = torch.rot90(local, rotations, dims=(-2, -1))
            filtered = _bounded(self.shared_strip(rotated))
            oriented.append(torch.rot90(filtered, -rotations, dims=(-2, -1)))
        oriented_stack = torch.stack(oriented, dim=1)
        batch, orientations, channels, height, width = oriented_stack.shape
        scores = self.orientation_score(oriented_stack.flatten(0, 1)).view(batch, orientations, 1, height, width)
        weights = torch.softmax(scores, dim=1)
        weighted = _bounded((oriented_stack * weights).sum(dim=1))
        orientation_mean = _bounded(oriented_stack.mean(dim=1))
        orientation_max = _bounded(oriented_stack.amax(dim=1))
        agreement = _bounded(orientation_mean * torch.sigmoid(orientation_max))
        gate = self.consensus_gate(torch.cat((appearance, local, weighted, agreement), dim=1))
        consensus = self.project(torch.cat((line_seed, local, weighted, orientation_mean, agreement), dim=1))
        return _bounded(gate * consensus)


class TemporalLineStateStem(nn.Module):
    """Fuse temporal frames and expose an early C4 orientation-consensus line state."""

    def __init__(self, frame_feature_channels: int, out_channels: int) -> None:
        super().__init__()
        self.frame_project = nn.Sequential(
            ConvNormAct(frame_feature_channels, out_channels, kernel_size=1),
            ResidualBlock(out_channels, out_channels),
        )
        self.attention_hidden = ConvNormAct(out_channels * 3, out_channels, kernel_size=1)
        self.attention_logits = nn.Conv2d(out_channels, 1, kernel_size=1)
        self.change_project = nn.Sequential(
            ConvNormAct(frame_feature_channels * 4, out_channels, kernel_size=1),
            ResidualBlock(out_channels, out_channels),
        )
        self.center_gate = nn.Sequential(
            ConvNormAct(out_channels * 3, out_channels, kernel_size=1),
            nn.Conv2d(out_channels, out_channels, kernel_size=1),
            nn.Sigmoid(),
        )
        self.appearance_fuse = nn.Sequential(
            ConvNormAct(out_channels * 3, out_channels, kernel_size=1),
            ResidualBlock(out_channels, out_channels),
        )
        self.line_seed = nn.Sequential(
            ConvNormAct(out_channels * 4, out_channels, kernel_size=1),
            ResidualBlock(out_channels, out_channels),
        )
        self.c4_line_consensus = C4OrientationConsensusLineState(out_channels)
        self.line_gate = nn.Sequential(
            ConvNormAct(out_channels * 2, out_channels, kernel_size=1),
            nn.Conv2d(out_channels, out_channels, kernel_size=1),
            nn.Sigmoid(),
        )
        self.output_refine = nn.Sequential(
            ConvNormAct(out_channels * 2, out_channels, kernel_size=1),
            ResidualBlock(out_channels, out_channels),
            ResidualBlock(out_channels, out_channels),
        )

    def _frame_attention_logit(self, frame_embed: Tensor, center_embed: Tensor) -> Tensor:
        attention_input = torch.cat((frame_embed, center_embed, torch.abs(frame_embed - center_embed)), dim=1)
        return self.attention_logits(self.attention_hidden(attention_input))

    def forward(self, previous: Tensor, center: Tensor, next_frame: Tensor) -> tuple[Tensor, Tensor]:
        previous_embed = self.frame_project(previous)
        center_embed = self.frame_project(center)
        next_embed = self.frame_project(next_frame)

        logits = torch.stack(
            (
                self._frame_attention_logit(previous_embed, center_embed),
                self._frame_attention_logit(center_embed, center_embed),
                self._frame_attention_logit(next_embed, center_embed),
            ),
            dim=1,
        )
        weights = torch.softmax(logits, dim=1)
        stacked_frames = torch.stack((previous_embed, center_embed, next_embed), dim=1)
        attended = _bounded((weights * stacked_frames).sum(dim=1))

        neighbor_mean = 0.5 * (previous + next_frame)
        change_features = torch.cat(
            (
                _finite_feature(center - neighbor_mean, limit=8.0),
                _finite_feature(next_frame - previous, limit=8.0),
                _finite_feature(torch.abs(center - previous), limit=8.0),
                _finite_feature(torch.abs(next_frame - center), limit=8.0),
            ),
            dim=1,
        )
        change_embed = self.change_project(change_features)
        center_weight = self.center_gate(torch.cat((center_embed, attended, change_embed), dim=1))
        center_residual = _bounded(center_weight * center_embed + (1.0 - center_weight) * attended)
        appearance = self.appearance_fuse(torch.cat((center_residual, attended, change_embed), dim=1))

        line_seed = self.line_seed(
            torch.cat((center_embed, attended, change_embed, torch.abs(center_embed - attended)), dim=1)
        )
        line_state = self.c4_line_consensus(line_seed, appearance)
        gate = self.line_gate(torch.cat((appearance, line_state), dim=1))
        fused = self.output_refine(torch.cat((appearance, gate * line_state), dim=1))
        return fused, _bounded(gate * line_state)


class DownBlock(nn.Module):
    """Downsample by two and encode the next scale."""

    def __init__(self, in_channels: int, out_channels: int) -> None:
        super().__init__()
        self.block = nn.Sequential(
            nn.MaxPool2d(2),
            ResidualBlock(in_channels, out_channels),
            ResidualBlock(out_channels, out_channels),
        )

    def forward(self, inputs: Tensor) -> Tensor:
        return self.block(inputs)


class SingleStreamEncoder(nn.Module):
    """Single compact encoder after temporal-attention fusion."""

    def __init__(self, base_channels: int) -> None:
        super().__init__()
        self.stem_refine = ResidualBlock(base_channels, base_channels)
        self.down1 = DownBlock(base_channels, base_channels * 2)
        self.down2 = DownBlock(base_channels * 2, base_channels * 4)
        self.down3 = DownBlock(base_channels * 4, base_channels * 8)

    def forward(self, features: Tensor) -> tuple[Tensor, Tensor, Tensor, Tensor]:
        scale0 = self.stem_refine(features)
        scale1 = self.down1(scale0)
        scale2 = self.down2(scale1)
        scale3 = self.down3(scale2)
        return scale0, scale1, scale2, scale3


class ASPPContext(nn.Module):
    """Small atrous context block at the bottleneck."""

    def __init__(self, channels: int) -> None:
        super().__init__()
        branch = max(channels // 4, 16)
        self.branch1 = ConvNormAct(channels, branch, kernel_size=1)
        self.branch2 = ConvNormAct(channels, branch, dilation=2)
        self.branch4 = ConvNormAct(channels, branch, dilation=4)
        self.branch8 = ConvNormAct(channels, branch, dilation=8)
        self.image_pool = nn.Sequential(nn.AdaptiveAvgPool2d(1), ConvNormAct(channels, branch, kernel_size=1))
        self.project = nn.Sequential(ConvNormAct(branch * 5, channels, kernel_size=1), ResidualBlock(channels, channels))

    def forward(self, inputs: Tensor) -> Tensor:
        pooled = F.interpolate(self.image_pool(inputs), size=inputs.shape[-2:], mode="bilinear", align_corners=False)
        return self.project(torch.cat((self.branch1(inputs), self.branch2(inputs), self.branch4(inputs), self.branch8(inputs), pooled), dim=1))


class DecoderFuse(nn.Module):
    """Upsample and merge decoder features with one encoder skip scale."""

    def __init__(self, in_channels: int, skip_channels: int, out_channels: int) -> None:
        super().__init__()
        self.input_project = ConvNormAct(in_channels, out_channels, kernel_size=1)
        self.skip_project = ConvNormAct(skip_channels, out_channels, kernel_size=1)
        self.fuse = nn.Sequential(ConvNormAct(out_channels * 2, out_channels), ResidualBlock(out_channels, out_channels))

    def forward(self, inputs: Tensor, skip: Tensor) -> Tensor:
        upsampled = F.interpolate(inputs, size=skip.shape[-2:], mode="bilinear", align_corners=False)
        return self.fuse(torch.cat((self.input_project(upsampled), self.skip_project(skip)), dim=1))


class LineStateInjector(nn.Module):
    """Gate an early temporal line state into one encoder scale."""

    def __init__(self, line_channels: int, scale_channels: int) -> None:
        super().__init__()
        self.line_project = ConvNormAct(line_channels, scale_channels, kernel_size=1)
        self.gate = nn.Sequential(
            ConvNormAct(scale_channels * 2, scale_channels, kernel_size=1),
            nn.Conv2d(scale_channels, scale_channels, kernel_size=1),
            nn.Sigmoid(),
        )
        self.refine = ResidualBlock(scale_channels, scale_channels)

    def forward(self, scale_features: Tensor, line_state: Tensor) -> Tensor:
        line_resized = F.interpolate(line_state, size=scale_features.shape[-2:], mode="bilinear", align_corners=False)
        line_projected = self.line_project(line_resized)
        gate = self.gate(torch.cat((scale_features, line_projected), dim=1))
        return self.refine(_bounded(scale_features + gate * line_projected))


class HighResolutionDirectionalContext(nn.Module):
    """Residual orientation-aware context over full-resolution decoder features."""

    def __init__(self, channels: int) -> None:
        super().__init__()
        self.local = ResidualBlock(channels, channels)
        self.horizontal = nn.Sequential(
            nn.Conv2d(channels, channels, kernel_size=(1, 9), padding=(0, 4), groups=channels, bias=False),
            nn.GroupNorm(_group_count(channels), channels),
            nn.GELU(),
            nn.Conv2d(channels, channels, kernel_size=1, bias=False),
        )
        self.vertical = nn.Sequential(
            nn.Conv2d(channels, channels, kernel_size=(9, 1), padding=(4, 0), groups=channels, bias=False),
            nn.GroupNorm(_group_count(channels), channels),
            nn.GELU(),
            nn.Conv2d(channels, channels, kernel_size=1, bias=False),
        )
        self.diagonal_near = ConvNormAct(channels, channels, dilation=2)
        self.diagonal_wide = ConvNormAct(channels, channels, dilation=4)
        self.gate = nn.Sequential(
            ConvNormAct(channels * 5, channels, kernel_size=1),
            nn.Conv2d(channels, channels, kernel_size=1),
            nn.Sigmoid(),
        )
        self.project = nn.Sequential(
            ConvNormAct(channels * 5, channels, kernel_size=1),
            ResidualBlock(channels, channels),
        )

    def forward(self, inputs: Tensor) -> Tensor:
        local = self.local(inputs)
        horizontal = _bounded(self.horizontal(local))
        vertical = _bounded(self.vertical(local))
        diagonal_near = self.diagonal_near(local)
        diagonal_wide = self.diagonal_wide(local)
        stacked = torch.cat((local, horizontal, vertical, diagonal_near, diagonal_wide), dim=1)
        directional = self.project(stacked)
        gate = self.gate(stacked)
        return _bounded(inputs + gate * directional)


class ConnectedRecallLadderHead(nn.Module):
    """Mask/line/centerline logits with compact connected-recall support.

    ABI-306 left useful latent recall below the trusted 0.5 threshold while
    becoming a compact high-precision temporal C4 comparator.  This head keeps a
    base mask anchor and adds only bounded architecture-internal logit changes:
    a non-negative recall ladder in the soft mask uncertainty band, gated by
    learned mask/line/centerline agreement and a local continuity summary, plus a
    small low-evidence veto for decoder regions with weak line support.  It does
    not implement thresholding, morphology, Artifact Filters, postprocessing, or
    custom losses.
    """

    def __init__(self, channels: int) -> None:
        super().__init__()
        self.shared = nn.Sequential(
            ConvNormAct(channels, channels),
            ResidualBlock(channels, channels),
            ConvNormAct(channels, channels // 2, kernel_size=1),
        )
        head_channels = channels // 2
        self.base_mask_logits = nn.Conv2d(head_channels, 1, kernel_size=1)
        self.line_logits = nn.Conv2d(head_channels, 1, kernel_size=1)
        self.centerline_logits = nn.Conv2d(head_channels, 1, kernel_size=1)
        self.continuity_context = nn.Sequential(
            nn.Conv2d(head_channels, head_channels, kernel_size=(1, 11), padding=(0, 5), groups=head_channels, bias=False),
            nn.GroupNorm(_group_count(head_channels), head_channels),
            nn.GELU(),
            nn.Conv2d(head_channels, head_channels, kernel_size=(11, 1), padding=(5, 0), groups=head_channels, bias=False),
            nn.GroupNorm(_group_count(head_channels), head_channels),
            nn.GELU(),
            nn.Conv2d(head_channels, head_channels, kernel_size=1, bias=False),
        )
        self.recall_gate = nn.Sequential(
            ConvNormAct(head_channels + 6, head_channels, kernel_size=1),
            nn.Conv2d(head_channels, 1, kernel_size=1),
            nn.Sigmoid(),
        )
        self.recall_ladder_logits = nn.Conv2d(head_channels, 1, kernel_size=1)
        self.clutter_veto = nn.Sequential(
            ConvNormAct(head_channels + 4, head_channels, kernel_size=1),
            nn.Conv2d(head_channels, 1, kernel_size=1),
            nn.Sigmoid(),
        )

    def forward(self, features: Tensor) -> dict[str, Tensor]:
        shared = self.shared(features)
        continuity = _bounded(self.continuity_context(shared))
        base_mask = self.base_mask_logits(shared)
        line_logits = self.line_logits(shared)
        centerline_logits = self.centerline_logits(shared)

        mask_prob = torch.sigmoid(base_mask)
        line_prob = torch.sigmoid(line_logits)
        centerline_prob = torch.sigmoid(centerline_logits)
        line_agreement = torch.sqrt(torch.clamp(line_prob * centerline_prob, min=0.0, max=1.0))
        continuity_prob = torch.sigmoid(continuity.mean(dim=1, keepdim=True))
        uncertainty_band = torch.clamp((0.62 - mask_prob).clamp_min(0.0) * (mask_prob - 0.12).clamp_min(0.0) * 12.0, 0.0, 1.0)
        high_confidence_anchor = torch.clamp((mask_prob - 0.48) * 5.0, 0.0, 1.0)
        low_line_evidence = torch.clamp(0.45 - torch.maximum(line_prob, centerline_prob), min=0.0, max=0.45) / 0.45

        recall_inputs = torch.cat(
            (
                shared,
                mask_prob,
                line_prob,
                centerline_prob,
                line_agreement,
                continuity_prob,
                uncertainty_band,
            ),
            dim=1,
        )
        recall_gate = self.recall_gate(recall_inputs)
        positive_ladder = 0.55 * uncertainty_band * recall_gate * torch.sigmoid(self.recall_ladder_logits(shared))

        veto_inputs = torch.cat((shared, mask_prob, line_agreement, continuity_prob, low_line_evidence), dim=1)
        veto = 0.25 * low_line_evidence * (1.0 - high_confidence_anchor) * self.clutter_veto(veto_inputs)
        mask_logits = _bounded(base_mask + positive_ladder - veto)
        return {
            "mask_logits": mask_logits,
            "line_logits": line_logits,
            "centerline_logits": centerline_logits,
        }


class TemporalLineStateAttentionUNet(nn.Module):
    """Temporal C4 line-state U-Net with a connected-recall ladder logit head."""

    def __init__(self) -> None:
        super().__init__()
        base = 24
        self.temporal_features = TemporalFrameFeatureBuilder()
        self.temporal_stem = TemporalLineStateStem(self.temporal_features.out_channels, base)
        self.encoder = SingleStreamEncoder(base)
        self.inject0 = LineStateInjector(base, base)
        self.inject1 = LineStateInjector(base, base * 2)
        self.inject2 = LineStateInjector(base, base * 4)
        self.inject3 = LineStateInjector(base, base * 8)
        self.context = ASPPContext(base * 8)
        self.up2 = DecoderFuse(base * 8, base * 4, base * 4)
        self.up1 = DecoderFuse(base * 4, base * 2, base * 2)
        self.up0 = DecoderFuse(base * 2, base, base)
        self.refine = nn.Sequential(
            ConvNormAct(base * 2, base),
            ResidualBlock(base, base),
            ResidualBlock(base, base),
        )
        self.directional_context = HighResolutionDirectionalContext(base)
        self.head = ConnectedRecallLadderHead(base)

    def forward(self, inputs: Tensor) -> dict[str, Tensor]:
        previous, center, next_frame = self.temporal_features(inputs)
        stem, line_state = self.temporal_stem(previous, center, next_frame)
        scale0, scale1, scale2, scale3 = self.encoder(stem)
        scale0 = self.inject0(scale0, line_state)
        scale1 = self.inject1(scale1, line_state)
        scale2 = self.inject2(scale2, line_state)
        scale3 = self.inject3(scale3, line_state)
        context = self.context(scale3)
        dec2 = self.up2(context, scale2)
        dec1 = self.up1(dec2, scale1)
        dec0 = self.up0(dec1, scale0)
        refined = self.refine(torch.cat((dec0, scale0), dim=1))
        refined = self.directional_context(refined)
        return self.head(refined)


def _validate_auxiliary_outputs(output_spec: dict[str, object]) -> None:
    auxiliary_outputs = output_spec.get("auxiliary_outputs")
    expected = [
        {"target": "line", "name": "line_logits", "shape": [1, 256, 256]},
        {"target": "centerline", "name": "centerline_logits", "shape": [1, 256, 256]},
    ]
    if auxiliary_outputs != expected:
        raise ValueError(f"{CANDIDATE_ID} requires trusted line_logits and centerline_logits auxiliary outputs")


def build_model(input_spec: dict[str, object], output_spec: dict[str, object]) -> nn.Module:
    """Build the model for the Harness-supplied temporal ABI contract."""

    if input_spec.get("mode") != "abi_16ch_plus_sza_temporal":
        raise ValueError(f"{CANDIDATE_ID} requires abi_16ch_plus_sza_temporal input")
    if input_spec.get("shape") != [INPUT_CHANNELS, 256, 256]:
        raise ValueError(f"{CANDIDATE_ID} requires [{INPUT_CHANNELS}, 256, 256] input")
    if input_spec.get("layout") != "channel_stacked_temporal_frames":
        raise ValueError(f"{CANDIDATE_ID} requires channel-stacked temporal input")
    if input_spec.get("base_channels_per_frame") != CHANNELS_PER_FRAME:
        raise ValueError(f"{CANDIDATE_ID} requires {CHANNELS_PER_FRAME} channels per temporal frame")
    offsets = input_spec.get("temporal_frame_offsets", input_spec.get("default_temporal_frame_offsets"))
    if offsets != TEMPORAL_OFFSETS:
        raise ValueError(f"{CANDIDATE_ID} requires temporal frame offsets {TEMPORAL_OFFSETS}")
    if input_spec.get("source_channel_indices_per_frame") not in (None, list(range(16)) + [18]):
        raise ValueError(f"{CANDIDATE_ID} received an unexpected per-frame source-channel contract")
    if output_spec.get("form") != "mask_logits" or output_spec.get("shape") != [1, 256, 256]:
        raise ValueError(f"{CANDIDATE_ID} requires mask_logits [1, 256, 256] primary output")
    _validate_auxiliary_outputs(output_spec)
    return TemporalLineStateAttentionUNet()
