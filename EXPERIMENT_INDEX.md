# Experiment Index

## Candidate Experiments and notes

| Candidate Experiment | Description | Related Research Notes | Key Runs / Evaluations | Status |
| --- | --- | --- | --- | --- |
| [`candidates/abi025_manual_canary_v1`](candidates/abi025_manual_canary_v1/README.md) | Minimal manually authored ABI Candidate Execution lifecycle canary. | Pending full Research Note. | `run_20260810_110532_b465cf`; `eval_20260810_110644_c0d61d` | Manual canary approved at Gate 3; clean Agent Control Boundary handoff retry in progress. |

| `candidates/abi_spectral_resunet_scout_v1` | [`README.md`](candidates/abi_spectral_resunet_scout_v1/README.md) — Source-balanced spectral residual U-Net family scout for thin-contrail segmentation. | Pending full Research Note. | Pending Research Problem Run. | Pending Harness Run; ingested from Agent Workspace. |
| ABI-029 operator GPU profiles ([protocol](docs/abi-gpu-resource-profiling.md)) | One-epoch, source-identical spectral ResUNet derivatives at batch sizes 1/2/4/8/16; reproducible with `scripts/prepare_abi029_gpu_profiles.py`. | Profiling protocol and results table. | `run_20260810_195338_853320`; `run_20260810_195523_8326f6`; `run_20260810_195710_c261ae`; `run_20260810_195845_df2123`; `run_20260810_200027_cf7110` | Complete without OOM/retry; batch size 8 selected; concurrency canary awaiting human gate. |

## Chronological Research Notes

No Research Notes have been recorded yet.
