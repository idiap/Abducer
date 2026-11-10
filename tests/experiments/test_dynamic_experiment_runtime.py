# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Probe triage and import checks independent of retired experiment execution."""

from __future__ import annotations

import subprocess
import sys

from agentic.discovery.contracts import canonical_digest
from agentic.experiments import triage_probe


def _triage(
    *,
    registered_claim_kind: str = "model_consequence",
    registered_target_relation: str = "toy_or_proxy",
    **overrides: object,
) -> dict:
    request = {
        "target_id": "target-pvsnp",
        "theory_programme_id": "theory-programme-1",
        "source_theory_programme_digest": canonical_digest(
            {"programme_id": "theory-programme-1", "obligations": ["O1"]}
        ),
        "source_reflection_packet_digest": canonical_digest(
            {"packet_id": "reflection-1", "rounds": ["R1", "R2"]}
        ),
        "conceptual_system_ids": ["concept-system-a", "concept-system-b"],
        "theoretical_question_id": "question-1",
        "question": "Does the exact finite invariant equal the proposed value?",
        "programme_maturity": "mature",
        "probe_role": "discriminator",
        "decision_effect": {
            "if_supported": "retain the invariant mechanism",
            "if_not_supported": "revise the invariant mechanism",
        },
        "expected_conceptual_change": "choose whether the invariant remains primitive or becomes derived",
        "theory_generated_justification": "reflection isolated this equality as the only remaining discriminator",
        "candidate_methods": [
            "exact",
            "finite_model",
            "numeric",
            "sweep",
            "sympy",
            "lean",
        ],
        "state_version": 7,
    }
    request.update(overrides)
    if "registered_theory_claims" not in overrides:
        claim_core = {
            "claim_id": request["theoretical_question_id"],
            "claim_kind": registered_claim_kind,
            "target_relation": registered_target_relation,
            "statement": request["question"],
            "theory_programme_id": request["theory_programme_id"],
            "conceptual_system_ids": sorted(request["conceptual_system_ids"]),
            "source_theory_programme_digest": request["source_theory_programme_digest"],
            "source_reflection_packet_digest": request[
                "source_reflection_packet_digest"
            ],
        }
        request["registered_theory_claims"] = (
            [{**claim_core, "claim_digest": canonical_digest(claim_core)}]
            if all(claim_core.values())
            else []
        )
    return triage_probe(request)


def test_triage_refuses_easy_but_theoretically_inert_probe() -> None:
    triage = _triage(
        expected_conceptual_change="",
        decision_effect={"if_supported": "same", "if_not_supported": "same"},
    )
    assert triage["decision"] == "no_probe_needed"


def test_triage_refuses_immature_or_unbound_question() -> None:
    triage = _triage(programme_maturity="incubating", theoretical_question_id=None)
    assert triage["decision"] == "immature_question"


def test_triage_refuses_reusable_ids_without_exact_theory_bytes() -> None:
    triage = _triage(
        source_theory_programme_digest=None,
        source_reflection_packet_digest=None,
    )
    assert triage["decision"] == "immature_question"


def test_experiment_package_imports_first_in_a_fresh_interpreter() -> None:
    completed = subprocess.run(
        [
            sys.executable,
            "-c",
            (
                "from agentic.experiments import execute_experiment; "
                "import agentic.discovery as discovery; "
                "assert callable(execute_experiment); "
                "assert callable(discovery.run_canonical_discovery_cycle)"
            ),
        ],
        check=False,
        capture_output=True,
        text=True,
    )
    assert completed.returncode == 0, completed.stderr
