"""MCAST 1.1-lineage model for a controlled BCE-Dice-clDice continuation."""

from __future__ import annotations

import segmentation_models_pytorch as smp
import torch
from torch import Tensor, nn


class MCAST11BCEDiceClDiceModel(nn.Module):
    """Derive the fixed MCAST 1.1 planes and emit contrail-mask logits."""

    _MEANS = (274.15866814464114, 275.74145854126134, 3.05802131633268)
    _STDS = (18.369019656652068, 19.497045505465557, 1.8518705027433054)

    def __init__(self) -> None:
        super().__init__()
        self.register_buffer(
            "channel_means",
            torch.tensor(self._MEANS, dtype=torch.float32).view(1, 3, 1, 1),
        )
        self.register_buffer(
            "channel_stds",
            torch.tensor(self._STDS, dtype=torch.float32).view(1, 3, 1, 1),
        )
        self.network = smp.Unet(
            encoder_name="resnet18",
            encoder_weights=None,
            in_channels=3,
            classes=1,
        )

    def forward(self, inputs: Tensor) -> Tensor:
        c11 = inputs[:, 10:11]
        c14 = inputs[:, 13:14]
        c13_minus_c15 = inputs[:, 12:13] - inputs[:, 14:15]
        mcast_planes = torch.cat((c11, c14, c13_minus_c15), dim=1)
        normalized = (mcast_planes - self.channel_means) / self.channel_stds
        return self.network(normalized)


def build_model(input_spec: dict[str, object], output_spec: dict[str, object]) -> nn.Module:
    """Build the model for the Harness-supplied ABI contract."""

    if input_spec.get("mode") != "abi_16ch" or input_spec.get("shape") != [16, 256, 256]:
        raise ValueError("abi037_mcast11_bce_dice_cldice_v1 requires abi_16ch [16, 256, 256] input")
    if output_spec.get("form") != "mask_logits" or output_spec.get("shape") != [1, 256, 256]:
        raise ValueError("abi037_mcast11_bce_dice_cldice_v1 requires mask_logits [1, 256, 256] output")
    return MCAST11BCEDiceClDiceModel()
