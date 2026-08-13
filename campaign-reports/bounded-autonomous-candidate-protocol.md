# Bounded autonomous Candidate execution protocol

## Execution contract

This protocol preregistered one bounded execution of the existing open `run_candidate` action for Candidate `abi032_mcast11_focal_tversky_v1`:

```bash
uv run ml-autoresearch execute-next-action --workspace-root .
```

The command was expected to create one stable Run and start trusted detached managed execution. Caller disconnect, nonzero return, timeout, stale result state, or incomplete host finalization did not create a second invocation or replacement Run. Once a Run ID existed, observation and recovery were restricted to `run-status` and idempotent `reconcile-run` for that identity.

## Preserved execution identity

The trusted Harness was clean commit `a38ad742e187e23b1fa13f7b0ec8bd21da7ad637`. Runtime validation completed at `2026-08-12T11:58:40Z` with:

- Harness fingerprint `4ee2c56b94e3a8e8`;
- runner `ml-autoresearch-runner:abi-research-problem-4ee2c56b94e3a8e8-13b99524f1`;
- Workspace Configuration SHA-256 `28586fdcc017ae955829f8658f6baa407910434645417e92f4e4d2bf0a23a430`;
- Docker GPU execution pinned to device `0` with rootless-container-root mode.

The dry-run action check reported exactly one action at ledger index 73 for Candidate `abi032_mcast11_focal_tversky_v1`. `agent-work/autonomy-step-result.json` independently recorded `status: ingested`, `executed_next_action: false`, and `execution: null` for the same action.

The canonical Candidate tree SHA-256 was `fbcf6294e7350286bfa734382d63b45ad0ed466f86d6e359b07253fdf6adf333`. Static validation passed. A normalized AST comparison against `abi031_mcast11_positive_control_v1/model.py` established executable architecture equivalence after Candidate/class-name and docstring normalization. The manifest changed trusted primary loss from `bce_dice` to `focal_tversky`.

The model receives only `abi_16ch`, uses source indices 10, 13, 12, and 14 to derive C11, C14, and C13-C15, and has no longitude/latitude path. Random initialization is fixed by `encoder_weights=None`.

## Fixed execution bounds

The Run was preregistered with:

- Docker managed lifecycle on A100 GPU device 0, sequential execution, concurrency one;
- provider-owned `combined_source_balanced` sampling;
- at most 128 training and 128 validation samples per Dataset Source per epoch;
- batch size 4 and at most three epochs;
- two fixed `first_n` prediction samples;
- trusted Docker wall-clock timeout of 1,800 seconds;
- at most 25,000,000 parameters, with 14,328,209 expected;
- no Experiment Batch or resource-failure retry for this reliability trial.

At preregistration there were 12 Run directories, three Evaluations, 74 Research Ledger lines, no active GPU process, and no managed Candidate container.

## Stable-Run procedure

After one `execute-next-action` invocation, the stable identity was observed with:

```bash
uv run ml-autoresearch run-status --workspace-root . --run-id <RUN_ID>
uv run ml-autoresearch reconcile-run --workspace-root . --run-id <RUN_ID>
```

A passing terminal Run required linked metadata, immutable Candidate snapshot, smoke/supervisor/training/validation logs, model summary, metrics, finite checkpoint, resource profile, one atomic validation-postprocessing report per epoch, two bounded prediction sets, no non-finite diagnostic, and exactly one terminal Research Ledger event.

## Preregistered evidence criteria

The reliability criteria required:

1. one stable completed Run and exactly one terminal lifecycle event;
2. one successful removed container with no timeout, forced termination, retry, replacement, or unexpected concurrent workload;
3. finite smoke, training, validation, postprocessing, resource, gradient, parameter, and checkpoint evidence;
4. exactly three epochs at batch 4 with no more than 128 train and validation samples from each Dataset Source per epoch;
5. aggregate, MIT, and Google raw/filtered Dice above `0.0001`, with finite non-degenerate precision and recall;
6. both bounded prediction masks containing positive and negative pixels;
7. complete and mutually consistent artifact, provenance, mount, coordinate, resource, timeout, postprocessing, and lifecycle evidence.

The 128-per-source budget made the result directional reliability evidence rather than promotion-grade or directly comparable scientific evidence.

## Pre-execution validation

- ABI focused provider/training/Candidate-boundary suite: 33 passed.
- Harness autonomy/config/reconciliation suite: 56 passed.
- Static Candidate validation: passed.
- Runtime-image identity validation: passed.
- Normalized architecture AST comparison: equal.
- Open-action dry run: exactly one matching action and zero executions.
