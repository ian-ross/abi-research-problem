---
id: ABI-006
title: Provide reusable Learned Channel Mixer front ends
status: To Do
assignee: []
created_date: '2026-07-12 12:04'
updated_date: '2026-07-12 12:07'
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
- [ ] #1 Conv1x1ChannelMixer utility is available to candidate models
- [ ] #2 RawPlusLearnedChannelMixer utility is available to candidate models
- [ ] #3 Documentation briefly explains physically relevant brightness-temperature differences without hard-coding the search space
- [ ] #4 Example candidate or tests demonstrate importing and using the mixer utilities
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
