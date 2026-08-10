# ABI-029 two-Run concurrency canary

## Shared hypothesis

Two identical, independently initialized replicas of the profiled spectral residual U-Net can train concurrently on the pinned A100 without Resource Failure, artifact collision, or unacceptable throughput contention.

## Shared comparison target

Compare each concurrent Run with the isolated batch-size-8 profile `run_20260810_195845_df2123`; scientific metric ordering is out of scope.

## Per-candidate variant rationale

Replicas A and B intentionally have byte-identical model source and training policy so observed differences measure concurrent execution effects rather than architecture changes.

## Expected ordering or decision criteria

Both Runs should complete independently with similar memory envelopes. Aggregate throughput should be at least 1.5 times isolated throughput, aggregate GPU memory must remain within the reviewed headroom, and neither Run may use Resource Failure retry.

## Batch-level success criteria

The Harness enforces concurrency two, creates isolated Run/artifact records, preserves independent failure handling, records two resource profiles, and leaves at least 8 GiB and 30% A100 memory headroom.

## Requested budget/concurrency

Exactly 2 Runs, concurrency 2, batch size 8, one epoch, at most 32 training and validation samples per Dataset Source, two qualitative samples per Run, no Post-Run Evaluation, and no automatic follow-up.
