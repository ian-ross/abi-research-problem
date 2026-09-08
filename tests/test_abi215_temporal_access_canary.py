from __future__ import annotations

import ast
from pathlib import Path

import torch

from abi_contrail.research_problem import build_spec
from ml_autoresearch.candidates import validate_candidate_directory
from ml_autoresearch.problem_support.segmentation import bce_dice_loss
from ml_autoresearch.research_problems import ResearchProblemSpecRegistry
from ml_autoresearch.smoke import _import_candidate_model


CANDIDATE = Path("candidates/abi215_temporal_access_canary_v1")
EXPECTED_PARAMETER_COUNT = 18_321


def _temporal_input_spec() -> dict[str, object]:
    spec = build_spec()
    return spec.build_input_spec(
        {
            "input_mode": "abi_16ch_plus_sza_temporal",
            "output_form": "mask_logits",
            "data": {"temporal_frame_offsets": [-1, 0, 1]},
        }
    )


def test_abi215_candidate_contract_uses_provider_temporal_offsets() -> None:
    spec = build_spec()
    registry = ResearchProblemSpecRegistry((spec,), active_id=spec.id)

    manifest = validate_candidate_directory(
        CANDIDATE,
        require_proposal=True,
        require_readme=True,
        research_problem_registry=registry,
    )
    source = (CANDIDATE / "model.py").read_text()
    tree = ast.parse(source)
    imported_roots = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported_roots.update(alias.name.split(".", 1)[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module is not None:
            imported_roots.add(node.module.split(".", 1)[0])

    assert manifest.input_mode == "abi_16ch_plus_sza_temporal"
    assert manifest.output_form == "mask_logits"
    assert manifest.data.frame_selection_policy == "temporal_eligible_center"
    assert manifest.data.temporal_frame_offsets == [-1, 0, 1]
    assert manifest.data.sampling_policy == "sequential"
    assert manifest.data.augmentation_policy == "none"
    assert manifest.training.loss == "bce_dice"
    assert manifest.training.optimizer == "adamw"
    assert manifest.training.batch_size == 2
    assert manifest.training.max_epochs == 1
    assert imported_roots == {"__future__", "torch"}
    for forbidden in ("open(", "Path(", "np.", "numpy", "pandas", "xarray", "s3", "httpx", "requests", "boto"):
        assert forbidden not in source


def test_abi215_input_spec_resolves_to_three_abi_sza_frames() -> None:
    input_spec = _temporal_input_spec()

    assert input_spec["mode"] == "abi_16ch_plus_sza_temporal"
    assert input_spec["shape"] == [51, 256, 256]
    assert input_spec["layout"] == "channel_stacked_temporal_frames"
    assert input_spec["base_channels_per_frame"] == 17
    assert input_spec["frame_count"] == 3
    assert input_spec["temporal_frame_offsets"] == [-1, 0, 1]
    assert input_spec["target_frame_index"] == 1
    assert input_spec["target_channel_start"] == 17
    assert input_spec["source_channel_indices_per_frame"] == list(range(16)) + [18]


def test_abi215_builds_small_finite_model_sensitive_to_nonzero_offsets() -> None:
    module = _import_candidate_model(CANDIDATE)
    model = module.build_model(
        _temporal_input_spec(),
        {"form": "mask_logits", "shape": [1, 256, 256]},
    )
    model.eval()

    assert sum(parameter.numel() for parameter in model.parameters()) == EXPECTED_PARAMETER_COUNT
    assert model.front_end.out_channels == 119

    for parameter in model.parameters():
        torch.nn.init.constant_(parameter, 0.01)

    inputs = torch.zeros(1, 51, 16, 16)
    frames = inputs.reshape(1, 3, 17, 16, 16)
    frames[:, :, :16, :, :] = model.front_end.abi_means
    frames[:, :, 16:17, :, :] = 90.0

    with torch.no_grad():
        baseline = model(inputs)
        previous_changed = inputs.clone()
        previous_changed[:, 0, :, :] += 0.25
        previous_output = model(previous_changed)
        next_changed = inputs.clone()
        next_changed[:, 34, :, :] += 0.25
        next_output = model(next_changed)

    assert baseline.shape == (1, 1, 16, 16)
    assert torch.isfinite(baseline).all()
    assert torch.isfinite(previous_output).all()
    assert torch.isfinite(next_output).all()
    assert not torch.allclose(previous_output, baseline)
    assert not torch.allclose(next_output, baseline)


def test_abi215_tiny_harness_owned_fixture_step_is_finite() -> None:
    module = _import_candidate_model(CANDIDATE)
    model = module.build_model(
        _temporal_input_spec(),
        {"form": "mask_logits", "shape": [1, 256, 256]},
    )
    model.train()
    optimizer = torch.optim.AdamW(model.parameters(), lr=0.001)
    inputs = torch.randn(1, 51, 32, 32)
    inputs[:, 16:17, :, :] = 90.0
    inputs[:, 33:34, :, :] = 90.0
    inputs[:, 50:51, :, :] = 90.0
    targets = torch.zeros(1, 1, 32, 32)
    targets[:, :, 14:18, 6:26] = 1.0

    optimizer.zero_grad(set_to_none=True)
    logits = model(inputs)
    loss = bce_dice_loss(logits, targets)
    loss.backward()
    optimizer.step()

    assert logits.shape == (1, 1, 32, 32)
    assert torch.isfinite(logits).all()
    assert torch.isfinite(loss)
    assert all(torch.isfinite(parameter).all() for parameter in model.parameters())
    assert all(parameter.grad is None or torch.isfinite(parameter.grad).all() for parameter in model.parameters())
