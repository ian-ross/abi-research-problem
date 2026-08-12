"""Trusted representative record selection for bounded ABI research runs.

The selector operates only on provider-owned :class:`ABIPatchIndexRecord`
metadata after Dataset Source and Leakage-Safe Split construction.  Candidate
manifests cannot choose this policy or its seed, and audit metadata contains
only aggregate counts and a digest rather than selected record identities.
"""

from __future__ import annotations

import hashlib
import json
from collections import defaultdict
from collections.abc import Sequence
from dataclasses import dataclass

from abi_contrail.datasets import (
    ABIDatasetSource,
    ABIPatchIndexRecord,
    ABISplitName,
)

BOUNDED_SELECTION_POLICY_NAME = "abi_representative_scene_positive_hash"
BOUNDED_SELECTION_POLICY_VERSION = "v1"
BOUNDED_SELECTION_POLICY_SEED = 20260812


@dataclass(frozen=True)
class ABIRecordSelection:
    """Selected records and bounded provider-owned audit metadata."""

    records: tuple[ABIPatchIndexRecord, ...]
    metadata: dict[str, object]


def canonical_record_identity(record: ABIPatchIndexRecord) -> str:
    """Return the canonical trusted identity for one ABI Patch record.

    Positivity is deliberately not an identity component: it is audited as a
    selected-set aggregate and may change if labels are corrected without
    changing which source patch the record addresses.
    """

    return json.dumps(
        [
            record.dataset_source,
            record.split,
            record.scene_name,
            record.scene_index,
            record.goes_time,
            record.sample_index,
            record.row,
            record.col,
        ],
        ensure_ascii=False,
        separators=(",", ":"),
    )


def selected_record_identity_digest(records: Sequence[ABIPatchIndexRecord]) -> str:
    """Digest selected record membership independently of input/output order."""

    digest = hashlib.sha256()
    for identity in sorted(canonical_record_identity(record) for record in records):
        digest.update(identity.encode("utf-8") + b"\n")
    return digest.hexdigest()


def select_representative_records(
    records: Sequence[ABIPatchIndexRecord],
    max_samples: int | None,
    *,
    dataset_source: ABIDatasetSource,
    split: ABISplitName,
) -> ABIRecordSelection:
    """Select a reproducible representative subset within one source and split.

    The effective cap is applied independently to each Dataset Source and
    Leakage-Safe Split.  Capped membership is hash-ranked rather than based on
    record-prefix order.  The selector reserves positive coverage whenever a
    positive record exists, reserves negative coverage when both classes exist
    and the cap is at least two, then spreads each class quota over MIT scenes
    or Google provenance scene names before taking a second record from a
    group.  Full/oversized caps preserve the input record order.
    """

    source_records = tuple(records)
    _validate_boundary(source_records, dataset_source=dataset_source, split=split)
    available_count = len(source_records)
    effective_cap = _effective_cap(available_count, max_samples)

    if effective_cap >= available_count:
        selected = source_records
    else:
        positive_quota = _positive_quota(source_records, effective_cap)
        positive_records = tuple(record for record in source_records if record.positive)
        negative_records = tuple(record for record in source_records if not record.positive)
        selected_positive = _spread_across_groups(
            positive_records,
            positive_quota,
            dataset_source=dataset_source,
            split=split,
            positive=True,
            previously_selected_groups=frozenset(),
        )
        selected_groups = frozenset(record.scene_name for record in selected_positive)
        selected_negative = _spread_across_groups(
            negative_records,
            effective_cap - positive_quota,
            dataset_source=dataset_source,
            split=split,
            positive=False,
            previously_selected_groups=selected_groups,
        )
        selected = tuple(
            sorted(
                selected_positive + selected_negative,
                key=canonical_record_identity,
            )
        )

    available_positive_count = sum(record.positive for record in source_records)
    selected_positive_count = sum(record.positive for record in selected)
    metadata: dict[str, object] = {
        "policy_name": BOUNDED_SELECTION_POLICY_NAME,
        "policy_version": BOUNDED_SELECTION_POLICY_VERSION,
        "seed": BOUNDED_SELECTION_POLICY_SEED,
        "dataset_source": dataset_source,
        "split": split,
        "requested_cap": max_samples,
        "effective_cap": effective_cap,
        "selection_applied": effective_cap < available_count,
        "available_count": available_count,
        "selected_count": len(selected),
        "available_positive_count": available_positive_count,
        "available_negative_count": available_count - available_positive_count,
        "selected_positive_count": selected_positive_count,
        "selected_negative_count": len(selected) - selected_positive_count,
        "coverage_group": (
            "mit_scene_name"
            if dataset_source == "mit"
            else "google_provenance_scene_name"
        ),
        "available_scene_or_provenance_count": len(
            {record.scene_name for record in source_records}
        ),
        "selected_scene_or_provenance_count": len(
            {record.scene_name for record in selected}
        ),
        "selected_record_identity_sha256": selected_record_identity_digest(selected),
        "record_identities_disclosed": False,
    }
    return ABIRecordSelection(records=selected, metadata=metadata)


def _validate_boundary(
    records: Sequence[ABIPatchIndexRecord],
    *,
    dataset_source: ABIDatasetSource,
    split: ABISplitName,
) -> None:
    unexpected_sources = {
        record.dataset_source for record in records if record.dataset_source != dataset_source
    }
    if unexpected_sources:
        raise ValueError(
            "representative record selection cannot cross the Dataset Source boundary: "
            f"expected {dataset_source!r}, found {sorted(unexpected_sources)!r}"
        )
    unexpected_splits = {record.split for record in records if record.split != split}
    if unexpected_splits:
        raise ValueError(
            "representative record selection cannot cross the Leakage-Safe Split boundary: "
            f"expected {split!r}, found {sorted(unexpected_splits)!r}"
        )


def _effective_cap(available_count: int, max_samples: int | None) -> int:
    if max_samples is None:
        return available_count
    if available_count == 0:
        return 0
    return max(1, min(available_count, int(max_samples)))


def _positive_quota(records: Sequence[ABIPatchIndexRecord], cap: int) -> int:
    positive_count = sum(record.positive for record in records)
    negative_count = len(records) - positive_count
    if cap == 0 or positive_count == 0:
        return 0
    if negative_count == 0:
        return cap

    proportional = (cap * positive_count + len(records) // 2) // len(records)
    minimum = max(1, cap - negative_count)
    maximum = min(positive_count, cap)
    if cap >= 2:
        maximum = min(maximum, cap - 1)
    return max(minimum, min(maximum, proportional))


def _spread_across_groups(
    records: Sequence[ABIPatchIndexRecord],
    count: int,
    *,
    dataset_source: ABIDatasetSource,
    split: ABISplitName,
    positive: bool,
    previously_selected_groups: frozenset[str],
) -> tuple[ABIPatchIndexRecord, ...]:
    if count <= 0:
        return ()

    grouped: dict[str, list[ABIPatchIndexRecord]] = defaultdict(list)
    for record in records:
        grouped[record.scene_name].append(record)
    for group_records in grouped.values():
        group_records.sort(
            key=lambda record: _policy_rank(
                "record",
                canonical_record_identity(record),
            )
        )
    group_names = sorted(
        grouped,
        key=lambda group: (
            group in previously_selected_groups,
            _policy_rank(
                "group",
                dataset_source,
                split,
                "positive" if positive else "negative",
                group,
            ),
        ),
    )

    selected: list[ABIPatchIndexRecord] = []
    depth = 0
    while len(selected) < count:
        added = False
        for group in group_names:
            group_records = grouped[group]
            if depth >= len(group_records):
                continue
            selected.append(group_records[depth])
            added = True
            if len(selected) == count:
                break
        if not added:
            break
        depth += 1
    return tuple(selected)


def _policy_rank(*parts: str) -> str:
    payload = "\x1f".join(
        (
            BOUNDED_SELECTION_POLICY_NAME,
            BOUNDED_SELECTION_POLICY_VERSION,
            str(BOUNDED_SELECTION_POLICY_SEED),
            *parts,
        )
    )
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


__all__ = [
    "ABIRecordSelection",
    "BOUNDED_SELECTION_POLICY_NAME",
    "BOUNDED_SELECTION_POLICY_SEED",
    "BOUNDED_SELECTION_POLICY_VERSION",
    "canonical_record_identity",
    "select_representative_records",
    "selected_record_identity_digest",
]
