# ABI-025 Agent Control Boundary handoff campaign report

## Scope

Human Execution Gate 6 authorized separate execution of the previously reviewed Agent-generated Candidate Submission `abi_spectral_resunet_scout_v1`. Trusted Harness configuration enforced a maximum of 1,024 samples per Dataset Source. The Candidate requested 12 epochs and batch size 4.

## Run and evaluation

- Candidate Run: `run_20260810_204928_ab0218`
- Full Working Validation evaluation: `eval_20260811_054134_51fc4c`
- Canonical target registry: `abi-mcast-working-validation-v1`
- Training samples: 2,048 combined (1,024 per Dataset Source)
- Validation samples during training: 2,048 combined (1,024 per Dataset Source)
- Post-Run Evaluation samples: 3,088 (MIT 1,232; Google 1,856)
- Epochs: 12
- Batch size: 4
- Device: pinned NVIDIA A100-PCIE-40GB, CUDA device 0
- Peak CUDA memory: 1,714 MiB reserved, 1,454 MiB allocated
- Diagnostic bound: four samples and eight GeoTIFFs

The source copied into the Run matches the reviewed canonical Candidate byte-for-byte. Static validation still passes. The model summary records only ABI channels 1–16 and explicitly forbids longitude, latitude, and source channel indices 16/17. Candidate source owns architecture only; trusted training, loss, metrics, filters, sampling, augmentation, data loading, and read-only data mounts remained provider/Harness-owned.

The original synchronous `execute-open-actions` client reached its two-hour caller timeout while the Docker operation continued. No duplicate Run was launched. Docker exited successfully after writing all required artifacts; the stale `training` metadata and missing terminal ledger event were reconciled once, using the Harness artifact validation and metadata/event helpers with duplicate-event preconditions.

## Scientific result

The Candidate is a bad research result and must not be promoted:

- Training loss became non-finite after the first two batches of epoch 1 and remained non-finite for all remaining batches and epochs.
- The selected epoch-1 checkpoint contains 2,539,889 non-finite parameter values out of 2,539,921 tensor values; the 32 finite values are non-parameter counters.
- Full-validation predictions contain zero positive pixels.
- Raw and filtered Dice: approximately `1.41e-13`.
- Raw and filtered recall: approximately `1.41e-13`.
- MIT filtered Dice: approximately `2.05e-13`.
- Google filtered Dice: approximately `4.54e-13`.
- MCAST 2.1 canonical filtered Dice: `0.387284866824332`.

The provider-owned `acceptance_report.json` is tied to the verified canonical registry and records `gate_flags_present` / `human_review_required`. Failure flags are:

1. aggregate below best baseline;
2. filtered recall regression;
3. catastrophic MIT Dataset Source failure;
4. catastrophic Google Dataset Source failure.

The high Contrail Connectivity value is not meaningful for this all-negative prediction and must not be interpreted as scientific quality.

## Artifact and ledger validation

The Run contains validation and smoke logs, `metrics.jsonl`, `final_metrics.json`, `best_metrics.json`, the selected checkpoint, two bounded training prediction samples, `resource_profile.json`, and model summary. The evaluation contains aggregate and per-sample metrics, a 19-threshold sweep, four bounded diagnostics/eight GeoTIFFs, evaluation metadata, and the provider-owned acceptance report.

The Research Ledger records proposal creation, Candidate creation/submission, Run start/completion, evaluation request, and evaluation completion. No open executable action remains.

## Residual risks and final-gate recommendation

- The trusted training path did not reject non-finite loss or non-finite model parameters, so it spent approximately 8.8 hours completing a hopeless Run and still classified the artifact-complete Run as `completed`.
- The synchronous caller timeout can orphan host-side finalization while Docker continues; this Run required one explicit reconciliation after container completion.
- Validation dominated runtime (about 31,573 seconds versus 257 training seconds), making non-finite fail-fast behavior especially important.
- `evaluation_metadata.json` reports the in-container native evaluator although the outer execution backend was Docker.
- `acceptance_report.json` remains provider-owned but is not listed in evaluation metadata or separately ledger-recorded.
- Provider Git provenance records a dirty working tree.

**Recommendation for Human Final Gate 7: no-go on a fully automatic autonomy iteration until trusted non-finite fail-fast validation and robust detached/synchronous Run finalization are addressed and validated.** This recommendation does not itself record the required human decision.
