# ABI-026 Agent Campaign Context validation

## Generated artifact

- schema: `abi_agent_campaign_context/v1`
- artifact: `abi_contrail/profile/agent-campaign-context.v1.json`
- canonical registry: `abi-mcast-working-validation-v1`
- ABI-025 Run: `run_20260810_110532_b465cf`
- ABI-025 Post-Run Evaluation: `eval_20260810_110644_c0d61d`

The JSON records its generation timestamp, generator version, Workspace Configuration checksum, canonical registry checksum, ABI-025 source-artifact checksums, dataset record/sample digests, and MCAST aggregate/threshold artifact checksums.

## Refresh command

```bash
RUN_ROOT=/data/iross/abi-ml-autoresearch/runs/run_20260810_110532_b465cf
uv run abi-campaign-context \
  --workspace-config ml-autoresearch.toml \
  --run "$RUN_ROOT" \
  --evaluation "$RUN_ROOT/outputs/evaluations/eval_20260810_110644_c0d61d" \
  --output abi_contrail/profile/agent-campaign-context.v1.json
```

Generation validates the canonical registry and referenced checksums, checks completed Run/Evaluation status and cross-artifact identities, emits only whitelisted summaries, rejects sensitive keys and host/model-artifact paths, writes atomically, and reloads the result.

## Agent Control Boundary validation

Validated with:

```bash
uv run ml-autoresearch prepare-agent-boundary \
  --workspace-root . \
  --skip-runtime-image-validation
```

The bounded preparation check confirmed:

- the generated JSON is copied to `agent-research-problem/abi_contrail/profile/agent-campaign-context.v1.json`;
- both generated indexes name it as a required Dataset Profile Artifact at `/research-problem/abi_contrail/profile/agent-campaign-context.v1.json`;
- `/research-problem` is a read-only pi-fort mount;
- full training, ancillary, and baselines roots are absent from pi-fort mounts;
- the generated Agent Workspace configuration contains no data-root mounts.

`--skip-runtime-image-validation` was used because this was a boundary-snapshot validation, not an autonomy or Candidate Execution run. No training or autonomy step was invoked.

## Residual limitations

- ABI channel ranges are bounded deterministic snapshot summaries, not physical validity bounds.
- The artifact contains no qualitative samples; future qualitative examples require separate bounded approval.
- The ABI-025 canary intentionally failed scientific quality gates; its value here is lifecycle and acceptance-report context. Promotion remains human-reviewed.
