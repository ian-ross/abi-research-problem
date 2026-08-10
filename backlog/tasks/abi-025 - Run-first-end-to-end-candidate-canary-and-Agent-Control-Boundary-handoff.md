---
id: ABI-025
title: Run first end-to-end candidate canary and Agent Control Boundary handoff
status: In Progress
assignee:
  - '@agent'
created_date: '2026-08-09 21:13'
updated_date: '2026-08-10 15:58'
labels:
  - harness
  - candidates
  - agent-boundary
  - canary
dependencies:
  - ABI-027
priority: high
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Prove the complete ABI Candidate Experiment lifecycle after the canonical MCAST baselines are available. First isolate the trusted Candidate Execution path with a manually authored, bounded canary Candidate Experiment; then exercise Agent Control Boundary generation, handoff ingestion, and separately approved execution.

This task is deliberately staged with explicit Human Review Gates. Agent steps must stop at each gate and must not proceed until the human approves the next step. Real training must run only on the approved GPU/cluster environment, never as an unapproved local run.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 A manually authored canary Candidate Experiment has a reviewed PROPOSAL.md and valid candidate contract without candidate-owned data loading, losses, metrics, filters, sampling, or augmentation
- [x] #2 Static validation and a human-approved bounded Docker training/evaluation run succeed on the GPU/cluster environment
- [x] #3 The canary Run produces expected Run artifacts, Research Ledger/index records, provider-owned metrics, and an acceptance report tied to the canonical MCAST registry
- [x] #4 Validation confirms longitude and latitude are not Candidate Experiment inputs and trusted data/baseline/ancillary mounts remain read-only and boundary-owned
- [ ] #5 One Agent Control Boundary autonomy step is run without automatic next-action execution, and its single handoff is inspected and approved before any candidate execution
- [ ] #6 The approved Agent-generated handoff is executed separately and its Run artifacts and acceptance report are validated
- [ ] #7 A final human go/no-go decision is recorded before enabling or attempting a fully automatic autonomy iteration
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
## Phase 0 — Task approval
1. **Agent:** Review the current Harness configuration, canonical MCAST registry, Candidate contract, and existing smoke fixture. Propose the exact canary scope, sample bound, training bound, expected artifacts, validation checks, and GPU-server command. Do not create candidate code or run training.
2. **Human Review Gate 0:** Approve or revise the canary scope and execution bounds.

## Phase 1 — Manual candidate canary
3. **Agent:** After Gate 0 approval, create the minimal legitimate canary Candidate Experiment outside the Agent Control Boundary, including `PROPOSAL.md`, manifest, model source, and concise rationale. Candidate code must stay within the provider-owned boundaries. Do not run training.
4. **Human Review Gate 1:** Inspect the proposal, model, manifest, resource bounds, and forbidden-input/boundary assumptions. Approve static validation only.
5. **Agent:** Run static Candidate validation and non-training checks. Report results and provide the exact bounded Docker/GPU execution command. Do not start the training Run.
6. **Human Execution Gate 2:** Approve and launch the bounded canary Run on the GPU/cluster environment, or explicitly authorize the Agent to launch it there.
7. **Agent:** Inspect the completed Run without retraining. Validate Run state, ledger/index entries, raw and filtered metrics, source-stratified metrics, connectivity metrics, acceptance-gate output, canonical MCAST registry provenance, qualitative artifact bounds, and absence of longitude/latitude Candidate inputs.
8. **Human Review Gate 3:** Review the canary evidence and decide whether Candidate Execution is trustworthy enough to proceed to the Agent Control Boundary test.

## Phase 2 — Agent Control Boundary handoff
9. **Agent:** After Gate 3 approval, re-check Agent Control Boundary preparation and document the expected read-only inputs, writable handoff paths, network policy, and single permitted handoff outcome. Provide the exact `autonomy-step` command without `--execute-next-action`. Do not invoke it.
10. **Human Execution Gate 4:** Launch one Agent Control Boundary autonomy step without automatic next-action execution.
11. **Agent:** Inspect the ingested handoff, generated Candidate/proposal, boundary-visible context, ledger event, and outstanding Harness-owned action. Do not execute the Candidate. Report any unexpected access, mutation, extra handoff, or policy violation.
12. **Human Review Gate 5:** Approve, reject, or request revision of the Agent-generated handoff. Explicit approval is required before execution.
13. **Human Execution Gate 6:** Run `execute-next-action`, or explicitly authorize the Agent to run it, for the approved handoff only.
14. **Agent:** Inspect the resulting Run and validate the same artifact, metric, baseline-provenance, boundary, and ledger checks used for the manual canary. Produce a concise final campaign report with residual risks.
15. **Human Final Gate 7:** Record a go/no-go decision on attempting a future fully automatic autonomy iteration. A go decision does not itself launch that iteration.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
- Phase 0 review completed; no candidate code was created and no training/evaluation was run.
- Verified canonical registry abi-mcast-working-validation-v1 at /data/iross/abi-ml-autoresearch/baselines/canonical/mcast-working-validation-v1.json; both MCAST targets and referenced artifacts/assets passed checksum verification.
- Refreshed Runtime Image validation for runner ml-autoresearch-runner:abi-research-problem-fa7d66587648b241-13b99524f1 (Harness commit 2698af8).
- Proposed Gate 0 bound: abi_16ch tiny convolutional canary, sequential/no augmentation, bce_dice/AdamW, batch size 2, one epoch, --max-samples 8 (8 per source, 16 combined for each train and validation), two prediction samples; then one full 3,088-sample Docker/GPU post-run evaluation with four bounded diagnostic samples.
- Gate 0 caveats: run-candidate/evaluate-run CLI execution options must explicitly repeat configured Docker image/GPU/rootless policy; evaluate-run must explicitly target the workspace ledger because external runs_root inference would choose the wrong ledger; acceptance-report generation exists only as a trusted provider API, not a CLI/integrated evaluation artifact; direct run-candidate does not update EXPERIMENT_INDEX.md; and actual per-run mount flags are not persisted as a command-level attestation beyond Harness policy plus run metadata.

- Human Review Gate 0 approved.
- Created the manually authored canary at candidates/abi025_manual_canary_v1 with manifest.yaml, model.py, PROPOSAL.md, and README.md; added the pending candidate to EXPERIMENT_INDEX.md.
- Candidate model is architecture-only (approximately 1,169 parameters) and selects only trusted manifest options. No static Candidate validation, model import/smoke test, Docker execution, or training has been run. Awaiting Human Review Gate 1 approval for static validation only.

- Human Review Gate 1 approved static validation.
- Static Candidate validation passed with required PROPOSAL.md and README.md; the resolved manifest selects only goes_abi_contrail_segmentation allowlisted values.
- Static source audit passed: exactly four allowed files, only torch imports, and no filesystem, network, data-loader, longitude, or latitude identifiers. The first audit helper invocation incorrectly classified from torch import nn as a top-level nn module; the corrected audit passed and no candidate change was needed.
- Focused trusted-boundary validation passed: 21 tests covering provider spec, Candidate longitude/latitude boundary, workspace configuration, canonical baseline targets, and acceptance-gate reporting. Canonical MCAST registry verification passed again.
- No Candidate model import, smoke test, Docker candidate execution, evaluation, or training has been run. Awaiting Human Execution Gate 2.

- Human Execution Gate 2 authorized Agent launch. Docker/GPU Run run_20260810_110532_b465cf completed in one attempt on CUDA with 16 training and 16 bounded validation samples, one epoch, batch size 2, two prediction samples, and no resource retry.
- Controlled smoke accepted the 1,169-parameter [2,16,256,256] -> [2,1,256,256] model. Run source copy matches the reviewed canonical candidate; expected validation/smoke/training logs, metrics history, final/best metrics, checkpoint, and qualitative artifacts exist.
- Docker/GPU Post-Run Evaluation eval_20260810_110644_c0d61d completed without retraining on all 3,088 Working Validation samples (MIT 1,232; Google 1,856), with 19 raw/filtered thresholds and four diagnostic samples/eight GeoTIFFs.
- Trusted provider API wrote acceptance_report.json tied to verified registry abi-mcast-working-validation-v1 and canonical MCAST 2.1 aggregate/run-manifest paths. The deliberately weak canary predicted no positive pixels and correctly received aggregate, recall, and both Dataset Source failure flags; promotion remains human_review_required.
- Run model_summary records only ABI channels 1-16, explicitly forbids longitude/latitude and source indices 16/17, and the copied candidate contains no coordinate access. run_metadata records training, ancillary, and baselines mounts at /data/<name> with readonly=true and Harness-owned Docker/GPU/resource policy.
- Research Ledger contains proposal_created, candidate_created, candidate_submitted, run_started, run_completed, evaluation_requested, and evaluation_completed events. EXPERIMENT_INDEX.md now records the Run and Evaluation.
- Gate 3 residuals for human review: evaluation_metadata.json says backend=native because the Docker container dispatches the native evaluator internally, despite the outer CLI recording backend=docker; acceptance_report.json is provider-owned but is not listed in evaluation_metadata.json or separately ledger-recorded; Run provider Git provenance is dirty because the reviewed candidate/index are uncommitted; per-run Docker argv/mount flags are not durably attested beyond Harness policy and run_metadata; and the connectivity metric is high for the all-negative canary, so it is not meaningful as standalone quality evidence.

- Human Review Gate 3 approved proceeding to the Agent Control Boundary test.
- Re-ran prepare-agent-boundary successfully and refreshed reference/history/provider snapshots. Manual canary Candidate, index record, ledger events, Run, Evaluation, and acceptance report are visible through read-only history/reference mounts.
- Boundary preflight found no queued primary handoff files, no stale autonomy result/prompt files, and no open executable Harness actions. Default Pi command and ML_AUTORESEARCH_PI_FORT=/home/iross/code/pi-fort are available.
- Agent Control Boundary has allow_egress=true, no /data mounts, and read-only /reference, /history (including external Runs root), /docs, /research-problem, and Harness package mounts. Only the Agent Workspace draft/submission/note/request/report/scratch locations are writable.
- Gate 4 command is uv run ml-autoresearch autonomy-step --workspace-root . --agent-command "pi --session-dir ../agent-sessions" with no --execute-next-action. Expected safe outcome is exactly one ingested handoff; a Candidate Submission should leave next_action=run_candidate outstanding and unexecuted for Gate 5 review.

- PAUSED before Human Execution Gate 4 by human decision. The autonomy-step command has not been invoked and no Agent-generated handoff exists.
- Boundary review found that Agent-visible context is only partial: the manual canary Run exposes split counts, bounded qualitative samples, full-validation metrics, and selected MCAST 2.1 acceptance values, but the declared Dataset Profile Artifact is mostly generation instructions and the Agent cannot see complete curated MCAST 1.1/2.1 summaries, threshold/filter behavior, or canonical provenance.
- Created blocking task ABI-026 to add a trusted, read-only Agent-visible ABI dataset and MCAST campaign context artifact without mounting raw training data, coordinates, model weights, or the baselines root. Resume ABI-025 Phase 2 preparation only after ABI-026 is complete and the refreshed boundary context is reviewed.

- ABI-026 completed: the refreshed Agent Control Boundary now exposes required curated artifact /research-problem/abi_contrail/profile/agent-campaign-context.v1.json with ABI snapshot, canonical MCAST 1.1/2.1, threshold/Artifact Filter, and manual-canary context. Boundary validation confirmed read-only index exposure with no training, ancillary, or baselines roots mounted.
- ABI-025 remains paused before Human Execution Gate 4. The autonomy-step command has not been invoked; explicit human review/approval of the refreshed pre-Gate-4 boundary context is required before proceeding.

- Human Execution Gate 4 authorized and invoked exactly once with no --execute-next-action. The step ingested one Candidate Submission, abi_spectral_resunet_scout_v1, and left next_action=run_candidate unexecuted; no Run was created.
- Gate 5 candidate inspection: canonical and submitted Candidate copies match byte-for-byte; static validation with required proposal/README passes; manifest uses abi_16ch plus trusted combined_source_balanced/random_mirroring/focal_tversky/AdamW policies; model source is architecture-only and contains no longitude/latitude, data loading, loss, metric, filter, sampling, network, or persistence ownership. Exactly one primary handoff exists, with one agent_handoff_ingested ledger event and a pending run_candidate action.
- Gate 5 boundary inspection found a blocking isolation failure: the Agent session had no /reference guest mount and executed tools against the host root, where /data, /net, and host repository paths were visible. It directly read only intended history/reference/provider snapshot content and the approved Runs root, and transcript review found no raw training/baselines/ancillary reads or unexpected writes, but the Agent Control Boundary was not actually enforced. Handoff execution is not approved; ABI-027 created as a blocker to make autonomy-step fail closed and prove isolation before retry.

- After ABI-027, human authorized cleanup and one Gate 4 retry using the current Pi setup with no additional isolation changes. Preserved the first attempt's immutable submission, canonical Candidate, ledger event, and Pi session as audit evidence; marked the Candidate quarantined/do-not-execute in EXPERIMENT_INDEX.md; cleared only mutable draft, scratch, stale prompt, and stale result state.
- Preflight passed: prepare-agent-boundary refreshed snapshots/config; no un-ingested primary handoff existed; no autonomy command override was configured; plain `pi list` discovered project-local pi-fort.
- Invoked `uv run ml-autoresearch autonomy-step --workspace-root .` once without `--execute-next-action`. Pi session 2026-08-10T15-45-22-476Z_019fec59-982b-7067-8930-e55100dc11b6 recorded `Fort active` and used intended `/reference`, `/history`, `/research-problem`, and Agent Workspace paths.
- Retry produced `status=no_handoff`, no ledger events, and `next_action=stop_for_human`: the Agent correctly saw the previously ingested `abi_spectral_resunet_scout_v1` with no Run and refused to create a second artifact while that action remains pending. No Candidate execution or training occurred. AC #5 remains open pending a human decision on how to retire or handle the quarantined open action.

- Human authorized destructive cleanup of invalid test state. Removed the first Gate 4 `abi_spectral_resunet_scout_v1` canonical Candidate, immutable queue entry, EXPERIMENT_INDEX row, and `agent_handoff_ingested` ledger event, plus stale runtime/draft/scratch state; refreshed the boundary from an empty primary handoff queue.
- Clean retry invoked `uv run ml-autoresearch autonomy-step --workspace-root .` once without `--execute-next-action`. Pi session 2026-08-10T15-53-12-047Z_019fec60-c26f-7155-bae3-168a5ac72977 recorded `Fort active`; transcript audit found no direct tool paths or commands referencing `/net` or `/data`.
- Retry produced and ingested exactly one primary handoff: Capability Request `capreq_agent_boundary_typed_data_config_v1`; no Candidate Submission, execution, or training occurred. The request is valid and asks the Harness to preserve typed `research_problem.data_config` values in generated Agent Workspace TOML. Current generation stringifies boolean `true`, integer `8`, and the `sources` array, causing static Candidate validation to fail with `data_config.geographic_filter_required must be a boolean`.
- Candidate draft `agent-work/drafts/candidates/abi_spectral_resunet_scout_v1` remains unsubmitted. Gate 5 now requires human approval/rejection/revision of the Capability Request; implementation is not authorized by ingestion.
<!-- SECTION:NOTES:END -->
