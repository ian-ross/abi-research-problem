"""Prepare the reviewed one-epoch ABI-031 resource-pilot derivative."""

from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path

import yaml

PILOT_ID = "abi031_mcast11_positive_control_pilot_1epoch"


def prepare_pilot(source: Path, output: Path) -> dict[str, object]:
    source = source.resolve()
    output = output.resolve()
    if not source.is_dir():
        raise ValueError(f"source Candidate does not exist: {source}")
    if output.exists():
        raise ValueError(f"pilot output already exists: {output}")

    shutil.copytree(source, output)
    manifest_path = output / "manifest.yaml"
    manifest = yaml.safe_load(manifest_path.read_text())
    if not isinstance(manifest, dict) or not isinstance(manifest.get("training"), dict):
        raise ValueError("source manifest must contain a training mapping")
    manifest["name"] = PILOT_ID
    manifest["description"] = "ABI-031 one-epoch resource-pilot derivative of the reviewed positive control."
    manifest["training"]["max_epochs"] = 1
    manifest_path.write_text(yaml.safe_dump(manifest, sort_keys=False))

    plan = {
        "candidate_id": PILOT_ID,
        "source": str(source),
        "output": str(output),
        "model_source_identical": (source / "model.py").read_bytes() == (output / "model.py").read_bytes(),
        "batch_size": int(manifest["training"]["batch_size"]),
        "max_epochs": 1,
        "max_samples_per_source": 32,
        "max_prediction_samples": 4,
        "sequential_only": True,
    }
    plan_path = output.parent / f"{output.name}-plan.json"
    plan_path.write_text(json.dumps(plan, indent=2, sort_keys=True) + "\n")
    return {**plan, "plan_path": str(plan_path)}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(prepare_pilot(args.source, args.output), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
