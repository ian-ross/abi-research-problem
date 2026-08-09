"""Operator CLI for trusted MCAST Baseline Segmenter evaluations."""

from __future__ import annotations

import argparse
import hashlib
import json
import logging
import os
import subprocess
import sys
import time
from collections.abc import Callable, Sequence
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from abi_contrail.ancillary import resolve_geographic_ancillary
from abi_contrail.baseline_segmenters import MCAST_BASELINE_METADATA, MCAST_BASELINE_NAMES, configured_mcast_baseline_assets


def run_configured_baseline_evaluations(
    *,
    workspace_root: str | Path,
    baseline_names: Sequence[str],
    output_root: str | Path,
    device: str = "cpu",
    evaluator: Any | None = None,
    progress: Callable[[str], None] | None = None,
    log_every: int = 100,
    postprocessing_batch_size: int = 8,
) -> tuple[dict[str, object], ...]:
    """Run configured trusted baselines and persist reproducibility manifests."""

    from ml_autoresearch.candidate_execution_config import load_candidate_execution_config

    if log_every <= 0:
        raise ValueError("log_every must be positive")
    emit = progress or (lambda _message: None)
    root = Path(workspace_root).expanduser().resolve()
    config = load_candidate_execution_config(root)
    provider = config.research_problem_provider
    if provider is None:
        raise ValueError("baseline evaluation requires a configured [research_problem] provider")
    if provider.id != "goes_abi_contrail_segmentation":
        raise ValueError(
            "configured Research Problem id must be 'goes_abi_contrail_segmentation' for ABI baseline evaluation"
        )
    names = tuple(baseline_names)
    if not names:
        raise ValueError("at least one baseline name is required")
    unknown = set(names) - set(MCAST_BASELINE_NAMES)
    if unknown:
        raise ValueError(f"unsupported MCAST baseline name(s): {sorted(unknown)}")

    data_config = provider.effective_data_config()
    geographic_ancillary = resolve_geographic_ancillary(data_config)
    configured_assets = configured_mcast_baseline_assets(data_config)
    missing = [name for name in names if name not in configured_assets]
    if missing:
        keys = [MCAST_BASELINE_METADATA[name].asset_config_key for name in missing]
        raise ValueError(f"missing configured MCAST baseline asset path(s): {keys}")

    if evaluator is None:
        from abi_contrail.evaluation import ABIEvaluationAdapter

        evaluator = ABIEvaluationAdapter()
    destination = Path(output_root).expanduser().resolve()
    destination.mkdir(parents=True, exist_ok=True)
    workspace_git = _git_provenance(root)
    harness_root = _configured_harness_root(root)
    harness_git = _git_provenance(harness_root) if harness_root is not None else None

    emit(
        f"configured evaluation: baselines={','.join(names)} device={device} "
        f"postprocessing_batch_size={postprocessing_batch_size} "
        f"output_root={destination} log_every={log_every}"
    )
    results: list[dict[str, object]] = []
    for ordinal, name in enumerate(names, start=1):
        evaluation_dir = destination / name
        evaluation_dir.mkdir(parents=True, exist_ok=True)
        emit(f"starting baseline {ordinal}/{len(names)}: {name}; output={evaluation_dir}")
        aggregate, per_sample, _threshold_sweep, diagnostics = evaluator.run_baseline_validation_evaluation(
            baseline_name=name,
            data_config=data_config,
            device=device,
            evaluation_dir=evaluation_dir,
            progress_callback=emit,
            log_every=log_every,
            postprocessing_batch_size=postprocessing_batch_size,
        )
        emit(f"collecting asset and Git provenance for {name}")
        manifest = {
            "status": "completed",
            "completed_at": _timestamp(),
            "research_problem": {
                "id": provider.id,
                "provider_target": provider.provider_target,
                "expected_contract_version": provider.expected_contract_version,
                "package_root": str(provider.package_root.resolve()),
            },
            "workspace_git": workspace_git,
            "harness_git": harness_git,
            "data_config": data_config,
            "baseline": {
                "name": name,
                "version": MCAST_BASELINE_METADATA[name].version,
                "device": device,
                "asset": _asset_provenance(configured_assets[name]),
            },
            "sample_count": len(per_sample),
            "metrics": aggregate,
            "artifact_filters": {
                "geographic_feature_filter": geographic_ancillary.provenance(),
            },
            "postprocessing": diagnostics.get("postprocessing", {}),
            "artifacts": {
                "aggregate_metrics": "aggregate_metrics.json",
                "per_sample_metrics": "per_sample_metrics.jsonl",
                "threshold_sweep": "threshold_sweep.json",
                "diagnostic_samples": "diagnostic_samples/samples.json",
            },
        }
        (evaluation_dir / "run_manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")
        results.append(manifest)
        emit(
            f"completed baseline {ordinal}/{len(names)}: {name}; samples={len(per_sample)} "
            f"filtered/dice={aggregate.get('filtered/dice')}"
        )
    emit(f"all requested baselines completed; output_root={destination}")
    return tuple(results)


def _asset_provenance(path: Path) -> dict[str, object]:
    resolved = path.expanduser().resolve(strict=True)
    if resolved.is_file():
        return {
            "path": str(resolved),
            "kind": "file",
            "size_bytes": resolved.stat().st_size,
            "sha256": _file_sha256(resolved),
        }
    if not resolved.is_dir():
        raise ValueError(f"baseline asset is neither a file nor a directory: {resolved}")
    files = sorted(item for item in resolved.rglob("*") if item.is_file())
    digest = hashlib.sha256()
    total_size = 0
    entries: list[dict[str, object]] = []
    for file_path in files:
        relative = file_path.relative_to(resolved).as_posix()
        file_digest = _file_sha256(file_path)
        size = file_path.stat().st_size
        total_size += size
        digest.update(relative.encode("utf-8") + b"\0" + file_digest.encode("ascii") + b"\n")
        entries.append({"path": relative, "size_bytes": size, "sha256": file_digest})
    return {
        "path": str(resolved),
        "kind": "directory",
        "size_bytes": total_size,
        "sha256": digest.hexdigest(),
        "files": entries,
    }


def _file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _configured_harness_root(workspace_root: Path) -> Path | None:
    import tomllib

    data = tomllib.loads((workspace_root / "ml-autoresearch.toml").read_text())
    settings = data.get("runtime_images", {})
    if not isinstance(settings, dict):
        return None
    value = settings.get("dev_source_path")
    if not isinstance(value, str) or not value:
        return None
    return Path(value).expanduser().resolve()


def _git_provenance(root: Path | None) -> dict[str, object] | None:
    if root is None or not root.is_dir():
        return None

    def git(*args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["git", "-C", str(root), *args],
            check=False,
            capture_output=True,
            text=True,
        )

    commit = git("rev-parse", "HEAD")
    if commit.returncode != 0:
        return None
    status = git("status", "--porcelain")
    return {
        "root": str(root),
        "commit": commit.stdout.strip(),
        "dirty": status.returncode == 0 and bool(status.stdout.strip()),
    }


def _timestamp() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run trusted MCAST Baseline Segmenter evaluations.")
    parser.add_argument("--workspace-root", type=Path, default=Path("."))
    parser.add_argument(
        "--baseline",
        action="append",
        choices=[*MCAST_BASELINE_NAMES, "all"],
        help="Baseline to run; repeat for multiple baselines. Defaults to all.",
    )
    parser.add_argument("--output-root", type=Path, required=True)
    parser.add_argument("--device", default="cuda")
    parser.add_argument(
        "--log-every",
        type=int,
        default=100,
        help="Emit sample-level progress every N samples (default: 100).",
    )
    parser.add_argument(
        "--postprocessing-batch-size",
        type=int,
        default=8,
        help="Maximum ABI Patches transferred to the postprocessing device at once (default: 8).",
    )
    args = parser.parse_args(argv)
    if args.log_every <= 0:
        parser.error("--log-every must be positive")
    if args.postprocessing_batch_size <= 0:
        parser.error("--postprocessing-batch-size must be positive")
    requested = tuple(args.baseline or ("all",))
    names = MCAST_BASELINE_NAMES if "all" in requested else requested
    output_root = args.output_root.expanduser().resolve()
    output_root.mkdir(parents=True, exist_ok=True)
    log_path = output_root / "baseline_evaluation.log"
    logger = _progress_logger(log_path)
    logger.info("baseline evaluation command started; log=%s", log_path)
    affinity = sorted(os.sched_getaffinity(0)) if hasattr(os, "sched_getaffinity") else []
    logger.info(
        "resource limits: cpu_affinity_count=%s cpu_affinity=%s OMP_NUM_THREADS=%s "
        "MKL_NUM_THREADS=%s OPENBLAS_NUM_THREADS=%s CUDA_VISIBLE_DEVICES=%s",
        len(affinity) if affinity else "unknown",
        affinity if affinity else "unknown",
        os.environ.get("OMP_NUM_THREADS", "unset"),
        os.environ.get("MKL_NUM_THREADS", "unset"),
        os.environ.get("OPENBLAS_NUM_THREADS", "unset"),
        os.environ.get("CUDA_VISIBLE_DEVICES", "unset"),
    )
    try:
        results = run_configured_baseline_evaluations(
            workspace_root=args.workspace_root,
            baseline_names=names,
            output_root=output_root,
            device=args.device,
            progress=logger.info,
            log_every=args.log_every,
            postprocessing_batch_size=args.postprocessing_batch_size,
        )
    except Exception:
        logger.exception("baseline evaluation failed")
        raise
    finally:
        _close_progress_logger(logger)
    print(json.dumps({"status": "completed", "output_root": str(output_root), "log": str(log_path), "baselines": [result["baseline"] for result in results]}, indent=2))
    return 0


def _progress_logger(log_path: Path) -> logging.Logger:
    logger = logging.getLogger(f"abi_contrail.baseline_cli.{id(log_path)}")
    logger.setLevel(logging.INFO)
    logger.propagate = False
    formatter = logging.Formatter("%(asctime)sZ %(levelname)s %(message)s", datefmt="%Y-%m-%dT%H:%M:%S")
    formatter.converter = time.gmtime
    stream = logging.StreamHandler(sys.stderr)
    stream.setFormatter(formatter)
    file_handler = logging.FileHandler(log_path, mode="a", encoding="utf-8")
    file_handler.setFormatter(formatter)
    logger.addHandler(stream)
    logger.addHandler(file_handler)
    return logger


def _close_progress_logger(logger: logging.Logger) -> None:
    for handler in tuple(logger.handlers):
        handler.close()
        logger.removeHandler(handler)


if __name__ == "__main__":
    raise SystemExit(main())
