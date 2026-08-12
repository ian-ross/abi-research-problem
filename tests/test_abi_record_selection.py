from __future__ import annotations

from dataclasses import replace

import pytest

from abi_contrail.datasets import ABIPatchIndexRecord
from abi_contrail.record_selection import (
    BOUNDED_SELECTION_POLICY_NAME,
    BOUNDED_SELECTION_POLICY_SEED,
    BOUNDED_SELECTION_POLICY_VERSION,
    canonical_record_identity,
    select_representative_records,
    selected_record_identity_digest,
)


def _record(
    index: int,
    *,
    source: str = "mit",
    split: str = "train",
    scene: str | None = None,
    positive: bool = False,
) -> ABIPatchIndexRecord:
    return ABIPatchIndexRecord(
        dataset_source=source,  # type: ignore[arg-type]
        split=split,  # type: ignore[arg-type]
        scene_name=scene or f"scene-{index // 2}",
        scene_index=index // 2,
        goes_time=f"2026-08-12T00:{index:02d}:00Z",
        row=(index % 2) * 256,
        col=0,
        positive=positive,
        sample_index=index if source == "google" else None,
    )


def _identities(records: tuple[ABIPatchIndexRecord, ...]) -> set[str]:
    return {canonical_record_identity(record) for record in records}


def test_canonical_identity_tracks_source_patch_location_not_label_stratum() -> None:
    record = _record(0, positive=False)

    assert canonical_record_identity(record) == canonical_record_identity(
        replace(record, positive=True)
    )
    moved = replace(record, row=256)
    assert canonical_record_identity(record) != canonical_record_identity(moved)
    assert selected_record_identity_digest((record,)) != selected_record_identity_digest((moved,))


def test_capped_selection_is_deterministic_and_independent_of_record_order() -> None:
    records = tuple(_record(index, positive=index % 3 == 0) for index in range(12))

    forward = select_representative_records(
        records,
        5,
        dataset_source="mit",
        split="train",
    )
    reversed_input = select_representative_records(
        tuple(reversed(records)),
        5,
        dataset_source="mit",
        split="train",
    )

    assert forward.records == reversed_input.records
    assert forward.metadata == reversed_input.metadata
    assert _identities(forward.records) != _identities(records[:5])


def test_selection_spreads_each_positivity_stratum_across_scenes_or_provenances() -> None:
    records = tuple(
        _record(index, scene=f"scene-{index // 2}", positive=index % 2 == 0)
        for index in range(8)
    )

    selected = select_representative_records(
        records,
        4,
        dataset_source="mit",
        split="train",
    )

    assert {record.positive for record in selected.records} == {False, True}
    assert len({record.scene_name for record in selected.records}) == 4
    assert selected.metadata["selected_positive_count"] == 2
    assert selected.metadata["selected_negative_count"] == 2
    assert selected.metadata["selected_scene_or_provenance_count"] == 4


def test_google_selection_uses_provenance_scene_names_for_spread() -> None:
    records = tuple(
        _record(
            index,
            source="google",
            scene=f"train-provenance-{index // 2}/patch-{index}.zarr",
            positive=index % 2 == 0,
        )
        for index in range(8)
    )

    selected = select_representative_records(
        records,
        4,
        dataset_source="google",
        split="train",
    )

    assert len({record.scene_name for record in selected.records}) == 4
    assert selected.metadata["coverage_group"] == "google_provenance_scene_name"


def test_selection_rejects_cross_source_or_cross_split_input() -> None:
    mit_train = _record(0)
    google_train = replace(_record(1), dataset_source="google", sample_index=1)
    mit_validation = replace(_record(2), split="validation")

    with pytest.raises(ValueError, match="Dataset Source boundary"):
        select_representative_records(
            (mit_train, google_train),
            1,
            dataset_source="mit",
            split="train",
        )
    with pytest.raises(ValueError, match="Leakage-Safe Split boundary"):
        select_representative_records(
            (mit_train, mit_validation),
            1,
            dataset_source="mit",
            split="train",
        )


def test_positive_and_negative_coverage_handles_tiny_and_minority_strata() -> None:
    records = tuple(_record(index, positive=index == 0) for index in range(6))

    cap_one = select_representative_records(records, 1, dataset_source="mit", split="train")
    cap_two = select_representative_records(records, 2, dataset_source="mit", split="train")
    no_positives = select_representative_records(
        tuple(replace(record, positive=False) for record in records),
        3,
        dataset_source="mit",
        split="train",
    )

    assert [record.positive for record in cap_one.records] == [True]
    assert {record.positive for record in cap_two.records} == {False, True}
    assert no_positives.metadata["selected_positive_count"] == 0
    assert no_positives.metadata["selected_negative_count"] == 3


def test_cap_behavior_and_uncapped_full_dataset_behavior_are_auditable() -> None:
    records = tuple(_record(index, positive=index % 2 == 0) for index in range(5))

    oversized = select_representative_records(records, 99, dataset_source="mit", split="train")
    uncapped = select_representative_records(records, None, dataset_source="mit", split="train")
    empty = select_representative_records((), 3, dataset_source="mit", split="validation")

    assert oversized.records == records
    assert oversized.metadata["requested_cap"] == 99
    assert oversized.metadata["effective_cap"] == 5
    assert oversized.metadata["selection_applied"] is False
    assert uncapped.records == records
    assert uncapped.metadata["requested_cap"] is None
    assert uncapped.metadata["effective_cap"] == 5
    assert empty.records == ()
    assert empty.metadata["effective_cap"] == 0
    assert empty.metadata["selected_count"] == 0
    assert len(str(uncapped.metadata["selected_record_identity_sha256"])) == 64


def test_metadata_identifies_fixed_provider_policy_without_disclosing_record_list() -> None:
    records = tuple(_record(index, positive=index % 2 == 0) for index in range(4))

    result = select_representative_records(records, 2, dataset_source="mit", split="train")

    assert result.metadata["policy_name"] == BOUNDED_SELECTION_POLICY_NAME
    assert result.metadata["policy_version"] == BOUNDED_SELECTION_POLICY_VERSION
    assert result.metadata["seed"] == BOUNDED_SELECTION_POLICY_SEED
    assert result.metadata["record_identities_disclosed"] is False
    assert "records" not in result.metadata
    assert all(record.scene_name not in str(result.metadata) for record in records)
