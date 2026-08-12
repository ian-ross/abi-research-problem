# ABI-034 bounded autonomy boundary trial

## Decision and scope

Human approval authorized one handoff-only Agent Control Boundary trial and conservative test-run limits. The trial deliberately invoked `autonomy-step` **without** `--execute-next-action`. It did not authorize Candidate training, Post-Run Evaluation, promotion, or an automatic iteration loop.

Approved local test limits:

- at most 128 samples per Dataset Source;
- at most 3 training epochs;
- at most one parallel Run;
- 1,800-second trusted Docker training wall-clock budget;
- notification recipient `iross@mit.edu`;
- existing Agent egress and full read-only Runs-history policy retained.

These are first-autonomy test ceilings, not proposed production exploration budgets.

## Trusted Harness changes

Harness commit `a38ad74` adds Workspace-owned `max_epochs` and `training_wall_clock_timeout_seconds` policy. Config-driven Candidate, managed continuation, Agent handoff, and Experiment Batch paths reject manifests above the epoch ceiling. Command-line sample requests are clamped to the configured sample ceiling, and config-driven Experiment Batch concurrency is clamped to the configured parallel cap. The existing Docker backend enforces the training timeout with graceful timeout signaling followed by its fixed grace period and forced termination if necessary.

Generated Agent Workspace configuration and instructions expose the sample, epoch, concurrency, parameter, and wall-clock policies. Agent-side static Candidate and submission preparation enforce the epoch ceiling; canonical handoff ingestion enforces it again. Mailjet credentials are not copied into the Agent Workspace.

The ABI local Workspace Configuration was set to the approved limits and rebuilt against clean Harness commit `a38ad742e187e23b1fa13f7b0ec8bd21da7ad637`. The validated runner is `ml-autoresearch-runner:abi-research-problem-4ee2c56b94e3a8e8-13b99524f1`.

## Campaign-state reconciliation and notification

`EXPERIMENT_INDEX.md` and the ABI-031 protocol now agree with the durable ABI-031 task decision: Human Gate 5 approved resuming autonomy planning only. The decision did not promote ABI-031, launch an automatic iteration, or waive ordinary acceptance gates.

All required local Mailjet fields loaded successfully. A single configuration-test message was sent to `iross@mit.edu`; no credentials were logged or copied into durable evidence.

## Boundary refresh

`prepare-agent-boundary` completed from clean ABI and Harness revisions. Inspection confirmed:

- `allow_egress = true` remains enabled;
- `/data/iross/abi-ml-autoresearch/runs` remains mounted at `/history/runs` read-only;
- Agent-visible config records `max_samples = 128`, `max_epochs = 3`, and `max_parallel_runs = 1`;
- Agent instructions record the 1,800-second trusted Docker training budget;
- the Agent-visible Experiment Index contains the completed Gate 5 planning-only decision;
- no `[mailjet]` table or credentials are present in `agent-work/ml-autoresearch.toml`.

## Handoff-only trial result

The exact command was:

```bash
uv run ml-autoresearch autonomy-step --workspace-root .
```

No `--execute-next-action` flag was supplied.

The Agent produced and the Harness ingested exactly one Candidate Submission, `abi032_mcast11_focal_tversky_v1`. It is a controlled MCAST 1.1-lineage continuation that changes the trusted primary loss to `focal_tversky`, requests three epochs, and explicitly excludes longitude/latitude and Candidate ownership of trusted training policy.

`agent-work/autonomy-step-result.json` records:

- `status: ingested`;
- `handoff_type: candidate_submission`;
- `next_action: run_candidate`;
- `executed_next_action: false`;
- `execution: null`;
- Agent return code 0.

Independent filesystem counts before and after the step were unchanged at 12 Run directories and 3 Evaluation directories. The Research Ledger increased from 73 to 74 lines solely for `agent_handoff_ingested`. No `candidate_submitted`, `run_started`, `run_completed`, `evaluation_requested`, or evaluation terminal event was added by the trial.

The ingested Candidate now appears as one open `run_candidate` action. `execute-open-actions --dry-run` reports it without executing it. It remains pending human review and is **not authorized for training by ABI-034**.

## Validation

- Focused Harness policy, Candidate, boundary, handoff, submission, batch, and CLI suites: 149 passed.
- Full ABI suite: 114 passed.
- Full Harness suite: 570 passed, 2 skipped, with one known unrelated GVCCS stale fake-Spec characterization failure (`focal_bce_dice` absent from that test fake allowlist).
- Runtime image build and identity validation passed.
- Mailjet configuration test delivered successfully.
- Candidate/evaluation counts prove no training or evaluation action executed during the trial.

## Residual risks and next decision

- The ingested Candidate has not received scientific/source review beyond static contract and boundary validation. Its open `run_candidate` action must remain unexecuted until separately approved.
- The 128-sample-per-source result, if later authorized, would be directional and not promotion-grade relative to ABI-031's 1,024-sample-per-source Run.
- The training timeout is a hard outer Docker budget with a graceful-stop phase, but no real training timeout canary was run under ABI-034 because this trial was explicitly non-training.
- Production-shape accelerated ABI validation throughput and peak CUDA allocation remain unmeasured.
- The retained egress and full read-only Runs mount are accepted for this trial based on prior GVCCS validation; this task did not narrow them.
