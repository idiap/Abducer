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

"""Generate taxonomy projection cards for all local skills."""

from __future__ import annotations

from pathlib import Path

from agentic_common import ROOT, clean_text, iter_skill_dirs, load_optional_json, read_skill_description, rel, skill_name_from_dir, write_json


OUT = ROOT / "registry" / "skill_projections" / "abducer_skill_projections.json"
REGISTRY = ROOT / "agentic" / "registries" / "skill_registry.yaml"
QUALITY = ROOT / "agentic" / "registries" / "skill_quality_registry.yaml"


DEPTH_REPORT = ROOT / "agentic/reports/skill_depth/latest.json"


# These contracts are keyed by semantic skill identity.  Keeping the override
# beside generation prevents a list-position insertion from silently attaching
# discovery, Category, HoTT, or Yang--Mills authority to an unrelated skill.
SKILL_QUALITY_OVERRIDES = {
    "categorical-concept-forger": {
        "deterministic_boundary": "Packet v5 schema, dependency-authority v2, formal-lens execution receipt v2, finite carrier/action totality, identity/composition laws, declared cone/factorization scope, exact current-literature projection replay, registry-bound countermodel replay, and parallel-evaluation v4 same-suite receipts are deterministic.",
        "generative_boundary": "Choosing a high-risk abstraction, proposing its general universal property, and interpreting conceptual relevance remain generative and reviewable.",
        "epistemic_risk": "A replayed finite local category model or internally authored calibration can be mistaken for a general universal property or authority-distinct conceptual value.",
        "necessary_conditions": ["The shared categorical heuristic recommends the lens and the target/literature pressure is frozen.", "Finite actions, universal-property scope, exact witness, auditors, exact executed literature projection, v2 dependency closure, v4 parallel evaluation, and a v2 formal-lens receipt are present."],
        "sufficiency_claim": "The skill can certify only its declared finite local model/countermodel and internal protocol wiring, not a general category-theoretic property, target theorem, or conceptual value.",
        "representation_contract": "Outputs must bind packet v5 finite carriers/actions/laws, complete declared cone scope, registry-replayed witness, exact current-literature/auditor receipts, parallel evaluation v4, dependency authority v2, formal-lens execution receipt v2, and explicit production/value/theorem nulls.",
        "contract_versions": {"forge_packet": "5.0.0", "parallel_evaluation": "4.0.0", "formal_dependency_authority": "2.0.0", "formal_lens_execution_receipt": "2.0.0"},
        "authority_boundary": "Finite internal execution identity only; no production-evidence, authority-distinct evaluation, cognitive-independence, theorem, continuum, physics-value, or investment authority.",
        "failure_modes": ["Metaphorical arrows or an incomplete finite mediator scope", "Treating a local countermodel or internal arm effect as a general theorem", "Missing depth signals: none observed"],
    },
    "hott-equivalence-coherence-forger": {
        "deterministic_boundary": "Packet v5 schema, dependency-authority v2, formal-lens execution receipt v2, finite term/map and inverse laws, predicate-fiber transport, exact pointwise-path boundaries, truncation state, exact current-literature projection replay, registry-bound countermodel replay, and parallel-evaluation v4 same-suite receipts are deterministic.",
        "generative_boundary": "Choosing a high-risk identity/coherence abstraction, proposing its general meaning, and interpreting conceptual relevance remain generative and reviewable.",
        "epistemic_risk": "A replayed finite term/fiber model can be mistaken for HoTT semantics, univalence, general coherence, or authority-distinct conceptual value.",
        "necessary_conditions": ["The shared HoTT heuristic recommends the lens and the target/literature pressure is frozen.", "Finite terms, actions, fibers, homotopies, exact coherence paths/truncation state, witness, auditors, exact executed literature projection, v2 dependency closure, v4 parallel evaluation, and a v2 formal-lens receipt are present."],
        "sufficiency_claim": "The skill can certify only its declared finite local term/fiber model and countermodel, not HoTT semantics, univalence, general coherence, a target theorem, or conceptual value.",
        "representation_contract": "Outputs must bind packet v5 terms/maps/fibers/paths/coherence, exact path boundaries, registry-replayed witness, exact current-literature/auditor receipts, truncation state, parallel evaluation v4, dependency authority v2, formal-lens execution receipt v2, and explicit production/value/theorem nulls.",
        "contract_versions": {"forge_packet": "5.0.0", "parallel_evaluation": "4.0.0", "formal_dependency_authority": "2.0.0", "formal_lens_execution_receipt": "2.0.0"},
        "authority_boundary": "Finite internal execution identity only; no production-evidence, authority-distinct evaluation, cognitive-independence, theorem, continuum, physics-value, or investment authority.",
        "failure_modes": ["Conflating equality, equivalence, analogy, or operational indistinguishability", "Treating a finite noncoherence witness or internal arm effect as a general theorem", "Missing depth signals: none observed"],
    },
    "central-formal-conceptual-routes": {
        "deterministic_boundary": "Exact committed-input reopening, registered five-route authorship, finite mediator/equivalence witness replay, both-order sequence comparison, terminal process receipts, candidate-derived physics-handback structure, method-neutral adjudication shape, and explicit authority nulls are deterministic.",
        "generative_boundary": "Choosing task-relevant abstractions, constructing candidate conceptual transformations, and interpreting their physics-facing burden changes remain generative and reviewable.",
        "epistemic_risk": "Formal vocabulary, finite witness completion, digest inequality, or an internally replayed physics action can be mistaken for deep abstraction, conceptual merit, physical value, or a theorem.",
        "necessary_conditions": ["One current-literature, ancestry-bound, deeply reflected theory core and one precommitted carrier-specific decision rule are store-reopened from the active verified commit.", "Five matched process authors receive identical bytes and budgets, the nonformal route has equal opportunity, every formal witness is independently replayed, and each admissible candidate returns a correction, discriminating falsifier, and next physics action derived from its own delta."],
        "sufficiency_claim": "The skill can certify only its bounded finite route execution, witness replay, and physics-handback protocol; it cannot establish conceptual superiority, physical truth, theorem status, continuum validity, or Yang--Mills progress.",
        "representation_contract": "Outputs must bind the exact verified commit/input, five terminal route outcomes, explicit identity/inverse/transport/naturality/coherence scopes, both-order semantic comparison, candidate-specific physics handbacks, a plural method-neutral result, and all formal/physics/value/theorem/YM authority nulls.",
        "contract_versions": {"central_route_input": "3.0.0", "central_route_packet": "3.0.0", "formal_sequence_algebra": "1.0.0", "research_worker_execution_receipt": "1.0.0"},
        "authority_boundary": "Finite candidate-generation and internal comparison only; no theorem, continuum, univalence, physics-truth, comparative-value, conceptual-merit, theory-selection, experiment, proof, or Yang--Mills authority.",
        "failure_modes": ["Identity or relabeling accepted as a nontrivial mediator/equivalence", "Copied shared physics text instead of a candidate-derived handback", "Formal-vocabulary bonus over a capable nonformal rival", "Isomorphism-search ceiling or protected-observable erasure treated as productive noncommutation"],
    },
    "conceptual-frontier-deepening": {
        "deterministic_boundary": "Exact literature/theory bindings, precommitted author and judge allocations, bounded process receipts, label-blind family reconstruction, target-predeclared coverage verification, reflection branch retention, complete-content semantic evaluation, optional finite formal-witness replay, physics-handback shape, and generation/authority nulls are deterministic.",
        "generative_boundary": "Inventing conceptual mechanisms, reconstructing explanatory relations, reflecting philosophically, interpreting higher abstractions, and proposing physics-facing actions remain generative and reviewable.",
        "epistemic_risk": "A large fluent portfolio, internally diverse process wave, formal abstraction, judge agreement, or downstream probe can be mistaken for genuine creativity, semantic independence, conceptual merit, physical value, truth, or discovery efficacy.",
        "necessary_conditions": ["One active verified theory head, exact current bounded literature authority, target/carrier/regime/quantifiers, protected successes, conceptual pressure, negative knowledge, and fixed resource ceilings are present.", "Eight to twelve precommitted author slots, protected wildcards, a capable conservative control, label-blind family reconstruction, verified target coverage, six full-core reflection lenses, route-neutral multi-judge evaluation, and candidate-derived physics returns complete or fail with typed nulls."],
        "sufficiency_claim": "The skill can certify only the execution and replay of its theory-first frontier protocol; it cannot establish creativity, merit, comparative value, truth, proof, physics efficacy, theorem status, or experimental value.",
        "representation_contract": "Outputs must bind all source/currentness identities, raw and matured branches, family assessment and coverage certificate, reflection transformations, evaluator allocations/reports/controls/uncertainty, optional formal witnesses, candidate-specific physics returns, subordinate proof/experiment requests, failures, negative knowledge, plural outcomes, and explicit nulls.",
        "contract_versions": {"aggressive_provider_search": "1.0.0", "route_neutral_semantic_evaluation": "1.0.0", "central_route_packet": "3.0.0", "descendant_experiment_lane": "3.0.0"},
        "authority_boundary": "Theory-first proposal, reflection, and internal evaluation only; no provider/model/human/cognitive/semantic independence, creativity, merit, comparative-value, truth, proof, experiment-value, physics, theorem, continuum, or Yang--Mills authority.",
        "failure_modes": ["Taxonomy or sibling leakage before raw invention", "Self-declared families or unverified under-six coverage", "Status/length/formal-vocabulary-driven evaluation", "Copied physics handbacks or same-generation proof/experiment authority", "Missing depth signals: none observed"],
    },
    "ym-categorical-hott-physics-bridge": {
        "deterministic_boundary": "Bridge v7 schema, dependency-authority v2, continuum-authority v1, exact v2 formal-lens execution receipts, finite physical-carrier laws, transitive forge/witness authority, exact current-literature projection replay, fourteen-row target/quantifier/evidence/handback ledgers, nine runner-registry replays, boundary-fixture typing, and parallel-evaluation v4 same-suite bindings are deterministic.",
        "generative_boundary": "Interpreting physical relevance, proposing continuum/spectral obligations, and deciding whether the abstraction merits theory refinement remain generative and reviewable.",
        "epistemic_risk": "Finite carriers, boundary fixtures, or successful local calibrations can be mistaken for continuum control, observable completeness, OS reconstruction, a Hamiltonian gap, or authority-distinct physics value.",
        "necessary_conditions": ["Transitively validated category/HoTT forge v5 packets, their finite/internal v2 execution receipts, the exact current-literature evaluation projection, and the four-dimensional pure Yang--Mills target are bound.", "Finite physical carriers, all fourteen structure and burden rows, full quantifiers, nine registered calibration rows, exact physics handback, unavailable continuum authority, downstream gates, and explicit value/production non-claims are present."],
        "sufficiency_claim": "The skill can certify only finite local bridge consistency and calibration replay; it cannot establish continuum Yang--Mills, a mass gap, general physics value, or investment authority.",
        "representation_contract": "Outputs must bind bridge v7 physical actions/laws, upstream forge v5 packets and v2 formal-lens receipts, dependency authority v2, parallel evaluation v4, continuum-authority v1 unavailable projection, all calibration runner/input/output digests, exact current-literature projection, fourteen-row physics handback, downstream gates, and production/value/theorem non-claims.",
        "contract_versions": {"bridge_packet": "7.0.0", "upstream_forge_packet": "5.0.0", "parallel_evaluation": "4.0.0", "formal_dependency_authority": "2.0.0", "formal_lens_execution_receipt": "2.0.0", "continuum_authority": "1.0.0"},
        "authority_boundary": "Finite internal bridge replay only; no production-evidence, authority-distinct evaluation, cognitive-independence, physical-equivalence, continuum, OS-reconstruction, spectral-gap, physics-value, or investment authority.",
        "failure_modes": ["Abstract vocabulary without exact Yang--Mills carriers or quantifiers", "Treating boundary fixtures, local runner outputs, or internal arm effects as continuum or spectral evidence", "Missing depth signals: none observed"],
    },
}


def classify(name: str, description: str) -> dict[str, list[str] | str]:
    text = f"{name} {description}".lower()
    if name == "route":
        return {
            "reasoning_types": ["deterministic_validation", "workflow_composition"],
            "problem_domain_types": ["agentic_control_plane"],
            "task_context_types": ["workflow_governance"],
            "workflow_role": "rigid-reasoning-router",
            "deterministic": True,
        }
    if name == "orch":
        return {
            "reasoning_types": ["generative_reasoning", "workflow_composition"],
            "problem_domain_types": ["agentic_control_plane"],
            "task_context_types": ["target_navigation", "workflow_governance"],
            "workflow_role": "dynamic-reasoning-orchestrator",
            "deterministic": False,
        }
    reasoning = {"generative_reasoning"}
    domain = {"theorem_discovery"}
    contexts = set()
    role = "generative-skill"
    deterministic = False
    if "script" in text or "orchestrator" in text or "cycle" in text or name in {"work", "kb-orchestrator"}:
        reasoning.add("workflow_composition")
        reasoning.add("deterministic_validation")
        role = "hybrid-runner"
        deterministic = True
    if "validate" in text or "evaluator" in text or "critic" in text or "audit" in text:
        reasoning.add("evidence_assessment")
        role = "critic-or-validator"
    if "abduc" in text or "hypoth" in text:
        reasoning.add("abductive")
    if "deduce" in text or "entail" in text or "proof" in text:
        reasoning.add("deductive")
        reasoning.add("proof_search")
    if "dependency" in text or "target" in text or "pathway" in text or "entrypoint" in text:
        reasoning.add("dependency_closure")
        contexts.add("dependency_cartography")
    if "looper" in name:
        domain.add("agentic_control_plane")
        contexts.add("target_navigation")
        if "goal" in name:
            contexts.add("goal_enrichment")
            role = "control-plane-generative-intake"
        elif "dependency" in name:
            contexts.add("dependency_cartography")
            role = "control-plane-generative-cartographer"
        elif "workflow" in name or "hook" in name:
            contexts.add("workflow_governance")
            role = "control-plane-governor"
        elif "release" in name:
            contexts.add("release_promotion")
            role = "control-plane-release-interpreter"
    if "pvsnp" in name or "complexity" in text or "circuit" in text:
        domain.add("complexity_theory")
    if "lean" in text or "proof" in text or "mathlib" in text:
        domain.add("proof_engineering")
    if not contexts:
        contexts.add("target_navigation" if "orchestrator" in text else "dependency_cartography")
    return {
        "reasoning_types": sorted(reasoning),
        "problem_domain_types": sorted(domain),
        "task_context_types": sorted(contexts),
        "workflow_role": role,
        "deterministic": deterministic,
    }


def inline_depth_summary(skill_dir: Path) -> dict[str, object]:
    text = (skill_dir / "SKILL.md").read_text(encoding="utf-8-sig").lower()
    signals = {
        "guardrails": "guardrails" in text,
        "output_contract": "output contract" in text or "required output" in text,
        "epistemic_status": "epistemic status" in text or "conjectural" in text,
        "mathematical_invariant": "invariant" in text,
        "demotion": "demotion" in text or "disconfirm" in text or "quarantine" in text,
        "codex_exec_protocol": "codex exec protocol" in text,
    }
    missing = [key for key, present in signals.items() if not present]
    evidence = [key for key, present in signals.items() if present]
    return {
        "status": "pass" if not missing else "needs-depth-review",
        "critical_findings": 0 if not missing else len(missing),
        "missing_depth_signals": missing,
        "evidence_signals": evidence,
    }


def load_depth_by_name() -> dict[str, dict[str, object]]:
    payload = load_optional_json(DEPTH_REPORT)
    rows = payload.get("skills", [])
    if not isinstance(rows, list):
        return {}
    by_name = {}
    for row in rows:
        if isinstance(row, dict) and isinstance(row.get("skill_name"), str):
            by_name[row["skill_name"]] = row
    return by_name


def main() -> int:
    projections = []
    registry_cards = []
    quality_cards = []
    depth_by_name = load_depth_by_name()
    for skill_dir in iter_skill_dirs():
        name = skill_name_from_dir(skill_dir)
        description = read_skill_description(skill_dir)
        classification = classify(name, description)
        depth = depth_by_name.get(name) or inline_depth_summary(skill_dir)
        missing_depth = []
        for finding_field in ["mathematician_findings", "epistemologist_findings"]:
            for finding in depth.get(finding_field, []) if isinstance(depth.get(finding_field), list) else []:
                if isinstance(finding, dict) and finding.get("severity") == "critical":
                    missing_depth.append(str(finding.get("item", "unknown")))
        if not missing_depth:
            missing_depth = list(depth.get("missing_depth_signals", [])) if isinstance(depth.get("missing_depth_signals"), list) else []
        evidence_signals = list(depth.get("present_signals", [])) if isinstance(depth.get("present_signals"), list) else list(depth.get("evidence_signals", []))
        depth_status = "promoted" if int(depth.get("critical_findings", 0)) == 0 else "needs-depth-review"
        has_scripts = (skill_dir / "scripts").exists()
        projection = {
            "skill_name": name,
            "path": rel(skill_dir),
            "description": description,
            **classification,
            "inputs": ["target packet, KB, artifacts, or prompt context depending on invocation"],
            "outputs": ["artifact, report, proof route, or control-plane packet depending on workflow role"],
            "deterministic_boundaries": [
                "Filesystem, schema, path, and artifact existence checks are deterministic.",
                "Mathematical judgment, route interpretation, and release meaning require generative review."
            ],
            "generative_boundaries": [
                "Generative claims must cite KB IDs, dependency node IDs, artifact paths, or explicit unknowns.",
                "Generative skills may recommend actions but cannot silently mark gates passed."
            ],
            "prerequisites": ["Relevant KB and artifact evidence must exist or be explicitly unknown."],
            "validators": [
                "agentic/scripts/validate_skill_taxonomy_projections.py",
                "agentic/scripts/validate_skill_depth.py"
            ],
            "skill_depth": {
                "status": depth_status,
                "critical_findings": depth.get("critical_findings", 0),
                "evidence_signals": evidence_signals,
                "missing_depth_signals": missing_depth,
            },
            "failure_modes": [
                "Overbroad routing makes the skill appear useful for every workflow.",
                "Uncited mathematical claims are mistaken for grounded evidence."
            ]
        }
        formal_profile = SKILL_QUALITY_OVERRIDES.get(name)
        if formal_profile is not None:
            # Generated projections must expose the same live contract versions
            # and authority ceiling as the quality registry.  Otherwise a
            # taxonomy consumer sees a generic card while the executable skill
            # has a much narrower finite-formal boundary.
            projection.update(
                {
                    "contract_versions": dict(formal_profile["contract_versions"]),
                    "authority_boundary": formal_profile["authority_boundary"],
                    "deterministic_boundaries": [
                        formal_profile["deterministic_boundary"]
                    ],
                    "generative_boundaries": [
                        formal_profile["generative_boundary"]
                    ],
                    "prerequisites": list(formal_profile["necessary_conditions"]),
                    "failure_modes": list(formal_profile["failure_modes"]),
                }
            )
        projections.append(projection)
        registry_cards.append(
            {
                "name": name,
                "status": "promoted",
                "path": rel(skill_dir),
                "description": description,
                "workflow_role": classification["workflow_role"],
                "required_eval": "agentic/scripts/validate_skill_depth.py",
            }
        )
        quality_card = {
                "name": name,
                "status": depth_status,
                "deterministic_boundary": "Schema, path, artifact, and lifecycle checks are deterministic.",
                "generative_boundary": "Mathematical and workflow-fit judgments must cite artifacts and remain reviewable.",
                "epistemic_risk": "The skill can overstate support if artifact presence is confused with proof.",
                "necessary_conditions": ["Relevant evidence artifacts exist or unknowns are surfaced."],
                "sufficiency_claim": "The skill is sufficient only for its declared workflow role, not for proving the target.",
                "representation_contract": "Outputs must cite KB IDs, artifact paths, dependency nodes, or TODO blockers.",
                "skill_depth": {
                    "critical_findings": depth.get("critical_findings", 0),
                    "evidence_signals": evidence_signals,
                    "missing_depth_signals": missing_depth,
                    "source": "agentic/reports/skill_depth/latest.json" if depth_by_name else "inline-skill-body-scan",
                },
                "validation_oracles": [
                    "agentic/scripts/validate_skill_taxonomy_projections.py",
                    "agentic/scripts/validate_skill_depth.py",
                ],
                "failure_modes": [
                    "Overbroad triggering",
                    "Unsupported mathematical claims",
                    f"Missing depth signals: {', '.join(missing_depth) if missing_depth else 'none observed'}",
                ],
            }
        quality_card.update(SKILL_QUALITY_OVERRIDES.get(name, {}))
        quality_cards.append(quality_card)
    payload = {"version": 1, "generated_for": "abducer", "skills": projections}
    write_json(OUT, payload)
    write_json(REGISTRY, {"version": 1, "skills": registry_cards})
    write_json(QUALITY, {"version": 1, "skill_quality": quality_cards})
    print(f"Wrote {rel(OUT)} with {len(projections)} skill projections")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
