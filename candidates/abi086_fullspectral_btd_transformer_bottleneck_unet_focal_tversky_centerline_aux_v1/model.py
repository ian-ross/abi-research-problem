"""Full-spectral BTD transformer-bottleneck U-Net for ABI contrail segmentation."""

from __future__ import annotations

import torch
import torch.nn.functional as F
from torch import Tensor, nn


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
    """Residual convolution block used at each image scale."""

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


class DownBlock(nn.Module):
    """Resolution-halving residual encoder block."""

    def __init__(self, in_channels: int, out_channels: int) -> None:
        super().__init__()
        self.block = nn.Sequential(nn.MaxPool2d(2), ResidualBlock(in_channels, out_channels))

    def forward(self, inputs: Tensor) -> Tensor:
        return self.block(inputs)


class UpBlock(nn.Module):
    """Upsample decoder features and fuse with a skip tensor."""

    def __init__(self, in_channels: int, skip_channels: int, out_channels: int) -> None:
        super().__init__()
        self.skip_project = ConvNormAct(skip_channels, skip_channels, kernel_size=1)
        self.fuse = nn.Sequential(
            ConvNormAct(in_channels + skip_channels, out_channels),
            ResidualBlock(out_channels, out_channels),
        )

    def forward(self, inputs: Tensor, skip: Tensor) -> Tensor:
        upsampled = F.interpolate(inputs, size=skip.shape[-2:], mode="bilinear", align_corners=False)
        return self.fuse(torch.cat((upsampled, self.skip_project(skip)), dim=1))


class BottleneckSelfAttentionBlock(nn.Module):
    """Global self-attention over the low-resolution feature map."""

    def __init__(self, channels: int, *, num_heads: int = 8, mlp_ratio: int = 3) -> None:
        super().__init__()
        self.norm1 = nn.LayerNorm(channels)
        self.attn = nn.MultiheadAttention(channels, num_heads=num_heads, batch_first=True)
        self.norm2 = nn.LayerNorm(channels)
        hidden = channels * mlp_ratio
        self.mlp = nn.Sequential(
            nn.Linear(channels, hidden),
            nn.GELU(),
            nn.Linear(hidden, channels),
        )
        self.spatial_project = ConvNormAct(channels, channels, kernel_size=1)

    def forward(self, inputs: Tensor) -> Tensor:
        batch, channels, height, width = inputs.shape
        tokens = inputs.flatten(2).transpose(1, 2)
        attn_tokens, _ = self.attn(self.norm1(tokens), self.norm1(tokens), self.norm1(tokens), need_weights=False)
        tokens = tokens + attn_tokens
        tokens = tokens + self.mlp(self.norm2(tokens))
        features = tokens.transpose(1, 2).reshape(batch, channels, height, width)
        return self.spatial_project(features + inputs)


class TransformerBottleneck(nn.Module):
    """Two global-attention blocks at 1/16 resolution plus dilated convolution context."""

    def __init__(self, channels: int) -> None:
        super().__init__()
        self.pre = ResidualBlock(channels, channels, dilation=2)
        self.attn1 = BottleneckSelfAttentionBlock(channels)
        self.attn2 = BottleneckSelfAttentionBlock(channels)
        self.post = nn.Sequential(
            ResidualBlock(channels, channels, dilation=4),
            ConvNormAct(channels, channels, kernel_size=1),
        )

    def forward(self, inputs: Tensor) -> Tensor:
        features = self.pre(inputs)
        features = self.attn1(features)
        features = self.attn2(features)
        return self.post(features)


class DetailAwareHead(nn.Module):
    """Fuse decoded mask evidence with high-resolution spectral detail before logits."""

    def __init__(self, channels: int) -> None:
        super().__init__()
        self.detail = nn.Sequential(
            ConvNormAct(channels, channels, kernel_size=3),
            ResidualBlock(channels, channels),
        )
        self.context_gate = nn.Sequential(
            ConvNormAct(channels * 2, channels, kernel_size=1),
            nn.Conv2d(channels, channels, kernel_size=1, bias=True),
            nn.Sigmoid(),
        )
        self.project = nn.Sequential(
            ConvNormAct(channels * 2, channels),
            ResidualBlock(channels, channels),
        )

    def forward(self, inputs: Tensor) -> Tensor:
        local_detail = self.detail(inputs - F.avg_pool2d(inputs, kernel_size=9, stride=1, padding=4, count_include_pad=False))
        smooth_context = F.avg_pool2d(inputs, kernel_size=17, stride=1, padding=8, count_include_pad=False)
        gate = self.context_gate(torch.cat((inputs, smooth_context), dim=1))
        return self.project(torch.cat((inputs * (0.75 + 0.5 * gate), local_detail), dim=1))


class FullSpectralBTDTransformerBottleneckUNet(nn.Module):
    """Compact U-Net scout with global low-resolution scene attention."""

    def __init__(self) -> None:
        super().__init__()
        self.front_end = NormalizedBTDFrontEnd(learned_channels=16)
        base = 40
        self.stem = nn.Sequential(
            ConvNormAct(self.front_end.out_channels, base, kernel_size=1),
            ResidualBlock(base, base),
        )
        self.enc1 = DownBlock(base, base * 2)
        self.enc2 = DownBlock(base * 2, base * 4)
        self.enc3 = DownBlock(base * 4, base * 6)
        self.enc4 = DownBlock(base * 6, base * 8)
        self.context = TransformerBottleneck(base * 8)
        self.up3 = UpBlock(base * 8, base * 6, base * 6)
        self.up2 = UpBlock(base * 6, base * 4, base * 4)
        self.up1 = UpBlock(base * 4, base * 2, base * 2)
        self.up0 = UpBlock(base * 2, base, base)
        self.head_features = DetailAwareHead(base)
        self.mask_head = nn.Conv2d(base, 1, kernel_size=1)
        self.centerline_head = nn.Conv2d(base, 1, kernel_size=1)

    def forward(self, inputs: Tensor) -> dict[str, Tensor]:
        features = self.front_end(inputs)
        stem = self.stem(features)
        enc1 = self.enc1(stem)
        enc2 = self.enc2(enc1)
        enc3 = self.enc3(enc2)
        enc4 = self.enc4(enc3)
        context = self.context(enc4)
        dec3 = self.up3(context, enc3)
        dec2 = self.up2(dec3, enc2)
        dec1 = self.up1(dec2, enc1)
        dec0 = self.up0(dec1, stem)
        refined = self.head_features(dec0)
        return {
            "mask_logits": self.mask_head(refined),
            "centerline_logits": self.centerline_head(refined),
        }


def _validate_centerline_auxiliary_output(output_spec: dict[str, object]) -> None:
    auxiliary_outputs = output_spec.get("auxiliary_outputs")
    expected = [{"target": "centerline", "name": "centerline_logits", "shape": [1, 256, 256]}]
    if auxiliary_outputs != expected:
        raise ValueError(
            "abi086_fullspectral_btd_transformer_bottleneck_unet_focal_tversky_centerline_aux_v1 requires "
            "exactly one trusted centerline auxiliary output named centerline_logits"
        )


def build_model(input_spec: dict[str, object], output_spec: dict[str, object]) -> nn.Module:
    """Build the model for the Harness-supplied ABI contract."""

    if input_spec.get("mode") != "abi_16ch" or input_spec.get("shape") != [16, 256, 256]:
        raise ValueError(
            "abi086_fullspectral_btd_transformer_bottleneck_unet_focal_tversky_centerline_aux_v1 requires "
            "abi_16ch [16, 256, 256] input"
        )
    if output_spec.get("form") != "mask_logits" or output_spec.get("shape") != [1, 256, 256]:
        raise ValueError(
            "abi086_fullspectral_btd_transformer_bottleneck_unet_focal_tversky_centerline_aux_v1 requires "
            "mask_logits [1, 256, 256] primary output"
        )
    _validate_centerline_auxiliary_output(output_spec)
    return FullSpectralBTDTransformerBottleneckUNet()
