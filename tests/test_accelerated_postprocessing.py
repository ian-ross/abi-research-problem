from __future__ import annotations

import numpy as np
import pytest
import torch

from abi_contrail.artifact_filters import ABIArtifactFilterPipeline, GeographicFeatureFilter, ScanlineArtifactFilter
from abi_contrail.postprocessing import BoundedBatchPostprocessor, aggregate_counts, mean_connectivity, metrics_from_counts


class _CountingContextDataset:
    def __init__(self, masks: list[np.ndarray]) -> None:
        self.masks = masks
        self.context_reads = [0] * len(masks)

    def filter_context(self, index: int) -> dict[str, object]:
        self.context_reads[index] += 1
        return {"geographic_feature_mask": self.masks[index]}


def _fixture() -> tuple[torch.Tensor, torch.Tensor, _CountingContextDataset, ABIArtifactFilterPipeline]:
    probabilities = torch.zeros((3, 1, 4, 12), dtype=torch.float32)
    probabilities[0, 0, 1, 1:8] = 0.8
    probabilities[1, 0, 2, 1:11] = 0.72
    probabilities[2, 0, 3, 1:11] = torch.linspace(0.55, 0.95, 10)
    targets = torch.zeros_like(probabilities)
    targets[0, 0, 1, 1] = 1.0
    targets[2, 0, 3, 1:11] = 1.0
    masks = [np.zeros((4, 12), dtype=bool) for _ in range(3)]
    masks[0][1, 3:5] = True
    dataset = _CountingContextDataset(masks)
    pipeline = ABIArtifactFilterPipeline(
        filters=(
            GeographicFeatureFilter(pixel_buffer=0),
            ScanlineArtifactFilter(min_length_pixels=8, max_probability_std=0.01),
        ),
        pixel_area_km2=2.5,
    )
    return probabilities, targets, dataset, pipeline


def test_bounded_cpu_postprocessing_matches_reference_filters_and_metrics() -> None:
    from ml_autoresearch.problem_support.segmentation import binary_segmentation_metrics, contrail_connectivity_metric

    probabilities, targets, dataset, pipeline = _fixture()
    messages: list[str] = []
    processor = BoundedBatchPostprocessor(
        filter_pipeline=pipeline,
        device="cpu",
        batch_size=2,
        progress_callback=messages.append,
        log_every=1,
    )
    contexts = processor.prepare_contexts(dataset=dataset, sample_count=3, prediction_shape=(4, 12))
    result = processor.evaluate_operational(
        probabilities=probabilities,
        targets=targets,
        threshold=0.5,
        contexts=contexts,
    )

    expected_masks: list[torch.Tensor] = []
    expected_diagnostics: list[dict[str, object]] = []
    for index in range(3):
        reference = pipeline.apply(
            probabilities[index].numpy() >= 0.5,
            probabilities[index].numpy(),
            context={"geographic_feature_mask": dataset.masks[index]},
        )
        expected_masks.append(torch.from_numpy(reference.filtered_mask))
        expected_diagnostics.append(reference.diagnostics)
    expected_filtered = torch.stack(expected_masks)
    raw = probabilities >= 0.5
    target_masks = targets >= 0.5

    assert dataset.context_reads == [1, 1, 1]
    assert torch.equal(result.raw_predictions, raw)
    assert torch.equal(result.filtered_predictions, expected_filtered)
    assert result.filter_diagnostics == tuple(expected_diagnostics)
    assert metrics_from_counts(aggregate_counts(result.raw_counts)) == binary_segmentation_metrics(raw, target_masks)
    assert metrics_from_counts(aggregate_counts(result.filtered_counts)) == binary_segmentation_metrics(
        expected_filtered, target_masks
    )
    assert mean_connectivity(result.raw_connectivity) == pytest.approx(
        contrail_connectivity_metric(raw, target_masks), abs=1e-7
    )
    assert mean_connectivity(result.filtered_connectivity) == pytest.approx(
        contrail_connectivity_metric(expected_filtered, target_masks), abs=1e-7
    )
    assert processor.report["target_skeleton_batches"] == 2
    assert any(message.startswith("Artifact Filter phase started") for message in messages)
    assert any(message.startswith("ordinary metric phase started") for message in messages)
    assert any(message.startswith("connectivity metric phase started") for message in messages)


def test_scanline_population_std_boundary_matches_numpy_reference() -> None:
    width = 10
    base = np.linspace(0.6, 0.8, width, dtype=np.float32)
    boundary = float(np.std(base))
    probabilities = torch.from_numpy(
        np.stack(
            [
                np.full(width, 0.7, dtype=np.float32),
                base,
                np.linspace(0.55, 0.85, width, dtype=np.float32),
            ]
        )[:, np.newaxis, np.newaxis, :]
    )
    targets = torch.zeros_like(probabilities)
    dataset = _CountingContextDataset([np.zeros((1, width), dtype=bool) for _ in range(3)])
    pipeline = ABIArtifactFilterPipeline(
        filters=(ScanlineArtifactFilter(min_length_pixels=width, max_probability_std=boundary),),
        pixel_area_km2=1.0,
    )
    processor = BoundedBatchPostprocessor(filter_pipeline=pipeline, device="cpu", batch_size=2)
    contexts = processor.prepare_contexts(dataset=dataset, sample_count=3, prediction_shape=(1, width))
    result = processor.evaluate_operational(
        probabilities=probabilities,
        targets=targets,
        threshold=0.5,
        contexts=contexts,
    )

    expected = torch.stack(
        [
            torch.from_numpy(pipeline.apply(row.numpy() >= 0.5, row.numpy()).filtered_mask)
            for row in probabilities
        ]
    )
    assert torch.equal(result.filtered_predictions, expected)
    assert [record["removed_pixel_count"] for record in result.filter_diagnostics] == [10, 10, 0]


def test_threshold_sweep_counts_match_reference_pipeline_and_reuse_prepared_contexts() -> None:
    probabilities, targets, dataset, pipeline = _fixture()
    processor = BoundedBatchPostprocessor(filter_pipeline=pipeline, device="cpu", batch_size=2, threshold_tile_size=1)
    contexts = processor.prepare_contexts(dataset=dataset, sample_count=3, prediction_shape=(4, 12))
    raw_counts, filtered_counts = processor.threshold_sweep_counts(
        probabilities=probabilities,
        targets=targets,
        thresholds=(0.5, 0.75),
        contexts=contexts,
    )

    for threshold_index, threshold in enumerate((0.5, 0.75)):
        raw = probabilities >= threshold
        expected_filtered = torch.stack(
            [
                torch.from_numpy(
                    pipeline.apply(
                        raw[index].numpy(),
                        probabilities[index].numpy(),
                        context={"geographic_feature_mask": dataset.masks[index]},
                    ).filtered_mask
                )
                for index in range(3)
            ]
        )
        expected_raw_counts = {
            "positive_pixel_count": int((targets >= 0.5).sum()),
            "predicted_positive_pixel_count": int(raw.sum()),
            "true_positive_pixels": int((raw & (targets >= 0.5)).sum()),
            "false_positive_pixels": int((raw & ~(targets >= 0.5)).sum()),
            "false_negative_pixels": int((~raw & (targets >= 0.5)).sum()),
        }
        expected_filtered_counts = {
            "positive_pixel_count": int((targets >= 0.5).sum()),
            "predicted_positive_pixel_count": int(expected_filtered.sum()),
            "true_positive_pixels": int((expected_filtered & (targets >= 0.5)).sum()),
            "false_positive_pixels": int((expected_filtered & ~(targets >= 0.5)).sum()),
            "false_negative_pixels": int((~expected_filtered & (targets >= 0.5)).sum()),
        }
        assert raw_counts[threshold_index] == expected_raw_counts
        assert filtered_counts[threshold_index] == expected_filtered_counts
    assert dataset.context_reads == [1, 1, 1]


@pytest.mark.skipif(not torch.cuda.is_available(), reason="CUDA is unavailable")
def test_cuda_backend_matches_cpu_backend_on_filter_hit_fixture() -> None:
    probabilities, targets, cpu_dataset, pipeline = _fixture()
    cuda_dataset = _CountingContextDataset(cpu_dataset.masks)
    cpu = BoundedBatchPostprocessor(filter_pipeline=pipeline, device="cpu", batch_size=2)
    cuda = BoundedBatchPostprocessor(filter_pipeline=pipeline, device="cuda", batch_size=2)
    cpu_contexts = cpu.prepare_contexts(dataset=cpu_dataset, sample_count=3, prediction_shape=(4, 12))
    cuda_contexts = cuda.prepare_contexts(dataset=cuda_dataset, sample_count=3, prediction_shape=(4, 12))
    cpu_result = cpu.evaluate_operational(
        probabilities=probabilities, targets=targets, threshold=0.5, contexts=cpu_contexts
    )
    cuda_result = cuda.evaluate_operational(
        probabilities=probabilities, targets=targets, threshold=0.5, contexts=cuda_contexts
    )

    assert cuda.report["backend"] == "torch_cuda"
    assert cuda.report["max_device_batch_samples"] == 2
    assert torch.equal(cuda_result.filtered_predictions, cpu_result.filtered_predictions)
    assert cuda_result.filter_diagnostics == cpu_result.filter_diagnostics
    assert cuda_result.raw_metrics == pytest.approx(cpu_result.raw_metrics, abs=1e-7)
    assert cuda_result.filtered_metrics == pytest.approx(cpu_result.filtered_metrics, abs=1e-7)
    assert cuda_result.raw_connectivity == pytest.approx(cpu_result.raw_connectivity, abs=1e-6)
    assert cuda_result.filtered_connectivity == pytest.approx(cpu_result.filtered_connectivity, abs=1e-6)

    cpu_raw_sweep, cpu_filtered_sweep = cpu.threshold_sweep_counts(
        probabilities=probabilities,
        targets=targets,
        thresholds=(0.5, 0.75),
        contexts=cpu_contexts,
    )
    cuda_raw_sweep, cuda_filtered_sweep = cuda.threshold_sweep_counts(
        probabilities=probabilities,
        targets=targets,
        thresholds=(0.5, 0.75),
        contexts=cuda_contexts,
    )
    assert cuda_raw_sweep == cpu_raw_sweep
    assert cuda_filtered_sweep == cpu_filtered_sweep
