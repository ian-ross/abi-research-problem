---
id: ABI-032
title: Harden configured Docker defaults and pre-training Run recovery
status: To Do
assignee: []
created_date: '2026-08-11 13:05'
updated_date: '2026-08-11 13:05'
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
