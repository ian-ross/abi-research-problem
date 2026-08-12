# ABI-037 first post-onboarding bounded Autonomy Step

## Scope and authorization

ABI-036 durably authorized routine bounded autonomy without per-step chat approval while retaining trusted ceilings and human stops for policy changes, unbounded actions, promotion, and numerical/lifecycle/contract failures. The operator then requested one boundary refresh and one Autonomy Step.

This task invoked exactly one:

```bash
uv run ml-autoresearch autonomy-step --workspace-root . --execute-next-action
```

It did not invoke a second step, Post-Run Evaluation, Experiment Batch, or replacement Candidate.

## Preflight and boundary refresh

Before the step:

- ABI commit `240fef02de53a86dde205bf9c1d745ab5405c1cf` was clean, pushed, and at zero upstream divergence;
- Harness commit `a38ad742e187e23b1fa13f7b0ec8bd21da7ad637` was clean, pushed, and at zero upstream divergence;
- runtime validation passed at `2026-08-12T15:11:41Z` for Harness fingerprint `4ee2c56b94e3a8e8`, runner `ml-autoresearch-runner:abi-research-problem-4ee2c56b94e3a8e8-13b99524f1`, and Workspace Configuration SHA-256 `28586fdcc017ae955829f8658f6baa407910434645417e92f4e4d2bf0a23a430`;
- the Research Ledger ended with `campaign_resumed(reason=bounded_autonomy_authorized_after_abi035_onboarding)` linked to `campaign-reports/abi-036-bounded-autonomy-authorization.md`;
- there were 13 Runs, 3 Evaluations, 83 ledger events, no open Harness action, no GPU process, and no managed container;
- all existing primary handoffs had ingestion markers.

`prepare-agent-boundary` refreshed `/reference` and `/history`. Inspection proved that `/reference/EXPERIMENT_INDEX.md` exposed the active authorization and `/history/research-ledger.jsonl` contained its resume event. Egress and the full read-only `/history/runs` mount remained unchanged.

The generated Agent policy retained:

- 128 training and validation samples per Dataset Source per epoch;
- at most three epochs;
- concurrency one;
- two `first_n` predictions;
- 25,000,000 parameters;
- trusted 1,800-second Docker training timeout;
- managed Docker execution pinned to A100 GPU 0 with rootless-container-root mode.

## Handoff and action

The Agent returned code 0 and created exactly one Candidate Submission:

- Candidate: `abi037_mcast11_bce_dice_cldice_v1`;
- handoff source: `agent-work/submissions/abi037_mcast11_bce_dice_cldice_v1`;
- canonical path: `candidates/abi037_mcast11_bce_dice_cldice_v1`;
- requested experiment: change trusted loss from ABI-032 `focal_tversky` to `bce_dice_cldice` while retaining architecture, inputs, sampling, optimizer, learning rate, batch size, and epochs.

Static validation passed. The Candidate tree SHA-256 is `f6f5adb84d0376561249d0c2a57874961eddd7bb4fd5e3056263e3aa0e4ae61c`; the immutable Run snapshot matches it. `model.py` differs from ABI-032 only in names/docstrings and remains executable-architecture equivalent. The manifest's sole experimental factor is trusted loss `focal_tversky` to `bce_dice_cldice`.

The Harness ingested the handoff and executed its one `run_candidate` action. `agent-work/autonomy-step-result.json` records:

- `status: ingested`;
- `executed_next_action: true`;
- stable Run ID `run_20260812_151543_5b9508`;
- initial status `training` and managed state `supervisor_running`;
- next action advanced to `reconcile_run`.

No launch command was repeated. The same Run ID was observed and, after its sole container exited, reconciled twice idempotently.

## Execution and policy evidence

Run `run_20260812_151543_5b9508` completed through the trusted Docker lifecycle:

- runner `ml-autoresearch-runner:abi-research-problem-4ee2c56b94e3a8e8-13b99524f1`;
- A100 GPU device 0;
- rootless-container-root mode;
- `--max-samples 128` applied per Dataset Source;
- batch size 4 and three epochs;
- two `first_n` prediction samples;
- 1,800-second timeout recorded;
- one container attempt, exit 0, removed, cleanup completed;
- no timeout, forced termination, OOM, rejection, failure classification, or resource retry (`retry_count: 0`).

Each epoch processed 256 training and 256 validation observations: 128 MIT plus 128 Google under provider-owned per-source limiting. Total processed counts were 768 training and 768 validation observations.

The model summary records 14,328,209 parameters, `abi_16ch` source indices 0-15, and explicit exclusion of longitude, latitude, and source indices 16-17. Training, ancillary, and baseline mounts were read-only. Postprocessing produced three atomic epoch reports using bounded `torch_cuda` batches of 8 without full-validation GPU residency.

Resource evidence:

- Run operation: 44.65 seconds;
- training: 768 observations in 10.40 seconds (73.88/s);
- validation: 768 observations in 32.16 seconds (23.88/s);
- peak CUDA allocated/reserved: 945,349,632 / 958,398,464 bytes;
- free CUDA memory at start: 41,855,287,296 bytes.

A recursive audit parsed 207 JSON/JSONL records and 1,202 numeric values; all were finite. The selected checkpoint contained 184 tensors and 14,339,829 values, all finite. No non-finite diagnostic exists. The ledger contains exactly one `candidate_submitted`, one `run_started`, and one `run_completed` event for the stable Run. Reconciliation added no duplicate terminal event. Final counts are 14 Runs and 3 Evaluations. There were 89 lifecycle ledger events before report registration; initial registration and the reviewed report update added two `campaign_report_written` events, bringing the ledger to 91. No open action remains.

## Scientific result and branch decision

The Run was operationally reliable but scientifically poor under the bounded comparison.

| Stratum | Filtered Dice | Filtered precision | Filtered recall | Reported filtered connectivity |
| --- | ---: | ---: | ---: | ---: |
| Aggregate | 0.000123 | 0.022857 | 0.0000618 | 0.511727 |
| Google | ~7.72e-12 | ~7.14e-10 | ~7.81e-12 | 0.523438 |
| MIT | 0.000154 | 0.114286 | 0.0000770 | 0.500016 |

Compared with ABI-032 under the same 128-per-source/three-epoch policy, aggregate filtered Dice fell from 0.0462 to 0.000123, filtered precision fell from 0.0251 to 0.0229, and filtered recall collapsed from 0.2925 to 0.0000618. Google raw/filtered Dice is at the all-negative numerical floor. Both bounded prediction masks contain zero positive and 65,536 negative pixels.

The reported connectivity near 0.5 is not evidence of useful connected contrails in this state: ordinary Dice/recall and the bounded masks show near-total/all-negative collapse. Connectivity must not be interpreted independently of non-degeneracy evidence.

The Candidate's preregistered success criteria fail and its hard stop applies to this exact `bce_dice_cldice` branch. Do not repeat or promote this Candidate. The result is finite and contract-compliant, so it remains valid negative scientific evidence rather than a Harness failure. A future bounded Autonomy Step may broaden to a separately proposed augmentation, input policy, or architecture family under the existing ABI-036 authorization; ABI-037 itself does not launch that step.

## Residual risks

- The two `first_n` samples are bounded evidence, but their all-negative masks agree with the source-stratified Google numerical floor and aggregate recall collapse.
- The connectivity formulation yields a high value in a near-empty regime; future hypothesis selection must gate connectivity interpretation on predicted-positive/non-degeneracy evidence.
- Resource Failure retry support remains structurally enabled although no retry occurred.
- The resolved manifest reports provider commit `240fef0` as dirty because handoff ingestion created the canonical Candidate and appended tracked ledger/index state before Run submission. The clean pushed preflight revision and immutable Candidate checksum preserve the relevant identities.
- This bounded Run is not promotion-grade evidence.

## Validation and independent review

- Full ABI suite: 114 passed.
- Focused Harness autonomy, boundary, handoff, submission, configuration, reconciliation, and research-loop suite: 123 passed.
- Static Candidate validation: passed.
- Normalized AST comparison with ABI-032: executable architecture equal after Candidate/class-name and docstring normalization.
- Runtime identity, boundary authorization visibility, terminal artifact, finite numeric/checkpoint, prediction-mask, ledger exactly-once, post-step open-action, GPU-idle, and container-cleanup inspections passed.

A separate read-only Pi session reviewed the authorization, task, report, index, ledger, handoff result, Candidate, and terminal artifacts. It found no blocker/high issue and assessed all five ABI-037 acceptance criteria as passed after normal task metadata synchronization. Its low findings are retained as residual risks: `autonomy-step-result.json` captures the initial managed-running state rather than terminal reconciliation; provider revision metadata is dirty after expected handoff/ledger mutations; resource-retry support remained enabled with zero retries; and the reviewed evidence has no separate immutable Autonomy Step ID beyond the singleton result, one ingestion event, and one Run lifecycle. The reviewer agreed that the scientific state is near-total/all-negative collapse, the high connectivity value is not useful evidence in that regime, and this exact loss branch should stop.

## Commands

```bash
uv run ml-autoresearch validate-runtime-images --workspace-root .
uv run ml-autoresearch execute-open-actions --workspace-root . --dry-run --max-actions 10
uv run ml-autoresearch prepare-agent-boundary --workspace-root .
uv run ml-autoresearch autonomy-step --workspace-root . --execute-next-action
uv run ml-autoresearch run-status --workspace-root . --run-id run_20260812_151543_5b9508
uv run ml-autoresearch reconcile-run --workspace-root . --run-id run_20260812_151543_5b9508
uv run ml-autoresearch validate-candidate \
  --candidate candidates/abi037_mcast11_bce_dice_cldice_v1 \
  --workspace-root .
```
