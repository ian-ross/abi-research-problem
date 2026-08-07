from __future__ import annotations

from torch import nn


class TinyABISmokeModel(nn.Module):
    def __init__(self, input_channels: int) -> None:
        super().__init__()
        self.mask = nn.Conv2d(input_channels, 1, kernel_size=1)

    def forward(self, inputs):
        return {"mask_logits": self.mask(inputs)}


def build_model(input_spec: dict, output_spec: dict):
    return TinyABISmokeModel(int(input_spec["shape"][0]))
