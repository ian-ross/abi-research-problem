---
id: ABI-006
title: Provide reusable Learned Channel Mixer front ends
status: In Progress
assignee:
  - '@agent'
created_date: '2026-07-12 12:04'
updated_date: '2026-07-12 16:05'
labels:
  - model-support
  - docs
dependencies:
  - ABI-005
priority: medium
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Add reusable model-support utilities and brief guidance for Learned Channel Mixer front ends so candidates can reuse channel-mixing patterns across architectures without constraining exploration.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 Conv1x1ChannelMixer utility is available to candidate models
- [x] #2 RawPlusLearnedChannelMixer utility is available to candidate models
- [x] #3 Documentation briefly explains physically relevant brightness-temperature differences without hard-coding the search space
- [x] #4 Example candidate or tests demonstrate importing and using the mixer utilities
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Add a small model-support module in the ABI provider package for reusable channel-mixer front ends.
2. Implement Conv1x1ChannelMixer with clear input/output shape behavior.
3. Implement RawPlusLearnedChannelMixer that concatenates selected raw channels with learned 1x1 projections.
4. Add tests or an example candidate showing these utilities can be imported from candidate model.py.
5. Add brief documentation explaining BTD motivation lightly, including that useful channel combinations should remain open to exploration.
6. Avoid hard-coding MCAST three-channel features as the candidate search space.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
- Added abi_contrail.model_support with Conv1x1ChannelMixer and RawPlusLearnedChannelMixer.
- Added tests for shape behavior, validation, and candidate model.py import/use.
- Updated README and provider brief with channel-mixer import guidance and BTD motivation without fixing the search space.
- Validation: uv run pytest -q (23 passed).

- Reopened to refine RawPlusLearnedChannelMixer so the preserved raw side can include brightness-temperature difference features, not only individual channels.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Implemented reusable ABI learned channel mixer front ends for candidate models. Added Conv1x1ChannelMixer and RawPlusLearnedChannelMixer in abi_contrail.model_support, with clear shape validation for [C,H,W] and [N,C,H,W] tensors. Added tests that cover mixer behavior and demonstrate importing the utilities from a candidate model.py. Updated README and provider brief with light BTD/channel-combination motivation while keeping candidate exploration open and preserving provider-owned input selection.

Tests:
- uv run pytest -q (23 passed)
<!-- SECTION:FINAL_SUMMARY:END -->
