"""Explicit operator commands for trusted geographic ancillary data."""

from __future__ import annotations

import argparse
import json
import os
import tempfile
from collections.abc import Callable, Mapping
from pathlib import Path
from typing import Any

import numpy as np

from abi_contrail.ancillary import (
    AncillaryDataError,
    committed_natural_earth_manifest_path,
    load_ancillary_manifest,
    verify_manifest_dataset_file,
)
from abi_contrail.artifact_filters import ABIArtifactFilterPipeline, build_default_artifact_filter_pipeline

DownloadFunction = Callable[[str, Path], None]


def provision_natural_earth(
    *,
    dataset_root: str | Path,
    source_manifest_path: str | Path | None = None,
    destination: str | Path = "ancillary/natural-earth",
    downloader: DownloadFunction | None = None,
    verify_only: bool = False,
) -> dict[str, object]:
    """Idempotently provision pinned Natural Earth files beneath a data root."""

    root = Path(dataset_root).expanduser().resolve()
    if not root.is_dir():
        raise AncillaryDataError(f"dataset_root does not exist or is not a directory: {root}")
    source_path = Path(source_manifest_path or committed_natural_earth_manifest_path()).expanduser().resolve()
    manifest = load_ancillary_manifest(source_path)
    destination_path = Path(destination).expanduser()
    if not destination_path.is_absolute():
        destination_path = root / destination_path
    destination_path = destination_path.resolve()
    try:
        destination_path.relative_to(root)
    except ValueError as exc:
        raise AncillaryDataError(
            f"Natural Earth destination must be beneath dataset_root {root}: {destination_path}"
        ) from exc
    destination_path.mkdir(parents=True, exist_ok=True)
    fetch = downloader or _download_http

    results: list[dict[str, object]] = []
    for raw in manifest["datasets"]:
        if not isinstance(raw, Mapping):  # Manifest validation already rejects this.
            continue
        dataset = dict(raw)
        target = destination_path / str(dataset["filename"])
        status = "already_valid"
        try:
            verify_manifest_dataset_file(target, dataset)
        except AncillaryDataError:
            if verify_only:
                raise
            status = "downloaded"
            temporary = _temporary_path(destination_path, target.name)
            try:
                fetch(str(dataset["immutable_url"]), temporary)
                verify_manifest_dataset_file(temporary, dataset)
                os.replace(temporary, target)
            finally:
                temporary.unlink(missing_ok=True)
        results.append(
            {
                "id": dataset["id"],
                "path": str(target),
                "size_bytes": dataset["size_bytes"],
                "sha256": dataset["sha256"],
                "status": status,
            }
        )

    installed_manifest = destination_path / "manifest.json"
    canonical_manifest = json.dumps(manifest, indent=2, sort_keys=True) + "\n"
    if not installed_manifest.is_file() or installed_manifest.read_text() != canonical_manifest:
        temporary_manifest = _temporary_path(destination_path, "manifest.json")
        try:
            temporary_manifest.write_text(canonical_manifest)
            os.replace(temporary_manifest, installed_manifest)
        finally:
            temporary_manifest.unlink(missing_ok=True)
    return {
        "status": "verified" if verify_only else "provisioned",
        "dataset_root": str(root),
        "destination": str(destination_path),
        "manifest": str(installed_manifest),
        "bundle_id": manifest["bundle_id"],
        "datasets": results,
        "evaluation_network_policy": "offline_no_runtime_downloads",
    }


def run_geographic_filter_smoke(
    *,
    dataset: object,
    filter_pipeline: ABIArtifactFilterPipeline,
    max_samples: int = 64,
) -> dict[str, object]:
    """Boundedly prove real provider context can remove geographic pixels."""

    if max_samples < 1:
        raise ValueError("max_samples must be positive")
    sample_limit = min(len(dataset), max_samples)  # type: ignore[arg-type]
    if sample_limit < 1:
        raise RuntimeError("geographic filter smoke requires a non-empty evaluation dataset")
    samples_examined = 0
    removed_total = 0
    feature_total = 0
    candidate_channels: int | None = None
    active = False
    for index in range(sample_limit):
        candidate_inputs, target = dataset[index]  # type: ignore[index]
        if candidate_channels is None:
            candidate_channels = int(candidate_inputs.shape[0])
        shape = tuple(int(value) for value in target.shape[-2:])
        prediction = np.ones((1, *shape), dtype=bool)
        probabilities = np.ones((1, *shape), dtype=np.float32)
        context_getter = getattr(dataset, "filter_context", None)
        context = dict(context_getter(index)) if callable(context_getter) else {}
        filtered = filter_pipeline.apply(prediction, probabilities, context=context)
        geographic = _geographic_diagnostics(filtered.diagnostics)
        active = active or bool(geographic.get("active", False))
        removed_total += int(geographic.get("removed_pixel_count", 0))
        feature_total += int(geographic.get("feature_pixel_count", 0))
        samples_examined += 1
        if removed_total > 0:
            break
    if not active:
        raise RuntimeError("Geographic Feature Filter was not active during bounded smoke")
    if removed_total < 1:
        raise RuntimeError(
            f"Geographic Feature Filter rasterized no pixels in {samples_examined} bounded validation samples"
        )
    return {
        "status": "passed",
        "samples_examined": samples_examined,
        "max_samples": max_samples,
        "candidate_input_channels": candidate_channels,
        "longitude_latitude_exposed_to_candidate": False,
        "provider_filter_context": "longitude_latitude_or_pre_rasterized_mask",
        "geographic_filter_active": active,
        "geographic_feature_pixel_count": feature_total,
        "geographic_removed_pixel_count": removed_total,
    }


def provision_main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Provision pinned Natural Earth data for the trusted ABI Geographic Feature Filter."
    )
    parser.add_argument("--dataset-root", type=Path, required=True)
    parser.add_argument("--destination", type=Path, default=Path("ancillary/natural-earth"))
    parser.add_argument("--source-manifest", type=Path, default=committed_natural_earth_manifest_path())
    parser.add_argument("--verify-only", action="store_true")
    args = parser.parse_args(argv)
    report = provision_natural_earth(
        dataset_root=args.dataset_root,
        source_manifest_path=args.source_manifest,
        destination=args.destination,
        verify_only=args.verify_only,
    )
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


def smoke_main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Run a bounded trusted Geographic Feature Filter smoke check without training."
    )
    parser.add_argument("--workspace-root", type=Path, default=Path("."))
    parser.add_argument(
        "--dataset-root",
        type=Path,
        help="Optional trusted host dataset-root override for operator smoke validation.",
    )
    parser.add_argument("--max-samples", type=int, default=64)
    args = parser.parse_args(argv)

    from abi_contrail.adapters import ABITrainingAdapter
    from ml_autoresearch.candidate_execution_config import load_candidate_execution_config

    workspace_root = args.workspace_root.expanduser().resolve()
    config = load_candidate_execution_config(workspace_root)
    provider = config.research_problem_provider
    if provider is None:
        raise RuntimeError("workspace has no configured Research Problem provider")
    data_config = dict(provider.data_config)
    if args.dataset_root is not None:
        data_config["dataset_root"] = str(args.dataset_root.expanduser().resolve())
    adapter = ABITrainingAdapter(data_config)
    dataset = adapter.build_evaluation_dataset(
        data_config=data_config,
        resolved_manifest_path=Path("__abi_geographic_smoke_default_manifest__.yaml"),
    )
    pipeline = build_default_artifact_filter_pipeline(data_config)
    report = run_geographic_filter_smoke(
        dataset=dataset,
        filter_pipeline=pipeline,
        max_samples=args.max_samples,
    )
    report["workspace_root"] = str(workspace_root)
    report["artifact_filter_provenance"] = pipeline.provenance()
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


def _download_http(url: str, destination: Path) -> None:
    import httpx

    with httpx.stream("GET", url, follow_redirects=True, timeout=120.0) as response:
        response.raise_for_status()
        with destination.open("wb") as handle:
            for chunk in response.iter_bytes():
                handle.write(chunk)


def _temporary_path(directory: Path, name: str) -> Path:
    descriptor, value = tempfile.mkstemp(prefix=f".{name}.", suffix=".tmp", dir=directory)
    os.close(descriptor)
    return Path(value)


def _geographic_diagnostics(diagnostics: Mapping[str, object]) -> Mapping[str, object]:
    filters = diagnostics.get("filters")
    if isinstance(filters, list):
        for item in filters:
            if isinstance(item, Mapping) and item.get("filter") == "geographic_feature_filter":
                return item
    raise RuntimeError("Artifact Filter pipeline did not report Geographic Feature Filter diagnostics")


__all__ = [
    "provision_main",
    "provision_natural_earth",
    "run_geographic_filter_smoke",
    "smoke_main",
]
