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
"""Validate discovery-marathon cycle packets."""

from __future__ import annotations

import argparse
import contextlib
import io
import json
import re
from collections.abc import Mapping
from pathlib import Path
from typing import Any

from agentic.discovery.contracts import ContractError, canonical_digest, file_digest, validate_instance
from agentic.discovery.theory_gate import VerifiedTheoryAuthorization, verify_canonical_theory_cycle
from agentic.state.discovery_transaction import DiscoveryTransactionStore
from agentic_common import ROOT, clean_text, fail, load_json_object, rel
from artifact_or_stop_control import validate_cycle_artifact_or_stop
from discovery_marathon_common import load_cycles, load_run_state
from physical_relevance_impact import (
    PHYSICAL_IMPACT_DIMS,
    PHYSICAL_RELEVANCE_DECISIONS,
    PHYSICS_PUBLICATION_INVESTMENT_DECISIONS,
    YM_TARGET_ID,
)
from target_profiles import target_profile
from validate_discovery_marathon_skill_dispatch import validate_trace
from validate_proof_depth_control import validate_packet as validate_proof_depth_packet_payload


GENERIC_PHRASES = [
    "factor the opaque obligation",
    "smaller lemmas",
    "continue the analysis",
    "run the workflow",
    "generic strategy",
]

CONTRIBUTION_PIVOT_STATEMENT = (
    "If the next work only restates the obstruction ladder, the branch is looping; "
    "if it computes the first concrete H,K Wilson collar case or proves the finite theorem rigorously, "
    "or if it computes the post-H,K R/kappa_4 endpoint-box term needed by the paper handoff, "
    "or if it advances a Yang-Mills representational-dynamics frontier gate such as observable density, "
    "same-theory nontriviality, regulator/RG basin entry, large-field/topology control, continuum OS coherence, "
    "or spectral transfer, "
    "it is moving toward a real scientific contribution."
)
COMPATIBILITY_CONTRACT_VERSION = "canonical-theory-compatibility/2.0.0"


def _immutable_compatibility_envelope(
    cycle: Mapping[str, Any], source: Path
) -> dict[str, Any] | None:
    """Recover a v2 authority envelope from the legacy CAS commit, if present."""

    receipt = cycle.get("transaction_receipt")
    if not isinstance(receipt, Mapping) or not receipt.get("commit_id"):
        return None
    roots = []
    if receipt.get("transaction_root"):
        roots.append(Path(str(receipt["transaction_root"])).resolve())
    roots.append((ROOT / "agentic/state/discovery_transactions").resolve())
    for root in dict.fromkeys(roots):
        try:
            store = DiscoveryTransactionStore(
                root,
                target_id=str(cycle.get("target_id")),
                run_id=str(cycle.get("run_id")),
            )
            store.current_generation()
        except (ContractError, OSError, TypeError, ValueError):
            continue
        for commit_path in store.commits_dir.iterdir():
            manifest_path = commit_path / "manifest.json"
            if not manifest_path.is_file():
                continue
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            if (
                manifest.get("commit_id") != receipt.get("commit_id")
                or manifest.get("generation") != receipt.get("generation")
            ):
                continue
            candidates = [
                row
                for row in manifest.get("artifacts", [])
                if str(row.get("path", "")).endswith(
                    f"/cycles/{cycle.get('cycle_id')}/canonical-authority.json"
                )
            ]
            if not candidates:
                return None
            if len(candidates) != 1:
                fail(f"{rel(source)} legacy CAS has ambiguous canonical authority artifacts")
            artifact = commit_path / "artifacts" / candidates[0]["path"]
            envelope = json.loads(artifact.read_text(encoding="utf-8"))
            if not isinstance(envelope, dict):
                fail(f"{rel(source)} immutable canonical authority envelope is malformed")
            claimed = envelope.get("compatibility_digest")
            if claimed != canonical_digest(envelope, exclude_keys=("compatibility_digest",)):
                fail(f"{rel(source)} immutable canonical authority envelope digest is invalid")
            return envelope
    return None


def source_cycle_number(source: Path) -> int:
    raw = str(source)
    match = re.search(r"cycle-(\d{4})", raw)
    if not match:
        return 0
    return int(match.group(1))


def validate_contribution_pivot_invariant(output: dict[str, Any], source: Path) -> None:
    """Prevent current/future Wilson-OS cycles from only restating the obstruction ladder."""
    cycle_number = source_cycle_number(source)
    text = clean_text(output).lower()
    if cycle_number and cycle_number < 230:
        return
    if not any(term in text for term in ["wilson", "hairpin", "collar", "schur", "feshbach", "obstruction ladder"]):
        return
    next_experiment = clean_text(output.get("next_experiment", "")).lower()
    branch_title = clean_text(output.get("branch_title", "")).lower()
    finite_theorem_move = (
        any(term in next_experiment for term in ["prove", "state", "formalize"])
        and "finite" in next_experiment
        and any(term in next_experiment for term in ["theorem", "schur", "feshbach", "tangent-cone", "tangent cone"])
    )
    hk_case_move = (
        any(term in next_experiment for term in ["compute", "extract", "parameterize", "parametrize", "evaluate", "test"])
        and any(term in next_experiment for term in ["h,k", "h and k", " h ", " h,", "corrected k"])
        and any(term in next_experiment for term in ["wilson", "hairpin", "collar"])
    )
    rkappa_case_move = (
        any(term in next_experiment for term in ["compute", "extract", "estimate", "bound", "evaluate", "enumerate", "test"])
        and any(term in next_experiment for term in ["r_", " r ", "r^{", "kappa", "κ", "endpoint", "plaquette", "four-flux", "commutator"])
        and any(term in next_experiment for term in ["wilson", "hairpin", "boundary", "plaquette", "footprint", "heat-kernel"])
    )
    ym_overlay_move = (
        any(
            term in next_experiment
            for term in [
                "prove",
                "construct",
                "certify",
                "select",
                "compute",
                "bound",
                "test",
                "falsify",
                "audit",
                "verify",
                "validate",
                "identify",
                "isolate",
                "classify",
                "localize",
                "formalize",
                "state",
            ]
        )
        and any(
            term in next_experiment
            for term in [
                "observable density",
                "gauge-invariant observable density",
                "gauge-invariant observable",
                "observable algebra",
                "excitation sector",
                "excitation-sector",
                "cyclicity",
                "cyclic vector",
                "reflection positivity",
                "reflection-positive",
                "os positivity",
                "os reconstruction",
                "os hilbert",
                "hilbert observable",
                "vacuum-orthogonal",
                "p_perp",
                "hamiltonian",
                "h_ym",
                "separating",
                "continuum schwinger",
                "nontriviality witness",
                "same-theory nontriviality",
                "connected cumulant",
                "connected cumulant witness",
                "non-gaussian",
                "surviving cumulant",
                "higher cumulant",
                "schwinger family",
                "same-theory",
                "same theory",
                "regulator",
                "rg",
                "basin entry",
                "large-field",
                "topolog",
                "fiber",
                "os algebra",
                "cutoff removal",
                "spectral measure",
                "witness selection",
                "spectral transfer",
                "frontier",
                "claim level",
                "proof object",
            ]
        )
    )
    ym_frontier_branch_move = (
        any(
            term in branch_title
            for term in [
                "nontriviality witness",
                "observable density",
                "excitation sector",
                "reflection-positivity",
                "reflection positivity",
                "closed-cone topology",
            ]
        )
        and any(
            term in next_experiment
            for term in [
                "prove",
                "construct",
                "certify",
                "select",
                "compute",
                "bound",
                "test",
                "falsify",
                "audit",
                "verify",
                "validate",
                "formalize",
                "state",
                "instantiate",
                "derive",
                "identify",
                "isolate",
                "classify",
                "localize",
                "separate",
                "compare",
            ]
        )
        and not any(phrase in next_experiment for phrase in GENERIC_PHRASES)
    )
    explicit_loop_decision = (
        "looping" in text
        and any(term in text for term in ["backtrack", "repair", "quarantine"])
    )
    if finite_theorem_move or hk_case_move or rkappa_case_move or ym_overlay_move or ym_frontier_branch_move or explicit_loop_decision:
        return
    fail(
        f"{rel(source)} violates contribution pivot invariant: {CONTRIBUTION_PIVOT_STATEMENT} "
        "The next_experiment must aim at the finite theorem, the concrete H,K Wilson collar case, the post-H,K R/kappa_4 endpoint calculation, a representational-dynamics YM frontier gate, or an explicit loop/backtrack/quarantine decision."
    )


def validate_equation(eq: dict[str, Any], source: Path) -> None:
    for field in ["label", "latex", "valid_when"]:
        if not clean_text(eq.get(field)):
            fail(f"{rel(source)} equation missing {field}")
    if len(clean_text(eq.get("valid_when")).split()) < 8:
        fail(f"{rel(source)} equation validity condition must explain when it applies")


def validate_cross_target_terms(output: dict[str, Any], source: Path, target_id: str | None) -> None:
    profile = target_profile(target_id)
    text = clean_text(output).lower()
    forbidden = [term for term in profile.get("forbidden_cross_target_terms", []) if term in text]
    if forbidden:
        fail(f"{rel(source)} branch output for {profile['target_id']} contains cross-target terms: {sorted(set(forbidden))}")


def validate_parallel_execution(cycle: dict[str, Any], source: Path) -> None:
    parallel = cycle.get("parallel_execution")
    synthesis = cycle.get("parallel_synthesis")
    if parallel is None and synthesis is None:
        return
    if not isinstance(parallel, dict):
        fail(f"{rel(source)} parallel_execution must be an object when present")
    if not isinstance(synthesis, dict):
        fail(f"{rel(source)} parallel_synthesis must be an object when parallel_execution is present")
    for field in ["enabled", "max_workers", "worker_engine", "merge_policy", "state_mutation_policy"]:
        if field not in parallel:
            fail(f"{rel(source)} parallel_execution missing {field}")
    if parallel.get("merge_policy") != "scheduler_order_single_writer":
        fail(f"{rel(source)} parallel_execution must use scheduler_order_single_writer")
    if int(parallel.get("max_workers", 0)) < 1:
        fail(f"{rel(source)} parallel_execution max_workers must be positive")
    selected_ids = cycle.get("selected_branch_ids", [])
    output_ids = [output.get("branch_id") for output in cycle.get("branch_outputs", [])]
    if len(set(output_ids)) != len(output_ids) or [item for item in selected_ids if item in set(output_ids)] != output_ids:
        fail(f"{rel(source)} successful branch_outputs must be an ordered subset of selected_branch_ids")
    records = cycle.get("branch_execution_records", [])
    for index, record in enumerate(records):
        if not isinstance(record, dict):
            fail(f"{rel(source)} branch_execution_records[{index}] must be an object")
        if "parallel_worker_index" not in record or "parallel_max_workers" not in record:
            fail(f"{rel(source)} branch_execution_records[{index}] missing parallel worker metadata")
        if int(record.get("parallel_worker_index", -1)) != index:
            fail(f"{rel(source)} branch_execution_records[{index}] worker index must match scheduler order")
    for field in ["merge_policy", "state_mutation_policy", "cited_branch_ids", "common_proof_obligations", "queue_promotions"]:
        if field not in synthesis:
            fail(f"{rel(source)} parallel_synthesis missing {field}")
    if synthesis.get("merge_policy") != "scheduler_order_single_writer":
        fail(f"{rel(source)} parallel_synthesis must use scheduler_order_single_writer")
    if synthesis.get("cited_branch_ids") != output_ids:
        fail(f"{rel(source)} parallel_synthesis cited_branch_ids must match validated successful outputs")
    promotions = synthesis.get("queue_promotions", [])
    if not isinstance(promotions, list) or (output_ids and not promotions):
        fail(f"{rel(source)} parallel_synthesis needs queue_promotions for successful outputs")
    for item in promotions:
        if not isinstance(item, dict):
            fail(f"{rel(source)} parallel_synthesis queue promotion must be an object")
        for field in ["pressure_family", "cited_branch_ids", "next_analysis", "promotion_test"]:
            if not clean_text(item.get(field)):
                fail(f"{rel(source)} parallel_synthesis queue promotion missing {field}")
        if cycle.get("target_id") == "p-vs-np-target":
            for field in ["novelty_signal", "high_reward_payoff", "step_back_or_pivot_criterion"]:
                if not clean_text(item.get(field)):
                    fail(f"{rel(source)} P vs NP parallel_synthesis queue promotion missing {field}")
        if cycle.get("target_id") == YM_TARGET_ID and (source_cycle_number(source) >= 352 or source_cycle_number(source) == 0):
            for field in ["physics_conceptual_reward", "investment_decision"]:
                if not clean_text(item.get(field)):
                    fail(f"{rel(source)} YM parallel_synthesis queue promotion missing {field}")
            if item.get("major_publication_potential") not in {True, False}:
                fail(f"{rel(source)} YM parallel_synthesis queue promotion major_publication_potential must be boolean")
            if clean_text(item.get("investment_decision")) not in PHYSICS_PUBLICATION_INVESTMENT_DECISIONS:
                fail(f"{rel(source)} YM parallel_synthesis queue promotion invalid investment_decision {item.get('investment_decision')}")


def validate_branch_output(output: dict[str, Any], source: Path, target_id: str | None = None) -> None:
    for field in ["branch_id", "branch_title", "candidate_lemmas", "attempted_derivation", "falsifiers", "dependency_updates", "mathematical_learning", "control_decision", "next_experiment"]:
        if not output.get(field):
            fail(f"{rel(source)} branch output missing {field}")
    text = clean_text(output).lower()
    for phrase in GENERIC_PHRASES:
        if phrase in text:
            fail(f"{rel(source)} branch output contains stale generic phrase `{phrase}`")
    profile = target_profile(target_id)
    required_markers = ["source object", "target object", "valid", "falsifier"]
    if not any(marker in text for marker in profile.get("consistency_markers", [])):
        fail(f"{rel(source)} branch output lacks a target consistency marker: {profile.get('consistency_markers', [])}")
    for marker in required_markers:
        if marker not in text:
            fail(f"{rel(source)} branch output lacks mathematical marker `{marker}`")
    validate_cross_target_terms(output, source, target_id)
    lemmas = output.get("candidate_lemmas", [])
    if not isinstance(lemmas, list) or not lemmas:
        fail(f"{rel(source)} branch output needs candidate lemmas")
    for lemma in lemmas:
        for field in ["lemma_id", "statement", "definitions", "assumptions", "equations", "proof_role", "failure_test"]:
            if not lemma.get(field):
                fail(f"{rel(source)} lemma missing {field}")
        if len(lemma.get("definitions", [])) < 3 or len(lemma.get("assumptions", [])) < 2:
            fail(f"{rel(source)} lemma must state definitions and assumptions")
        validate_definition_assumption_elicitation(lemma, output, source, target_id)
        for eq in lemma.get("equations", []):
            validate_equation(eq, source)
    derivation = output.get("attempted_derivation", {})
    if len(derivation.get("steps", [])) < 3 or not clean_text(derivation.get("blocking_gap")):
        fail(f"{rel(source)} attempted derivation must have steps and blocking gap")
    if len(output.get("falsifiers", [])) < 2:
        fail(f"{rel(source)} branch output needs falsifiers")
    validate_gedanken_experiment_design(output, source, target_id)
    validate_negative_tactic_decision(output, source, target_id)
    validate_pvsnp_inference_quality_packet(output, source, target_id)
    validate_proof_depth_control_packet(output, source, target_id)
    validate_physical_relevance_impact_packet(output, source, target_id)
    validate_contribution_pivot_invariant(output, source)


def requires_physical_relevance_packet(source: Path, target_id: str | None) -> bool:
    if clean_text(target_id) != YM_TARGET_ID:
        return False
    raw = str(source)
    if "api-output:" in raw or "codex-output:" in raw:
        return True
    cycle_number = source_cycle_number(source)
    return bool(cycle_number and cycle_number >= 352)


def validate_physical_relevance_impact_packet(output: dict[str, Any], source: Path, target_id: str | None) -> None:
    packet = output.get("physical_relevance_impact")
    if packet is None:
        if requires_physical_relevance_packet(source, target_id):
            fail(f"{rel(source)} YM branch output missing physical_relevance_impact packet for physical relevance and general impact gating")
        return
    if not isinstance(packet, dict):
        fail(f"{rel(source)} physical_relevance_impact must be an object when present")
    if clean_text(packet.get("target_id")) != clean_text(target_id):
        fail(f"{rel(source)} physical_relevance_impact target_id must match the branch target")
    required = [
        "packet_id",
        "branch_id",
        "cycle_id",
        "source_object",
        "target_object",
        "physical_carrier",
        "target_commitments_touched",
        "general_impact_vector",
        "relevance_decision",
        "general_impact_claim",
        "incremental_math_drift_risk",
        "next_physical_relevance_test",
        "evidence",
        "generated_by_skills",
        "validation_handoff",
    ]
    for field in required:
        if not clean_text(packet.get(field)):
            fail(f"{rel(source)} physical_relevance_impact missing {field}")
    if clean_text(packet.get("relevance_decision")) not in PHYSICAL_RELEVANCE_DECISIONS:
        fail(f"{rel(source)} physical_relevance_impact has invalid relevance_decision {packet.get('relevance_decision')}")
    commitments = packet.get("target_commitments_touched")
    if not isinstance(commitments, list) or len([item for item in commitments if clean_text(item)]) < 1:
        fail(f"{rel(source)} physical_relevance_impact needs target_commitments_touched")
    evidence = packet.get("evidence")
    if not isinstance(evidence, list) or len([item for item in evidence if clean_text(item)]) < 3:
        fail(f"{rel(source)} physical_relevance_impact needs at least three evidence anchors")
    generated = set(packet.get("generated_by_skills", [])) if isinstance(packet.get("generated_by_skills"), list) else set()
    if "physical-relevance-impact-auditor" not in generated:
        fail(f"{rel(source)} physical_relevance_impact must cite physical-relevance-impact-auditor")
    vector = packet.get("general_impact_vector")
    if not isinstance(vector, dict):
        fail(f"{rel(source)} physical_relevance_impact general_impact_vector must be an object")
    for dim in PHYSICAL_IMPACT_DIMS:
        item = vector.get(dim)
        if not isinstance(item, dict):
            fail(f"{rel(source)} physical_relevance_impact general_impact_vector missing {dim}")
        for field in ["score", "evidence", "missing_evidence", "demotion_trigger"]:
            if not clean_text(item.get(field)):
                fail(f"{rel(source)} physical_relevance_impact {dim} missing {field}")
        try:
            score = int(item.get("score"))
        except (TypeError, ValueError):
            fail(f"{rel(source)} physical_relevance_impact {dim}.score must be an integer")
        if score < 0 or score > 5:
            fail(f"{rel(source)} physical_relevance_impact {dim}.score must be between 0 and 5")
    packet_text = clean_text(packet).lower()
    physical_terms = [
        "gauge-invariant",
        "gauge invariant",
        "wilson",
        "schwinger",
        "os hilbert",
        "observable",
        "hamiltonian",
        "spectral",
        "mass gap",
        "nontrivial",
        "cumulant",
    ]
    if not any(term in packet_text for term in physical_terms):
        fail(f"{rel(source)} physical_relevance_impact lacks concrete Yang-Mills physical-carrier language")
    if clean_text(packet.get("relevance_decision")) == "physically_relevant_candidate":
        if "missing physical carrier" in packet_text or "not_yet_identified" in packet_text:
            fail(f"{rel(source)} physically relevant candidate cannot have missing carrier or target commitment")
    if requires_physical_relevance_packet(source, target_id):
        validate_major_publication_gate(output, packet, source)


def validate_major_publication_gate(output: dict[str, Any], packet: dict[str, Any], source: Path) -> None:
    gate = packet.get("major_publication_gate")
    if not isinstance(gate, dict):
        fail(f"{rel(source)} physical_relevance_impact missing major_publication_gate")
    required = [
        "investment_decision",
        "major_publication_potential",
        "physics_conceptual_reward",
        "publication_claim_candidate",
        "must_change_understanding",
        "unification_power_requirement",
        "investment_rationale",
        "non_investment_trigger",
        "required_next_artifact",
        "validation_rule",
    ]
    for field in required:
        value = gate.get(field)
        if field == "major_publication_potential":
            if not isinstance(value, bool):
                fail(f"{rel(source)} major_publication_gate.major_publication_potential must be boolean")
        elif not clean_text(value):
            fail(f"{rel(source)} major_publication_gate missing {field}")
    decision = clean_text(gate.get("investment_decision"))
    if decision not in PHYSICS_PUBLICATION_INVESTMENT_DECISIONS:
        fail(f"{rel(source)} major_publication_gate has invalid investment_decision {decision}")
    major_publication_potential = bool(gate.get("major_publication_potential"))
    if major_publication_potential != (decision == "invest_high_physics_reward"):
        fail(f"{rel(source)} major_publication_gate major_publication_potential does not match investment_decision")
    gate_text = clean_text(gate).lower()
    if "publication" not in gate_text or not any(term in gate_text for term in ["understand", "conceptual", "field-facing"]):
        fail(f"{rel(source)} major_publication_gate must state publication and conceptual-understanding payoff")
    if not any(term in gate_text for term in ["unification", "unify", "unified", "unifying"]):
        fail(f"{rel(source)} major_publication_gate must state unification-power payoff")
    if decision == "invest_high_physics_reward":
        if clean_text(gate.get("physics_conceptual_reward")) != "high":
            fail(f"{rel(source)} invest_high_physics_reward requires physics_conceptual_reward=high")
        packet_text = clean_text(packet).lower()
        if "missing physical carrier" in packet_text or "not_yet_identified" in packet_text:
            fail(f"{rel(source)} invest_high_physics_reward cannot have missing carrier or target commitment")
        if clean_text(packet.get("relevance_decision")) != "physically_relevant_candidate":
            fail(f"{rel(source)} invest_high_physics_reward requires physically_relevant_candidate relevance")
        return
    branch_control_text = clean_text(
        {
            "control_decision": output.get("control_decision"),
            "next_experiment": output.get("next_experiment"),
            "falsifiers": output.get("falsifiers"),
            "major_publication_gate": gate,
        }
    ).lower()
    stop_markers = [
        "do not invest",
        "support-only",
        "support only",
        "demote",
        "demotion",
        "quarantine",
        "stop",
        "pivot",
        "reframe",
        "artifact_sprint",
        "falsifier_sprint",
        "publication_demotion",
    ]
    if not any(marker in branch_control_text for marker in stop_markers):
        fail(
            f"{rel(source)} non-investable YM branch must demote, reframe, pivot, stop, "
            "or quarantine instead of requesting another ordinary proof cycle"
        )


def validate_proof_depth_control_packet(output: dict[str, Any], source: Path, target_id: str | None) -> None:
    packet = output.get("proof_depth_control")
    if packet is None:
        return
    if not isinstance(packet, dict):
        fail(f"{rel(source)} proof_depth_control must be an object when present")
    if clean_text(packet.get("target_id")) != clean_text(target_id):
        fail(f"{rel(source)} proof_depth_control target_id must match the branch target")
    validate_proof_depth_packet_payload(packet, source)


def validate_definition_assumption_elicitation(lemma: dict[str, Any], output: dict[str, Any], source: Path, target_id: str | None) -> None:
    """Require future timeline entries to make definitions and assumptions content-specific."""
    cycle_number = source_cycle_number(source)
    if not cycle_number or cycle_number < 61:
        return
    if clean_text(target_id) == YM_TARGET_ID and cycle_number < 352:
        return
    definitions_text = clean_text(lemma.get("definitions", [])).lower()
    assumptions_text = clean_text(lemma.get("assumptions", [])).lower()
    if "source object" not in definitions_text:
        fail(f"{rel(source)} lemma definitions must identify the source object for timeline readability")
    if "target object" not in definitions_text:
        fail(f"{rel(source)} lemma definitions must identify the target object for timeline readability")
    regime_markers = [
        "valid",
        "regime",
        "model",
        "uniform",
        "advice",
        "barrier",
        "natural",
        "same-theory",
        "same theory",
        "cutoff",
        "covariance",
        "density",
        "rule",
        "syntax",
        "syntactic",
        "transcript",
        "proof-size",
        "proof size",
        "semantic",
        "computable",
        "occurrence",
        "certificate",
        "local",
        "constraint",
        "projection",
        "cluster",
        "continuum",
        "field",
        "gauge",
        "affine",
        "consistency",
        "axiom",
        "function",
        "patch",
        "regulator",
        "reflection",
        "spectral",
        "topolog",
        "volume",
        "wilson",
        "observable",
        "os positivity",
        "row",
    ]
    if not any(marker in assumptions_text for marker in regime_markers):
        fail(f"{rel(source)} lemma assumptions must state a validity regime or model condition")
    weak_phrases = ["under the assumptions", "under stated assumptions", "as above", "standard assumptions"]
    if any(phrase in assumptions_text for phrase in weak_phrases):
        fail(f"{rel(source)} lemma assumptions are too generic for timeline use")
    derivation_text = clean_text(output.get("attempted_derivation", {})).lower()
    if output.get("attempted_derivation", {}).get("steps") and not any(
        marker in derivation_text for marker in ["definition", "assumption", "valid", "regime", "model", "source object", "target object"]
    ):
        fail(f"{rel(source)} attempted derivation must cite definitions, assumptions, or validity regime")


def validate_negative_tactic_decision(output: dict[str, Any], source: Path, target_id: str | None) -> None:
    """Require scoped contradiction/no-go tactic control for new P vs NP branch packets."""
    if target_id != "p-vs-np-target":
        return
    cycle_number = source_cycle_number(source)
    should_require = cycle_number == 0 or cycle_number >= 61
    packet = output.get("negative_tactic_decision")
    if packet is None and not should_require:
        return
    if not isinstance(packet, dict):
        fail(f"{rel(source)} P vs NP branch output missing negative_tactic_decision")
    required = [
        "tactic_mode",
        "route_family",
        "reason_for_tactic",
        "exact_negation_or_method_class",
        "contradiction_carrier_or_no_go_family",
        "conflict_target",
        "escape_conditions",
        "proof_obligations",
        "branch_control_decision",
        "next_validation_handoff",
        "paper_contribution_potential",
    ]
    for field in required:
        if not clean_text(packet.get(field)):
            fail(f"{rel(source)} P vs NP negative_tactic_decision missing {field}")
    allowed_modes = {
        "constructive_bridge",
        "proof_by_contradiction",
        "impossibility_theorem",
        "falsifier_search",
        "backtrack",
        "quarantine",
        "stop",
    }
    if packet.get("tactic_mode") not in allowed_modes:
        fail(f"{rel(source)} P vs NP negative_tactic_decision invalid tactic_mode {packet.get('tactic_mode')}")
    for list_field in ["escape_conditions", "proof_obligations"]:
        items = packet.get(list_field)
        if not isinstance(items, list) or len([item for item in items if clean_text(item)]) < 2:
            fail(f"{rel(source)} P vs NP negative_tactic_decision needs at least two {list_field}")
    tactic_text = clean_text(packet).lower()
    domain_markers = [
        "sat",
        "circuit",
        "p/poly",
        "np",
        "beta",
        "q",
        "padding",
        "natural",
        "mcsp",
        "mktp",
        "proof",
        "advice",
        "oracle",
        "algebrization",
        "relativization",
    ]
    if not any(marker in tactic_text for marker in domain_markers):
        fail(f"{rel(source)} P vs NP negative_tactic_decision lacks concrete complexity-theoretic language")
    if packet.get("tactic_mode") in {"proof_by_contradiction", "impossibility_theorem"}:
        for marker in ["method", "conflict", "target", "escape"]:
            if marker not in tactic_text:
                fail(f"{rel(source)} P vs NP negative_tactic_decision lacks `{marker}` for {packet.get('tactic_mode')}")
    if "assume p=np" in tactic_text and "local" not in tactic_text:
        fail(f"{rel(source)} P vs NP negative_tactic_decision uses global assume P=NP rhetoric without local carrier")


def validate_pvsnp_inference_quality_packet(output: dict[str, Any], source: Path, target_id: str | None) -> None:
    """Require live inference-quality packets for P vs NP cycles after the proof-convergence reset."""
    if target_id != "p-vs-np-target":
        return
    cycle_number = source_cycle_number(source)
    if cycle_number and cycle_number < 90:
        return
    packet = output.get("pvsnp_inference_quality")
    if not isinstance(packet, dict):
        fail(
            f"{rel(source)} P vs NP branch output missing pvsnp_inference_quality; "
            "cycle 90+ is focused on live inference-quality packet emission before promotion"
        )
    if packet.get("live_packet") is not True:
        fail(f"{rel(source)} P vs NP pvsnp_inference_quality must set live_packet=true")
    from validate_pvsnp_inference_quality import SCHEMA as PVSNP_IQ_SCHEMA
    from validate_pvsnp_inference_quality import validate_packet as validate_pvsnp_packet

    validate_pvsnp_packet(packet, source, load_json_object(PVSNP_IQ_SCHEMA))


def validate_gedanken_experiment_design(output: dict[str, Any], source: Path, target_id: str | None) -> None:
    """Require concrete thought-experiment content for new P vs NP branch packets."""
    cycle_number = source_cycle_number(source)
    if target_id != "p-vs-np-target":
        return
    # Cycles before this validator existed may have empty renderer scaffolding.
    if cycle_number and cycle_number < 11:
        return
    design = output.get("gedanken_experiment_design")
    if not isinstance(design, dict):
        fail(f"{rel(source)} P vs NP branch output missing gedanken_experiment_design")
    required = [
        "need_decision",
        "rationale",
        "situation_seed",
        "varied_variable",
        "held_fixed_controls",
        "expected_observation",
        "transfer_certificate_needed",
    ]
    for field in required:
        if not clean_text(design.get(field)):
            fail(f"{rel(source)} P vs NP gedanken_experiment_design missing {field}")
    controls = design.get("held_fixed_controls")
    if not isinstance(controls, list) or len([item for item in controls if clean_text(item)]) < 2:
        fail(f"{rel(source)} P vs NP gedanken_experiment_design needs at least two held-fixed controls")
    concrete_text = clean_text(design).lower()
    domain_markers = [
        "sat",
        "circuit",
        "mcsp",
        "mktp",
        "oracle",
        "proof",
        "advice",
        "density",
        "explicit",
        "verifier",
        "query",
        "threshold",
        "lower bound",
        "p/poly",
        "nexp",
    ]
    if not any(marker in concrete_text for marker in domain_markers):
        fail(f"{rel(source)} P vs NP gedanken_experiment_design must name a concrete complexity-theoretic situation")
    if any(clean_text(design.get(field)) in {"", "``"} for field in required):
        fail(f"{rel(source)} P vs NP gedanken_experiment_design contains empty scaffold text")


def validate_receipt_backed_cycle(cycle: dict[str, Any], source: Path) -> None:
    """Validate semantic validity independently of elapsed-time observations."""

    selected = cycle["selected_branch_ids"]
    receipts = cycle.get("operator_receipts", [])
    deltas = cycle.get("learning_deltas", [])
    reducer_receipts = cycle.get("learning_reducer_receipts", [])
    transaction = cycle.get("transaction_receipt")
    basis = cycle.get("research_validity_basis")
    if not isinstance(basis, dict) or basis.get("policy") != "semantic_receipts_not_elapsed_time":
        fail(f"{rel(source)} receipt-backed cycle has invalid research_validity_basis")
    if not isinstance(transaction, dict) or not clean_text(transaction.get("commit_id")):
        fail(f"{rel(source)} receipt-backed cycle lacks a CAS transaction receipt")
    if not isinstance(receipts, list) or len(receipts) != len(selected):
        fail(f"{rel(source)} receipt-backed cycle needs one operator receipt per attempted branch")
    receipt_by_branch: dict[str, dict[str, Any]] = {}
    for receipt in receipts:
        try:
            validate_instance(receipt, "discovery_operator_receipt.schema.json")
        except ContractError as exc:
            fail(f"{rel(source)} invalid operator receipt: {exc}")
        identity = receipt["identity"]
        if identity["target_id"] != cycle["target_id"] or identity["run_id"] != cycle["run_id"]:
            fail(f"{rel(source)} operator receipt crossed target/run identity")
        receipt_by_branch[identity["branch_id"]] = receipt
    if set(receipt_by_branch) != set(selected):
        fail(f"{rel(source)} operator receipts do not cover the exact selected branches")
    if set(basis.get("operator_receipt_ids", [])) != {row["receipt_id"] for row in receipts}:
        fail(f"{rel(source)} validity basis does not bind all operator receipts")

    if not isinstance(deltas, list) or len(deltas) != len(selected):
        fail(f"{rel(source)} receipt-backed cycle needs one learning delta per attempted branch")
    delta_by_branch: dict[str, dict[str, Any]] = {}
    for delta in deltas:
        try:
            validate_instance(delta, "discovery_learning_delta.schema.json")
        except ContractError as exc:
            fail(f"{rel(source)} invalid learning delta: {exc}")
        branch_id = delta["identity"]["branch_id"]
        receipt = receipt_by_branch.get(branch_id)
        if receipt is None or receipt["receipt_id"] not in delta["operator_receipt_ids"]:
            fail(f"{rel(source)} learning delta is not bound to its branch operator receipt")
        if receipt["status"] != "succeeded" and delta["classification"] != "operational_failure":
            fail(f"{rel(source)} failed execution was converted into epistemic learning")
        delta_by_branch[branch_id] = delta
    if set(delta_by_branch) != set(selected):
        fail(f"{rel(source)} learning deltas do not cover the exact selected branches")

    if not isinstance(reducer_receipts, list) or len(reducer_receipts) != len(selected):
        fail(f"{rel(source)} receipt-backed cycle needs one reducer receipt per attempted branch")
    recognized_ids = {
        row.get("delta_id")
        for row in reducer_receipts
        if isinstance(row, dict) and row.get("learning_recognized") is True
    }
    if recognized_ids != set(basis.get("recognized_learning_delta_ids", [])):
        fail(f"{rel(source)} validity basis does not match reducer-recognized deltas")
    expected_valid = cycle.get("execution_mode") == "research" and bool(recognized_ids)
    if cycle.get("valid_as_research_cycle") is not expected_valid:
        fail(f"{rel(source)} valid_as_research_cycle must derive from semantic reducer receipts")
    failed_ids = {
        branch_id
        for branch_id, delta in delta_by_branch.items()
        if delta["classification"] == "operational_failure"
    }
    if failed_ids != set(cycle.get("operational_failure_branch_ids", [])):
        fail(f"{rel(source)} operational failure branch ledger is inconsistent")
    successful_ids = [
        branch_id for branch_id in selected if receipt_by_branch[branch_id]["status"] == "succeeded"
    ]
    if successful_ids != cycle.get("successful_branch_ids", []):
        fail(f"{rel(source)} successful branch ledger is inconsistent")


def validate_canonical_theory_gate(
    cycle: dict[str, Any], source: Path
) -> VerifiedTheoryAuthorization | None:
    """Replay the exact canonical commit named by a modern compatibility cycle."""

    immutable_envelope = _immutable_compatibility_envelope(cycle, source)
    phase_ids = {
        row.get("phase")
        for row in cycle.get("skill_dispatch_trace", [])
        if isinstance(row, dict)
    }
    modern = (
        "current_literature_assimilation_rebase" in phase_ids
        or cycle.get("version") == 2
        or cycle.get("compatibility_contract_version") == COMPATIBILITY_CONTRACT_VERSION
        or immutable_envelope is not None
    )
    if not modern:
        return None
    if immutable_envelope is not None:
        if cycle.get("compatibility_contract_version") != COMPATIBILITY_CONTRACT_VERSION:
            fail(f"{rel(source)} removed or downgraded its immutable v2 compatibility contract")
        for field in ("canonical_theory_gate", "canonical_action_reservation"):
            if canonical_digest(cycle.get(field)) != canonical_digest(immutable_envelope.get(field)):
                fail(f"{rel(source)} {field} differs from the immutable legacy CAS envelope")
        if sorted(cycle.get("selected_branch_ids", [])) != immutable_envelope.get("selected_branch_ids"):
            fail(f"{rel(source)} selected branches differ from the immutable authority envelope")
    gate = cycle.get("canonical_theory_gate")
    if not isinstance(gate, dict):
        fail(f"{rel(source)} modern marathon cycle lacks canonical_theory_gate")
    if cycle.get("execution_mode") != "research":
        if gate.get("status") != "smoke_non_authoritative" or gate.get("authoritative") is not False:
            fail(f"{rel(source)} non-research compatibility cycle must carry a non-authoritative smoke gate")
        return None
    if gate.get("status") != "verified_active_current" or gate.get("authoritative") is not True:
        fail(f"{rel(source)} research cycle lacks an authoritative active-current theory gate")
    if gate.get("target_id") != cycle.get("target_id") or gate.get("run_id") != cycle.get("run_id"):
        fail(f"{rel(source)} canonical theory gate crossed target/run identity")
    if not set(cycle.get("selected_branch_ids", [])).issubset(
        set(gate.get("eligible_branch_ids", []))
    ):
        fail(f"{rel(source)} selected branches exceed canonical schedule authorization")
    try:
        verified = verify_canonical_theory_cycle(
            gate.get("projection_path", ""),
            target_id=cycle["target_id"],
            run_id=cycle["run_id"],
            state_root=gate.get("transaction_root", ""),
            require_current=False,
        )
    except (ContractError, OSError, TypeError, ValueError) as exc:
        fail(f"{rel(source)} cannot replay canonical theory gate: {exc}")
    stable_fields = {
        "target_id",
        "run_id",
        "cycle_id",
        "prior_state_version",
        "committed_state_version",
        "commit_id",
        "manifest_digest",
        "transaction_root",
        "commit_path",
        "manifest_path",
        "projection_path",
        "projection_digest",
        "literature_snapshot_id",
        "literature_snapshot_digest",
        "literature_freshness_policy",
        "literature_consume_before",
        "schedule_id",
        "schedule_digest",
        "schedule",
        "proof_handoff",
        "operator_evidence_digest",
        "conceptual_authority",
        "operator_bindings",
        "eligible_branch_ids",
        "action_ids_by_branch",
        "action_kinds_by_branch",
        "authorization_semantics",
        "authorization_digest",
    }
    recorded = {field: gate.get(field) for field in stable_fields}
    replayed = {field: verified.get(field) for field in stable_fields}
    if canonical_digest(recorded) != canonical_digest(replayed):
        fail(f"{rel(source)} canonical theory gate differs from replayed commit authorization")
    if cycle.get("compatibility_contract_version") == COMPATIBILITY_CONTRACT_VERSION:
        reservation = cycle.get("canonical_action_reservation")
        if not isinstance(reservation, dict):
            fail(f"{rel(source)} v2 compatibility cycle lacks canonical action reservation")
        core_keys = {
            "schema_version",
            "reservation_id",
            "target_id",
            "run_id",
            "source_cycle_id",
            "source_commit_id",
            "source_state_generation",
            "reserved_state_generation",
            "schedule_id",
            "schedule_digest",
            "action_ids",
            "actions",
            "consumer_receipt_id",
            "consume_before",
            "status",
            "event_ids",
            "reservation_digest",
        }
        core = {key: reservation.get(key) for key in core_keys}
        if core["reservation_digest"] != canonical_digest(
            core, exclude_keys=("reservation_digest",)
        ):
            fail(f"{rel(source)} canonical action reservation digest is invalid")
        if (
            core["target_id"] != cycle.get("target_id")
            or core["run_id"] != cycle.get("run_id")
            or core["source_cycle_id"] != gate.get("cycle_id")
            or core["source_commit_id"] != gate.get("commit_id")
            or core["source_state_generation"] != gate.get("committed_state_version")
            or core["reserved_state_generation"] != gate.get("committed_state_version") + 1
            or core["schedule_id"] != gate.get("schedule_id")
            or core["schedule_digest"] != gate.get("schedule_digest")
            or core["status"] != "reserved_before_investment"
        ):
            fail(f"{rel(source)} canonical action reservation crossed theory lineage")
        selected = set(cycle.get("selected_branch_ids", []))
        reserved_branches = {
            branch_id for action in core["actions"] for branch_id in action.get("branch_ids", [])
        }
        gate_action_ids = {
            action_id
            for branch_id in selected
            for action_id in gate.get("action_ids_by_branch", {}).get(branch_id, [])
        }
        if (
            selected != reserved_branches
            or not set(core["action_ids"]).issubset(gate_action_ids)
            or any(action.get("kind") in {"prove", "probe"} for action in core["actions"])
        ):
            fail(f"{rel(source)} marathon reservation exceeds conceptual branch/action authority")
        if (
            reservation.get("reservation_transaction_root") != gate.get("transaction_root")
            or reservation.get("reservation_committed_state_version")
            != core["reserved_state_generation"]
        ):
            fail(f"{rel(source)} reservation commit location/generation is inconsistent")
        reservation_store = DiscoveryTransactionStore(
            Path(str(reservation["reservation_transaction_root"])),
            target_id=cycle["target_id"],
            run_id=cycle["run_id"],
        )
        reservation_store.current_generation()
        matches = [
            path
            for path in reservation_store.commits_dir.iterdir()
            if path.name.endswith(str(reservation.get("reservation_commit_id")))
        ]
        if len(matches) != 1 or file_digest(matches[0] / "manifest.json") != reservation.get(
            "reservation_manifest_digest"
        ):
            fail(f"{rel(source)} reservation commit ID/manifest is absent or ambiguous")
    return verified


def validate_cycle(cycle: dict[str, Any], source: Path) -> None:
    for field in ["version", "run_id", "cycle_id", "cycle_index", "target_id", "selected_branch_ids", "scheduler_decisions", "branch_outputs", "skill_dispatch_trace", "cycle_learning", "next_cycle_queue", "validation_handoff"]:
        if field not in cycle:
            fail(f"{rel(source)} cycle missing {field}")
    for field in ["version", "run_id", "cycle_id", "cycle_index", "target_id", "selected_branch_ids", "scheduler_decisions", "skill_dispatch_trace", "cycle_learning", "validation_handoff"]:
        if not cycle.get(field):
            fail(f"{rel(source)} cycle has empty required field {field}")
    mode = cycle.get("execution_mode", "synthetic_legacy")
    if mode not in {"research", "research_engine_check", "smoke", "synthetic_legacy"}:
        fail(f"{rel(source)} invalid execution_mode {mode}")
    if mode == "research":
        for field in ["created_utc", "completed_utc", "research_seconds_target", "research_seconds_elapsed", "branch_execution_records", "timing_validation"]:
            if field not in cycle:
                fail(f"{rel(source)} research cycle missing {field}")
        records = cycle.get("branch_execution_records", [])
        if not isinstance(records, list) or len(records) != len(cycle.get("selected_branch_ids", [])):
            fail(f"{rel(source)} research cycle needs one branch_execution_record per selected branch")
        allowed_engines = {"codex_exec", "azure_responses_api", "host_model_channel"}
        for record in records:
            if not isinstance(record, dict):
                fail(f"{rel(source)} research cycle branch records must be objects")
            if record.get("operator_receipt_status") == "succeeded" and record.get("engine") not in allowed_engines:
                fail(f"{rel(source)} successful research branch must use a real engine: {sorted(allowed_engines)}")
    elif mode == "research_engine_check":
        if cycle.get("valid_as_research_cycle"):
            fail(f"{rel(source)} research_engine_check cannot be valid_as_research_cycle")
        records = cycle.get("branch_execution_records", [])
        if not isinstance(records, list) or not records:
            fail(f"{rel(source)} research_engine_check must record branch_execution_records")
        allowed_engines = {"codex_exec", "azure_responses_api", "host_model_channel"}
        if not all(record.get("engine") in allowed_engines for record in records if isinstance(record, dict)):
            fail(f"{rel(source)} research_engine_check branch records must use a real branch engine: {sorted(allowed_engines)}")
    else:
        if cycle.get("valid_as_research_cycle"):
            fail(f"{rel(source)} non-research cycle cannot be valid_as_research_cycle")
        if mode == "synthetic_legacy" and not clean_text(cycle.get("synthetic_reason")):
            fail(f"{rel(source)} synthetic legacy cycle must state synthetic_reason")
    if not cycle.get("selected_branch_ids"):
        fail(f"{rel(source)} cycle needs selected branches")
    outputs = cycle.get("branch_outputs", [])
    if not isinstance(outputs, list):
        fail(f"{rel(source)} branch_outputs must be a list")
    if cycle.get("research_validity_basis") is not None:
        validate_receipt_backed_cycle(cycle, source)
    elif len(outputs) != len(cycle.get("selected_branch_ids", [])):
        fail(f"{rel(source)} legacy branch_outputs must match selected_branch_ids")
    for output in outputs:
        validate_branch_output(output, source, target_id=cycle.get("target_id"))
    validate_parallel_execution(cycle, source)
    artifact_errors = validate_cycle_artifact_or_stop(cycle)
    if artifact_errors:
        fail(f"{rel(source)} artifact-or-stop control invalid: {'; '.join(artifact_errors)}")
    verified_gate = validate_canonical_theory_gate(cycle, source)
    validate_trace(
        cycle.get("skill_dispatch_trace", []), source, verified_gate=verified_gate
    )
    text = clean_text(cycle).lower()
    for marker in ["typed branch lemmas", "source object", "target object", "equation", "validity condition", "falsifier"]:
        if marker not in text:
            fail(f"{rel(source)} cycle learning lacks `{marker}`")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="*")
    args = parser.parse_args()
    paths = [Path(path) for path in args.paths]
    if not paths:
        _, run_state = load_run_state()
        cycles = load_cycles(run_state) if run_state else []
        for cycle in cycles:
            validate_cycle(cycle, ROOT / f"agentic/runs/discovery_marathons/{run_state['run_id']}/cycles/{cycle['cycle_id']}.json")
        valid = ROOT / "tests/fixtures/discovery_marathon/valid_cycle.json"
        if valid.exists():
            validate_cycle(load_json_object(valid), valid)
        invalid = ROOT / "tests/fixtures/discovery_marathon/invalid_shallow_cycle.json"
        if invalid.exists():
            try:
                with contextlib.redirect_stderr(io.StringIO()):
                    validate_cycle(load_json_object(invalid), invalid)
            except SystemExit:
                pass
            else:
                fail(f"{rel(invalid)} should fail shallow-cycle validation")
        print(f"validated {len(cycles)} active discovery marathon cycle(s)")
        return 0
    for path in paths:
        validate_cycle(load_json_object(path), path)
    print(f"validated {len(paths)} discovery marathon cycle file(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
