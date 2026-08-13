# ABI-043 Independent Read-Only Review

## Review

### Blockers

- **No substantive blocker found.** The evidence supports ABI-043 as a successful contract/resource/finite/non-degeneracy pilot.
- **Procedural closeout remains:** ABI-043 is still `In Progress`, all acceptance boxes remain unchecked, and its notes still say no Run has launched (`backlog/tasks/abi-043 - Run-the-first-promoted-architecture-resource-pilot.md:4,30-38,60`). The campaign report also says independent review is pending (`campaign-reports/abi-043-first-promoted-architecture-resource-pilot.md:131`). These are expected before this review, but must be synchronized through the Backlog CLI before marking the task Done.

### Correct

- **Materially different family:** The Candidate is a randomly initialized, 16-channel SMP DeepLabV3+ with ResNet-18, distinct from the prior U-Net families. Its source fixes `encoder_weights=None`, `in_channels=16`, and `classes=1` (`candidates/abi043_fullspectral_deeplabv3plus_resource_pilot_v1/model.py:9-88`).
- **Coordinate boundary:** Runtime model evidence restricts source indices to 0–15 and explicitly forbids longitude/latitude indices 16/17 (`/data/iross/abi-ml-autoresearch/runs/run_20260813_131515_ff53ab/outputs/model_summary.json:1-80`).
- **Exact reduced budget:** Trusted local policy sets `max_samples=32`, `max_epochs=1`, batch ceiling 4, concurrency 1, GPU 0, and a 3,600-second timeout (`ml-autoresearch.toml:19,26,32,34,39,42-44`). The Candidate manifest requests one epoch but contains no record cap, selector, source override, or selector seed (`candidates/abi043_fullspectral_deeplabv3plus_resource_pilot_v1/manifest.yaml:1-15`).
- **Exact source/split realization:** Run metadata records `requested_cap_per_source_split: 32` and `selected_count: 32` for MIT train, MIT validation, Google train, and Google validation (`run_metadata.json:25,44,65,91,112`). The registered selector is `abi_representative_scene_positive_hash` v1, seed `20260812`, scoped independently per Dataset Source and Leakage-Safe Split.
- **Exactly one epoch:** The manifest and Workspace maximum are both one; terminal metadata records `epochs_completed: 1` and `stop_reason: max_epochs_reached` (`run_metadata.json:477-485`). Metrics contain only epoch 1, with 16 training batches at effective batch 4 for 64 total training observations (`outputs/metrics.jsonl`).
- **Exactly-once lifecycle:** The ledger contains one ABI-043 `agent_handoff_ingested`, one `candidate_submitted`, one `run_started`, and one `run_completed`, with no ABI-043 `run_failed` (`research-ledger.jsonl:97-102`). There are 15 Run directories, consistent with the documented 14-directory preflight baseline plus this single Run.
- **Single container attempt/no retry:** `execution.json` records attempt 1, successful exit, removal, finalized state, and terminal status `completed` (`execution.json:3-55`). Run metadata records one completed resource attempt and `retry_count: 0` (`run_metadata.json:459-472`).
- **No Evaluation, Batch, or scout:** No evaluation artifacts exist under this Run. ABI-043 ledger events end at the single `run_completed`; evaluation and batch events in the ledger predate ABI-043. The only ABI-043 Run completed one epoch, so no 12-epoch scout occurred.
- **Static/runtime contract and parameter evidence:** Smoke testing was accepted at 12,370,065 parameters (`outputs/logs/smoke_test.log`). Model summary records a finite-shaped `(2,1,256,256)` output contract under the 25M ceiling (`outputs/model_summary.json:61-80`).
- **Resource evidence:** Batch 4 completed on A100 GPU 0 with 463,730,688 bytes peak allocation and 528,482,304 bytes peak reservation. Training throughput was 38.26 samples/s, validation throughput 14.79 samples/s, and profiled Run work was 8.06 seconds (`outputs/resource_profile.json:2-23`). Managed wall time was about 23.68 seconds against 3,600 seconds, leaving substantial timeout headroom (`execution.json:26-55`; campaign report line 105).
- **Finite/checkpoint evidence:** Losses and all reported metrics are finite. The report records a recursive audit of 27 JSON/JSONL records and 516 numeric values, plus 183 checkpoint tensors containing 12,383,918 finite values (`campaign-reports/abi-043-first-promoted-architecture-resource-pilot.md:107`). The checkpoint exists at `outputs/models/best_epoch_model.pt`.
- **Source-specific non-degeneracy:** Aggregate, Google, and MIT predicted-positive fractions are all strictly between zero and one in raw and filtered metrics (`outputs/best_metrics.json`). The report additionally records positive counts of 4,685, 30,153, 3,698, and 15,156 out of 65,536 for the four bounded masks (`campaign-reports/abi-043-first-promoted-architecture-resource-pilot.md:117`), excluding gross all-negative/all-positive behavior in those samples.
- **Interpretation is appropriately limited:** Both the campaign report and Experiment Index explicitly prohibit ranking, promotion, elimination from the low one-epoch score, concurrency authorization, or automatic continuation (`campaign-reports/abi-043-first-promoted-architecture-resource-pilot.md:121`; `EXPERIMENT_INDEX.md:7-8,25`).

### Controlled-factor deviation determination

**Severity: residual comparison risk; not an ABI-043 acceptance blocker.**

The outer protocol intended no augmentation and AdamW at `0.001` (`campaign-reports/abi-043-first-promoted-architecture-resource-pilot.md:24`). The Agent’s concrete proposal instead selected provider-owned `random_mirroring` and AdamW at `0.0003` (`candidates/abi043_fullspectral_deeplabv3plus_resource_pilot_v1/PROPOSAL.md:23-24`; `manifest.yaml:9,13`).

This was preregistered before execution: `proposal_created` occurred at `13:15:15Z`, before `candidate_submitted` at `13:15:22Z` and `run_started` at `13:15:23Z` (`research-ledger.jsonl:98,100-101`). Both choices came through trusted contract surfaces rather than Candidate-owned transforms or training code.

Consequently:

- It does **not** invalidate the stated contract/resource/finite/non-degeneracy purpose.
- It does **not** violate the exact-32, one-epoch, lifecycle, artifact, or interpretation acceptance criteria.
- It **does** invalidate any claim that architecture/input representation were the only changed scientific variables relative to ABI-031.
- A later scout must preregister whether to retain these settings or restore no augmentation/`0.001`; results across those settings must not be treated as a clean architecture-only comparison.

### Notes

- `agent-work/autonomy-step-result.json` is a launch-time record and therefore still reports `supervisor_running` with `next_action: reconcile_run`. Current terminal state is instead established by the stable Run’s finalized `execution.json`, the single ledger completion event, and the campaign report’s reconciliation/open-action attestation. The stale launch snapshot is not itself evidence of an unresolved current action.
- The finite checkpoint audit, bounded-mask pixel counts, repeated reconciliation, open-action check, and pre/postflight GPU checks are summarized in the durable report rather than retained as separate machine-readable audit artifacts. This meets the requested attested evidence level but limits later independent re-audit without rerunning read-only inspection tools.
- Reported validation totals—133 ABI tests and 135 focused Harness tests—were inspected in the report but not rerun during this read-only review (`campaign-reports/abi-043-first-promoted-architecture-resource-pilot.md:127-129`).

## Acceptance-Criteria Assessment

| AC | Assessment | Evidence |
|---|---|---|
| #1 | **Satisfied** | Family, hypothesis, controlled factors, success evidence, and stop conditions are documented in the campaign report and Candidate proposal. |
| #2 | **Satisfied** | Trusted config enforces 32/source/split and one epoch; terminal metadata shows all four selected counts equal 32 and one completed epoch. |
| #3 | **Satisfied, attested** | Campaign report records clean pushed ABI/Harness revisions, boundary synchronization, named roots, idle GPU, and no preflight action/container. Runtime validation metadata independently corroborates the clean Harness commit, image identity, and Workspace checksum. |
| #4 | **Satisfied** | One autonomy result, one submission, one stable Run, one container attempt, zero retries, and no ABI-043 Evaluation or Batch. |
| #5 | **Satisfied, attested** | Stable Run is finalized; ledger lifecycle is exactly once; container was removed. Idempotent reconciliation and no-open-action state are explicitly recorded in the campaign report. |
| #6 | **Satisfied** | Finite/checkpoint audit, parameter count, throughput, wall time, GPU peaks, batch result, source metrics, predicted-positive evidence, selector identity, and timeout headroom are all recorded. |
| #7 | **Satisfied** | Report, Candidate docs, and Experiment Index consistently restrict interpretation to pilot evidence. |
| #8 | **Satisfied upon persistence of this review** | Durable campaign report, Experiment Index, ledger events, validation results, and residual risks exist; this artifact supplies the pending independent review. Backlog/report status text still requires closeout synchronization. |
| #9 | **Satisfied** | Only one epoch ran; no second Run, scout, extension, evaluation, promotion, concurrency change, or policy-limit increase is evidenced. |

## Residual Risks

1. The augmentation/LR deviation prevents clean architecture-only comparison with ABI-031.
2. One epoch over 32 records per source/split is insufficient for ranking, promotion, elimination, or optimization conclusions.
3. Four bounded masks establish only narrow sample-level non-degeneracy.
4. Resource retry remains structurally enabled, although this Run used zero retries; future protocols requiring an absolute no-retry mechanism should address that distinction.
5. Resource evidence supports batch 4 on one A100 Run only and does not establish concurrency safety.
6. Some operational and finite/checkpoint audits are report attestations rather than standalone retained audit outputs.
7. Task metadata remains intentionally pre-closeout and must be updated through the Backlog CLI after this review is accepted.