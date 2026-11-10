"""Serialized orchestration over immutable skill artifacts."""

from __future__ import annotations

from collections import Counter
from pathlib import Path
from typing import Any

from tdr.domain.models import RunPhase, RunState, stable_id
from tdr.provenance import Repository
from tdr.skills import CATALOG, execute_skill
from .state import next_phase


class DiscoveryEngine:
    def __init__(self, project_dir: str | Path):
        self.repository = Repository(project_dir)

    def create_run(self, context_id: str = "pending-context", budget: dict[str, float] | None = None) -> RunState:
        state = RunState(
            run_id=stable_id("run"),
            context_id=context_id,
            budget_remaining=dict(budget or {"steps": 50.0, "wall_seconds": 3600.0}),
        )
        self.repository.save_run(state)
        return state

    def load_run(self, run_id: str) -> RunState:
        return RunState(**self.repository.load_run(run_id))

    def execute(self, run_id: str, skill_name: str, payload: dict[str, Any]) -> dict[str, Any]:
        state = self.load_run(run_id)
        if state.budget_remaining.get("steps", 1.0) <= 0:
            state.phase = RunPhase.BLOCKED.value
            state.terminal_reason = "step budget exhausted"
            self.repository.save_run(state)
            return {"status": "blocked", "messages": [state.terminal_reason], "artifacts": [], "claims": [], "uncertainties": [], "next": [], "provenance": {}}

        output = execute_skill(skill_name, payload)
        role = CATALOG[skill_name].role
        event = self.repository.append_event(run_id, skill_name, role, payload, output)
        state.budget_remaining["steps"] = state.budget_remaining.get("steps", 1.0) - 1.0
        state.artifact_ids.append(event["result_hash"])
        state = next_phase(state, skill_name, output)
        if skill_name == "scope-research-context" and output.get("artifacts"):
            state.context_id = str(output["artifacts"][0].get("context_id", state.context_id))
        self._persist_typed_artifacts(output)
        self._route_repeated_failure(state)
        self.repository.save_run(state)
        return output

    def _persist_typed_artifacts(self, output: dict[str, Any]) -> None:
        id_keys = {
            "context_id": "context",
            "fragment_id": "fragment",
            "morphism_id": "morphism",
            "cell_id": "higher_cell",
            "pressure_id": "pressure",
            "profile_id": "meaning_profile",
            "site_id": "fragmentation_site",
            "reflection_id": "reflection",
            "candidate_id": "candidate",
            "validation_id": "validation",
            "mutation_id": "representation_mutation",
            "portfolio_id": "portfolio",
            "audit_id": "audit",
        }
        for artifact in output.get("artifacts", []):
            if not isinstance(artifact, dict):
                continue
            for key, record_type in id_keys.items():
                if artifact.get(key):
                    value = dict(artifact)
                    value.setdefault("record_id", artifact[key])
                    self.repository.save_record(value, record_type)
                    break

    def _route_repeated_failure(self, state: RunState) -> None:
        reasons = Counter(item.get("reason") for item in state.failures)
        if any(count >= 3 for count in reasons.values()) and state.phase in {RunPhase.FORMALIZED.value, RunPhase.TESTED.value}:
            state.phase = RunPhase.REPRESENTATION_REVIEW.value
            state.revision += 1

    def inspect(self, run_id: str) -> dict[str, Any]:
        return {"state": self.repository.load_run(run_id), "events": self.repository.run_events(run_id)}

    def replay(self, run_id: str, *, verify_only: bool = True) -> dict[str, Any]:
        def normalized(value: Any) -> Any:
            if isinstance(value, dict):
                return {key: normalized(item) for key, item in value.items() if key != "created_at"}
            if isinstance(value, list):
                return [normalized(item) for item in value]
            return value

        events = self.repository.run_events(run_id)
        comparisons: list[dict[str, Any]] = []
        for event in events:
            inputs = self.repository.artifacts.get_json(event["input_hash"])
            expected = self.repository.artifacts.get_json(event["result_hash"])
            actual = execute_skill(event["skill_name"], inputs)
            comparisons.append({
                "sequence": event["sequence"],
                "skill_name": event["skill_name"],
                "equivalent": normalized(expected) == normalized(actual),
                "would_write": not verify_only,
            })
        return {"run_id": run_id, "verified": all(item["equivalent"] for item in comparisons), "events": comparisons}

    def run_demo(self) -> dict[str, Any]:
        state = self.create_run()
        run_id = state.run_id
        context_result = self.execute(run_id, "scope-research-context", {
            "question": "When is a multilinear interaction best represented by a universal object?",
            "goals": ["unblock factorization proofs", "transport bilinear constructions"],
            "scope": {"domain": "modules over a commutative ring", "regime": "algebraic"},
            "protected_commitments": ["bilinearity", "unique factorization through the universal map"],
        })
        fragment_result = self.execute(run_id, "map-theory-fragment", {
            "name": "Bilinear maps",
            "sources": [{"artifact_id": "demo-source", "locator": "demo", "content": "Sort: Module\nSymbol: bilinear : M x N -> P\nAxiom: bilinear preserves addition in each variable\nClaim: bilinear maps should factor through one linear map\nScope: modules over a commutative ring"}],
        })
        pressure_result = self.execute(run_id, "interpret-conceptual-pressure", {
            "events": [{
                "description": "Proofs repeatedly cannot derive a unique linear factorization from raw bilinear maps.",
                "locus": ["bilinear_map", "factorization_lemma"],
                "severity": 0.9,
                "reliability": 0.9,
                "evidence": [{"evidence_type": "proof", "reliability": 0.9}],
            }],
            "dependency_graph": {"nodes": ["bilinear_map", "factorization_lemma", "homology", "base_change"], "edges": [["bilinear_map", "factorization_lemma"], ["factorization_lemma", "homology"], ["factorization_lemma", "base_change"]]},
        })
        profile_a = execute_skill("profile-concept-meaning", {
            "concept_id": "bilinear-interaction", "theory_id": "raw-maps",
            "referential_role": ["a two-input function"], "inferential_commitments": ["linear in each variable"],
            "identity_criteria": ["pointwise equality"], "modal_commitments": ["varies with codomain"],
            "operational_anchors": ["evaluate on pairs"], "scale_and_scope": ["modules over R"],
            "explanatory_role": ["couples two inputs"], "pragmatic_uses": ["define pairings"],
            "protected_distinctions": ["two input positions"],
        })["artifacts"][0]
        profile_b = execute_skill("profile-concept-meaning", {
            "concept_id": "universal-representer", "theory_id": "linear-maps",
            "referential_role": ["an object representing a functor"], "inferential_commitments": ["unique factorization"],
            "identity_criteria": ["unique isomorphism"], "modal_commitments": ["natural in codomain"],
            "operational_anchors": ["compose one linear map"], "scale_and_scope": ["R-linear category"],
            "explanatory_role": ["explains all bilinear maps universally"], "pragmatic_uses": ["transport and compute"],
            "protected_distinctions": ["universal property"],
        })["artifacts"][0]
        site_result = self.execute(run_id, "detect-essential-fragmentation", {
            "profiles": [profile_a, profile_b], "downstream_impact": 0.95,
            "downstream_targets": ["factorization_lemma", "homology", "base_change"],
        })
        site = site_result["artifacts"][0]
        reflection_result = self.execute(run_id, "run-philosophical-reflection", {"site": site, "profiles": [profile_a, profile_b]})
        reflection = reflection_result["artifacts"][0]
        defect_result = self.execute(run_id, "diagnose-categorical-defect", {"site": site, "reflection": reflection})
        generation_result = self.execute(run_id, "generate-theory-candidates", {
            "pressures": pressure_result["artifacts"], "reflections": [reflection], "defects": defect_result["artifacts"], "seed": 7,
        })
        candidates = generation_result["artifacts"]
        relevance_result = self.execute(run_id, "evaluate-relevance", {
            "candidates": candidates, "context": context_result["artifacts"][0],
            "dependency_graph": {"nodes": ["bilinear_map", "factorization_lemma", "homology", "base_change"], "reachable_from_pressure": ["factorization_lemma", "homology", "base_change"]},
        })
        frontier_ids = next(item["frontier"] for item in relevance_result["artifacts"] if "frontier" in item)
        candidate = next(item for item in candidates if item["candidate_id"] == frontier_ids[0])
        formal_result = self.execute(run_id, "formalize-candidate", {"candidate": candidate})
        concrete_result = self.execute(run_id, "instantiate-concretely", {"candidate": candidate, "targets": [{"name": "free finite modules", "assumptions": ["finite rank"]}]})
        adversarial_result = self.execute(run_id, "falsify-candidate", {
            "candidate": candidate,
            "test_results": {"degenerate_case": "passed", "scope_boundary": "passed", "rival_explanation": "passed", "protected_loss": "passed"},
        })
        evaluations = [item for item in relevance_result["artifacts"] if item.get("candidate_id")]
        validations = [formal_result["artifacts"][0], concrete_result["artifacts"][0], adversarial_result["artifacts"][0]]
        synthesis_result = self.execute(run_id, "synthesize-portfolio", {"candidates": candidates, "evaluations": evaluations, "validations": validations})
        return {"run_id": run_id, "phase": self.load_run(run_id).phase, "candidate_count": len(candidates), "synthesis": synthesis_result["artifacts"][0], "fragment_id": fragment_result["artifacts"][0]["fragment_id"]}
