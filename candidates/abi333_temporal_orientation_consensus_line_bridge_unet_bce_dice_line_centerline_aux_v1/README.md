# ABI-333 temporal orientation-consensus line bridge U-Net

ABI-333 is an exploratory family-development Candidate for GOES ABI Contrail Segmentation. It reuses the resource-safe three-frame temporal persistence/detail stem from ABI-331/332, then adds an explicit architecture-internal orientation-consensus bridge in the line/detail head.

The mechanism targets ABI-332's residual weakness: late learning raised recall, but connected-line support remained below ABI-324 and ABI-223. ABI-333 asks whether horizontal, vertical, and diagonal line evidence can be combined as a bounded differentiable consensus signal before logit emission, raising true contrail logits at the fixed Harness threshold without broad Candidate-owned thresholding, morphology, postprocessing, or Artifact Filters.

The Candidate consumes only provider-owned `abi_16ch_plus_sza_temporal` tensors with trusted `temporal_eligible_center` selection over offsets `[-1, 0, 1]`. Candidate code defines architecture only and does not own data loading, temporal lookup, sampling, target derivation, losses, metrics, thresholding, postprocessing, Artifact Filters, coordinates, Dataset Source identity, downloads, resource scheduling, prediction retention, or training lifecycle behavior.
