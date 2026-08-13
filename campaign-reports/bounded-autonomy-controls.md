# Bounded autonomy control evidence

## Scope

This report records the control state established after the bounded autonomous Candidate trial. Routine Autonomy Steps operated under the trusted Workspace Configuration, with at most one allowlisted Harness-owned next action from each successful step.

The control path demonstrated that the Agent and Harness:

- stop conservatively when required state is absent or ambiguous;
- preserve stable Run and Evaluation identities;
- avoid duplicate submission and replacement execution;
- enforce configured Candidate resource ceilings and provider-owned boundaries;
- return control through `no_handoff`, non-executable handoffs, Capability Requests, Campaign Reports, or `stop_for_human`.

## Trusted bounded policy recorded at the time

The measured policy was:

- at most 128 training samples per Dataset Source per epoch;
- at most 128 validation samples per Dataset Source per epoch;
- at most three training epochs;
- at most one concurrent Run;
- a trusted Docker Candidate wall-clock timeout of 1,800 seconds;
- at most two fixed `first_n` prediction samples;
- at most 25,000,000 Candidate parameters;
- managed Docker execution on pinned A100 GPU device 0 with rootless-container-root mode;
- provider-owned data loading, sampling, losses, metrics, Artifact Filters, Baseline Segmenter access, training policy, and evaluation semantics;
- Candidate inputs restricted to ABI channels 1-16, with longitude and latitude excluded.

These values describe the bounded reliability trial. The active Workspace Configuration remains authoritative for subsequent research.

## Exactly-once and stop behavior

Caller disconnect, command timeout, stale metadata, or incomplete host finalization did not create a second submission. Once a stable identifier existed, observation and reconciliation used that same artifact idempotently. Non-finite state, timeout, forced termination, duplicate or lifecycle inconsistency, contract violation, unexpected resource retry, missing required artifacts, coordinate exposure, and Harness failure retained fail-closed behavior.

Run `run_20260812_121722_8d6cd3` passed its preregistered finite, non-degenerate, resource, artifact, coordinate, mount, and exactly-once reliability checks. A subsequent Autonomy Step returned `no_handoff` because the interactive decision expected by that snapshot was not present in Agent-visible state. The absence of a handoff was a safe control outcome rather than a scientific failure.
