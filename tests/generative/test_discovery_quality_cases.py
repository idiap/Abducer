# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Execute blinded adversarial cases and persist machine-checkable receipts."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from agentic.discovery.contracts import adjudicate_quality_case, canonical_digest


CASES_PATH = Path(__file__).with_name("discovery_quality_cases.jsonl")


def _records() -> list[dict]:
    return [json.loads(line) for line in CASES_PATH.read_text(encoding="utf-8").splitlines() if line.strip()]


def _cases() -> list[dict]:
    """Flatten blinded cases nested beside the existing evaluation mutations."""

    return [case for record in _records() for case in record.get("blinded_cases", [])]


@pytest.mark.generative
@pytest.mark.parametrize("case", _cases(), ids=lambda case: case["case_id"])
def test_blinded_quality_case_matches_versioned_adjudication(case: dict, tmp_path: Path) -> None:
    # Expected fields are deliberately withheld from the evaluator.
    blinded = {key: case[key] for key in ("case_id", "category", "case_payload")}
    receipt = adjudicate_quality_case(blinded)
    assert receipt["decision"] == case["expected"]["decision"]
    assert receipt["reason_codes"] == case["expected"]["reason_codes"]
    assert receipt["case_digest"] == canonical_digest(case["case_payload"])
    receipt_path = tmp_path / f"{case['case_id']}.receipt.json"
    receipt_path.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    persisted = json.loads(receipt_path.read_text(encoding="utf-8"))
    assert persisted["adjudication_digest"] == receipt["adjudication_digest"]
    assert persisted["adjudication_receipt_id"] == receipt["adjudication_receipt_id"]


def test_case_corpus_covers_required_operational_and_conceptual_regressions() -> None:
    assert all(record["fixture_version"] == "1.0.0" for record in _records())
    categories = {case["category"] for case in _cases()}
    assert {
        "philosophical_vapour",
        "unification_by_erasure",
        "relevance_drift",
        "premature_convergence",
        "false_breakthrough",
        "proxy_drift",
        "stale_evidence",
        "fabricated_certificate",
        "wrong_target_global_latest",
        "structurally_duplicate_branches",
        "correlated_parallel_branches",
        "literature_supersession",
        "partial_worker_failure",
        "paraphrase_loop",
        "pseudo_radical_hypothesis",
        "shallow_cycle",
    } <= categories
