import importlib.util
from pathlib import Path

import pytest


torch = pytest.importorskip("torch")

from abi_contrail.model_support import Conv1x1ChannelMixer, RawPlusLearnedChannelMixer


def test_conv1x1_channel_mixer_preserves_spatial_shape_for_batched_input() -> None:
    mixer = Conv1x1ChannelMixer(in_channels=16, out_channels=6)

    output = mixer(torch.zeros(2, 16, 8, 9))

    assert output.shape == (2, 6, 8, 9)


def test_conv1x1_channel_mixer_preserves_unbatched_rank() -> None:
    mixer = Conv1x1ChannelMixer(in_channels=10, out_channels=4)

    output = mixer(torch.zeros(10, 5, 6))

    assert output.shape == (4, 5, 6)


def test_raw_plus_learned_channel_mixer_concatenates_explicit_features_first() -> None:
    mixer = RawPlusLearnedChannelMixer(
        in_channels=4,
        learned_channels=2,
        raw_channel_indices=(1,),
        difference_channel_pairs=((3, 2), (2, 0)),
    )
    inputs = torch.arange(4 * 3 * 2, dtype=torch.float32).reshape(1, 4, 3, 2)

    output = mixer(inputs)

    assert output.shape == (1, 5, 3, 2)
    torch.testing.assert_close(output[:, 0], inputs[:, 1])
    torch.testing.assert_close(output[:, 1], inputs[:, 3] - inputs[:, 2])
    torch.testing.assert_close(output[:, 2], inputs[:, 2] - inputs[:, 0])


def test_raw_plus_learned_channel_mixer_rejects_invalid_explicit_feature_indices() -> None:
    with pytest.raises(ValueError, match="invalid indices"):
        RawPlusLearnedChannelMixer(in_channels=3, learned_channels=2, raw_channel_indices=(0, 3))

    with pytest.raises(ValueError, match="unique"):
        RawPlusLearnedChannelMixer(in_channels=3, learned_channels=2, raw_channel_indices=(1, 1))

    with pytest.raises(ValueError, match="invalid indices"):
        RawPlusLearnedChannelMixer(in_channels=3, learned_channels=2, difference_channel_pairs=((2, 3),))

    with pytest.raises(ValueError, match="different channels"):
        RawPlusLearnedChannelMixer(in_channels=3, learned_channels=2, difference_channel_pairs=((2, 2),))


def test_candidate_model_py_can_import_and_use_mixer_utilities(tmp_path: Path) -> None:
    candidate_path = tmp_path / "model.py"
    candidate_path.write_text(
        "import torch\n"
        "from abi_contrail.model_support import RawPlusLearnedChannelMixer\n\n"
        "class Model(torch.nn.Module):\n"
        "    def __init__(self):\n"
        "        super().__init__()\n"
        "        self.front_end = RawPlusLearnedChannelMixer(\n"
        "            16, learned_channels=3, raw_channel_indices=(13,), difference_channel_pairs=((13, 14), (14, 15))\n"
        "        )\n\n"
        "    def forward(self, x):\n"
        "        return self.front_end(x)\n"
    )
    spec = importlib.util.spec_from_file_location("candidate_model", candidate_path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    output = module.Model()(torch.zeros(1, 16, 4, 4))

    assert output.shape == (1, 6, 4, 4)
