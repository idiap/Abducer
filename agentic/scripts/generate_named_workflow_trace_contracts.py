#!/usr/bin/env python3
# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Generate explicit public-trace requirements for named workflow steps.

The source registry remains the execution authority.  This projection declares
what an expert must be able to inspect for every step, including conditional and
validator-only steps.  It describes public, artifact-grounded inference summaries
and never requests hidden chain-of-thought.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "agentic/registries/named_workflow_contracts.yaml"
OUTPUT = ROOT / "agentic/registries/named_workflow_trace_contracts.yaml"


WORKFLOW_SEMANTICS: dict[str, dict[str, Any]] = {
    "evidence_to_proof_route_onramp": {
        "expert_question": "How did source-bound evidence become a ranked, adversarially tested proof route?",
        "trace_spine": ["provenance", "normalization", "grounding", "connection", "bias_correction", "ranking", "regime_audit", "falsification", "handoff"],
        "contrast": "Expose the promoted route beside a demoted alternative and the evidence, bias correction, regime issue, or falsifier that separates them.",
        "authority": "May recommend an evidence-bound route; may not assert a theorem or erase provenance and assertion-license limits.",
    },
    "conceptual_frontier_deepening": {
        "expert_question": "Which conceptual transformation improved the frozen frontier, and why did blind adjudication prefer it?",
        "trace_spine": ["frozen_context", "literature_delta", "invention", "branch_lineage", "reflection_delta", "synthesis", "blind_adjudication", "equivalence", "formal_readiness"],
        "contrast": "Retain a rejected alternative with the adjudication criterion; conceal candidate identity during blind selection and disclose it only afterward.",
        "authority": "May propose and rank theories under frozen context; experiments constrain but never select a conceptual theory, and no proof is certified.",
    },
    "theorem_proof_delivery": {
        "expert_question": "How does the exact scoped theorem reduce to obligations and a lemma DAG, and where is the residual gap?",
        "trace_spine": ["statement_binding", "obligation_derivation", "lemma_dag", "gap_or_countermodel", "domain_audit", "proof_gate"],
        "contrast": "Expose failed lemmas, circularity, model mismatch, or countermodels beside the surviving chain and exact residual obligation.",
        "authority": "May validate only the exact bound statement after the proof gate; may not silently close gaps or widen quantifiers, model, or regime.",
    },
    "scientific_contribution_cultivation": {
        "expert_question": "What is the smallest honest contribution supported by the result delta, and what does it enable?",
        "trace_spine": ["atlas_delta", "subgoal_enablement", "contribution_class", "value_evidence", "target_alignment", "enablement_counterfactual", "handoff"],
        "contrast": "Contrast target-critical novelty with local, supporting, prior-art-covered, or non-enabling interpretations.",
        "authority": "May classify and package supported contribution candidates; may not inflate novelty, target alignment, or paper readiness.",
    },
    "manuscript_result_elaboration": {
        "expert_question": "How did bounded result packets change the manuscript while preserving theorem scope and prior-art limits?",
        "trace_spine": ["marker_inventory", "bounded_plan", "candidate_delta", "self_critique", "scope_boundary", "proof_packet", "prior_art", "manuscript_diff", "readiness"],
        "contrast": "Show rejected revisions and unresolved markers, with finite, asymptotic, and continuum claims kept explicitly distinct.",
        "authority": "May elaborate and integrate supported manuscript claims; may not perform implicit discovery, erase disqualifiers, or promote finite evidence to continuum scope.",
    },
    "deep_review_and_reorientation": {
        "expert_question": "What did independent reviewers agree and disagree about, and how did that evidence govern the repair route?",
        "trace_spine": ["immutable_snapshot", "framework_state", "independent_lenses", "findings", "agreements_disagreements", "meta_synthesis", "understanding_delta", "repair_queue"],
        "contrast": "Retain minority findings and unresolved disagreement rather than averaging them away in the meta-review.",
        "authority": "May diagnose and route repairs; has no authority to prove claims, release artifacts, or perform epistemic upgrades.",
    },
}


PROFILE_SEMANTICS = {
    "route_a": {
        "trace_spine": ["profile_activation", "open_point_plan", "specialist_fan_out", "symbolic_audit", "finite_scope", "specialist_join", "integration_delta", "validation_tail"],
        "contrast": "Expose failed identities, endpoints, same-theory bindings, margins, and the explicit bar against finite-to-continuum promotion.",
        "authority": "May integrate a bounded Route-A result into the parent manuscript workflow; may not promote a finite packet past the common validation tail.",
    }
}


def _event_family(step_id: str, mode: str) -> str:
    if mode == "validator_only" or any(token in step_id for token in ("audit", "gate", "check", "certif")):
        return "validation"
    if any(token in step_id for token in ("handoff", "integrate", "package")):
        return "handoff"
    if any(token in step_id for token in ("review", "reflect", "adjudicate", "meta")):
        return "adjudication"
    if any(token in step_id for token in ("hunt", "counter", "gap", "split", "fals")):
        return "falsification"
    if any(token in step_id for token in ("plan", "orchestrate", "manage")):
        return "planning"
    return "transformation"


def _operator(step_id: str, skill: str) -> str:
    text = f"{step_id} {skill}"
    rules = (
        (("ingest", "parse", "normalize"), "normalize_with_provenance"),
        (("ground",), "ground_claim_to_target"),
        (("connect", "pathfind", "entrypoint"), "construct_and_rank_route"),
        (("bias",), "compare_pre_post_bias_correction"),
        (("counter", "fals", "gap"), "adversarially_test_or_split"),
        (("literature",), "assimilate_prior_evidence"),
        (("portfolio", "parallel", "forge", "invention"), "generate_independent_alternatives"),
        (("reflect", "synthesize"), "revise_and_synthesize"),
        (("adjudicate",), "blind_multi_criterion_compare"),
        (("equivalence",), "test_semantic_equivalence"),
        (("formalize", "obligation"), "derive_formal_obligations"),
        (("lemma",), "compose_lemma_dependency"),
        (("proof", "gate"), "validate_exact_claim_boundary"),
        (("atlas",), "compute_result_atlas_delta"),
        (("contribution", "value"), "classify_and_assess_contribution"),
        (("alignment",), "audit_main_target_alignment"),
        (("enablement",), "evaluate_counterfactual_enablement"),
        (("scope",), "bind_claim_scope"),
        (("prior",), "test_prior_art_disqualifiers"),
        (("review", "meta"), "evidence_bound_review_synthesis"),
        (("integrate", "insert", "draft"), "apply_traceable_artifact_delta"),
        (("cas", "symbolic"), "verify_symbolic_identity"),
        (("endpoint", "margin", "collar", "factor"), "verify_bounded_specialist_obligation"),
    )
    for tokens, operator in rules:
        if any(token in text for token in tokens):
            return operator
    return "artifact_grounded_transformation"


def _disposition(mode: str, *, specialist: bool = False) -> str:
    if specialist:
        return "specialist_event_required"
    if mode == "conditional":
        return "conditional_event_or_justified_na"
    if mode == "validator_only":
        return "validator_event_required"
    return "semantic_event_required"


def _requirement(step: dict[str, Any], semantics: dict[str, Any], *, specialist: bool = False) -> dict[str, Any]:
    mode = "specialist" if specialist else str(step["mode"])
    return {
        "step_id": str(step["id"]),
        "skill": str(step["skill"]),
        "mode": mode,
        "disposition": _disposition(mode, specialist=specialist),
        "event_family": _event_family(str(step["id"]), mode),
        "inference_operator": _operator(str(step["id"]), str(step["skill"])),
        "required_fields": [
            "public_inference.question", "public_inference.premises", "public_inference.warrant",
            "public_inference.conclusion", "public_inference.scope", "evidence", "authority",
        ],
        "evidence_roles": ["supports", "constrains", "refutes"],
        "required_contrast": str(semantics["contrast"]),
        "authority_boundary": str(semantics["authority"]),
        "consumes": list(step.get("consumes", [])),
        "produces": list(step.get("produces", [])),
        "when": step.get("when"),
    }


def build_contracts(source: dict[str, Any]) -> dict[str, Any]:
    workflows = []
    for workflow in source["workflows"]:
        semantics = WORKFLOW_SEMANTICS[workflow["id"]]
        profiles = []
        for profile in workflow.get("profiles", []):
            profile_semantics = PROFILE_SEMANTICS[profile["id"]]
            specialists = [
                _requirement(
                    {"id": skill.replace("-", "_"), "skill": skill, "mode": "required", "consumes": [], "produces": [profile["specialist_output"]], "when": None},
                    profile_semantics,
                    specialist=True,
                )
                for skill in profile.get("specialist_skills", [])
            ]
            profiles.append({
                "id": profile["id"],
                "version": profile["version"],
                "trace_spine": profile_semantics["trace_spine"],
                "steps": [_requirement(step, profile_semantics) for step in profile["steps"]],
                "specialists": specialists,
                "validation_tail_start": profile.get("validation_tail_start"),
                "validation_tail_adapter": profile.get("validation_tail_adapter"),
            })
        workflows.append({
            "id": workflow["id"],
            "version": workflow["version"],
            "trace_spine": semantics["trace_spine"],
            "expert_question": semantics["expert_question"],
            "steps": [_requirement(step, semantics) for step in workflow["steps"]],
            "profiles": profiles,
        })
    return {"version": 1, "source_registry": str(SOURCE.relative_to(ROOT)), "workflows": workflows}


def main() -> int:
    source = json.loads(SOURCE.read_text(encoding="utf-8"))
    OUTPUT.write_text(json.dumps(build_contracts(source), indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
