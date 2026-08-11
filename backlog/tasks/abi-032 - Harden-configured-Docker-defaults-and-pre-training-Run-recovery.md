---
id: ABI-032
title: Harden configured Docker defaults and pre-training Run recovery
status: In Progress
assignee:
  - '@agent'
created_date: '2026-08-11 13:05'
updated_date: '2026-08-11 13:22'
labels:
  - harness
  - docker
  - reliability
dependencies:
  - ABI-030
priority: medium
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
ABI-030 Human Execution Gate 1 exposed residual submission-phase gaps. Host run-candidate uses fixed Docker option defaults instead of the workspace-configured image/GPU/rootless settings when flags are omitted, and managed execution begins only after synchronous smoke acceptance, so caller loss during smoke leaves a Run without execution.json. Align host CLI defaults with candidate_execution config and make smoke/submission interruption observable and recoverable without resubmission. Also ensure trusted provider/bootstrap failures are not mislabeled as Candidate bugs.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Omitted run-candidate Docker options resolve to the validated workspace candidate_execution image, GPU device, and ownership policy, while explicit CLI options still override configuration
- [ ] #2 Caller interruption during Docker smoke leaves a durable observable execution phase that can be reconciled by the same Run ID without resubmission
- [ ] #3 Trusted image/provider/data bootstrap failures receive a Harness-owned classification rather than candidate_bug
- [ ] #4 Tests cover configured defaults, smoke-phase caller interruption, reconciliation idempotence, and explicit override behavior
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Add public-CLI regression tests for omitted versus explicit run-candidate Docker image, GPU device/enablement, and ownership options; introduce one validated option-resolution path so Workspace Configuration supplies omitted values and explicit flags (including explicit disablement) win consistently across smoke and managed continuation.
2. Refactor the managed Run lifecycle in vertical TDD slices so a stable Run and execution.json phase exist before Docker smoke, the detached supervisor owns smoke and training for both foreground and --detach callers, and caller loss can be observed/reconciled by the same Run ID without relaunching the Candidate.
3. Add typed Harness-owned bootstrap failure handling for Docker image/runtime, trusted Research Problem provider, and data setup failures while preserving candidate_bug for Candidate validation/model smoke failures; make repeated reconciliation idempotent in pre-training, failed, and completed states.
4. Update ADR/run-lifecycle/operator guidance to match the pre-smoke managed lifecycle and explicit override semantics, then run focused lifecycle/backend/CLI suites and the full Harness suite without real training.
5. Integrate the validated Harness revision into the ABI workspace, update bounded reliability evidence/tests as required, run the ABI unit suite, and complete task acceptance metadata and final summary.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
- ABI-030 dependency confirmed Done; ABI-032 assigned to @agent and moved to In Progress.
- Read-only inspection traced the gap through run-candidate, prepare_candidate_run_from_workspace, submit_candidate, DockerBackend.smoke_test, managed execution, and reconcile_run.
- Focused pre-change Harness baseline: 51 passed (`uv run pytest -q tests/test_cli_submission.py tests/test_cli_default_backend.py tests/test_cli_backend_selection.py tests/test_run_reconciliation.py tests/test_execution_backends.py`). No real model training or external ABI data used.
<!-- SECTION:NOTES:END -->
