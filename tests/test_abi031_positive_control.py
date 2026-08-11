from __future__ import annotations

import ast
from pathlib import Path

import torch

from abi_contrail.research_problem import build_spec
from ml_autoresearch.candidates import validate_candidate_directory
from ml_autoresearch.problem_support.segmentation import bce_dice_loss
from ml_autoresearch.research_problems import ResearchProblemSpecRegistry
from ml_autoresearch.smoke import _import_candidate_model


CANDIDATE = Path("candidates/abi031_mcast11_positive_control_v1")
EXPECTED_PARAMETER_COUNT = 14_328_209


def test_abi031_candidate_contract_and_source_boundary() -> None:
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

    assert manifest.input_mode == "abi_16ch"
    assert manifest.output_form == "mask_logits"
    assert manifest.data.sampling_policy == "combined_source_balanced"
    assert manifest.data.augmentation_policy == "none"
    assert manifest.training.loss == "bce_dice"
    assert manifest.training.optimizer == "adamw"
    assert manifest.training.batch_size == 4
    assert manifest.training.max_epochs == 3
    assert imported_roots == {"__future__", "segmentation_models_pytorch", "torch"}
    for forbidden in ("longitude", "latitude", "baseline", "checkpoint", "torch.load", "open(", "Path("):
        assert forbidden not in source


def test_abi031_candidate_matches_mcast_lineage_and_parameter_budget() -> None:
    module = _import_candidate_model(CANDIDATE)
    model = module.build_model(
        {"mode": "abi_16ch", "shape": [16, 256, 256]},
        {"form": "mask_logits", "shape": [1, 256, 256]},
    )

    assert sum(parameter.numel() for parameter in model.parameters()) == EXPECTED_PARAMETER_COUNT
    assert model.network.encoder._in_channels == 3
    assert model.network.segmentation_head[0].out_channels == 1
    assert model.network.encoder._depth == 5
    torch.testing.assert_close(
        model.channel_means.flatten(),
        torch.tensor([274.15866814464114, 275.74145854126134, 3.05802131633268]),
    )
    torch.testing.assert_close(
        model.channel_stds.flatten(),
        torch.tensor([18.369019656652068, 19.497045505465557, 1.8518705027433054]),
    )


def test_abi031_candidate_zero_and_random_forward_backward_are_finite() -> None:
    module = _import_candidate_model(CANDIDATE)
    model = module.build_model(
        {"mode": "abi_16ch", "shape": [16, 256, 256]},
        {"form": "mask_logits", "shape": [1, 256, 256]},
    )
    model.train()

    for inputs in (torch.zeros(1, 16, 64, 64), torch.randn(1, 16, 64, 64)):
        model.zero_grad(set_to_none=True)
        outputs = model(inputs)
        loss = torch.nn.functional.mse_loss(outputs, torch.zeros_like(outputs))
        loss.backward()

        assert outputs.shape == (1, 1, 64, 64)
        assert torch.isfinite(outputs).all()
        assert torch.isfinite(loss)
        assert all(torch.isfinite(parameter).all() for parameter in model.parameters())
        assert all(
            parameter.grad is None or torch.isfinite(parameter.grad).all()
            for parameter in model.parameters()
        )

    model.eval()
    with torch.no_grad():
        full_size_output = model(torch.zeros(1, 16, 256, 256))
    assert full_size_output.shape == (1, 1, 256, 256)
    assert torch.isfinite(full_size_output).all()


def test_abi031_candidate_tiny_harness_owned_fixture_step_writes_finite_checkpoint(tmp_path: Path) -> None:
    module = _import_candidate_model(CANDIDATE)
    model = module.build_model(
        {"mode": "abi_16ch", "shape": [16, 256, 256]},
        {"form": "mask_logits", "shape": [1, 256, 256]},
    )
    optimizer = torch.optim.AdamW(model.parameters(), lr=0.001)
    inputs = torch.randn(1, 16, 64, 64)
    targets = torch.zeros(1, 1, 64, 64)
    targets[:, :, 28:36, 8:56] = 1.0
    initial_head = model.network.segmentation_head[0].weight.detach().clone()

    optimizer.zero_grad(set_to_none=True)
    logits = model(inputs)
    loss = bce_dice_loss(logits, targets)
    loss.backward()
    optimizer.step()

    assert torch.isfinite(loss)
    assert not torch.equal(initial_head, model.network.segmentation_head[0].weight)
    assert all(torch.isfinite(parameter).all() for parameter in model.parameters())
    checkpoint_path = tmp_path / "fixture_checkpoint.pt"
    torch.save({"model_state_dict": model.state_dict()}, checkpoint_path)
    checkpoint = torch.load(checkpoint_path, map_location="cpu", weights_only=True)
    assert all(torch.isfinite(value).all() for value in checkpoint["model_state_dict"].values())
