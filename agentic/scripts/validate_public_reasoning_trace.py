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
"""Validate public reasoning traces beyond their JSON shape.

The validator deliberately checks inspectable, artifact-grounded summaries. It
does not require or accept private chain-of-thought as evidence.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

from agentic_common import ROOT, load_json_object, rel


EVIDENCE_RELATIONS = {"supports", "refutes", "constrains", "background"}
EPISTEMIC_UPGRADES = {"validated", "accepted", "established", "proved", "theorem"}
ROUTE_A_SPECIALISTS = {
    "routea-geometric-collar-builder", "routea-same-theory-normalization-certifier",
    "routea-geometric-coefficient-extractor", "routea-finite-margin-evaluator",
    "routea-margin-endpoint-certifier", "routea-endpoint-error-budget-certifier",
    "routea-endpoint-local-integral-calculator", "routea-same-theory-factorization-hunter",
    "routea-collar-redesign-forger", "routea-continuum-gap-gatekeeper",
}
DEFAULT_TRACE_GLOB = "tests/fixtures/reasoning_trace/generated/*.trace.json"
EXPECTED_RELEASE_STEMS = {
    "conceptual_frontier_deepening",
    "deep_review_and_reorientation",
    "evidence_to_proof_route_onramp",
    "manuscript_result_elaboration",
    "manuscript_result_elaboration-route_a",
    "scientific_contribution_cultivation",
    "theorem_proof_delivery",
}
REQUIRED_COVERAGE_DIMENSIONS = {
    "control_covered",
    "semantic_covered",
    "evidence_resolved",
    "authority_covered",
    "html_visible",
}


@dataclass(frozen=True)
class TraceIssue:
    code: str
    location: str
    message: str

    def render(self) -> str:
        return f"{self.code} at {self.location}: {self.message}"


def _events(trace: dict[str, Any]) -> list[dict[str, Any]]:
    raw = trace.get("events", trace.get("timeline", []))
    return [event for event in raw if isinstance(event, dict)] if isinstance(raw, list) else []


def _identity(event: dict[str, Any]) -> str:
    return str(event.get("event_id") or event.get("id") or "")


def _parents(event: dict[str, Any]) -> list[str]:
    raw = event.get("causal_parent_event_ids", event.get("parent_event_ids", event.get("parents", [])))
    return [str(value) for value in raw] if isinstance(raw, list) else []


def _walk_values(value: Any, location: str = "$") -> Iterable[tuple[str, Any]]:
    yield location, value
    if isinstance(value, dict):
        for key, item in value.items():
            yield from _walk_values(item, f"{location}.{key}")
    elif isinstance(value, list):
        for index, item in enumerate(value):
            yield from _walk_values(item, f"{location}[{index}]")


def validate_trace(trace: dict[str, Any]) -> list[TraceIssue]:
    issues: list[TraceIssue] = []
    run = trace.get("run", trace.get("identity", trace))
    if not isinstance(run, dict):
        run = {}
    for field in ("run_id", "workflow_id"):
        if not run.get(field) and not trace.get(field):
            issues.append(TraceIssue("missing-run-identity", "$", f"missing {field}"))

    events = _events(trace)
    if not events:
        issues.append(TraceIssue("empty-trace", "$.events", "no public events are present"))
        return issues

    by_id: dict[str, dict[str, Any]] = {}
    artifact_by_id: dict[str, dict[str, Any]] = {}
    receipt_by_id: dict[str, dict[str, Any]] = {}
    artifact_rows = list(trace.get("artifacts", [])) if isinstance(trace.get("artifacts"), list) else []
    receipt_rows = list(trace.get("receipts", [])) if isinstance(trace.get("receipts"), list) else []
    for event in events:
        artifact_rows.extend(event.get("artifacts", []) if isinstance(event.get("artifacts"), list) else [])
        receipt_rows.extend(event.get("receipts", []) if isinstance(event.get("receipts"), list) else [])
    for row in artifact_rows + receipt_rows:
        if not isinstance(row, dict):
            continue
        if row.get("artifact_id"):
            artifact_by_id[str(row["artifact_id"])] = row
        if row.get("receipt_id"):
            receipt_by_id[str(row["receipt_id"])] = row
    last_sequence: int | None = None
    for index, event in enumerate(events):
        location = f"$.events[{index}]"
        event_id = _identity(event)
        if not event_id:
            issues.append(TraceIssue("missing-event-id", location, "event_id is required"))
        elif event_id in by_id:
            issues.append(TraceIssue("duplicate-event-id", location, event_id))
        else:
            by_id[event_id] = event
        sequence = event.get("sequence")
        if not isinstance(sequence, int):
            issues.append(TraceIssue("invalid-sequence", location, "sequence must be an integer"))
        elif last_sequence is not None and sequence <= last_sequence:
            issues.append(TraceIssue("non-monotonic-sequence", location, f"{sequence} follows {last_sequence}"))
        else:
            last_sequence = sequence

        family = str(event.get("event_family", event.get("family", "")))
        if family in {"inference", "public_inference", "transformation", "validation", "claim", "decision"}:
            inference = event.get("public_inference", event.get("inference", event))
            if not isinstance(inference, dict):
                inference = {}
            for key in ("question", "warrant", "conclusion"):
                if not inference.get(key):
                    issues.append(TraceIssue("missing-public-rationale", location, f"inference needs {key}"))
            if not inference.get("premises"):
                issues.append(TraceIssue("missing-public-rationale", location, "inference needs typed premises"))

        for ev_index, evidence in enumerate(event.get("evidence", [])):
            if not isinstance(evidence, dict):
                issues.append(TraceIssue("malformed-evidence", f"{location}.evidence[{ev_index}]", "must be an object"))
                continue
            relation = evidence.get("relation")
            if relation not in EVIDENCE_RELATIONS:
                issues.append(TraceIssue("invalid-evidence-relation", f"{location}.evidence[{ev_index}]", repr(relation)))
            digest = evidence.get("digest")
            if digest is not None and not re.fullmatch(r"(?:sha256:)?[0-9a-fA-F]{64}", str(digest)):
                issues.append(TraceIssue("malformed-evidence-digest", f"{location}.evidence[{ev_index}]", "expected SHA-256"))

        status = str(event.get("claim_epistemic_status", "")).lower()
        authority = event.get("authority", {})
        can_upgrade = isinstance(authority, dict) and bool(
            authority.get("epistemic_upgrade") or authority.get("exercised")
        )
        if status in EPISTEMIC_UPGRADES and not can_upgrade:
            issues.append(TraceIssue("authority-free-epistemic-upgrade", location, status))

        inference_payload = event.get("public_inference") if isinstance(event.get("public_inference"), dict) else event
        novelty_claim_text = " ".join(
            str(inference_payload.get(field, "")) for field in ("question", "conclusion")
        ).lower()
        exercised_text = json.dumps(authority.get("exercised", []) if isinstance(authority, dict) else []).lower()
        if status in {"evidence_backed", "validated"} and re.search(r"\bnovel(?:ty)?\b", novelty_claim_text) \
                and "novelty" not in exercised_text:
            issues.append(TraceIssue("novelty-inflation", location, "novelty claims require explicit novelty-assessment authority"))

        inference = event.get("public_inference") if isinstance(event.get("public_inference"), dict) else {}
        scope = event.get("scope_transition")
        if isinstance(scope, dict) and scope.get("widens") is True and not scope.get("evidence"):
            issues.append(TraceIssue("unsupported-scope-widening", location, "scope widening needs explicit evidence"))
        public_scope = event.get("scope") if isinstance(event.get("scope"), dict) else inference.get("scope", {})
        if isinstance(public_scope, dict):
            before = str(public_scope.get("before", "")).lower()
            after = str(public_scope.get("after", "")).lower()
            if before and after and before != after and (not event.get("evidence") or not can_upgrade):
                issues.append(TraceIssue("unsupported-scope-transition", location, "scope changes need evidence and explicit authority"))
            if "finite" in before and "continuum" in after and status not in {"unknown", "conjectural", "quarantined", "not_applicable"}:
                issues.append(TraceIssue("finite-to-continuum-promotion", location, "finite evidence cannot silently establish a continuum claim"))

        if event.get("step_id") == "blind_adjudicate":
            serialized = json.dumps(event, sort_keys=True).lower()
            if any(marker in serialized for marker in ("author_identity", "candidate_owner", "agent_identity")):
                issues.append(TraceIssue("blind-identity-leak", location, "candidate identity is visible during adjudication"))

        workflow_id = str(event.get("workflow_id") or run.get("workflow_id") or trace.get("workflow_id") or "")
        if workflow_id == "deep_review_and_reorientation" and isinstance(authority, dict):
            exercised = " ".join(map(str, authority.get("exercised", []))).lower()
            if any(marker in exercised for marker in ("proof acceptance", "proof_acceptance", "release authority", "epistemic upgrade")):
                issues.append(TraceIssue("review-authority-escalation", location, "review workflow has advisory and repair authority only"))

        if family == "skip" and not (event.get("warrant") or event.get("conclusion") or event.get("control", {}).get("reason")):
            issues.append(TraceIssue("unexplained-skip", location, "a conditional skip needs a public reason"))

        for artifact_id in event.get("parent_artifact_ids", []):
            if artifact_by_id and str(artifact_id) not in artifact_by_id:
                issues.append(TraceIssue("missing-parent-artifact", location, str(artifact_id)))

        for ev_index, evidence in enumerate(event.get("evidence", [])):
            if not isinstance(evidence, dict):
                continue
            evidence_location = f"{location}.evidence[{ev_index}]"
            receipt_id = evidence.get("receipt_id")
            if receipt_id:
                receipt = receipt_by_id.get(str(receipt_id))
                if receipt is None:
                    issues.append(TraceIssue("unbound-evidence-receipt", evidence_location, str(receipt_id)))
                else:
                    for field in ("path", "digest"):
                        if evidence.get(field) and receipt.get(field) and evidence[field] != receipt[field]:
                            issues.append(TraceIssue("receipt-binding-mismatch", evidence_location, f"{field} differs from receipt {receipt_id}"))
            digest = evidence.get("digest")
            path = evidence.get("path")
            if digest and path and not evidence.get("external", False):
                candidate = ROOT / str(path)
                if candidate.is_file():
                    expected = str(digest).removeprefix("sha256:").lower()
                    actual = hashlib.sha256(candidate.read_bytes()).hexdigest()
                    if actual != expected:
                        issues.append(TraceIssue("evidence-digest-mismatch", evidence_location, f"expected {expected}, observed {actual}"))

    for index, event in enumerate(events):
        for parent in _parents(event):
            if parent not in by_id:
                issues.append(TraceIssue("missing-causal-parent", f"$.events[{index}]", parent))

    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(event_id: str) -> None:
        if event_id in visiting:
            issues.append(TraceIssue("causal-cycle", f"$.events[{event_id}]", "causal graph is cyclic"))
            return
        if event_id in visited or event_id not in by_id:
            return
        visiting.add(event_id)
        for parent in _parents(by_id[event_id]):
            visit(parent)
        visiting.remove(event_id)
        visited.add(event_id)

    for event_id in by_id:
        visit(event_id)

    profile_id = str(run.get("profile_id") or trace.get("profile_id") or "")
    if profile_id == "route_a":
        observed_specialists = {str(event.get("skill", "")) for event in events}
        missing = sorted(ROUTE_A_SPECIALISTS - observed_specialists)
        if missing:
            issues.append(TraceIssue("missing-route-a-specialists", "$.events", ", ".join(missing)))
        if not any(event.get("skill") == "routea-symbolic-cas-auditor" or event.get("step_id") == "routea_symbolic_audit" for event in events):
            issues.append(TraceIssue("missing-route-a-cas-audit", "$.events", "symbolic/CAS audit needs an event or justified skip"))

    for location, value in _walk_values(trace):
        if isinstance(value, str):
            candidate = Path(value)
            if (candidate.is_absolute() or ".." in candidate.parts) and any(
                marker in location.lower() for marker in ("path", "artifact", "evidence")
            ):
                issues.append(TraceIssue("non-portable-path", location, value))

    return issues


def validate_release_companions(path: Path, trace: dict[str, Any]) -> list[TraceIssue]:
    """Check that one committed trace has matching expert HTML and coverage evidence."""

    issues: list[TraceIssue] = []
    stem = path.name.removesuffix(".trace.json")
    packet_path = path.with_name(f"{stem}.packet.json")
    html_path = path.with_name(f"{stem}.html")
    coverage_path = ROOT / "agentic/reports/reasoning_trace_coverage/by_workflow" / f"{stem}.json"
    for companion in (packet_path, html_path, coverage_path):
        if not companion.is_file():
            issues.append(TraceIssue("missing-release-companion", "$", rel(companion)))
    if issues:
        return issues

    packet = load_json_object(packet_path)
    page = html_path.read_text(encoding="utf-8")
    match = re.search(
        r'<script id="trace-data" type="application/json">(.*?)</script>', page, re.DOTALL
    )
    if not match:
        issues.append(TraceIssue("missing-embedded-packet", "$html", rel(html_path)))
    else:
        try:
            embedded = json.loads(match.group(1))
        except json.JSONDecodeError as exc:
            issues.append(TraceIssue("invalid-embedded-packet", "$html", str(exc)))
        else:
            if embedded != packet:
                issues.append(TraceIssue("stale-html-packet", "$html", rel(html_path)))
    lower = page.lower()
    for marker in ("<script src=", "<link ", "http://", "https://", "@import", "<img "):
        if marker in lower:
            issues.append(TraceIssue("non-offline-html", "$html", marker))

    trace_identity = trace.get("identity") if isinstance(trace.get("identity"), dict) else trace
    packet_identity = packet.get("identity", {})
    for key in ("run_id", "workflow_id", "profile_id"):
        if str(trace_identity.get(key) or "") != str(packet_identity.get(key) or ""):
            issues.append(TraceIssue("companion-identity-mismatch", f"$packet.identity.{key}", stem))

    coverage = load_json_object(coverage_path)
    for dimension in REQUIRED_COVERAGE_DIMENSIONS:
        metric = coverage.get("summary", {}).get(dimension, {})
        if metric.get("percent") != 100.0:
            issues.append(
                TraceIssue(
                    "incomplete-release-coverage",
                    f"$coverage.summary.{dimension}",
                    repr(metric.get("percent")),
                )
            )
    return issues


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "trace",
        type=Path,
        nargs="*",
        help=(
            "Trace JSON files to validate. When omitted, validate every committed "
            f"named-workflow release fixture matching {DEFAULT_TRACE_GLOB}."
        ),
    )
    parser.add_argument("--quiet", action="store_true")
    args = parser.parse_args()
    paths = [path if path.is_absolute() else ROOT / path for path in args.trace]
    release_mode = not paths
    if release_mode:
        paths = sorted(ROOT.glob(DEFAULT_TRACE_GLOB))
        if not paths:
            print(f"ERROR: no default public reasoning traces match {DEFAULT_TRACE_GLOB}")
            return 1
        observed_stems = {path.name.removesuffix(".trace.json") for path in paths}
        if observed_stems != EXPECTED_RELEASE_STEMS:
            missing = sorted(EXPECTED_RELEASE_STEMS - observed_stems)
            extra = sorted(observed_stems - EXPECTED_RELEASE_STEMS)
            print(f"ERROR: release fixture set mismatch: missing={missing}, extra={extra}")
            return 1
    failed = False
    for path in paths:
        payload = load_json_object(path)
        issues = validate_trace(payload)
        if release_mode:
            issues.extend(validate_release_companions(path, payload))
        if issues:
            failed = True
            for issue in issues:
                print(f"ERROR: {rel(path)}: {issue.render()}")
        elif not args.quiet:
            print(f"Validated public reasoning trace: {rel(path)}")
    if failed:
        return 1
    if not args.quiet and len(paths) > 1:
        print(f"Validated {len(paths)} public reasoning trace and HTML release fixtures.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
