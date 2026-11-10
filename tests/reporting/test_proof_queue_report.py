# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT

"""Regression tests for proof-queue LaTeX report generation."""

from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPT_DIR = ROOT / "skills" / "discovery" / "kb-prove-cycle" / "scripts"
COMMON_DIR = ROOT / "skills" / "common"
for path in (SCRIPT_DIR, COMMON_DIR):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from generate_proof_queue_report import build_report, render_tex


def test_proof_queue_report_renders_current_queue_state() -> None:
    queue = {
        "metadata": {
            "kb_ref": "demo-kb",
            "queue_version": 2,
            "updated_utc": "2026-03-17T00:00:00+00:00",
            "pending_count": 1,
            "in_progress_count": 1,
            "completed_count": 1,
        },
        "entries": [
            {
                "queue_id": "proofq.demo.001",
                "status": "pending",
                "priority": 0.91,
                "bridge_id": "bridge.001",
                "source_statement_id": "st.src",
                "target_statement_id": "st.tgt",
                "candidate_object": "Witness family",
                "carrier_kind": "family of instances equipped with a witness measure",
                "preserved_invariant": "witness complexity profile",
                "conjecture_statement": "There exists an admissible Witness family such that the source lower bound yields the target separation.",
                "missing_route_lemma": "Show the witness family transports the lower bound.",
                "route_synopsis": "Move from st.src to st.tgt through the witness family.",
                "source_excerpt": "Source theorem excerpt.",
                "target_excerpt": "Target theorem excerpt.",
                "proof_obligations": ["Build the witness family."],
                "candidate_lemmas": ["Source-to-object lemma."],
            },
            {
                "queue_id": "proofq.demo.002",
                "status": "in_progress",
                "priority": 0.88,
                "bridge_id": "bridge.002",
                "source_statement_id": "st.src.2",
                "target_statement_id": "st.tgt.2",
                "candidate_object": "Second carrier",
                "carrier_kind": "transfer map",
                "preserved_invariant": "alignment invariant",
                "conjecture_statement": "There exists an admissible transfer map for the second route.",
                "missing_route_lemma": "Show the transfer map preserves the invariant.",
                "route_synopsis": "Move from st.src.2 to st.tgt.2.",
                "source_excerpt": "Second source excerpt.",
                "target_excerpt": "Second target excerpt.",
                "attempt_ids": ["attempt.demo.001"],
            },
            {
                "queue_id": "proofq.demo.003",
                "status": "proved",
                "priority": 0.51,
                "bridge_id": "bridge.003",
                "source_statement_id": "st.src.3",
                "target_statement_id": "st.tgt.3",
                "candidate_object": "Resolved carrier",
                "carrier_kind": "certificate family",
                "preserved_invariant": "certificate complexity",
                "conjecture_statement": "The resolved carrier yields the third target.",
                "missing_route_lemma": "Show the certificate family closes the route.",
                "route_synopsis": "Move from st.src.3 to st.tgt.3.",
                "source_excerpt": "Third source excerpt.",
                "target_excerpt": "Third target excerpt.",
                "resolution_summary": "Informal proof completed.",
            },
        ],
    }

    report = build_report(queue=queue, kb_ref="demo-kb")
    assert report["metadata"]["entry_count"] == 3
    assert len(report["by_status"]["pending"]) == 1
    assert len(report["by_status"]["in_progress"]) == 1
    assert len(report["by_status"]["proved"]) == 1

    tex = render_tex(report)
    assert "Proof Queue Report for" in tex
    assert "\\section{Queue Snapshot}" in tex
    assert "\\section{In Progress}" in tex
    assert "\\section{Pending}" in tex
    assert "\\section{Proved}" in tex
    assert "There exists an admissible Witness family" in tex
    assert "Show the witness family transports the lower bound." in tex
