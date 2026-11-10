# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Generate branch maturation and objection-bearing conceptual reflection.

Calls are serialized through the host channel, while each branch sees only its
own frozen seed and evidence. The source reducer subsequently consumes their
separate outputs. Reflection keeps prior rounds and their exact system snapshots
in the model journal so a reported change is reviewable against what preceded it.
"""
from __future__ import annotations

import copy
from typing import Any, Mapping

from .bootstrap_authoring import TEXT, array_schema, object_schema, schema_fragment
from .contracts import ContractError, canonical_digest, stable_identifier
from .conceptual_adjudication import _typed_unification_assessment
from .model_author import ModelAuthor, validate_value
from .parallel import build_parallel_manifest, _normalize_result
from .reflection import validate_reflection_round, validate_reflection_rounds


def author_maturation(author: ModelAuthor, *, portfolio: Mapping[str, Any],
                      snapshot: Mapping[str, Any], assessment: Mapping[str, Any],
                      max_branches: int = 3) -> dict[str, Any]:
    """Author distinct branch outputs without leaking another branch's results."""
    seeds = list(portfolio["parallel_branch_seeds"][:max_branches])
    budget = {"wall_seconds": 60, "max_workers": 1, "cost_units": max_branches,
              "storage_bytes": 2_000_000, "matched_budget_baseline_corner_coverage": 1}
    manifest = build_parallel_manifest(portfolio, base_theory_state_version=0,
        branch_seeds=seeds, resource_budget=budget)
    dependency = object_schema({"source": TEXT, "relation": TEXT, "target": TEXT})
    distinction = object_schema({"name": TEXT, "left": TEXT, "right": TEXT, "preservation_condition": TEXT})
    schema = object_schema({
        "theory_delta": object_schema({"delta_class": {"const": "conceptual_maturation"},
            "changed_question": TEXT, "mechanism": TEXT,
            "new_explanatory_dependencies": array_schema(dependency, 0, 4),
            "new_distinctions": array_schema(distinction, 0, 4),
            "blocking_gaps": array_schema(TEXT), "falsifiers": array_schema(TEXT)}),
        "claims": array_schema(object_schema({"proposition": TEXT,
            "stance": {"enum": ["support", "oppose", "uncertain"]},
            "epistemic_status": {"const": "conjectural"}}), 0, 4),
        "is_dissent": {"type": "boolean"},
    })
    hypotheses = {row["hypothesis_id"]: row for row in portfolio["hypotheses"]}
    outputs, records = {}, []
    for request in manifest["branch_requests"]:
        hypothesis = hypotheses[request["hypothesis_id"]]
        source_ids = set(hypothesis["literature_source_ids"])
        record = author.author("mature-" + request["branch_id"], instruction=(
            "Mature only this frozen conjecture. Attempt a concrete derivation or counterexample, "
            "state assumptions and quantifiers, and locate the earliest decisive falsifier. "
            "Report what changed in the explanatory dependency or distinction, with remaining gaps. "
            "An unsuccessful attempt is a valid result; do not invent a discovery to fill the schema. "
            "You have no access to other branches' conclusions. Source abstracts remain unverified."),
            inputs={"branch_request": request, "hypothesis": hypothesis,
                    "sources": [row for row in snapshot["sources"] if row["source_id"] in source_ids],
                    "source_assessments": [row for row in assessment["value"]["assessments"] if row["source_id"] in source_ids]},
            schema=schema, validator=lambda value: _normalize_result(value, request), max_tokens=10000)
        outputs[request["branch_id"]] = {**record["value"], "genealogy": [hypothesis["hypothesis_id"]]}
        records.append(record)
    return {"branch_seeds": seeds, "resource_budget": budget, "worker_outputs": outputs,
            "authoring_records": records,
            "execution_boundary": "Model maturation was serialized in isolated branch contexts; reducer worker time excludes those model calls."}


def system_schema() -> dict[str, Any]:
    """Describe conceptual content while keeping operational state source-owned."""
    schema = schema_fragment("reflective_conceptual_discovery_packet.schema.json", "/$defs/system")
    properties = {key: value for key, value in schema["properties"].items()
                  if key not in {"structural_identity", "lifecycle_state"}}
    properties["unification_claims"] = schema_fragment("conceptual_adjudication_evidence.schema.json", "/$defs/typedUnificationClaims")
    mediator = properties["unification_claims"]["properties"]["mediator"]["properties"]
    for field in ("primitive_refs", "relation_refs"):
        mediator[field]["items"].update({
            "pattern": r"\S+(?:\s+\S+){3,}",
            "description": "A substantive description identifying the referenced concept or relation (at least four words), not a short identifier.",
        })
    transition = properties["unification_claims"]["properties"]["explanatory_graph_transition"]
    derived = {"before_graph_digest", "after_graph_digest", "added_nodes", "added_edges"}
    transition["properties"] = {key: value for key, value in transition["properties"].items() if key not in derived}
    transition["required"] = [key for key in transition["required"] if key not in derived]
    properties["relation"] = {"enum": ["incumbent", "rival", "synthesis", "challenger"]}
    for field in ("primitives", "relations_operations_and_dynamics", "implications_and_new_questions",
                  "correction_conditions", "protected_successes", "target_pressures_addressed"):
        properties[field]["minItems"] = 1
    return object_schema(properties)


def compile_system(raw: Mapping[str, Any]) -> dict[str, Any]:
    """Derive typed structural IDs from authored content, without adding content."""
    value = copy.deepcopy(dict(raw))
    transition = value["unification_claims"]["explanatory_graph_transition"]
    before, after = transition["before_graph"], transition["after_graph"]
    transition["before_graph_digest"] = canonical_digest(before)
    transition["after_graph_digest"] = canonical_digest(after)
    for collection in ("nodes", "edges"):
        transition["added_" + collection] = sorted(
            [row for row in after[collection] if row not in before[collection]], key=canonical_digest)
    value["lifecycle_state"] = "articulated"
    value["structural_identity"] = {
        "primitive_ids": [stable_identifier("primitive", row) for row in value["primitives"]],
        "relation_ids": [stable_identifier("relation", row) for row in value["relations_operations_and_dynamics"]],
        "mechanism_id": stable_identifier("mechanism", value["mechanism_or_principle"]),
        "maturation_question_id": stable_identifier("question", value["implications_and_new_questions"]),
        "genealogy_ids": list(value["conceptual_ancestors"]),
    }
    return value


def authored_system_view(system: Mapping[str, Any]) -> dict[str, Any]:
    """Project content without asking the model to echo executable bookkeeping."""
    value = copy.deepcopy({key: row for key, row in system.items()
                           if key not in {"structural_identity", "lifecycle_state"}})
    transition = value["unification_claims"]["explanatory_graph_transition"]
    for key in ("before_graph_digest", "after_graph_digest", "added_nodes", "added_edges"):
        transition.pop(key, None)
    return value


def version_synthesis(parent_systems: list[dict], parent_rounds: list[dict], record: Mapping[str, Any]) -> dict[str, Any]:
    """Preserve committed candidate identities and add changed descendants.

    The author edits exact parent candidates. A changed candidate becomes a new
    content-bound identity whose ancestor is the old one; unchanged parents stay
    present so the canonical reducer can reopen the full genealogy. Only the
    new round's references are remapped. Prior critique/history stays immutable.
    """
    parents = {row["system_id"]: row for row in parent_systems}
    systems, replacements = copy.deepcopy(parent_systems), {}
    for raw in record["value"]["systems"]:
        candidate = compile_system(raw)
        prior_id = candidate["system_id"]
        if prior_id not in parents:
            raise ContractError("synthesis cannot invent an unassigned parent identity")
        if candidate != parents[prior_id]:
            new_id = stable_identifier("system-revision", prior_id, canonical_digest(candidate))
            candidate["system_id"] = new_id
            candidate["conceptual_ancestors"] = [prior_id]
            candidate["structural_identity"]["genealogy_ids"] = [prior_id]
            replacements[prior_id] = new_id
            systems.append(candidate)
    round_row = copy.deepcopy(record["value"]["round"])
    round_row["system_ids"] = [replacements.get(value, value) for value in round_row["system_ids"]]
    for link in round_row.get("semantic_patch_links", []):
        link["candidate_ref"] = replacements.get(link["candidate_ref"], link["candidate_ref"])
    return {"systems": systems, "rounds": [*copy.deepcopy(parent_rounds), round_row],
            "authoring_record": copy.deepcopy(dict(record)), "revision_identities": replacements}


def author_systems(author: ModelAuthor, *, charter: Mapping[str, Any], portfolio: Mapping[str, Any],
                   parallel: Mapping[str, Any], stage_id: str = "conceptual-systems") -> dict[str, Any]:
    """Articulate rival conceptual systems from the actual matured hypotheses."""
    hypotheses = {row["hypothesis_id"]: row for row in portfolio["hypotheses"]}
    selected = [hypotheses[row["hypothesis_id"]] for row in portfolio["parallel_branch_seeds"][:3]]
    assignments = [{"system_id": stable_identifier("system", row["hypothesis_id"]),
                    "ancestor_hypothesis_id": row["hypothesis_id"]} for row in selected]
    schema = object_schema({"systems": array_schema(system_schema(), len(assignments), len(assignments))})
    def validate(value):
        expected = {row["system_id"]: row for row in assignments}
        if sorted(row["system_id"] for row in value["systems"]) != sorted(expected):
            raise ContractError("system articulation must preserve the exact assigned candidate identities")
        for row in value["systems"]:
            if row["conceptual_ancestors"] != [expected[row["system_id"]]["ancestor_hypothesis_id"]]:
                raise ContractError("system articulation crossed its source hypothesis")
            _typed_unification_assessment(compile_system(row))
    return author.author(stage_id, instruction=(
        "Articulate one concrete conceptual system for each assigned hypothesis, informed by its maturation. "
        "Use the exact assigned system and ancestor IDs. Each remains a conjectural rival. "
        "State a noncircular mediator and a typed unification of at least two named source cases, "
        "including graph before/after, preserved differences, scope limits and failure conditions. "
        "Keep every before-graph node and edge unchanged in the after graph; add an explicit mediator "
        "and the source-to-mediator connections. All case IDs must be source_case nodes and all mediator "
        "node IDs must be mediator nodes. Map and preserve differences for every source case. "
        "The mediator primitive_refs and relation_refs are explanatory descriptions of at least four words "
        "each, not short identifiers. Node labels need two words; edge statements need four. "
        "Graph content_paths are JSON pointers into this same system, such as /mechanism_or_principle. "
        "Do not invent evidence, a preferred candidate, formal proof or maturity certification."),
        inputs={"charter": charter, "assignments": assignments, "hypotheses": selected, "parallel_results": parallel},
        schema=schema, validator=validate, max_tokens=24000)


def author_reflection_round(author: ModelAuthor, *, stage_id: str, systems: list[dict],
                            rounds: list[dict], charter: Mapping[str, Any],
                            critique: Mapping[str, Any] | None = None) -> dict[str, Any]:
    """Execute one real critique/revision round and check its change claims."""
    ids = [row["system_id"] for row in systems]
    round_schema = schema_fragment("reflective_conceptual_discovery_packet.schema.json", "/$defs/reflection")
    round_id = stable_identifier("reflection", stage_id, canonical_digest(systems), canonical_digest(rounds))
    round_schema["properties"]["round_id"] = {"const": round_id}
    round_schema["properties"]["system_ids"]["items"] = {"enum": ids}
    schema = object_schema({"systems": array_schema(system_schema(), len(systems), len(systems)),
                            "round": round_schema})
    originals = {row["system_id"]: row for row in systems}
    def validate(value):
        if sorted(row["system_id"] for row in value["systems"]) != sorted(ids):
            raise ContractError("reflection cannot drop or replace candidate identities")
        compiled = [compile_system(row) for row in value["systems"]]
        for row in compiled:
            _typed_unification_assessment(row)
        changed = [row["system_id"] for row in compiled if row != originals[row["system_id"]]]
        if not set(changed).issubset(value["round"]["system_ids"]):
            raise ContractError("reflection changed a system outside its recorded round")
        if (value["round"]["result"] == "no_change") != (not changed):
            raise ContractError("reflection result does not match its actual before/after content")
        validate_reflection_round(value["round"])
        history = [*rounds, value["round"]]
        if len(history) >= 2:
            empty = sum(row["result"] == "no_change" for row in history)
            validate_reflection_rounds(history, {"materially_empty_rounds": empty, "action": "reframe"})
    return author.author(stage_id, instruction=(
        "Execute one substantive reflection round. Expose the strongest objections and missing mediation "
        "using at least ontological and dialectical lenses, then revise only what those objections warrant. "
        "Return all candidate systems with their existing IDs and record exact changed content, "
        "preserved/lost content, correction tests and unresolved dissent. "
        "Each semantic_patch_links objection must exactly copy a strongest_objections entry in this round; "
        "each correction_test must exactly copy a correction_tests entry in this round. "
        "If no defensible revision exists, return the systems unchanged and an explicit no_change reason. "
        "No score inflation or forced convergence. "
        "If sealing a synthesis, preserve the rival differences and identify the mediation's failure conditions. "
        "Keep all prior rounds unchanged; the runtime appends your single new round."),
        inputs={"charter": charter, "systems": [authored_system_view(row) for row in systems],
                "prior_rounds": rounds, "round_id": round_id, "sealed_critique": critique},
        schema=schema, validator=validate, max_tokens=26000)
