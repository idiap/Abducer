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
"""Evaluate one claim-bound exact or finite-model proof request.

This worker is intentionally a small, standard-library-only protocol endpoint.
It receives one canonical request on stdin and writes one canonical response on
stdout.  Process isolation and resource enforcement belong exclusively to the
parent ``ResourceGovernor``; this worker never launches another process.

The response is scoped evidence about the supplied finite claim.  It is not
theorem authority, checker-soundness authority, theory-selection authority, or
permission to mutate theory state.
"""

from __future__ import annotations

import ast
import hashlib
import itertools
import json
import math
import sys
from fractions import Fraction
from typing import Any, Mapping


WORKER_RESPONSE_CONTRACT_VERSION = "proof-execution-worker-response/3.0.0"

_AUTHORITY_NULLS = {
    "truth_authority": False,
    "checker_soundness_authority": False,
    "theorem_authority": False,
    "physics_authority": False,
    "theory_selection_authority": False,
    "same_cycle_theory_mutation": False,
    "serialized_execution_authority": False,
    "cryptographic_authenticity": False,
}

_REQUEST_KEYS = frozenset(
    {
        "schema_version",
        "contract_version",
        "message_kind",
        "binding_id",
        "binding_digest",
        "execution_claim_id",
        "execution_claim_digest",
        "reservation_id",
        "reservation_digest",
        "attempt_id",
        "attempt_number",
        "handoff_id",
        "handoff_digest",
        "formal_claim",
        "formal_claim_digest",
        "adapter",
        "runtime_route_id",
        "runtime_route_digest",
        "execution_plan",
        "execution_plan_digest",
        "artifact_policy",
        "resource_budget",
        "resource_budget_digest",
        "execution_policy",
        "execution_policy_digest",
        "proof_runtime_ref",
        "authority_nulls",
        "request_id",
        "content_digest",
    }
)

_RESPONSE_KEYS = frozenset(
    {
        "schema_version",
        "contract_version",
        "message_kind",
        "response_id",
        "request_id",
        "binding_id",
        "binding_digest",
        "execution_claim_id",
        "execution_claim_digest",
        "attempt_id",
        "attempt_number",
        "handoff_id",
        "handoff_digest",
        "formal_claim_digest",
        "adapter",
        "runtime_route_id",
        "proof_verdict",
        "result",
        "scoped_certificate",
        "completeness",
        "uncertainty",
        "artifact",
        "authority_boundary",
        "authority_nulls",
        "content_digest",
    }
)

_ROUTES = {
    "exact": "proof-runtime-exact-v1",
    "finite_model": "proof-runtime-finite-model-v1",
}

_BINARY = {
    ast.Add: lambda left, right: left + right,
    ast.Sub: lambda left, right: left - right,
    ast.Mult: lambda left, right: left * right,
    ast.Div: lambda left, right: left / right,
    ast.FloorDiv: lambda left, right: left // right,
    ast.Mod: lambda left, right: left % right,
    ast.Pow: lambda left, right: left**right,
}
_UNARY = {
    ast.UAdd: lambda value: value,
    ast.USub: lambda value: -value,
    ast.Not: lambda value: not value,
}
_COMPARE = {
    ast.Eq: lambda left, right: left == right,
    ast.NotEq: lambda left, right: left != right,
    ast.Lt: lambda left, right: left < right,
    ast.LtE: lambda left, right: left <= right,
    ast.Gt: lambda left, right: left > right,
    ast.GtE: lambda left, right: left >= right,
}


class WorkerProtocolError(ValueError):
    """Reject an unbound, malformed, or unsupported request."""


class ClaimSpecError(ValueError):
    """Reject a formal claim outside the worker's finite language."""


def _canonical_bytes(value: Any) -> bytes:
    try:
        text = json.dumps(
            value,
            ensure_ascii=False,
            allow_nan=False,
            sort_keys=True,
            separators=(",", ":"),
        )
    except (TypeError, ValueError) as exc:
        raise WorkerProtocolError(f"value is not canonical JSON: {exc}") from exc
    return text.encode("utf-8")


def _digest(value: Any) -> str:
    return "sha256:" + hashlib.sha256(_canonical_bytes(value)).hexdigest()


def _self_digest(value: Mapping[str, Any]) -> str:
    return _digest(
        {key: item for key, item in value.items() if key != "content_digest"}
    )


def _stable_identifier(prefix: str, *parts: Any) -> str:
    suffix = _digest(list(parts)).removeprefix("sha256:")[:24]
    return f"{prefix}.{suffix}"


def _validate_request(raw: Mapping[str, Any]) -> dict[str, Any]:
    request = dict(raw)
    if frozenset(request) != _REQUEST_KEYS:
        raise WorkerProtocolError("proof request shape differs from protocol v3")
    if (
        request["schema_version"] != 1
        or request["contract_version"] != "proof-execution-invocation/1.0.0"
        or request["message_kind"] != "proof_execution_request"
        or request["authority_nulls"] != _AUTHORITY_NULLS
        or request["content_digest"] != _self_digest(request)
    ):
        raise WorkerProtocolError("proof request constants or digest are invalid")
    adapter = request["adapter"]
    if adapter not in _ROUTES or request["runtime_route_id"] != _ROUTES[adapter]:
        raise WorkerProtocolError("proof request route is not a built-in v3 route")
    if request["artifact_policy"] != "forbidden":
        raise WorkerProtocolError("built-in worker forbids result artifacts")
    if request["execution_plan"] != {"kind": "builtin_worker"}:
        raise WorkerProtocolError("built-in worker requires the exact built-in plan")
    digest_pairs = (
        ("formal_claim", "formal_claim_digest"),
        ("execution_plan", "execution_plan_digest"),
        ("resource_budget", "resource_budget_digest"),
        ("execution_policy", "execution_policy_digest"),
    )
    for value_field, digest_field in digest_pairs:
        if _digest(request[value_field]) != request[digest_field]:
            raise WorkerProtocolError(
                f"proof request {value_field} digest is invalid"
            )
    if not isinstance(request["formal_claim"], Mapping):
        raise WorkerProtocolError("proof request formal claim is not an object")
    return request


def _fraction(value: Any) -> Fraction:
    if isinstance(value, bool) or not isinstance(value, (int, float, str)):
        raise ClaimSpecError("exact variables must be finite JSON numbers or strings")
    try:
        return Fraction(str(value))
    except (ValueError, ZeroDivisionError) as exc:
        raise ClaimSpecError("exact variable is not a rational value") from exc


def _safe_expression(
    expression: Any,
    names: Mapping[str, Any] | None = None,
) -> Any:
    if (
        not isinstance(expression, str)
        or not expression.strip()
        or len(expression.encode("utf-8")) > 4096
    ):
        raise ClaimSpecError("expression must be a bounded non-empty string")
    try:
        tree = ast.parse(expression, mode="eval")
    except SyntaxError as exc:
        raise ClaimSpecError(f"invalid expression: {exc.msg}") from exc
    if sum(1 for _node in ast.walk(tree)) > 256:
        raise ClaimSpecError("expression syntax tree exceeds the finite limit")
    environment = {
        str(name): _fraction(value) for name, value in dict(names or {}).items()
    }

    def visit(node: ast.AST) -> Any:
        if isinstance(node, ast.Expression):
            return visit(node.body)
        if (
            isinstance(node, ast.Constant)
            and isinstance(node.value, (int, float))
            and not isinstance(node.value, bool)
        ):
            return _fraction(node.value)
        if isinstance(node, ast.Name):
            if node.id not in environment:
                raise ClaimSpecError(f"unbound variable {node.id!r}")
            return environment[node.id]
        if isinstance(node, ast.BinOp) and type(node.op) in _BINARY:
            left, right = visit(node.left), visit(node.right)
            if isinstance(node.op, ast.Pow):
                if right.denominator != 1 or abs(right.numerator) > 64:
                    raise ClaimSpecError("power exponent must be a bounded integer")
                right = right.numerator
            try:
                return _BINARY[type(node.op)](left, right)
            except (ArithmeticError, TypeError, ValueError) as exc:
                raise ClaimSpecError(f"exact arithmetic failed: {exc}") from exc
        if isinstance(node, ast.UnaryOp) and type(node.op) in _UNARY:
            return _UNARY[type(node.op)](visit(node.operand))
        if isinstance(node, ast.BoolOp) and isinstance(node.op, (ast.And, ast.Or)):
            values = [visit(child) for child in node.values]
            if any(type(value) is not bool for value in values):
                raise ClaimSpecError("boolean operators require boolean operands")
            return all(values) if isinstance(node.op, ast.And) else any(values)
        if isinstance(node, ast.Compare):
            left = visit(node.left)
            for operator, comparator in zip(
                node.ops, node.comparators, strict=True
            ):
                compare = _COMPARE.get(type(operator))
                if compare is None:
                    raise ClaimSpecError("comparison operator is forbidden")
                right = visit(comparator)
                if not compare(left, right):
                    return False
                left = right
            return True
        raise ClaimSpecError(
            f"expression node {type(node).__name__} is forbidden"
        )

    return visit(tree)


def _fraction_text(value: Fraction) -> str:
    return f"{value.numerator}/{value.denominator}"


def _certificate(
    request: Mapping[str, Any],
    *,
    certificate_kind: str,
    claim_holds: bool,
    evidence: Mapping[str, Any],
) -> dict[str, Any]:
    certificate: dict[str, Any] = {
        "schema_version": 1,
        "certificate_kind": certificate_kind,
        "request_id": request["request_id"],
        "binding_id": request["binding_id"],
        "binding_digest": request["binding_digest"],
        "execution_claim_id": request["execution_claim_id"],
        "execution_claim_digest": request["execution_claim_digest"],
        "attempt_id": request["attempt_id"],
        "handoff_id": request["handoff_id"],
        "handoff_digest": request["handoff_digest"],
        "formal_claim_digest": request["formal_claim_digest"],
        "adapter": request["adapter"],
        "claim_holds": claim_holds,
        "evidence": dict(evidence),
        "authority_scope": (
            "deterministic_evaluation_of_only_the_bound_rational_or_finite_claim"
        ),
        "authority_nulls": dict(_AUTHORITY_NULLS),
    }
    certificate["content_digest"] = _self_digest(certificate)
    return certificate


def _evaluate_exact(
    request: Mapping[str, Any],
) -> tuple[str, dict[str, Any], dict[str, Any], dict[str, Any]]:
    claim = dict(request["formal_claim"])
    operation = claim.get("operation", "equality")
    if operation == "equality" and claim.get("claim_kind") == "exact_equality":
        left = _safe_expression(claim.get("left"))
        right = _safe_expression(claim.get("right"))
        if not isinstance(left, Fraction) or not isinstance(right, Fraction):
            raise ClaimSpecError("exact equality must produce rational values")
        holds = left == right
        evidence = {
            "operation": "equality",
            "left": _fraction_text(left),
            "right": _fraction_text(right),
            "difference": _fraction_text(left - right),
        }
        verdict = (
            "claim_validated_within_declared_scope"
            if holds
            else "counterexample_validated_within_declared_scope"
        )
        return (
            verdict,
            {
                "kind": "exact_claim_result",
                "adapter_status": "succeeded" if holds else "counterexample",
                "claim_holds": holds,
                **evidence,
            },
            _certificate(
                request,
                certificate_kind="normalized_rational_equality",
                claim_holds=holds,
                evidence=evidence,
            ),
            {"complete": True, "scope": "declared rational expression"},
        )
    if (
        operation == "integer_predicate"
        and claim.get("claim_kind") == "exact_integer_predicate"
    ):
        variables = claim.get("variables")
        if not isinstance(variables, Mapping):
            raise ClaimSpecError("integer predicate variables must be an object")
        value = _safe_expression(claim.get("predicate"), variables)
        if type(value) is not bool:
            raise ClaimSpecError("integer predicate must evaluate to boolean")
        evidence = {
            "operation": "integer_predicate",
            "predicate": claim.get("predicate"),
            "assignment": dict(variables),
            "value": value,
        }
        verdict = (
            "claim_validated_within_declared_scope"
            if value
            else "counterexample_validated_within_declared_scope"
        )
        return (
            verdict,
            {
                "kind": "exact_claim_result",
                "adapter_status": "succeeded" if value else "counterexample",
                "claim_holds": value,
                "assignment": dict(variables),
            },
            _certificate(
                request,
                certificate_kind="exact_integer_predicate",
                claim_holds=value,
                evidence=evidence,
            ),
            {"complete": True, "scope": "declared exact assignment"},
        )
    raise ClaimSpecError("formal claim is not a registered exact claim")


def _evaluate_finite(
    request: Mapping[str, Any],
) -> tuple[
    str,
    dict[str, Any],
    dict[str, Any] | None,
    dict[str, Any],
]:
    claim = dict(request["formal_claim"])
    variables = claim.get("variables")
    predicate = claim.get("predicate")
    quantifier = claim.get("quantifier", "forall")
    if (
        claim.get("claim_kind") != "finite_model"
        or not isinstance(variables, Mapping)
        or not variables
        or not isinstance(predicate, str)
        or quantifier not in {"forall", "exists"}
    ):
        raise ClaimSpecError("formal claim is not a registered finite-model claim")
    names = sorted(variables)
    domains: list[list[Any]] = []
    for name in names:
        values = variables[name]
        if not isinstance(name, str) or not name.isidentifier():
            raise ClaimSpecError("finite variable name is invalid")
        if not isinstance(values, list) or not values:
            raise ClaimSpecError("finite domains must be non-empty lists")
        domains.append(values)
    state_count = math.prod(len(values) for values in domains)
    max_states = claim.get("max_states", state_count)
    if (
        isinstance(max_states, bool)
        or not isinstance(max_states, int)
        or max_states < 1
    ):
        raise ClaimSpecError("finite max_states must be a positive integer")
    explored = 0
    witness: dict[str, Any] | None = None
    counterexample: dict[str, Any] | None = None
    for values in itertools.product(*domains):
        if explored >= max_states:
            break
        assignment = dict(zip(names, values, strict=True))
        outcome = _safe_expression(predicate, assignment)
        if type(outcome) is not bool:
            raise ClaimSpecError("finite predicate must evaluate to boolean")
        explored += 1
        if outcome and witness is None:
            witness = assignment
        if not outcome and counterexample is None:
            counterexample = assignment
        if quantifier == "forall" and counterexample is not None:
            break
        if quantifier == "exists" and witness is not None:
            break
    decisive_early = (
        quantifier == "forall" and counterexample is not None
    ) or (quantifier == "exists" and witness is not None)
    complete = explored == state_count or decisive_early
    completeness = {
        "complete": complete,
        "explored": explored,
        "state_count": state_count,
        "max_states": max_states,
        "scope": "declared finite Cartesian domains",
    }
    if not complete:
        return (
            "inconclusive",
            {
                "kind": "finite_model_result",
                "adapter_status": "resource_exhausted",
                "claim_holds": None,
                "explored": explored,
                "state_count": state_count,
            },
            None,
            completeness,
        )
    holds = counterexample is None if quantifier == "forall" else witness is not None
    evidence = {
        "quantifier": quantifier,
        "predicate": predicate,
        "domains": {name: list(variables[name]) for name in names},
        "witness": witness,
        "counterexample": counterexample,
        "explored": explored,
        "state_count": state_count,
        "decisive_early": decisive_early,
    }
    verdict = (
        "claim_validated_within_declared_scope"
        if holds
        else "counterexample_validated_within_declared_scope"
    )
    return (
        verdict,
        {
            "kind": "finite_model_result",
            "adapter_status": "succeeded" if holds else "counterexample",
            "claim_holds": holds,
            "witness": witness,
            "counterexample": counterexample,
            "explored": explored,
            "state_count": state_count,
        },
        _certificate(
            request,
            certificate_kind="finite_model_exhaustion",
            claim_holds=holds,
            evidence=evidence,
        ),
        completeness,
    )


def execute(raw: Mapping[str, Any]) -> dict[str, Any]:
    """Return one exact response for a validated built-in request."""

    request = _validate_request(raw)
    try:
        if request["adapter"] == "exact":
            verdict, result, certificate, completeness = _evaluate_exact(request)
            uncertainty = {"kind": "none_exact_rational_arithmetic"}
        else:
            verdict, result, certificate, completeness = _evaluate_finite(request)
            uncertainty = {"kind": "none_finite_deterministic"}
    except ClaimSpecError as exc:
        verdict = "inconclusive"
        result = {
            "kind": "claim_spec_rejection",
            "adapter_status": "invalid_spec",
            "claim_holds": None,
            "reason": str(exc),
        }
        certificate = None
        completeness = {
            "complete": False,
            "scope": "claim_rejected_before_evaluation",
        }
        uncertainty = {"kind": "not_evaluated_invalid_claim"}

    response: dict[str, Any] = {
        "schema_version": 3,
        "contract_version": WORKER_RESPONSE_CONTRACT_VERSION,
        "message_kind": "proof_execution_response",
        "response_id": _stable_identifier(
            "proof-execution-worker-response-v3",
            request["request_id"],
            request["binding_digest"],
            verdict,
            result,
            certificate,
            completeness,
        ),
        "request_id": request["request_id"],
        "binding_id": request["binding_id"],
        "binding_digest": request["binding_digest"],
        "execution_claim_id": request["execution_claim_id"],
        "execution_claim_digest": request["execution_claim_digest"],
        "attempt_id": request["attempt_id"],
        "attempt_number": request["attempt_number"],
        "handoff_id": request["handoff_id"],
        "handoff_digest": request["handoff_digest"],
        "formal_claim_digest": request["formal_claim_digest"],
        "adapter": request["adapter"],
        "runtime_route_id": request["runtime_route_id"],
        "proof_verdict": verdict,
        "result": result,
        "scoped_certificate": certificate,
        "completeness": completeness,
        "uncertainty": uncertainty,
        "artifact": None,
        "authority_boundary": (
            "response_is_claim_bound_finite_evaluation_evidence_and_requires_"
            "parent_process_protocol_and_certificate_validation"
        ),
        "authority_nulls": dict(_AUTHORITY_NULLS),
    }
    if frozenset(response) | {"content_digest"} != _RESPONSE_KEYS:
        raise AssertionError("internal worker response shape drift")
    response["content_digest"] = _self_digest(response)
    return response


def main() -> int:
    """Read one request and emit one response; errors are operational only."""

    try:
        raw = sys.stdin.buffer.read()
        if not raw or len(raw) > 8 * 1024 * 1024:
            raise WorkerProtocolError("proof worker stdin is empty or oversized")
        value = json.loads(raw.decode("utf-8"))
        if not isinstance(value, Mapping) or _canonical_bytes(value) != raw:
            raise WorkerProtocolError("proof worker stdin is not one canonical object")
        response = execute(value)
    except Exception as exc:
        sys.stderr.write(f"{type(exc).__name__}: {exc}\n")
        return 2
    sys.stdout.buffer.write(_canonical_bytes(response))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
