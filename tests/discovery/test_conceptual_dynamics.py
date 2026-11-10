# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT

"""
Regression tests for conceptual dynamics monitoring.

Concept: Verifies that the dashboard tracks conceptual objects, hypothesis lifecycles, and surfaced taxonomy overlays.
Contribution: Prevents regressions that would flatten the discovery process back into purely syntactic artifact counting.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[2]
ORCH_SCRIPTS = ROOT / "skills" / "orchestration" / "kb-orchestrator" / "scripts"
if str(ORCH_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(ORCH_SCRIPTS))

from generate_conceptual_dynamics import _build_conceptual_dynamics, _render_html
from generate_reasoning_surface_index import _load_surfaces


def _write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def _write_surface(
    path: Path,
    *,
    agent: str,
    run_id: str,
    kb_ref: str,
    artifacts_dir: Path,
    stage: str,
    title: str,
    taxonomy: dict,
    metrics: dict,
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "agent": agent,
        "run_id": run_id,
        "started_utc": "2026-03-14T10:00:00+00:00",
        "ended_utc": "2026-03-14T10:00:02+00:00",
        "duration_s": 0.2,
        "status": "success",
        "summary": "surface ok",
        "internal_log_path": str(path.with_suffix(".md")),
        "surface_markdown_path": str(path.with_suffix(".surface.md")),
        "surface_json_path": str(path),
        "context": {
            "kb": f"KB/{kb_ref}.kb.md",
            "kb_ref": kb_ref,
            "artifacts_dir": str(artifacts_dir),
        },
        "outputs": [],
        "moments": [
            {
                "timestamp": "2026-03-14T10:00:01+00:00",
                "kind": "conceptual_move",
                "title": title,
                "focus": stage,
                "significance": "surfaces a prompt-level conceptual shift",
                "details": ["generated via IDE-based generative reasoning"],
                "tags": ["conceptual", "prompt"],
                "stage": stage,
                "taxonomy": taxonomy,
                "metrics": metrics,
            }
        ],
    }
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def test_conceptual_dynamics_tracks_lifecycle_and_surface_taxonomy(tmp_path: Path) -> None:
    """
    Concept: Validates that conceptual dynamics integrates artifact lifecycles with surfaced conceptual taxonomy.
    Contribution: Keeps the dashboard aligned with both deterministic stage outputs and prompt-driven conceptual annotations.
    """

    repo_root = tmp_path
    artifacts_dir = repo_root / "artifacts" / "alpha-kb"
    surface_root = repo_root / "artifacts" / "reasoning-surfaces"
    phyp_dir = repo_root / "phyp"
    artifacts_dir.mkdir(parents=True, exist_ok=True)
    phyp_dir.mkdir(parents=True, exist_ok=True)

    (phyp_dir / "alpha-kb.proof-hypotheses.yaml").write_text(
        yaml.safe_dump(
            {
                "metadata": {},
                "hypotheses": [
                    {"id": "hyp.1", "kind": "bridge-link", "status": "tentative", "priority": 0.8, "title": "Construct bridge"},
                    {"id": "hyp.2", "kind": "definition-introduction", "status": "tentative", "priority": 0.6, "title": "Refine definition"},
                ],
            },
            sort_keys=False,
        ),
        encoding="utf-8",
    )

    _write_json(
        artifacts_dir / "connection-analysis.json",
        {
            "stats": {"statement_count": 2, "edge_count": 1},
            "top_interventions": [
                {
                    "concept_focus": ["positivity"],
                    "concept_profile": {"consequence_signatures": ["representation-target"]},
                }
            ],
            "connection_candidates": [],
        },
    )
    _write_json(
        artifacts_dir / "bridge-plan.json",
        {
            "bridge_programs": [
                {
                    "bridge_id": "bridge.1",
                    "from_id": "hyp.1",
                    "to_id": "hyp.2",
                    "bridge_type": "measure-representation",
                    "bridge_score": 0.84,
                    "evidence_terms": ["positive functional"],
                    "inferential_commitment": {
                        "support_antecedent_schema": "positive-functional",
                        "target_consequence_schema": "representation-target",
                        "preserved_invariant": "regularity",
                    },
                    "statement_delta": {
                        "source_problem_family": "functional analysis",
                        "target_problem_family": "measure representation",
                        "source_model": "positive linear functional",
                        "target_model": "regular Borel measure",
                        "source_claim_focus": "positive-functional",
                        "target_claim_focus": "representation-target",
                        "model_shift": "functional -> measure",
                        "threshold_shift": "existence -> representation theorem",
                        "consequence_shift": "upgrade `positive-functional` into `representation-target`",
                        "typed_object_expectation": "representing measure",
                        "typing_status": "typed",
                        "missing_witness_or_transport": "Show that positivity and regularity force a representing measure.",
                        "route_synopsis": "Move from a positive functional on the source side to a regular Borel measure that represents it on the target side.",
                        "source_theorem_excerpt": "Every positive functional on the test algebra should induce a measure candidate.",
                        "target_theorem_excerpt": "There exists a unique regular Borel measure representing the functional.",
                    },
                    "mathematical_program": {
                        "bridge_question": "Which regular Borel measure packages the positivity data into an actual representation theorem?",
                        "theorem_template": "If the source functional induces a regular Borel measure preserving regularity, then the representation target follows.",
                        "source_assumption": "Assume the functional is positive on the relevant algebra.",
                        "target_payoff": "Derive the representing measure conclusion.",
                        "invariant_transport": "Track regularity while passing from the functional to the measure object.",
                        "inspection_checklist": [
                            "Construct the candidate measure from the positive functional.",
                            "Prove regularity of the constructed measure.",
                            "Verify that integration against the measure recovers the original functional.",
                        ],
                        "obstruction_pressure": "The route fails if positivity does not control regularity strongly enough.",
                    },
                }
            ],
            "recommended_run_order": ["bridge.1"],
        },
    )
    _write_json(
        artifacts_dir / "concept-gap-abstractions.json",
        {
            "gap_clusters": [
                {
                    "gap_axes": [{"axis": "regularity gap"}],
                    "recommended_abstraction_families": ["measure reconstruction"],
                }
            ],
            "abstraction_conjectures": [
                {
                    "conjecture_id": "conj.1",
                    "bridge_id": "bridge.1",
                    "abstraction_type": "measure-representation",
                    "abstraction_label": "representing measure",
                    "target_consequence_schema": "representation-target",
                    "support_antecedent_schema": "positive-functional",
                    "preserved_invariant": "regularity",
                    "mathematical_object_role": "measure object",
                    "priority": 0.9,
                    "carrier_kind": "regular Borel measure",
                    "typing_status": "typed",
                    "statement_delta": {
                        "source_problem_family": "functional analysis",
                        "target_problem_family": "measure representation",
                        "source_model": "positive linear functional",
                        "target_model": "regular Borel measure",
                        "source_claim_focus": "positive-functional",
                        "target_claim_focus": "representation-target",
                        "model_shift": "functional -> measure",
                        "threshold_shift": "existence -> uniqueness",
                        "consequence_shift": "upgrade `positive-functional` into `representation-target`",
                        "typed_object_expectation": "representing measure",
                        "typing_status": "typed",
                        "missing_witness_or_transport": "Prove that the representing measure preserves regularity and reconstructs the functional.",
                        "route_synopsis": "Turn positivity data into a typed measure object with enough regularity to recover the target theorem.",
                        "source_theorem_excerpt": "Positive functionals should generate finitely additive content before regularization.",
                        "target_theorem_excerpt": "A regular Borel measure represents the functional and is unique.",
                    },
                    "mathematical_specification": {
                        "statement_delta": {
                            "source_problem_family": "functional analysis",
                            "target_problem_family": "measure representation",
                            "source_model": "positive linear functional",
                            "target_model": "regular Borel measure",
                            "source_claim_focus": "positive-functional",
                            "target_claim_focus": "representation-target",
                            "model_shift": "functional -> measure",
                            "threshold_shift": "existence -> uniqueness",
                            "consequence_shift": "upgrade `positive-functional` into `representation-target`",
                            "typed_object_expectation": "representing measure",
                            "typing_status": "typed",
                            "missing_witness_or_transport": "Prove that the representing measure preserves regularity and reconstructs the functional.",
                            "route_synopsis": "Turn positivity data into a typed measure object with enough regularity to recover the target theorem.",
                            "source_theorem_excerpt": "Positive functionals should generate finitely additive content before regularization.",
                            "target_theorem_excerpt": "A regular Borel measure represents the functional and is unique.",
                        },
                        "carrier_kind": "regular Borel measure",
                        "typing_status": "typed",
                        "definition_template": "A representing measure is a regular Borel measure whose integrals recover the original functional.",
                        "assumptions": [
                            "The functional is positive on nonnegative test functions.",
                            "The measure candidate is countably additive and regular.",
                        ],
                        "conditional_claim": "If a regular Borel measure realizes the positivity data, the representation target follows.",
                        "proof_obligation_templates": [
                            "Construct the measure from positivity data.",
                            "Show regularity and uniqueness of the measure.",
                        ],
                        "obstruction_template": "The conjecture fails if the candidate object does not preserve regularity.",
                        "inspection_focus": [
                            "Locate the step where positivity becomes countable additivity.",
                            "Track how regularity is certified in the construction.",
                        ],
                    },
                    "counterfactual_probes": [
                        {
                            "intervention": "Drop regularity from the candidate measure.",
                            "expected_bridge_effect": "bridge-degrades-or-fails",
                        }
                    ],
                }
            ],
            "recommended_run_order": ["conj.1"],
        },
    )
    _write_json(
        artifacts_dir / "proof-strategies.json",
        {
            "strategies": [
                {
                    "strategy_id": "strat.1",
                    "name": "Construct the measure",
                    "phase": "constructive",
                    "strategy_score": 0.82,
                    "concept_fertility": 0.6,
                    "anchor_concepts": ["positivity"],
                    "abstraction_concepts": ["representing measure"],
                    "bridge_ids": ["bridge.1"],
                    "hypothesis_ids": ["hyp.1"],
                }
            ]
        },
    )
    _write_json(
        artifacts_dir / "proof-sketches.json",
        {
            "proof_sketches": [
                {
                    "sketch_id": "sk.1",
                    "title": "Recover representing measure",
                    "proof_strategy_family": "measure-construction-from-positive-functional",
                    "sketch_score": 0.77,
                    "conjectured_object": "representing measure",
                    "target_consequence_schema": "representation-target",
                    "support_antecedent_schema": "positive-functional",
                    "preserved_invariant": "regularity",
                    "definitional_commitments": ["regular Borel measure"],
                    "proof_obligations": [{"requirement": "show uniqueness"}],
                    "candidate_lemmas": [{"statement": "positivity implies boundedness"}],
                    "proof_outline_steps": [
                        {"objective": "Construct the measure from positive linear data."},
                        {"objective": "Show the measure is regular and unique."},
                    ],
                    "conjecture_id": "conj.1",
                    "strategy_id": "strat.1",
                    "bridge_id": "bridge.1",
                    "statement_delta": {
                        "source_problem_family": "functional analysis",
                        "target_problem_family": "measure representation",
                        "source_model": "positive linear functional",
                        "target_model": "regular Borel measure",
                        "source_claim_focus": "positive-functional",
                        "target_claim_focus": "representation-target",
                        "model_shift": "functional -> measure",
                        "threshold_shift": "existence -> uniqueness",
                        "consequence_shift": "upgrade `positive-functional` into `representation-target`",
                        "typed_object_expectation": "representing measure",
                        "typing_status": "typed",
                        "missing_witness_or_transport": "Show that positivity and regularity yield a unique representing measure.",
                        "route_synopsis": "Promote positivity into a measure object and then discharge uniqueness and representation.",
                        "source_theorem_excerpt": "A positive functional should admit a measure witness if boundedness and positivity align.",
                        "target_theorem_excerpt": "A unique regular Borel measure represents the functional.",
                    },
                    "mathematical_argument": {
                        "bridge_definition": "Treat the representing measure as the typed object that transports positivity into the representation theorem.",
                        "assumptions": [
                            "The source functional is positive and bounded on the test algebra.",
                            "The candidate measure is regular on compact-open approximations.",
                        ],
                        "proposition": "If the representing measure exists with the required regularity, the representation target follows.",
                        "statement_delta": {
                            "source_problem_family": "functional analysis",
                            "target_problem_family": "measure representation",
                            "source_model": "positive linear functional",
                            "target_model": "regular Borel measure",
                            "source_claim_focus": "positive-functional",
                            "target_claim_focus": "representation-target",
                            "model_shift": "functional -> measure",
                            "threshold_shift": "existence -> uniqueness",
                            "consequence_shift": "upgrade `positive-functional` into `representation-target`",
                            "typed_object_expectation": "representing measure",
                            "typing_status": "typed",
                            "missing_witness_or_transport": "Show that positivity and regularity yield a unique representing measure.",
                            "route_synopsis": "Promote positivity into a measure object and then discharge uniqueness and representation.",
                            "source_theorem_excerpt": "A positive functional should admit a measure witness if boundedness and positivity align.",
                            "target_theorem_excerpt": "A unique regular Borel measure represents the functional.",
                        },
                        "source_theorem_excerpt": "A positive functional should admit a measure witness if boundedness and positivity align.",
                        "target_theorem_excerpt": "A unique regular Borel measure represents the functional.",
                        "lemma_chain": [
                            "Source-to-object lemma: positivity yields a measure candidate.",
                            "Regularity lemma: compact-open approximation upgrades the candidate to a regular measure.",
                            "Payoff lemma: integration against the measure recovers the original functional.",
                        ],
                        "failure_mode": "The route fails if regularity cannot be preserved while constructing the measure.",
                        "inspection_points": [
                            "Identify where boundedness is used to control total mass.",
                            "Identify where regularity is first required.",
                        ],
                    },
                    "counterfactual_test": {
                        "intervention": "Allow the measure candidate to lose regularity.",
                        "expected_bridge_effect": "bridge-degrades-or-fails",
                    },
                }
            ]
        },
    )
    _write_json(
        artifacts_dir / "hypothesis-evaluation.json",
        {
            "summary": {
                "verdict_counts": {"supported": 1, "inconclusive": 1},
                "next_status_counts": {"supported": 1, "needs-testing": 1},
            },
            "results": [
                {
                    "hypothesis_id": "hyp.1",
                    "kind": "bridge-link",
                    "priority": 0.8,
                    "confidence": 0.7,
                    "verdict": "supported",
                    "next_status": "supported",
                    "recommended_action": "promote",
                    "inferential_commitment": {
                        "support_antecedent_schema": "positive-functional",
                        "target_consequence_schema": "representation-target",
                        "preserved_invariant": "regularity",
                        "barrier_scope": "none",
                    },
                },
                {
                    "hypothesis_id": "hyp.2",
                    "kind": "definition-introduction",
                    "priority": 0.6,
                    "confidence": 0.4,
                    "verdict": "inconclusive",
                    "next_status": "needs-testing",
                    "recommended_action": "refine",
                    "inferential_commitment": {
                        "support_antecedent_schema": "positive-functional",
                        "target_consequence_schema": "representation-target",
                        "preserved_invariant": "regularity",
                        "barrier_scope": "none",
                    },
                },
            ],
        },
    )
    _write_json(
        artifacts_dir / "hypothesis-refutation-loop.json",
        {
            "rounds": [{"round": 1, "verdict_counts": {"supported": 1, "inconclusive": 1}}],
            "final_summary": {
                "supported_count": 1,
                "refuted_count": 0,
                "provisionally_supported_count": 0,
                "provisionally_refuted_count": 0,
                "unresolved_count": 1,
                "open_count": 1,
                "supported_ids": ["hyp.1"],
                "refuted_ids": [],
                "provisionally_supported_ids": [],
                "provisionally_refuted_ids": [],
                "unresolved_ids": ["hyp.2"],
            },
            "promotion_candidates": [{"hypothesis_id": "hyp.2", "priority": 0.6}],
            "belief_revision_actions": [{"hypothesis_id": "hyp.2", "action": "refine definition"}],
        },
    )
    _write_json(
        artifacts_dir / "revision-loop.json",
        {
            "revision_summary": {
                "revision_count": 1,
                "unresolved_hypotheses": 1,
                "provisionally_refuted_hypotheses": 0,
                "low_coherence_hypotheses": 0,
                "conceptual_unresolved_hypotheses": 1,
            },
            "priority_program": [{"revision_id": "rev.1"}],
            "revision_actions": [
                {
                    "revision_id": "rev.1",
                    "revision_type": "concept-splitting",
                    "trigger": "unresolved cluster",
                    "action": "split the overloaded bridge concept",
                    "success_criteria": "smaller unresolved cluster",
                }
            ],
            "executable_revision": {
                "generated_hypothesis_ids": ["hyp.3"],
                "operator_counts": {"generated_statements": 1},
            },
        },
    )

    _write_surface(
        surface_root / "kb-gap-abstraction-conjecturer" / "a.json",
        agent="kb-gap-abstraction-conjecturer",
        run_id="run-1",
        kb_ref="alpha-kb",
        artifacts_dir=artifacts_dir,
        stage="conjecture",
        title="Introduce a transport object",
        taxonomy={
            "target_concepts": ["regular representation"],
            "hypotheses": [
                {
                    "id": "hyp.extra.1",
                    "label": "Probe impossibility of irregular witnesses",
                    "kind": "barrier-link",
                    "state": "tentative",
                    "generated": True,
                    "prioritized": True,
                }
            ],
            "reasoning_types": ["negative-obstruction-probe"],
        },
        metrics={"generative_target_concepts": 1},
    )
    _write_surface(
        surface_root / "kb-proof-sketcher" / "b.json",
        agent="kb-proof-sketcher",
        run_id="run-1",
        kb_ref="alpha-kb",
        artifacts_dir=artifacts_dir,
        stage="proof-sketch",
        title="Commit to a duality route",
        taxonomy={"proof_strategy_families": ["duality-construction"]},
        metrics={"formalization_pressure": 2},
    )

    surfaces = _load_surfaces(
        surface_root,
        repo_root=repo_root,
        artifacts_dir=artifacts_dir,
        kb_ref_filter="alpha-kb",
        run_id="run-1",
    )
    report = _build_conceptual_dynamics(
        repo_root=repo_root,
        artifacts_dir=artifacts_dir,
        surfaces=surfaces,
        kb="KB/alpha-kb.kb.md",
        kb_ref="alpha-kb",
        selected_run_id="run-1",
        selection_reason="explicit-run-id",
    )

    current = report["summary"]["current"]
    assert report["summary"]["surface_count"] == 2
    assert report["summary"]["surface_moment_count"] == 2
    assert current["hypothesis_count"] == 4
    assert current["target_concept_count"] >= 2
    assert current["lifecycle_totals"]["formalized"] >= 1
    assert current["lifecycle_totals"]["supported"] >= 1
    assert current["reasoning_type_counts"]["negative-obstruction-probe"] == 1
    assert current["proof_strategy_family_counts"]["duality-construction"] == 1
    assert any(row["label"] == "regularity" for row in current["highlights"]["leading_invariants"])

    stages = {row["stage"]: row for row in report["timeline"]}
    assert stages["conjecture"]["surface"]["moment_count"] == 1
    assert stages["proof-sketch"]["metrics"]["formalization_pressure"] == 2
    assert stages["revision-loop"]["state"]["lifecycle_totals"]["revised"] >= 1
    assert any(row["label"] == "representing measure" for row in stages["conjecture"]["state"]["highlights"]["introduced_bridge_objects"])
    assert stages["proof-sketch"]["state"]["highlights"]["stage_proof_sketches"][0]["id"] == "sk.1"
    primary = stages["proof-sketch"]["state"]["highlights"]["primary_dossier"]
    assert primary["id"] == "sk.1"
    assert primary["content"]["source_excerpt"].startswith("A positive functional should admit")
    assert primary["content"]["target_excerpt"].startswith("A unique regular Borel measure")
    assert primary["content"]["statement_delta"]["model_shift"] == "functional -> measure"
    assert primary["content"]["obligations"][0] == "show uniqueness"
    assert any("positivity yields a measure candidate" in row for row in primary["content"]["lemmas"])
    assert primary["content"]["failure_diagnosis"].startswith("The route fails")

    html = _render_html(report)
    assert "Primary Mathematical Dossier" in html
    assert "Mathematical delta" in html
    assert "Counterfactual probe" in html
    assert "A positive functional should admit a measure witness" in html
