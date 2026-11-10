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
"""Author aggressive pre-taxonomy inventions from exact semantic literature."""

from __future__ import annotations

import hashlib
import json
import os
import sys
from collections.abc import Mapping
from pathlib import Path
from typing import Any


REQUEST_FIELDS = {
    "schema_version",
    "study_id",
    "role",
    "operation",
    "request_nonce",
    "invocation_context",
    "payload",
    "payload_digest",
    "isolation_requirement",
    "fault_mode",
}
PROGRAMMES = (
    "introduce_mediator",
    "invert_dependence",
    "protect_invariant",
    "localize_obstruction",
    "quotient_redundancy",
    "close_feedback",
    "split_regime",
    "dualize_carrier",
)
PROGRAMME_LANGUAGE = {
    "introduce_mediator": {
        "verb": "insert an obligation-bearing mediator between",
        "prediction": "a previously disconnected target burden becomes jointly expressible",
        "correction": "remove the mediator if it merely renames either endpoint",
    },
    "invert_dependence": {
        "verb": "reverse the inherited explanatory dependence between",
        "prediction": "the target separates into two direction-sensitive regimes",
        "correction": "restore or split the relation when reverse dependence is not witnessed",
    },
    "protect_invariant": {
        "verb": "hold the protected carrier invariant while varying",
        "prediction": "the protected success persists across the proposed transformation",
        "correction": "restrict the scope at the first invariant violation",
    },
    "localize_obstruction": {
        "verb": "localize the obstruction that prevents",
        "prediction": "one exact local obstruction blocks the global explanatory step",
        "correction": "retype the obstruction if localization changes its carrier",
    },
    "quotient_redundancy": {
        "verb": "quotient representational redundancy while preserving",
        "prediction": "explanatory degrees of freedom decrease without losing the protected success",
        "correction": "retract the quotient when distinct physical carriers collapse",
    },
    "close_feedback": {
        "verb": "close a corrective feedback loop between",
        "prediction": "removing the feedback edge increases the target discrepancy",
        "correction": "abandon the loop when its direction is observationally idle",
    },
    "split_regime": {
        "verb": "split the target into regimes before relating",
        "prediction": "the apparent contradiction bifurcates at an explicit regime boundary",
        "correction": "merge regimes again if the boundary has no discriminating consequence",
    },
    "dualize_carrier": {
        "verb": "construct a dual carrier for",
        "prediction": "the protected consequence is invariant while the explanatory route changes",
        "correction": "change the relation when the dual map is not reversible on the protected sector",
    },
}
OUTPUT_CONTRACT = "literature-conditioned-pre-taxonomy-invention.v1"


def _canonical_json(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        allow_nan=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def _digest(value: Any) -> str:
    return "sha256:" + hashlib.sha256(_canonical_json(value)).hexdigest()


def _stable_identifier(prefix: str, *parts: Any) -> str:
    suffix = hashlib.sha256(_canonical_json(list(parts))).hexdigest()[:24]
    return f"{prefix}.{suffix}"


def _text(value: Any, field: str) -> str:
    result = " ".join(str(value or "").split())
    if not result:
        raise ValueError(f"{field} must be nonempty")
    return result


def _verify_seal(value: Mapping[str, Any], field: str, label: str) -> None:
    expected = _digest({key: item for key, item in value.items() if key != field})
    if value.get(field) != expected:
        raise ValueError(f"{label} digest changed")


def _validate_payload(payload: Mapping[str, Any]) -> dict[str, Any]:
    if set(payload) != {"invention_request", "invention_request_digest"}:
        raise ValueError("worker payload must contain only the sealed invention request")
    request = payload["invention_request"]
    if not isinstance(request, Mapping):
        raise ValueError("invention request must be an object")
    result = dict(request)
    _verify_seal(result, "content_digest", "invention request")
    if (
        payload["invention_request_digest"] != result["content_digest"]
        or result.get("artifact_kind") != "literature_conditioned_invention_request"
        or result.get("required_output_contract") != OUTPUT_CONTRACT
        or result.get("caller_supplied_inventions") is not False
        or result.get("caller_supplied_family_labels") is not False
    ):
        raise ValueError("invention request identity or causal boundary changed")
    namespace = result.get("namespace")
    constraints = result.get("target_constraints")
    literature = result.get("literature_derived_invention_input")
    if (
        not isinstance(namespace, Mapping)
        or not isinstance(constraints, Mapping)
        or not isinstance(literature, Mapping)
        or result.get("literature_derived_invention_input_digest")
        != literature.get("content_digest")
    ):
        raise ValueError("request namespace, constraints, or literature input is invalid")
    _verify_seal(literature, "content_digest", "literature input")
    count = result.get("requested_count")
    if (
        isinstance(count, bool)
        or not isinstance(count, int)
        or not 6 <= count <= len(PROGRAMMES)
    ):
        raise ValueError("requested invention count is outside six through eight")
    contradictions = constraints.get("root_contradictions")
    successes = constraints.get("protected_successes")
    if (
        not isinstance(contradictions, list)
        or not contradictions
        or not isinstance(successes, list)
        or not successes
    ):
        raise ValueError("target contradictions and protected successes are required")
    _text(constraints.get("target_pressure"), "target pressure")
    return result


def _claim_anchor(row: Mapping[str, Any] | None) -> dict[str, str]:
    if row is None:
        return {
            "causal_input_id": "literature-causal-input.absent",
            "source_id": "no-literature",
            "claim_digest": _digest("no-literature"),
            "warrant_digest": _digest("no-warrant"),
            "assimilation_event": "no_literature_counterfactual",
        }
    assimilation = row.get("assimilation_delta")
    return {
        "causal_input_id": _text(row.get("causal_input_id"), "causal input id"),
        "source_id": _text(row.get("source_id"), "source id"),
        "claim_digest": _text(row.get("claim_digest"), "claim digest"),
        "warrant_digest": _text(
            row.get("semantic_warrant_set_digest"), "warrant digest"
        ),
        "assimilation_event": _text(
            assimilation.get("event_type")
            if isinstance(assimilation, Mapping)
            else None,
            "assimilation event",
        ),
    }


def _family_evidence(
    *,
    invention_id: str,
    programme: str,
    programme_index: int,
    causal_index: int,
    anchor: Mapping[str, str],
    constraints: Mapping[str, Any],
) -> dict[str, Any]:
    contradiction_index = programme_index % len(constraints["root_contradictions"])
    success_index = programme_index % len(constraints["protected_successes"])
    language = PROGRAMME_LANGUAGE[programme]
    target_pressure = str(constraints["target_pressure"])
    contradiction = str(constraints["root_contradictions"][contradiction_index])
    protected = str(constraints["protected_successes"][success_index])
    input_ids = (
        []
        if anchor["causal_input_id"] == "literature-causal-input.absent"
        else [anchor["causal_input_id"]]
    )
    core = {
        "invention_id": invention_id,
        "literature_causal_input_ids": input_ids,
        "target_grounding": {
            "target_pressure_digest": _digest(target_pressure),
            "root_contradiction_index": contradiction_index,
            "root_contradiction_digest": _digest(contradiction),
            "protected_success_index": success_index,
            "protected_success_digest": _digest(protected),
        },
        "intervention_program": {
            "operation": programme,
            "literature_input_path": (
                f"/literature_derived_invention_input/causal_inputs/{causal_index}"
                if input_ids
                else "/literature_derived_invention_input/causal_inputs"
            ),
            "target_constraint_path": (
                f"/target_constraints/root_contradictions/{contradiction_index}"
            ),
            "transformation": {
                "verb": language["verb"],
                "source_id": anchor["source_id"],
                "claim_digest": anchor["claim_digest"],
                "semantic_warrant_set_digest": anchor["warrant_digest"],
                "assimilation_event": anchor["assimilation_event"],
                "target_pressure_digest": _digest(target_pressure),
                "contradiction_digest": _digest(contradiction),
                "protected_success_digest": _digest(protected),
            },
        },
        "prediction": {
            "observable_path": (
                f"/target_constraints/protected_successes/{success_index}"
            ),
            "decisive_change": language["prediction"],
            "failure_boundary": (
                f"The prediction fails if {protected} cannot be distinguished "
                f"after applying {programme}."
            ),
        },
        "correction": {
            "trigger": language["correction"],
            "revision_action": (
                f"Revise the {programme} relation while retaining the exact "
                f"negative result for {anchor['causal_input_id']}."
            ),
            "negative_knowledge": (
                f"The failed {programme} mapping cannot mediate "
                f"{anchor['claim_digest']} and {contradiction}."
            ),
        },
        "falsifier": {
            "countermodel": (
                f"Construct a target model satisfying {protected} and the "
                f"literature condition {anchor['claim_digest']} while the "
                f"{programme} consequence is false."
            ),
            "decisive_outcome": (
                f"One such countermodel falsifies this {programme} family."
            ),
        },
        "physics_return": {
            "protected_success_path": (
                f"/target_constraints/protected_successes/{success_index}"
            ),
            "next_theory_action": (
                f"Build the smallest carrier-specific witness that tests "
                f"{programme} against {protected}."
            ),
            "value_condition": (
                f"Retain the route only if it changes the exact obligation "
                f"induced by {target_pressure} without sacrificing {protected}."
            ),
            "nonclaim": (
                "This is a theory action, not a proof, theorem, experiment "
                "result, or physics result."
            ),
        },
    }
    return {**core, "evidence_digest": _digest(core)}


def _raw_invention(
    *,
    invention_id: str,
    programme: str,
    anchor: Mapping[str, str],
    constraints: Mapping[str, Any],
    evidence: Mapping[str, Any],
) -> dict[str, Any]:
    language = PROGRAMME_LANGUAGE[programme]
    grounding = evidence["target_grounding"]
    contradiction = constraints["root_contradictions"][
        grounding["root_contradiction_index"]
    ]
    protected = constraints["protected_successes"][
        grounding["protected_success_index"]
    ]
    return {
        "invention_id": invention_id,
        "conjecture": (
            f"If we {language['verb']} the target pressure and contradiction "
            f"under semantic input {anchor['causal_input_id']}, a new "
            f"obligation structure appears before formalization."
        ),
        "primitive_hunches": [
            f"{programme} carrier anchored by {anchor['claim_digest']}",
            f"protected-success witness for {protected}",
        ],
        "relation_hunches": [
            f"{programme} relates {contradiction} to {protected}",
            f"{anchor['assimilation_event']} conditions the proposed relation",
        ],
        "mechanism_hunch": (
            f"{language['verb']} {contradiction} and {protected}, using the "
            f"exact warrant {anchor['warrant_digest']} as a defeasible input."
        ),
        "root_tension_contact": str(contradiction),
        "counterfactual_world": (
            f"In a world where {programme} is disabled, "
            f"{language['prediction']} does not occur."
        ),
        "protected_successes": [str(protected)],
        "risk_if_wrong": (
            f"The {programme} operation is only a redescription and leaves "
            f"the target obligation unchanged."
        ),
        "upside_if_right": (
            f"The {programme} operation exposes a new relation-bearing "
            f"conceptual corner with an exact physics-facing return."
        ),
        "first_falsifier": str(evidence["falsifier"]["countermodel"]),
        "correction_path": str(evidence["correction"]["revision_action"]),
    }


def _identity_erased_conceptual_signature(
    evidence_rows: list[dict[str, Any]],
) -> str:
    """Compare conceptual operations without receipt or source-identity churn.

    Literature IDs, claim/warrant digests, assimilation labels, invention IDs,
    and prose that embeds those values are deliberately absent.  A changed
    signature therefore requires a changed intervention programme, target
    grounding, prediction kind, correction trigger, falsifier outcome, or
    physics-facing action rather than a freshly sealed request.
    """

    projection = []
    for row in evidence_rows:
        grounding = row["target_grounding"]
        programme = row["intervention_program"]
        transformation = programme["transformation"]
        prediction = row["prediction"]
        correction = row["correction"]
        falsifier = row["falsifier"]
        physics_return = row["physics_return"]
        projection.append(
            {
                "operation": programme["operation"],
                "target_constraint_path": programme["target_constraint_path"],
                "root_contradiction_index": grounding[
                    "root_contradiction_index"
                ],
                "protected_success_index": grounding[
                    "protected_success_index"
                ],
                "transformation_verb": transformation["verb"],
                "prediction_observable_path": prediction["observable_path"],
                "prediction_decisive_change": prediction["decisive_change"],
                "correction_trigger": correction["trigger"],
                "falsifier_decisive_outcome": falsifier["decisive_outcome"],
                "physics_protected_success_path": physics_return[
                    "protected_success_path"
                ],
                "physics_next_theory_action": physics_return[
                    "next_theory_action"
                ],
                "physics_value_condition": physics_return["value_condition"],
            }
        )
    projection.sort(key=_digest)
    return _digest(projection)


def _produce(request: Mapping[str, Any]) -> dict[str, Any]:
    constraints = request["target_constraints"]
    literature = request["literature_derived_invention_input"]
    causal_rows = [
        row
        for row in literature["causal_inputs"]
        if row.get("source_correction_status") != "retracted"
        and not (
            isinstance(row.get("assimilation_delta"), Mapping)
            and row["assimilation_delta"].get("event_type") == "retire"
        )
    ]
    count = request["requested_count"]
    inventions = []
    evidence_rows = []
    for index, programme in enumerate(PROGRAMMES[:count]):
        causal_index = index % len(causal_rows) if causal_rows else 0
        anchor = _claim_anchor(causal_rows[causal_index] if causal_rows else None)
        invention_id = _stable_identifier(
            "literature-conditioned-invention",
            request["request_id"],
            programme,
            anchor,
            index,
        )
        evidence = _family_evidence(
            invention_id=invention_id,
            programme=programme,
            programme_index=index,
            causal_index=causal_index,
            anchor=anchor,
            constraints=constraints,
        )
        inventions.append(
            _raw_invention(
                invention_id=invention_id,
                programme=programme,
                anchor=anchor,
                constraints=constraints,
                evidence=evidence,
            )
        )
        evidence_rows.append(evidence)
    semantic_signature = _digest(
        [
            {
                "intervention_program": row["intervention_program"],
                "prediction": row["prediction"],
                "correction": row["correction"],
                "falsifier": row["falsifier"],
                "physics_return": row["physics_return"],
            }
            for row in sorted(evidence_rows, key=lambda item: item["invention_id"])
        ]
    )
    return {
        "output_kind": "high_risk_generation",
        "output_contract": OUTPUT_CONTRACT,
        "request_id": request["request_id"],
        "request_digest": request["content_digest"],
        "literature_derived_invention_input_digest": request[
            "literature_derived_invention_input_digest"
        ],
        "known_taxonomy_commitment_digest": request[
            "known_taxonomy_commitment_digest"
        ],
        "caller_supplied_inventions_consumed": False,
        "caller_supplied_family_labels_consumed": False,
        "raw_inventions": inventions,
        "family_evidence": evidence_rows,
        "semantic_output_signature": semantic_signature,
        "identity_erased_conceptual_signature": (
            _identity_erased_conceptual_signature(evidence_rows)
        ),
        "literature_effect_null": (
            {
                "status": "explicit_no_literature_counterfactual",
                "reason": (
                    "No semantic literature row was available; target-only "
                    "programmes were produced for causal comparison."
                ),
            }
            if not causal_rows
            else None
        ),
        "authority_boundary": (
            "Local process authorship from exact request bytes only; no "
            "creativity, novelty, merit, truth, proof, or physics authority."
        ),
    }


def main() -> int:
    try:
        envelope = json.load(sys.stdin)
        if not isinstance(envelope, Mapping) or set(envelope) != REQUEST_FIELDS:
            raise ValueError("worker request must be the exact closed envelope")
        if (
            envelope["schema_version"] != 1
            or envelope["role"] != "high_risk"
            or envelope["operation"] != "high_risk_generation"
            or not isinstance(envelope["invocation_context"], Mapping)
            or not isinstance(envelope["payload"], Mapping)
            or envelope["payload_digest"] != _digest(envelope["payload"])
            or envelope["fault_mode"] is not None
        ):
            raise ValueError("worker request identity or payload digest mismatch")
        request = _validate_payload(envelope["payload"])
        context = envelope["invocation_context"]
        if context != {
            "request_id": request["request_id"],
            "invention_request_digest": request["content_digest"],
            "literature_derived_invention_input_digest": request[
                "literature_derived_invention_input_digest"
            ],
            "known_taxonomy_commitment_digest": request[
                "known_taxonomy_commitment_digest"
            ],
        }:
            raise ValueError("worker invocation context changed")
        environment = {name: os.environ[name] for name in sorted(os.environ)}
        response = {
            "schema_version": 1,
            "role": "high_risk",
            "operation": "high_risk_generation",
            "request_nonce": str(envelope["request_nonce"]),
            "environment_observation": {
                "names": sorted(environment),
                "values_digest": _digest(environment),
                "working_directory": str(Path.cwd().resolve()),
            },
            "output": _produce(request),
        }
        sys.stdout.buffer.write(_canonical_json(response) + b"\n")
        return 0
    except Exception as exc:
        error = {
            "status": "worker_protocol_error",
            "error_type": type(exc).__name__,
            "message": str(exc),
        }
        sys.stderr.buffer.write(_canonical_json(error) + b"\n")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
