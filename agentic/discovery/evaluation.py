# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Independent structural evaluation of reflective discovery deltas.

Creative worth is plural and Pareto-shaped.  It is deliberately kept separate
from proof/evidence authority and from literature-novelty authority.
"""

from __future__ import annotations

import re
from collections import Counter, defaultdict
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

from agentic.discovery.contracts import ContractError, canonical_digest, stable_identifier, utc_now, validate_payload


SCHEMA = Path(__file__).resolve().parents[1] / "spec" / "discovery_evaluation_receipt.schema.json"
DIMENSIONS = (
    "conceptual_depth",
    "explanatory_understanding",
    "unification",
    "preserved_difference",
    "generativity",
    "coherence",
    "truth_aptness",
)
CONCEPTUAL_GATE_IDS = (
    "G0_essential_relevance",
    "G0L_literature_rebase",
    "G1_genuine_transformation",
    "G2_philosophical_depth",
    "G3_unification",
    "G4_understanding_gain",
    "G5_reflective_resilience",
    "G6_truth_apt_articulation",
)
EVALUATION_ROLES = frozenset({"diagnostic", "conceptual_gate"})

# These are semantic release floors, not weights.  A candidate must clear every
# coordinate to be preferred; strength on one virtue cannot compensate for a
# missing mechanism, erased difference, or non-correctable claim on another.
PREFERENCE_FLOORS = {
    "conceptual_depth": 0.70,
    "explanatory_understanding": 0.70,
    "unification": 0.65,
    "preserved_difference": 0.75,
    "generativity": 0.65,
    "coherence": 0.50,
    "truth_aptness": 0.65,
}

_TOKEN = re.compile(r"[A-Za-z][A-Za-z0-9]*")
_PLACEHOLDERS = frozenset(
    {
        "x",
        "y",
        "z",
        "foo",
        "bar",
        "baz",
        "tbd",
        "todo",
        "placeholder",
        "dummy",
        "thing",
        "stuff",
        "text",
        "label",
        "item",
        "value",
        "unknown",
        "none",
        "na",
    }
)


def _rows(value: Any) -> list[Mapping[str, Any]]:
    return [row for row in value if isinstance(row, Mapping)] if isinstance(value, list) else []


def _texts(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [" ".join(str(item).split()) for item in value if str(item).strip()]


def _norm(value: Any) -> str:
    return " ".join(str(value or "").lower().split())


def _semantic_tokens(value: Any) -> list[str]:
    """Return content-bearing tokens while discarding IDs and placeholders.

    Token identity is never used as a quality signal.  The filter exists only
    to reject empty label-preserving packets such as ``"x"`` or
    ``"YM21-F01: x"`` before their field counts can masquerade as depth.
    """

    output: list[str] = []
    for token in _TOKEN.findall(str(value or "").lower()):
        if token in _PLACEHOLDERS or len(token) == 1:
            continue
        if re.fullmatch(r"(?:ym|dwf|gate|round|system|concept|item)?\d+", token):
            continue
        output.append(token)
    return output


def _meaningful_term(value: Any) -> bool:
    return bool(_semantic_tokens(value))


def _meaningful_statement(value: Any, *, minimum_tokens: int = 4) -> bool:
    tokens = _semantic_tokens(value)
    return len(tokens) >= minimum_tokens and len(set(tokens)) >= min(3, minimum_tokens)


def _valid_relation(row: Mapping[str, Any], relation_key: str = "kind") -> bool:
    source = row.get("source")
    target = row.get("target")
    relation = row.get(relation_key)
    return (
        _meaningful_term(source)
        and _meaningful_term(relation)
        and _meaningful_term(target)
        and _norm(source) != _norm(target)
    )


def _valid_stage(row: Mapping[str, Any]) -> bool:
    return (
        _meaningful_term(row.get("input"))
        and _meaningful_term(row.get("operation"))
        and _meaningful_term(row.get("output"))
        and _norm(row.get("input")) != _norm(row.get("output"))
    )


def _semantic_inventory(candidate: Mapping[str, Any]) -> dict[str, list[Any]]:
    """Collect valid semantic-role occupants without grading their terminology."""

    concepts = _rows(candidate.get("concepts"))
    ontology = candidate.get("ontology", {}) if isinstance(candidate.get("ontology"), Mapping) else {}
    mechanism = candidate.get("mechanism", {}) if isinstance(candidate.get("mechanism"), Mapping) else {}
    understanding = candidate.get("understanding_delta", {}) if isinstance(candidate.get("understanding_delta"), Mapping) else {}
    unification = candidate.get("unification_map", {}) if isinstance(candidate.get("unification_map"), Mapping) else {}
    synthesis = candidate.get("synthesis", {}) if isinstance(candidate.get("synthesis"), Mapping) else {}

    primitive_values = [*_texts(ontology.get("primitives"))]
    primitive_values.extend(
        primitive for concept in concepts for primitive in _texts(concept.get("primitives"))
    )
    primitives = sorted({_norm(value) for value in primitive_values if _meaningful_term(value)})
    relation_rows = _rows(ontology.get("relations")) + [
        row for concept in concepts for row in _rows(concept.get("relations"))
    ]
    relations = [row for row in relation_rows if _valid_relation(row)]
    distinctions = [
        value
        for concept in concepts
        for value in _texts(concept.get("distinctions"))
        if _meaningful_statement(value)
    ]
    stages = [row for row in _rows(mechanism.get("stages")) if _valid_stage(row)]
    causal_edges = [
        row
        for row in _rows(mechanism.get("causal_edges"))
        if _valid_relation(row, "relation")
    ]
    counterfactuals = [
        value
        for value in _texts(mechanism.get("counterfactuals"))
        if _meaningful_statement(value)
    ]
    dependencies = [
        row
        for row in _rows(understanding.get("new_explanatory_dependencies"))
        if _valid_relation(row, "relation")
    ]
    questions = [
        value
        for value in [*_texts(candidate.get("new_questions")), *_texts(understanding.get("new_questions"))]
        if _meaningful_statement(value)
    ]
    mappings = [
        row
        for row in _rows(unification.get("mappings"))
        if _meaningful_term(row.get("source_system"))
        and _meaningful_term(row.get("bridge"))
        and _meaningful_term(row.get("target_system"))
        and _norm(row.get("source_system")) != _norm(row.get("target_system"))
    ]
    differences = [
        value
        for value in _texts(unification.get("preserved_differences"))
        if _meaningful_statement(value)
    ]
    transformations = [
        value
        for value in _texts(synthesis.get("transformations"))
        if _meaningful_statement(value, minimum_tokens=3)
    ]
    obligations = [
        row
        for row in _rows(candidate.get("obligations"))
        if _meaningful_term(row.get("kind"))
        and _meaningful_term(row.get("depends_on"))
        and _meaningful_statement(row.get("tests"), minimum_tokens=2)
    ]
    predictions = [
        row
        for row in _rows(candidate.get("predictions"))
        if _meaningful_term(row.get("observable"))
        and _meaningful_statement(row.get("condition"), minimum_tokens=2)
        and _meaningful_statement(row.get("direction"), minimum_tokens=2)
    ]
    reflection_rounds = [
        row
        for row in _rows(candidate.get("reflection_rounds"))
        if row.get("result") in {"mutated", "synthesized", "demoted"}
        and any(
            _meaningful_statement(value, minimum_tokens=2)
            for value in row.get("mutation_or_synthesis", {}).get(
                "changed_primitives_relations_or_explanation", []
            )
        )
        and any(_meaningful_statement(value) for value in row.get("strongest_objections", []))
    ]
    return {
        "primitives": primitives,
        "relations": relations,
        "distinctions": distinctions,
        "stages": stages,
        "causal_edges": causal_edges,
        "counterfactuals": counterfactuals,
        "dependencies": dependencies,
        "questions": questions,
        "mappings": mappings,
        "differences": differences,
        "transformations": transformations,
        "obligations": obligations,
        "predictions": predictions,
        "reflection_rounds": reflection_rounds,
    }


def _structural_profile(candidate: Mapping[str, Any]) -> tuple[tuple[str, int], ...]:
    """Return a terminology-invariant semantic-role profile.

    Renaming every primitive and relation consistently leaves this profile
    unchanged.  Deleting a mediator, mechanism stage, preserved distinction,
    correction-bearing round, or other semantic role changes it.
    """

    inventory = _semantic_inventory(candidate)
    return tuple(sorted((role, len(rows)) for role, rows in inventory.items()))


def _anonymous_graph_signature(candidate: Mapping[str, Any]) -> dict[str, Any]:
    """Return a terminology-invariant typed conceptual-graph signature.

    Nodes begin with semantic-role colours and are refined from the direction
    and class of incident edges.  Names never enter the final signature, so a
    consistent vocabulary substitution is invisible; changing mediation,
    explanatory dependency, stage composition, or unification topology is not.
    This is an auditable structural discriminator, not a claim that graph
    isomorphism by itself judges philosophical worth.
    """

    inventory = _semantic_inventory(candidate)
    node_roles: dict[str, set[str]] = defaultdict(set)
    edges: list[tuple[str, str, str]] = []

    def node(value: Any, role: str) -> str:
        key = _norm(value)
        if _meaningful_term(key):
            node_roles[key].add(role)
            return key
        return ""

    def edge(source: Any, target: Any, kind: str) -> None:
        left = node(source, f"{kind}_source")
        right = node(target, f"{kind}_target")
        if left and right and left != right:
            edges.append((left, kind, right))

    for primitive in inventory["primitives"]:
        node(primitive, "primitive")
    for value in _texts(candidate.get("relevance", {}).get("target_dependencies")):
        node(value, "target_dependency")
    for value in _texts(candidate.get("relevance", {}).get("root_tensions")):
        node(value, "root_tension")
    for row in inventory["relations"]:
        edge(row.get("source"), row.get("target"), "typed_relation")
    for row in inventory["stages"]:
        edge(row.get("input"), row.get("output"), "mechanism_stage")
    for row in inventory["causal_edges"]:
        edge(row.get("source"), row.get("target"), "causal_edge")
    for row in inventory["dependencies"]:
        edge(row.get("source"), row.get("target"), "explanatory_dependency")
    for row in inventory["mappings"]:
        edge(row.get("source_system"), row.get("target_system"), "unification_mapping")

    colours = {
        key: canonical_digest(sorted(roles))
        for key, roles in node_roles.items()
    }
    incident: dict[str, list[tuple[str, str, str]]] = defaultdict(list)
    for source, kind, target in edges:
        incident[source].append(("out", kind, target))
        incident[target].append(("in", kind, source))
    for _ in range(max(1, len(node_roles))):
        refined = {
            key: canonical_digest(
                {
                    "self": colours[key],
                    "neighbours": sorted(
                        (direction, kind, colours[other])
                        for direction, kind, other in incident.get(key, [])
                    ),
                }
            )
            for key in node_roles
        }
        if refined == colours:
            break
        colours = refined

    undirected: dict[str, set[str]] = defaultdict(set)
    incoming: Counter[str] = Counter()
    outgoing: Counter[str] = Counter()
    for source, _, target in edges:
        undirected[source].add(target)
        undirected[target].add(source)
        outgoing[source] += 1
        incoming[target] += 1
    seen: set[str] = set()
    component_sizes: list[int] = []
    for start in sorted(node_roles):
        if start in seen:
            continue
        frontier = [start]
        size = 0
        while frontier:
            current = frontier.pop()
            if current in seen:
                continue
            seen.add(current)
            size += 1
            frontier.extend(sorted(undirected[current] - seen))
        component_sizes.append(size)
    node_colours = sorted(Counter(colours.values()).items())
    edge_colours = sorted(
        Counter((colours[source], kind, colours[target]) for source, kind, target in edges).items()
    )
    signature_material = {
        "node_colours": node_colours,
        "edge_colours": edge_colours,
        "component_sizes": sorted(component_sizes),
        "mediator_count": sum(
            incoming[key] > 0 and outgoing[key] > 0 for key in node_roles
        ),
    }
    return {
        **signature_material,
        "node_count": len(node_roles),
        "edge_count": len(edges),
        "signature_digest": canonical_digest(signature_material),
    }


def _semantic_facet_digests(candidate: Mapping[str, Any]) -> dict[str, str]:
    """Bind decision-bearing content by facet without turning words into scores."""

    inventory = _semantic_inventory(candidate)
    facets: dict[str, Any] = {
        "mechanism": {
            "stages": inventory["stages"],
            "causal_edges": inventory["causal_edges"],
            "counterfactuals": inventory["counterfactuals"],
        },
        "explanation": {
            "dependencies": inventory["dependencies"],
            "understanding": candidate.get("understanding_delta", {}),
        },
        "unification_and_difference": {
            "mappings": inventory["mappings"],
            "differences": inventory["differences"],
        },
        "generativity": {
            "questions": inventory["questions"],
            "obligations": inventory["obligations"],
            "predictions": inventory["predictions"],
        },
        "reflective_transformation": {
            "transformations": inventory["transformations"],
            "rounds": inventory["reflection_rounds"],
        },
        "truth_boundary": {
            "correction_conditions": candidate.get("correction_conditions", []),
            "falsifiers": candidate.get("falsifiers", []),
            "scope_conditions": candidate.get("scope_conditions", []),
        },
    }
    return {name: canonical_digest(value) for name, value in facets.items()}


def structural_atoms(candidate: Mapping[str, Any]) -> set[str]:
    """Extract terminology-invariant role and anonymous-topology atoms."""

    atoms = {
        f"{role}-slot:{index}"
        for role, count in _structural_profile(candidate)
        for index in range(count)
    }
    graph = _anonymous_graph_signature(candidate)
    if graph["node_count"] and graph["edge_count"]:
        atoms.add(f"anonymous-topology:{graph['signature_digest']}")
    return atoms


def semantic_delta_evidence(
    before: Mapping[str, Any] | None, after: Mapping[str, Any]
) -> dict[str, Any]:
    """Describe a pairwise semantic-role delta without using vocabulary drift."""

    after_atoms = structural_atoms(after)
    after_graph = _anonymous_graph_signature(after)
    after_profile = dict(_structural_profile(after))
    after_facets = _semantic_facet_digests(after)
    if before is None:
        return {
            "applicability": "not_applicable",
            "reason": "the first diagnostic evaluation has no predecessor candidate",
            "baseline_digest": None,
            "candidate_digest": canonical_digest(after),
            "added_roles": sorted(after_atoms),
            "removed_roles": [],
            "changed_role_families": [],
            "anonymous_topology_changed": False,
            "changed_semantic_facets": [],
            "new_material_reflection_rounds": 0,
            "material": False,
        }
    before_atoms = structural_atoms(before)
    before_graph = _anonymous_graph_signature(before)
    before_profile = dict(_structural_profile(before))
    before_facets = _semantic_facet_digests(before)
    added = sorted(after_atoms - before_atoms)
    removed = sorted(before_atoms - after_atoms)
    role_families = sorted(
        role
        for role in set(before_profile) | set(after_profile)
        if before_profile.get(role, 0) != after_profile.get(role, 0)
    )
    topology_changed = (
        before_graph["signature_digest"] != after_graph["signature_digest"]
    )
    facet_changes = sorted(
        name for name in after_facets if after_facets[name] != before_facets[name]
    )
    new_rounds = max(
        0,
        after_profile.get("reflection_rounds", 0)
        - before_profile.get("reflection_rounds", 0),
    )
    # A lone extra slot is padding, not discovery.  Materiality requires either
    # an objection-bearing transformation round, or a topology change supported
    # by more than one decision-bearing semantic facet/role family.
    material = (
        (new_rounds > 0 and "reflective_transformation" in facet_changes)
        or (
            topology_changed
            and len(set(role_families) | set(facet_changes)) >= 2
        )
    )
    return {
        "applicability": "applicable",
        "reason": (
            "typed conceptual topology and decision-bearing facets changed"
            if material
            else "only terminology, ordering, unsupported same-role content, or isolated padding changed"
        ),
        "baseline_digest": canonical_digest(before),
        "candidate_digest": canonical_digest(after),
        "added_roles": added,
        "removed_roles": removed,
        "changed_role_families": role_families,
        "anonymous_topology_changed": topology_changed,
        "before_topology_digest": before_graph["signature_digest"],
        "after_topology_digest": after_graph["signature_digest"],
        "changed_semantic_facets": facet_changes,
        "new_material_reflection_rounds": new_rounds,
        "material": material,
    }


def structural_novelty(candidate: Mapping[str, Any], genealogy: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    """Compare typed conceptual structure, never vocabulary distance."""

    candidate_atoms = structural_atoms(candidate)
    candidate_profile = _structural_profile(candidate)
    candidate_graph = _anonymous_graph_signature(candidate)
    candidate_inventory = _semantic_inventory(candidate)
    has_conceptual_core = (
        len(candidate_inventory["primitives"]) >= 1
        and len(candidate_inventory["relations"]) >= 1
        and len(candidate_inventory["stages"]) >= 1
    )
    matched: list[str] = []
    prior_union: set[str] = set()
    exact = False
    for record in genealogy:
        record_atoms = structural_atoms(record)
        prior_union.update(record_atoms)
        record_graph = _anonymous_graph_signature(record)
        if (
            candidate_atoms
            and candidate_profile == _structural_profile(record)
            and candidate_graph["signature_digest"] == record_graph["signature_digest"]
        ):
            exact = True
            matched.append(str(record.get("conceptual_system_id") or record.get("id") or "anonymous"))
        elif candidate_atoms and candidate_atoms.issubset(record_atoms):
            matched.append(str(record.get("conceptual_system_id") or record.get("id") or "anonymous"))
    new_atoms = sorted(candidate_atoms - prior_union)
    if exact or (candidate_atoms and not new_atoms and matched):
        classification = "duplicate"
    elif prior_union and new_atoms:
        classification = "extension"
    elif candidate_atoms and has_conceptual_core:
        classification = "structurally_new"
    elif not candidate_atoms or not has_conceptual_core:
        classification = "undetermined"
    else:
        classification = "undetermined"
    basis = [
        f"valid semantic-role atoms in candidate: {len(candidate_atoms)}",
        f"new semantic-role atoms against genealogy: {len(new_atoms)}",
        f"anonymous typed graph nodes/edges: {candidate_graph['node_count']}/{candidate_graph['edge_count']}",
        "terminology, surface wording, and citation counts were not used as novelty scores",
    ]
    return {
        "classification": classification,
        "new_elements": new_atoms,
        "matched_genealogy_ids": sorted(set(matched)),
        "basis": basis,
    }


def _dimension(score: float, evidence: list[str], unknowns: list[str] | None = None) -> dict[str, Any]:
    return {"score": round(max(0.0, min(1.0, score)), 3), "evidence": evidence, "unknowns": unknowns or []}


def _quality(candidate: Mapping[str, Any], novelty: Mapping[str, Any]) -> dict[str, dict[str, Any]]:
    inventory = _semantic_inventory(candidate)
    mechanism = candidate.get("mechanism", {}) if isinstance(candidate.get("mechanism"), Mapping) else {}
    understanding = candidate.get("understanding_delta", {}) if isinstance(candidate.get("understanding_delta"), Mapping) else {}
    unification = candidate.get("unification_map", {}) if isinstance(candidate.get("unification_map"), Mapping) else {}
    primitives = inventory["primitives"]
    relations = inventory["relations"]
    distinctions = inventory["distinctions"]
    stages = inventory["stages"]
    causal_edges = inventory["causal_edges"]
    counterfactuals = inventory["counterfactuals"]
    graph = _anonymous_graph_signature(candidate)

    def coverage(count: int, required: int) -> float:
        return min(1.0, count / required)

    depth_semantic_core = (
        len(primitives) >= 2
        and len(relations) >= 2
        and len(stages) >= 2
        and graph["mediator_count"] >= 1
    )
    depth_score = (
        sum(
            (
                coverage(len(primitives), 2),
                coverage(len(relations), 2),
                coverage(len(distinctions), 1),
                coverage(len(stages), 2),
                coverage(len(causal_edges), 1),
            )
        )
        / 5
        if depth_semantic_core
        else 0.0
    )
    if novelty["classification"] == "duplicate":
        depth_score = 0.0
    depth_unknowns = []
    if len(primitives) < 2 or len(relations) < 2 or len(stages) < 2:
        depth_unknowns.append("a preferred theory needs at least two meaningful primitives, relations, and mechanism stages")
    depth_evidence = [
        f"{len(primitives)} meaningful primitives",
        f"{len(relations)} meaningful typed relations",
        f"{len(stages)} meaningful mechanism stages",
        f"{graph['mediator_count']} anonymous graph mediators",
        f"minimum semantic core present={depth_semantic_core}",
        f"novelty={novelty['classification']}",
    ]

    before = _norm(understanding.get("before"))
    after = _norm(understanding.get("after"))
    before_after = (
        _meaningful_statement(before)
        and _meaningful_statement(after)
        and before != after
    )
    gain_edges = inventory["dependencies"]
    changed_questions = inventory["questions"]
    understanding_score = sum(
        (
            1.0 if before_after else 0.0,
            coverage(len(gain_edges), 2),
            coverage(len(counterfactuals), 1),
            coverage(len(changed_questions), 1),
        )
    ) / 4
    understanding_unknowns = [] if before_after and len(gain_edges) >= 2 else [
        "understanding needs a substantive before/after contrast and two explanatory dependencies"
    ]
    understanding_evidence = [
        f"substantive before/after distinction={before_after}",
        f"{len(gain_edges)} meaningful explanatory dependencies",
        f"{len(counterfactuals)} meaningful counterfactual tests",
    ]

    mapped_systems: set[str] = set()
    mappings = inventory["mappings"]
    for row in mappings:
        mapped_systems.update(filter(None, [str(row.get("source_system") or ""), str(row.get("target_system") or "")]))
    differences = inventory["differences"]
    bridge_coverage = (
        sum(_meaningful_term(row.get("bridge")) for row in mappings) / len(mappings)
        if mappings
        else 0.0
    )
    unification_score = sum(
        (
            coverage(len(mappings), 2),
            coverage(len(mapped_systems), 3),
            bridge_coverage,
        )
    ) / 3
    preserved_score = coverage(len(differences), 2)
    unification_evidence = [f"{len(mapped_systems)} systems connected", f"{len(mappings)} explicit mappings"]
    preserved_evidence = [f"{len(differences)} substantive differences explicitly preserved"]

    questions = inventory["questions"]
    obligations = inventory["obligations"]
    predictions = inventory["predictions"]
    generativity_score = sum(
        (
            coverage(len(questions), 2),
            coverage(len(obligations), 1),
            coverage(len(predictions), 1),
        )
    ) / 3
    generativity_evidence = [
        f"{len(questions)} consequential questions",
        f"{len(obligations)} typed obligations",
        f"{len(predictions)} scoped predictions",
    ]

    consistency = candidate.get("consistency", {}) if isinstance(candidate.get("consistency"), Mapping) else {}
    raw_unresolved = _texts(consistency.get("unresolved_contradictions"))
    raw_assumptions = _texts(consistency.get("assumptions"))
    unresolved = [value for value in raw_unresolved if _meaningful_statement(value)]
    explicit_assumptions = [
        value for value in raw_assumptions if _meaningful_statement(value, minimum_tokens=2)
    ]
    semantic_core = len(primitives) >= 2 and len(relations) >= 2 and len(stages) >= 2
    coherence_score = (
        max(
            0.0,
            min(
                1.0,
                0.55
                + min(0.35, 0.07 * len(explicit_assumptions))
                - 0.25 * len(unresolved)
                - 0.20
                * ((len(raw_assumptions) - len(explicit_assumptions)) + (len(raw_unresolved) - len(unresolved))),
            ),
        )
        if semantic_core
        else 0.0
    )
    coherence_evidence = [
        f"{len(explicit_assumptions)} substantive explicit assumptions",
        f"{len(unresolved)} substantive unresolved contradictions",
        f"semantic core present={semantic_core}",
    ]

    correction_conditions = [
        value
        for value in _texts(candidate.get("correction_conditions"))
        if _meaningful_statement(value)
    ]
    falsifiers = [
        row
        for row in _rows(candidate.get("falsifiers"))
        if _meaningful_term(row.get("kind"))
        and _meaningful_statement(row.get("claim"), minimum_tokens=3)
    ]
    applicability = [
        value
        for value in _texts(candidate.get("scope_conditions"))
        if _meaningful_statement(value, minimum_tokens=2)
    ]
    truth_score = min(1.0, 0.2 * len(correction_conditions) + 0.2 * len(falsifiers) + 0.12 * len(applicability))
    truth_evidence = [f"{len(correction_conditions)} correction conditions", f"{len(falsifiers)} falsifiers", f"{len(applicability)} scope conditions"]
    return {
        "conceptual_depth": _dimension(depth_score, depth_evidence, depth_unknowns),
        "explanatory_understanding": _dimension(understanding_score, understanding_evidence, understanding_unknowns),
        "unification": _dimension(unification_score, unification_evidence),
        "preserved_difference": _dimension(preserved_score, preserved_evidence),
        "generativity": _dimension(generativity_score, generativity_evidence),
        "coherence": _dimension(coherence_score, coherence_evidence),
        "truth_aptness": _dimension(truth_score, truth_evidence),
    }


def conceptual_gate_vector(packet: Mapping[str, Any]) -> dict[str, str]:
    """Return the complete G0--G6 vector from a reflective packet."""

    raw = packet.get("stage_gates", {})
    gates = raw if isinstance(raw, Mapping) else {}
    return {gate_id: str(gates.get(gate_id, "missing")) for gate_id in CONCEPTUAL_GATE_IDS}


def conceptual_gates_pass(packet: Mapping[str, Any]) -> bool:
    """Require every applicable conceptual gate, never only the attractive pair."""

    return all(status == "pass" for status in conceptual_gate_vector(packet).values())


def _literature(candidate: Mapping[str, Any]) -> dict[str, Any]:
    snapshot = candidate.get("literature_snapshot", {}) if isinstance(candidate.get("literature_snapshot"), Mapping) else {}
    assessments = _rows(candidate.get("source_relation_assessments"))
    target_match = bool(snapshot.get("target_id")) and snapshot.get("target_id") == candidate.get("target_id")
    status = str(snapshot.get("status", "missing"))
    current = status == "validated_current"
    allowed_relations = {"anticipates", "contradicts", "sharpens", "independent", "partially_overlaps"}
    assessments_valid = bool(assessments) and all(row.get("relation") in allowed_relations and row.get("source_id") for row in assessments)
    claim_allowed = current and target_match and assessments_valid and bool(snapshot.get("content_digest"))
    if not current:
        reason = "snapshot is missing, stale, superseded, or unvalidated"
    elif not target_match:
        reason = "snapshot targets a different discovery problem"
    elif not assessments_valid:
        reason = "citation absence/count was not replaced by source-to-hypothesis relation assessment"
    elif not snapshot.get("content_digest"):
        reason = "snapshot lacks immutable content provenance"
    else:
        reason = "current target-scoped sources were related semantically to the candidate"
    return {
        "claim_allowed": claim_allowed,
        "snapshot_status": status,
        "target_match": target_match,
        "source_relation_assessments": [dict(row) for row in assessments],
        "reason": reason,
    }


def _gates(candidate: Mapping[str, Any]) -> tuple[list[dict[str, Any]], bool]:
    output: list[dict[str, Any]] = []
    blocked = False
    gates = _rows(candidate.get("established_claim_gates"))
    if candidate.get("promotion_requested") and not gates:
        gates = [{"gate_id": "unspecified_required_authority", "applicability": "unknown", "status": "unknown", "reason": "promotion requested without typed hard gates"}]
    for row in gates:
        applicability = str(row.get("applicability", "unknown"))
        status = str(row.get("status", "unknown"))
        reason = str(row.get("reason", "")).strip()
        if applicability not in {"applicable", "not_applicable", "unknown"}:
            raise ContractError(f"invalid gate applicability for {row.get('gate_id')}")
        if applicability == "not_applicable" and len(reason.split()) < 3:
            raise ContractError(f"not-applicable gate {row.get('gate_id')} requires a reasoned waiver")
        if applicability == "unknown" or (applicability == "applicable" and status != "passed"):
            blocked = True
        output.append({"gate_id": str(row.get("gate_id", "unknown-gate")), "applicability": applicability, "status": status, "reason": reason})
    return output, blocked


def evaluate_discovery_delta(
    candidate: Mapping[str, Any],
    *,
    evaluator_identity: str,
    evaluator_invocation_id: str,
    evaluator_version: str,
    genealogy: Sequence[Mapping[str, Any]] = (),
    deterministic_validator: bool = False,
) -> dict[str, Any]:
    """Evaluate a candidate from blind structural inputs and emit a receipt."""

    proposer_identity = str(candidate.get("proposer_identity", ""))
    proposal_invocation_id = str(candidate.get("proposal_invocation_id", ""))
    if not proposer_identity or not proposal_invocation_id:
        raise ContractError("candidate must name proposer identity and proposal invocation")
    if not deterministic_validator and (evaluator_identity == proposer_identity or evaluator_invocation_id == proposal_invocation_id):
        raise ContractError("proposer and independent evaluator must not share identity or invocation")
    proposal_receipts = sorted(set(_texts(candidate.get("proposal_receipt_ids"))))
    if not proposal_receipts:
        raise ContractError("evaluation requires proposal receipt provenance")
    blinded = {
        key: value
        for key, value in candidate.items()
        if key not in {"self_assessment", "claimed_score", "preferred_theory", "blind_input_digest"}
    }
    blind_digest = canonical_digest(blinded)
    supplied_blind = candidate.get("blind_input_digest")
    if supplied_blind and supplied_blind != blind_digest:
        raise ContractError("blind input digest does not match candidate input")

    novelty = structural_novelty(candidate, genealogy)
    quality = _quality(candidate, novelty)
    pareto = {dimension: quality[dimension]["score"] for dimension in DIMENSIONS}
    relevance = candidate.get("relevance", {}) if isinstance(candidate.get("relevance"), Mapping) else {}
    target_dependencies = _texts(relevance.get("target_dependencies"))
    root_tensions = _texts(relevance.get("root_tensions"))
    essential = relevance.get("essential") is True
    relevance_passed = essential and bool(target_dependencies) and bool(root_tensions)
    relevance_floor = {
        "passed": relevance_passed,
        "target_dependencies": target_dependencies,
        "root_tensions": root_tensions,
        "reason": "candidate contacts an essential target dependency and root tension" if relevance_passed else "essential target dependence or root-tension contact is missing",
    }

    risk = candidate.get("risk_reward", {}) if isinstance(candidate.get("risk_reward"), Mapping) else {}
    truth_confidence = float(risk.get("truth_confidence", 0.0))
    value_if_right = float(risk.get("value_if_right", 0.0))
    learning_if_false = float(risk.get("learning_value_if_false", 0.0))
    mechanism_path = str(risk.get("mechanism_path", "")).strip()
    correction_conditions = _texts(candidate.get("correction_conditions"))
    wildcard = relevance_passed and value_if_right >= 0.75 and learning_if_false >= 0.5 and bool(mechanism_path) and bool(correction_conditions)
    if wildcard and truth_confidence < 0.5:
        portfolio_status = "protected_wildcard"
    elif relevance_passed and mechanism_path:
        portfolio_status = "ordinary_candidate"
    else:
        portfolio_status = "demote_unstructured_or_irrelevant"
    risk_reward = {
        "truth_confidence": truth_confidence,
        "value_if_right": value_if_right,
        "learning_value_if_false": learning_if_false,
        "mechanism_path": mechanism_path,
        "correction_conditions": correction_conditions,
        "portfolio_status": portfolio_status,
    }
    literature = _literature(candidate)
    gates, gates_blocked = _gates(candidate)

    preference_floor_passed = all(
        pareto[dimension] >= floor
        for dimension, floor in PREFERENCE_FLOORS.items()
    )
    if novelty["classification"] == "duplicate":
        creative_decision = "duplicate"
    elif novelty["classification"] == "undetermined" or not relevance_passed or portfolio_status.startswith("demote"):
        creative_decision = "demote"
    elif wildcard and truth_confidence < 0.5:
        creative_decision = "incubate"
    elif preference_floor_passed:
        creative_decision = "prefer"
    else:
        creative_decision = "revise"

    promotion_requested = bool(candidate.get("promotion_requested"))
    proof_status = str(candidate.get("proof_status", "open"))
    evidence_status = str(candidate.get("evidence_status", "open"))
    if not promotion_requested:
        promotion = "not_requested"
    elif gates_blocked or (proof_status != "proved" and evidence_status != "supported"):
        promotion = "blocked"
    else:
        promotion = "eligible"

    receipt = {
        "schema_version": 1,
        "evaluation_id": stable_identifier("evaluation", proposal_receipts, evaluator_identity, evaluator_version, blind_digest),
        "proposal_receipt_ids": proposal_receipts,
        "proposal_invocation_id": proposal_invocation_id,
        "proposer_identity": proposer_identity,
        "evaluator_identity": evaluator_identity,
        "evaluator_invocation_id": evaluator_invocation_id,
        "evaluator_version": evaluator_version,
        "deterministic_validator": deterministic_validator,
        "blind_input_digest": blind_digest,
        "candidate_digest": canonical_digest(candidate),
        "structural_novelty": novelty,
        "relevance_floor": relevance_floor,
        "theory_quality": quality,
        "pareto_vector": pareto,
        "risk_reward": risk_reward,
        "literature_novelty": literature,
        "established_claim_gates": gates,
        "creative_worth_decision": creative_decision,
        "promotion_decision": promotion,
        "proof_status": proof_status,
        "evidence_status": evidence_status,
        "created_at": utc_now(),
    }
    receipt["receipt_digest"] = canonical_digest(receipt, exclude_keys=("receipt_digest", "created_at"))
    validate_evaluation_receipt(receipt)
    return receipt


def validate_evaluation_receipt(receipt: Mapping[str, Any]) -> None:
    """Validate evaluator separation, digest integrity, and authority boundaries."""

    validate_payload(dict(receipt), SCHEMA)
    expected = canonical_digest(receipt, exclude_keys=("receipt_digest", "created_at"))
    if receipt.get("receipt_digest") != expected:
        raise ContractError("evaluation receipt digest mismatch")
    quality = receipt.get("theory_quality", {})
    pareto = receipt.get("pareto_vector", {})
    if set(pareto) != set(DIMENSIONS):
        raise ContractError("evaluation Pareto vector has unknown or missing dimensions")
    for dimension in DIMENSIONS:
        score = quality.get(dimension, {}).get("score")
        if isinstance(score, bool) or not isinstance(score, (int, float)) or not 0.0 <= float(score) <= 1.0:
            raise ContractError(f"evaluation dimension score is invalid: {dimension}")
        if float(pareto[dimension]) != float(score):
            raise ContractError(f"Pareto vector does not equal theory-quality evidence: {dimension}")
    if receipt.get("creative_worth_decision") == "prefer" and not all(
        float(pareto[dimension]) >= floor
        for dimension, floor in PREFERENCE_FLOORS.items()
    ):
        raise ContractError("preferred evaluation failed a non-compensatory semantic floor")
    if not receipt.get("deterministic_validator") and (
        receipt.get("evaluator_identity") == receipt.get("proposer_identity")
        or receipt.get("evaluator_invocation_id") == receipt.get("proposal_invocation_id")
    ):
        raise ContractError("evaluation is not independent")
    novelty = receipt.get("literature_novelty", {})
    if novelty.get("claim_allowed") and (novelty.get("snapshot_status") != "validated_current" or novelty.get("target_match") is not True):
        raise ContractError("literature novelty authority is invalid")
    if receipt.get("promotion_decision") == "eligible":
        for gate in receipt.get("established_claim_gates", []):
            if gate.get("applicability") == "unknown" or (gate.get("applicability") == "applicable" and gate.get("status") != "passed"):
                raise ContractError("unknown or failed hard gate cannot permit promotion")


__all__ = [
    "CONCEPTUAL_GATE_IDS",
    "DIMENSIONS",
    "EVALUATION_ROLES",
    "PREFERENCE_FLOORS",
    "conceptual_gate_vector",
    "conceptual_gates_pass",
    "evaluate_discovery_delta",
    "semantic_delta_evidence",
    "structural_atoms",
    "structural_novelty",
    "validate_evaluation_receipt",
]
