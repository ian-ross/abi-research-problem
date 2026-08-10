"""Dataset Profile Artifact generator for GOES ABI Contrail Segmentation."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections.abc import Mapping, Sequence
from datetime import datetime, timezone
from pathlib import Path
from statistics import mean
from typing import Any

from ml_autoresearch.errors import ResearchProblemDataError

from abi_contrail.adapters import RESEARCH_PROBLEM_ID, RESEARCH_PROBLEM_VERSION, split_data_policy_metadata
from abi_contrail.data_config import ABIDataConfigError, resolve_training_data_root
from abi_contrail.datasets import (
    ABIPatchIndexRecord,
    build_google_abi_patch_index,
    build_mit_abi_patch_index,
    load_abi_metadata_rows,
    open_abi_patch_arrays,
)

GENERATOR_VERSION = "abi_contrail.profile.v1"
CHANNEL_STAT_MAX_RECORDS_PER_SPLIT = 16
CHANNEL_STAT_MAX_PIXELS_PER_RECORD = 1024

_ABI_CHANNELS = (
    (1, "Blue", 0.47, "reflectance_factor"),
    (2, "Red", 0.64, "reflectance_factor"),
    (3, "Veggie", 0.865, "reflectance_factor"),
    (4, "Cirrus", 1.378, "reflectance_factor"),
    (5, "Snow/Ice", 1.61, "reflectance_factor"),
    (6, "Cloud Particle Size", 2.25, "reflectance_factor"),
    (7, "Shortwave Window", 3.9, "kelvin"),
    (8, "Upper-level Water Vapor", 6.19, "kelvin"),
    (9, "Mid-level Water Vapor", 6.95, "kelvin"),
    (10, "Lower-level Water Vapor", 7.34, "kelvin"),
    (11, "Cloud-top Phase", 8.5, "kelvin"),
    (12, "Ozone", 9.61, "kelvin"),
    (13, "Clean Longwave Window", 10.35, "kelvin"),
    (14, "Longwave Window", 11.2, "kelvin"),
    (15, "Dirty Longwave Window", 12.3, "kelvin"),
    (16, "CO2 Longwave Infrared", 13.3, "kelvin"),
)


def generate_dataset_profile(data_config: Mapping[str, object]) -> dict[str, Any]:
    """Generate trusted agent-visible ABI dataset summaries from local data.

    ``data_config`` follows the same source layout used by ``ABITrainingAdapter``:
    either a single source with ``layout``, ``inputs_zarr`` and ``labels_zarr``, or
    a top-level ``sources`` list containing MIT and/or Google source configs.
    Google sources require ``metadata_rows`` so the provider can preserve the
    distributed train/validation provenance.
    """

    try:
        root = resolve_training_data_root(data_config)
    except ABIDataConfigError as exc:
        raise ResearchProblemDataError(str(exc)) from exc
    if not root.is_dir():
        raise ResearchProblemDataError(
            f"ABI training data root does not exist or is not a directory: {root}"
        )

    source_profiles = [_profile_source(root, source_config) for source_config in _source_data_configs(data_config)]
    safe_range_statistics = {
        source["dataset_source"]: source.pop("safe_channel_statistics")
        for source in source_profiles
    }
    return {
        "artifact_type": "dataset_profile",
        "schema_version": "dataset-profile.v1",
        "provenance": {
            "research_problem_id": RESEARCH_PROBLEM_ID,
            "research_problem_version": RESEARCH_PROBLEM_VERSION,
            "dataset_identity": "GOES ABI Contrail Segmentation on ABI Patches from MIT and Google Dataset Sources",
            "data_config_scope": _profile_config_scope(data_config),
            "generation_command": "uv run python -m abi_contrail.profile --data-config <CONFIG_JSON> --output <OUTPUT_JSON>",
            "generation_version": GENERATOR_VERSION,
            "generation_timestamp": _timestamp(),
            "source_policy": "trusted Research Problem package-generated",
            "split_scope": "Google source provenance plus MIT deterministic whole-scene split before windowing",
        },
        "task": {
            "name": "binary GOES ABI Contrail Segmentation",
            "sample_unit": "ABI Patch",
            "target": "Contrail Mask, labels != 0",
            "candidate_input_guardrail": "longitude and latitude source channels are never exposed as candidate inputs",
        },
        "source_profiles": source_profiles,
        "combined_counts": _combine_counts(source_profiles),
        "abi_channels": {
            "semantics": _abi_channel_semantics(),
            "safe_range_statistics_by_source": safe_range_statistics,
            "source_channel_indices_included": list(range(16)),
            "source_channel_indices_excluded": [16, 17],
            "statistics_scope": {
                "selection": "deterministic evenly-spaced records within each split",
                "max_records_per_split": CHANNEL_STAT_MAX_RECORDS_PER_SPLIT,
                "max_pixels_per_record": CHANNEL_STAT_MAX_PIXELS_PER_RECORD,
                "nonfinite_values_excluded_from_ranges": True,
            },
        },
        "split_policy": split_data_policy_metadata(),
        "positivity": {
            "definition": "positive ABI Patch has any nonzero Contrail Mask pixel",
            "by_source": {source["dataset_source"]: source["positivity"] for source in source_profiles},
        },
        "projection_caveats": _projection_caveats(),
        "known_caveats": [
            "Counts summarize the local mounted dataset snapshot and may differ from later downloaded or regenerated snapshots.",
            "MIT full-scene arrays are split by whole scene before 256x256 windowing to avoid scene leakage.",
            "Google patch train/validation membership is treated as provenance encoded in scene/file names, not reshuffled.",
            "Projection metadata is not candidate input; candidate models receive only provider-approved ABI channels and optional solar geometry input.",
        ],
    }


def missing_data_profile(data_config: Mapping[str, object] | None, reason: str) -> dict[str, Any]:
    """Return a documented placeholder when optional full ABI data is unavailable."""

    return {
        "artifact_type": "dataset_profile",
        "schema_version": "dataset-profile.v1",
        "provenance": {
            "research_problem_id": RESEARCH_PROBLEM_ID,
            "research_problem_version": RESEARCH_PROBLEM_VERSION,
            "dataset_identity": "GOES ABI Contrail Segmentation on ABI Patches from MIT and Google Dataset Sources",
            "data_config_scope": _profile_config_scope(data_config or {}),
            "generation_command": "uv run python -m abi_contrail.profile --allow-missing --output <OUTPUT_JSON>",
            "generation_version": GENERATOR_VERSION,
            "generation_timestamp": _timestamp(),
            "source_policy": "trusted Research Problem package-generated placeholder",
            "split_scope": "no raw data available",
        },
        "status": "missing_optional_data",
        "reason": reason,
        "expected_sources": ["mit", "google"],
        "expected_summaries": [
            "MIT and Google train/validation counts",
            "positive ABI Patch counts and prevalence",
            "per-split Contrail Mask area distributions",
            "bounded safe-range statistics for ABI channels 1-16",
            "source split policy metadata",
            "input/label array shapes and projection caveats",
        ],
        "known_caveats": [
            "Run the generator outside the Agent Control Boundary with local ABI zarr paths to produce numeric summaries.",
            "Use --allow-missing only for scaffolding or environments where full ABI data is intentionally absent.",
        ],
    }


def _profile_source(root: Path, source_config: Mapping[str, object]) -> dict[str, Any]:
    layout = str(source_config.get("layout", ""))
    if layout not in {"mit", "google"}:
        raise ResearchProblemDataError("ABI profile source layout must be 'mit' or 'google'")
    inputs_path = _resolve_required_path(root, source_config, "inputs_zarr")
    labels_path = _resolve_required_path(root, source_config, "labels_zarr")
    arrays = open_abi_patch_arrays(inputs_path, labels_path, layout=layout)  # type: ignore[arg-type]
    try:
        metadata_rows = load_abi_metadata_rows(root, source_config)
    except ValueError as exc:
        raise ResearchProblemDataError(str(exc)) from exc
    if layout == "google":
        if metadata_rows is None:
            raise ResearchProblemDataError(
                "google ABI profile sources require data_config.metadata_rows or data_config.metadata_parquet"
            )
        split_index = build_google_abi_patch_index(metadata_rows)
    else:
        scene_names = _optional_string_sequence(source_config.get("scene_names"))
        goes_times = _optional_string_sequence(source_config.get("goes_times"))
        if metadata_rows is not None:
            scene_names = tuple(str(row["scene_name"]) for row in metadata_rows)
            goes_times = tuple(str(row["goes_time"]) if row.get("goes_time") is not None else None for row in metadata_rows)
        split_index = build_mit_abi_patch_index(
            arrays.labels,
            scene_names=scene_names,
            goes_times=goes_times,
            val_fraction=float(source_config.get("val_fraction", 0.2)),
            seed=int(source_config.get("split_seed", 20260712)),
            patch_size=int(source_config.get("patch_size", 256)),
            stride=int(source_config.get("stride", 256)),
        )
    records = split_index.records
    return {
        "dataset_source": layout,
        "source_artifacts": {
            "inputs": _logical_artifact_reference(source_config.get("inputs_zarr"), "inputs.zarr"),
            "labels": _logical_artifact_reference(source_config.get("labels_zarr"), "labels.zarr"),
            "metadata": _logical_artifact_reference(source_config.get("metadata_parquet"), "inline_or_unspecified"),
        },
        "input_shape": list(arrays.inputs.shape),
        "input_dtype": str(arrays.inputs.dtype),
        "input_chunks": list(arrays.inputs.chunks) if arrays.inputs.chunks is not None else None,
        "label_shape": list(arrays.labels.shape),
        "label_dtype": str(arrays.labels.dtype),
        "label_chunks": list(arrays.labels.chunks) if arrays.labels.chunks is not None else None,
        "split_counts": {
            "train": len(split_index.train),
            "validation": len(split_index.validation),
            "total": len(records),
        },
        "positivity": _positive_summary(records),
        "mask_area_distribution": _mask_area_summary(records, arrays.labels),
        "safe_channel_statistics": _safe_channel_statistics(records, arrays.inputs),
        "record_index_sha256": _record_index_digest(records),
        "split_policy": _safe_split_policy(split_index.data_policy_metadata),
    }


def _positive_summary(records: Sequence[ABIPatchIndexRecord]) -> dict[str, Any]:
    total = len(records)
    positive = sum(1 for record in records if record.positive)
    by_split = {}
    for split in ("train", "validation"):
        split_records = [record for record in records if record.split == split]
        split_positive = sum(1 for record in split_records if record.positive)
        by_split[split] = {
            "sample_count": len(split_records),
            "positive_patch_count": split_positive,
            "negative_patch_count": len(split_records) - split_positive,
            "positive_patch_prevalence": split_positive / len(split_records) if split_records else 0.0,
        }
    return {
        "sample_count": total,
        "positive_patch_count": positive,
        "negative_patch_count": total - positive,
        "positive_patch_prevalence": positive / total if total else 0.0,
        "by_split": by_split,
    }


def _mask_area_summary(records: Sequence[ABIPatchIndexRecord], labels: Any) -> dict[str, Any]:
    fractions = [_mask_area_fraction(record, labels) for record in records]
    summary = _fraction_summary(fractions)
    summary["by_split"] = {
        split: _fraction_summary([
            value for record, value in zip(records, fractions, strict=True) if record.split == split
        ])
        for split in ("train", "validation")
    }
    return summary


def _fraction_summary(fractions: Sequence[float]) -> dict[str, Any]:
    positive_fractions = [value for value in fractions if value > 0.0]
    bins = [0.0, 0.0001, 0.001, 0.005, 0.01, 0.05, 0.1, 1.0]
    digest = hashlib.sha256()
    for value in fractions:
        digest.update(float(value).hex().encode() + b"\n")
    return {
        "sample_count": len(fractions),
        "fractions_sha256": digest.hexdigest(),
        "min_fraction": min(fractions) if fractions else 0.0,
        "mean_fraction": mean(fractions) if fractions else 0.0,
        "max_fraction": max(fractions) if fractions else 0.0,
        "positive_mean_fraction": mean(positive_fractions) if positive_fractions else 0.0,
        "histogram_bins_fraction": bins,
        "histogram_counts": _histogram(fractions, bins),
    }


def _mask_area_fraction(record: ABIPatchIndexRecord, labels: Any) -> float:
    import numpy as np

    if record.sample_index is not None:
        label_window = np.asarray(labels[record.sample_index, :, :])
    else:
        row_end = record.row + 256
        col_end = record.col + 256
        label_window = np.asarray(labels[record.scene_index, record.row : row_end, record.col : col_end])
    return float(np.count_nonzero(label_window != 0)) / float(label_window.size) if label_window.size else 0.0


def _safe_split_policy(policy: Mapping[str, object]) -> dict[str, object]:
    safe = {
        key: value
        for key, value in policy.items()
        if key not in {"train_scenes", "validation_scenes"}
    }
    for split in ("train", "validation"):
        scenes = policy.get(f"{split}_scenes")
        if isinstance(scenes, Sequence) and not isinstance(scenes, (str, bytes)):
            digest = hashlib.sha256()
            for scene in scenes:
                digest.update(str(scene).encode() + b"\n")
            safe[f"{split}_scene_count"] = len(scenes)
            safe[f"{split}_scene_ids_sha256"] = digest.hexdigest()
    return safe


def _safe_channel_statistics(
    records: Sequence[ABIPatchIndexRecord], inputs: Any
) -> dict[str, Any]:
    import numpy as np

    selected = []
    for split in ("train", "validation"):
        split_records = [record for record in records if record.split == split]
        if len(split_records) <= CHANNEL_STAT_MAX_RECORDS_PER_SPLIT:
            selected.extend(split_records)
        elif split_records:
            indices = np.linspace(
                0, len(split_records) - 1, CHANNEL_STAT_MAX_RECORDS_PER_SPLIT, dtype=int
            )
            selected.extend(split_records[int(index)] for index in indices)

    channel_values: list[list[Any]] = [[] for _ in range(16)]
    sampled_pixel_count = 0
    sample_digest = hashlib.sha256()
    value_digest = hashlib.sha256()
    for record in selected:
        window = _input_window(record, inputs)
        if window.ndim != 3 or window.shape[-1] < 16:
            raise ResearchProblemDataError(
                f"ABI source input must have shape [H, W, >=16], got {window.shape}"
            )
        flat = window[..., :16].reshape(-1, 16)
        count = min(len(flat), CHANNEL_STAT_MAX_PIXELS_PER_RECORD)
        if count == 0:
            continue
        indices = np.linspace(0, len(flat) - 1, count, dtype=int)
        sampled = flat[indices]
        sampled_pixel_count += len(sampled)
        sample_digest.update(_record_identity(record).encode() + b"\n")
        value_digest.update(np.asarray(sampled, dtype="<f4").tobytes(order="C"))
        for channel_index in range(16):
            channel_values[channel_index].append(np.asarray(sampled[:, channel_index]))

    summaries = []
    for source_index, values in enumerate(channel_values):
        merged = np.concatenate(values) if values else np.asarray([], dtype=np.float32)
        finite = merged[np.isfinite(merged)]
        summaries.append(
            {
                "abi_channel": source_index + 1,
                "source_channel_index": source_index,
                "sampled_value_count": int(merged.size),
                "finite_value_count": int(finite.size),
                "nonfinite_value_count": int(merged.size - finite.size),
                "min": float(np.min(finite)) if finite.size else None,
                "p01": float(np.quantile(finite, 0.01)) if finite.size else None,
                "mean": float(np.mean(finite)) if finite.size else None,
                "p99": float(np.quantile(finite, 0.99)) if finite.size else None,
                "max": float(np.max(finite)) if finite.size else None,
            }
        )
    return {
        "selection_record_count": len(selected),
        "sampled_pixel_count": sampled_pixel_count,
        "selected_records_sha256": sample_digest.hexdigest(),
        "sampled_values_sha256": value_digest.hexdigest(),
        "channels": summaries,
    }


def _input_window(record: ABIPatchIndexRecord, inputs: Any) -> Any:
    import numpy as np

    if record.sample_index is not None:
        return np.asarray(inputs[record.sample_index, :, :, :16])
    row_end = record.row + 256
    col_end = record.col + 256
    return np.asarray(
        inputs[record.scene_index, record.row : row_end, record.col : col_end, :16]
    )


def _record_index_digest(records: Sequence[ABIPatchIndexRecord]) -> str:
    digest = hashlib.sha256()
    for record in records:
        digest.update(_record_identity(record).encode() + b"\n")
    return digest.hexdigest()


def _record_identity(record: ABIPatchIndexRecord) -> str:
    return "|".join(
        (
            record.dataset_source,
            record.split,
            record.scene_name,
            str(record.scene_index),
            str(record.sample_index),
            str(record.row),
            str(record.col),
            "1" if record.positive else "0",
        )
    )


def _abi_channel_semantics() -> list[dict[str, Any]]:
    return [
        {
            "abi_channel": channel,
            "source_channel_index": channel - 1,
            "common_name": name,
            "central_wavelength_micrometers": wavelength,
            "unit": unit,
        }
        for channel, name, wavelength, unit in _ABI_CHANNELS
    ]


def _combine_counts(source_profiles: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    split_counts = {"train": 0, "validation": 0, "total": 0}
    positive = 0
    for source in source_profiles:
        counts = source["split_counts"]
        for key in split_counts:
            split_counts[key] += int(counts[key])
        positive += int(source["positivity"]["positive_patch_count"])
    total = split_counts["total"]
    return {
        "split_counts": split_counts,
        "positive_patch_count": positive,
        "negative_patch_count": total - positive,
        "positive_patch_prevalence": positive / total if total else 0.0,
    }


def _source_data_configs(data_config: Mapping[str, object]) -> tuple[Mapping[str, object], ...]:
    sources = data_config.get("sources")
    if sources is None:
        return (data_config,)
    if not isinstance(sources, Sequence) or isinstance(sources, (str, bytes)):
        raise ResearchProblemDataError("ABI data_config.sources must be a sequence of source configs")
    configs = []
    for source in sources:
        if not isinstance(source, Mapping):
            raise ResearchProblemDataError("each ABI data_config.sources item must be a mapping")
        merged = {key: value for key, value in data_config.items() if key != "sources"}
        merged.update(source)
        configs.append(merged)
    if not configs:
        raise ResearchProblemDataError("ABI data_config.sources must not be empty")
    return tuple(configs)


def _projection_caveats() -> list[str]:
    return [
        "GOES ABI source pixels are geostationary satellite observations; pixel size and viewing geometry vary across the disk.",
        "MIT full-scene sources may be reprojected/windowed before ABI Patch indexing; profile counts should record the local generation snapshot.",
        "Google 256x256 patches are already patch products; train/validation provenance is encoded by source names rather than recomputed from map geometry.",
        "Longitude and latitude, when present in source arrays, are trusted-provider context only for diagnostics/Artifact Filters and are forbidden candidate inputs.",
    ]


def _histogram(values: Sequence[float], bins: Sequence[float]) -> list[int]:
    counts = [0 for _ in range(len(bins) - 1)]
    for value in values:
        for index, (low, high) in enumerate(zip(bins, bins[1:], strict=True)):
            in_bin = low <= value <= high if index == len(counts) - 1 else low <= value < high
            if in_bin:
                counts[index] += 1
                break
    return counts


def _resolve_required_path(root: Path, data_config: Mapping[str, object], key: str) -> Path:
    value = data_config.get(key)
    if not isinstance(value, str) or not value:
        raise ResearchProblemDataError(f"ABI data_config.{key} is required")
    path = Path(value).expanduser()
    if not path.is_absolute():
        path = root / path
    path = path.resolve()
    if not path.exists():
        raise ResearchProblemDataError(f"ABI data_config.{key} does not exist: {path}")
    return path


def _optional_string_sequence(value: object) -> tuple[str, ...] | None:
    if value is None:
        return None
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes)):
        raise ValueError("expected a sequence of strings")
    return tuple(str(item) for item in value)


def _profile_config_scope(data_config: Mapping[str, object]) -> dict[str, Any]:
    safe_keys = ("layout", "val_fraction", "split_seed", "patch_size", "stride")
    return {
        "logical_data_root": "training",
        "sources": [
            {
                **{key: source[key] for key in safe_keys if key in source},
                "inputs": _logical_artifact_reference(source.get("inputs_zarr"), "inputs.zarr"),
                "labels": _logical_artifact_reference(source.get("labels_zarr"), "labels.zarr"),
                "metadata": _logical_artifact_reference(source.get("metadata_parquet"), "inline_or_unspecified"),
            }
            for source in _source_data_configs(data_config)
        ],
    }


def _logical_artifact_reference(value: object, fallback: str) -> str:
    if not isinstance(value, str) or not value:
        return fallback
    path = Path(value)
    if path.is_absolute() or ".." in path.parts:
        return path.name
    return path.as_posix()


def _timestamp() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Generate an ABI Dataset Profile Artifact.")
    parser.add_argument("--data-config", type=Path, help="JSON file containing ABI data_config")
    parser.add_argument("--output", type=Path, required=True, help="Output JSON artifact path")
    parser.add_argument("--allow-missing", action="store_true", help="Write a documented placeholder instead of failing when data is unavailable")
    args = parser.parse_args(argv)

    data_config: dict[str, object] = {}
    if args.data_config is not None:
        data_config = json.loads(args.data_config.read_text())
    try:
        if args.data_config is None:
            raise ResearchProblemDataError("--data-config is required unless --allow-missing is used")
        profile = generate_dataset_profile(data_config)
    except ResearchProblemDataError as exc:
        if not args.allow_missing:
            raise SystemExit(str(exc)) from exc
        profile = missing_data_profile(data_config, str(exc))

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(profile, indent=2, sort_keys=True) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
