# Candidate losses are selected from trusted allowlists

GOES ABI contrail segmentation candidates select loss functions from a trusted allowlist exposed by the research problem spec. Initial losses are `bce_dice`, `focal_tversky`, and `bce_dice_cldice`. Candidate code does not define arbitrary losses, because loss functions affect the optimization objective and evaluation comparability. New losses require an explicit capability request, approval, implementation in trusted harness/problem-support code, and an update to the agent control boundary contract.
