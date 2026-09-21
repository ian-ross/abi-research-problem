# ABI-369 temporal-attention pre-decoder line-support no-mirroring late36

## Classification

Family-development continuation / controlled data-policy continuation in the temporal-attention architecture family. This is not a promotion claim and not whole-validation evidence.

## Hypothesis

ABI-350's temporal-attention pre-decoder line-support model is the current strongest capped temporal-eligible comparator, but its recent descendants still oscillate among compact precision, fixed-threshold recall, and connected-line continuity. Trusted `random_mirroring` may help generic invariance, but it may also blur physically meaningful GOES scan/illumination orientation cues used by temporal attention and orientation line-support gates.

The hypothesis is that disabling mirroring with the allowlisted `none` augmentation policy may improve MIT/source balance, recall, or connected-line continuity on this specific ABI-350 scaffold without changing candidate-owned data, augmentation implementation, loss, metrics, thresholds, postprocessing, or temporal provisioning.

## Comparison Target

- ABI-350 (`run_20260919_013306_9ca44e`): direct same-architecture temporal-attention pre-decoder line-support parent with trusted random mirroring.
- ABI-337 (`run_20260917_201833_57b081`): related temporal no-mirroring control that nearly tied its mirrored parent while shifting MIT/recall but worsening connectivity/clutter.
- ABI-223 (`run_20260908_154531_8c7e2b`): temporal-attention connectivity comparator.
- ABI-202/249: full-validation context only, not direct temporal-eligible promotion targets.

## Expected Effect

Expected positive signal would be one or more of: higher MIT filtered Dice, higher fixed-threshold recall, or higher filtered connectivity than ABI-350 while keeping aggregate/source filtered Dice close to ABI-350 and avoiding a large filtered-positive footprint increase. A negative signal would be the ABI-337-style trade-off on this stronger scaffold: small recall/source changes accompanied by worse connectivity, precision, Google Dice, or clutter.

## Implementation sketch

Copy the ABI-350 architecture unchanged. The model keeps the three-frame provider-owned temporal input, finite ABI+SZA+BTD feature builder, shared frame projection, per-pixel temporal attention/change stem, U-Net encoder, ASPP bottleneck, three decoder stages, `PreDecoderLineSupportGate` modules at encoder scales 2, 1, and 0, and trusted mask/Line/Centerline heads.

The only controlled change from ABI-350 is manifest-selected augmentation policy: `random_mirroring` -> `none`. This uses the provider/Harness trusted augmentation allowlist; Candidate code does not implement augmentation transforms.

## Contract Features Used

- Input mode: `abi_16ch_plus_sza_temporal`.
- Trusted frame selection: `temporal_eligible_center`.
- Temporal offsets: `[-1, 0, 1]`.
- No longitude/latitude inputs.
- Trusted sampling policy: `combined_source_balanced`.
- Trusted augmentation policy: `none`.
- Trusted loss: `bce_dice` with trusted Line and Centerline `weighted_bce` auxiliaries.
- Optimizer/scheduler: AdamW with constant LR.
- Candidate source defines architecture only and does not implement data loading, temporal lookup, sample selection, augmentation, losses, metrics, Artifact Filters, thresholds, postprocessing, training loops, downloads, coordinates, Dataset Source identity, resource scheduling, or lifecycle behavior.

## Budget Requested

Request the Harness-owned `late_improving` budget for 36 epochs via `budget_request.yaml`, with exploratory fallback if denied. The request is justified by ABI-350's epoch-33 best checkpoint and by ABI-337's late-budget no-mirroring control showing that the augmentation-policy trade-off is trajectory-dependent.

## Success criteria

ABI-369 is useful if it completes finitely and shows at least one targeted improvement over ABI-350 without a material aggregate/source regression:

- MIT filtered Dice or fixed-threshold recall improves without a large Google/source regression;
- filtered connectivity improves or remains near ABI-350 while recall/source balance improves;
- filtered predicted-positive pixels remain close to ABI-350 rather than expanding into ABI-356/360-style broad recall footprints;
- source-balanced behavior has no MIT or Google collapse.

Hard-stop evidence for this exact data-policy branch would be contract/smoke failure, non-finite behavior, persistent prediction collapse, or the ABI-337-style pattern of small recall/source shifts with worse connectivity, precision, Google Dice, or negative-patch clutter.

## Fallback decision

If ABI-369 repeats the ABI-337 pattern, do not promote and do not spend another Run on unchanged no-mirroring, seed, or augmentation-only variants. Broaden to a genuinely mechanism-changing temporal backbone, single-frame C4/detail recall support, or trusted evaluation/policy question tied to a specific failure mode. If the Harness denies the late budget, treat the exploratory fallback as the bounded Result and continue from its evidence.
