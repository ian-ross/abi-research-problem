# ABI-330 temporal-attention compact strip-token line-mixer U-Net

ABI-330 is a resource-bounded continuation of ABI-329 for GOES ABI Contrail Segmentation. ABI-329 was finite and source-informative through epoch 10, but the Harness classified the Run as a `resource_failure` after exhausting the 3,600-second exploratory wall-clock budget before completing all 12 epochs.

This Candidate keeps the ABI-329 hypothesis—provider-owned three-frame temporal attention plus differentiable horizontal/vertical strip-token line mixing for connected contrail evidence—but narrows the base width from 24 to 20 channels and shortens the strip kernels. The intended change is resource fit, not a new data, loss, threshold, postprocessing, or Artifact Filter policy.

Candidate code defines architecture only. It consumes only provider-owned `abi_16ch_plus_sza_temporal` tensors with trusted `temporal_eligible_center` selection and offsets `[-1, 0, 1]`. It does not implement data loading, temporal lookup, sampling, target construction, losses, metrics, thresholds, postprocessing, Artifact Filters, coordinate features, or resource scheduling.
