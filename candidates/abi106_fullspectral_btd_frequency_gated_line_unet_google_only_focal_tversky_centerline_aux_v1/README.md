# ABI-106 full-spectral BTD frequency-gated line U-Net Google-only continuation

ABI-106 is a data-policy continuation of ABI-068. It keeps the same full-spectral ABI plus thermal BTD frequency-gated line U-Net architecture, trusted focal-Tversky primary loss, provider-derived Centerline Target auxiliary output, trusted random mirroring, AdamW learning rate, batch size, and epoch budget. The controlled change is the trusted provider/Harness sampling policy: `combined_source_balanced` is replaced with `google_only`.

The hypothesis is that the Google provenance subset may supply a cleaner thin-contrail operating point for the focal-Tversky frequency-gated branch, improving Google-source filtered Dice, precision, or positive-area discipline enough to clarify whether recent source-balanced training is masking a source-specialized strength. Validation remains Harness-owned; this candidate does not implement data loading, sampling, augmentation, metrics, thresholds, Artifact Filters, or target derivation.

The model accepts only provider-approved `abi_16ch` tensors and derives deterministic BTD features solely from ABI channels 1-16. It never receives longitude, latitude, or reconstructed coordinate inputs. It emits `mask_logits` and `centerline_logits` for the trusted auxiliary target declared in the manifest.
