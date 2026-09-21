# ABI-361 temporal shift-aligned detail-consensus line support late36

ABI-361 is a mechanism-changing continuation of the temporal-attention pre-decoder line-support branch. It keeps provider-owned three-frame `abi_16ch_plus_sza_temporal` inputs, trusted temporal-eligible center selection, BCE-Dice, Line and Centerline auxiliary targets, source-balanced sampling, random mirroring, and batch size 2.

The model changes ABI-350/360 by aligning previous and next frame feature maps to the center frame through a learned soft bank of small zero-padded integer shifts before temporal attention and line-supported decoding. The hypothesis is that center-aligned neighbor detail will raise true-positive line evidence and connectivity at threshold 0.5 without the broad low-precision footprint seen in recall-heavy temporal heads.

This candidate does not implement data loading, temporal lookup, cache access, target derivation, losses, metrics, Artifact Filters, thresholds, postprocessing, coordinate/location features, Dataset Source identity features, downloads, or resource scheduling.
