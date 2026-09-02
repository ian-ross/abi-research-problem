"""Full-spectral DeepLabV3+ BTD-mixer with a trusted Centerline Target auxiliary head."""

from __future__ import annotations

import segmentation_models_pytorch as smp
import torch
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
    # Zero-based candidate-input channel pairs. All use already-approved ABI channels.
    # These emphasize longwave-window, dirty-window, cloud-phase, and water-vapor contrasts.
    _BTD_PAIRS = (
        (12, 13),  # ABI 13 - ABI 14
        (13, 14),  # ABI 14 - ABI 15
        (12, 14),  # ABI 13 - ABI 15
        (10, 13),  # ABI 11 - ABI 14
        (6, 13),   # ABI 7 - ABI 14
        (7, 9),    # ABI 8 - ABI 10
        (7, 12),   # ABI 8 - ABI 13
        (8, 13),   # ABI 9 - ABI 14
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


class FullSpectralBTDClDiceCenterlineAuxDeepLabV3Plus(nn.Module):
    """DeepLabV3+ decoder with primary mask and trusted Centerline Target auxiliary logits."""

    def __init__(self) -> None:
        super().__init__()
        self.front_end = NormalizedBTDFrontEnd(learned_channels=16)
        self.network = smp.DeepLabV3Plus(
            encoder_name="resnet18",
            encoder_weights=None,
            in_channels=self.front_end.out_channels,
            classes=2,
            encoder_output_stride=16,
            decoder_channels=256,
            decoder_atrous_rates=(12, 24, 36),
            upsampling=4,
        )

    def forward(self, inputs: Tensor) -> dict[str, Tensor]:
        features = self.front_end(inputs)
        logits = self.network(features)
        mask_logits, centerline_logits = logits.split(1, dim=1)
        return {"mask_logits": mask_logits, "centerline_logits": centerline_logits}


def _validate_centerline_auxiliary_output(output_spec: dict[str, object]) -> None:
    auxiliary_outputs = output_spec.get("auxiliary_outputs")
    expected = [{"target": "centerline", "name": "centerline_logits", "shape": [1, 256, 256]}]
    if auxiliary_outputs != expected:
        raise ValueError(
            "abi051_fullspectral_deeplabv3plus_btd_cldice_centerline_aux_v1 requires "
            "exactly one trusted centerline auxiliary output named centerline_logits"
        )


def build_model(input_spec: dict[str, object], output_spec: dict[str, object]) -> nn.Module:
    """Build the model for the Harness-supplied ABI contract."""

    if input_spec.get("mode") != "abi_16ch" or input_spec.get("shape") != [16, 256, 256]:
        raise ValueError(
            "abi051_fullspectral_deeplabv3plus_btd_cldice_centerline_aux_v1 requires "
            "abi_16ch [16, 256, 256] input"
        )
    if output_spec.get("form") != "mask_logits" or output_spec.get("shape") != [1, 256, 256]:
        raise ValueError(
            "abi051_fullspectral_deeplabv3plus_btd_cldice_centerline_aux_v1 requires "
            "mask_logits [1, 256, 256] primary output"
        )
    _validate_centerline_auxiliary_output(output_spec)
    return FullSpectralBTDClDiceCenterlineAuxDeepLabV3Plus()
