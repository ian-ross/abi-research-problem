---
id: ABI-025
title: Run first end-to-end candidate canary and Agent Control Boundary handoff
status: In Progress
assignee:
  - '@agent'
created_date: '2026-08-09 21:13'
updated_date: '2026-08-10 11:00'
labels:
  - harness
  - candidates
  - agent-boundary
  - canary
dependencies: []
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
- [ ] #2 Static validation and a human-approved bounded Docker training/evaluation run succeed on the GPU/cluster environment
- [ ] #3 The canary Run produces expected Run artifacts, Research Ledger/index records, provider-owned metrics, and an acceptance report tied to the canonical MCAST registry
- [ ] #4 Validation confirms longitude and latitude are not Candidate Experiment inputs and trusted data/baseline/ancillary mounts remain read-only and boundary-owned
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
<!-- SECTION:NOTES:END -->
