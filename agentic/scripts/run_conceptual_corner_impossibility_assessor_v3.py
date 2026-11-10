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
"""Assess one immutable typed causal-family freeze in a separate process.

The worker receives only a closed, digest-bound assessment input.  It
recomputes pairwise causal-family contrasts and the largest qualifying clique,
then reports whether the exact immutable freeze can contain six already-sealed
families.  It does not claim that a future generation cannot invent another
family, or that any family is true, novel, creative, or scientifically useful.
"""

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
PAYLOAD_FIELDS = {
    "conditioned_freeze_digest",
    "source_freeze_digest",
    "literature_derived_invention_input_digest",
    "required_family_count",
    "family_contracts",
    "grounding_evidence",
}
CONTRACT_FIELDS = {
    "invention_id",
    "source_invention_digest",
    "primitive_kind",
    "relation_kind",
    "mechanism_kind",
    "intervention_kind",
    "prediction_direction",
    "correction_kind",
    "target_grounding_paths",
    "literature_causal_input_ids",
    "contract_digest",
}


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
    result = " ".join(str(value or "").strip().split())
    if not result:
        raise ValueError(f"{field} must be nonempty")
    return result


def _validated_contracts(value: Any) -> list[dict[str, Any]]:
    if not isinstance(value, list) or not value:
        raise ValueError("family_contracts must be a nonempty list")
    rows: list[dict[str, Any]] = []
    for index, raw in enumerate(value):
        if not isinstance(raw, Mapping) or set(raw) != CONTRACT_FIELDS:
            raise ValueError(f"family_contracts[{index}] is not closed")
        row = dict(raw)
        unsigned = {
            key: item for key, item in row.items() if key != "contract_digest"
        }
        if row["contract_digest"] != _digest(unsigned):
            raise ValueError(f"family_contracts[{index}] digest mismatch")
        for field in (
            "invention_id",
            "source_invention_digest",
            "primitive_kind",
            "relation_kind",
            "mechanism_kind",
            "intervention_kind",
            "prediction_direction",
            "correction_kind",
        ):
            _text(row[field], f"family_contracts[{index}].{field}")
        for field in (
            "target_grounding_paths",
            "literature_causal_input_ids",
        ):
            child = row[field]
            if (
                not isinstance(child, list)
                or not child
                or len(child) != len(set(child))
            ):
                raise ValueError(
                    f"family_contracts[{index}].{field} must be unique and nonempty"
                )
            for item in child:
                _text(item, f"family_contracts[{index}].{field}")
        rows.append(row)
    rows.sort(key=lambda row: row["invention_id"])
    if len({row["invention_id"] for row in rows}) != len(rows):
        raise ValueError("family_contracts repeat invention identities")
    return rows


def _pair_contrast(
    left: Mapping[str, Any], right: Mapping[str, Any]
) -> dict[str, Any]:
    requirements = {
        "primitive_or_relation": (
            left["primitive_kind"],
            left["relation_kind"],
        )
        != (
            right["primitive_kind"],
            right["relation_kind"],
        ),
        "mechanism_dependency": left["mechanism_kind"]
        != right["mechanism_kind"],
        "discriminating_prediction": (
            left["intervention_kind"],
            left["prediction_direction"],
        )
        != (
            right["intervention_kind"],
            right["prediction_direction"],
        ),
        "falsifier_or_correction": left["correction_kind"]
        != right["correction_kind"],
    }
    core = {
        "left_invention_id": left["invention_id"],
        "right_invention_id": right["invention_id"],
        "domain_requirements": requirements,
        "status": (
            "registered_typed_causal_family_contrast"
            if all(requirements.values())
            else "insufficient_typed_causal_contrast"
        ),
    }
    return {**core, "contrast_digest": _digest(core)}


def _largest_clique(
    family_ids: list[str], contrastive_pairs: set[tuple[str, str]]
) -> list[str]:
    ordered = tuple(sorted(family_ids))
    adjacency = {
        family_id: {
            other
            for other in ordered
            if other != family_id
            and tuple(sorted((family_id, other))) in contrastive_pairs
        }
        for family_id in ordered
    }
    best: tuple[str, ...] = ()

    def search(chosen: tuple[str, ...], candidates: tuple[str, ...]) -> None:
        nonlocal best
        if len(chosen) > len(best):
            best = chosen
        if len(chosen) + len(candidates) <= len(best):
            return
        for index, candidate in enumerate(candidates):
            search(
                (*chosen, candidate),
                tuple(
                    other
                    for other in candidates[index + 1 :]
                    if other in adjacency[candidate]
                ),
            )

    search((), ordered)
    return list(best)


def _assessment(payload: Mapping[str, Any]) -> dict[str, Any]:
    if set(payload) != PAYLOAD_FIELDS:
        raise ValueError("assessment payload is not closed")
    for field in (
        "conditioned_freeze_digest",
        "source_freeze_digest",
        "literature_derived_invention_input_digest",
    ):
        _text(payload[field], field)
    required = payload["required_family_count"]
    if not isinstance(required, int) or isinstance(required, bool) or required != 6:
        raise ValueError("required_family_count must be exactly six")
    contracts = _validated_contracts(payload["family_contracts"])
    grounding = payload["grounding_evidence"]
    if not isinstance(grounding, list) or not grounding:
        raise ValueError("grounding_evidence must be nonempty")
    pairwise: list[dict[str, Any]] = []
    contrastive: set[tuple[str, str]] = set()
    for index, left in enumerate(contracts):
        for right in contracts[index + 1 :]:
            contrast = _pair_contrast(left, right)
            pairwise.append(contrast)
            if (
                contrast["status"]
                == "registered_typed_causal_family_contrast"
            ):
                contrastive.add(
                    tuple(
                        sorted(
                            (
                                left["invention_id"],
                                right["invention_id"],
                            )
                        )
                    )
                )
    clique = _largest_clique(
        [row["invention_id"] for row in contracts], contrastive
    )
    if len(clique) >= required:
        raise ValueError(
            "a freeze satisfying six families needs no impossibility assessment"
        )
    constraints = [
        {
            "constraint_id": "immutable-freeze-membership",
            "constraint_kind": "sealed_generation_membership",
            "grounding_paths": sorted(
                {
                    path
                    for row in contracts
                    for path in row["target_grounding_paths"]
                }
            ),
            "witness_digest": payload["conditioned_freeze_digest"],
            "statement": (
                "The exact sealed generation contains no additional family "
                "bytes that can join the independently replayed clique."
            ),
        },
        {
            "constraint_id": "target-and-literature-binding",
            "constraint_kind": "target_preserving_input_closure",
            "grounding_paths": sorted(
                {
                    path
                    for row in contracts
                    for path in row["target_grounding_paths"]
                }
            ),
            "witness_digest": (
                payload["literature_derived_invention_input_digest"]
            ),
            "statement": (
                "Adding a family while preserving the exact target and "
                "literature input closure requires a new freeze digest."
            ),
        },
    ]
    core = {
        "output_kind": "reflection",
        "assessment_kind": "corner_impossibility_assessment",
        "status": "registered_freeze_bounded_impossibility",
        "conditioned_freeze_digest": payload["conditioned_freeze_digest"],
        "source_freeze_digest": payload["source_freeze_digest"],
        "literature_derived_invention_input_digest": payload[
            "literature_derived_invention_input_digest"
        ],
        "required_family_count": required,
        "observed_family_count": len(contracts),
        "maximum_registered_typed_family_count": len(clique),
        "missing_registered_typed_family_count": required - len(clique),
        "largest_registered_clique_ids": clique,
        "pairwise_contrasts": pairwise,
        "grounding_evidence": grounding,
        "blocking_constraints": constraints,
        "scope": "exact_immutable_freeze_only",
        "reopen_condition": (
            "Run and seal a new pre-taxonomy generation against the same or a "
            "newer independently bridged semantic literature input."
        ),
        "authority_nulls": {
            "future_generation_impossibility_authority": None,
            "semantic_impossibility_authority": None,
            "creativity_authority": None,
            "truth_authority": None,
        },
    }
    return {**core, "assessment_digest": _digest(core)}


def main() -> int:
    try:
        request = json.load(sys.stdin)
        if not isinstance(request, Mapping) or set(request) != REQUEST_FIELDS:
            raise ValueError("worker request must be the exact closed envelope")
        if (
            request["schema_version"] != 1
            or request["role"] != "candidate"
            or request["operation"] != "reflection"
            or not isinstance(request["invocation_context"], Mapping)
            or not isinstance(request["payload"], Mapping)
            or request["payload_digest"] != _digest(request["payload"])
            or request["fault_mode"] is not None
        ):
            raise ValueError("worker request identity or payload digest mismatch")
        output = _assessment(request["payload"])
        environment = {name: os.environ[name] for name in sorted(os.environ)}
        response = {
            "schema_version": 1,
            "role": "candidate",
            "operation": "reflection",
            "request_nonce": str(request["request_nonce"]),
            "environment_observation": {
                "names": sorted(environment),
                "values_digest": _digest(environment),
                "working_directory": str(Path.cwd().resolve()),
            },
            "output": output,
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
