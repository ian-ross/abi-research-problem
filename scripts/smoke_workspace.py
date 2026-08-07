"""Smoke-test the configured ABI Candidate Execution Boundary without training."""

from __future__ import annotations

import argparse
import json
import tempfile
from pathlib import Path

from ml_autoresearch.candidate_execution_config import (
    execution_backend_from_config,
    load_candidate_execution_config,
    load_configured_research_problem_registry,
)
from ml_autoresearch.runs import RunStatus, submit_candidate
from ml_autoresearch.runtime_images import require_runtime_image_validation


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace-root", type=Path, default=Path("."))
    parser.add_argument(
        "--candidate",
        type=Path,
        default=Path("tests/fixtures/candidates/abi_tiny_smoke"),
    )
    args = parser.parse_args()

    root = args.workspace_root.resolve()
    require_runtime_image_validation(root)
    config = load_candidate_execution_config(root)
    registry = load_configured_research_problem_registry(root)
    if registry is None:
        raise SystemExit("workspace has no configured Research Problem provider")
    backend = execution_backend_from_config(config)

    with tempfile.TemporaryDirectory(prefix="abi-workspace-smoke-") as temporary:
        temporary_root = Path(temporary)
        run = submit_candidate(
            args.candidate.resolve(),
            temporary_root / "runs",
            backend=backend,
            ledger_path=temporary_root / "research-ledger.jsonl",
            require_proposal=False,
            research_problem_registry=registry,
        )
        payload = {
            "status": run.status.value,
            "run_id": run.run_id,
            "candidate": str(args.candidate.resolve()),
            "backend": config.backend,
            "docker_image": config.docker_image if config.backend == "docker" else None,
            "trained": False,
        }
        print(json.dumps(payload, indent=2, sort_keys=True))
        return 0 if run.status == RunStatus.ACCEPTED else 1


if __name__ == "__main__":
    raise SystemExit(main())
