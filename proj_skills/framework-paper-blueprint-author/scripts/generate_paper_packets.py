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
"""Create digest-bound paper blueprints and controlled section packets."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


SECTIONS = (
    ("abstract", "Abstract", "framework-paper-abstract-writer"),
    ("introduction", "Introduction", "framework-paper-introduction-writer"),
    ("related-work", "Related Work", "framework-paper-related-work-writer"),
    ("method", "Method", "framework-paper-method-writer"),
    ("architecture", "Architecture", "framework-paper-architecture-writer"),
    ("implementation", "Implementation", "framework-paper-implementation-writer"),
    ("evaluation", "Evaluation", "framework-paper-evaluation-writer"),
    ("limitations", "Limitations", "framework-paper-limitations-writer"),
    ("conclusion", "Conclusion", "framework-paper-conclusion-writer"),
)
BODY = {item[0] for item in SECTIONS} - {"abstract", "conclusion"}
ELIGIBLE_CLAIM_STATUSES = {"declared", "observed", "replayed", "inferred", "verified"}
LITERATURE_REQUIRED_CLASSES = {"comparative", "novelty"}
RESULT_REQUIRED_CLASSES = {"evaluative"}


def load(path: Path) -> Any:
    with path.open(encoding="utf-8") as stream:
        return json.load(stream)


def canonical_digest(items: list[Any]) -> str:
    payload = json.dumps(items, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    return "sha256:" + hashlib.sha256(payload.encode()).hexdigest()


def claim_id(claim: dict[str, Any]) -> str:
    value = claim.get("claim_id", claim.get("id"))
    if not isinstance(value, str) or not value:
        raise ValueError("every ledger claim needs claim_id")
    return value


def claims_from(ledger: dict[str, Any]) -> list[dict[str, Any]]:
    claims = ledger.get("claims")
    if not isinstance(claims, list):
        raise ValueError("claim ledger must contain a claims array")
    return [item for item in claims if isinstance(item, dict)]


def has_literature_authority(snapshot: Any) -> bool:
    if (
        not isinstance(snapshot, dict)
        or snapshot.get("status") not in {"valid", "frozen"}
        or not str(snapshot.get("content_digest", "")).startswith("sha256:")
        or not snapshot.get("query_protocol")
    ):
        return False
    records = snapshot.get("records", [])
    return bool(records) and all(
        isinstance(record, dict)
        and record.get("citation_key")
        and record.get("content_digest", "").startswith("sha256:")
        and record.get("source_version")
        and record.get("provenance")
        and record.get("correction_state") in {"none_known", "corrected", "retracted", "unknown"}
        and record.get("conflict_state") in {"none_known", "conflicting", "unknown"}
        and any(record.get(key) for key in ("doi", "arxiv_id", "publisher_url"))
        for record in records
    )


def has_result_authority(packet: Any) -> bool:
    if not isinstance(packet, dict) or packet.get("authorization_status") != "authorized":
        return False
    required = ("protocol_id", "receipt_digests", "metric_definitions", "limitations", "uncertainty", "replication")
    return (
        all(packet.get(key) for key in required)
        and packet.get("evidence_tier") in {"observed_single_run", "externally_authorized_replicated"}
        and str(packet.get("content_digest", "")).startswith("sha256:")
        and all(
        isinstance(value, str) and value.startswith("sha256:")
        for value in packet["receipt_digests"]
        )
    )


def allocated_sections(claim: dict[str, Any]) -> list[str]:
    explicit = claim.get("allowed_sections", claim.get("section_ids", claim.get("target_sections", [])))
    if explicit:
        return [value for value in explicit if value in {item[0] for item in SECTIONS}]
    kind = claim.get("claim_class", claim.get("class", "descriptive"))
    return {
        "evaluative": ["evaluation", "limitations"],
        "comparative": ["related-work", "introduction"],
        "novelty": ["related-work", "introduction"],
        "proposed": ["method", "limitations"],
        "interpretive": ["method", "architecture"],
    }.get(kind, ["introduction", "method", "implementation"])


def command_blueprint(args: argparse.Namespace) -> None:
    ledger = load(args.ledger)
    abstraction = load(args.abstraction)
    literature = load(args.literature) if args.literature else None
    results = load(args.result_packet) if args.result_packet else None
    literature_ok = has_literature_authority(literature)
    results_ok = has_result_authority(results)
    assignments = {item[0]: [] for item in SECTIONS}
    non_claims: list[str] = []
    citation_keys = sorted(
        record["citation_key"] for record in (literature or {}).get("records", [])
        if literature_ok and record.get("citation_key")
    )
    for claim in claims_from(ledger):
        cid = claim_id(claim)
        status = claim.get("status", "unknown")
        kind = claim.get("claim_class", claim.get("class", "descriptive"))
        blocked = status not in ELIGIBLE_CLAIM_STATUSES
        blocked |= claim.get("resolution", "accepted") != "accepted"
        blocked |= claim.get("freshness", "current") == "stale"
        blocked |= kind in LITERATURE_REQUIRED_CLASSES and not literature_ok
        blocked |= kind in RESULT_REQUIRED_CLASSES and not results_ok
        if blocked:
            non_claims.append(cid)
            continue
        for section in allocated_sections(claim):
            assignments[section].append(cid)
    body_claims = sorted({cid for section in BODY for cid in assignments[section]})
    assignments["abstract"] = body_claims
    assignments["conclusion"] = body_claims
    sections = []
    for sid, title, owner in SECTIONS:
        if sid == "related-work" and not literature_ok:
            title = "Related Work Evidence Status"
        if sid == "evaluation" and not results_ok:
            title = "Current Evidence Status"
        sections.append({
            "section_id": sid,
            "title": title,
            "owner": owner,
            "allowed_claim_ids": sorted(set(assignments[sid])),
            "required": True,
        })
    thesis = abstraction.get("thesis") or abstraction.get("framework_summary")
    if not isinstance(thesis, str) or not thesis.strip():
        constructs = abstraction.get("constructs", [])
        names = [item.get("name") for item in constructs if isinstance(item, dict) and item.get("name")]
        suffix = ", ".join(names[:3])
        thesis = "This paper describes the framework's evidence-bound functional and workflow abstractions"
        thesis += f", centered on {suffix}." if suffix else "."
    packet = {
        "schema_version": "1.0.0",
        "blueprint_id": args.blueprint_id,
        "title": "An Evidence-Qualified Abstraction of a Repository-Governed AI Workflow",
        "input_digest": canonical_digest([ledger, abstraction, literature, results]),
        "thesis": thesis,
        "paper_kind": "descriptive_framework" if not (literature_ok and results_ok) else "empirical_framework",
        "section_order": [item[0] for item in SECTIONS],
        "sections": sections,
        "glossary": {
            item["name"]: item["definition"] for item in abstraction.get("constructs", [])
            if isinstance(item, dict) and item.get("name") and item.get("definition")
        },
        "notation_ids": abstraction.get("notation_ids", []),
        "figure_plan": abstraction.get("figure_plan", []),
        "non_claims": sorted(set(non_claims)),
        "citation_keys": citation_keys,
    }
    packet["blueprint_digest"] = canonical_digest([packet])
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(packet, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def tex_escape(text: str) -> str:
    replacements = {
        "\\": r"\textbackslash{}", "&": r"\&", "%": r"\%", "$": r"\$",
        "#": r"\#", "_": r"\_", "{": r"\{", "}": r"\}",
        "~": r"\textasciitilde{}", "^": r"\textasciicircum{}",
    }
    return "".join(replacements.get(char, char) for char in text)


def command_section(args: argparse.Namespace) -> None:
    blueprint = load(args.blueprint)
    ledger = load(args.ledger)
    models = [load(path) for path in args.model]
    draft = load(args.draft)
    literature = load(args.literature) if args.literature else None
    results = load(args.result_packet) if args.result_packet else None
    specs = {item["section_id"]: item for item in blueprint["sections"]}
    if args.section_id not in specs:
        raise ValueError(f"section {args.section_id!r} is absent from blueprint")
    spec = specs[args.section_id]
    permitted = set(spec["allowed_claim_ids"])
    known = {claim_id(item) for item in claims_from(ledger)}
    paragraphs = draft.get("paragraphs", [])
    if not isinstance(paragraphs, list):
        raise ValueError("draft paragraphs must be an array")
    consumed: set[str] = set()
    citations: set[str] = set()
    text_parts: list[str] = []
    warnings = list(draft.get("warnings", []))
    for paragraph in paragraphs:
        ids = set(paragraph.get("claim_ids", []))
        if not ids <= permitted or not ids <= known:
            raise ValueError(f"paragraph uses unauthorized claim IDs: {sorted(ids - permitted)}")
        keys = set(paragraph.get("citation_keys", []))
        if not keys <= set(blueprint.get("citation_keys", [])):
            raise ValueError(f"paragraph uses unauthorized citations: {sorted(keys)}")
        consumed |= ids
        citations |= keys
        text_parts.append(tex_escape(str(paragraph.get("text", "")).strip()))
    if args.section_id == "related-work" and not has_literature_authority(literature):
        if citations:
            raise ValueError("repository-only related work cannot cite external literature")
        text_parts = [
            "No provenance-valid literature snapshot was supplied. Comparative and novelty claims therefore remain unknown; systematic literature intake is required before positioning this framework against prior work."
        ]
        warnings.append("literature_snapshot_missing: comparative and novelty claims withheld")
        consumed.clear()
    if args.section_id == "evaluation" and not has_result_authority(results):
        text_parts = [
            "No authorized result packet was supplied. The current evidence establishes only the declared protocols and contract checks represented in the controlled models; efficacy and causal effects remain unknown."
        ]
        warnings.append("authorized_results_missing: efficacy and causal claims withheld")
        consumed.clear()
    if args.section_id in {"abstract", "conclusion"}:
        body_claims = set(draft.get("accepted_body_claim_ids", []))
        if not consumed <= body_claims:
            raise ValueError("abstract/conclusion claims must be entailed by accepted body claims")
    title = spec["title"]
    content = "\n\n".join(filter(None, text_parts))
    if args.section_id == "abstract":
        tex = "\\begin{abstract}\n" + content + "\n\\end{abstract}\n"
    else:
        tex = "\\section{" + tex_escape(title) + "}\n\n" + content + "\n"
    args.tex_output.parent.mkdir(parents=True, exist_ok=True)
    args.tex_output.write_text(tex, encoding="utf-8")
    packet = {
        "schema_version": "1.0.0",
        "section_id": args.section_id,
        "section_owner": spec["owner"],
        "title": title,
        # The assembler interprets input_digest as the frozen source snapshot,
        # while section_digest below binds this packet's full local derivation.
        "input_digest": blueprint["input_digest"],
        "consumed_claim_ids": sorted(consumed),
        "citations": sorted(citations),
        "figure_ids": sorted(set(draft.get("figure_ids", []))),
        "table_ids": sorted(set(draft.get("table_ids", []))),
        "notation_ids": sorted(set(draft.get("notation_ids", []))),
        "unresolved_todos": list(draft.get("unresolved_todos", [])),
        "warnings": sorted(set(warnings)),
        "tex_fragment": args.tex_output.name,
    }
    packet["section_digest"] = canonical_digest([packet])
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(packet, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(description=__doc__)
    commands = root.add_subparsers(required=True)
    blueprint = commands.add_parser("blueprint")
    blueprint.add_argument("--ledger", type=Path, required=True)
    blueprint.add_argument("--abstraction", type=Path, required=True)
    blueprint.add_argument("--literature", type=Path)
    blueprint.add_argument("--result-packet", type=Path)
    blueprint.add_argument("--blueprint-id", default="framework-paper")
    blueprint.add_argument("--output", type=Path, required=True)
    blueprint.set_defaults(func=command_blueprint)
    section = commands.add_parser("section")
    section.add_argument("--blueprint", type=Path, required=True)
    section.add_argument("--ledger", type=Path, required=True)
    section.add_argument("--model", type=Path, action="append", default=[])
    section.add_argument("--draft", type=Path, required=True)
    section.add_argument("--literature", type=Path)
    section.add_argument("--result-packet", type=Path)
    section.add_argument("--section-id", choices=[item[0] for item in SECTIONS], required=True)
    section.add_argument("--output", type=Path, required=True)
    section.add_argument("--tex-output", type=Path, required=True)
    section.set_defaults(func=command_section)
    return root


def main() -> None:
    args = parser().parse_args()
    try:
        args.func(args)
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        raise SystemExit(f"error: {exc}") from exc


if __name__ == "__main__":
    main()
