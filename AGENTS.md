# Agent instructions for the ABI Research Problem Workspace

## Domain context

Read `CONTEXT.md` for the GOES ABI Contrail Segmentation ubiquitous language. Read `abi_contrail/brief/` and `abi_contrail/profile/` for Research Problem background, Dataset Profile context, and current research guidance.

Use `../ml-autoresearch` as the Harness reference and integration target.

## Operator-invoked autonomous research

This workspace is commissioned for autonomous research. Direct operator invocation of either command is sufficient authority for the bounded work performed by that command:

```bash
uv run ml-autoresearch autonomy-step --workspace-root . --execute-next-action
uv run ml-autoresearch run-autonomous-iteration --workspace-root . --max-steps <N> --notify-email <address>
```

The active Workspace Configuration and Research Problem Spec define the available actions and their trusted resource, data, sampling, coordinate, loss, metric, Artifact Filter, execution, and lifecycle bounds. Candidate source, Candidate manifests, and Agent handoffs cannot raise or bypass those bounds.

An explicit `campaign_paused` ledger state stops autonomous iteration until the operator records a resume. `stop_for_human`, Capability Requests, Campaign Reports requesting review, non-finite state, contract violations, timeouts, lifecycle inconsistencies, missing artifacts, and Harness failures stop or bound the current command according to Harness semantics. Caller disconnection does not create authority for a duplicate or replacement Run; observe and reconcile the stable Run identity. Promotion, deployment, and production claims remain operator decisions.

## Experiment index maintenance

Update `EXPERIMENT_INDEX.md` whenever a new Candidate Experiment is introduced or a new Research Note is written. Keep current policy at the top of the index.

## ABI architecture research policy

The generated Workspace Configuration defines the current sample, epoch, batch, parameter, timeout, prediction, scheduler, early-stopping, GPU, and concurrency limits. A research command may use any in-contract values at or below those limits.

Treat first attempts at materially different architecture families as scouts rather than final verdicts. Do not abandon a substantially new family after one untuned or lightly tuned regression against a mature incumbent. Low score alone is not elimination evidence when a finite trajectory is improving, source-balanced, novel, noisy, or ambiguous. Prefer bounded family development and source-stratified, non-degeneracy, trajectory, and failure-mode evidence before making comparative claims.

Representative capped Runs are feasibility evidence rather than full-data promotion evidence. Candidate code cannot alter trusted limits or reinterpret capped evidence as full-data evidence.

## Trusted provider and Candidate boundary

- Candidate models must never receive longitude or latitude inputs. These encourage route-location priors and reduce transferability.
- Candidate code must not own data loading, loss definitions, metric definitions, Artifact Filters, Baseline Segmenter loading, target derivation, augmentation implementation, or sampling policies. These belong in trusted provider or Harness code.
- Candidate manifests may select only provider-advertised input modes, losses, augmentations, schedulers, auxiliary targets, and other allowlisted fields.
- New trusted capabilities require a Capability Request or operator-directed provider/Harness implementation and an allowlist update before Candidate use.
- The `data` symlink points to external training data and may not exist in every environment. Unit tests should use tiny fixtures unless explicitly marked as data-dependent integration tests.

## Python and uv execution safety

This repository is uv-managed.

- Use `uv` for dependency management.
- Run Python through uv, for example `uv run python ...`.
- Do not run bare `python ...` commands.
- Prefer `uv run pytest ...` or other `uv run ...` forms for project tools.

Do not run `uv run`, `uv sync`, or other virtual-environment-mutating commands from this repository when it is mounted inside a Fort/Gondolin VM. The host `.venv/` is not portable into the VM and may be damaged if uv attempts to repair it.

If an operator explicitly asks you to run `uv` against this workspace from inside a VM, force uv to use a VM-local environment outside the mounted repository, for example:

```bash
UV_PROJECT_ENVIRONMENT=/tmp/abi-research-problem-venv uv run ...
```

Inside the Agent Control Boundary, prefer `ml-autoresearch-agent` commands from the Agent Workspace rather than host-style `uv run` commands.
