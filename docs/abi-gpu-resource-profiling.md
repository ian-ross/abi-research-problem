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

### Stage C — concurrency characterization

Run a two-candidate Experiment Batch containing closely comparable, one-epoch profiling candidates, with 32 samples per Dataset Source and the Stage B batch size. Keep both Runs pinned to GPU 0. Capture per-Run profiles plus external aggregate `nvidia-smi` memory/utilization at one-second intervals.

Concurrency 2 is eligible only if:

- both siblings complete without Resource Failure retry;
- aggregate observed GPU memory remains at or below 70% of 40,960 MiB and leaves at least 8 GiB free;
- no candidate exceeds its isolated reserved-memory envelope by more than 15%;
- aggregate samples/second is at least 1.5× sequential throughput;
- container CPU/RAM limits and DataLoader workers do not create sustained starvation.

Test concurrency 3 only after separate human approval and only if the two-Run canary remains below 55% aggregate GPU memory while satisfying the throughput criterion. The hard Harness cap remains 4; this protocol does not approve concurrency 4.

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
