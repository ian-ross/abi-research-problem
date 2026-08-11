# Experiment Index

## Candidate Experiments and notes

| Candidate Experiment | Description | Related Research Notes | Key Runs / Evaluations | Status |
| --- | --- | --- | --- | --- |
| [`candidates/abi025_manual_canary_v1`](candidates/abi025_manual_canary_v1/README.md) | Minimal manually authored ABI Candidate Execution lifecycle canary. | Pending full Research Note. | `run_20260810_110532_b465cf`; `eval_20260810_110644_c0d61d` | Manual canary approved at Gate 3; clean Agent Control Boundary handoff retry in progress. |

| `candidates/abi_spectral_resunet_scout_v1` | [`README.md`](candidates/abi_spectral_resunet_scout_v1/README.md) — Source-balanced spectral residual U-Net family scout for thin-contrail segmentation. | [`campaign-reports/abi-025-agent-handoff-canary.md`](campaign-reports/abi-025-agent-handoff-canary.md) | `run_20260810_204928_ab0218`; `eval_20260811_054134_51fc4c` | Executed from the approved Agent handoff; non-finite training and all-negative full-validation predictions failed acceptance gates. Do not promote. |
| [`candidates/abi031_mcast11_positive_control_v1`](candidates/abi031_mcast11_positive_control_v1/README.md) | Manually authored, randomly initialized MCAST 1.1-lineage SMP U-Net/ResNet-18 positive control for Candidate Execution reliability. | [`campaign-reports/abi-031-positive-control-protocol.md`](campaign-reports/abi-031-positive-control-protocol.md) | Main `run_20260811_160920_07a7f4`; canonical `eval_20260811_194238_7183db` | Positive-control hypothesis passed all finite/non-degenerate, source, artifact, ledger, and provenance criteria. Ordinary promotion gates fail versus MCAST 2.1 as expected; do not promote. Gate 5 autonomy-planning decision pending. |
| ABI-029 operator GPU profiles ([protocol](docs/abi-gpu-resource-profiling.md)) | One-epoch, source-identical spectral ResUNet derivatives at batch sizes 1/2/4/8/16 plus an approved two-Run canary; reproducible with `scripts/prepare_abi029_gpu_profiles.py` and `scripts/prepare_abi029_concurrency_canary.py`. | Profiling protocol and results tables. | Isolated: `run_20260810_195338_853320`, `run_20260810_195523_8326f6`, `run_20260810_195710_c261ae`, `run_20260810_195845_df2123`, `run_20260810_200027_cf7110`; concurrent batch `batch_20260810_200944_ba10a4`: `run_20260810_200944_8efa2f`, `run_20260810_200944_599e67` | Complete without OOM/retry; batch size 8 and A100 concurrency cap 2 approved for the profiled class. |

## Chronological Research Notes

No Research Notes have been recorded yet.
