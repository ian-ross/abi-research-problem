"""Minimal temporal ABI+SZA access canary for provider-owned ±1 frame patches."""

from __future__ import annotations

import torch
from torch import Tensor, nn


CANDIDATE_ID = "abi215_temporal_access_canary_v1"
TEMPORAL_OFFSETS = [-1, 0, 1]
CHANNELS_PER_FRAME = 17
FRAME_COUNT = 3
INPUT_CHANNELS = CHANNELS_PER_FRAME * FRAME_COUNT


class TemporalAccessFrontEnd(nn.Module):
    """Split the channel-stacked temporal tensor and expose all three frames to the head."""

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

    def __init__(self) -> None:
        super().__init__()
        self.register_buffer("abi_means", torch.tensor(self._ABI_MEANS, dtype=torch.float32).view(1, 1, 16, 1, 1))
        self.register_buffer("abi_scales", torch.tensor(self._ABI_SCALES, dtype=torch.float32).view(1, 1, 16, 1, 1))
        self.out_channels = CHANNELS_PER_FRAME * 7

    def forward(self, inputs: Tensor) -> Tensor:
        if inputs.ndim != 4 or inputs.shape[1] != INPUT_CHANNELS:
            raise ValueError(f"expected [N, {INPUT_CHANNELS}, H, W] temporal ABI+SZA tensor, got {tuple(inputs.shape)}")
        batch, _, height, width = inputs.shape
        frames = inputs.reshape(batch, FRAME_COUNT, CHANNELS_PER_FRAME, height, width)
        abi = frames[:, :, :16, :, :]
        sza = frames[:, :, 16:17, :, :]
        normalized_abi = (abi - self.abi_means) / self.abi_scales
        sza_scaled = (torch.clamp(sza, 0.0, 180.0) - 90.0) / 90.0
        normalized_frames = torch.cat((normalized_abi, sza_scaled), dim=2)

        previous_frame = normalized_frames[:, 0, :, :, :]
        center_frame = normalized_frames[:, 1, :, :, :]
        next_frame = normalized_frames[:, 2, :, :, :]
        temporal_mean = normalized_frames.mean(dim=1)
        previous_to_center = center_frame - previous_frame
        center_to_next = next_frame - center_frame
        next_minus_previous = next_frame - previous_frame
        return torch.cat(
            (
                previous_frame,
                center_frame,
                next_frame,
                temporal_mean,
                previous_to_center,
                center_to_next,
                next_minus_previous,
            ),
            dim=1,
        )


class ABI215TemporalAccessCanary(nn.Module):
    """Tiny fully convolutional model that necessarily reads the -1, 0, and +1 frames."""

    def __init__(self) -> None:
        super().__init__()
        self.front_end = TemporalAccessFrontEnd()
        self.network = nn.Sequential(
            nn.Conv2d(self.front_end.out_channels, 16, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.Conv2d(16, 8, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.Conv2d(8, 1, kernel_size=1),
        )

    def forward(self, inputs: Tensor) -> Tensor:
        return self.network(self.front_end(inputs))


def build_model(input_spec, output_spec):
    """Build the temporal access canary for the Harness-supplied ABI contract."""

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
    if output_spec.get("form") != "mask_logits":
        raise ValueError(f"{CANDIDATE_ID} produces mask_logits output")
    if output_spec.get("shape") != [1, 256, 256]:
        raise ValueError(f"{CANDIDATE_ID} requires [1, 256, 256] output")
    return ABI215TemporalAccessCanary()
