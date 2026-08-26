# Operator-invoked autonomous research policy

## Active authority

Direct operator invocation of either command is sufficient authority for the bounded work performed by that command:

```bash
uv run ml-autoresearch autonomy-step --workspace-root . --execute-next-action
uv run ml-autoresearch run-autonomous-iteration \
  --workspace-root . \
  --max-steps <N> \
  --notify-email <address>
```

The active Workspace Configuration and Research Problem Spec define the available Harness-owned actions and trusted bounds. The current machine policy permits at most 1,024 provider-selected records per Dataset Source and Leakage-Safe Split, 12 epochs, batch size 4, 25 million parameters, 3,600 seconds, four fixed `first_n` predictions, constant learning rate, disabled early stopping, concurrency one, and A100 device 0.

Candidate source, Candidate manifests, and Agent handoffs remain within those limits. Trusted provider and Harness code retain ownership of resource placement, data loading, Leakage-Safe Split construction, Source-Balanced Sampling, capped-record selection, losses, metrics, targets, augmentations, Artifact Filters, Baseline Segmenters, coordinate exclusion, retries, and lifecycle behavior.

## Operational safeguards

Each operator-invoked command retains the trusted controls appropriate to its bounded operation:

- longitude and latitude remain forbidden Candidate inputs;
- Candidate fields remain allowlisted;
- one Autonomy Step produces at most one primary handoff and at most one applicable Harness-owned next action;
- caller disconnection and stale state preserve the stable Run identity for idempotent observation and reconciliation;
- non-finite state, contract violations, timeouts, lifecycle inconsistencies, missing artifacts, and Harness failures retain fail-closed behavior;
- an explicit `campaign_paused` ledger state stops autonomous iteration until the operator records a resume;
- Capability Requests, Campaign Reports requesting review, and `stop_for_human` return control to the operator; and
- promotion, deployment, baseline replacement, and production claims remain operator decisions.

## Scientific interpretation

Materially different architecture families begin with bounded sequential evidence when their resource behavior is unknown. A short resource pilot can establish compatibility, while capped representative Runs establish feasibility. Aggregate and source-stratified trajectories, prediction non-degeneracy, finite/resource behavior, and failure modes support family decisions. Low score alone does not eliminate a finite, improving, source-balanced, novel, noisy, or ambiguous family, and capped evidence does not establish full-data performance.
