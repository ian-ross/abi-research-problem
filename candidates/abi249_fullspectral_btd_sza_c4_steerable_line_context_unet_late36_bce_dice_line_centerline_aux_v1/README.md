# ABI-249 full-spectral BTD+SZA C4 steerable line-context U-Net late36

ABI-249 is a late-improving close-continuation of ABI-248 for GOES ABI Contrail Segmentation. It keeps the exact provider-approved full-spectral ABI plus Solar Geometry Input architecture, C4 rotation-shared anisotropic line-context block, source-balanced sampling, trusted random mirroring, BCE-Dice loss, AdamW constant learning rate, batch size 4, and trusted Line/Centerline auxiliary outputs.

The parent ABI-248 Run (`run_20260911_102833_5db7f8`) completed finitely and selected epoch 12 as its best checkpoint, with best aggregate/source Dice, precision, and connectivity at the final epoch. ABI-249 therefore requests the approved `late_improving` 36-epoch budget through candidate-local `budget_request.yaml`; if denied, the exploratory budget remains the valid fallback.

Candidate code defines model architecture only. It does not implement data loading, target derivation, losses, metrics, Artifact Filters, thresholding, postprocessing, augmentation transforms, sampling policy, training loops, downloads, filesystem probes, coordinate inputs, Dataset Source identity, resource placement, or lifecycle behavior.
