# ABI-340 overlap SegFormer low-cost line-consensus decoder

ABI-340 is a mechanism-changing continuation of the ABI-262 overlap SegFormer scout. It keeps the provider-owned `abi_16ch_plus_sza` input and trusted training/data/loss/auxiliary policies, but replaces broad evidence raising with a compact line-consensus head intended to recover connected thin-line evidence without ABI-263s heavier directional decoder.

The candidate is architecture-only. It does not implement data loading, sample selection, target derivation, custom losses, metrics, thresholding, postprocessing, Artifact Filters, coordinate inputs, downloads, resource scheduling, or lifecycle behavior.
