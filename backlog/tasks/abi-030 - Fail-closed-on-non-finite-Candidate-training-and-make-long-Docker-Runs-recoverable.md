---
id: ABI-030
title: >-
  Fail closed on non-finite Candidate training and make long Docker Runs
  recoverable
status: To Do
assignee: []
created_date: '2026-08-11 10:29'
labels:
  - harness
  - candidates
  - reliability
  - docker
dependencies: []
priority: high
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
ABI-025 exposed two trusted Harness reliability gaps. Candidate training continued for nearly nine hours after loss and model parameters became non-finite, then produced an artifact-complete Run marked completed. Separately, a synchronous caller timeout disconnected from a still-running Docker operation and left host-side Run metadata and the Research Ledger without terminal finalization. Harden trusted Candidate Execution so bad numerical state fails quickly and long-running Docker Runs can be detached, observed, and finalized exactly once without duplicate training.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Trusted training detects non-finite batch loss, aggregate loss/metrics, gradients, or model parameters at a defined bounded checkpoint and terminates promptly with an explicit failure reason and appropriate Harness-owned classification
- [ ] #2 A non-finite failure writes a bounded diagnostic artifact identifying epoch, batch, failing quantity, and finite/non-finite counts without exposing raw samples or moving loss/metric ownership into Candidate code
- [ ] #3 Long Docker Candidate Runs survive caller disconnection through a supported detached or reattachable execution path, and their status can be observed without launching a duplicate Run
- [ ] #4 A supported idempotent reconciliation/finalization path validates completed artifacts and records exactly one terminal Run metadata state and exactly one terminal Research Ledger event
- [ ] #5 Tests cover non-finite training, caller interruption, successful reattachment/reconciliation, duplicate-finalization prevention, and distinction from Resource Failure retry behavior
- [ ] #6 Operator and Agent-visible guidance documents the fail-fast and long-Run lifecycle semantics before another fully automatic autonomy iteration is approved
<!-- AC:END -->
