"""Prepare the reviewed two-Run ABI-029 Experiment Batch concurrency canary.

This static preparation copies a reviewed model architecture and never imports
Candidate code, accesses data, selects a GPU, or starts execution.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from pathlib import Path

import yaml

DEFAULT_BATCH_SIZE = 8
DEFAULT_CANDIDATE_COUNT = 2
PROFILE_MAX_SAMPLES_PER_SOURCE = 32
PROFILE_MAX_EPOCHS = 1


def prepare_concurrency_canary(
    source: Path,
    output: Path,
    *,
    batch_size: int = DEFAULT_BATCH_SIZE,
    candidate_count: int = DEFAULT_CANDIDATE_COUNT,
) -> dict[str, object]:
    source = source.resolve(strict=True)
    if output.exists():
        raise ValueError(f"output directory already exists: {output}")
    if batch_size < 1:
        raise ValueError("batch size must be positive")
    if candidate_count < 2 or candidate_count > 4:
        raise ValueError("candidate count must be between 2 and 4")
    for name in ("manifest.yaml", "model.py"):
        if not (source / name).is_file():
            raise ValueError(f"source Candidate is missing {name}")

    source_manifest = yaml.safe_load((source / "manifest.yaml").read_text())
    if not isinstance(source_manifest, dict) or not isinstance(source_manifest.get("training"), dict):
        raise ValueError("source manifest must contain a training mapping")
    source_id = str(source_manifest.get("name") or source.name)
    model_sha256 = hashlib.sha256((source / "model.py").read_bytes()).hexdigest()

    candidates_root = output / "candidates"
    candidates_root.mkdir(parents=True)
    records: list[dict[str, object]] = []
    for index in range(candidate_count):
        label = chr(ord("a") + index)
        candidate_id = f"{source_id}_concurrency_{label}"
        destination = candidates_root / candidate_id
        destination.mkdir()
        shutil.copy2(source / "model.py", destination / "model.py")
        manifest = dict(source_manifest)
        manifest["name"] = candidate_id
        manifest["description"] = (
            f"ABI-029 concurrency canary replica {label.upper()} of {source_id} at batch size {batch_size}."
        )
        training = dict(source_manifest["training"])
        training["batch_size"] = batch_size
        training["max_epochs"] = PROFILE_MAX_EPOCHS
        manifest["training"] = training
        (destination / "manifest.yaml").write_text(yaml.safe_dump(manifest, sort_keys=False))
        (destination / "README.md").write_text(
            f"# {candidate_id}\n\n"
            f"Operator-authored ABI-029 concurrency canary replica of `{source_id}`. "
            "The model source is byte-for-byte identical. Candidate code does not own concurrency, GPU placement, resource measurement, or retry.\n"
        )
        records.append(
            {
                "candidate_id": candidate_id,
                "batch_size": batch_size,
                "max_epochs": PROFILE_MAX_EPOCHS,
                "model_sha256": model_sha256,
                "path": str(destination),
            }
        )

    (output / "BATCH_PROPOSAL.md").write_text(
        "# ABI-029 two-Run concurrency canary\n\n"
        "## Shared hypothesis\n\nTwo identical, independently initialized replicas of the profiled spectral residual U-Net can train concurrently on the pinned A100 without Resource Failure, artifact collision, or unacceptable throughput contention.\n\n"
        "## Shared comparison target\n\nCompare each concurrent Run with the isolated batch-size-8 profile `run_20260810_195845_df2123`; scientific metric ordering is out of scope.\n\n"
        "## Per-candidate variant rationale\n\nReplicas A and B intentionally have byte-identical model source and training policy so observed differences measure concurrent execution effects rather than architecture changes.\n\n"
        "## Expected ordering or decision criteria\n\nBoth Runs should complete independently with similar memory envelopes. Aggregate throughput should be at least 1.5 times isolated throughput, aggregate GPU memory must remain within the reviewed headroom, and neither Run may use Resource Failure retry.\n\n"
        "## Batch-level success criteria\n\nThe Harness enforces concurrency two, creates isolated Run/artifact records, preserves independent failure handling, records two resource profiles, and leaves at least 8 GiB and 30% A100 memory headroom.\n\n"
        f"## Requested budget/concurrency\n\nExactly {candidate_count} Runs, concurrency {candidate_count}, batch size {batch_size}, one epoch, at most {PROFILE_MAX_SAMPLES_PER_SOURCE} training and validation samples per Dataset Source, two qualitative samples per Run, no Post-Run Evaluation, and no automatic follow-up.\n"
    )

    plan = {
        "schema_version": "abi_gpu_concurrency_canary.v1",
        "source_candidate": str(source),
        "source_candidate_id": source_id,
        "source_model_sha256": model_sha256,
        "batch_size": batch_size,
        "candidate_count": candidate_count,
        "max_parallel_runs": candidate_count,
        "max_samples_per_source": PROFILE_MAX_SAMPLES_PER_SOURCE,
        "max_epochs": PROFILE_MAX_EPOCHS,
        "candidates": records,
    }
    (output / "CONCURRENCY_PLAN.json").write_text(json.dumps(plan, indent=2, sort_keys=True) + "\n")
    return plan


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True, help="Reviewed source Candidate directory")
    parser.add_argument("--output", type=Path, required=True, help="New Experiment Batch directory")
    parser.add_argument("--batch-size", type=int, default=DEFAULT_BATCH_SIZE)
    parser.add_argument("--candidate-count", type=int, default=DEFAULT_CANDIDATE_COUNT)
    args = parser.parse_args()
    plan = prepare_concurrency_canary(
        args.source,
        args.output,
        batch_size=args.batch_size,
        candidate_count=args.candidate_count,
    )
    print(json.dumps(plan, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
