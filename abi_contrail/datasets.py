"""Dataset placeholders for GOES ABI Contrail Segmentation.

Dataset loading is intentionally not implemented in ABI-001. Later tasks add
provider-owned ABI Patch discovery, label bit-plane collapse, leakage-safe
splits, and source-balanced sampling.
"""

from __future__ import annotations

ABI_PATCH_SHAPE = (16, 256, 256)
CONTRAIL_MASK_SHAPE = (1, 256, 256)

__all__ = ["ABI_PATCH_SHAPE", "CONTRAIL_MASK_SHAPE"]
