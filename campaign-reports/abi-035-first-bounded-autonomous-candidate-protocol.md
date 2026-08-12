# ABI-035 first bounded autonomous Candidate execution protocol

## Status and authorization boundary

This protocol preregisters the first bounded automatic Candidate execution after ABI-034. It records evidence and stop rules **before** launch. It does not itself authorize training.

Human Gate 0 may authorize exactly one invocation of:

```bash
uv run ml-autoresearch execute-next-action --workspace-root .
```

That invocation may create exactly one stable Run for the existing open `run_candidate` action and start its trusted detached managed execution. A caller disconnect, nonzero return, timeout, stale result file, or incomplete host finalization does not authorize another invocation, another Candidate, an automatic retry, or a replacement Run. Once a Run ID exists, observation and recovery are limited to `run-status` and idempotent `reconcile-run` for that same Run ID.

No Post-Run Evaluation, second Candidate, Experiment Batch, automatic iteration, or subsequent Autonomy Step is authorized by Gate 0.

## Preserved revisions and runtime identity

The execution-bearing ABI-034 source and Candidate state is durably preserved on `origin/main` through ABI commit `c8adf5cded0d5058f6ad50fb4b14177c1638dbf1`; the substantive ABI-034 trial commit is `696bc929a5f1afa67b03d9c50b64c75f119c3708`. ABI-035 task/protocol commits must also be pushed and the worktree must be clean before launch. The operator will record the exact clean launch-time ABI HEAD in Gate 0 evidence and the resulting Run metadata.

The trusted Harness is clean commit `a38ad742e187e23b1fa13f7b0ec8bd21da7ad637` on `main`, equal to `origin/main`.

Runtime validation completed at `2026-08-12T11:58:40Z` with:

- Harness fingerprint: `4ee2c56b94e3a8e8`;
- runner: `ml-autoresearch-runner:abi-research-problem-4ee2c56b94e3a8e8-13b99524f1`;
- Workspace Configuration SHA-256: `28586fdcc017ae955829f8658f6baa407910434645417e92f4e4d2bf0a23a430`;
- Harness Git state: clean;
- configured backend: Docker with GPU enabled, pinned device `0`, and rootless-container-root mode.

Any Harness revision, ABI execution-bearing code/config change, runner identity change, or dirty worktree invalidates this record. Revalidate and return to human review rather than launching.

## Exact open action and Candidate

`execute-open-actions --dry-run --max-actions 10` reported exactly one action and executed none:

- ledger index: `73` (zero-based; Research Ledger line 74);
- created at: `2026-08-12T10:55:24Z`;
- handoff type: `candidate_submission`;
- action: `run_candidate`;
- Candidate ID: `abi032_mcast11_focal_tversky_v1`;
- canonical path: `candidates/abi032_mcast11_focal_tversky_v1`.

`agent-work/autonomy-step-result.json` independently records `status: ingested`, `executed_next_action: false`, and `execution: null` for the same action.

Canonical Candidate tree SHA-256: `fbcf6294e7350286bfa734382d63b45ad0ed466f86d6e359b07253fdf6adf333`.

| File | SHA-256 |
| --- | --- |
| `manifest.yaml` | `61ffe4a102d1b6523296cb705dd89bdd3afa7a3710fc38b4d5c356a1a3833a2b` |
| `model.py` | `e9b6b3bba8de5f5a1f1ea89039b0742f0b08af0f6003d1e2b3b0825ec221518b` |
| `PROPOSAL.md` | `d548767967acf0a30b13c10c547d1304e31fceaf6395a5c198390b02edd67c50` |
| `README.md` | `3350db0c0939f09e9fe16f5647caa1a09c8fae6dc0e2327631d82e2d770afa05` |

Static Candidate validation passed. A normalized AST comparison against `abi031_mcast11_positive_control_v1/model.py` proves the executable architecture is identical after normalizing Candidate/class names and docstrings. The manifest differs only in Candidate identity/description and trusted primary loss `bce_dice` to `focal_tversky`. The model imports only Python future annotations, `segmentation_models_pytorch`, and `torch`; it contains no file/network access, checkpoint or Baseline Segmenter loading, runtime download, data loading, loss, metric, Artifact Filter, sampling, optimizer, device, retry, training-loop, or persistence ownership.

The model receives only `abi_16ch`, uses source indices 10, 13, 12, and 14 to derive C11, C14, and C13-C15, and has no longitude/latitude path. Provider source indices 16 and 17 remain forbidden. Random initialization remains enforced by `encoder_weights=None`.

## Fixed execution bounds

The single Run is preregistered with these trusted ceilings and effective policies:

- Docker managed lifecycle only;
- A100 GPU device 0 only, sequential execution, concurrency one;
- `combined_source_balanced` sampling owned by the provider;
- at most 128 training samples **per Dataset Source per epoch** (256 combined);
- at most 128 validation samples **per Dataset Source per epoch** (256 combined);
- batch size 4;
- at most three epochs;
- at most 768 combined training observations and 768 combined validation observations across three full epochs;
- exactly the configured maximum of two bounded prediction samples using `first_n`;
- trusted Docker training wall-clock timeout of 1,800 seconds, followed only by the Harness's fixed graceful-stop/forced-termination lifecycle;
- maximum 25,000,000 parameters; expected architecture count 14,328,209;
- no Experiment Batch and no resource-failure retry is acceptable for this reliability trial.

The 1,800-second value is a failure ceiling, not permission to resubmit after caller timeout or disconnect.

## Pre-launch snapshot and commands

At preregistration:

- Run directory count: 12;
- Evaluation count: 3 (top-level `outputs/evaluations/eval_*` directories; diagnostic subdirectories excluded);
- Research Ledger lines: 74;
- GPU 0: NVIDIA A100-PCIE-40GB, 40,960 MiB total, 0 MiB used, 0% utilization;
- GPU 1: Tesla T4, not selected;
- compute-process query: no active process;
- managed Docker container query: no ABI/ml-autoresearch container.

Immediately before launch the operator must repeat and capture:

```bash
git status --short --branch
git rev-parse HEAD
git -C ../ml-autoresearch status --short --branch
git -C ../ml-autoresearch rev-parse HEAD
uv run ml-autoresearch validate-runtime-images --workspace-root .
uv run ml-autoresearch validate-candidate \
  --candidate candidates/abi032_mcast11_focal_tversky_v1 \
  --workspace-root .
uv run ml-autoresearch execute-open-actions \
  --workspace-root . --dry-run --max-actions 10
nvidia-smi --query-gpu=index,name,uuid,memory.total,memory.used,utilization.gpu \
  --format=csv,noheader
nvidia-smi --query-compute-apps=gpu_uuid,pid,process_name,used_memory \
  --format=csv,noheader
```

The preflight must still show clean preserved revisions, the validated runtime identity/config checksum above, no GPU workload, baseline counts 12 Runs/3 Evaluations/74 ledger lines, and exactly the one matching open action. Any mismatch stops for review.

## Stable-Run and no-resubmission procedure

After explicit Gate 0 authorization, invoke `execute-next-action` exactly once. Capture stdout/stderr, exit status, and the stable Run ID. The expected successful immediate result is a managed Run in `training` state, not necessarily a terminal Run, because Docker continuation is detached.

After a Run ID appears, use only:

```bash
uv run ml-autoresearch run-status --workspace-root . --run-id <RUN_ID>
uv run ml-autoresearch reconcile-run --workspace-root . --run-id <RUN_ID>
```

`reconcile-run` may be used only after the recorded managed container has exited or durable state requires finalization. It is idempotent and never creates a Run. Do not rerun `execute-next-action`, `execute-open-actions`, `run-candidate`, or `autonomy-step`; do not delete/replace Run metadata; and do not clean or replace `agent-work/autonomy-step-result.json`.

If no Run ID is visible after caller failure, inspect the Research Ledger, configured Runs root, managed execution records, and open-action dry run. A `candidate_submitted` event or newly created Run establishes the stable identity and forbids resubmission.

## Expected terminal evidence

A passing Run must contain and consistently link at least:

- `run_metadata.json`, `execution.json`, `resolved_manifest.yaml`, and immutable `candidate/` snapshot;
- `outputs/logs/smoke_test.log`, `supervisor.log`, `training.log`, and `validation.log`;
- `outputs/model_summary.json`;
- `outputs/metrics.jsonl`, `final_metrics.json`, and `best_metrics.json`;
- `outputs/models/best_epoch_model.pt`;
- `outputs/resource_profile.json` and the effective batch resource profile;
- `outputs/validation_postprocessing/index.json` and one atomic report per completed epoch;
- `outputs/prediction_samples/samples.json` and two bounded sets of input, truth, probability, prediction, and overlay artifacts;
- no `outputs/nonfinite_diagnostic.json`;
- one candidate-submission/Run lineage and exactly one terminal Research Ledger event.

Terminal review must verify the immutable Candidate tree checksum; resolved trusted loss and policy; Docker image/GPU 0/rootless execution; one container attempt and completed cleanup; read-only training, ancillary, and baseline mounts; `abi_16ch` source indices 0-15 with longitude/latitude explicitly forbidden; parameter count; batch/sample/epoch ceilings; timeout state; effective resource retry count zero; resource/timing profile; bounded postprocessing backend, batch size, timings, progress reports, and filter order; and all expected artifacts.

## Preregistered numerical and lifecycle continuation gate

The Run passes the ABI-035 reliability continuation gate only if every item below is evidenced:

1. Status terminalizes exactly once as `completed`; there is exactly one `candidate_submitted`, one `run_started`, and one `run_completed` event for the stable Run ID, with no `run_failed` event or duplicate lineage.
2. The single managed container exits successfully and is removed. No timeout request, graceful timeout termination, forced termination, resource retry, replacement Run, or unexpected GPU/concurrent workload occurs.
3. All numeric values in smoke output, every training/validation metric record, final/best metrics, postprocessing reports, and resource profile are finite.
4. Trusted per-step finite checks complete without a non-finite diagnostic, proving finite outputs, losses, gradients, and parameters. Every tensor in the selected checkpoint is independently loaded on CPU and checked finite.
5. Exactly three epochs complete; no more than 128 train and 128 validation samples per MIT/Google source per epoch are used; batch size remains 4; all aggregate processed counts match three epochs and the configured ceilings.
6. Aggregate and both MIT/Google source strata have raw and filtered Dice strictly greater than `0.0001`, the preregistered numerical floor above the observed all-negative regime. Their raw and filtered precision and recall must each be finite and strictly between 0 and 1, ruling out aggregate/source all-negative and all-positive behavior.
7. Each of the two bounded binary prediction masks contains both classes: positive pixels strictly greater than 0 and strictly fewer than 65,536.
8. All expected artifacts, provenance, mount, input exclusion, resource, timeout, postprocessing, and exactly-once evidence above are complete and mutually consistent.

A scientifically poor but finite, non-degenerate Result may pass this reliability gate. Any contract violation, Harness failure, missing artifact, non-finite state, checkpoint failure, coordinate exposure, all-negative/all-positive behavior, source collapse, timeout, forced termination, resource retry, lifecycle inconsistency, or incomplete evidence fails the gate and stops the campaign for human review.

## Interpretation and conditional continuation

This trial uses 128 training/validation samples per source, while ABI-031's main Run used 1,024 per source. Its metrics are directional autonomy/reliability evidence only. They are not promotion-grade, production-throughput evidence, baseline parity, or a directly comparable scientific result.

After terminal review, the operator will write a durable Run report and present Human Gate 1. Even a passing gate does not automatically authorize continuation. Only separate Gate 1 approval may authorize one boundary refresh and exactly one subsequent bounded `autonomy-step --execute-next-action`. A failed or incomplete gate stops ABI-035 before boundary refresh or another Autonomy Step.

## Pre-execution validation completed

- ABI focused provider/training/Candidate-boundary suite: 33 passed.
- Harness autonomy/config/reconciliation suite: 56 passed.
- Static Candidate validation: passed.
- Runtime-image identity validation: passed.
- Normalized architecture AST comparison: equal.
- Open-action dry run: exactly one matching action; zero executions.
