# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Author target-specific initialization content through the selected host model.

The first pass sees only the target and its commitments. The second pass reads
the frozen acquisition and explicitly rebases those conjectures. Source records
remain immutable; judgments of relevance and credibility are separate artifacts.
All operator-owned IDs, seals, state transitions and receipts are computed by
the existing deterministic producers, never requested from the language model.
"""
from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any, Mapping

from .contracts import ContractError, canonical_digest, stable_identifier
from .hypotheses import forge_high_risk_portfolio
from .model_author import ModelAuthor


SPEC = Path(__file__).resolve().parents[1] / "spec"
TARGETS = {
    "markov-kakutani-fixed-point-theorem-target": {
        "topic": "Markov Kakutani fixed point theorem",
        "statement": "Reconstruct the known finite-family Markov-Kakutani theorem: every finite pairwise commuting family of continuous affine self-maps of a nonempty compact convex subset K of a Hausdorff locally convex real topological vector space has a common fixed point.",
        "commitments": [
            "This is reconstruction and validation of a known theorem, not a claim of novel discovery.",
            "Preserve nonemptiness, compactness, convexity, continuity, affinity, self-map invariance and pairwise commutativity.",
            "Use KB/markov-kakutani-fixed-point-theorem.kb.md, especially st.lem.finite-family-common-fixed-point, as the repository target; distinguish finite-dimensional examples from the general locally convex theorem.",
            "Explain Cesaro averaging, the fixed-set invariance bridge and finite-family induction; use convergent subnets when compactness does not imply sequential compactness.",
            "Check explicit counterexamples after removing assumptions, and do not infer a general theorem from a numerical example.",
        ],
    },
    "p-vs-np-target": {
        "topic": "P versus NP",
        "statement": "Determine whether deterministic polynomial-time decision (P) equals nondeterministic polynomial-time decision (NP).",
        "commitments": [
            "Preserve uniform algorithms, worst-case bounds, all input lengths and the stated computational model.",
            "Distinguish restricted circuit/formula lower bounds from general P versus NP.",
            "State reduction overheads, quantifier order, and relativization, natural-proofs and algebrization limits where applicable.",
        ],
    },
    "yang-mills-existence-and-mass-gap-target": {
        "topic": "Yang-Mills existence and mass gap",
        "statement": "Construct a nontrivial quantum Yang-Mills theory on four-dimensional Euclidean space for every compact simple gauge group, with the required reconstruction axioms and a positive mass gap.",
        "commitments": [
            "Preserve the same nontrivial gauge theory through regulator removal and reconstruction.",
            "Distinguish fixed-cutoff or finite-volume estimates from a uniform continuum and infinite-volume construction.",
            "State gauge-invariant observables, positivity, topology, limit order and the spectral-gap interface explicitly.",
        ],
    },
}


def target_context(target_id: str) -> dict[str, Any]:
    if target_id not in TARGETS:
        raise ContractError("automatic initialization is not registered for this target")
    return {"target_id": target_id, **copy.deepcopy(TARGETS[target_id])}


def object_schema(properties: Mapping[str, Any]) -> dict[str, Any]:
    return {"type": "object", "additionalProperties": False,
            "required": list(properties), "properties": dict(properties)}


def array_schema(items: Mapping[str, Any], minimum=1, maximum=12) -> dict[str, Any]:
    return {"type": "array", "minItems": minimum, "maxItems": maximum, "items": dict(items)}


TEXT = {"type": "string", "minLength": 1}


def schema_fragment(name: str, pointer: str) -> dict[str, Any]:
    """Inline only reachable local schema definitions for a compact model task."""
    def resolve(value, path, seen):
        if isinstance(value, list):
            return [resolve(row, path, seen) for row in value]
        if not isinstance(value, dict):
            return value
        if "$ref" in value:
            reference = value["$ref"]
            file, _, fragment = reference.partition("#")
            destination = (path.parent / file).resolve() if file else path
            destination.relative_to(SPEC.resolve())
            identity = (str(destination), fragment)
            if identity in seen:
                raise ContractError("recursive schema is not supported in a bounded authoring task")
            node = json.loads(destination.read_text())
            for part in fragment.strip("/").split("/") if fragment else []:
                node = node[part.replace("~1", "/").replace("~0", "~")]
            return resolve(node, destination, {*seen, identity})
        return {key: resolve(row, path, seen) for key, row in value.items()
                if key not in {"$schema", "$id", "$defs"}}
    return resolve({"$ref": "#" + pointer}, SPEC / name, set())


def author_charter(author: ModelAuthor) -> dict[str, Any]:
    """Freeze a target-specific charter before any acquired literature is shown."""
    target = target_context(author.identity["target_id"])
    name = "reflective_conceptual_discovery_packet.schema.json"
    schema = object_schema({
        "discovery_charter": schema_fragment(name, "/$defs/charter"),
        "conceptual_genealogy": schema_fragment(name, "/$defs/genealogy"),
        "root_tensions": array_schema(schema_fragment(name, "/$defs/tension"), 2, 4),
        "explicit_unknowns": array_schema(TEXT),
    })
    def validate(value):
        if not set(target["commitments"]).issubset(value["discovery_charter"]["target_commitments"]):
            raise ContractError("charter must preserve each exact supplied target commitment")
        if value["discovery_charter"]["bottleneck_diagnosis"] == "not_conceptual":
            raise ContractError("initialization needs explicit conceptual questions; do not assert the target is resolved")
        if not value["conceptual_genealogy"]["protected_successes"]:
            raise ContractError("charter must name protected known special cases or definitions")
    return author.author("target-charter", instruction=(
        "Write a research charter for the exact target. Include every supplied commitment verbatim. "
        "Name 2–4 concrete root tensions, their strongest opposed commitments and missing mediation. "
        "Historical background from model knowledge is provisional until checked against acquired sources. "
        "Do not propose a preferred solution or claim current literature was searched."),
        inputs=target, schema=schema, validator=validate, max_tokens=9000)


def high_risk_charter(target_id: str, theory_digest: str, authored_charter: Mapping[str, Any]) -> dict[str, Any]:
    value = authored_charter["value"]
    target = target_context(target_id)
    charter = {"target_id": target_id, "target_statement": target["statement"],
            "theory_state_digest": theory_digest,
            "root_tensions": [row["minimal_incompatibility_or_missing_mediation"] for row in value["root_tensions"]],
            "target_commitments": value["discovery_charter"]["target_commitments"],
            "protected_successes": value["conceptual_genealogy"]["protected_successes"],
            "forbidden_target_drift": " ".join(target["commitments"])}
    if target_id == "markov-kakutani-fixed-point-theorem-target":
        # The portfolio contract supports explicit absence of viable wildcards.
        # A known-theorem reconstruction must not invent low confidence or
        # relax exact commutativity just to satisfy a frontier-search policy.
        charter.update(wildcards_available=False, fewer_wildcards_reason=(
            "This target reconstructs an established finite-family theorem. Its exact "
            "proof mechanisms are known, while approximate-commutation extensions "
            "change the target. Two genuinely low-confidence, high-upside in-scope "
            "wildcards are not warranted; retain the conservative proof and explicit "
            "assumption/counterexample audits without inventing scientific novelty."
        ))
    return charter


def proposal_schema() -> dict[str, Any]:
    """Require every conceptual field so the source forger supplies no ideas."""
    candidate = schema_fragment("high_risk_hypothesis_portfolio.schema.json", "/$defs/candidate")
    computed = {"hypothesis_id", "concept_lifecycle_state", "maturation_status", "truth_status",
                "intuition_provenance", "target_commitments", "protected_successes",
                "literature_relation", "literature_source_ids", "literature_rebase_receipt",
                "blind_articulation_digest", "novelty_claim", "branch_independence_signature",
                "genealogy", "structural_signature", "selection_status"}
    return object_schema({key: value for key, value in candidate["properties"].items() if key not in computed})


def author_blind_proposals(author: ModelAuthor, charter: Mapping[str, Any]) -> dict[str, Any]:
    """Generate ideas without exposing retrieved sources or an incumbent deck."""
    schema = object_schema({"proposals": array_schema(proposal_schema(), 10, 10)})
    def validate(value):
        rows = value["proposals"]
        if len({row["corner_family"] for row in rows if not row["is_control"]}) < 6:
            raise ContractError("hypotheses must cover at least six distinct conceptual corners")
        if sum(row["is_control"] for row in rows) != 1:
            raise ContractError("hypotheses need exactly one conservative control")
        if len({row["mechanism_key"] for row in rows}) != len(rows):
            raise ContractError("hypotheses must have distinct mechanism identifiers")
        if not any(row["is_wildcard"] and not row["is_control"] for row in rows):
            raise ContractError("retain at least one explicitly speculative wildcard")
        if any(row["is_control"] != (row["corner_family"] == "conservative_control") for row in rows):
            raise ContractError("control flags must match their conceptual corner")
    return author.author("blind-hypotheses", instruction=(
        "Articulate ten target-specific conjectures across at least six distinct conceptual corners, "
        "including exactly one conservative control and one or two high-upside wildcards. "
        "You have not seen the acquired literature. Do not claim literature distance or novelty is measured; "
        "scores are provisional internal judgments, with literature_distance=0 until rebase. "
        "Write an actual mechanism, primitive, falsifier and boundary case for each; no generic renamed obstruction. "
        "Preserve target commitments and use non-circular maturation questions. Keep each proposal concise."),
        inputs={"charter": charter}, schema=schema, validator=validate, max_tokens=24000)


def author_source_assessment(author: ModelAuthor, snapshot: Mapping[str, Any]) -> dict[str, Any]:
    """Judge every retrieved source without rewriting acquisition or source status."""
    ids = [source["source_id"] for source in snapshot["sources"]]
    row = object_schema({"source_id": {"enum": ids},
        "relevance": {"enum": ["direct", "adjacent", "irrelevant", "unclear"]},
        "source_excerpt": TEXT, "reason": TEXT,
        "credibility_concerns": array_schema(TEXT, 0), "usable_for": array_schema(TEXT, 0),
        "claims_verified": {"const": False}})
    schema = object_schema({"assessments": array_schema(row, len(ids), len(ids)),
                            "coverage_limitations": array_schema(TEXT)})
    by_id = {source["source_id"]: source for source in snapshot["sources"]}
    def validate(value):
        if sorted(item["source_id"] for item in value["assessments"]) != sorted(ids):
            raise ContractError("source assessment must cover each acquired source exactly once")
        grounded = 0
        for item in value["assessments"]:
            source = by_id[item["source_id"]]
            texts = [source["title"], *source["claims"]]
            if not any(item["source_excerpt"] in text for text in texts):
                raise ContractError("source assessment excerpt is absent from the acquired title/abstract")
            if item["relevance"] in {"direct", "adjacent"} and source["claims"]:
                grounded += 1
        if not grounded:
            raise ContractError("acquired sources do not contain a relevant abstract; refine acquisition before research")
    return author.author("source-assessment", instruction=(
        "Assess each retrieved source against the target, using only its supplied title and abstract. "
        "Copy a short exact excerpt supporting the assessment. Identify irrelevant search noise, unsupported "
        "solution claims, correction/retraction uncertainty, and what cannot be inferred without full text. "
        "No claims are independently verified here. A source claiming to solve the target must never be "
        "accepted as established. Keep source metadata, acquisition times and unknown correction status unchanged."),
        inputs={"target": target_context(author.identity["target_id"]), "snapshot_id": snapshot["snapshot_id"],
                "snapshot_digest": snapshot["content_digest"], "sources": snapshot["sources"]},
        schema=schema, validator=validate, max_tokens=14000)


def author_rebase(author: ModelAuthor, *, snapshot: Mapping[str, Any], charter: Mapping[str, Any],
                  blind: Mapping[str, Any], assessment: Mapping[str, Any]) -> dict[str, Any]:
    """Preserve the blind ideas while adding an explicit, bounded source relation."""
    proposals = blind["value"]["proposals"]
    keys = [row["mechanism_key"] for row in proposals]
    eligible = {row["source_id"] for row in assessment["value"]["assessments"]
                if row["relevance"] in {"direct", "adjacent"}}
    row = object_schema({"mechanism_key": {"enum": keys},
        "literature_relation": {"enum": ["partly_anticipated", "cross_field_bridge", "coverage_unknown"]},
        "source_ids": array_schema({"enum": sorted(eligible)}, 0, 4),
        "rationale": TEXT, "remaining_checks": array_schema(TEXT)})
    def validate(value):
        if sorted(row["mechanism_key"] for row in value["rebases"]) != sorted(keys):
            raise ContractError("rebase must cover each frozen blind hypothesis exactly once")
        if any(row["literature_relation"] != "coverage_unknown" and not row["source_ids"] for row in value["rebases"]):
            raise ContractError("a non-unknown literature relation needs acquired source references")
    return author.author("hypothesis-rebase", instruction=(
        "Rebase the exact blind hypotheses against assessed source abstracts. Preserve every blind idea; "
        "add only its closest bounded literature relation, source IDs, rationale, and unresolved checks. "
        "A search miss cannot establish novelty or apparent openness; use coverage_unknown. "
        "Do not infer entailment or contradiction from incomplete abstracts. No source is verified."),
        inputs={"charter": charter, "blind_proposals": proposals, "assessment": assessment["value"],
                "sources": [source for source in snapshot["sources"] if source["source_id"] in eligible]},
        schema=object_schema({"rebases": array_schema(row, len(keys), len(keys))}),
        validator=validate, max_tokens=9000)


def compile_proposals(*, charter: Mapping[str, Any], blind: Mapping[str, Any], rebase: Mapping[str, Any]) -> list[dict[str, Any]]:
    """Add only deterministic bookkeeping to the fully authored conceptual fields."""
    relations = {row["mechanism_key"]: row for row in rebase["value"]["rebases"]}
    proposals = []
    for raw in blind["value"]["proposals"]:
        row = copy.deepcopy(raw)
        identity = stable_identifier("hypothesis", charter["target_id"], blind["content_digest"], raw["mechanism_key"])
        relation = relations[raw["mechanism_key"]]
        row.update({"hypothesis_id": identity, "concept_lifecycle_state": "conceptually_articulated",
            "maturation_status": "theory_question_open" if row["is_control"] else "parallel_ready",
            "truth_status": "conjectural", "novelty_claim": False,
            "intuition_provenance": {"mode": "blind_intuition_first", "trigger": row["target_pressures_addressed"][0],
                                     "pre_literature_statement": row["intuitive_leap"]},
            "target_commitments": list(charter["target_commitments"]), "protected_successes": list(charter["protected_successes"]),
            "literature_relation": relation["literature_relation"], "literature_source_ids": relation["source_ids"],
            "genealogy": [stable_identifier("model-articulation", blind["content_digest"], identity)],
            "branch_independence_signature": {
                "unique_primitives": row["ontology_delta"]["new_primitives"], "unique_mechanism": row["mechanism"],
                "forbidden_cross_branch_context": ["Other branch results before the divergence barrier"],
                "required_context": ["Frozen target charter", "Frozen literature acquisition and assessment"],
                "overlaps_with_hypothesis_ids": []}})
        proposals.append(row)
    return proposals


def produce_portfolio(*, charter: Mapping[str, Any], snapshot: Mapping[str, Any],
                      blind: Mapping[str, Any], rebase: Mapping[str, Any]) -> dict[str, Any]:
    """Execute the original rebase, diversity, Pareto and wildcard producer."""
    return forge_high_risk_portfolio(charter, snapshot,
        proposals=compile_proposals(charter=charter, blind=blind, rebase=rebase), requested_count=10)
