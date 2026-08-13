# Agent instructions for the ABI Research Problem Workspace

## Domain context

Read `CONTEXT.md` for the GOES ABI Contrail Segmentation ubiquitous language. Read `abi_contrail/brief/` and `abi_contrail/profile/` for Research Problem background, Dataset Profile context, and current research guidance.

Use `../ml-autoresearch` as the Harness reference and integration target. Use `../gvccs-research-problem` as the commissioned operational pattern, not as domain truth to copy blindly.

## Operator-invoked autonomous research

This repository is commissioned for autonomous research. Direct operator invocation of either of these commands is sufficient authority for the work that command performs:

```bash
uv run ml-autoresearch autonomy-step --workspace-root . --execute-next-action
uv run ml-autoresearch run-autonomous-iteration --workspace-root . --max-steps <N> --notify-email <address>
```

Ordinary bounded research operations do not require a Backlog task, implementation plan, campaign authorization report, `campaign_resumed` event, separate per-step approval, clean/pushed Git preflight, manual boundary refresh, lifecycle-count baseline, or manual GPU-idle attestation. The commands prepare the Agent Control Boundary and apply their own Harness checks. An operator may choose to perform additional diagnostics, but they are not authorization gates.

The active Workspace Configuration and Research Problem Spec are authoritative. Operator invocation authorizes the Harness-owned actions available within those limits, including successive Autonomy Steps in a bounded autonomous iteration. Candidate source, Candidate manifests, and the Agent cannot raise or bypass trusted resource, data, sampling, coordinate, loss, metric, Artifact Filter, execution, or lifecycle bounds.

Retain the commissioned GVCCS control model:

- an explicit `campaign_paused` ledger state stops autonomous iteration until the operator records a resume;
- `stop_for_human`, Capability Requests, Campaign Reports requesting review, non-finite state, contract violations, timeouts, lifecycle inconsistencies, missing artifacts, and Harness failures stop or bound the current command according to Harness semantics;
- caller disconnection never authorizes a duplicate or replacement Run; observe and reconcile the stable Run identity;
- promotion, deployment, and production claims remain operator decisions, but they are not prerequisites for ordinary research-loop execution;
- historical commissioning reports and tasks describe the controls used at the time and are not active per-operation gates.

## Experiment index maintenance

Update `EXPERIMENT_INDEX.md` whenever a new Candidate Experiment is introduced or a new Research Note is written. Keep current policy at the top of the index and preserve historical commissioning records as history.

## ABI architecture research policy

The generated Workspace Configuration defines the current sample, epoch, batch, parameter, timeout, prediction, scheduler, early-stopping, GPU, and concurrency limits. A research command may use any in-contract values at or below those limits without a separate authorization step.

Treat first attempts at materially different architecture families as scouts rather than final verdicts. Do not abandon a substantially new family after one untuned or lightly tuned regression against a mature incumbent. Low score alone is not elimination evidence when a finite trajectory is improving, source-balanced, novel, noisy, or ambiguous. Prefer bounded family development and source-stratified, non-degeneracy, trajectory, and failure-mode evidence before making comparative claims.

Representative capped Runs remain feasibility evidence rather than full-data promotion evidence. If the operator activates larger trusted limits, the resulting command invocation is sufficient authority to use them; Candidate code still cannot alter those limits or reinterpret capped evidence as full-data evidence.

## Trusted provider and Candidate boundary

- Candidate models must never receive longitude or latitude inputs. These encourage route-location priors and reduce transferability.
- Candidate code must not own data loading, loss definitions, metric definitions, Artifact Filters, Baseline Segmenter loading, target derivation, augmentation implementation, or sampling policies. These belong in trusted provider or Harness code.
- Candidate manifests may select only provider-advertised input modes, losses, augmentations, schedulers, auxiliary targets, and other allowlisted fields.
- New trusted capabilities require a Capability Request or operator-directed provider/Harness implementation and an allowlist update before Candidate use. They do not require a per-operation research authorization ceremony after activation.
- The `data` symlink points to external training data and may not exist in every environment. Unit tests should use tiny fixtures unless explicitly marked as data-dependent integration tests.

## Python and uv

This repository is uv-managed.

- Use `uv` for dependency management.
- Run Python through uv, for example `uv run python ...`.
- Do not run bare `python ...` commands.
- Prefer `uv run pytest ...` or other `uv run ...` forms for project tools.
