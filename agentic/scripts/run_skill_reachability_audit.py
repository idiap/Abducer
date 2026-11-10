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
"""Audit skill reachability as an evidence ladder, not a registry mention.

For the six reflective-discovery operators the useful question is whether an
operator was merely documented or whether a real, digest-valid output changed
durable state.  The audit therefore reports seven monotone levels:
``documented -> registered -> routed -> executable -> exercised -> consumed ->
feedback_effective``.  Historical skills retain a conservative projection-only
classification and can never be upgraded by this script without receipts.

``consumed`` and ``feedback_effective`` are deliberately stronger than fields
with those names in an arbitrary JSON document.  They require a canonical-cycle
projection that verifies against the current immutable transaction commit, an
independently recomputed ledger suffix, and the exact producer receipt/output
bytes in the operator workspace.  This keeps the audit an evidence consumer
rather than another self-attestation surface.
"""

from __future__ import annotations

import argparse
import copy
import datetime as dt
import json
import sys
from pathlib import Path
from typing import Any, Iterable, Mapping

from agentic_common import ROOT, load_json_object, rel, write_json

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from agentic.discovery.contracts import (  # noqa: E402
    ContractError,
    canonical_digest,
    validate_payload,
    verify_artifact_descriptor,
)
from agentic.discovery.contracts import Namespace  # noqa: E402
from agentic.discovery.theory_gate import (  # noqa: E402
    DEFAULT_CANONICAL_THEORY_STATE_ROOT,
    authorization_projection,
    verify_canonical_theory_cycle,
)


OPERATOR_REGISTRY = ROOT / "agentic/registries/discovery_operator_registry.yaml"
PROJECTIONS = ROOT / "registry/skill_projections/abducer_skill_projections.json"
DEFAULT_RECEIPTS = ROOT / "agentic/runs/discovery_operator_receipts"
DEFAULT_FEEDBACK = ROOT / "agentic/state/discovery_feedback_edges.json"
DEFAULT_JSON = ROOT / "agentic/reports/skill_reachability/latest.json"
DEFAULT_MARKDOWN = ROOT / "agentic/reports/skill_reachability/latest.md"

LEVELS = (
    "documented",
    "registered",
    "routed",
    "executable",
    "exercised",
    "consumed",
    "feedback_effective",
)


def _json_files(root: Path) -> Iterable[Path]:
    if root.is_file():
        yield root
    elif root.is_dir():
        yield from sorted(root.rglob("*.json"))


def _load_receipts(root: Path) -> list[dict[str, Any]]:
    """Load only schema-valid receipts; malformed evidence stays visible as invalid."""

    receipts: list[dict[str, Any]] = []
    for path in _json_files(root):
        try:
            payload = load_json_object(path)
            validate_payload(payload, "discovery_operator_receipt.schema.json")
        except (OSError, ValueError, ContractError):
            continue
        payload["_receipt_path"] = rel(path) if path.is_relative_to(ROOT) else str(path)
        receipts.append(payload)
    return receipts


def _load_feedback(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    payload = load_json_object(path)
    rows = payload.get("feedback_edges", []) if isinstance(payload, dict) else payload
    if not isinstance(rows, list):
        raise ValueError("feedback evidence must be a list or contain feedback_edges")
    return [dict(row) for row in rows if isinstance(row, Mapping)]


def _command_exists(command: list[Any]) -> bool:
    """Check the repository-backed part of a declared argv route."""

    if not command or not all(isinstance(part, str) and part for part in command):
        return False
    candidates = [part for part in command[1:] if part.endswith((".py", ".sh"))]
    return bool(candidates) and all((ROOT / part).is_file() for part in candidates)


def _receipt_is_exercised(receipt: Mapping[str, Any], artifact_root: Path) -> bool:
    """Verify successful execution and every declared output against its bytes."""

    if receipt.get("status") != "succeeded" or not receipt.get("validator_receipts"):
        return False
    if any(row.get("status") != "passed" for row in receipt["validator_receipts"]):
        return False
    try:
        namespace = Namespace.from_mapping(receipt["identity"])
        for descriptor in receipt.get("output_artifacts", []):
            verify_artifact_descriptor(descriptor, artifact_root, namespace)
    except (KeyError, ContractError):
        return False
    return bool(receipt.get("output_artifacts"))


def _edge_descriptor_digest(rows: Any) -> str:
    """Normalize receipt/edge descriptors before comparing their causal identity."""

    if not isinstance(rows, list):
        raise ContractError("producer output descriptors must be a list")
    normalized: list[dict[str, Any]] = []
    for row in rows:
        if not isinstance(row, Mapping):
            raise ContractError("producer output descriptor is malformed")
        normalized.append(
            {
                "path": row.get("path"),
                "sha256": row.get("sha256"),
                "size_bytes": row.get("size_bytes"),
            }
        )
    return canonical_digest(normalized)


def _verified_feedback_by_receipt(
    *,
    canonical_cycle_path: Path | None,
    canonical_state_root: Path,
    target_id: str | None,
    run_id: str | None,
    receipts: list[dict[str, Any]],
    artifact_root: Path,
) -> tuple[dict[str, dict[str, Any]], dict[str, Any] | None, list[str]]:
    """Bind feedback edges to one exact canonical commit and producer receipt.

    No canonical projection means no trusted consumption evidence.  When a
    projection is supplied, inconsistency is retained as an explicit evidence
    error and the affected receipt cannot advance beyond ``exercised``.
    Structural or registry presence alone is never promoted.
    """

    if canonical_cycle_path is None:
        return {}, None, []

    projection = load_json_object(canonical_cycle_path)
    projected_target = projection.get("target_id")
    projected_run = projection.get("run_id")
    if not isinstance(projected_target, str) or not isinstance(projected_run, str):
        raise ContractError("canonical cycle projection lacks target/run identity")
    if target_id is not None and target_id != projected_target:
        raise ContractError("requested target_id differs from canonical cycle")
    if run_id is not None and run_id != projected_run:
        raise ContractError("requested run_id differs from canonical cycle")

    authorization = verify_canonical_theory_cycle(
        canonical_cycle_path,
        target_id=target_id or projected_target,
        run_id=run_id or projected_run,
        state_root=canonical_state_root,
    )
    by_receipt: dict[str, list[dict[str, Any]]] = {}
    for receipt in receipts:
        by_receipt.setdefault(str(receipt.get("receipt_id", "")), []).append(receipt)
    events = {
        str(event.get("event_id")): event
        for event in projection.get("events", [])
        if isinstance(event, Mapping) and event.get("event_id")
    }

    trusted: dict[str, dict[str, Any]] = {}
    errors: list[str] = []
    for edge in projection.get("feedback_edges", []):
        receipt_id = str(edge.get("producer_receipt_id", ""))
        operator_id = str(edge.get("producer_operator_id", ""))
        candidates = by_receipt.get(receipt_id, [])
        if len(candidates) != 1:
            errors.append(
                f"{operator_id}: expected one exact receipt {receipt_id!r}, found {len(candidates)}"
            )
            continue
        receipt = candidates[0]
        identity = receipt.get("identity", {})
        event = events.get(str(edge.get("consumer_event_id")))
        checks = {
            "receipt_exercised": _receipt_is_exercised(receipt, artifact_root),
            "operator_identity": receipt.get("operator", {}).get("operator_id") == operator_id,
            "request_identity": receipt.get("request_id") == edge.get("producer_request_id"),
            "target_identity": identity.get("target_id") == projected_target,
            "run_identity": identity.get("run_id") == projected_run,
            "state_identity": identity.get("state_version") == projection.get("prior_state_version"),
            "receipt_in_cycle": receipt_id in set(projection.get("input_receipt_ids", [])),
            "consumed_claim": edge.get("consumed") is True,
            "commit_claim": edge.get("state_edge_committed") is True,
            "committed_generation": edge.get("committed_state_generation")
            == projection.get("committed_state_version"),
            "event_exists": event is not None,
            "event_hash": event is not None
            and event.get("event_hash") == edge.get("consumer_event_hash"),
            "event_source": event is not None
            and receipt_id in set(event.get("source_receipt_ids", [])),
            "output_descriptors": _edge_descriptor_digest(receipt.get("output_artifacts", []))
            == _edge_descriptor_digest(edge.get("producer_output_artifacts", [])),
        }
        failed = sorted(name for name, passed in checks.items() if not passed)
        if failed:
            errors.append(f"{operator_id}: feedback evidence failed {failed}")
            continue
        if receipt_id in trusted:
            errors.append(f"{operator_id}: duplicate canonical feedback edge for {receipt_id}")
            trusted.pop(receipt_id, None)
            continue
        trusted[receipt_id] = dict(edge)

    return trusted, authorization, errors


def build_reachability_report(
    *,
    receipt_root: Path = DEFAULT_RECEIPTS,
    feedback_path: Path = DEFAULT_FEEDBACK,
    canonical_cycle_path: Path | None = None,
    canonical_state_root: Path = DEFAULT_CANONICAL_THEORY_STATE_ROOT,
    artifact_root: Path = ROOT,
    target_id: str | None = None,
    run_id: str | None = None,
) -> dict[str, Any]:
    """Build a deterministic, receipt-and-commit-backed reachability report."""

    registry = load_json_object(OPERATOR_REGISTRY)
    operators = {row["operator_id"]: row for row in registry.get("operators", [])}
    projections = load_json_object(PROJECTIONS).get("skills", [])
    projected = {row.get("skill_name"): row for row in projections if isinstance(row, Mapping)}
    receipts = _load_receipts(receipt_root)
    by_operator: dict[str, list[dict[str, Any]]] = {}
    for receipt in receipts:
        by_operator.setdefault(receipt.get("operator", {}).get("operator_id", ""), []).append(receipt)

    # The legacy feedback file remains visible in the report for migration
    # diagnostics, but it cannot establish consumption.  Only a verified
    # canonical transaction may populate this trusted mapping.
    legacy_feedback_count = len(_load_feedback(feedback_path))
    feedback_by_receipt, canonical_authorization, evidence_errors = _verified_feedback_by_receipt(
        canonical_cycle_path=canonical_cycle_path,
        canonical_state_root=canonical_state_root,
        target_id=target_id,
        run_id=run_id,
        receipts=receipts,
        artifact_root=artifact_root,
    )
    names = sorted(set(projected) | set(operators))
    rows: list[dict[str, Any]] = []
    for name in names:
        projection = projected.get(name, {})
        operator = operators.get(name)
        skill_path = Path(str(operator.get("skill_path"))) if operator else Path(str(projection.get("path", ""))) / "SKILL.md"
        documented = bool(str(skill_path)) and (ROOT / skill_path).is_file()
        registered = operator is not None
        routed = bool(operator and isinstance(operator.get("entrypoint"), list))
        executable = bool(operator and _command_exists(operator["entrypoint"]) and _command_exists(operator.get("validator", [])))
        successful = [
            receipt
            for receipt in by_operator.get(name, [])
            if _receipt_is_exercised(receipt, artifact_root)
        ]
        consumed_receipts = [
            receipt
            for receipt in successful
            if feedback_by_receipt.get(receipt["receipt_id"], {}).get("consumed") is True
        ]
        effective_receipts = [
            receipt
            for receipt in consumed_receipts
            if feedback_by_receipt.get(receipt["receipt_id"], {}).get("state_edge_committed") is True
            and isinstance(feedback_by_receipt.get(receipt["receipt_id"], {}).get("consumer_event_id"), str)
            and feedback_by_receipt[receipt["receipt_id"]]["consumer_event_id"].strip()
        ]
        flags = {
            "documented": documented,
            "registered": registered,
            "routed": routed,
            "executable": executable,
            "exercised": bool(successful),
            "consumed": bool(consumed_receipts),
            "feedback_effective": bool(effective_receipts),
        }
        attained = "unreachable"
        for level in LEVELS:
            if flags[level]:
                attained = level
            else:
                break
        rows.append(
            {
                "skill_id": name,
                "operator": registered,
                "attained_level": attained,
                "levels": flags,
                "skill_path": skill_path.as_posix() if str(skill_path) else "",
                "entrypoint": operator.get("entrypoint", []) if operator else [],
                "receipt_ids": [row["receipt_id"] for row in successful],
                "feedback_event_ids": [
                    feedback_by_receipt[row["receipt_id"]]["consumer_event_id"]
                    for row in effective_receipts
                ],
                "evidence_boundary": (
                    "Receipt and committed consumption edge establish feedback-effective execution."
                    if effective_receipts
                    else "Registry, projection, or executable presence alone does not establish use or learning."
                ),
            }
        )

    operator_rows = [row for row in rows if row["operator"]]
    portable_authorization = (
        authorization_projection(canonical_authorization)
        if canonical_authorization is not None
        else None
    )
    if portable_authorization is not None:
        verifier_projection_digest = portable_authorization.pop("authorization_digest")
        for field in (
            "transaction_root",
            "commit_path",
            "manifest_path",
            "projection_path",
        ):
            value = portable_authorization.get(field)
            if not isinstance(value, str):
                continue
            candidate = Path(value)
            if candidate.is_absolute() and candidate.resolve().is_relative_to(ROOT.resolve()):
                portable_authorization[field] = rel(candidate)
        portable_authorization["verifier_issued_projection_digest"] = (
            verifier_projection_digest
        )
        portable_authorization["portable_projection_digest"] = canonical_digest(
            portable_authorization,
            exclude_keys=("portable_projection_digest",),
        )
    return {
        "schema_version": "1.0.0",
        "operator_registry": rel(OPERATOR_REGISTRY),
        "receipt_root": rel(receipt_root) if receipt_root.is_relative_to(ROOT) else str(receipt_root),
        "artifact_root": rel(artifact_root) if artifact_root.is_relative_to(ROOT) else str(artifact_root),
        "legacy_feedback_path": rel(feedback_path) if feedback_path.is_relative_to(ROOT) else str(feedback_path),
        "legacy_feedback_edge_count": legacy_feedback_count,
        "legacy_feedback_authoritative": False,
        "canonical_cycle_path": (
            rel(canonical_cycle_path)
            if canonical_cycle_path is not None and canonical_cycle_path.is_relative_to(ROOT)
            else str(canonical_cycle_path) if canonical_cycle_path is not None else None
        ),
        "canonical_state_root": (
            rel(canonical_state_root)
            if canonical_state_root.is_relative_to(ROOT)
            else str(canonical_state_root)
        ),
        "canonical_authorization": portable_authorization,
        "evidence_errors": evidence_errors,
        "operator_count": len(operator_rows),
        "all_operators_feedback_effective": (
            bool(operator_rows)
            and not evidence_errors
            and all(row["levels"]["feedback_effective"] for row in operator_rows)
        ),
        "skills": rows,
    }



def comparison_projection(report: Mapping[str, Any]) -> dict[str, Any]:
    """Compare audited facts while retaining separately verified clock provenance.

    The caller still runs the current canonical verifier before checking a saved
    report. Only two evaluation instants and their three dependent digests vary
    without changing its meaning. Validate every saved digest before replacing
    those exact values; preserve all identity, freshness, authority and evidence
    fields so a changed decision remains stale. This is integrity checking, not
    an attestation against an attacker able to replace all local evidence.
    """
    compared = copy.deepcopy(dict(report))
    authorization = compared.get("canonical_authorization")
    if authorization is None:
        return compared
    if not isinstance(authorization, dict):
        raise ContractError("reachability authorization must be an object")
    if authorization.get("portable_projection_digest") != canonical_digest(
        authorization, exclude_keys=("portable_projection_digest",)
    ):
        raise ContractError("reachability portable projection digest is invalid")
    # Reverse only the documented four portable path rewrites before checking the
    # original verifier-issued digest. All other original fields stay untouched.
    verifier_projection = copy.deepcopy(authorization)
    verifier_projection.pop("portable_projection_digest")
    verifier_digest = verifier_projection.pop("verifier_issued_projection_digest", None)
    for field in ("transaction_root", "commit_path", "manifest_path", "projection_path"):
        value = verifier_projection.get(field)
        if isinstance(value, str) and not Path(value).is_absolute():
            verifier_projection[field] = str((ROOT / value).resolve())
    if verifier_digest != canonical_digest(verifier_projection):
        raise ContractError("reachability verifier projection digest is invalid")
    decision = authorization.get("present_investment_decision")
    if isinstance(decision, dict):
        if authorization.get("present_investment_decision_digest") != canonical_digest(decision):
            raise ContractError("reachability present decision digest is invalid")
        instant = decision.get("evaluated_at")
        if not isinstance(instant, str) or authorization.get("literature_present_use_evaluated_at") != instant:
            raise ContractError("reachability evaluation instant join is invalid")
        try:
            parsed = dt.datetime.fromisoformat(instant.replace("Z", "+00:00"))
        except ValueError as exc:
            raise ContractError("reachability evaluation instant is invalid") from exc
        if parsed.tzinfo is None:
            raise ContractError("reachability evaluation instant lacks timezone")
        decision["evaluated_at"] = "<verified-evaluation-instant>"
        authorization["literature_present_use_evaluated_at"] = "<verified-evaluation-instant>"
        authorization["present_investment_decision_digest"] = "<verified-decision-digest>"
    # Null historical decisions remain null and do not become current authority.
    authorization["verifier_issued_projection_digest"] = "<verified-projection-digest>"
    authorization["portable_projection_digest"] = "<verified-portable-digest>"
    return compared

def render_markdown(report: Mapping[str, Any]) -> str:
    lines = [
        "# Skill Reachability Audit",
        "",
        "Presence is not execution. Each column requires the preceding evidence level plus its own durable evidence.",
        "",
        "| Skill | Attained | Registered | Executable | Exercised | Consumed | Feedback-effective |",
        "| --- | --- | ---: | ---: | ---: | ---: | ---: |",
    ]
    for row in report["skills"]:
        flags = row["levels"]
        mark = lambda key: "yes" if flags[key] else "no"  # noqa: E731 - table helper
        lines.append(
            f"| `{row['skill_id']}` | `{row['attained_level']}` | {mark('registered')} | "
            f"{mark('executable')} | {mark('exercised')} | {mark('consumed')} | {mark('feedback_effective')} |"
        )
    lines.extend(
        [
            "",
            f"All {report['operator_count']} registered discovery operators feedback-effective: `{'yes' if report['all_operators_feedback_effective'] else 'no'}`.",
            "",
            (
                "Authority: exact canonical cycle, CAS manifest, event-chain, producer receipt, and output bytes verified."
                if report.get("canonical_authorization") and not report.get("evidence_errors")
                else "Authority: no complete canonical evidence chain was verified."
            ),
            "",
            "A negative result is an honest evidence gap, not an implicit invocation.",
        ]
    )
    if report.get("evidence_errors"):
        lines.extend(["", "Evidence errors:"])
        lines.extend(f"- {error}" for error in report["evidence_errors"])
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--receipt-root", type=Path, default=DEFAULT_RECEIPTS)
    parser.add_argument("--feedback-edges", type=Path, default=DEFAULT_FEEDBACK)
    parser.add_argument(
        "--canonical-cycle",
        type=Path,
        help="Exact immutable-cycle result projection; required for consumed/effective claims.",
    )
    parser.add_argument(
        "--canonical-state-root",
        type=Path,
        default=DEFAULT_CANONICAL_THEORY_STATE_ROOT,
    )
    parser.add_argument(
        "--artifact-root",
        type=Path,
        default=ROOT,
        help="Dispatcher workspace against which receipt output descriptors are verified.",
    )
    parser.add_argument("--target-id")
    parser.add_argument("--run-id")
    parser.add_argument("--json-output", type=Path, default=DEFAULT_JSON)
    parser.add_argument("--markdown-output", type=Path, default=DEFAULT_MARKDOWN)
    parser.add_argument("--require-feedback-effective", action="store_true")
    parser.add_argument(
        "--check",
        action="store_true",
        help="compare deterministic output with existing files without writing them",
    )
    args = parser.parse_args()
    try:
        report = build_reachability_report(
            receipt_root=args.receipt_root,
            feedback_path=args.feedback_edges,
            canonical_cycle_path=args.canonical_cycle,
            canonical_state_root=args.canonical_state_root,
            artifact_root=args.artifact_root,
            target_id=args.target_id,
            run_id=args.run_id,
        )
        rendered = render_markdown(report)
        if args.check:
            existing_json = load_json_object(args.json_output)
            # Canonical serialization preserves JSON type distinctions (1 != true).
            if canonical_digest(comparison_projection(existing_json)) != canonical_digest(comparison_projection(report)):
                raise ContractError(
                    f"reachability JSON is stale: {args.json_output}"
                )
            if args.markdown_output.read_text(encoding="utf-8") != rendered:
                raise ContractError(
                    f"reachability Markdown is stale: {args.markdown_output}"
                )
        else:
            write_json(args.json_output, report)
            args.markdown_output.parent.mkdir(parents=True, exist_ok=True)
            args.markdown_output.write_text(rendered, encoding="utf-8")
    except (OSError, ValueError, ContractError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    verb = "validated" if args.check else "wrote"
    print(
        f"{verb} {args.markdown_output} and {args.json_output}; "
        f"feedback_effective={report['all_operators_feedback_effective']}"
    )
    return 1 if args.require_feedback_effective and not report["all_operators_feedback_effective"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
