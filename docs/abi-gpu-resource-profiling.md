# ABI Candidate GPU resource profiling protocol

## Purpose

This protocol measures trusted training resource use for ABI Candidate Experiments before enabling parallel Experiment Batch execution. Candidate code does not choose devices, launch workers, measure resources, or set concurrency.

## Current execution environment

Preflight on 2026-08-10 found:

| Host GPU index | Device | Memory | Initial policy |
| --- | --- | ---: | --- |
| 0 | NVIDIA A100-PCIE-40GB | 40,960 MiB | Approved profiling and Candidate Run device |
| 1 | Tesla T4 | 15,360 MiB | Excluded until separately profiled and explicitly scheduled |

The host has 24 logical CPUs and 251 GiB RAM. Each Candidate Docker container is currently limited to 2 CPUs, 4 GiB RAM, 2 GiB shared memory, 2 GiB scratch, and 512 PIDs.

The trusted Workspace Configuration pins Candidate Docker Runs to GPU 0. Experiment Batch execution remains sequential (`max_parallel_runs = 1`) until the concurrency gate below is complete. The heterogeneous T4 must not be treated as interchangeable with the A100.

## Trusted measurements

Each training attempt writes:

- `outputs/resource_profile.json` for the latest attempt;
- `outputs/resource_profiles/batch_size_<N>.json` for batch-size-specific retry/profiling evidence;
- normal Run metadata with requested/effective batch size and Resource Failure retry history.

The resource profile records:

- device type, CUDA device index/name, compute capability, total memory, and free memory at start;
- peak PyTorch CUDA allocated and reserved bytes;
- total, training-phase, and validation-phase wall time;
- processed sample counts and training/validation throughput;
- failed-attempt reason when training does not complete.

PyTorch reserved memory does not include every driver/context allocation or memory used by sibling processes. Parallel recommendations therefore require an actual concurrent canary and external `nvidia-smi` observation in addition to per-Run profiles.

## Representative classes

1. **Lifecycle control:** `abi025_manual_canary_v1`. This tiny model checks measurement plumbing but is not concurrency evidence for scientific candidates.
2. **High-resolution residual scout:** `abi_spectral_resunet_scout_v1`. This 16-channel, 256×256 residual encoder-decoder is the initial representative scientific architecture.
3. **Unprofiled architecture:** any materially different family, resolution, temporal input, auxiliary-head structure, attention block, or activation layout. Parameter count alone does not assign a class. Unprofiled architectures run sequentially.

A class recommendation applies only to candidates with comparable input/output shapes, activation structure, trusted loss, and effective batch size.

## Bounded profiling matrix

All real-data commands require an explicit human execution decision on the approved GPU environment. Stop after the first OOM at a given stage and preserve Resource Failure artifacts.

### Stage A — isolated batch-size characterization

For the high-resolution residual scout, create operator-authored profiling variants that differ only in manifest batch size. Use batch sizes `1, 2, 4, 8, 16`, one epoch, at most 32 training and 32 validation samples per Dataset Source, two qualitative samples, Docker GPU execution, and GPU 0 only.

For each batch size record:

- controlled smoke outcome and parameter count;
- requested/effective batch size and any Resource Failure retry;
- peak allocated/reserved memory;
- training and validation throughput;
- run wall time and Docker resource limits.

Do not continue to a larger batch size after OOM unless the failure is classified as unrelated to GPU memory.

### Stage B — bounded real-data confirmation

Select the largest batch size that:

- completed without Resource Failure retry;
- used no more than 70% of A100 memory by observed reserved/process memory;
- leaves at least 8 GiB absolute headroom;
- does not materially reduce throughput relative to the preceding size.

Confirm that size with one epoch and 32 samples per Dataset Source before using it for a longer scientific Run. ABI-025 Gate 6 remains separately bounded to 1,024 samples per Dataset Source and 12 epochs.

### Stage A/B results — 2026-08-10

All five representative high-resolution residual scout profiles completed on the pinned A100 without GPU OOM or Resource Failure retry. Each Run used 64 combined training samples and 64 combined validation samples (32 per Dataset Source), one epoch, the validated runner `ml-autoresearch-runner:abi-research-problem-4ea195c26918b493-13b99524f1`, and the 2,539,889-parameter source model.

| Batch | Run | Peak allocated | Peak reserved | Train samples/s | Train seconds | Validation samples/s | Run seconds | Retry |
| ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| 1 | `run_20260810_195338_853320` | 386.1 MiB | 494.0 MiB | 20.20 | 3.168 | 0.968 | 70.49 | none |
| 2 | `run_20260810_195523_8326f6` | 745.3 MiB | 936.0 MiB | 35.36 | 1.810 | 0.967 | 69.23 | none |
| 4 | `run_20260810_195710_c261ae` | 1,454.3 MiB | 1,714.0 MiB | 46.27 | 1.383 | 0.978 | 68.07 | none |
| 8 | `run_20260810_195845_df2123` | 2,873.3 MiB | 3,404.0 MiB | 52.45 | 1.220 | 0.980 | 67.80 | none |
| 16 | `run_20260810_200027_cf7110` | 5,717.3 MiB | 7,042.0 MiB | 47.44 | 1.349 | 0.974 | 68.30 | none |

**Isolated recommendation:** use batch size 8 for this profiled architecture class. It delivered the highest observed training throughput and reserved about 8.3% of the 40 GiB A100. Batch size 16 doubled reserved memory while reducing throughput by about 9.6%, so it is not preferred. Batch size 4 remains a conservative fallback for longer Runs or candidates with modestly larger activation envelopes.

Validation/postprocessing dominated wall time at roughly 65–66 seconds and about 0.97 samples/s for every batch size. Consequently, isolated GPU memory arithmetic alone cannot justify parallel execution: the concurrency canary must also test CPU/DataLoader and provider-postprocessing contention. No OOM boundary was observed within the approved matrix; larger batch sizes are not authorized because batch 16 was already throughput-negative.

At batch size 8, two isolated reserved-memory envelopes sum to 6,808 MiB (16.6% of A100 memory), and four sum to 13,616 MiB (33.2%). These are planning estimates only. The initial simultaneous-candidate recommendation remains **two**, contingent on the Stage C concurrent canary, with the Harness cap kept at one until that canary passes. Unknown or materially different architectures remain sequential.

### Stage C — concurrency characterization

Run a two-candidate Experiment Batch containing closely comparable, one-epoch profiling candidates, with 32 samples per Dataset Source and the Stage B batch size. Keep both Runs pinned to GPU 0. Capture per-Run profiles plus external aggregate `nvidia-smi` memory/utilization at one-second intervals.

Concurrency 2 is eligible only if:

- both siblings complete without Resource Failure retry;
- aggregate observed GPU memory remains at or below 70% of 40,960 MiB and leaves at least 8 GiB free;
- no candidate exceeds its isolated reserved-memory envelope by more than 15%;
- aggregate samples/second is at least 1.5× sequential throughput;
- container CPU/RAM limits and DataLoader workers do not create sustained starvation.

Test concurrency 3 only after separate human approval and only if the two-Run canary remains below 55% aggregate GPU memory while satisfying the throughput criterion. The hard Harness cap remains 4; this protocol does not approve concurrency 4.

### Stage C results — 2026-08-10

Human-approved Experiment Batch `batch_20260810_200944_ba10a4` ran two byte-identical batch-size-8 replicas concurrently on GPU 0:

| Candidate | Run | Peak allocated | Peak reserved | Train samples/s | Validation samples/s | Run seconds | Retry |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| concurrency A | `run_20260810_200944_8efa2f` | 2,873.3 MiB | 3,404.0 MiB | 37.04 | 0.977 | 68.59 | none |
| concurrency B | `run_20260810_200944_599e67` | 2,873.3 MiB | 3,404.0 MiB | 37.51 | 0.970 | 69.06 | none |

Both Runs completed independently in one attempt with isolated artifacts. Neither exceeded the isolated batch-size-8 reserved-memory envelope. The one-second external monitor captured 93 samples, a maximum 7,830 MiB process/device memory use (19.1% of 40,960 MiB), and a minimum 32,508 MiB free (79.4%, or 31.7 GiB). Memory remained above 6,000 MiB for 67 samples, confirming sustained overlap. No GPU OOM, host/container Resource Failure, retry, or artifact collision occurred.

For the batch-level throughput criterion, end-to-end processed-sample throughput increased from 128 samples / 67.80 seconds = 1.89 samples/s in the isolated batch-size-8 Run to 256 samples / 69.06 seconds = 3.71 samples/s concurrently, a 1.96× ratio. The short training phase showed contention—aggregate training throughput was 74.55 samples/s versus 52.45 isolated, or 1.42×—but validation throughput per Run was essentially unchanged and end-to-end overlap exceeded the reviewed 1.5× criterion. This distinction is retained as a residual risk for longer, training-dominated Runs.

**Approved policy:** Harness concurrency is capped at two on the A100 for controlled Experiment Batches of comparable 2.54M-parameter, 16-channel, 256×256 spectral residual U-Net candidates at batch size 8 or lower. Batch size 8 is preferred; batch size 4 is the conservative fallback. This evidence does not approve concurrency three or four, batch sizes above 8, materially different architectures, or any T4 execution. Such workloads remain sequential pending separate profiling and human review.

## Preparation and execution commands

Prepare immutable profiling derivatives without importing Candidate code or reading data:

```bash
PROFILE_ROOT=/tmp/abi029-spectral-resunet-profiles
uv run python scripts/prepare_abi029_gpu_profiles.py \
  --source candidates/abi_spectral_resunet_scout_v1 \
  --output "$PROFILE_ROOT"
```

After runtime-image validation and the batch-size execution gate, run one profile at a time in ascending batch-size order. Replace `<N>` and `<validated-runner-image>` with the reviewed values:

```bash
uv run ml-autoresearch run-candidate \
  --candidate "$PROFILE_ROOT/abi_spectral_resunet_scout_v1_profile_bs<N>" \
  --workspace-root . \
  --max-samples 32 \
  --max-prediction-samples 2 \
  --backend docker \
  --docker-image <validated-runner-image> \
  --docker-enable-gpu \
  --docker-gpu-device 0 \
  --docker-rootless-container-root
```

Stop after the first GPU OOM. Do not invoke ABI-025 `execute-next-action` as part of the profile sweep; its separately approved 1,024-per-source scientific Run remains a later gate.

After isolated-result review and the separate concurrency execution gate, prepare and execute the two-Run canary:

```bash
CANARY_ROOT=/tmp/abi029-concurrency-canary
uv run python scripts/prepare_abi029_concurrency_canary.py \
  --source candidates/abi_spectral_resunet_scout_v1 \
  --output "$CANARY_ROOT" \
  --batch-size 8 \
  --candidate-count 2

nvidia-smi \
  --query-gpu=timestamp,index,name,memory.used,memory.free,utilization.gpu \
  --format=csv -l 1 > /tmp/abi029-concurrency-nvidia-smi.csv &
MONITOR_PID=$!

uv run ml-autoresearch run-experiment-batch \
  --batch "$CANARY_ROOT" \
  --batches-root batches \
  --runs-root /data/iross/abi-ml-autoresearch/runs \
  --workspace-root . \
  --max-samples 32 \
  --max-parallel-runs 2 \
  --max-prediction-samples 2 \
  --backend docker \
  --docker-image ml-autoresearch-runner:abi-research-problem-4ea195c26918b493-13b99524f1 \
  --docker-enable-gpu \
  --docker-gpu-device 0 \
  --docker-rootless-container-root

kill "$MONITOR_PID"
```

The monitor must be stopped on command failure as well; an operator shell should use a trap when launching the approved canary.

## Agent Experiment Batch policy

The Agent Control Boundary may propose an Experiment Batch only when:

- two to four candidates test one shared hypothesis or controlled factor comparison;
- every candidate belongs to a trusted profiled resource class;
- requested concurrency does not exceed the Agent-visible Harness cap;
- batch and per-candidate budgets are explicit;
- the batch is one primary handoff and execution remains separately human/Harness controlled.

Use sequential Candidate Submissions for new architecture families, heterogeneous resource envelopes, or unclear memory behavior. If a required scheduling policy is unavailable, create a Capability Request rather than adding Candidate-owned scheduling.

## Human gates

1. **Instrumentation gate:** trusted code/tests and runner image validation may proceed without real-data training.
2. **Batch-size execution gate:** approve Stage A/B commands and confirm the target GPU is idle.
3. **Concurrency execution gate:** review isolated measurements before approving the two-candidate batch canary.
4. **Policy gate:** record the selected batch-size classes, headroom, and `max_parallel_runs` before refreshing Agent-visible guidance.

No profiling approval launches a later scientific or autonomous Run automatically.
