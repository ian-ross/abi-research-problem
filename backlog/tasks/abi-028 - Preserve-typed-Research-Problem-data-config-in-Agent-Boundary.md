---
id: ABI-028
title: Preserve typed Research Problem data config in Agent Boundary
status: To Do
assignee: []
created_date: '2026-08-10 16:17'
labels:
  - harness
  - agent-boundary
  - bug
dependencies: []
priority: high
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Fix the trusted Harness Agent Boundary TOML generation bug discovered by ABI-025: generated research_problem.data_config values are stringified, so provider construction and static Candidate validation fail for booleans, integers, arrays, and nested mappings. This blocks the approved Agent Control Boundary handoff canary.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Generated Agent Workspace TOML preserves supported scalar, array, and nested mapping data_config value types
- [ ] #2 A regression test reproduces the ABI boolean/integer/list failure and passes after the fix
- [ ] #3 ABI boundary preparation and agent-side static Candidate validation succeed without changing isolation or mount policy
<!-- AC:END -->
