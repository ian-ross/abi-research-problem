"""Prepare operator-authored ABI-029 batch-size profiling Candidate derivatives.

This script copies only the reviewed model architecture and writes one-epoch
manifests/proposals. It never imports Candidate code, reads training data, or
starts Candidate execution.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from pathlib import Path

import yaml

DEFAULT_BATCH_SIZES = (1, 2, 4, 8, 16)
PROFILE_MAX_SAMPLES_PER_SOURCE = 32
PROFILE_MAX_EPOCHS = 1


def prepare_profiles(source: Path, output: Path, batch_sizes: tuple[int, ...] = DEFAULT_BATCH_SIZES) -> dict[str, object]:
    source = source.resolve(strict=True)
    required = ("manifest.yaml", "model.py", "PROPOSAL.md", "README.md")
    missing = [name for name in required if not (source / name).is_file()]
    if missing:
        raise ValueError(f"source Candidate is missing required files: {', '.join(missing)}")
    if output.exists():
        raise ValueError(f"output directory already exists: {output}")
    if not batch_sizes or any(size < 1 for size in batch_sizes) or len(set(batch_sizes)) != len(batch_sizes):
        raise ValueError("batch sizes must be unique positive integers")

    source_manifest = yaml.safe_load((source / "manifest.yaml").read_text())
    if not isinstance(source_manifest, dict) or not isinstance(source_manifest.get("training"), dict):
        raise ValueError("source manifest must contain a training mapping")
    source_id = str(source_manifest.get("name") or source.name)
    model_sha256 = hashlib.sha256((source / "model.py").read_bytes()).hexdigest()

    output.mkdir(parents=True)
    candidate_records: list[dict[str, object]] = []
    for batch_size in batch_sizes:
        candidate_id = f"{source_id}_profile_bs{batch_size}"
        destination = output / candidate_id
        destination.mkdir()
        shutil.copy2(source / "model.py", destination / "model.py")

        manifest = dict(source_manifest)
        manifest["name"] = candidate_id
        manifest["description"] = (
            f"ABI-029 one-epoch GPU resource profile derivative of {source_id} at batch size {batch_size}."
        )
        training = dict(source_manifest["training"])
        training["batch_size"] = batch_size
        training["max_epochs"] = PROFILE_MAX_EPOCHS
        manifest["training"] = training
        (destination / "manifest.yaml").write_text(yaml.safe_dump(manifest, sort_keys=False))
        (destination / "README.md").write_text(
            f"# {candidate_id}\n\n"
            f"Operator-authored ABI-029 resource profiling derivative of `{source_id}`. "
            "The model source is copied byte-for-byte; only manifest name, description, batch size, and the one-epoch profiling bound differ. "
            "Harness execution must additionally pass the reviewed 32-samples-per-Dataset-Source cap. "
            "This profile is not a scientific promotion candidate.\n"
        )
        (destination / "PROPOSAL.md").write_text(
            f"# ABI-029 GPU profile: {source_id}, batch size {batch_size}\n\n"
            "## Classification\n\nOperator resource profile; not a scientific Candidate comparison or promotion request.\n\n"
            "## Hypothesis\n\nThe reviewed high-resolution residual scout can complete one training epoch at this batch size within the pinned A100 resource envelope.\n\n"
            f"## Comparison Target\n\nCompare only with the other ABI-029 batch-size profiles derived from `{source_id}`; scientific quality comparisons are out of scope.\n\n"
            "## Expected Effect\n\nIncreasing batch size should increase peak allocated/reserved CUDA memory and may improve throughput until memory or input-pipeline limits dominate.\n\n"
            f"## Implementation Sketch\n\nKeep `model.py` byte-for-byte identical to `{source_id}` and change only manifest identity, batch size `{batch_size}`, and the one-epoch bound.\n\n"
            "## Contract Features Used\n\nUse the source Candidate input/output contract and trusted provider-owned sampling, augmentation, loss, metrics, filters, and execution. No Candidate-owned resource policy is added.\n\n"
            f"## Budget Requested\n\nOne epoch, at most {PROFILE_MAX_SAMPLES_PER_SOURCE} training and validation samples per Dataset Source, two qualitative samples, no Post-Run Evaluation, and no automatic follow-up.\n\n"
            "## Success Criteria\n\nRecord controlled smoke outcome, peak allocated/reserved GPU memory, throughput, wall time, requested/effective batch size, and any Resource Failure retry without changing model source.\n\n"
            "## Fallback Next Decision\n\nStop the increasing batch-size sweep after the first GPU OOM. Use the largest successful size satisfying the reviewed headroom policy for a bounded confirmation Run; otherwise keep the architecture sequential.\n"
        )
        candidate_records.append(
            {
                "candidate_id": candidate_id,
                "batch_size": batch_size,
                "max_epochs": PROFILE_MAX_EPOCHS,
                "model_sha256": model_sha256,
                "path": str(destination),
            }
        )

    plan = {
        "schema_version": "abi_gpu_profile_plan.v1",
        "source_candidate": str(source),
        "source_candidate_id": source_id,
        "source_model_sha256": model_sha256,
        "max_samples_per_source": PROFILE_MAX_SAMPLES_PER_SOURCE,
        "max_epochs": PROFILE_MAX_EPOCHS,
        "batch_sizes": list(batch_sizes),
        "candidates": candidate_records,
    }
    (output / "PROFILE_PLAN.json").write_text(json.dumps(plan, indent=2, sort_keys=True) + "\n")
    return plan


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True, help="Reviewed source Candidate directory")
    parser.add_argument("--output", type=Path, required=True, help="New profiling Candidate root")
    parser.add_argument(
        "--batch-size",
        type=int,
        action="append",
        dest="batch_sizes",
        help="Batch size to prepare; repeat to override the default 1,2,4,8,16 matrix",
    )
    args = parser.parse_args()
    plan = prepare_profiles(
        args.source,
        args.output,
        tuple(args.batch_sizes) if args.batch_sizes else DEFAULT_BATCH_SIZES,
    )
    print(json.dumps(plan, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
