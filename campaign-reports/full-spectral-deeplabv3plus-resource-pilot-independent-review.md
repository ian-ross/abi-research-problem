# Full-spectral DeepLabV3+ resource-pilot independent review

## Conclusion

A fresh-context read-only review found no substantive blocker. The evidence supports the completed Run as a successful contract, resource, finite-state, and gross non-degeneracy pilot. Its one-epoch score is not architecture-ranking evidence.

## Verified evidence

- **Materially different family:** Candidate `abi043_fullspectral_deeplabv3plus_resource_pilot_v1` is a randomly initialized 16-channel SMP DeepLabV3+ with ResNet-18, distinct from the prior U-Net families. Its source fixes `encoder_weights=None`, `in_channels=16`, and `classes=1`.
- **Exact reduced budget:** Trusted local policy set `max_samples=32`, `max_epochs=1`, batch ceiling 4, concurrency 1, GPU 0, and a 3,600-second timeout. The Candidate manifest requested one epoch and contained no record cap, selector, source override, or selector seed.
- **Exactly-once lifecycle:** The ledger contains one `agent_handoff_ingested`, one `candidate_submitted`, one `run_started`, and one `run_completed` event for stable Run `run_20260813_131515_ff53ab`, with no corresponding failure event. One container attempt completed with zero retries.
- **No Evaluation, Batch, or scout:** No evaluation artifacts exist under this Run, and it completed one epoch.
- **Finite/checkpoint evidence:** Losses and all reported metrics are finite. A recursive audit covered 27 JSON/JSONL records and 516 numeric values; 183 checkpoint tensors contained 12,383,918 finite values.
- **Source-specific non-degeneracy:** Aggregate, Google, and MIT predicted-positive fractions are strictly between zero and one in raw and filtered metrics. Four bounded masks contained 4,685, 30,153, 3,698, and 15,156 positive pixels out of 65,536.
- **Interpretation:** The report limits the result to contract, resource, finite-state, batch-compatibility, and gross non-degeneracy evidence.

## Comparison residual

The comparison design expected no augmentation and AdamW at `0.001`. The concrete pre-run proposal selected provider-owned `random_mirroring` and AdamW at `0.0003`. The proposal and `proposal_created` event preceded Candidate submission and execution, and both settings used trusted contract surfaces.

This difference prevents a clean architecture-only comparison with the MCAST-lineage positive control. It does not invalidate the resource, contract, lifecycle, finite-state, or non-degeneracy evidence, and it does not justify ranking the family.

## Review limits

The review was read-only. It inspected durable repository and Run artifacts rather than rerunning GPU work. Reported ABI and focused Harness validation totals were checked as recorded evidence but were not rerun during this independent review.
