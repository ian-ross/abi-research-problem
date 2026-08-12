# ABI-036 durable bounded-autonomy authorization

## Decision

Human review is complete. The operator authorizes continuation of routine autonomous research under the current trusted ABI Workspace Configuration without requiring a separate chat approval before every Autonomy Step or every Harness-owned action that is already bounded by that configuration.

The explicit per-step Human Gates used through ABI-035 were onboarding and reliability gates. ABI-035 demonstrated that the Agent and Harness stop conservatively when authorization is absent or ambiguous, preserve a stable Run identity, avoid duplicate execution, and enforce the configured Candidate ceilings. Those onboarding gates are now satisfied.

This decision is intended to be copied into the Agent Control Boundary through the Experiment Index and Research Ledger. It supersedes the stale Agent-visible statement that ABI-035 Human Gate 1 is pending.

## Authorized routine operation

The operator authorizes the Harness to continue bounded Autonomy Steps and to execute at most the single allowlisted Harness-owned next action produced by each successful step, without another per-step chat approval, when all of the following remain true:

- the ABI and Harness revisions used by the boundary are clean and durably preserved;
- runtime-image identity validation passes;
- the Workspace Configuration is unchanged from the approved bounded policy;
- the action is validated and enforceable through trusted Harness/provider code;
- no campaign pause, unresolved failure, contract violation, or human-review request is active;
- the action has applicable trusted resource and lifecycle bounds;
- stable Run/Evaluation identities are observed and reconciled idempotently without duplicate submission.

A normal `no_handoff`, non-executable handoff, capability request, or `stop_for_human` outcome ends that step safely. It does not authorize fabricating a handoff or bypassing review.

## Approved bounded policy

The current Candidate policy remains:

- at most 128 training samples per Dataset Source per epoch;
- at most 128 validation samples per Dataset Source per epoch;
- at most three training epochs;
- at most one concurrent Run;
- trusted Docker Candidate wall-clock timeout of 1,800 seconds;
- at most two `first_n` bounded prediction samples;
- maximum 25,000,000 Candidate parameters;
- managed Docker execution on pinned A100 GPU device 0 with rootless-container-root mode;
- provider-owned data loading, sampling, losses, metrics, Artifact Filters, Baseline Segmenter access, training policy, and evaluation semantics;
- Candidate inputs restricted to ABI channels 1-16, with longitude and latitude excluded.

These are autonomy test ceilings, not promotion-grade scientific budgets. The Harness may clamp or reject requests to these limits; the Agent and Candidate may not raise them.

An allowlisted non-Candidate action may execute without another chat approval only when trusted Harness/provider policy supplies applicable bounds and lifecycle evidence. If an action lacks an applicable trusted ceiling, the campaign must stop for human review rather than infer authorization.

## Human review remains required

This authorization does **not** waive human review for:

- changing or raising sample, epoch, concurrency, timeout, parameter, prediction, GPU, egress, mount, or other trusted policy limits;
- changing the Research Problem contract, trusted provider/Harness ownership boundary, coordinate exclusion, Artifact Filters, metrics, loss definitions, or data/sampling policy;
- promotion, deployment, production claims, baseline replacement, or treating bounded results as promotion-grade evidence;
- recovery after non-finite state, timeout, forced termination, duplicate/lifecycle inconsistency, contract violation, unexpected resource retry, missing required artifact, coordinate exposure, or Harness failure;
- an action for which the Harness cannot prove applicable bounds;
- an explicit Agent/Harness `stop_for_human`, campaign pause condition, unresolved capability request, or other exceptional decision outside established policy.

Scientifically poor but finite and contract-compliant results may inform the next bounded hypothesis; they do not automatically require human approval unless a configured stop condition or one of the conditions above applies.

## Exactly-once and stop rules

Caller disconnect, command timeout, stale metadata, or incomplete host finalization never authorizes resubmission. Once a stable identifier exists, observe and reconcile that same artifact idempotently. Automatic replacement Runs and duplicate action execution remain forbidden.

If trusted execution requests timeout termination, observes non-finite state, violates a contract, loses required evidence, exceeds policy, or reaches an unbounded action, stop the autonomous campaign for human review. Do not hide the failure by retrying a new Candidate or starting another Autonomy Step.

## Basis and interpretation

ABI-035 Run `run_20260812_121722_8d6cd3` passed its preregistered finite, non-degenerate, resource, artifact, coordinate, mount, and exactly-once reliability gate. The subsequent approved Autonomy Step returned `no_handoff` because the interactive Gate 1 approval had not yet been written into Agent-visible durable state. That was a safe outcome, not a scientific failure.

This ABI-036 record closes that visibility gap. After this report, the Experiment Index, and the linked `campaign_resumed` event are committed and pushed, the boundary may be refreshed and routine bounded autonomy may continue without recreating the ABI-035 onboarding gate. Pushing and launching the next step remain separate operator actions; this commit itself executes no Candidate, evaluation, batch, or Autonomy Step.
