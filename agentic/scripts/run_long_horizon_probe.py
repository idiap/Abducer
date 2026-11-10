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

"""Evaluate the latest long-horizon reasoning run for content-specific control."""

from __future__ import annotations

from typing import Any

from agentic_common import ROOT, clean_text, kb_ref_from_path, load_json_object, rel, repo_path, utc_now, write_json
from abstraction_machinery_selection import summarize_machinery_portfolio, validate_machinery_shape
from formal_subgoal_control import summary_from_controls, validate_control_shape


PACKET = ROOT / "agentic/reports/reasoning_monitor/latest.json"
HYPOTHESIS_MAP = ROOT / "artifacts/hegelian/hypothesis_exploration_map.json"
SKILL_PROJECTIONS = ROOT / "registry/skill_projections/abducer_skill_projections.json"
TASK_REGISTRIES = ROOT / "registry/tasks"
OUT_JSON = ROOT / "agentic/reports/long_horizon/latest.json"
OUT_MD = ROOT / "agentic/reports/long_horizon/latest.md"
YANG_MILLS_TARGET = "yang-mills-existence-and-mass-gap-target"
GENERIC_ROUTE_MARKERS = [
    "target:yang-mills-existence-and-mass-gap-target",
    "weaken the theorem-shaped obligation",
]


def load_ledger(packet: dict[str, Any]) -> dict[str, Any]:
    target = packet["target"]
    kb_ref = kb_ref_from_path(repo_path(str(target["kb_path"]), must_exist=True))
    path = ROOT / "agentic/state/essential_target_ledgers" / f"{kb_ref}.json"
    return load_json_object(path) if path.exists() else {}


def clean_list(values: list[Any]) -> list[str]:
    return [clean_text(value) for value in values if clean_text(value)]


def route_card(route: dict[str, Any]) -> dict[str, Any]:
    domain = route.get("domain_specificity", {})
    family = route.get("route_blueprint", {}).get("route_family", "")
    family_lower = family.lower()
    if "balaban" in family_lower or "rg" in family_lower:
        physics_story = (
            "Regulated non-Abelian gauge fields must remain controlled under scale integration so that cutoff removal leaves "
            "a non-Gaussian, reflection-positive continuum vacuum sector with gauge-invariant observables that can witness interaction."
        )
        physical_failure = (
            "The mechanism fails if the limit is only finite-volume/fixed-cutoff, if reflection positivity is not closed in the limiting topology, "
            "if all connected gauge-invariant observable witnesses collapse to a Gaussian/free theory, or if no same-theory spectral witness can be extracted."
        )
    elif "correlator" in family_lower or "spectral-gap" in family_lower:
        physics_story = (
            "Gauge-invariant Euclidean time correlations in the continuum Yang-Mills object must have spectral measures with support "
            "bounded away from zero, and the same observable family must survive OS reconstruction densely enough to control the physical excitation sector."
        )
        physical_failure = (
            "The mechanism fails if decay constants vanish under cutoff removal, if the observables are not gauge invariant or spectrally determining, "
            "or if the gap only exists in a regulated lattice Hilbert space."
        )
    else:
        physics_story = (
            "The candidate must identify the Yang-Mills object, observable algebra, limiting regime, and spectral or nontriviality mechanism it acts on."
        )
        physical_failure = "The mechanism fails if those objects belong to different theories or if the continuum/spectral transfer cannot be stated."
    return {
        "candidate_id": route["candidate_id"],
        "priority": route.get("priority"),
        "route_disposition": route.get("route_disposition"),
        "routing_decision": route.get("routing_decision"),
        "target_relevance_score": route.get("target_relevance_score"),
        "drift_risk": route.get("drift_risk"),
        "creative_operation": route.get("creative_operation"),
        "commitment_ids": route.get("cited_commitment_ids", []),
        "domain_terms": domain.get("route_terms", []),
        "specificity_score": domain.get("score", 0),
        "transformation": route.get("proposed_transformation", ""),
        "source_witness": route.get("source_witness", ""),
        "route_family": family,
        "physics_story": physics_story,
        "physical_failure_mode": physical_failure,
        "obligations": [
            row.get("requirement", "")
            for row in route.get("obligations", [])
            if isinstance(row, dict)
        ][:6],
        "source_artifacts": route.get("source_artifacts", []),
        "subgoal_control": route.get("subgoal_control", {}),
        "machinery_selection": route.get("machinery_selection", {}),
    }


def is_generic_route(route: dict[str, Any]) -> bool:
    text = clean_text(f"{route.get('proposed_transformation', '')} {route.get('source_witness', '')}").lower()
    return any(marker in text for marker in GENERIC_ROUTE_MARKERS)


def build_skill_ecosystem_coherence() -> dict[str, Any]:
    projections = load_json_object(SKILL_PROJECTIONS).get("skills", [])
    projection_by_name = {row["skill_name"]: row for row in projections if isinstance(row, dict) and row.get("skill_name")}
    workflows = []
    direct_skills: set[str] = set()
    for manifest_path in sorted(TASK_REGISTRIES.glob("*/task_registry.json")):
        manifest = load_json_object(manifest_path)
        for workflow in manifest.get("visible_workflows", []):
            if not isinstance(workflow, dict):
                continue
            skills = clean_list(workflow.get("composed_skills", []))
            direct_skills.update(skills)
            workflows.append(
                {
                    "task_id": manifest.get("task_id", ""),
                    "task_status": manifest.get("status", ""),
                    "workflow": workflow.get("name", ""),
                    "key_function": workflow.get("key_function", ""),
                    "composed_skills": skills,
                    "skill_count": len(skills),
                    "reasoning_types": clean_list(workflow.get("reasoning_types", [])),
                    "task_context_types": clean_list(workflow.get("task_context_types", [])),
                    "validators": clean_list(workflow.get("validators", [])),
                }
            )
    all_skill_names = set(projection_by_name)
    projected_only = sorted(all_skill_names - direct_skills)
    role_counts: dict[str, int] = {}
    context_counts: dict[str, int] = {}
    for row in projection_by_name.values():
        role = clean_text(row.get("workflow_role", "unknown")) or "unknown"
        role_counts[role] = role_counts.get(role, 0) + 1
        for context in clean_list(row.get("task_context_types", [])):
            context_counts[context] = context_counts.get(context, 0) + 1
    direct_workflow_names = {row["workflow"]: row for row in workflows}
    target_nav = direct_workflow_names.get("target-navigation-control-plane", {})
    conceptual = direct_workflow_names.get("conceptual-obstruction-refinement", {})
    findings: list[dict[str, str]] = []
    required_target_navigation_skills = {
        "looper-target-goal-enricher",
        "looper-target-dependency-cartographer",
        "looper-workflow-contract-governor",
        "looper-hook-policy-maintainer",
        "looper-release-promoter",
        "kb-orchestrator",
        "work",
    }
    required_conceptual_roles = {
        "abducer-conceptual-pressure-formalizer",
        "abducer-failure-signal-cartographer",
        "kb-induce",
        "kb-abduce",
        "kb-deduce",
        "kb-concept-bridge-planner",
        "abducer-mediation-candidate-generator",
        "abducer-obligation-gatekeeper",
        "counterfactual-route-prober",
        "epistemic-status-ledger",
        "kb-end-to-end-proof-critic",
        "abducer-refinement-route-ranker",
        "work",
    }
    if not target_nav:
        findings.append({"severity": "critical", "check": "target-navigation-workflow", "message": "Missing active target-navigation-control-plane workflow."})
    else:
        missing = sorted(required_target_navigation_skills - set(target_nav.get("composed_skills", [])))
        if missing:
            findings.append({"severity": "critical", "check": "target-navigation-skills", "message": f"Target navigation lacks required control skills: {missing}"})
    if not conceptual:
        findings.append({"severity": "critical", "check": "conceptual-workflow", "message": "Missing conceptual-obstruction-refinement workflow for discovery/evaluation skill use."})
    else:
        missing = sorted(required_conceptual_roles - set(conceptual.get("composed_skills", [])))
        if missing:
            findings.append({"severity": "critical", "check": "conceptual-skills", "message": f"Conceptual refinement lacks required discovery/evaluation skills: {missing}"})
    unprojected_direct = sorted(direct_skills - all_skill_names)
    if unprojected_direct:
        findings.append({"severity": "critical", "check": "projection-coverage", "message": f"Direct workflow skills missing projections: {unprojected_direct}"})
    review_pool = sorted(name for name in all_skill_names if name.startswith("review-reasoner"))
    reporting_pool = sorted(name for name in all_skill_names if projection_by_name[name].get("path", "").startswith("skills/reporting/"))
    ingest_pool = sorted(name for name in all_skill_names if projection_by_name[name].get("path", "").startswith("skills/ingest/"))
    if not review_pool:
        findings.append({"severity": "warning", "check": "review-pool", "message": "No review reasoner pool is available for stress testing."})
    if not reporting_pool:
        findings.append({"severity": "warning", "check": "reporting-pool", "message": "No reporting pool is available for handoff."})
    critical = sum(1 for finding in findings if finding["severity"] == "critical")
    return {
        "status": "pass" if critical == 0 else "fail",
        "critical_findings": critical,
        "findings": findings,
        "policy": (
            "Maximal skill use means phase-complete composition with conditional dispatch, not firing every skill in every iteration. "
            "Control-plane skills govern the target loop; discovery/evaluation/reasoning skills act in conceptual refinement; "
            "ingest, review, and reporting skills remain available as triggered evidence, stress-test, and handoff pools."
        ),
        "metrics": {
            "projected_skill_count": len(all_skill_names),
            "direct_workflow_skill_count": len(direct_skills),
            "projected_conditional_skill_count": len(projected_only),
            "workflow_count": len(workflows),
        },
        "role_counts": dict(sorted(role_counts.items())),
        "context_counts": dict(sorted(context_counts.items())),
        "phase_coverage": [
            {
                "phase": "target_navigation",
                "workflow": "target-navigation-control-plane",
                "status": "role-complete" if target_nav and not (required_target_navigation_skills - set(target_nav.get("composed_skills", []))) else "incomplete",
                "composed_skills": target_nav.get("composed_skills", []),
                "why_consistent": "This phase controls goals, dependencies, hooks, validation, release, and handoff; it should stay lean and not run every discovery/review skill directly.",
            },
            {
                "phase": "conceptual_refinement",
                "workflow": "conceptual-obstruction-refinement",
                "status": "role-complete" if conceptual and not (required_conceptual_roles - set(conceptual.get("composed_skills", []))) else "incomplete",
                "composed_skills": conceptual.get("composed_skills", []),
                "why_consistent": "This phase carries the dense discovery stack: conceptual pressure, failure signals, induction, abduction, deduction, bridge planning, obligation gates, counterfactual probes, ledgers, proof critique, ranking, and work-loop handoff.",
            },
            {
                "phase": "conditional_pools",
                "workflow": "triggered-by-frontier-or-handoff",
                "status": "available",
                "review_pool": review_pool,
                "ingest_pool": ingest_pool,
                "reporting_pool": reporting_pool,
                "why_consistent": "These skills should be invoked when the route demands prior-art intake, persona stress testing, or expert-facing compression, rather than bloating every control-plane cycle.",
            },
        ],
        "projected_conditional_skill_examples": projected_only[:12],
    }


def build_probe() -> dict[str, Any]:
    packet = load_json_object(PACKET)
    hypothesis = load_json_object(HYPOTHESIS_MAP)
    ledger = load_ledger(packet)
    skill_coherence = build_skill_ecosystem_coherence()
    commitments = [row["id"] for row in ledger.get("essential_commitments", []) if isinstance(row, dict) and row.get("id")]
    proof_budget = ledger.get("route_budgets", {}).get("proof_queue", 2)
    routes = packet["candidate_routes"]
    active_proof_routes = [route for route in routes if route.get("route_disposition") == "proof_queue"]
    top_routes = routes[:5]
    commitment_union = sorted({cid for route in active_proof_routes for cid in route.get("cited_commitment_ids", [])})
    demoted_by_budget = [
        route for route in routes if any("route budget" in reason for reason in route.get("reasons", []))
    ]
    findings: list[dict[str, str]] = []
    for finding in skill_coherence.get("findings", []):
        if finding.get("severity") == "critical":
            findings.append({"severity": "critical", "check": f"skill-coherence:{finding.get('check')}", "message": finding.get("message", "")})
    is_yang_mills = packet["target"]["target_id"] == YANG_MILLS_TARGET
    if packet.get("validation", {}).get("missing_evidence_count") != 0:
        findings.append({"severity": "critical", "check": "evidence", "message": "Monitor packet has missing evidence."})
    if packet.get("stale_workflow", {}).get("critical_findings") != 0:
        findings.append({"severity": "critical", "check": "stale-workflow", "message": "Stale-workflow preflight has critical findings."})
    if hypothesis.get("target_id") != packet["target"]["target_id"]:
        findings.append(
            {
                "severity": "critical",
                "check": "hypothesis-map-target",
                "message": f"Hypothesis map target {hypothesis.get('target_id')} does not match monitor target {packet['target']['target_id']}.",
            }
        )
    if not active_proof_routes:
        findings.append({"severity": "critical", "check": "proof-queue", "message": "No active proof-queue routes are present."})
    if len(active_proof_routes) > proof_budget:
        findings.append({"severity": "critical", "check": "proof-queue-budget", "message": f"Proof queue has {len(active_proof_routes)} routes over budget {proof_budget}."})
    if is_yang_mills and any(is_generic_route(route) for route in top_routes):
        findings.append({"severity": "critical", "check": "generic-route", "message": "A generic target rewrite appears in the top five routes."})
    missing_commitments = sorted(set(commitments) - set(commitment_union))
    if missing_commitments:
        findings.append({"severity": "critical", "check": "commitment-coverage", "message": f"Active proof queue misses commitments: {missing_commitments}"})
    for route in active_proof_routes:
        route_text = clean_text(route.get("proposed_transformation", "")).lower()
        if "factor the opaque obligation" in route_text or "smaller lemmas, evidence tasks, or discovery branches" in route_text:
            findings.append({"severity": "critical", "check": "strategy-language", "message": f"{route['candidate_id']} still uses generic factorization language."})
        if route.get("target_relevance_score", 0) < 0.8:
            findings.append({"severity": "warning", "check": "target-relevance", "message": f"{route['candidate_id']} has weak target relevance."})
        if is_yang_mills and not route.get("domain_specificity", {}).get("route_terms"):
            findings.append({"severity": "critical", "check": "specificity", "message": f"{route['candidate_id']} lacks Yang-Mills domain terms."})
        generic_obligations = [
            row.get("requirement", "")
            for row in route.get("obligations", [])
            if isinstance(row, dict) and row.get("requirement", "").startswith("Discharge `")
        ]
        if generic_obligations:
            findings.append({"severity": "critical", "check": "obligation-language", "message": f"{route['candidate_id']} still has generic gate obligations."})
    if not demoted_by_budget and len(routes) > proof_budget:
        findings.append({"severity": "warning", "check": "budget-signal", "message": "No candidates record proof-queue budget demotion."})
    reorientation = packet.get("reorientation_control", {})
    machinery_selections = [
        route.get("machinery_selection", {})
        for route in routes
        if isinstance(route.get("machinery_selection"), dict) and route.get("machinery_selection")
    ]
    machinery_portfolio = summarize_machinery_portfolio(machinery_selections)
    controls = [route.get("subgoal_control", {}) for route in routes if isinstance(route.get("subgoal_control"), dict)]
    control_summary = summary_from_controls(controls)
    if len(controls) != len(routes):
        findings.append({"severity": "critical", "check": "subgoal-control-coverage", "message": "Not every route carries subgoal_control."})
    for route in routes:
        ok, reason = validate_control_shape(route.get("subgoal_control"))
        if not ok:
            findings.append({"severity": "critical", "check": "subgoal-control-shape", "message": f"{route.get('candidate_id')} invalid subgoal_control: {reason}"})
        if route.get("route_disposition") in {"proof_queue", "discovery_branch"} and route.get("subgoal_control", {}).get("decision") != "persist_adapt":
            findings.append({"severity": "critical", "check": "subgoal-control-disposition", "message": f"{route.get('candidate_id')} has active disposition with decision {route.get('subgoal_control', {}).get('decision')}"})
        ok, reason = validate_machinery_shape(route.get("machinery_selection"))
        if not ok:
            findings.append({"severity": "critical", "check": "machinery-selection-shape", "message": f"{route.get('candidate_id')} invalid machinery_selection: {reason}"})
        elif route.get("route_disposition") == "proof_queue" and route["machinery_selection"].get("machinery_role") == "obstruction":
            findings.append({"severity": "critical", "check": "machinery-proof-queue", "message": f"{route.get('candidate_id')} proof_queue route uses obstruction machinery"})
    if is_yang_mills and machinery_portfolio.get("missing_core_roles"):
        findings.append({"severity": "warning", "check": "machinery-portfolio", "message": f"Machinery portfolio missing core roles: {machinery_portfolio['missing_core_roles']}"})
    if control_summary.get("has_stale_repeated_blockers"):
        findings.append({"severity": "critical", "check": "stale-subgoal-blocker", "message": "A route persists despite repeated blockers without an action decision."})
    reorientation_text = clean_text(reorientation).lower()
    for marker in ["restrategize", "backtrack", "pivot", "quarantine", "same-theory"]:
        if marker not in reorientation_text:
            findings.append({"severity": "critical", "check": "reorientation-control", "message": f"Missing reorientation marker: {marker}"})
    if len(reorientation.get("active_reorientation_queue", [])) < 3:
        findings.append({"severity": "critical", "check": "reorientation-queue", "message": "Active reorientation queue is too small for long-horizon control."})
    if not reorientation.get("route_assessments"):
        findings.append({"severity": "critical", "check": "route-reorientation", "message": "No route-level reorientation assessments are present."})
    contract = reorientation.get("bounded_reflection_contract", {})
    if not contract.get("stop_reflecting_when"):
        findings.append({"severity": "critical", "check": "bounded-reflection", "message": "Reorientation lacks bounded reflection stop conditions."})
    critical = sum(1 for finding in findings if finding["severity"] == "critical")
    proof_cards = [route_card(route) for route in active_proof_routes]
    discovery_cards = [route_card(route) for route in routes if route.get("route_disposition") == "discovery_branch"][:8]
    return {
        "version": 1,
        "generated_utc": utc_now(),
        "target_id": packet["target"]["target_id"],
        "quality_gate": "pass" if critical == 0 else "fail",
        "critical_findings": critical,
        "findings": findings,
        "metrics": {
            "reasoning_events": packet["reasoning_events"]["event_count"],
            "frontier_total": packet["frontier"]["total"],
            "candidate_routes": len(routes),
            "proof_obligations": packet["proof_obligations"]["total"],
            "proof_queue_budget": proof_budget,
            "proof_queue_count": len(active_proof_routes),
            "discovery_branch_count": sum(1 for route in routes if route.get("route_disposition") == "discovery_branch"),
            "missing_evidence_count": packet["validation"]["missing_evidence_count"],
            "stale_critical_findings": packet["stale_workflow"]["critical_findings"],
            "subgoal_control_count": control_summary["active_control_count"],
            "stale_repeated_blockers": len(control_summary["stale_repeated_blockers"]),
            "machinery_selection_count": machinery_portfolio["selection_count"],
        },
        "active_proof_queue": proof_cards,
        "discovery_branches": discovery_cards,
        "commitment_coverage": {
            "required_commitments": commitments,
            "active_proof_queue_union": commitment_union,
            "missing": missing_commitments,
        },
        "pipeline_observations": [
            "Active mechanism candidates must survive a physics/math interpretation pass: they must name gauge-field objects, observables, limits, and spectral meaning.",
            "The proof-queue budget is a sequencing control; it is not the explanation. The explanation lives in whether the RG and decay mechanisms can meet in one continuum theory.",
            "The active monitor remains stale-safe when missing evidence and stale critical findings are zero, but mathematical progress still depends on same-theory bridge lemmas.",
            "Reorientation control should diagnose physical obstruction types: cutoff leakage, loss of reflection positivity, Gaussian collapse, weak observable sector, or vanishing decay scale.",
            "Skill use is maximal only when the current physical obstruction triggers the right evidence, review, proof, or reporting skill, not when every skill is invoked indiscriminately.",
        ],
        "skill_ecosystem_coherence": skill_coherence,
        "reorientation_control": {
            "current_diagnosis": reorientation.get("current_diagnosis", ""),
            "current_recommendation": reorientation.get("current_recommendation", {}),
            "bounded_reflection_contract": reorientation.get("bounded_reflection_contract", {}),
            "route_assessments": reorientation.get("route_assessments", []),
            "active_queue": reorientation.get("active_reorientation_queue", []),
            "decision_points": reorientation.get("decision_points", []),
        },
        "formal_subgoal_control": {
            "policy": packet.get("formal_subgoal_control_policy", {}),
            "summary": control_summary,
            "active_controls": controls,
        },
        "machinery_portfolio": {
            "summary": machinery_portfolio,
            "active_selections": machinery_selections,
            "interpretation": (
                "The route portfolio is coherent only when construction, transfer, witness, and validation roles are all visible. "
                "For Yang-Mills this means RG construction cannot replace OS transfer, correlator decay cannot replace continuum construction, "
                "and Hamiltonian language remains endpoint validation unless reconstruction premises are supplied."
            ),
        },
        "interpretation_artifacts": [
            "agentic/reports/physics_math_interpretation/latest.json",
            "agentic/reports/physics_math_interpretation/latest.md",
        ],
        "residual_weak_zones": [
            "The Balaban/RG mechanism still has to show that scale control produces OS-positive continuum Schwinger functions rather than merely stable cutoff actions.",
            "The correlator-decay mechanism still has to show cutoff-uniform spectral support away from zero for a gauge-invariant observable family dense enough to see physical excitations.",
            "The nontriviality witness must be a connected gauge-invariant observable in the same limiting Schwinger family used for reconstruction and gap analysis.",
            "The next Yang-Mills pass should trigger ingest, review, or reporting skills only when a bridge lemma names a precise theorem target, observable family, or expert-checkable claim.",
        ],
        "source_artifacts": [
            "agentic/reports/reasoning_monitor/latest.json",
            "artifacts/hegelian/hypothesis_exploration_map.json",
            "agentic/state/essential_target_ledgers/yang-mills-existence-and-mass-gap.json",
            "KB/yang-mills-existence-and-mass-gap.kb.md",
        ],
    }


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Long-Horizon Yang-Mills Probe",
        "",
        f"- Target: `{report['target_id']}`",
        f"- Quality gate: `{report['quality_gate']}`",
        f"- Critical findings: {report['critical_findings']}",
        "",
        "## Metrics",
        "",
    ]
    for key, value in report["metrics"].items():
        lines.append(f"- `{key}`: {value}")
    lines.extend(["", "## Active Mechanism Candidates", ""])
    for route in report["active_proof_queue"]:
        lines.append(f"### {route['candidate_id']}")
        lines.append("")
        lines.append(f"- Operation: `{route['creative_operation']}`")
        if route["route_family"]:
            lines.append(f"- Route family: `{route['route_family']}`")
        lines.append(f"- Physics story: {route['physics_story']}")
        lines.append(f"- Physical failure mode: {route['physical_failure_mode']}")
        lines.append(f"- Target relevance: `{route['target_relevance_score']}`")
        lines.append(f"- Commitments: `{', '.join(route['commitment_ids'])}`")
        lines.append(f"- Domain terms: `{', '.join(route['domain_terms'])}`")
        lines.append(f"- Transformation: {route['transformation']}")
        if route["source_witness"]:
            lines.append(f"- Source witness: {route['source_witness']}")
        if route["obligations"]:
            lines.append("- First obligations:")
            for obligation in route["obligations"][:4]:
                lines.append(f"  - {obligation}")
        lines.append("")
    lines.extend(["## Discovery Branches Held By Sequencing Budget", ""])
    for route in report["discovery_branches"][:6]:
        lines.append(f"- `{route['candidate_id']}` `{route['creative_operation']}` score `{route['target_relevance_score']}` terms `{', '.join(route['domain_terms'])}`")
    lines.extend(["", "## Commitment Coverage", ""])
    coverage = report["commitment_coverage"]
    lines.append(f"- Required: `{', '.join(coverage['required_commitments'])}`")
    lines.append(f"- Covered by active proof queue: `{', '.join(coverage['active_proof_queue_union'])}`")
    lines.append(f"- Missing: `{', '.join(coverage['missing']) or 'none'}`")
    lines.extend(["", "## Findings", ""])
    if not report["findings"]:
        lines.append("None.")
    for finding in report["findings"]:
        lines.append(f"- `{finding['severity']}` `{finding['check']}`: {finding['message']}")
    lines.extend(["", "## Pipeline Observations", ""])
    for item in report["pipeline_observations"]:
        lines.append(f"- {item}")
    lines.extend(["", "## Skill Ecosystem Coherence", ""])
    skill_coherence = report.get("skill_ecosystem_coherence", {})
    lines.append(f"- Status: `{skill_coherence.get('status', '')}`")
    lines.append(f"- Critical findings: `{skill_coherence.get('critical_findings', '')}`")
    if skill_coherence.get("policy"):
        lines.append(f"- Policy: {skill_coherence['policy']}")
    metrics = skill_coherence.get("metrics", {})
    for key in ["projected_skill_count", "direct_workflow_skill_count", "projected_conditional_skill_count", "workflow_count"]:
        if key in metrics:
            lines.append(f"- `{key}`: {metrics[key]}")
    for phase in skill_coherence.get("phase_coverage", []):
        lines.append(f"- Phase `{phase.get('phase')}` via `{phase.get('workflow')}`: `{phase.get('status')}`")
        if phase.get("why_consistent"):
            lines.append(f"  - Why consistent: {phase['why_consistent']}")
        if phase.get("composed_skills"):
            lines.append(f"  - Skills: `{', '.join(phase['composed_skills'][:12])}`")
        if phase.get("review_pool"):
            lines.append(f"  - Review pool: `{', '.join(phase['review_pool'])}`")
        if phase.get("ingest_pool"):
            lines.append(f"  - Ingest pool: `{', '.join(phase['ingest_pool'])}`")
        if phase.get("reporting_pool"):
            lines.append(f"  - Reporting pool: `{', '.join(phase['reporting_pool'])}`")
    if skill_coherence.get("findings"):
        lines.append("- Skill coherence findings:")
        for finding in skill_coherence["findings"]:
            lines.append(f"  - `{finding.get('severity')}` `{finding.get('check')}`: {finding.get('message')}")
    lines.extend(["", "## Reorientation Control", ""])
    reorientation = report.get("reorientation_control", {})
    if reorientation.get("current_diagnosis"):
        lines.append(reorientation["current_diagnosis"])
        lines.append("")
    recommendation = reorientation.get("current_recommendation", {})
    if recommendation:
        lines.append(f"- Current recommendation: `{recommendation.get('decision', '')}`")
        if recommendation.get("rationale"):
            lines.append(f"  - Rationale: {recommendation['rationale']}")
        if recommendation.get("pivot_guard"):
            lines.append(f"  - Pivot guard: {recommendation['pivot_guard']}")
    contract = reorientation.get("bounded_reflection_contract", {})
    if contract:
        lines.append(f"- Max reflection passes before action: `{contract.get('max_reflection_passes_before_action', '')}`")
        for stop in contract.get("stop_reflecting_when", [])[:3]:
            lines.append(f"  - Stop reflecting when: {stop}")
    for assessment in reorientation.get("route_assessments", [])[:4]:
        lines.append(f"- Route `{assessment.get('candidate_id')}` -> `{assessment.get('recommended_move')}`")
        lines.append(f"  - Obstruction: {assessment.get('obstruction_type')}")
        lines.append(f"  - Next probe: {assessment.get('next_probe')}")
    for action in reorientation.get("active_queue", [])[:5]:
        lines.append(f"- `{action.get('mode')}` `{action.get('action_id')}`: {action.get('action')}")
        if action.get("why_now"):
            lines.append(f"  - Why now: {action['why_now']}")
        if action.get("success_condition"):
            lines.append(f"  - Success condition: {action['success_condition']}")
    lines.extend(["", "## Formal Subgoal Control", ""])
    formal = report.get("formal_subgoal_control", {})
    summary = formal.get("summary", {})
    lines.append(f"- Active controls: `{summary.get('active_control_count', 0)}`")
    lines.append(f"- Decision counts: `{summary.get('decision_counts', {})}`")
    lines.append(f"- Stale repeated blockers: `{len(summary.get('stale_repeated_blockers', []))}`")
    for control in formal.get("active_controls", [])[:6]:
        lines.append(f"- `{control.get('decision')}` {control.get('target_object_link')}")
        lines.append(f"  - Learning: {control.get('learning_from_failure')}")
        lines.append(f"  - Next action: {control.get('next_action')}")
    lines.extend(["", "## Machinery Portfolio", ""])
    machinery = report.get("machinery_portfolio", {})
    summary = machinery.get("summary", {})
    lines.append(f"- Interpretation: {machinery.get('interpretation', '')}")
    lines.append(f"- Selection count: `{summary.get('selection_count', 0)}`")
    lines.append(f"- Role counts: `{summary.get('role_counts', {})}`")
    lines.append(f"- Missing core roles: `{', '.join(summary.get('missing_core_roles', [])) or 'none'}`")
    for selection in machinery.get("active_selections", [])[:6]:
        lines.append(f"- `{selection.get('machinery_role')}` {selection.get('selected_machinery')}")
        lines.append(f"  - Controlled interface: {selection.get('controlled_interface')}")
        lines.append(f"  - Bridge obligation: {selection.get('required_bridge_obligation')}")
    lines.extend(["", "## Residual Weak Zones", ""])
    for item in report["residual_weak_zones"]:
        lines.append(f"- {item}")
    return "\n".join(lines) + "\n"


def main() -> int:
    report = build_probe()
    write_json(OUT_JSON, report)
    OUT_MD.parent.mkdir(parents=True, exist_ok=True)
    OUT_MD.write_text(render_markdown(report), encoding="utf-8")
    print(f"Wrote {rel(OUT_JSON)}")
    print(f"Wrote {rel(OUT_MD)}")
    return 0 if report["quality_gate"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
