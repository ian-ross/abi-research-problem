# ABI-032 MCAST 1.1 focal-Tversky continuation

This Candidate Experiment is a one-factor family-development continuation of `abi031_mcast11_positive_control_v1`.

It keeps the same fixed MCAST 1.1 C11, C14, and C13-C15 transforms and randomly initialized SMP U-Net/ResNet-18 architecture. The manifest changes only the trusted primary loss from `bce_dice` to recall-oriented `focal_tversky`.

## Contract summary

- Input: provider-approved `abi_16ch` only; no longitude or latitude.
- Output: one `mask_logits` tensor.
- Data: provider-owned `combined_source_balanced` sampling and no augmentation.
- Training: Harness-owned AdamW, learning rate 0.001, batch size 4, three epochs.
- Loss, metrics, Artifact Filters, checkpointing, and data access remain trusted provider/Harness responsibilities.

See `PROPOSAL.md` for the preregistered hypothesis, comparison targets, budget, and decision criteria.
