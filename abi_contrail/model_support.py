"""Reusable model-support utilities for ABI candidate architectures.

These modules are intentionally small front ends that candidate ``model.py``
files may import and compose. They do not own data loading, losses, metrics,
sampling, or channel-selection policy; those remain provider/harness concerns.
"""

from __future__ import annotations

from collections.abc import Sequence

try:
    import torch
    from torch import Tensor, nn
except ImportError as exc:  # pragma: no cover - exercised only without torch installed.
    raise ImportError(
        "abi_contrail.model_support requires torch; install the project's torch dependency group "
        "or run candidate training in an environment with PyTorch available."
    ) from exc


class Conv1x1ChannelMixer(nn.Module):
    """Learn a per-pixel linear mixture across input channels.

    Parameters
    ----------
    in_channels:
        Number of channels expected in the input tensor.
    out_channels:
        Number of learned mixed channels to emit.
    bias:
        Passed through to :class:`torch.nn.Conv2d`.
    activation:
        Optional module applied after the 1x1 convolution.

    Notes
    -----
    Accepts either ``[C, H, W]`` or ``[N, C, H, W]`` tensors and preserves the
    input rank. The module never selects provider source channels; it only mixes
    the already-approved candidate input tensor supplied by the harness.
    """

    def __init__(
        self,
        in_channels: int,
        out_channels: int,
        *,
        bias: bool = True,
        activation: nn.Module | None = None,
    ) -> None:
        super().__init__()
        self.in_channels = _positive_int(in_channels, "in_channels")
        self.out_channels = _positive_int(out_channels, "out_channels")
        self.projection = nn.Conv2d(self.in_channels, self.out_channels, kernel_size=1, bias=bias)
        self.activation = activation if activation is not None else nn.Identity()

    def forward(self, inputs: Tensor) -> Tensor:
        batched, restore_unbatched = _as_batched_channel_first(inputs, self.in_channels)
        mixed = self.activation(self.projection(batched))
        return mixed.squeeze(0) if restore_unbatched else mixed


class RawPlusLearnedChannelMixer(nn.Module):
    """Concatenate explicit physics-inspired features with learned 1x1 mixes.

    This is useful when a candidate wants to preserve physically interpretable
    features alongside a compact learned front end. The explicit side can include
    individual raw input channels and, more commonly for ABI contrail work,
    brightness-temperature differences such as ``channel_a - channel_b``.

    Parameters
    ----------
    in_channels:
        Number of channels expected in the input tensor.
    learned_channels:
        Number of learned 1x1 projection channels to concatenate.
    raw_channel_indices:
        Optional individual candidate-input channel positions to preserve.
    difference_channel_pairs:
        Optional ``(minuend_index, subtrahend_index)`` pairs. Each pair emits one
        explicit difference feature computed as ``inputs[minuend] - inputs[subtrahend]``.

    Notes
    -----
    The output channel count is ``len(raw_channel_indices) + len(difference_channel_pairs) + learned_channels``.
    All indices are positions in the already-selected candidate input tensor, not
    provider source-file indices. Candidate code chooses whether these positions
    correspond to brightness-temperature bands for its selected input mode.
    """

    def __init__(
        self,
        in_channels: int,
        learned_channels: int,
        raw_channel_indices: Sequence[int] = (),
        *,
        difference_channel_pairs: Sequence[tuple[int, int]] = (),
        bias: bool = True,
        activation: nn.Module | None = None,
    ) -> None:
        super().__init__()
        self.in_channels = _positive_int(in_channels, "in_channels")
        self.learned_channels = _positive_int(learned_channels, "learned_channels")
        self.raw_channel_indices = _validate_channel_indices(
            raw_channel_indices,
            in_channels=self.in_channels,
            name="raw_channel_indices",
        )
        self.difference_channel_pairs = _validate_channel_pairs(
            difference_channel_pairs,
            in_channels=self.in_channels,
            name="difference_channel_pairs",
        )
        self.learned_mixer = Conv1x1ChannelMixer(
            self.in_channels,
            self.learned_channels,
            bias=bias,
            activation=activation,
        )
        self.out_channels = len(self.raw_channel_indices) + len(self.difference_channel_pairs) + self.learned_channels

    def forward(self, inputs: Tensor) -> Tensor:
        batched, restore_unbatched = _as_batched_channel_first(inputs, self.in_channels)
        explicit_features: list[Tensor] = []
        if self.raw_channel_indices:
            explicit_features.append(batched[:, self.raw_channel_indices, :, :])
        for minuend_index, subtrahend_index in self.difference_channel_pairs:
            explicit_features.append(
                batched[:, minuend_index : minuend_index + 1, :, :]
                - batched[:, subtrahend_index : subtrahend_index + 1, :, :]
            )
        learned = self.learned_mixer(batched)
        mixed = torch.cat((*explicit_features, learned), dim=1) if explicit_features else learned
        return mixed.squeeze(0) if restore_unbatched else mixed


def _positive_int(value: int, name: str) -> int:
    value = int(value)
    if value <= 0:
        raise ValueError(f"{name} must be positive, got {value}")
    return value


def _validate_channel_indices(indices: Sequence[int], *, in_channels: int, name: str) -> tuple[int, ...]:
    validated = tuple(int(index) for index in indices)
    if len(set(validated)) != len(validated):
        raise ValueError(f"{name} must be unique, got {validated}")
    invalid = [index for index in validated if index < 0 or index >= in_channels]
    if invalid:
        raise ValueError(f"{name} must be in [0, {in_channels - 1}], got invalid indices {invalid}")
    return validated


def _validate_channel_pairs(
    pairs: Sequence[tuple[int, int]],
    *,
    in_channels: int,
    name: str,
) -> tuple[tuple[int, int], ...]:
    validated = tuple((int(minuend), int(subtrahend)) for minuend, subtrahend in pairs)
    invalid = [index for pair in validated for index in pair if index < 0 or index >= in_channels]
    if invalid:
        raise ValueError(f"{name} indices must be in [0, {in_channels - 1}], got invalid indices {invalid}")
    repeated = [pair for pair in validated if pair[0] == pair[1]]
    if repeated:
        raise ValueError(f"{name} entries must compare two different channels, got {repeated}")
    return validated


def _as_batched_channel_first(inputs: Tensor, expected_channels: int) -> tuple[Tensor, bool]:
    if inputs.ndim == 3:
        if inputs.shape[0] != expected_channels:
            raise ValueError(f"expected {expected_channels} input channels, got tensor shape {tuple(inputs.shape)}")
        return inputs.unsqueeze(0), True
    if inputs.ndim == 4:
        if inputs.shape[1] != expected_channels:
            raise ValueError(f"expected {expected_channels} input channels, got tensor shape {tuple(inputs.shape)}")
        return inputs, False
    raise ValueError(f"expected [C, H, W] or [N, C, H, W] input tensor, got shape {tuple(inputs.shape)}")


__all__ = ["Conv1x1ChannelMixer", "RawPlusLearnedChannelMixer"]
