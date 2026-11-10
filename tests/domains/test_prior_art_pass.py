# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT

"""Regression tests for the targeted prior-art pass."""

from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
COMMON_DIR = ROOT / "skills" / "common"
PROVE_SCRIPT_DIR = ROOT / "skills" / "discovery" / "kb-prove-cycle" / "scripts"
PRIOR_ART_SCRIPT_DIR = ROOT / "skills" / "discovery" / "kb-prior-art-pass" / "scripts"

for path in (COMMON_DIR, PROVE_SCRIPT_DIR, PRIOR_ART_SCRIPT_DIR):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from generate_prior_art_pass_report import _import_references
from generate_prior_art_pass_report import _normalize_reference
from generate_prior_art_pass_report import build_report
from problem_mathlib import default_mathlib
from proof_queue import default_queue
from proof_queue import enqueue_entries
from proof_queue import finalize_queue_entry


def test_prior_art_pass_imports_references_and_builds_obstruction_map(tmp_path: Path) -> None:
    repo_root = tmp_path
    mathlib = default_mathlib(kb_ref="demo")
    queue = default_queue(kb_ref="demo")
    enqueue_entries(
        queue,
        [
            {
                "queue_key": "bridge.001|st.tgt|repair-lemma",
                "title": "Formula-Size Transport Lemma: target",
                "priority": 0.61,
                "bridge_id": "bridge.001",
                "claim_type": "repair-lemma",
                "claim_text": "Formula-size transport lemma.",
                "conjecture_statement": "Formula-size transport lemma.",
                "source_statement_id": "st.src",
                "target_statement_id": "st.tgt",
            }
        ],
    )
    finalize_queue_entry(
        queue,
        queue_id="proofq.demo.001",
        outcome="blocked",
        result_id="",
        attempt_id="attempt.demo.001",
        summary="Missing transport theorem.",
    )

    references = [
        _normalize_reference(
            {
                "reference_type": "theorem",
                "title": "Explicit Hitting Sets Yield Black-Box PIT",
                "statement": "An explicit hitting-set generator yields a deterministic black-box PIT algorithm.",
                "source_name": "Example Paper",
                "source_url": "https://example.org/pit",
                "search_query": "explicit hitting set black box PIT theorem",
                "used_for": "Clarifies the PIT upgrade route.",
                "canonical_citation": "Example Author (2026). Example Paper.",
                "what_changed": "The gap is explicitness, not the abstract hitting-set to PIT implication.",
                "local_search_failure": "Local InformalMathLib and KB lacked an exact theorem for the hitting-set to PIT step.",
                "linked_queue_ids": ["proofq.demo.001"],
                "linked_obstruction_classes": ["pit-upgrade"],
            }
        )
    ]
    imported = _import_references(repo_root=repo_root, kb_ref="demo", mathlib=mathlib, references=references)
    assert len(imported) == 1
    assert mathlib["metadata"]["external_reference_count"] == 1
    assert Path(imported[0]["artifact_path"]).exists()

    report = build_report(
        kb_ref="demo",
        input_payload={"key_findings": ["Imported reference grounds the route."]},
        imported=imported,
        queue=queue,
    )
    assert report["metadata"]["imported_reference_count"] == 1
    assert report["obstruction_map"][0]["name"] == "pit-upgrade"
    assert report["obstruction_map"][0]["queue_ids"] == ["proofq.demo.001"]
    assert report["uncovered_blocked_routes"] == []


def test_prior_art_pass_normalizer_rejects_incomplete_rows() -> None:
    assert _normalize_reference({"reference_type": "note"}) == {}
    assert _normalize_reference({"reference_type": "theorem", "title": "", "statement": "x"}) == {}
