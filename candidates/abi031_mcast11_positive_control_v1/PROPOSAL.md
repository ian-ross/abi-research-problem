# ABI-031 MCAST 1.1-lineage positive-control proposal

## Hypothesis

A manually authored, randomly initialized MCAST 1.1-lineage architecture will remain finite and produce non-degenerate predictions through the complete trusted Candidate Execution path, distinguishing Harness reliability from the failed ABI-025 Agent-generated architecture.

## Comparison Target

The reliability criteria are preregistered in `campaign-reports/abi-031-positive-control-protocol.md`. Canonical MCAST 1.1 and 2.1 from registry `abi-mcast-working-validation-v1` provide provenance and scientific context, but the positive control is not required to beat either baseline.

## Expected Effect

The familiar SMP U-Net/ResNet-18 topology and MCAST 1.1 spectral transforms should provide finite optimization and predictions containing both contrail-positive and negative pixels after bounded training.

## Implementation Sketch

Derive C11, C14, and C13-C15 from the provider-supplied `abi_16ch` tensor, apply the fixed MCAST 1.1 means and standard deviations, and pass the normalized three-plane tensor through `segmentation_models_pytorch.Unet(encoder_name="resnet18", encoder_weights=None, in_channels=3, classes=1)`. Return one `mask_logits` tensor. Do not load files or weights.

## Contract Features Used

- Input mode: `abi_16ch`; source indices 16/17 (longitude/latitude) remain excluded.
- Output form: `mask_logits`.
- Provider-owned `combined_source_balanced` sampling and no augmentation.
- Trusted `bce_dice`, AdamW, metrics, Artifact Filters, evaluation, and execution.

## Budget Requested

Sequential pinned-A100 execution only. First run one epoch with 32 training and 32 validation samples per Dataset Source. After review, run at most 1,024 samples per Dataset Source for three epochs at the reviewed batch size, followed by one 3,088-sample Working Validation evaluation and four bounded diagnostic samples. The measured model size is 14,328,209 parameters under the trusted ABI 25,000,000-parameter smoke budget.

## Success Criteria

All required losses, metrics, gradients, parameters, and checkpoint tensors are finite; full-validation predictions satisfy the preregistered positive-pixel bounds; aggregate and MIT/Google raw/filtered Dice exceed the preregistered numerical floor; and all Run, evaluation, provenance, resource, qualitative, index, and ledger evidence is complete and linked.

## Fallback Next Decision

Any static, numerical, resource, lifecycle, or non-degeneracy failure stops the campaign for human review. A recorded failed positive control blocks planning for fully automatic autonomy; it does not trigger an automatic repair or rerun.
