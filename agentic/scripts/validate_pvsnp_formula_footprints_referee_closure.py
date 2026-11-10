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

"""Validate the Formula Footprints referee-objection closure packet."""

from __future__ import annotations

import json
from pathlib import Path

from agentic_common import ROOT, fail, rel
from check_strict_prefix_qrep_examples import scan


REPORT_DIR = ROOT / "agentic" / "reports" / "pvsnp_formula_footprints_referee_closure"

REQUIRED_ARTIFACTS = [
    "objection_ledger.md",
    "objection_ledger.json",
    "literature_anchor_table.md",
    "literature_anchor_table.json",
    "batched_dictionary_repair.md",
    "batched_dictionary_repair.tex",
    "nonvacuity_examples.md",
    "nonvacuity_examples.json",
    "sharpness_and_separations.md",
    "sharpness_and_separations.tex",
    "claim_reset_plan.md",
    "reframed_intro_patch.tex",
    "proof_system_instantiation_decision.md",
    "proof_system_instantiation_decision.json",
    "randomized_certificate_scope.md",
    "randomized_certificate_scope.json",
    "closure_gate_policy.md",
    "closure_gate_policy.json",
    "acceptance_response.md",
    "acceptance_response.json",
    "latest.md",
    "latest.json",
    "top_paper_criteria.md",
    "top_paper_criteria.json",
    "publication_level_gap_audit.md",
    "publication_level_gap_audit.json",
    "structured_certificate_lower_bounds_revision.tex",
    "structured_certificate_lower_bounds_revision.pdf",
    "randomized_accepting_union_theorem.md",
    "randomized_accepting_union_theorem.json",
    "identity_carrier_generic_sharpness.md",
    "identity_carrier_generic_sharpness.json",
    "proof_dependency_audit_map.md",
    "proof_dependency_audit_map.json",
    "proof_system_normalization_target.md",
    "proof_system_normalization_target.json",
    "assumption_resolution_instantiation.md",
    "assumption_resolution_instantiation.json",
    "resolution_unit_core_lower_bound.md",
    "resolution_unit_core_lower_bound.json",
    "resolution_local_clause_support.md",
    "resolution_local_clause_support.json",
    "support_local_auxiliary_resolution.md",
    "support_local_auxiliary_resolution.json",
    "support_local_extension_resolution.md",
    "support_local_extension_resolution.json",
    "dependency_cone_extension_normalizer.md",
    "dependency_cone_extension_normalizer.json",
    "canonical_syntactic_cone_normalizer.md",
    "canonical_syntactic_cone_normalizer.json",
    "final_backward_slice_lower_bound.md",
    "final_backward_slice_lower_bound.json",
    "slice_explicit_er_lower_bound.md",
    "slice_explicit_er_lower_bound.json",
    "displayed_acyclic_er_length_lower_bound.md",
    "displayed_acyclic_er_length_lower_bound.json",
    "compressed_er_expansion_transfer.md",
    "compressed_er_expansion_transfer.json",
    "macro_compressed_er_reuse_tradeoff.md",
    "macro_compressed_er_reuse_tradeoff.json",
    "support_declared_macro_er_normalizer.md",
    "support_declared_macro_er_normalizer.json",
    "support_audited_lrat_trace_normalizer.md",
    "support_audited_lrat_trace_normalizer.json",
    "provenance_typed_lrat_support_audit.md",
    "provenance_typed_lrat_support_audit.json",
    "namespace_typed_lrat_antecedent_closure_normalizer.md",
    "namespace_typed_lrat_antecedent_closure_normalizer.json",
    "strict_prefix_qrep_normalizer.md",
    "strict_prefix_qrep_normalizer.json",
    "strict_prefix_qrep_prefix_scan_examples.md",
    "strict_prefix_qrep_prefix_scan_examples.json",
    "support_audit_necessity_separator.md",
    "support_audit_necessity_separator.json",
    "support_erasure_indistinguishability_separator.md",
    "support_erasure_indistinguishability_separator.json",
    "plain_lrat_extraction_trichotomy.md",
    "plain_lrat_extraction_trichotomy.json",
    "semantic_relation_support_certificate.md",
    "semantic_relation_support_certificate.json",
    "acyclic_or_tree_residual_certificate.md",
    "acyclic_or_tree_residual_certificate.json",
    "or_dag_frontier_residual_certificate.md",
    "or_dag_frontier_residual_certificate.json",
    "acyclic_boolean_frontier_residual_certificate.md",
    "acyclic_boolean_frontier_residual_certificate.json",
    "visible_adaptive_frontier_residual_certificate.md",
    "visible_adaptive_frontier_residual_certificate.json",
    "visible_adaptive_branching_frontier_residual_certificate.md",
    "visible_adaptive_branching_frontier_residual_certificate.json",
    "hidden_adaptive_transcript_insufficiency_separator.md",
    "hidden_adaptive_transcript_insufficiency_separator.json",
    "controller_complete_adaptive_audit_normalizer.md",
    "controller_complete_adaptive_audit_normalizer.json",
    "trace_complete_dpll_decision_log_normalizer.md",
    "trace_complete_dpll_decision_log_normalizer.json",
    "antecedent_complete_cdcl_learned_clause_normalizer.md",
    "antecedent_complete_cdcl_learned_clause_normalizer.json",
    "cdcl_antecedent_erasure_trichotomy.md",
    "cdcl_antecedent_erasure_trichotomy.json",
    "rup_complete_cdcl_support_normalizer.md",
    "rup_complete_cdcl_support_normalizer.json",
    "canonical_namespace_rup_cdcl_standardizer.md",
    "canonical_namespace_rup_cdcl_standardizer.json",
    "carrier_independent_audit_upgrade_criterion.md",
    "carrier_independent_audit_upgrade_criterion.json",
    "self_auditing_rup_cdcl_instantiation.md",
    "self_auditing_rup_cdcl_instantiation.json",
    "append_only_self_auditing_rup_cdcl.md",
    "append_only_self_auditing_rup_cdcl.json",
    "prefix_typed_append_only_rup_cdcl.md",
    "prefix_typed_append_only_rup_cdcl.json",
    "prefix_typed_rup_support_witness_necessity.md",
    "prefix_typed_rup_support_witness_necessity.json",
    "cone_budget_extension_lower_bound.md",
    "cone_budget_extension_lower_bound.json",
    "bounded_depth_extension_tradeoff.md",
    "bounded_depth_extension_tradeoff.json",
    "support_local_normalization_transfer.md",
    "support_local_normalization_transfer.json",
    "novelty_delta_accounting.md",
    "novelty_delta_accounting.json",
    "cohered_result_spine.md",
    "cohered_result_spine.json",
]

REQUIRED_RESULT_CARD_FIELDS = {
    "external_anchor",
    "nonvacuity_witness",
    "sharpness_status",
    "demotion_boundary",
    "paper_claim_status",
    "closed_objection_ids",
}


def load_json(path: Path) -> dict:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        fail(f"{rel(path)} is not valid JSON: {exc}")
    if not isinstance(payload, dict):
        fail(f"{rel(path)} must contain a JSON object")
    return payload


def require_text(path: Path, fragments: list[str]) -> None:
    text = path.read_text(encoding="utf-8")
    for fragment in fragments:
        if fragment not in text:
            fail(f"{rel(path)} missing required text fragment: {fragment}")


def main() -> int:
    missing = [name for name in REQUIRED_ARTIFACTS if not (REPORT_DIR / name).is_file()]
    if missing:
        fail(f"missing closure artifacts: {', '.join(missing)}")

    json_payloads = {
        path.name: load_json(path)
        for path in REPORT_DIR.glob("*.json")
    }

    latest = json_payloads["latest.json"]
    if latest.get("status") != "implemented":
        fail("latest.json status must be implemented")
    if len(latest.get("implemented_todos", [])) != 10:
        fail("latest.json must list all 10 implemented TODO ids")
    if not isinstance(latest.get("top_paper_gate"), dict):
        fail("latest.json must record the top-paper gate result")
    narrative_weight_gate = latest["top_paper_gate"].get("narrative_weight_gate", "")
    if "cohered results criterion" not in narrative_weight_gate:
        fail("latest.json top-paper gate must name the cohered results criterion")
    if "cohered results as a criterion" not in narrative_weight_gate:
        fail("latest.json top-paper gate must treat cohered results as a criterion")
    if "fragmented ensemble of results" not in narrative_weight_gate:
        fail("latest.json top-paper gate must reject fragmented ensembles of results")
    if "flagship formula-footprint spine" not in latest["top_paper_gate"].get("coherence_pass_mode", ""):
        fail("latest.json top-paper gate must define how new results cohere with the flagship spine")
    if "novelty_delta_accounting_artifact" not in latest["top_paper_gate"]:
        fail("latest.json top-paper gate must point to the novelty-delta accounting artifact")
    if latest["top_paper_gate"].get("novelty_delta_accounting") != "integrated_in_revised_tex_as_C7_C11_before_after_shift_and_closest_literature_delta_matrix":
        fail("latest.json top-paper gate must record novelty-delta accounting integration status")
    if "closest-literature novelty delta" not in latest["top_paper_gate"].get("coherence_pass_mode", ""):
        fail("latest.json top-paper gate must require closest-literature novelty deltas")
    if latest.get("final_claim_state", {}).get("novelty_delta_accounting") != "integrated_in_revised_tex_as_C7_C11_before_after_shift":
        fail("latest.json must record novelty-delta accounting as integrated")
    if latest.get("final_claim_state", {}).get("self_auditing_rup_cdcl_instantiation") != "self_auditing_rup_cdcl_instantiation_proved":
        fail("latest.json must record the self-auditing RUP-CDCL instantiation as proved")
    if "self_auditing_rup_cdcl_instantiation" not in latest["top_paper_gate"]:
        fail("latest.json top-paper gate must record the self-auditing RUP-CDCL instantiation")
    if latest.get("final_claim_state", {}).get("append_only_self_auditing_rup_cdcl") != "append_only_self_auditing_rup_cdcl_proved":
        fail("latest.json must record the append-only self-auditing RUP-CDCL instantiation as proved")
    if "append_only_self_auditing_rup_cdcl" not in latest["top_paper_gate"]:
        fail("latest.json top-paper gate must record the append-only self-auditing RUP-CDCL instantiation")
    if latest.get("final_claim_state", {}).get("prefix_typed_append_only_rup_cdcl") != "prefix_typed_append_only_rup_cdcl_proved":
        fail("latest.json must record the prefix-typed append-only RUP-CDCL instantiation as proved")
    if "prefix_typed_append_only_rup_cdcl" not in latest["top_paper_gate"]:
        fail("latest.json top-paper gate must record the prefix-typed append-only RUP-CDCL instantiation")
    if "lose force" not in latest["top_paper_gate"].get("narrative_indivisibility_test", ""):
        fail("latest.json top-paper gate must require the narrative-indivisibility test")
    roles = latest["top_paper_gate"].get("coherence_admission_roles", [])
    if roles != ["flagship", "calibration", "interface_variant", "proof_system_bridge", "boundary"]:
        fail("latest.json top-paper gate must include the C11 coherence admission roles")
    if latest.get("artifact_count") != len(REQUIRED_ARTIFACTS):
        fail("latest.json artifact_count must match the required artifact list")

    criteria = json_payloads["top_paper_criteria.json"]
    c11 = next(
        (
            item
            for item in criteria.get("criteria", [])
            if isinstance(item, dict) and item.get("id") == "C11"
        ),
        None,
    )
    if not c11:
        fail("top_paper_criteria.json must include C11")
    if "cohered_results_as_formal_admission_criterion" not in c11.get("criterion_role", ""):
        fail("C11 must encode cohered results as a formal admission criterion")
    c11_fail_evidence = c11.get("fail_evidence", [])
    c11_pass_evidence = c11.get("pass_evidence", [])
    if not any("narrative indivisibility" in item for item in c11_pass_evidence):
        fail("C11 must include a narrative-indivisibility pass test")
    if not any("removed or reordered" in item for item in c11_fail_evidence):
        fail("C11 must include a structured fail condition for fragmented result bundles")
    if not any("ensemble of results" in item for item in c11_fail_evidence):
        fail("C11 must reject locally correct but narratively fragmented ensembles")
    if not any("separate mini-papers" in item for item in c11_fail_evidence):
        fail("C11 must reject results that split into separate mini-papers")
    if not any("technically correct" in item for item in c11_fail_evidence):
        fail("C11 must reject fragmented ensembles even when components are technically correct")
    if not any("admission criterion" in item for item in c11_pass_evidence):
        fail("C11 must treat cohered results as an admission criterion")
    c11_roles = c11.get("admission_roles", [])
    if c11_roles != ["flagship", "calibration", "interface_variant", "proof_system_bridge", "boundary"]:
        fail("C11 must define admission roles for cohered results")
    if not any("quarantine" in item for item in c11.get("admission_rule", [])):
        fail("C11 must quarantine locally correct additions that create a fragmented ensemble")

    acceptance = json_payloads["acceptance_response.json"]
    if acceptance.get("overall_decision") == "ready_for_selective_submission":
        fail("acceptance response must not mark the current theorem package ready for selective submission")
    if "remaining_blockers" not in acceptance or not acceptance["remaining_blockers"]:
        fail("acceptance response must keep explicit remaining blockers")
    if not any(
        item.get("objection") == "incomplete_literature_comparison"
        and item.get("status") == "closed_for_current_scope"
        for item in acceptance.get("responses", [])
        if isinstance(item, dict)
    ):
        fail("acceptance response must close the literature-comparison objection for the current scope")

    literature = json_payloads["literature_anchor_table.json"]
    if literature.get("citation_debt") != []:
        fail("literature anchor table must not keep stale citation debt after direct references are present")
    citation_status = literature.get("citation_status", {})
    direct_refs = set(citation_status.get("direct_references_present", []))
    expected_direct_refs = {
        "partial_mcsp_and_partial_functions",
        "circuit_test_suites_and_anti_checkers",
        "teaching_dimension_specification_dimension_and_exact_certification",
        "lower_bound_refuter_analogues",
    }
    if direct_refs != expected_direct_refs:
        fail("literature anchor table must record the direct nearest-literature references now present")
    novelty = literature.get("novelty_delta_accounting", {})
    if novelty.get("status") != "integrated_in_revised_tex":
        fail("literature anchor table must record novelty-delta accounting as integrated")
    if "completion-sound evidence" not in novelty.get("before_after_understanding_shift", ""):
        fail("literature anchor table must state the before-after understanding shift")
    if novelty.get("roles") != ["flagship", "calibration", "interface_variant", "proof_system_bridge", "boundary"]:
        fail("literature anchor table novelty accounting must use the C11 roles")

    closure = json_payloads["closure_gate_policy.json"]
    fields = set(closure.get("required_result_card_fields", []))
    if fields != REQUIRED_RESULT_CARD_FIELDS:
        fail("closure gate policy required result-card fields changed unexpectedly")

    require_text(
        REPORT_DIR / "batched_dictionary_repair.tex",
        ["query records", "dictionary records", "masked out", "symmetric"],
    )
    require_text(
        REPORT_DIR / "claim_reset_plan.md",
        ["Structured Certificate Lower Bounds", "Theorem-Status Table"],
    )
    require_text(
        REPORT_DIR / "acceptance_response.md",
        [
            "not_ready_for_selective_submission",
            "Remaining Blockers",
            "closed_for_current_scope",
            "current nearest-literature citation debt is resolved",
        ],
    )
    require_text(
        REPORT_DIR / "literature_anchor_table.md",
        [
            "Citation Status",
            "direct references",
            "Hirahara, FOCS 2022",
            "Chapman and Williams, ITCS 2015",
            "Anthony--Brightwell--Cohen--Shawe-Taylor, COLT 1992",
            "Doliwa--Fan--Simon--Zilles, JMLR 2014",
            "Remaining bibliography work is style-level only",
            "Novelty Delta Accounting",
            "Before/after understanding shift",
            "completion-sound evidence",
        ],
    )
    require_text(
        REPORT_DIR / "novelty_delta_accounting.md",
        [
            "Novelty Delta Matrix",
            "closest established object",
            "before/after understanding shift",
            "flagship formula-footprint arc",
            "Completion-sound evidence that a generated labeling is hard",
            "fragmented ensemble",
        ],
    )
    require_text(
        REPORT_DIR / "top_paper_criteria.md",
        [
            "C1. One-Line Theorem Identity",
            "C5. Standard-Model Or Extraction Payoff",
            "C11. Cohered Results Criterion: One Sharp, Novel, Weighty Result Package",
            "cohered results as a criterion",
            "Fail evidence:",
            "fragmented ensemble of results",
            "A paper that merely accumulates locally correct results still fails C11",
            "cohered result arc",
            "narrative-indivisibility test",
            "not a fragmented ensemble of results",
            "one recognizable before/after theorem arc",
            "Operational admission rule",
            "flagship, calibration, interface variant, proof-system bridge, or boundary",
        ],
    )
    require_text(
        REPORT_DIR / "cohered_result_spine.md",
        [
            "operational admission test",
            "Cohered results are a criterion for admission",
            "fragmented ensemble of results",
            "flagship, calibration, interface variant, proof-system bridge, or boundary",
            "before/after understanding shift",
            "Why would the result lose force",
            "one recognizable result arc",
            "antecedent-complete CDCL learned-clause normalizer",
            "prefix-typed append-only RUP-CDCL instantiation",
            "not top-ready",
        ],
    )
    require_text(
        REPORT_DIR / "publication_level_gap_audit.md",
        [
            "strong_preprint_not_top_ready",
            "pass_for_union_footprint",
            "Default next action",
            "C11 cohered results criterion",
            "C1 one-line theorem identity | `pass`",
            "pass_for_support_audited_and_provenance_typed_lrat_not_plain_arbitrary_proof_systems",
            "C8 proof auditability | `pass_for_current_theorem_package`",
            "C7 literature closure | `pass_for_current_scope_with_novelty_delta_accounting`",
            "novelty-delta accounting",
            "before/after understanding-shift matrix",
            "closest-literature delta",
            "Self-Auditing RUP-CDCL Update",
            "self_auditing_rup_cdcl_instantiation.md",
            "append_only_self_auditing_rup_cdcl.md",
            "prefix_typed_append_only_rup_cdcl.md",
            "prefix_typed_rup_support_witness_necessity.md",
            "supply an intrinsic support-locality invariant",
            "A fragmented ensemble of results is not a path to top-paper status",
            "narrative-indivisibility test",
            "C11 cohered results criterion",
            "cohered_result_spine.md",
            "not another fragmented result",
            "positive non-plain CDCL",
            "assumption-resolution theorem gives a restricted named resolution instantiation",
            "unit-core corollary lower-bounds faithful label-unit leaves",
            "local-clause theorem lower-bounds faithful formula-label support",
            "support-local auxiliary theorem handles mixed auxiliary clauses",
            "support-local extension-resolution theorem handles acyclic extension definitions",
            "dependency-cone extension normalizer extracts a support budget",
            "canonical syntactic-cone corollary extracts the same support directly",
            "final backward-slice corollary turns that support into a visible proof-object budget",
            "slice-explicit ER corollary turns the visible budget into a restricted ER-style proof-size lower bound",
            "displayed acyclic ER corollary removes the special slice-size convention",
            "expansion-bounded compressed ER corollary turns this into a decompression-budget tradeoff",
            "macro-compressed ER corollary turns ordinary macro sharing into a skeleton-plus-reuse tradeoff",
            "support-declared macro ER corollary turns any sound macro support summary into a near-threshold support-budget lower bound",
            "support-audited LRAT corollary turns any checker-visible support audit into the same near-threshold budget lower bound",
            "provenance-typed LRAT corollary proves that trusted variable roles and block-local provenance supply such an audit",
            "namespace-typed LRAT theorem closes the lighter reserved-label-namespace plus antecedent-closure route",
            "strict-prefix Qrep replay proposition turns quotient representative reuse into an already-charged same-theory replay condition",
            "trace-complete DPLL",
            "antecedent-complete CDCL",
            "CDCL antecedent-erasure trichotomy",
            "support-audit necessity separator shows why checked clausal unsatisfiability alone does not certify completion-local support",
            "support-erasure separator shows why untyped LRAT syntax does not determine formula-label support without provenance",
            "plain LRAT extraction trichotomy",
            "semantic-relation support certificate",
            "cone-budget corollary turns that support budget into a final-interface-size versus cone-size tradeoff",
            "bounded-depth corollary turns cone size into a bounded-fanin depth versus final-interface-size tradeoff",
            "support-local normalization transfer theorem converts any controlled support-local normalizer",
        ],
    )
    require_text(
        REPORT_DIR / "structured_certificate_lower_bounds_revision.tex",
        [
            "The Formula-Footprint Barrier",
            "Conceptual spine: one obstruction in three interfaces",
            "Claim status after the referee-objection closure pass",
            "Nearest-work comparison and novelty boundary",
            "Novelty accounting and narrative cohesion",
            "Novelty-delta accounting for the cohered result package",
            "completion-sound evidence that a generated labeling is hard must either",
            "proof-complexity applications require an auditable extractor",
            "query-record separation is required in all cases",
            "Accepting-query union is a certificate",
            "Displayed-atom extraction",
            "Generic sharpness in the identity carrier",
            "Nondeterministic formula-query decision-tree lower bound",
            "Proof dependency and audit map",
            "Proof dependency and audit map.  Every theorem-level claim",
            "The normalization target for proof-system applications",
            "Normalization targets for proof-system applications",
            "Resolution with explicit label assumptions",
            "Resolution unit-core lower bound",
            "Resolution local-clause support",
            "Support-local auxiliary resolution",
            "Support-local extension resolution",
            "Dependency-cone extension normalizer",
            "Canonical syntactic-cone normalizer",
            "Final backward-slice lower bound",
            "Slice-explicit extension-resolution lower bound",
            "Displayed acyclic ER length lower bound",
            "Expansion-bounded compressed ER transfer",
            "Macro-compressed ER reuse tradeoff",
            "Support-declared macro ER normalizer",
            "Support-audited LRAT trace normalizer",
            "Provenance-typed LRAT support audit",
            "cor:provenance-typed-lrat",
            "typed roles, block-local supports, and compatible witnesses do supply the support audit",
            "Namespace-typed LRAT antecedent-closure normalizer",
            "cor:namespace-typed-lrat",
            "LRAT antecedent closure of the final empty clause",
            "trusted formula-label namespace",
            "Support-audit necessity separator",
            "prop:support-audit-necessity",
            "Support-erasure indistinguishability separator",
            "prop:support-erasure-indistinguishability",
            "untyped LRAT syntax does not determine whether a variable is auxiliary or label support",
            "Plain LRAT extraction trichotomy",
            "prop:plain-lrat-extraction-trichotomy",
            "add provenance, pay role-agnostic worst-case support, or fail on a same-skeleton semantic lift",
            "Semantic-relation support certificate",
            "prop:semantic-relation-support",
            "ordinary membership certificate for each relation instance",
            "Acyclic OR-tree residual certificate",
            "prop:acyclic-or-tree-residual",
            "root \\(0\\) forces the root and all frontier leaves",
            "OR-DAG frontier residual certificate",
            "prop:or-dag-frontier-residual",
            "distinct reachable frontier class",
            "Acyclic Boolean frontier residual certificate",
            "prop:acyclic-boolean-frontier-residual",
            "support-locality is exactly the root coordinate plus an ordinary pointwise Boolean certificate",
            "Visible adaptive frontier residual certificate",
            "prop:visible-adaptive-frontier-residual",
            "the actual transcript path is sufficient support",
            "Visible adaptive branching-program frontier residual certificate",
            "prop:visible-adaptive-branching-frontier-residual",
            "the actual computation path is sufficient support",
            "Hidden adaptive transcript insufficiency",
            "prop:hidden-adaptive-transcript-insufficiency",
            "transcript-only support extraction is therefore unsound",
            "Controller-complete adaptive audit normalizer",
            "prop:controller-complete-adaptive-audit-normalizer",
            "local controller equivalence",
            "proof object paying for controller completeness",
            "Trace-complete DPLL log normalizer",
            "cor:trace-complete-dpll",
            "complete finite controller",
            "local clause or propagation witnesses",
            "Antecedent-complete CDCL normalizer",
            "CDCL antecedent-erasure trichotomy",
            "RUP-complete CDCL support normalizer",
            "Canonical-namespace RUP-CDCL standardizer",
            "Carrier-independent audit upgrade criterion",
            "cor:carrier-independent-audit-upgrade",
            "proof-system-intrinsic audit extractor",
            "without a carrier-specific manifest",
            "Self-auditing RUP-CDCL instantiation",
            "cor:self-auditing-rup-cdcl",
            "checked label decoder",
            "live-database reconstruction",
            "retained deleted-clause support",
            "proof object itself",
            "Append-only self-auditing RUP-CDCL",
            "cor:append-only-self-auditing-rup-cdcl",
            "append-only clause-addition log",
            "retained deleted-clause support records",
            "monotone clause database",
            "Prefix-typed append-only RUP-CDCL",
            "cor:prefix-typed-append-only-rup-cdcl",
            "public formula-label variable namespace",
            "no proof-internal label decoder",
            "Support-local witnesses are necessary for prefix-typed append-only RUP-CDCL",
            "prop:prefix-typed-rup-support-witness-necessity",
            "append-only RUP checking plus public",
            "equivalent intrinsic invariant",
            "cor:antecedent-complete-cdcl",
            "prop:cdcl-antecedent-erasure-trichotomy",
            "cor:rup-complete-cdcl",
            "cor:canonical-namespace-rup-cdcl",
            "acyclic antecedent DAG",
            "hidden learned-clause provenance",
            "provenance-free CDCL syntax is not a free normalizer",
            "checker-visible RUP propagation certificate",
            "known live clause database",
            "retained deleted-clause support",
            "reserved label-variable interval",
            "deterministic encoding manifest",
            "checked clausal unsatisfiability alone does not certify completion-local support",
            "Cone-budget extension lower bound",
            "Bounded-depth extension tradeoff",
            "Support-local normalization with support budget",
            "Support-local normalization transfer",
            "Easy-completion CNF",
            "Resolution support-local bridge",
            "Support-local normalization transfer",
            "Support-declared macro ER normalizer",
            "Support-audited LRAT trace normalizer",
            "Strict-prefix Qrep replay normalizer",
            "prop:strict-prefix-qrep",
            "quotient representatives replay from already charged same-theory forests",
            "Two-line prefix scan for Qrep",
            "certificate\\_not\\_strict\\_prefix",
            "The admission rule is that every result must play one of five roles",
            "fragmented ensemble of results",
            "Full-assignment resolution unit core",
            "Local resolution clauses",
            "Support-local auxiliary resolution",
            "Support-local extension resolution",
            "Dependency-cone extension normalizer",
            "Cone-budget extension lower bound",
            "Bounded-depth extension tradeoff",
        ],
    )
    randomized_packet = json_payloads.get("randomized_accepting_union_theorem.json", {})
    if randomized_packet.get("status") != "proved_in_revised_tex":
        fail("randomized accepting-union theorem packet must be proved_in_revised_tex")
    identity_packet = json_payloads.get("identity_carrier_generic_sharpness.json", {})
    if identity_packet.get("status") != "proved_in_revised_tex":
        fail("identity-carrier generic sharpness packet must be proved_in_revised_tex")
    dependency_packet = json_payloads.get("proof_dependency_audit_map.json", {})
    if dependency_packet.get("status") != "integrated_in_revised_tex":
        fail("proof dependency audit map packet must be integrated_in_revised_tex")
    normalization_packet = json_payloads.get("proof_system_normalization_target.json", {})
    if normalization_packet.get("status") != "integrated_in_revised_tex":
        fail("proof-system normalization target packet must be integrated_in_revised_tex")
    assumption_resolution_packet = json_payloads.get("assumption_resolution_instantiation.json", {})
    if assumption_resolution_packet.get("status") != "proved_in_revised_tex":
        fail("assumption-resolution instantiation packet must be proved_in_revised_tex")
    if assumption_resolution_packet.get("theorem_summary", {}).get("proof_system") != "resolution":
        fail("assumption-resolution packet must record resolution as the proof system")
    unit_core_packet = json_payloads.get("resolution_unit_core_lower_bound.json", {})
    if unit_core_packet.get("status") != "proved_in_revised_tex":
        fail("resolution unit-core packet must be proved_in_revised_tex")
    if unit_core_packet.get("theorem_summary", {}).get("measured_object") != "distinct faithful formula-label unit leaves used by the refutation":
        fail("resolution unit-core packet must record the measured proof object")
    local_clause_packet = json_payloads.get("resolution_local_clause_support.json", {})
    if local_clause_packet.get("status") != "proved_in_revised_tex":
        fail("resolution local-clause support packet must be proved_in_revised_tex")
    if local_clause_packet.get("theorem_summary", {}).get("measured_object") != "distinct formula-label variables occurring in faithful local clauses":
        fail("resolution local-clause packet must record the measured proof object")
    support_local_packet = json_payloads.get("support_local_auxiliary_resolution.json", {})
    if support_local_packet.get("status") != "proved_in_revised_tex":
        fail("support-local auxiliary resolution packet must be proved_in_revised_tex")
    if support_local_packet.get("theorem_summary", {}).get("measured_object") != "label support whose agreement preserves satisfiability of auxiliary constraints under all completions":
        fail("support-local auxiliary resolution packet must record the measured proof object")
    extension_packet = json_payloads.get("support_local_extension_resolution.json", {})
    if extension_packet.get("status") != "proved_in_revised_tex":
        fail("support-local extension resolution packet must be proved_in_revised_tex")
    if extension_packet.get("theorem_summary", {}).get("measured_object") != "fixed formula-label support driving acyclic extension definitions and final extension clauses":
        fail("support-local extension resolution packet must record the measured proof object")
    if "unrestricted_extended_resolution_lower_bound" not in extension_packet.get("boundary", {}).get("does_not_prove", []):
        fail("support-local extension resolution packet must preserve the unrestricted-ER nonclaim boundary")
    cone_packet = json_payloads.get("dependency_cone_extension_normalizer.json", {})
    if cone_packet.get("status") != "proved_in_revised_tex":
        fail("dependency-cone extension normalizer packet must be proved_in_revised_tex")
    if cone_packet.get("theorem_summary", {}).get("measured_object") != "union of declared formula-label dependency cones for final extension contradiction":
        fail("dependency-cone extension normalizer packet must record the measured proof object")
    if "normalizer_for_hidden_nonlocal_extension_variables" not in cone_packet.get("boundary", {}).get("does_not_prove", []):
        fail("dependency-cone extension normalizer packet must preserve the hidden-nonlocal-extension nonclaim boundary")
    canonical_cone_packet = json_payloads.get("canonical_syntactic_cone_normalizer.json", {})
    if canonical_cone_packet.get("status") != "proved_in_revised_tex":
        fail("canonical syntactic-cone normalizer packet must be proved_in_revised_tex")
    if canonical_cone_packet.get("theorem_summary", {}).get("measured_object") != "union of formula-label inputs reachable from variables in the final CNF":
        fail("canonical syntactic-cone packet must record the measured proof object")
    if "unrestricted_extended_resolution_lower_bound" not in canonical_cone_packet.get("nonclaims", []):
        fail("canonical syntactic-cone packet must preserve the unrestricted-ER nonclaim boundary")
    backward_slice_packet = json_payloads.get("final_backward_slice_lower_bound.json", {})
    if backward_slice_packet.get("status") != "proved_in_revised_tex":
        fail("final backward-slice lower-bound packet must be proved_in_revised_tex")
    if backward_slice_packet.get("theorem_summary", {}).get("measured_object") != "distinct formula-label inputs in the final backward slice":
        fail("final backward-slice packet must record the measured proof object")
    if "unrestricted_extended_resolution_lower_bound" not in backward_slice_packet.get("nonclaims", []):
        fail("final backward-slice packet must preserve the unrestricted-ER nonclaim boundary")
    slice_explicit_packet = json_payloads.get("slice_explicit_er_lower_bound.json", {})
    if slice_explicit_packet.get("status") != "proved_in_revised_tex":
        fail("slice-explicit ER lower-bound packet must be proved_in_revised_tex")
    if slice_explicit_packet.get("theorem_summary", {}).get("measured_object") != "proof-size measure charging distinct formula-label inputs in the final backward slice":
        fail("slice-explicit ER packet must record the measured proof object")
    if "proof_size_lower_bound_without_slice_boundary_charging" not in slice_explicit_packet.get("nonclaims", []):
        fail("slice-explicit ER packet must preserve the slice-charging nonclaim boundary")
    displayed_er_packet = json_payloads.get("displayed_acyclic_er_length_lower_bound.json", {})
    if displayed_er_packet.get("status") != "proved_in_revised_tex":
        fail("displayed acyclic ER length packet must be proved_in_revised_tex")
    if displayed_er_packet.get("theorem_summary", {}).get("measured_object") != "ordinary displayed literal length of extension definitions final clauses and resolution derivation":
        fail("displayed acyclic ER packet must record the measured proof object")
    if "compressed_proof_lower_bound" not in displayed_er_packet.get("nonclaims", []):
        fail("displayed acyclic ER packet must preserve the compressed-proof nonclaim boundary")
    compressed_er_packet = json_payloads.get("compressed_er_expansion_transfer.json", {})
    if compressed_er_packet.get("status") != "proved_in_revised_tex":
        fail("compressed ER expansion-transfer packet must be proved_in_revised_tex")
    if compressed_er_packet.get("theorem_summary", {}).get("measured_object") != "decompression budget B(|rho|) controlling displayed acyclic ER expansion length":
        fail("compressed ER expansion-transfer packet must record the measured proof object")
    if "arbitrary_compressed_proof_lower_bound" not in compressed_er_packet.get("nonclaims", []):
        fail("compressed ER expansion-transfer packet must preserve the arbitrary-compression nonclaim boundary")
    macro_er_packet = json_payloads.get("macro_compressed_er_reuse_tradeoff.json", {})
    if macro_er_packet.get("status") != "proved_in_revised_tex":
        fail("macro-compressed ER reuse-tradeoff packet must be proved_in_revised_tex")
    if macro_er_packet.get("theorem_summary", {}).get("measured_object") != "displayed skeleton length S plus macro invocation count r times macro-library length D":
        fail("macro-compressed ER packet must record the measured proof object")
    if "lower_bound_for_macros_with_nonlocal_semantics" not in macro_er_packet.get("nonclaims", []):
        fail("macro-compressed ER packet must preserve the nonlocal-macro nonclaim boundary")
    support_declared_macro_packet = json_payloads.get("support_declared_macro_er_normalizer.json", {})
    if support_declared_macro_packet.get("status") != "proved_in_revised_tex":
        fail("support-declared macro ER packet must be proved_in_revised_tex")
    if support_declared_macro_packet.get("theorem_summary", {}).get("measured_object") != "union of declared formula-label supports in the final macro support declaration":
        fail("support-declared macro ER packet must record the measured proof object")
    if "lower_bound_for_macros_with_unsound_or_hidden_nonlocal_support" not in support_declared_macro_packet.get("nonclaims", []):
        fail("support-declared macro ER packet must preserve the hidden-nonlocal-support nonclaim boundary")
    support_audited_lrat_packet = json_payloads.get("support_audited_lrat_trace_normalizer.json", {})
    if support_audited_lrat_packet.get("status") != "proved_in_revised_tex":
        fail("support-audited LRAT packet must be proved_in_revised_tex")
    if support_audited_lrat_packet.get("theorem_summary", {}).get("measured_object") != "union of declared formula-label supports audited by the LRAT trace":
        fail("support-audited LRAT packet must record the measured proof object")
    if "lower_bound_for_lrat_without_sound_support_audit" not in support_audited_lrat_packet.get("nonclaims", []):
        fail("support-audited LRAT packet must preserve the unaudited-LRAT nonclaim boundary")
    provenance_typed_lrat_packet = json_payloads.get("provenance_typed_lrat_support_audit.json", {})
    if provenance_typed_lrat_packet.get("status") != "proved_in_revised_tex":
        fail("provenance-typed LRAT packet must be proved_in_revised_tex")
    if provenance_typed_lrat_packet.get("theorem_summary", {}).get("measured_object") != "union of block-local formula-label provenance supports certified by a typed LRAT provenance package":
        fail("provenance-typed LRAT packet must record the measured proof object")
    if "support_extraction_from_untyped_lrat_syntax" not in provenance_typed_lrat_packet.get("nonclaims", []):
        fail("provenance-typed LRAT packet must preserve the raw/untyped LRAT nonclaim boundary")
    if latest["final_claim_state"].get("provenance_typed_lrat_support_audit") != "trusted_typed_provenance_supplies_support_audit_proved":
        fail("latest.json must record the provenance-typed LRAT support audit")
    namespace_lrat_packet = json_payloads.get("namespace_typed_lrat_antecedent_closure_normalizer.json", {})
    if namespace_lrat_packet.get("status") != "proved_in_revised_tex":
        fail("namespace-typed LRAT packet must be proved_in_revised_tex")
    if namespace_lrat_packet.get("theorem_summary", {}).get("measured_object") != "formula-label variables occurring in original auxiliary clauses in the LRAT antecedent closure of the empty clause":
        fail("namespace-typed LRAT packet must record the measured proof object")
    if "support_extraction_after_erasing_formula_label_namespace" not in namespace_lrat_packet.get("nonclaims", []):
        fail("namespace-typed LRAT packet must preserve the erased-namespace nonclaim")
    if "restrict_the_trace_to_the_LRAT_antecedent_closure_of_the_empty_clause" not in namespace_lrat_packet.get("proof_skeleton", []):
        fail("namespace-typed LRAT packet must record antecedent-closure restriction")
    if latest["final_claim_state"].get("namespace_typed_lrat_antecedent_closure_normalizer") != "trusted_namespace_and_lrat_antecedent_closure_supplies_support_audit_proved":
        fail("latest.json must record the namespace-typed LRAT support audit")
    support_audit_separator_packet = json_payloads.get("support_audit_necessity_separator.json", {})
    if support_audit_separator_packet.get("status") != "proved_in_revised_tex":
        fail("support-audit necessity separator packet must be proved_in_revised_tex")
    if support_audit_separator_packet.get("theorem_summary", {}).get("measured_object") != "minimum sound support declaration for a clausal constraint package that fixes a finite label set":
        fail("support-audit necessity separator packet must record the measured proof object")
    if "lower_bound_for_arbitrary_lrat" not in support_audit_separator_packet.get("nonclaims", []):
        fail("support-audit necessity separator must preserve the arbitrary-LRAT nonclaim boundary")
    if latest["final_claim_state"].get("support_audit_necessity_separator") != "proved_boundary_unsat_checking_does_not_imply_support_locality":
        fail("latest.json must record the support-audit necessity separator")
    support_erasure_packet = json_payloads.get("support_erasure_indistinguishability_separator.json", {})
    if support_erasure_packet.get("status") != "proved_in_revised_tex":
        fail("support-erasure indistinguishability separator packet must be proved_in_revised_tex")
    if support_erasure_packet.get("theorem_summary", {}).get("measured_object") != "semantic formula-label support determined by variable-role provenance rather than by an untyped LRAT skeleton":
        fail("support-erasure separator packet must record the measured proof object")
    if "impossibility_of_support_extraction_with_trusted_variable_roles" not in support_erasure_packet.get("nonclaims", []):
        fail("support-erasure separator must preserve the trusted-variable-role nonclaim boundary")
    if latest["final_claim_state"].get("support_erasure_indistinguishability_separator") != "proved_boundary_untyped_lrat_syntax_does_not_determine_support":
        fail("latest.json must record the support-erasure indistinguishability separator")
    plain_lrat_packet = json_payloads.get("plain_lrat_extraction_trichotomy.json", {})
    if plain_lrat_packet.get("status") != "proved_in_revised_tex":
        fail("plain LRAT extraction trichotomy packet must be proved_in_revised_tex")
    if plain_lrat_packet.get("theorem_summary", {}).get("measured_object") != "support set output by an extractor that sees only untyped clauses and LRAT antecedent hints":
        fail("plain LRAT trichotomy packet must record the measured proof object")
    if "impossibility_of_provenance_typed_lrat_support_audits" not in plain_lrat_packet.get("nonclaims", []):
        fail("plain LRAT trichotomy must preserve the provenance-typed LRAT nonclaim boundary")
    if latest["final_claim_state"].get("plain_lrat_extraction_trichotomy") != "proved_boundary_plain_trace_extraction_requires_provenance_or_worst_case_support":
        fail("latest.json must record the plain LRAT extraction trichotomy")
    semantic_relation_packet = json_payloads.get("semantic_relation_support_certificate.json", {})
    if semantic_relation_packet.get("status") != "proved_in_revised_tex":
        fail("semantic-relation support packet must be proved_in_revised_tex")
    if semantic_relation_packet.get("theorem_summary", {}).get("measured_object") != "declared support coordinates inside the scope of a nonlinear semantic relation":
        fail("semantic-relation support packet must record the measured proof object")
    if semantic_relation_packet.get("sat_self_reduction_example", {}).get("satisfying_tuple_costs", {}).get("000") != 3:
        fail("semantic-relation support packet must record the OR self-reduction 000 cost")
    if "full_sat_self_reduction_residual_completion_theorem" not in semantic_relation_packet.get("nonclaims", []):
        fail("semantic-relation support packet must preserve the global SAT residual-completion nonclaim")
    if latest["final_claim_state"].get("semantic_relation_support_certificate") != "proved_local_nonlinear_relation_support_boundary":
        fail("latest.json must record the semantic-relation support certificate")
    acyclic_or_packet = json_payloads.get("acyclic_or_tree_residual_certificate.json", {})
    if acyclic_or_packet.get("status") != "proved_in_revised_tex":
        fail("acyclic OR-tree residual packet must be proved_in_revised_tex")
    if acyclic_or_packet.get("theorem_summary", {}).get("measured_object") != "support coordinates for the root and frontier leaves of an acyclic OR self-reduction tree":
        fail("acyclic OR-tree residual packet must record the measured proof object")
    if acyclic_or_packet.get("certificate_costs", {}).get("root_zero") != "1_plus_number_of_frontier_leaves":
        fail("acyclic OR-tree residual packet must record the root-zero frontier cost")
    if "full_sat_self_reduction_residual_completion_theorem" not in acyclic_or_packet.get("nonclaims", []):
        fail("acyclic OR-tree residual packet must preserve the full SAT residual-completion nonclaim")
    if latest["final_claim_state"].get("acyclic_or_tree_residual_certificate") != "proved_bounded_global_or_frontier_certificate":
        fail("latest.json must record the acyclic OR-tree residual certificate")
    or_dag_packet = json_payloads.get("or_dag_frontier_residual_certificate.json", {})
    if or_dag_packet.get("status") != "proved_in_revised_tex":
        fail("OR-DAG frontier residual packet must be proved_in_revised_tex")
    if or_dag_packet.get("theorem_summary", {}).get("measured_object") != "support coordinates for the root and distinct reachable quotient-frontier classes of an acyclic OR DAG":
        fail("OR-DAG frontier residual packet must record the measured proof object")
    if or_dag_packet.get("certificate_costs", {}).get("root_zero") != "1_plus_number_of_distinct_reachable_frontier_classes":
        fail("OR-DAG frontier residual packet must record the root-zero frontier cost")
    if "full_sat_self_reduction_residual_completion_theorem" not in or_dag_packet.get("nonclaims", []):
        fail("OR-DAG frontier residual packet must preserve the full SAT residual-completion nonclaim")
    if latest["final_claim_state"].get("or_dag_frontier_residual_certificate") != "proved_bounded_shared_or_frontier_certificate":
        fail("latest.json must record the OR-DAG frontier residual certificate")
    acyclic_bool_packet = json_payloads.get("acyclic_boolean_frontier_residual_certificate.json", {})
    if acyclic_bool_packet.get("status") != "proved_in_revised_tex":
        fail("acyclic Boolean frontier residual packet must be proved_in_revised_tex")
    if acyclic_bool_packet.get("theorem_summary", {}).get("measured_object") != "root coordinate plus a pointwise Boolean certificate for the exposed acyclic frontier circuit":
        fail("acyclic Boolean frontier packet must record the measured proof object")
    if "hidden_semantic_proof_system_lower_bound" not in acyclic_bool_packet.get("nonclaims", []):
        fail("acyclic Boolean frontier packet must preserve the hidden semantic proof-system nonclaim")
    if latest["final_claim_state"].get("acyclic_boolean_frontier_residual_certificate") != "proved_exposed_acyclic_boolean_frontier_certificate_complexity_boundary":
        fail("latest.json must record the acyclic Boolean frontier residual certificate")
    visible_adaptive_packet = json_payloads.get("visible_adaptive_frontier_residual_certificate.json", {})
    if visible_adaptive_packet.get("status") != "proved_in_revised_tex":
        fail("visible adaptive frontier residual packet must be proved_in_revised_tex")
    if visible_adaptive_packet.get("theorem_summary", {}).get("measured_object") != "root coordinate plus a pointwise Boolean certificate for the exposed adaptive frontier decision tree":
        fail("visible adaptive frontier packet must record the measured proof object")
    if "hidden_adaptive_sat_self_reduction_invariant" not in visible_adaptive_packet.get("nonclaims", []):
        fail("visible adaptive frontier packet must preserve the hidden adaptive semantic nonclaim")
    if visible_adaptive_packet.get("certificate_costs", {}).get("transcript_path") != "sufficient_but_not_always_minimum":
        fail("visible adaptive frontier packet must record the transcript path support boundary")
    if latest["final_claim_state"].get("visible_adaptive_frontier_residual_certificate") != "proved_checker_visible_adaptive_frontier_certificate_complexity_boundary":
        fail("latest.json must record the visible adaptive frontier residual certificate")
    branching_adaptive_packet = json_payloads.get("visible_adaptive_branching_frontier_residual_certificate.json", {})
    if branching_adaptive_packet.get("status") != "proved_in_revised_tex":
        fail("visible adaptive branching frontier residual packet must be proved_in_revised_tex")
    if branching_adaptive_packet.get("theorem_summary", {}).get("measured_object") != "root coordinate plus a pointwise Boolean certificate for the exposed adaptive frontier branching program":
        fail("visible adaptive branching frontier packet must record the measured proof object")
    if "hidden_adaptive_sat_self_reduction_invariant" not in branching_adaptive_packet.get("nonclaims", []):
        fail("visible adaptive branching frontier packet must preserve the hidden adaptive semantic nonclaim")
    if branching_adaptive_packet.get("certificate_costs", {}).get("computation_path") != "sufficient_but_not_always_minimum":
        fail("visible adaptive branching frontier packet must record the computation path support boundary")
    if latest["final_claim_state"].get("visible_adaptive_branching_frontier_residual_certificate") != "proved_checker_visible_adaptive_branching_frontier_certificate_complexity_boundary":
        fail("latest.json must record the visible adaptive branching frontier residual certificate")
    hidden_transcript_packet = json_payloads.get("hidden_adaptive_transcript_insufficiency_separator.json", {})
    if hidden_transcript_packet.get("status") != "proved_in_revised_tex":
        fail("hidden adaptive transcript insufficiency packet must be proved_in_revised_tex")
    if hidden_transcript_packet.get("theorem_summary", {}).get("measured_object") != "support set output by an extractor that sees only an uncertified adaptive transcript summary":
        fail("hidden adaptive transcript packet must record the measured proof object")
    if hidden_transcript_packet.get("certificate_costs", {}).get("all_support_relation") != "1_plus_all_m_frontier_coordinates":
        fail("hidden adaptive transcript packet must record the all-frontier OR support cost")
    if "hidden_adaptive_sat_self_reduction_invariant" not in hidden_transcript_packet.get("nonclaims", []):
        fail("hidden adaptive transcript packet must preserve the hidden adaptive semantic nonclaim")
    if latest["final_claim_state"].get("hidden_adaptive_transcript_insufficiency_separator") != "proved_boundary_transcript_only_hidden_adaptive_extraction_is_unsound":
        fail("latest.json must record the hidden adaptive transcript insufficiency separator")
    controller_audit_packet = json_payloads.get("controller_complete_adaptive_audit_normalizer.json", {})
    if controller_audit_packet.get("status") != "proved_in_revised_tex":
        fail("controller-complete adaptive audit packet must be proved_in_revised_tex")
    if controller_audit_packet.get("theorem_summary", {}).get("measured_object") != "controller-complete adaptive audit exposing an acyclic branching controller, replay path, and local equivalence certificate":
        fail("controller-complete adaptive audit packet must record the measured proof object")
    if "local_equivalence_certificate_between_hidden_controller_and_exposed_controller_on_the_completion_cylinder" not in controller_audit_packet.get("audit_requirements", []):
        fail("controller-complete adaptive audit packet must require local equivalence")
    if controller_audit_packet.get("certificate_costs", {}).get("local_audit") != "root_plus_audited_path_coordinates_sufficient":
        fail("controller-complete adaptive audit packet must record the local path support cost")
    if "support_extraction_from_transcript_summary_without_controller_completeness" not in controller_audit_packet.get("nonclaims", []):
        fail("controller-complete adaptive audit packet must preserve the transcript-only nonclaim")
    if latest["final_claim_state"].get("controller_complete_adaptive_audit_normalizer") != "proved_positive_audited_hidden_adaptive_normalizer_condition":
        fail("latest.json must record the controller-complete adaptive audit normalizer")
    trace_complete_dpll_packet = json_payloads.get("trace_complete_dpll_decision_log_normalizer.json", {})
    if trace_complete_dpll_packet.get("status") != "proved_in_revised_tex":
        fail("trace-complete DPLL packet must be proved_in_revised_tex")
    if trace_complete_dpll_packet.get("theorem_summary", {}).get("measured_object") != "trace-complete DPLL decision log exposing the full acyclic controller, replay path, and local clause or propagation witnesses":
        fail("trace-complete DPLL packet must record the measured proof object")
    if "finite_acyclic_dpll_decision_controller" not in trace_complete_dpll_packet.get("audit_requirements", []):
        fail("trace-complete DPLL packet must require the full finite controller")
    if "support_extraction_from_partial_solver_transcripts" not in trace_complete_dpll_packet.get("nonclaims", []):
        fail("trace-complete DPLL packet must preserve the partial-transcript nonclaim")
    if "apply_controller_complete_adaptive_audit_normalizer" not in trace_complete_dpll_packet.get("proof_skeleton", []):
        fail("trace-complete DPLL packet must reduce to the controller-complete audit")
    if latest["final_claim_state"].get("trace_complete_dpll_decision_log_normalizer") != "trace_complete_dpll_controller_log_normalizer_proved":
        fail("latest.json must record the trace-complete DPLL decision-log normalizer")
    antecedent_cdcl_packet = json_payloads.get("antecedent_complete_cdcl_learned_clause_normalizer.json", {})
    if antecedent_cdcl_packet.get("status") != "proved_in_revised_tex":
        fail("antecedent-complete CDCL packet must be proved_in_revised_tex")
    if antecedent_cdcl_packet.get("theorem_summary", {}).get("measured_object") != "antecedent-complete CDCL log exposing used learned-clause antecedent DAGs down to audited local support":
        fail("antecedent-complete CDCL packet must record the measured proof object")
    if "acyclic_antecedent_DAG_for_every_used_learned_clause" not in antecedent_cdcl_packet.get("audit_requirements", []):
        fail("antecedent-complete CDCL packet must require acyclic learned-clause antecedent DAGs")
    if "arbitrary_cdcl_lower_bound" not in antecedent_cdcl_packet.get("nonclaims", []):
        fail("antecedent-complete CDCL packet must preserve the arbitrary-CDCL nonclaim")
    if "apply_controller_complete_adaptive_audit_normalizer" not in antecedent_cdcl_packet.get("proof_skeleton", []):
        fail("antecedent-complete CDCL packet must reduce to the controller-complete audit")
    if latest["final_claim_state"].get("antecedent_complete_cdcl_learned_clause_normalizer") != "antecedent_complete_cdcl_learned_clause_normalizer_proved":
        fail("latest.json must record the antecedent-complete CDCL learned-clause normalizer")
    cdcl_erasure_packet = json_payloads.get("cdcl_antecedent_erasure_trichotomy.json", {})
    if cdcl_erasure_packet.get("status") != "proved_in_revised_tex":
        fail("CDCL antecedent-erasure trichotomy packet must be proved_in_revised_tex")
    if cdcl_erasure_packet.get("theorem_summary", {}).get("measured_object") != "support set output by an extractor that sees only an antecedent-erased CDCL learned-clause skeleton":
        fail("CDCL antecedent-erasure trichotomy packet must record the measured proof object")
    if "add_learned_clause_antecedent_provenance_role_map_namespace_or_semantic_invariant" not in cdcl_erasure_packet.get("trichotomy", []):
        fail("CDCL antecedent-erasure trichotomy must include the provenance/non-plain-invariant branch")
    if "pay_role_agnostic_support_for_all_possible_label_lifts" not in cdcl_erasure_packet.get("trichotomy", []):
        fail("CDCL antecedent-erasure trichotomy must include the conservative-support branch")
    if "be_unsound_on_same_skeleton_label_lift" not in cdcl_erasure_packet.get("trichotomy", []):
        fail("CDCL antecedent-erasure trichotomy must include the unsoundness branch")
    if "support_extraction_from_provenance_free_learned_clauses" not in cdcl_erasure_packet.get("nonclaims", []):
        fail("CDCL antecedent-erasure trichotomy must preserve the provenance-free learned-clause nonclaim")
    if latest["final_claim_state"].get("cdcl_antecedent_erasure_trichotomy") != "cdcl_antecedent_erasure_trichotomy_proved":
        fail("latest.json must record the CDCL antecedent-erasure trichotomy")
    rup_cdcl_packet = json_payloads.get("rup_complete_cdcl_support_normalizer.json", {})
    if rup_cdcl_packet.get("status") != "proved_in_revised_tex":
        fail("RUP-complete CDCL packet must be proved_in_revised_tex")
    if rup_cdcl_packet.get("theorem_summary", {}).get("measured_object") != "RUP-complete CDCL log exposing checker-visible propagation traces and parsed formula-label support":
        fail("RUP-complete CDCL packet must record the measured proof object")
    if "checker_visible_RUP_propagation_certificate_for_every_used_learned_clause" not in rup_cdcl_packet.get("audit_requirements", []):
        fail("RUP-complete CDCL packet must require checker-visible RUP propagation certificates")
    if "known_live_clause_database_at_each_RUP_check" not in rup_cdcl_packet.get("audit_requirements", []):
        fail("RUP-complete CDCL packet must require a known live clause database")
    if "trusted_formula_label_namespace_or_role_map" not in rup_cdcl_packet.get("audit_requirements", []):
        fail("RUP-complete CDCL packet must require namespace or role parsing")
    if "retained_support_for_deleted_clause_consequences" not in rup_cdcl_packet.get("audit_requirements", []):
        fail("RUP-complete CDCL packet must retain deleted-clause support")
    if "support_extraction_from_raw_RUP_or_DRUP_without_namespace_or_role_map" not in rup_cdcl_packet.get("nonclaims", []):
        fail("RUP-complete CDCL packet must preserve the raw RUP/DRUP nonclaim")
    if "apply_controller_complete_adaptive_audit_normalizer" not in rup_cdcl_packet.get("proof_skeleton", []):
        fail("RUP-complete CDCL packet must reduce to the controller-complete audit")
    if latest["final_claim_state"].get("rup_complete_cdcl_support_normalizer") != "rup_complete_cdcl_support_normalizer_proved":
        fail("latest.json must record the RUP-complete CDCL support normalizer")
    canonical_rup_packet = json_payloads.get("canonical_namespace_rup_cdcl_standardizer.json", {})
    if canonical_rup_packet.get("status") != "proved_in_revised_tex":
        fail("canonical-namespace RUP-CDCL packet must be proved_in_revised_tex")
    if canonical_rup_packet.get("theorem_summary", {}).get("measured_object") != "canonical RUP-CDCL manifest with reserved formula-label interval live-database reconstruction and retained parsed support":
        fail("canonical-namespace RUP-CDCL packet must record the measured proof object")
    if "reserved_formula_label_variable_interval" not in canonical_rup_packet.get("manifest_requirements", []):
        fail("canonical-namespace RUP-CDCL packet must require the label-variable interval")
    if "injective_map_from_label_interval_to_frontier_coordinates" not in canonical_rup_packet.get("manifest_requirements", []):
        fail("canonical-namespace RUP-CDCL packet must require the injective coordinate map")
    if "live_database_log_for_each_RUP_check" not in canonical_rup_packet.get("manifest_requirements", []):
        fail("canonical-namespace RUP-CDCL packet must require live database reconstruction")
    if "retained_support_for_deleted_clause_consequences" not in canonical_rup_packet.get("manifest_requirements", []):
        fail("canonical-namespace RUP-CDCL packet must retain deleted-clause support")
    if "derive_equivalent_local_support_parser" not in canonical_rup_packet.get("proof_skeleton", []):
        fail("canonical-namespace RUP-CDCL packet must derive the support parser")
    if "apply_RUP_complete_CDCL_support_normalizer" not in canonical_rup_packet.get("proof_skeleton", []):
        fail("canonical-namespace RUP-CDCL packet must reduce to the RUP-complete theorem")
    if "support_extraction_from_unmanifested_DIMACS_syntax" not in canonical_rup_packet.get("nonclaims", []):
        fail("canonical-namespace RUP-CDCL packet must preserve the unmanifested-DIMACS nonclaim")
    if latest["final_claim_state"].get("canonical_namespace_rup_cdcl_standardizer") != "canonical_namespace_rup_cdcl_standardizer_proved":
        fail("latest.json must record the canonical-namespace RUP-CDCL standardizer")
    carrier_independent_packet = json_payloads.get("carrier_independent_audit_upgrade_criterion.json", {})
    if carrier_independent_packet.get("status") != "proved_in_revised_tex":
        fail("carrier-independent audit upgrade packet must be proved_in_revised_tex")
    if carrier_independent_packet.get("theorem_summary", {}).get("measured_object") != "proof-system-intrinsic audit extractor outputting support support-locality evidence and budget without carrier-specific manifest":
        fail("carrier-independent audit upgrade packet must record the measured proof object")
    if "polynomial_time_proof_system_intrinsic_audit_extractor" not in carrier_independent_packet.get("audit_requirements", []):
        fail("carrier-independent audit upgrade packet must require a proof-system-intrinsic audit extractor")
    if "no_carrier_specific_namespace_manifest" not in carrier_independent_packet.get("audit_requirements", []):
        fail("carrier-independent audit upgrade packet must exclude carrier-specific namespace manifests")
    if "no_hidden_role_advice" not in carrier_independent_packet.get("audit_requirements", []):
        fail("carrier-independent audit upgrade packet must exclude hidden role advice")
    if "apply_support_local_normalization_transfer" not in carrier_independent_packet.get("proof_skeleton", []):
        fail("carrier-independent audit upgrade packet must reduce to support-local normalization transfer")
    if "top_paper_completion_without_a_concrete_system_instantiation" not in carrier_independent_packet.get("nonclaims", []):
        fail("carrier-independent audit upgrade packet must preserve the no-top-paper-completion nonclaim")
    if latest["final_claim_state"].get("carrier_independent_audit_upgrade_criterion") != "carrier_independent_audit_upgrade_criterion_proved":
        fail("latest.json must record the carrier-independent audit upgrade criterion")
    self_auditing_packet = json_payloads.get("self_auditing_rup_cdcl_instantiation.json", {})
    if self_auditing_packet.get("status") != "proved_in_revised_tex":
        fail("self-auditing RUP-CDCL packet must be proved_in_revised_tex")
    if self_auditing_packet.get("theorem_summary", {}).get("measured_object") != "enriched RUP-CDCL proof object with internal label decoder live-database reconstruction RUP witnesses and retained support annotations":
        fail("self-auditing RUP-CDCL packet must record the measured proof object")
    for requirement in [
        "proof_internal_label_decoder",
        "live_database_reconstruction_log",
        "checker_visible_RUP_propagation_certificates",
        "retained_deleted_clause_support",
        "no_external_carrier_specific_manifest",
    ]:
        if requirement not in self_auditing_packet.get("audit_requirements", []):
            fail(f"self-auditing RUP-CDCL packet must require {requirement}")
    if "apply_carrier_independent_audit_upgrade_criterion" not in self_auditing_packet.get("proof_skeleton", []):
        fail("self-auditing RUP-CDCL packet must apply the carrier-independent audit criterion")
    for nonclaim in [
        "raw_dimacs_lower_bound",
        "raw_rup_drup_lower_bound_without_support_parsing",
        "arbitrary_cdcl_lower_bound",
        "frege_lower_bound",
    ]:
        if nonclaim not in self_auditing_packet.get("nonclaims", []):
            fail(f"self-auditing RUP-CDCL packet must preserve the {nonclaim} nonclaim")
    if self_auditing_packet.get("coherence", {}).get("c11_role") != "proof_system_bridge":
        fail("self-auditing RUP-CDCL packet must be C11 proof-system bridge work")
    if latest["final_claim_state"].get("self_auditing_rup_cdcl_instantiation") != "self_auditing_rup_cdcl_instantiation_proved":
        fail("latest.json must record the self-auditing RUP-CDCL instantiation")
    append_only_packet = json_payloads.get("append_only_self_auditing_rup_cdcl.json", {})
    if append_only_packet.get("status") != "proved_in_revised_tex":
        fail("append-only self-auditing RUP-CDCL packet must be proved_in_revised_tex")
    if append_only_packet.get("theorem_summary", {}).get("measured_object") != "deletion-free self-auditing RUP-CDCL proof object with internal label decoder append-only clause log and RUP witnesses":
        fail("append-only self-auditing RUP-CDCL packet must record the measured proof object")
    for requirement in [
        "proof_internal_label_decoder",
        "append_only_clause_addition_log",
        "checker_visible_RUP_propagation_certificates",
        "no_deleted_clause_support_annotations_needed",
        "no_external_carrier_specific_manifest",
    ]:
        if requirement not in append_only_packet.get("audit_requirements", []):
            fail(f"append-only self-auditing RUP-CDCL packet must require {requirement}")
    for proof_step in [
        "scan_append_only_clause_database_and_RUP_witnesses",
        "apply_carrier_independent_audit_upgrade_criterion",
    ]:
        if proof_step not in append_only_packet.get("proof_skeleton", []):
            fail(f"append-only self-auditing RUP-CDCL packet must include proof step {proof_step}")
    for nonclaim in [
        "deletion_bearing_raw_rup_drup_lower_bound",
        "arbitrary_cdcl_lower_bound",
        "checked_label_decoder_not_removed",
    ]:
        if nonclaim not in append_only_packet.get("nonclaims", []):
            fail(f"append-only self-auditing RUP-CDCL packet must preserve the {nonclaim} nonclaim")
    if append_only_packet.get("coherence", {}).get("c11_role") != "proof_system_bridge":
        fail("append-only self-auditing RUP-CDCL packet must be C11 proof-system bridge work")
    if latest["final_claim_state"].get("append_only_self_auditing_rup_cdcl") != "append_only_self_auditing_rup_cdcl_proved":
        fail("latest.json must record the append-only self-auditing RUP-CDCL instantiation")
    prefix_typed_packet = json_payloads.get("prefix_typed_append_only_rup_cdcl.json", {})
    if prefix_typed_packet.get("status") != "proved_in_revised_tex":
        fail("prefix-typed append-only RUP-CDCL packet must be proved_in_revised_tex")
    if prefix_typed_packet.get("theorem_summary", {}).get("measured_object") != "typed append-only RUP-CDCL proof object with public formula-label namespace append-only clause log RUP witnesses and support-local auxiliary witnesses":
        fail("prefix-typed append-only RUP-CDCL packet must record the measured proof object")
    for requirement in [
        "public_formula_label_variable_namespace",
        "append_only_clause_addition_log",
        "checker_visible_RUP_propagation_certificates",
        "support_local_auxiliary_witnesses",
        "no_proof_internal_label_decoder_needed",
        "no_deleted_clause_support_annotations_needed",
        "no_external_carrier_specific_manifest",
    ]:
        if requirement not in prefix_typed_packet.get("audit_requirements", []):
            fail(f"prefix-typed append-only RUP-CDCL packet must require {requirement}")
    for proof_step in [
        "parse_formula_label_support_from_public_syntactic_namespace",
        "verify_support_local_auxiliary_witnesses_for_touched_auxiliary_clauses",
        "apply_carrier_independent_audit_upgrade_criterion",
    ]:
        if proof_step not in prefix_typed_packet.get("proof_skeleton", []):
            fail(f"prefix-typed append-only RUP-CDCL packet must include proof step {proof_step}")
    for nonclaim in [
        "untyped_raw_rup_drup_lower_bound",
        "deletion_bearing_raw_rup_drup_lower_bound",
        "support_locality_witness_obligation_not_removed",
        "arbitrary_cdcl_lower_bound",
    ]:
        if nonclaim not in prefix_typed_packet.get("nonclaims", []):
            fail(f"prefix-typed append-only RUP-CDCL packet must preserve the {nonclaim} nonclaim")
    if prefix_typed_packet.get("coherence", {}).get("c11_role") != "proof_system_bridge":
        fail("prefix-typed append-only RUP-CDCL packet must be C11 proof-system bridge work")
    if latest["final_claim_state"].get("prefix_typed_append_only_rup_cdcl") != "prefix_typed_append_only_rup_cdcl_proved":
        fail("latest.json must record the prefix-typed append-only RUP-CDCL instantiation")
    if latest.get("final_claim_state", {}).get("prefix_typed_rup_support_witness_necessity") != "prefix_typed_rup_support_witness_necessity_proved":
        fail("latest.json must record the prefix-typed RUP support-witness necessity boundary")
    if "prefix_typed_rup_support_witness_necessity" not in latest["top_paper_gate"]:
        fail("latest.json top-paper gate must record the prefix-typed RUP support-witness necessity boundary")
    prefix_witness_packet = json_payloads.get("prefix_typed_rup_support_witness_necessity.json", {})
    if prefix_witness_packet.get("status") != "proved_in_revised_tex":
        fail("prefix-typed RUP support-witness necessity packet must be proved_in_revised_tex")
    if prefix_witness_packet.get("theorem_summary", {}).get("measured_object") != "typed append-only RUP-CDCL trace without support-local auxiliary witnesses":
        fail("prefix-typed RUP support-witness necessity packet must record the measured object")
    if "public formula-label typing and append-only RUP checking do not certify completion-local auxiliary support" not in prefix_witness_packet.get("theorem_summary", {}).get("conclusion", ""):
        fail("prefix-typed RUP support-witness necessity packet must state the support-locality boundary")
    for mechanism in [
        "scan_public_formula_label_namespace_in_append_only_log_and_RUP_certificates",
        "build_same_skeleton_auxiliary_lift_with_hidden_label_h_not_in_W",
        "observe_identical_trace_public_scan_and_RUP_certificates_but_different_auxiliary_support_locality",
    ]:
        if mechanism not in prefix_witness_packet.get("boundary_mechanism", []):
            fail(f"prefix-typed RUP support-witness necessity packet must include boundary mechanism {mechanism}")
    for route in [
        "intrinsic_support_locality_invariant_for_touched_auxiliary_clauses",
        "deletion_bearing_or_untyped_RUP_DRUP_support_extraction",
        "explicit_SAT_family_source_lower_bound",
    ]:
        if route not in prefix_witness_packet.get("required_next_routes", []):
            fail(f"prefix-typed RUP support-witness necessity packet must include next route {route}")
    for nonclaim in [
        "does_not_refute_prefix_typed_append_only_RUP_CDCL_positive_corollary",
        "does_not_rule_out_intrinsic_support_locality_proof_rule",
        "does_not_handle_untyped_raw_rup_drup",
    ]:
        if nonclaim not in prefix_witness_packet.get("nonclaims", []):
            fail(f"prefix-typed RUP support-witness necessity packet must preserve the {nonclaim} nonclaim")
    if prefix_witness_packet.get("coherence", {}).get("c11_role") != "boundary":
        fail("prefix-typed RUP support-witness necessity packet must be C11 boundary work")
    qrep_packet = json_payloads.get("strict_prefix_qrep_normalizer.json", {})
    if qrep_packet.get("status") != "proved_in_revised_tex":
        fail("strict-prefix Qrep packet must be proved_in_revised_tex")
    if qrep_packet.get("theorem_summary", {}).get("measured_object") != "strict-prefix quotient-replay support plus dictionary certificate charge":
        fail("strict-prefix Qrep packet must record the measured proof object")
    if "RealSATInfluenceRealizer_N_arb" not in qrep_packet.get("nonclaims", []):
        fail("strict-prefix Qrep packet must preserve the RealSATInfluenceRealizer nonclaim")
    if "first_late_representative_use" not in qrep_packet.get("falsifiers", []):
        fail("strict-prefix Qrep packet must record the temporal falsifier")
    if latest["final_claim_state"].get("strict_prefix_qrep_replay_normalizer") != "strict_prefix_qrep_replay_normalizer_proved":
        fail("latest.json must record the strict-prefix Qrep replay normalizer")
    qrep_examples = json_payloads.get("strict_prefix_qrep_prefix_scan_examples.json", {})
    if qrep_examples.get("status") != "implemented":
        fail("strict-prefix Qrep prefix-scan examples must be implemented")
    accepted_seen = False
    rejected_seen = False
    for example in qrep_examples.get("examples", []):
        result = scan(example)
        expected = example.get("expected_result", {})
        if result.get("accepted") != expected.get("accepted"):
            fail(f"strict-prefix Qrep example {example.get('id')} has unexpected acceptance result")
        if result.get("reason") != expected.get("reason"):
            fail(f"strict-prefix Qrep example {example.get('id')} has unexpected rejection reason")
        accepted_seen = accepted_seen or result.get("accepted") is True
        rejected_seen = rejected_seen or result.get("accepted") is False
    if not accepted_seen or not rejected_seen:
        fail("strict-prefix Qrep examples must include one accepted and one rejected case")
    if latest["final_claim_state"].get("strict_prefix_qrep_prefix_scan_examples") != "finite_verifier_examples_validated":
        fail("latest.json must record the strict-prefix Qrep prefix-scan examples")
    cone_budget_packet = json_payloads.get("cone_budget_extension_lower_bound.json", {})
    if cone_budget_packet.get("status") != "proved_in_revised_tex":
        fail("cone-budget extension lower-bound packet must be proved_in_revised_tex")
    if cone_budget_packet.get("theorem_summary", {}).get("measured_object") != "product of final-interface variable count and maximum declared dependency-cone size":
        fail("cone-budget packet must record the measured proof object")
    if "normalizer_for_hidden_nonlocal_extension_variables" not in cone_budget_packet.get("boundary", {}).get("does_not_prove", []):
        fail("cone-budget packet must preserve the hidden-nonlocal-extension nonclaim boundary")
    bounded_depth_packet = json_payloads.get("bounded_depth_extension_tradeoff.json", {})
    if bounded_depth_packet.get("status") != "proved_in_revised_tex":
        fail("bounded-depth extension tradeoff packet must be proved_in_revised_tex")
    if bounded_depth_packet.get("theorem_summary", {}).get("measured_object") != "final-interface variable count times fan-in to the extension depth":
        fail("bounded-depth packet must record the measured proof object")
    if "unrestricted_extended_resolution_lower_bound" not in bounded_depth_packet.get("boundary", {}).get("does_not_prove", []):
        fail("bounded-depth packet must preserve the unrestricted-ER nonclaim boundary")
    transfer_packet = json_payloads.get("support_local_normalization_transfer.json", {})
    if transfer_packet.get("status") != "proved_in_revised_tex":
        fail("support-local normalization transfer packet must be proved_in_revised_tex")
    if transfer_packet.get("theorem_summary", {}).get("measured_object") != "support budget B(|pi|) controlling the extracted formula-label support":
        fail("support-local normalization transfer packet must record the measured proof object")
    cohered_spine = json_payloads.get("cohered_result_spine.json", {})
    if cohered_spine.get("status") != "implemented":
        fail("cohered-result spine packet must be implemented")
    if cohered_spine.get("coherence_fail_mode") != "fragmented_ensemble_of_results_even_if_each_component_is_locally_correct":
        fail("cohered-result spine must reject fragmented ensembles explicitly")
    if "cohered_results_as_main_paper_criterion" not in cohered_spine.get("gate_role", ""):
        fail("cohered-result spine must make cohered results a main-paper criterion")
    if cohered_spine.get("result_roles") is None or len(cohered_spine.get("result_roles", [])) != 5:
        fail("cohered-result spine must define the five admission roles")
    if "what_is_the_before_after_understanding_shift" not in cohered_spine.get("admission_questions", []):
        fail("cohered-result spine must require a before-after understanding shift")
    if "why_would_it_lose_force_or_become_misleading_if_separated_from_the_flagship_arc" not in cohered_spine.get("admission_questions", []):
        fail("cohered-result spine must require narrative indivisibility")
    if "lose_force" not in cohered_spine.get("narrative_indivisibility_test", ""):
        fail("cohered-result spine must record the narrative-indivisibility test")
    if cohered_spine.get("required_result_shape") != "one_recognizable_result_arc_not_a_fragmented_accumulation_of_locally_correct_results":
        fail("cohered-result spine must require one recognizable result arc rather than fragmented accumulation")
    proof_bridge_examples = []
    for role in cohered_spine.get("result_roles", []):
        if role.get("role") == "proof_system_bridge":
            proof_bridge_examples = role.get("current_examples", [])
    if "antecedent_complete_cdcl_learned_clause_normalizer" not in proof_bridge_examples:
        fail("cohered-result spine must include antecedent-complete CDCL as a proof-system bridge")
    if "self_auditing_RUP_CDCL_instantiation" not in cohered_spine.get("current_gate_decision", {}).get("not_top_ready_reason", ""):
        fail("cohered-result spine must record the self-auditing RUP-CDCL instantiation in the current gate decision")
    if "append_only_self_auditing_RUP_CDCL" not in cohered_spine.get("current_gate_decision", {}).get("not_top_ready_reason", ""):
        fail("cohered-result spine must record the append-only self-auditing RUP-CDCL instantiation in the current gate decision")
    if "prefix_typed_append_only_RUP_CDCL" not in cohered_spine.get("current_gate_decision", {}).get("not_top_ready_reason", ""):
        fail("cohered-result spine must record the prefix-typed append-only RUP-CDCL instantiation in the current gate decision")
    if "prefix_typed_RUP_support_witness_necessity" not in cohered_spine.get("current_gate_decision", {}).get("not_top_ready_reason", ""):
        fail("cohered-result spine must record the prefix-typed RUP support-witness necessity boundary")
    if "intrinsic_support_locality_invariant" not in cohered_spine.get("current_gate_decision", {}).get("not_top_ready_reason", ""):
        fail("cohered-result spine must set the next top-paper blocker to an intrinsic support-locality invariant")
    if "untyped_or_deletion_bearing_trace_handling" not in cohered_spine.get("current_gate_decision", {}).get("not_top_ready_reason", ""):
        fail("cohered-result spine must set the next top-paper blocker to untyped or deletion-bearing trace handling")
    if "self_auditing_rup_cdcl_instantiation" not in proof_bridge_examples:
        fail("cohered-result spine must include self-auditing RUP-CDCL as a proof-system bridge")
    if "append_only_self_auditing_rup_cdcl" not in proof_bridge_examples:
        fail("cohered-result spine must include append-only self-auditing RUP-CDCL as a proof-system bridge")
    if "prefix_typed_append_only_rup_cdcl" not in proof_bridge_examples:
        fail("cohered-result spine must include prefix-typed append-only RUP-CDCL as a proof-system bridge")
    boundary_examples = []
    for role in cohered_spine.get("result_roles", []):
        if role.get("role") == "boundary":
            boundary_examples = role.get("current_examples", [])
    if "cdcl_antecedent_erasure_trichotomy" not in boundary_examples:
        fail("cohered-result spine must include CDCL antecedent-erasure as boundary work")
    if "prefix_typed_rup_support_witness_necessity" not in boundary_examples:
        fail("cohered-result spine must include prefix-typed RUP support-witness necessity as boundary work")

    print(f"validated {len(REQUIRED_ARTIFACTS)} Formula Footprints closure artifacts")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
