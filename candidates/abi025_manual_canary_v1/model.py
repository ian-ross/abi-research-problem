"""Minimal architecture-only Candidate Execution lifecycle canary."""

import torch
from torch import nn


class ABI025CanaryModel(nn.Module):
    """Small fully convolutional model for ABI Patch mask logits."""

    def __init__(self) -> None:
        super().__init__()
        self.network = nn.Sequential(
            nn.Conv2d(16, 8, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.Conv2d(8, 1, kernel_size=1),
        )

    def forward(self, inputs: torch.Tensor) -> torch.Tensor:
        return self.network(inputs)


def build_model(input_spec, output_spec):
    """Build the canary model for the Harness-supplied ABI contract."""

    if input_spec.get("mode") != "abi_16ch":
        raise ValueError("abi025_manual_canary_v1 requires abi_16ch input")
    if input_spec.get("shape") != [16, 256, 256]:
        raise ValueError("abi025_manual_canary_v1 requires [16, 256, 256] input")
    if output_spec.get("form") != "mask_logits":
        raise ValueError("abi025_manual_canary_v1 produces mask_logits output")
    if output_spec.get("shape") != [1, 256, 256]:
        raise ValueError("abi025_manual_canary_v1 requires [1, 256, 256] output")
    return ABI025CanaryModel()
