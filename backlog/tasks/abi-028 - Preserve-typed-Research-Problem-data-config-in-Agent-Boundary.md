---
id: ABI-028
title: Preserve typed Research Problem data config in Agent Boundary
status: In Progress
assignee:
  - '@agent'
created_date: '2026-08-10 16:17'
updated_date: '2026-08-10 16:27'
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
- [x] #1 Generated Agent Workspace TOML preserves supported scalar, array, and nested mapping data_config value types
- [x] #2 A regression test reproduces the ABI boolean/integer/list failure and passes after the fix
- [x] #3 ABI boundary preparation and agent-side static Candidate validation succeed without changing isolation or mount policy
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Add a focused failing Harness regression test for typed Agent Workspace data_config TOML generation
2. Implement minimal type-preserving TOML serialization without changing mounts or isolation policy
3. Run focused Harness tests and the ABI prepare/agent validation repro
4. Record validation and unblock ABI-025
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
- Reproduced the bug with a failing Harness test: generated booleans, integers, floats, arrays, and nested mappings all parsed back as strings.
- Fixed `../ml-autoresearch/src/ml_autoresearch/agent_boundary.py` with recursive type-preserving TOML rendering; no Fort, mount, egress, or isolation policy changed.
- Real Fort smoke passed after an adjacent ABI provider fix allowed rootless static contract loading while keeping `validate_data_root` fail-closed before execution.
- GitHub issue: ian-ross/ml-autoresearch#123 (closed).
- Validation: Harness focused 47 passed; ABI focused 32 passed; ABI full 101 passed; Fort candidate validation valid. Harness full suite reached 517 passed/2 skipped with 4 unrelated external-fixture/environment failures.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Fixed Agent Boundary data_config type preservation and rootless ABI static contract loading. Generated TOML now round-trips strings, booleans, integers, floats, arrays, and nested mappings. Operational data validation remains fail-closed and isolation policy is unchanged.

Tests:
- cd ../ml-autoresearch && uv run pytest tests/test_agent_boundary.py tests/test_autonomy_step.py -q (47 passed)
- uv run pytest tests/test_provider_spec.py tests/test_abi_training_adapter.py tests/test_ancillary_data.py -q (32 passed)
- uv run pytest -q (101 passed)
- Fort agent-side validate-candidate smoke (valid)

Residual validation:
- Harness full suite: 517 passed, 2 skipped, 4 unrelated external-fixture/environment failures.
<!-- SECTION:FINAL_SUMMARY:END -->
