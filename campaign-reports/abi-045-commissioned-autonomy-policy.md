# ABI-045 commissioned autonomy policy

## Commissioning transition

The ABI Research Workspace is commissioned for routine autonomous research. Its active operator policy now matches the commissioned model in `../gvccs-research-problem`: the operator starts research by directly invoking `autonomy-step` or `run-autonomous-iteration`, and that invocation is sufficient authority for the bounded work performed by the command.

No Backlog task, implementation plan, campaign authorization report, `campaign_resumed` event, separate per-step approval, clean/pushed Git gate, manual Agent Control Boundary refresh, lifecycle-count baseline, or manual GPU-idle attestation is required for an ordinary research operation. The Harness prepares the boundary, checks its Runtime Image Validation Stamp, ingests at most one primary handoff per Autonomy Step, executes only Harness-owned next actions, and bounds autonomous iteration by the operator's step/duration arguments and stop conditions.

This report launches no Autonomy Step, Candidate Run, Post-Run Evaluation, Experiment Batch, or GPU operation. It is a prospective policy transition, not an execution authorization artifact.

## Active authority and bounds

The operator may run:

```bash
uv run ml-autoresearch autonomy-step --workspace-root . --execute-next-action
uv run ml-autoresearch run-autonomous-iteration \
  --workspace-root . \
  --max-steps <N> \
  --notify-email <address>
```

The command invocation authorizes all in-contract Agent choices and Harness-owned actions available under the active trusted Workspace Configuration. The current machine policy remains capped at 1,024 provider-selected records per Dataset Source and Leakage-Safe Split, 12 epochs, batch size 4, 25 million parameters, 3,600 seconds, four fixed `first_n` predictions, constant learning rate, disabled early stopping, concurrency one, and A100 device 0. These values are operating limits, not a separate authorization checklist.

If the operator later changes trusted Workspace limits or provider/Harness capabilities, invoking the command is sufficient authority to use the resulting active policy. Candidate source, manifests, and Agent handoffs cannot make those changes, exceed them, or substitute Candidate-owned resource placement, data loading, sampling, loss, metric, Artifact Filter, coordinate, retry, or lifecycle behavior.

## Retained commissioned safeguards

The transition removes ceremony, not trusted controls:

- longitude and latitude remain forbidden Candidate inputs;
- data loading, Leakage-Safe Split construction, Source-Balanced Sampling, capped-record selection, losses, metrics, targets, augmentations, Artifact Filters, and Baseline Segmenters remain provider/Harness-owned;
- Candidate fields remain allowlisted and resource/lifecycle limits remain Harness-enforced across direct, handoff, autonomy, reconciliation, and batch paths;
- one Autonomy Step still produces at most one primary handoff and at most one applicable Harness-owned next action;
- caller disconnection or stale state never creates a second Run; stable identities are observed and reconciled idempotently;
- non-finite state, contract violations, timeouts, lifecycle inconsistencies, missing artifacts, and Harness failures retain their fail-closed semantics;
- an explicit `campaign_paused` ledger state stops autonomous iteration until the operator records a resume;
- Capability Requests, Campaign Reports requesting review, and `stop_for_human` deliberately return control to the operator;
- promotion, deployment, baseline replacement, and production claims remain operator decisions rather than automatic consequences of a research Result.

Manual clean-Git, pushed-revision, boundary-snapshot, GPU-idle, and lifecycle-count checks may still be useful diagnostics. They are no longer prerequisites or authority gates beyond checks the Harness itself performs.

## Superseded commissioning conditions

ABI-034 through ABI-044 remain immutable historical evidence. Their per-task Human Gates, one-step execution approvals, hard stops, and requirements for a later separate Backlog task or authorization applied during commissioning and to those named operations. They do not constrain future operator-invoked bounded research.

In particular, this transition prospectively supersedes active use of:

- the task-specific gate in the former README reliability guidance;
- ABI-039's requirement for a separate task before the first promoted pilot;
- ABI-043's pilot-only stop before a representative scout;
- ABI-044's stop after exactly one representative scout and its requirement that every later Autonomy Step receive separate authorization.

The scientific interpretations remain: a one-epoch pilot is resource evidence, capped representative Runs are feasibility evidence rather than full-data evidence, low score alone is not enough to eliminate an improving or ambiguous family, and promotion claims need appropriately strong evidence. These are evidence-quality rules, not launch-authorization gates.

## GVCCS policy comparison

The commissioned GVCCS workspace has no Backlog directory or per-operation approval workflow. Its root `AGENTS.md` directly governs scientific branch selection and trusted Candidate boundaries, while operators invoke Harness commands against the workspace. Its autonomous loop stops on explicit campaign pause, Capability Request, Campaign Report/human-review handoff, no handoff, execution failure, or configured loop limits. ABI now follows that same control model while retaining ABI-specific data, coordinate, artifact-filter, source-balance, and resource policies.
