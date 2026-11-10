# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT

"""Regression tests for Lean/Lake-backed bounded discovery search."""

from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
COMMON_DIR = ROOT / "skills" / "common"

if str(COMMON_DIR) not in sys.path:
    sys.path.insert(0, str(COMMON_DIR))

from discovery_calculus import RouteSignature
from lean_discovery import run_lean_search


def test_lean_search_bootstraps_lake_project_and_returns_shapes(tmp_path: Path) -> None:
    route = RouteSignature(
        source_statement_id="st.src",
        target_statement_id="st.tgt",
        source_regime="nonuniform-circuits",
        target_regime="formula-size",
        invariant="MCSP complexity profile",
        candidate_object="MCSP witness family",
        branch_family="equivalence-coherence-reframing",
        source_excerpt="A barely nontrivial lower bound for MCSP in a weak model.",
        target_excerpt="Major lower bounds for NP in a stronger model.",
        multiple_operationalizations=True,
        equivalence_pressure=True,
        factorization_pressure=True,
        negative_pressure=True,
        under_typed_carrier=False,
        barrier_scope="natural proofs",
    )

    payload = run_lean_search(
        tmp_path,
        kb_ref="demo",
        execution_id="discexec.demo.001",
        routes=[
            {
                "queue_id": "proofq.demo.001",
                "bridge_id": "bridge.001",
                "route": route,
            }
        ],
        max_candidates_per_route=5,
    )

    assert payload["available"] is True
    assert payload["build_ok"] is True
    assert Path(payload["module_path"]).exists()
    assert (tmp_path / "lakefile.toml").exists()
    assert (tmp_path / "AbducerFormal" / "Discovery" / "Search.lean").exists()
    assert payload["routes"][0]["search_shapes"] == [
        "realization",
        "transport",
        "equivalence",
        "factorization",
        "obstruction",
    ]
    assert any(row["candidate"]["shape"] == "transport" for row in payload["candidates"])
