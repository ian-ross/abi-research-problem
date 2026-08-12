# ABI-037 MCAST 1.1 BCE-Dice-clDice continuation

This Candidate Experiment is a one-factor family-development continuation of `abi032_mcast11_focal_tversky_v1`.

It keeps the same fixed MCAST 1.1 C11, C14, and C13-C15 transforms and randomly initialized SMP U-Net/ResNet-18 architecture. The manifest changes only the trusted primary loss from `focal_tversky` to `bce_dice_cldice` to test whether continuity supervision improves connected thin structures while restoring precision-recall balance.

## Contract summary

- Input: provider-approved `abi_16ch` only; no longitude or latitude.
- Output: one `mask_logits` tensor.
- Data: provider-owned `combined_source_balanced` sampling and no augmentation.
- Training: Harness-owned AdamW, learning rate 0.001, batch size 4, three epochs.
- Loss, metrics, Artifact Filters, checkpointing, and data access remain trusted provider/Harness responsibilities.

See `PROPOSAL.md` for the preregistered hypothesis, comparison targets, budget, and decision criteria.
