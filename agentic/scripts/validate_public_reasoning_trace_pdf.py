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
"""Read-only cross-format validator for expert public reasoning-trace PDFs.

The packet remains the semantic authority.  This module checks projection
completeness; it never derives a scientific conclusion from TeX or PDF layout.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

from build_reasoning_trace_pdf_manifest import validate_manifest_bindings
from reasoning_trace_print_model import select_print_lens


ROOT = Path(__file__).resolve().parents[2]
GENERATED = ROOT / "tests/fixtures/reasoning_trace/generated"
EXPECTED_STEMS = {
    "conceptual_frontier_deepening",
    "deep_review_and_reorientation",
    "evidence_to_proof_route_onramp",
    "manuscript_result_elaboration",
    "manuscript_result_elaboration-route_a",
    "scientific_contribution_cultivation",
    "theorem_proof_delivery",
}
MATERIAL_OVERFULL_PT = 12.0
TEMPLATE_PATHS = tuple(sorted((ROOT / "agentic/templates").glob("*reasoning_trace*.tex")))


@dataclass(frozen=True)
class PdfTraceIssue:
    code: str
    location: str
    message: str

    def render(self) -> str:
        return f"{self.code} at {self.location}: {self.message}"


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _norm(value: Any) -> str:
    text = str(value).replace("\u2010", "-").replace("\u2011", "-").replace("\u2013", "-").replace("\u2212", "-")
    # pdftotext preserves discretionary line-end hyphens inserted by TeX.  They
    # are layout, not packet semantics (``indepen-\ndently`` is still
    # ``independently``), so remove only alpha-to-alpha line-wrap hyphens.
    text = re.sub(r"(?<=[A-Za-z])-\s*\n\s*(?=[A-Za-z])", "", text)
    return re.sub(r"\s+", " ", text).strip().casefold()


def semantic_visible(needle: Any, haystack: str) -> bool:
    normalized = _norm(needle)
    normalized_haystack = _norm(haystack)
    if normalized in normalized_haystack:
        return True
    # TeX tables can wrap stable dotted IDs at arbitrary boundaries.  This
    # whitespace-insensitive comparison is restricted to identifier tokens.
    if normalized and re.fullmatch(r"[a-z0-9_.:-]+", normalized):
        compact_haystack = re.sub(r"\s+", "", normalized_haystack)
        if re.sub(r"\s+", "", normalized) in compact_haystack:
            return True
        # A long digest can be interrupted by the adjacent column when
        # pdftotext linearizes a multipage table.  Its independently visible
        # prefix and suffix still identify it; tuple membership is protected
        # by the digest-bound inventory.
        compact_identifier = re.sub(r"[^a-z0-9]", "", normalized)
        compact_alnum_haystack = re.sub(r"[^a-z0-9]", "", normalized_haystack)
        if "_" in normalized:
            components = [re.sub(r"[^a-z0-9]", "", part) for part in normalized.split("_")]
            components = [part for part in components if len(part) >= 4]
            if components and all(part in compact_alnum_haystack for part in components):
                return True
        if len(compact_identifier) >= 32:
            return compact_identifier[:16] in compact_alnum_haystack and compact_identifier[-16:] in compact_alnum_haystack
        # Multi-column text extraction may interleave another column between a
        # dotted ID's prefix and digest.  Both unique components must survive.
        if "." in normalized:
            prefix, suffix = normalized.rsplit(".", 1)
            compact_alnum_haystack = re.sub(r"[^a-z0-9]", "", normalized_haystack)
            compact_suffix = re.sub(r"[^a-z0-9]", "", suffix)
            parts = [re.sub(r"[^a-z0-9]", "", part) for part in prefix.split(".")]
            distinctive = next((part for part in reversed(parts) if len(part) >= 8), "")
            suffix_visible = compact_suffix in compact_alnum_haystack
            if len(compact_suffix) >= 12:
                suffix_visible = compact_suffix[:8] in compact_alnum_haystack and compact_suffix[-4:] in compact_alnum_haystack
            return bool(suffix_visible and (not distinctive or distinctive in compact_alnum_haystack))
    # Layout-preserving extraction can place an adjacent table column between
    # wrapped prose fragments.  Require every meaningful token in order while
    # allowing only a bounded amount of intervening text.
    tokens = re.findall(r"[a-z0-9]+", normalized)
    if len(tokens) >= 3:
        # TeX may split a long identifier without an explicit hyphen
        # (``ProofDeliv\neryPlan``).  Permit whitespace/hyphenation *inside*
        # an expected token while retaining ordered, bounded token matching.
        # This is deliberately stricter than a bag-of-words check: deleting or
        # reordering a premise/warrant/status still fails validation.
        flexible_tokens = [r"[\s-]*".join(re.escape(char) for char in token) for token in tokens]
        pattern = r".{0,400}?".join(flexible_tokens)
        return re.search(pattern, normalized_haystack) is not None
    return False


def extract_html_packet(path: Path) -> dict[str, Any]:
    content = path.read_text(encoding="utf-8")
    match = re.search(r'<script id="trace-data" type="application/json">(.*?)</script>', content, re.S)
    if not match:
        raise ValueError("HTML has no embedded trace-data packet")
    value = json.loads(match.group(1))
    if not isinstance(value, dict):
        raise ValueError("embedded trace-data is not an object")
    return value


def extract_pdf_text(path: Path) -> str:
    tool = shutil.which("pdftotext")
    if tool is None:
        raise RuntimeError("pdftotext is required for release PDF semantic validation")
    result = subprocess.run(
        [tool, "-layout", str(path), "-"], capture_output=True, text=True, timeout=60, check=False
    )
    if result.returncode:
        raise RuntimeError(f"pdftotext failed ({result.returncode}): {result.stderr[-1000:]}")
    return result.stdout


def validate_pdf_quality(pdf_path: Path, manifest: dict[str, Any]) -> list[PdfTraceIssue]:
    issues: list[PdfTraceIssue] = []
    compiler = manifest.get("compiler", {}) if isinstance(manifest.get("compiler"), dict) else {}
    diagnostics = str(compiler.get("diagnostics", "")) + "\n" + "\n".join(map(str, compiler.get("warnings", [])))
    lower = diagnostics.casefold()
    for marker, code in (
        ("undefined reference", "undefined-reference"), ("undefined citation", "undefined-citation"),
        ("missing character:", "missing-glyph"), ("destination with the same identifier", "duplicate-destination"),
    ):
        if marker in lower:
            issues.append(PdfTraceIssue(code, "$.compiler.diagnostics", marker))
    for match in re.finditer(r"Overfull \\[hv]box \(([-+0-9.]+)pt too (?:wide|high)\)", diagnostics, re.I):
        amount = float(match.group(1))
        if amount > MATERIAL_OVERFULL_PT:
            issues.append(PdfTraceIssue("material-overfull-box", "$.compiler.diagnostics", f"{amount}pt exceeds {MATERIAL_OVERFULL_PT}pt"))
    tool = shutil.which("pdfinfo")
    if tool is None:
        issues.append(PdfTraceIssue("pdfinfo-unavailable", str(pdf_path), "pdfinfo is required for release validation"))
        return issues
    result = subprocess.run([tool, str(pdf_path)], capture_output=True, text=True, timeout=30, check=False)
    if result.returncode:
        issues.append(PdfTraceIssue("pdfinfo-failed", str(pdf_path), result.stderr[-500:]))
        return issues
    page_match = re.search(r"(?m)^Pages:\s*(\d+)\s*$", result.stdout)
    if not page_match or int(page_match.group(1)) < 1:
        issues.append(PdfTraceIssue("invalid-page-count", str(pdf_path), "PDF must contain at least one page"))
    if not re.search(r"(?m)^Title:\s*Public Reasoning Trace\s*$", result.stdout):
        issues.append(PdfTraceIssue("invalid-pdf-title", str(pdf_path), "expected Public Reasoning Trace metadata title"))
    return issues


def _ids(rows: Any, *fields: str) -> set[str]:
    if not isinstance(rows, list):
        return set()
    found: set[str] = set()
    for row in rows:
        if not isinstance(row, dict):
            continue
        for field in fields:
            if row.get(field) not in (None, ""):
                found.add(str(row[field]))
                break
    return found


def packet_semantic_ids(packet: dict[str, Any]) -> dict[str, set[str]]:
    graph = packet.get("graph", {}) if isinstance(packet.get("graph"), dict) else {}
    return {
        "route_steps": _ids(packet.get("declared_route"), "step_id"),
        "inferences": _ids(packet.get("inferences"), "event_id"),
        "claims": _ids(packet.get("claims"), "claim_id"),
        "evidence": _ids(packet.get("evidence"), "evidence_id"),
        "negative_paths": _ids(packet.get("alternatives_and_failures"), "alternative_id", "falsifier_id", "failure_id", "event_id", "id"),
        "gates": _ids(packet.get("decisions_and_gates"), "event_id", "gate_id", "decision_id"),
        "obligations": _ids(packet.get("obligations"), "obligation_id"),
        "artifacts": _ids(packet.get("artifacts_and_receipts"), "artifact_id", "receipt_id"),
        "authority": _ids(packet.get("authority_ledger"), "event_id", "authority_id"),
        "handoffs": _ids(packet.get("handoffs"), "event_id", "handoff_id"),
        "graph_nodes": _ids(graph.get("nodes"), "id"),
    }


def _inventory_ids(inventory: dict[str, Any]) -> set[str]:
    raw = inventory.get("semantic_ids", {})
    result: set[str] = set()
    if isinstance(raw, dict):
        for values in raw.values():
            if isinstance(values, list):
                result.update(str(value) for value in values)
            elif isinstance(values, dict):
                result.update(str(value) for value in values.keys())
    return result


def _manifest_values(manifest: dict[str, Any]) -> dict[str, str]:
    result: dict[str, str] = {}

    def walk(value: Any, prefix: str = "") -> None:
        if isinstance(value, dict):
            for key, item in value.items():
                walk(item, f"{prefix}.{key}" if prefix else str(key))
        elif isinstance(value, (str, int, float, bool)):
            result[prefix] = str(value)

    walk(manifest)
    return result


def _digest_matches(values: dict[str, str], aliases: Iterable[str], expected: str) -> bool:
    aliases = tuple(alias.casefold() for alias in aliases)
    candidates = [value.removeprefix("sha256:").casefold() for key, value in values.items() if any(alias in key.casefold() for alias in aliases) and ("digest" in key.casefold() or "sha256" in key.casefold())]
    return expected.casefold() in candidates


def _required_pdf_strings(packet: dict[str, Any]) -> list[tuple[str, str]]:
    required: list[tuple[str, str]] = []

    def add_leaves(location: str, value: Any) -> None:
        """Add every public semantic leaf, without treating container syntax as meaning."""
        if isinstance(value, dict):
            for key, child in value.items():
                add_leaves(f"{location}.{key}", child)
        elif isinstance(value, list):
            for index, child in enumerate(value):
                add_leaves(f"{location}[{index}]", child)
        elif value not in (None, ""):
            required.append((location, str(value)))

    identity = packet.get("identity", {})
    lens = packet.get("lens", {})
    for field in ("trace_id", "run_id", "workflow_id", "profile_id"):
        if isinstance(identity, dict) and identity.get(field):
            required.append((f"identity.{field}", str(identity[field])))
    if isinstance(lens, dict) and lens.get("focus_question"):
        required.append(("lens.focus_question", str(lens["focus_question"])))
    for index, step in enumerate(packet.get("declared_route", [])):
        if not isinstance(step, dict):
            continue
        # Route identity, mode, observability state, and contract I/O must be
        # inspectable; a route table containing only step names is not enough.
        for field in ("step_id", "skill", "mode", "status", "observability_gap", "consumes", "produces"):
            add_leaves(f"declared_route[{index}].{field}", step.get(field))
    for index, inference in enumerate(packet.get("inferences", [])):
        if not isinstance(inference, dict):
            continue
        # These are the expert validation dossier, not optional decoration.
        # Requiring each leaf closes a former gap where an ID and conclusion
        # could pass even if premises, warrant, scope, or status disappeared.
        for field in (
            "event_id", "step_id", "skill", "question", "premises", "operator",
            "warrant", "conclusion", "uncertainty", "assumptions", "scope",
            "parent_event_ids", "artifact_validation_status",
            "claim_epistemic_status", "workflow_disposition", "authority",
            "handoff",
        ):
            add_leaves(f"inferences[{index}].{field}", inference.get(field))
    for lane, visible_fields in (
        ("evidence", ("evidence_id", "event_id", "relation", "artifact_type", "digest", "path")),
        ("obligations", ("obligation_id", "event_id", "requirement", "status")),
        ("handoffs", ("event_id", "handoff_id", "destination_workflow_id", "target_workflow", "workflow", "disposition", "accepted")),
        ("alternatives_and_failures", ("alternative_id", "falsifier_id", "failure_id", "event_id", "kind", "candidate", "description", "disposition")),
        ("authority_ledger", ("event_id", "authority_id", "step_id", "exercised", "absent", "prohibitions", "prohibitions_checked")),
    ):
        for index, row in enumerate(packet.get(lane, [])):
            if not isinstance(row, dict):
                continue
            for field in visible_fields:
                value = row.get(field)
                if field == "candidate" and isinstance(value, str) and ":" in value:
                    # The first long artifact identifier occupies a narrow
                    # table column and can be interleaved with adjacent-column
                    # text by pdftotext.  Validate its identifier and the
                    # substantive rejection text independently.
                    prefix, rationale = value.split(":", 1)
                    tokens = prefix.split()
                    if tokens:
                        add_leaves(f"{lane}[{index}].candidate_target", tokens[-1])
                    add_leaves(f"{lane}[{index}].candidate_rationale", rationale.strip())
                else:
                    add_leaves(f"{lane}[{index}].{field}", value)

    graph = packet.get("graph", {}) if isinstance(packet.get("graph"), dict) else {}
    for index, node in enumerate(graph.get("nodes", [])):
        if isinstance(node, dict):
            for field in ("id", "type", "label", "status"):
                add_leaves(f"graph.nodes[{index}].{field}", node.get(field))
    for index, edge in enumerate(graph.get("edges", [])):
        if not isinstance(edge, dict):
            continue
        # The digest-bound inventory proves tuple membership.  PDF extraction
        # from a multi-column longtable does not preserve row order reliably,
        # so visibility is checked per tuple component here rather than by a
        # false-failing concatenated row sentinel.
        source, relation, target = edge.get("source"), edge.get("type"), edge.get("target")
        add_leaves(f"graph.edges[{index}].source", source)
        add_leaves(f"graph.edges[{index}].type", relation)
        add_leaves(f"graph.edges[{index}].target", target)
        add_leaves(f"graph.edges[{index}].adapter", edge.get("adapter"))
    return required


def validate_companions(
    packet: dict[str, Any], html_path: Path, inventory: dict[str, Any], tex_path: Path,
    pdf_path: Path, manifest: dict[str, Any], *, pdf_text: str | None = None,
) -> list[PdfTraceIssue]:
    issues: list[PdfTraceIssue] = []
    try:
        embedded = extract_html_packet(html_path)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        issues.append(PdfTraceIssue("invalid-html-companion", str(html_path), str(exc)))
    else:
        if embedded != packet:
            issues.append(PdfTraceIssue("packet-html-identity-mismatch", str(html_path), "embedded packet differs from source packet"))

    expected_ids = packet_semantic_ids(packet)
    flattened_expected = set().union(*expected_ids.values())
    missing_inventory = sorted(flattened_expected - _inventory_ids(inventory))
    if missing_inventory:
        issues.append(PdfTraceIssue("inventory-semantic-omission", "$.semantic_ids", ", ".join(missing_inventory[:20])))

    values = _manifest_values(manifest)
    packet_digest = sha256_bytes(canonical_bytes(packet))
    inventory_digest = sha256_bytes(canonical_bytes(inventory))
    tex_bytes = tex_path.read_bytes()
    tex_digest = sha256_bytes(tex_bytes)
    pdf_bytes = pdf_path.read_bytes() if pdf_path.is_file() else b""
    pdf_digest = sha256_bytes(pdf_bytes)
    for aliases, expected, name in (
        (("packet",), packet_digest, "packet"), (("inventory",), inventory_digest, "inventory"),
        (("tex", "latex"), tex_digest, "TeX"), (("pdf",), pdf_digest, "PDF"),
    ):
        if not _digest_matches(values, aliases, expected):
            issues.append(PdfTraceIssue("manifest-digest-mismatch", "$.manifest", f"missing current {name} SHA-256"))
    identity = packet.get("identity", {})
    for field in ("trace_id", "run_id", "workflow_id", "profile_id"):
        expected = str(identity.get(field, "")) if isinstance(identity, dict) else ""
        if expected and expected not in [value for key, value in values.items() if key.endswith(field)]:
            issues.append(PdfTraceIssue("manifest-identity-mismatch", f"$.identity.{field}", expected))
    for error in validate_manifest_bindings(
        manifest, packet, inventory, select_print_lens(packet),
        tex_path, pdf_path, template_paths=TEMPLATE_PATHS,
    ):
        issues.append(PdfTraceIssue("manifest-binding-error", "$.manifest", error))

    if not pdf_bytes.startswith(b"%PDF-"):
        issues.append(PdfTraceIssue("invalid-pdf", str(pdf_path), "missing PDF header"))
        return issues
    issues.extend(validate_pdf_quality(pdf_path, manifest))
    if pdf_text is None:
        try:
            pdf_text = extract_pdf_text(pdf_path)
        except (OSError, RuntimeError, subprocess.SubprocessError) as exc:
            issues.append(PdfTraceIssue("pdf-text-extraction-failed", str(pdf_path), str(exc)))
            return issues
    normalized_pdf = _norm(pdf_text)
    if "public rationale" not in normalized_pdf or "chain-of-thought" not in normalized_pdf:
        issues.append(PdfTraceIssue("missing-public-rationale-notice", str(pdf_path), "public-rationale/no-chain-of-thought notice is absent"))
    for location, sentinel in _required_pdf_strings(packet):
        normalized = _norm(sentinel)
        if normalized and not semantic_visible(sentinel, pdf_text):
            issues.append(PdfTraceIssue("pdf-semantic-omission", location, sentinel[:160]))
    return issues


def companion_paths(stem: str, directory: Path = GENERATED) -> dict[str, Path]:
    base = directory / stem
    return {
        "packet": base.with_suffix(".packet.json"), "html": base.with_suffix(".html"),
        "inventory": base.with_suffix(".inventory.json"), "tex": base.with_suffix(".tex"),
        "pdf": base.with_suffix(".pdf"), "manifest": base.with_suffix(".manifest.json"),
    }


def validate_set(paths: dict[str, Path]) -> list[PdfTraceIssue]:
    missing = [f"{kind}={path}" for kind, path in paths.items() if not path.is_file()]
    if missing:
        return [PdfTraceIssue("missing-companion", "$", ", ".join(missing))]
    packet = json.loads(paths["packet"].read_text(encoding="utf-8"))
    inventory = json.loads(paths["inventory"].read_text(encoding="utf-8"))
    manifest = json.loads(paths["manifest"].read_text(encoding="utf-8"))
    return validate_companions(packet, paths["html"], inventory, paths["tex"], paths["pdf"], manifest)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--packet", type=Path); parser.add_argument("--html", type=Path)
    parser.add_argument("--inventory", type=Path); parser.add_argument("--tex", type=Path)
    parser.add_argument("--pdf", type=Path); parser.add_argument("--manifest", type=Path)
    args = parser.parse_args()
    supplied = [args.packet, args.html, args.inventory, args.tex, args.pdf, args.manifest]
    sets: list[dict[str, Path]]
    if any(supplied):
        if not all(supplied):
            parser.error("focused validation requires all six companion paths")
        sets = [{k: getattr(args, k) for k in ("packet", "html", "inventory", "tex", "pdf", "manifest")}]
    else:
        observed = {path.name.removesuffix(".packet.json") for path in GENERATED.glob("*.packet.json")}
        if observed != EXPECTED_STEMS:
            print(f"fixture stem mismatch: expected={sorted(EXPECTED_STEMS)} observed={sorted(observed)}")
            return 1
        sets = [companion_paths(stem) for stem in sorted(EXPECTED_STEMS)]
    issues: list[PdfTraceIssue] = []
    for paths in sets:
        issues.extend(validate_set(paths))
    for issue in issues:
        print(issue.render())
    if issues:
        print(f"reasoning-trace PDF validation failed: {len(issues)} issue(s)")
        return 1
    print(f"reasoning-trace PDF validation passed: {len(sets)} companion set(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
