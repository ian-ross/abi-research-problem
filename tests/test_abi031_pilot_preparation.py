from pathlib import Path

import yaml

from scripts.prepare_abi031_positive_control_pilot import PILOT_ID, prepare_pilot


SOURCE = Path("candidates/abi031_mcast11_positive_control_v1")


def test_prepare_abi031_pilot_changes_only_identity_description_and_epoch_bound(tmp_path: Path) -> None:
    output = tmp_path / PILOT_ID

    plan = prepare_pilot(SOURCE, output)

    source_manifest = yaml.safe_load((SOURCE / "manifest.yaml").read_text())
    pilot_manifest = yaml.safe_load((output / "manifest.yaml").read_text())
    assert pilot_manifest.pop("name") == PILOT_ID
    assert pilot_manifest.pop("description").startswith("ABI-031 one-epoch")
    source_manifest.pop("name")
    source_manifest.pop("description")
    assert pilot_manifest["training"].pop("max_epochs") == 1
    assert source_manifest["training"].pop("max_epochs") == 3
    assert pilot_manifest == source_manifest
    assert (output / "model.py").read_bytes() == (SOURCE / "model.py").read_bytes()
    assert sorted(path.name for path in output.iterdir()) == [
        "PROPOSAL.md",
        "README.md",
        "manifest.yaml",
        "model.py",
    ]
    assert plan["model_source_identical"] is True
    assert plan["max_samples_per_source"] == 32
    assert plan["max_prediction_samples"] == 4
    assert plan["sequential_only"] is True
    assert Path(plan["plan_path"]).is_file()
