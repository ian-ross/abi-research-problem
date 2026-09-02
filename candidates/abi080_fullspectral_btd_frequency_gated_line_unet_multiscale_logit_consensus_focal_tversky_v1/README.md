# ABI-080 Full-spectral BTD frequency-gated line U-Net multi-scale logit consensus

ABI-080 is a bounded family-development continuation of ABI-068. It keeps the full-spectral `abi_16ch` input, thermal BTD feature planes, learned 1x1 channel mixer, frequency-gated U-Net decoder, trusted `focal_tversky` loss, and low-weight provider-derived centerline auxiliary output.

The controlled architecture change is the final mask head: a `MultiScaleLogitConsensusHead` blends logits from local-detail, broad-context, and oriented-ridge branches with an in-model softmax gate. The intent is to recover some of ABI-066's precision/connectivity and reduce ABI-068's negative-patch clutter without using candidate-owned thresholding, postprocessing, Artifact Filters, data loading, loss code, target derivation, metrics, resource placement, network access, or pretrained weights.

This Candidate must be interpreted under the Harness-owned 1,024-record-per-Dataset-Source/split representative cap and current 12-epoch, batch-size-4, constant-LR policy. Capped evidence is family-development evidence only, not a full-data promotion claim.
