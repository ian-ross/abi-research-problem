---
id: ABI-021
title: Complete ml-autoresearch runtime setup for ABI workspace
status: To Do
assignee: []
created_date: '2026-08-07 10:23'
labels:
  - harness
  - containers
  - baselines
dependencies: []
priority: high
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Make the ABI research workspace runnable through the sibling ml-autoresearch harness. Complete and validate workspace configuration, build/reference the required runtime images, and document trusted data and baseline-weight provisioning so ABI-017 can run reproducibly.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 ml-autoresearch.toml contains valid, non-secret workspace, provider, candidate execution, and agent-boundary settings
- [ ] #2 The required runner and agent images can be built and their resulting identities are documented in the workspace configuration or setup documentation
- [ ] #3 Dataset and MCAST 1.1/2.1 weight paths are provisioned through explicit trusted host paths or links and are available at the paths expected by the provider and container runtime
- [ ] #4 Harness setup/config validation and a bounded provider or candidate smoke run succeed without real model training
- [ ] #5 A reproducible handoff documents commands and prerequisites for ABI-017 baseline evaluation on the GPU server
<!-- AC:END -->
