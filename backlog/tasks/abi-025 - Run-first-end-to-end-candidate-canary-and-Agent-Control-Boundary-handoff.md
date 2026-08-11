---
id: ABI-025
title: Run first end-to-end candidate canary and Agent Control Boundary handoff
status: Done
assignee:
  - '@agent'
created_date: '2026-08-09 21:13'
updated_date: '2026-08-11 10:30'
labels:
  - harness
  - candidates
  - agent-boundary
  - canary
dependencies:
  - ABI-028
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
- [x] #5 One Agent Control Boundary autonomy step is run without automatic next-action execution, and its single handoff is inspected and approved before any candidate execution
- [x] #6 The approved Agent-generated handoff is executed separately and its Run artifacts and acceptance report are validated
- [x] #7 A final human go/no-go decision is recorded before enabling or attempting a fully automatic autonomy iteration
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

- ABI-028 completed and GitHub Harness issue #123 closed. Agent Boundary TOML now preserves typed provider data config. ABI provider static contract loading works without operational data-root mounts, while execution remains fail-closed through `validate_data_root`. Fort candidate validation of the retained `abi_spectral_resunet_scout_v1` draft now passes. No Candidate Submission, Run, or training was performed; a fresh autonomy-step still requires the next explicit human gate.

- Fresh Human Execution Gate 4 autonomy step invoked once with `uv run ml-autoresearch autonomy-step --workspace-root .`, without `--execute-next-action`. Fort session `2026-08-10T18-50-24-737Z_019fed03-0061-71af-84d9-ee6f24c2ca5a` was active and used intended `/reference`, `/history`, `/docs`, and `/research-problem` inputs; tool-call audit found no direct `/data` or `/net` access.
- Exactly one Candidate Submission, `abi_spectral_resunet_scout_v1`, was ingested. Canonical and submitted candidate files match byte-for-byte; Harness static validation passes; source inspection finds architecture-only Torch/provider support imports with no longitude/latitude or candidate-owned data, loss, metric, filter, sampling, augmentation, network, or persistence behavior. One `agent_handoff_ingested` ledger event and one pending `run_candidate` action exist; no Run or training was started.
- Gate 5 review concern: the proposal requests at most 1,024 training samples per Dataset Source, but `execute-next-action` has no bound option and current `[candidate_execution]` has no `max_samples`, so execution would not enforce the reviewed sample cap. Human approval is pending a decision on enforcing the bound before Gate 6.

- Human approved the `abi_spectral_resunet_scout_v1` handoff conditionally on enforcing its requested sample cap. Added trusted `[candidate_execution] max_samples = 1024`; config loading confirms the cap, Candidate static validation remains valid, and `execute-open-actions --dry-run` shows exactly one pending `run_candidate` action. No execution or training occurred; Gate 6 remains a separate human execution decision.

- Human Execution Gate 6 authorized execution of the single approved `abi_spectral_resunet_scout_v1` handoff. Proceeding with `execute-open-actions --max-actions 1` under the enforced 1,024-samples-per-source bound.

- Gate 6 execution created Run `run_20260810_204928_ab0218` with the approved 1,024-samples-per-source bound and read-only trusted mounts. The foreground client timed out after two hours while Docker remained active in epoch 3/12; no duplicate Run was launched. Interim inspection found training loss had become NaN in epoch 3. Final outcome and Harness reconciliation remain pending container completion.

- Human Execution Gate 6 completed for Agent-generated Candidate `abi_spectral_resunet_scout_v1`: Run `run_20260810_204928_ab0218` executed 12 epochs on pinned A100 with the enforced 1,024 samples per Dataset Source (2,048 combined train and validation), batch size 4, and no resource retry.
- The synchronous CLI caller timed out after two hours while Docker continued. No duplicate Run was launched. Docker exited 0 after writing required artifacts; stale host metadata and the missing terminal ledger event were reconciled once with Harness validation/finalization helpers and duplicate-event preconditions.
- Training became non-finite after two batches of epoch 1 and remained non-finite. The selected checkpoint has 2,539,889 non-finite parameter values out of 2,539,921 tensor values; the full Working Validation evaluation `eval_20260811_054134_51fc4c` predicted zero positive pixels across 3,088 samples.
- Provider-owned acceptance report is tied to verified registry `abi-mcast-working-validation-v1` and flags aggregate baseline failure, recall regression, and catastrophic MIT and Google source failures. Promotion remains human_review_required.
- Boundary/artifact validation passed: canonical and Run Candidate copies match byte-for-byte; static validation passes; model summary permits only ABI channels 1-16 and forbids longitude/latitude; trusted mounts are recorded read-only; expected Run/evaluation/ledger artifacts and four bounded diagnostic samples/eight GeoTIFFs exist.
- Wrote final Gate 6 report `campaign-reports/abi-025-agent-handoff-canary.md`. Recommendation for Human Final Gate 7 is no-go until trusted non-finite fail-fast checks and robust detached/synchronous Run finalization are addressed. Final human go/no-go decision is not yet recorded.

- Human Final Gate 7 recorded **NO-GO** on attempting a fully automatic autonomy iteration. Required Harness hardening is tracked in ABI-030: fail closed on non-finite Candidate training and provide supported observable/idempotent long-Docker-Run finalization.
- A future positive-control Candidate canary is recommended after ABI-030, using an MCAST-like architecture without Candidate access to baseline weights or the baselines root; scope remains a separate human-reviewed task.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Completed the staged ABI Candidate Experiment lifecycle through the manual canary, isolated Agent Control Boundary handoff, separately approved Agent-generated Candidate execution, full Working Validation evaluation, and final human decision.

Manual lifecycle canary:
- Run `run_20260810_110532_b465cf` and evaluation `eval_20260810_110644_c0d61d` validated trusted artifacts, ledger/index integration, read-only mounts, forbidden coordinate inputs, and canonical MCAST acceptance reporting.

Agent Control Boundary:
- Remediated boundary context, isolation, and typed-config blockers through ABI-026/027/028.
- Ingested and reviewed exactly one Candidate Submission, `abi_spectral_resunet_scout_v1`, without automatic execution.
- Enforced the approved 1,024-samples-per-source bound before separate Human Execution Gate 6.

Agent-generated Candidate result:
- Run `run_20260810_204928_ab0218` and evaluation `eval_20260811_054134_51fc4c` completed with expected artifacts and canonical acceptance report.
- Candidate source matched the reviewed handoff, used only ABI channels 1-16, and retained provider/Harness ownership of data, loss, metrics, filters, sampling, augmentation, and read-only mounts.
- Training became non-finite after two batches; the checkpoint was non-finite and full validation produced all-negative predictions. All scientific acceptance gates failed; promotion was rejected.

Final decision:
- Human Final Gate 7 recorded NO-GO on fully automatic autonomy. ABI-030 tracks required trusted non-finite fail-fast and long Docker Run recovery/finalization fixes.
- Final campaign evidence is recorded in `campaign-reports/abi-025-agent-handoff-canary.md`.

Validation:
- Candidate static validation passed.
- Canonical and Run Candidate copies matched byte-for-byte.
- Canonical registry `abi-mcast-working-validation-v1` and both baseline references verified.
- Run/evaluation status, expected artifacts, 3,088-sample metrics, four diagnostic samples/eight GeoTIFFs, acceptance report linkage, model input boundary, read-only mounts, and Research Ledger events were inspected.
- `execute-open-actions --dry-run` reported no remaining open actions.
<!-- SECTION:FINAL_SUMMARY:END -->
