"""Full-spectral DeepLabV3+ representative scout for ABI contrail segmentation."""

from __future__ import annotations

import segmentation_models_pytorch as smp
import torch
from torch import Tensor, nn


class FullSpectralDeepLabV3Plus(nn.Module):
    """Normalize all approved ABI channels and predict one Contrail Mask logit plane."""

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

    def __init__(self) -> None:
        super().__init__()
        self.register_buffer(
            "channel_means",
            torch.tensor(self._CHANNEL_MEANS, dtype=torch.float32).view(1, 16, 1, 1),
        )
        self.register_buffer(
            "channel_scales",
            torch.tensor(self._CHANNEL_SCALES, dtype=torch.float32).view(1, 16, 1, 1),
        )
        self.network = smp.DeepLabV3Plus(
            encoder_name="resnet18",
            encoder_weights=None,
            in_channels=16,
            classes=1,
            encoder_output_stride=16,
            decoder_channels=256,
            decoder_atrous_rates=(12, 24, 36),
            upsampling=4,
        )

    def forward(self, inputs: Tensor) -> Tensor:
        normalized = (inputs - self.channel_means) / self.channel_scales
        return self.network(normalized)


def build_model(input_spec: dict[str, object], output_spec: dict[str, object]) -> nn.Module:
    """Build the model for the Harness-supplied ABI contract."""

    if input_spec.get("mode") != "abi_16ch" or input_spec.get("shape") != [16, 256, 256]:
        raise ValueError(
            "abi044_fullspectral_deeplabv3plus_representative_scout_v1 requires "
            "abi_16ch [16, 256, 256] input"
        )
    if output_spec.get("form") != "mask_logits" or output_spec.get("shape") != [1, 256, 256]:
        raise ValueError(
            "abi044_fullspectral_deeplabv3plus_representative_scout_v1 requires "
            "mask_logits [1, 256, 256] output"
        )
    return FullSpectralDeepLabV3Plus()
