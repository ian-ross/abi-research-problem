---
id: ABI-031
title: Run an MCAST-lineage positive-control Candidate canary
status: To Do
assignee: []
created_date: '2026-08-11 10:31'
updated_date: '2026-08-11 10:32'
labels:
  - harness
  - candidates
  - canary
  - positive-control
  - mcast
dependencies:
  - ABI-030
priority: high
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
After ABI-030 hardens trusted numerical fail-fast and long-Run lifecycle handling, run a separately reviewed positive-control Candidate Experiment through the complete Candidate Execution path. Use a manually authored MCAST 1.1-lineage SMP U-Net/ResNet-18 architecture with random initialization and only provider-approved ABI inputs. The Candidate must not load MCAST weights, access the baselines root, or own data loading, loss, metrics, Artifact Filters, sampling, augmentation, or execution policy. This experiment distinguishes Candidate Execution reliability from the failed Agent-generated architecture while preserving the Candidate/Provider boundary. Scientific success means finite, non-degenerate behavior under preregistered criteria; beating canonical MCAST is not required.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 A reviewed positive-control protocol defines the MCAST-lineage architecture, approved-channel transforms, random initialization, sequential GPU policy, sample/epoch bounds, finite-state checks, non-degeneracy thresholds, expected artifacts, and explicit human review/execution gates
- [ ] #2 The manually authored Candidate contains architecture-only code, uses no baseline weights or baseline-root access, receives no longitude/latitude, and leaves data loading, losses, metrics, filters, sampling, augmentation, and execution policy to trusted provider/Harness code
- [ ] #3 Static validation, controlled model smoke tests, and bounded fixture checks pass before any real-data training is authorized
- [ ] #4 A human-approved sequential Docker/GPU Run executes only after ABI-030 is complete and demonstrates the new non-finite fail-fast and recoverable long-Run lifecycle behavior
- [ ] #5 A full canonical Working Validation evaluation and provider-owned acceptance report evaluate preregistered finite/non-degenerate criteria, including finite checkpoint parameters, finite losses, predicted-positive pixels, aggregate raw/filtered metrics, and MIT/Google source-stratified metrics
- [ ] #6 Run, evaluation, resource profile, bounded qualitative artifacts, Research Ledger/index records, canonical MCAST provenance, and all pass/fail evidence are validated and recorded durably whether the positive-control hypothesis passes or fails
- [ ] #7 A final human decision records whether Candidate Execution is trustworthy enough to resume planning for fully automatic autonomy; the decision does not itself launch an automatic iteration
<!-- AC:END -->
