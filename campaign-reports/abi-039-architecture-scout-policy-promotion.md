# ABI-039 architecture-scout policy promotion

## Decision and scope

Human review approved replacing the ABI-034/ABI-036 onboarding ceilings with a staged architecture-feasibility envelope. This report activates only the resource-pilot and representative-scout stages. ABI-039 launches no Candidate Run, Post-Run Evaluation, Experiment Batch, or Autonomy Step.

The active envelope remains trusted Harness/provider policy. Candidate source and manifests cannot raise it, select capped records, own data loading, loss or metric definitions, Artifact Filters, Baseline Segmenter loading, sampling policy, scheduling, resource placement, or lifecycle behavior. Longitude and latitude remain prohibited Candidate inputs.

## Activated policy

| Policy dimension | Active trusted ceiling or rule |
| --- | --- |
| Representative records | 1,024 records per Dataset Source and Leakage-Safe Split using ABI-038 provider-owned selection |
| Resource pilot request | 32 records per Dataset Source and Leakage-Safe Split, one epoch; non-ranking evidence only |
| Epochs | 12 |
| Wall-clock timeout | 3,600 seconds, including trusted graceful-stop/forced-termination handling |
| Candidate batch size | 4 |
| Parameters | 25,000,000 |
| Prediction artifacts | Four using fixed `first_n` policy |
| Scheduler | `constant_lr` only |
| Early stopping | Disabled |
| Parallel Runs | One |
| GPU | Docker execution pinned to A100 device 0 with rootless-container-root mode |

The Harness may clamp command requests or reject manifests and handoffs at these limits. Candidate code cannot substitute a prediction policy, scheduler, early-stopping policy, record selector, GPU, or concurrency mechanism.

A new or materially different architecture family starts with the 32-per-source-and-split, one-epoch resource pilot and remains sequential. ABI-029's concurrency-two result applies only to comparable measured 2.54M-parameter spectral ResUNets; it is not a global Agent allowance. Concurrency requires a separately measured, compatible resource class and explicit trusted authorization.

## Representative-scout interpretation

The cap is applied independently after each Dataset Source and Leakage-Safe Split is constructed. ABI-038 policy `abi_representative_scene_positive_hash` version `v1`, provider seed `20260812`, uses trusted record metadata and stable hash ranking rather than raw prefix order. It preserves positive/negative coverage when possible, spreads selections over MIT scenes or Google provenance scene names, and records aggregate selection metadata and a stable identity digest without exposing record lists or coordinates.

The mounted snapshot contains 25,457 training records (MIT 4,928; Google 20,529) and 3,088 validation records (MIT 1,232; Google 1,856). Twelve epochs over 1,024 selected records from each training source expose 24,576 training observations, roughly one percent of the 2,545,700 record-exposures in 100 full-data epochs. The scout is therefore a feasibility/failure screen, not a reliable final ranking or promotion result.

Decisions are asymmetric. Elimination at 12 epochs requires hard failure, persistent collapse, clear optimization failure, or convincing plateau/divergence. A low score alone is insufficient. Low-scoring but improving, source-balanced, novel, noisy, or ambiguous trajectories remain eligible for a separately authorized extension; no strict top-k or absolute-Dice cutoff applies.

## Evidence and headroom

ABI-037's 14.33M-parameter, batch-4 bounded Run measured 73.88 training observations/s, 23.88 validation observations/s, about 958 MB peak CUDA reserved, and 44.65 seconds for three epochs of 256 training plus 256 validation observations. This supports batch 4 and leaves substantial A100 memory headroom, while the one-hour timeout deliberately allows architecture and validation-cost variation. It does not justify concurrency for unprofiled families.

The operator reports canonical MCAST 2.1 required approximately 3.7 hours for 100 epochs on this machine/A100. That evidence rejects a short full-data confirmation stage as likely under-training and supports keeping focused full-data work separately authorized.

## Inactive future transitions

A roughly 36-epoch extended representative scout is documented as the likely next stage for extension-eligible trajectories. Full-data focused training may later allow up to 100 epochs with a provisional eight-hour timeout and separately selected scheduler/early-stopping policy. Neither stage is active. Each requires measured evidence, a Workspace policy change, and separate human authorization.

## Retained human stops

Human review remains required for:

- any change to sample, epoch, batch, parameter, timeout, prediction, scheduler, early-stopping, concurrency, GPU, egress, mount, or other trusted limits;
- a new or changed Research Problem contract, provider/Harness ownership boundary, coordinate exclusion, loss, metric, Artifact Filter, Baseline Segmenter, data source, or sampling policy;
- an unprofiled concurrency/resource-class request, an action without applicable trusted bounds, or any unbounded action;
- promotion, deployment, production claims, baseline replacement, or treating representative-scout evidence as full-data evidence;
- recovery after non-finite state, timeout, forced termination, duplicate/lifecycle inconsistency, contract violation, unexpected resource retry, missing required artifact, coordinate exposure, Harness failure, campaign pause, or explicit `stop_for_human`.

Caller disconnect or stale state never authorizes replacement execution. Stable Run/Evaluation identities must be observed and reconciled idempotently; automatic replacement Runs and duplicate actions remain forbidden.

## Activation and validation

The machine-local Workspace Configuration activates the table above. The committed example mirrors the portable policy shape. Harness commit `c346f07aa4c837cdefcccf3fbe5fb675186efa2a` contains ABI-040 enforcement and Agent-visible staged guidance. Runtime images were rebuilt because the prior images identified the pre-ABI-040 Harness; the promoted runner is `ml-autoresearch-runner:abi-research-problem-44aa1c67f09ecad7-13b99524f1`.

Pre-activation execution counts were 14 Runs, 3 requested/completed Evaluations, one Experiment Batch, 91 Research Ledger events, no open Harness action, no managed container, and no GPU process. The only recorded Capability Request, `capreq_agent_boundary_typed_data_config_v1`, is historical and resolved by the typed boundary serialization already present in the active Harness.

Final runtime identity, Agent Control Boundary inspection, operational preflight, test results, and unchanged execution counts are recorded below after validation.

## Non-training boundary and operational validation

Runtime-image validation passed at `2026-08-12T21:18:23Z` for clean Harness commit `c346f07aa4c837cdefcccf3fbe5fb675186efa2a`, fingerprint `44aa1c67f09ecad7`, runner `ml-autoresearch-runner:abi-research-problem-44aa1c67f09ecad7-13b99524f1`, and Workspace Configuration SHA-256 `a2b30bfbde6a49e1b898efef9a0999563db245069f3b50e45c1518c3e104cdae`. Docker GPU validation saw PyTorch 2.5.1+cu121, CUDA 12.1, and the A100. Rootless Docker security is active.

`prepare-agent-boundary` completed after the report and linked `campaign_resumed` event were recorded. Inspection confirmed:

- generated `agent-work/ml-autoresearch.toml` contains 1,024 samples, 12 epochs, batch 4, constant LR only, disabled early stopping, 3,600 seconds, concurrency one, four `first_n` predictions, and 25M parameters;
- the generated TOML reloads with typed booleans, integers, source arrays, and the expected policy, proving the historical typed-data-config Capability Request is resolved;
- generated `agent-work/AGENTS.md` exposes all effective limits, representative selection, the one-epoch pilot, asymmetric elimination, sequential-family rule, and separate full-data authorization;
- `/reference/EXPERIMENT_INDEX.md` contains the ABI-039 authorization and `/history/research-ledger.jsonl` ends with its report and resume events;
- `/history/runs`, `/reference`, `/history`, `/docs`, and `/research-problem` remain read-only mounts; no raw training root is mounted into the Agent boundary.

Operational preflight passed: configured training, ancillary, baseline, and Runs roots exist; canonical MCAST registry and 1.1/2.1 assets exist; Natural Earth ancillary metadata/assets exist; the rebuilt runner image exists; A100 device 0 was idle with no compute process; no managed container existed; no campaign pause was active; and `execute-open-actions --dry-run` reported no open action. ABI and Harness worktrees began clean and at zero upstream divergence. The ABI worktree is intentionally dirty only with ABI-039 policy/report/index/test/ledger changes; Harness remains clean and pushed.

Final non-scientific counts are 14 Runs, three requested/completed Evaluations, one created/completed Experiment Batch, 14 Candidate submissions/starts, four ingested Agent handoffs, and 94 ledger events. Compared with the pre-activation snapshot, only two `campaign_report_written` events (initial registration and reviewed validation update) and one `campaign_resumed` event were added. Run, Evaluation, Batch, Candidate lifecycle, and handoff counts did not change. No Autonomy Step was invoked.

## Tests

- `uv run pytest -q` in ABI: 133 passed.
- Focused Harness policy, direct/configured execution, Candidate contract, boundary, handoff, Autonomy Step, and batch suites: 186 passed.
- Full Harness suite with `ML_AUTORESEARCH_GVCCS_PROBLEM_ROOT=../gvccs-research-problem` and `ML_AUTORESEARCH_TEST_PROBLEM_ROOT=../test-research-problem`: 581 passed, 2 skipped, one known unrelated external GVCCS characterization failure because its stale fake Spec allows only `bce_dice` while a committed external Candidate selects `focal_bce_dice`.
- Workspace-template focused test: 2 passed.
- Runtime image build smoke, runtime identity validation, Docker CUDA/GPU validation, generated boundary config reload, dry-run open-action check, and `git diff --check`: passed.

## Residual risks and next task

- A one-hour timeout is conservative rather than calibrated for every possible architecture; the first real resource pilot must measure throughput, peak allocation/reservation, and timeout headroom before a representative scout is authorized for that family.
- Representative selection improves bounded-study validity but cannot make a one-percent exposure budget equivalent to full-data training.
- Prediction artifacts remain bounded qualitative evidence and must be interpreted with aggregate and source-stratified metrics and provider-owned non-degeneracy assessment.
- The 36-epoch and full-data stages remain inactive.

A separate backlog task must authorize the first 32-per-source-and-split, one-epoch calibration Run. It should preregister one Candidate family, verify clean/pushed ABI and Harness identities, run exactly one sequential Candidate on pinned A100 device 0, record resource/non-degeneracy evidence, reconcile exactly once, and stop before a 12-epoch scout decision.
