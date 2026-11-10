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
"""Render deterministic expert LaTeX from a public reasoning monitor packet."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import tempfile
from pathlib import Path
from typing import Any, Iterable

try:
    from reasoning_trace_print_model import (
        build_print_inventory, canonical_json_bytes, section, select_print_lens,
    )
    from reasoning_trace_tex_safety import format_value, tex_escape
except ImportError:  # pragma: no cover - package import path
    from agentic.scripts.reasoning_trace_print_model import (
        build_print_inventory, canonical_json_bytes, section, select_print_lens,
    )
    from agentic.scripts.reasoning_trace_tex_safety import format_value, tex_escape


RENDERER_VERSION = "1.0"
SUBSTANTIVE_FAMILIES = {"inference", "claim", "transformation", "validation", "alternative", "falsifier", "obligation"}
EDGE_TYPES = ("precedes", "contains", "supports", "refutes", "constrains", "produces", "branches", "joins", "refines", "validates", "blocks", "hands_off", "background")

PREAMBLE = r"""\documentclass[10pt,a4paper]{article}
\usepackage[margin=20mm]{geometry}
\usepackage{iftex}
\ifPDFTeX\usepackage[T1]{fontenc}\usepackage[utf8]{inputenc}\else\usepackage{fontspec}\fi
\usepackage{xcolor,longtable,array,booktabs,hyperref,fancyhdr}
\hypersetup{unicode=true,pdftitle={Public Reasoning Trace},colorlinks=true,linkcolor=blue}
\setlength{\parindent}{0pt}\setlength{\parskip}{4pt}\setlength{\emergencystretch}{3em}
\raggedbottom\sloppy
\setcounter{tocdepth}{2}
\pagestyle{fancy}\fancyhf{}\lhead{Public Reasoning Trace}\rhead{Expert validation copy}\cfoot{\thepage}
\newcommand{\TraceText}[1]{#1}
\newcommand{\TraceStatus}[2]{\textbf{#1:} #2\quad}
\newcommand{\TraceField}[2]{\par\noindent\textbf{#1}\par\noindent #2\par\smallskip}
\newenvironment{TraceDossier}{\par\medskip\noindent\hrule\medskip}{\medskip\hrule\par\medskip}
\newcommand{\TraceEdge}[3]{#1 & \textbf{#2} & #3\\}
\newcommand{\TraceRouteState}[2]{\textbf{#1} (#2)}
\begin{document}
"""

POSTAMBLE = "\\end{document}\n"


def _label(kind: str, semantic_id: str) -> str:
    digest = hashlib.sha256(f"{kind}:{semantic_id}".encode("utf-8")).hexdigest()[:18]
    return f"trace-{kind}-{digest}"


def _target(kind: str, semantic_id: str, display: Any | None = None) -> str:
    shown = semantic_id if display is None else display
    return rf"\hypertarget{{{_label(kind, semantic_id)}}}{{{format_value(shown)}}}"


def _link(kind: str, semantic_id: str) -> str:
    return rf"\hyperlink{{{_label(kind, semantic_id)}}}{{{format_value(semantic_id)}}}"


def _values(value: Any) -> list[Any]:
    if value is None or value == "":
        return []
    return value if isinstance(value, list) else [value]


def _plain(value: Any, empty: str = "Not recorded") -> str:
    return format_value(value if value not in (None, "", [], {}) else empty)


def _field(label: str, value: Any, empty: str = "Not recorded") -> str:
    return rf"\TraceField{{{tex_escape(label)}}}{{{_plain(value, empty)}}}" + "\n"


def _field_tex(label: str, value_tex: str, empty: str = "Not recorded") -> str:
    """Render only renderer-owned TeX; packet values must be escaped upstream."""
    return rf"\TraceField{{{tex_escape(label)}}}{{{value_tex or tex_escape(empty)}}}" + "\n"


def _section_rows(inventory: dict[str, Any], section_id: str) -> list[dict[str, Any]]:
    return [row for row in section(inventory, section_id).get("items", []) if isinstance(row, dict)]


def _longtable(headers: list[str], widths: list[str], rows: Iterable[list[Any]], empty: str) -> str:
    spec = "@{}" + "".join(f">{{\\raggedright\\arraybackslash}}p{{{width}}}" for width in widths) + "@{}"
    head = " & ".join(rf"\textbf{{{tex_escape(h)}}}" for h in headers) + r"\\\midrule"
    body_rows = list(rows)
    if not body_rows:
        body = rf"\multicolumn{{{len(headers)}}}{{l}}{{{tex_escape(empty)}}}\\"
    else:
        body = "\n".join(" & ".join(str(cell) for cell in row) + r"\\" for row in body_rows)
    return rf"""\begingroup\setlength{{\tabcolsep}}{{2pt}}\small
\begin{{longtable}}{{{spec}}}
\toprule
{head}
\endfirsthead
\toprule
{head}
\endhead
{body}
\bottomrule
\end{{longtable}}
\normalsize\endgroup
"""


def _render_cover(packet: dict[str, Any], inventory: dict[str, Any], lens: dict[str, Any]) -> str:
    identity = packet.get("identity", {}) if isinstance(packet.get("identity"), dict) else {}
    rows = "\n".join(_field(str(key).replace("_", " ").title(), value) for key, value in identity.items() if value not in (None, ""))
    return rf"""\hypersetup{{pageanchor=false}}
\begin{{titlepage}}
\centering
{{\LARGE\bfseries {format_value(lens.get('visible_name', 'Public Reasoning Trace'))}\par}}
\vspace{{1em}}
{{\large Expert inference validation report\par}}
\vspace{{2em}}
\begin{{minipage}}{{0.92\linewidth}}
{_field('Focus question', lens.get('focus_question'))}
{rows}
{_field('Canonical packet SHA-256', inventory.get('packet_digest'))}
\end{{minipage}}
\vfill
{{\small Renderer {tex_escape(RENDERER_VERSION)}. Generated from the validated workflow-neutral monitor packet.}}
\end{{titlepage}}
\pagenumbering{{roman}}\tableofcontents\clearpage
\hypersetup{{pageanchor=true}}\pagenumbering{{arabic}}
"""


def _render_contract(inventory: dict[str, Any]) -> str:
    return rf"""\section{{Expert reading contract}}\label{{sec-reading-contract}}
{_field('Public rationale boundary', inventory.get('public_rationale_boundary'))}
This document records inspectable premises, public warrants, evidence, conclusions,
uncertainty, scope, authority, failures, and obligations. It does not expose private
chain-of-thought. Execution authorization, artifact integrity, scientific epistemic
status, and workflow disposition are independent. Chronological precedence does not
mean logical or evidential support.

\subsection{{Status legend}}
\TraceStatus{{Artifact integrity}}{{whether referenced bytes and receipts validate}}
\TraceStatus{{Scientific epistemic status}}{{the bounded support assigned to a claim}}
\TraceStatus{{Workflow disposition}}{{what the workflow did with the item}}
"""


def _render_dashboard(packet: dict[str, Any], lens: dict[str, Any]) -> str:
    coverage = packet.get("coverage", {}) if isinstance(packet.get("coverage"), dict) else {}
    contrasts = lens.get("required_contrasts", [])
    return "\\section{Validation dashboard}\\label{sec-dashboard}\n" + \
        _field("Control coverage", coverage.get("control_coverage")) + \
        _field("Semantic coverage", coverage.get("semantic_coverage")) + \
        _field("Evidence resolution", coverage.get("evidence_resolution")) + \
        _field("Visible trace gaps", coverage.get("trace_gaps")) + \
        _field("Required expert contrasts", contrasts, "No lens-specific contrast declared")


def _render_route(inventory: dict[str, Any], lens: dict[str, Any]) -> str:
    route = _section_rows(inventory, "declared_route")
    rows = []
    for item in route:
        sid = str(item.get("step_id") or item.get("print_semantic_id"))
        state = f"{item.get('mode', 'unknown')} / {item.get('status', 'unknown')}"
        if item.get("observability_gap"):
            state += f"; gap: {item['observability_gap']}"
        rows.append([
            _target("step", sid), _plain(item.get("skill")), _plain(state),
            _plain(item.get("consumes", []), "None"), _plain(item.get("produces", []), "None"),
        ])
    topology = lens.get("topology_mode", "neutral")
    return rf"\section{{Declared route and topology}}\label{{sec-route}}" + "\n" + \
        _field("Route spine", lens.get("spine_label")) + _field("Topology mode", topology) + \
        _longtable(["Step", "Skill", "Mode / observed state", "Consumes", "Produces"], [".13\\linewidth", ".18\\linewidth", ".17\\linewidth", ".18\\linewidth", ".18\\linewidth"], rows, "No declared route was recorded.")


def _event_relations(packet: dict[str, Any], event_id: str) -> dict[str, list[str]]:
    result: dict[str, list[str]] = {}
    mappings = (
        ("evidence", "evidence_id"), ("obligations", "obligation_id"),
        ("artifacts_and_receipts", "artifact_id"), ("alternatives_and_failures", "alternative_id"),
        ("authority_ledger", "event_id"), ("handoffs", "event_id"),
    )
    for lane, id_field in mappings:
        result[lane] = [str(row.get(id_field)) for row in packet.get(lane, []) if isinstance(row, dict) and str(row.get("event_id")) == event_id and row.get(id_field)]
    return result


def _linked_list(kind: str, ids: list[str]) -> str:
    return ", ".join(_link(kind, value) for value in ids) if ids else tex_escape("None recorded")


def _render_inferences(packet: dict[str, Any], inventory: dict[str, Any]) -> str:
    rows = _section_rows(inventory, "inferences")
    output = [r"\section{Expert inference dossiers}\label{sec-inferences}",
              "Each dossier is bound to its semantic event ID. Control-only events appear in the lifecycle appendix and are not scientific claims."]
    if not rows:
        output.append(r"\textit{No substantive inferences were recorded; the trace is visibly incomplete for inference validation.}")
    for number, event in enumerate(rows, 1):
        event_id = str(event.get("event_id") or event.get("print_semantic_id"))
        relations = _event_relations(packet, event_id)
        family = str(event.get("event_family", "unknown"))
        incomplete = bool(event.get("trace_incomplete")) or family not in SUBSTANTIVE_FAMILIES
        output.extend([
            rf"\pagebreak[2]\subsection{{Inference {number}: {format_value(event_id)}}}\label{{{_label('inference', event_id)}}}",
            r"\begin{TraceDossier}",
            _field("Trace disposition", "TRACE INCOMPLETE" if incomplete else "Complete public dossier"),
            _field("Step / skill", f"{event.get('step_id', '')} / {event.get('skill', '')}"),
            _field("Question", event.get("question")),
            _field("Typed premises", event.get("premises"), "No premises recorded — trace incomplete"),
            _field("Transformation / operator", event.get("operator"), "No operator recorded — trace incomplete"),
            _field("Bounded public warrant", event.get("warrant"), "No public warrant recorded — trace incomplete"),
            _field("Conclusion", event.get("conclusion"), "No conclusion recorded — trace incomplete"),
            _field("Uncertainty", event.get("uncertainty")),
            _field("Assumptions", event.get("assumptions"), "None recorded"),
            _field("Scope before / after / model / regime", event.get("scope"), "No scope recorded — trace incomplete"),
            _field("Causal parents", event.get("parent_event_ids"), "None; root event"),
            _field("Artifact integrity status", event.get("artifact_validation_status", "unknown")),
            _field("Scientific epistemic status", event.get("claim_epistemic_status", "unknown")),
            _field("Workflow disposition", event.get("workflow_disposition", "unknown")),
            _field_tex("Evidence links", _linked_list("evidence", relations["evidence"]), "None recorded"),
            _field_tex("Alternative / falsifier / failure links", _linked_list("alternative", relations["alternatives_and_failures"]), "None recorded"),
            _field_tex("Obligation links", _linked_list("obligation", relations["obligations"]), "None recorded"),
            _field_tex("Artifact / receipt links", _linked_list("artifact", relations["artifacts_and_receipts"]), "None recorded"),
            _field("Authority", event.get("authority"), "No authority recorded — trace incomplete"),
            _field("Handoff", event.get("handoff"), "None recorded"),
            r"\end{TraceDossier}",
        ])
    return "\n".join(output) + "\n"


def _render_negative_paths(inventory: dict[str, Any]) -> str:
    items = _section_rows(inventory, "alternatives_and_failures")
    rows = []
    for item in items:
        sid = str(item.get("alternative_id") or item.get("print_semantic_id"))
        description = item.get("description") or item.get("candidate") or item.get("reason") or "Not described"
        rows.append([_target("alternative", sid), _plain(item.get("kind", "alternative")), _plain(item.get("event_id")), _plain(description), _plain(item.get("disposition"))])
    return r"\section{Alternatives, falsifiers, and failed paths}\label{sec-negative-paths}" + "\n" + _longtable(
        ["ID", "Kind", "Inference", "Description", "Disposition"], [".16\\linewidth", ".09\\linewidth", ".15\\linewidth", ".31\\linewidth", ".12\\linewidth"], rows,
        "No alternative, falsifier, or failure was recorded; this is explicit, not silently omitted.")


def _render_body_ledgers(packet: dict[str, Any], inventory: dict[str, Any]) -> str:
    output = [r"\section{Cross-cutting validation ledgers}\label{sec-body-ledgers}"]
    configs = (
        ("scope_ledger", "Scope transitions", "scope"),
        ("authority_ledger", "Authority boundaries", "authority"),
        ("obligations", "Open and discharged obligations", "obligation"),
        ("handoffs", "Handoffs", "handoff"),
    )
    for lane, title, kind in configs:
        items = _section_rows(inventory, lane)
        rows = []
        for item in items:
            sid = str(item.get({"scope_ledger":"event_id", "authority_ledger":"event_id", "obligations":"obligation_id", "handoffs":"event_id"}[lane]) or item.get("print_semantic_id"))
            detail = {k: v for k, v in item.items() if k not in {"print_semantic_id"}}
            rows.append([_target(kind, sid), _plain(detail)])
        output.extend([rf"\subsection{{{tex_escape(title)}}}", _longtable(["Semantic ID", "Complete recorded detail"], [".20\\linewidth", ".67\\linewidth"], rows, f"No {title.lower()} recorded.")])
    return "\n".join(output)


def _render_timeline(inventory: dict[str, Any]) -> str:
    items = _section_rows(inventory, "timeline")
    rows = []
    for item in items:
        event_id = str(item.get("event_id") or item.get("print_semantic_id"))
        rows.append([_target("event", event_id), _plain(item.get("sequence")), _plain(item.get("event_family")), _plain(item.get("step_id")), _plain(item.get("workflow_disposition")), _plain(item.get("parent_event_ids"), "None")])
    return r"\section{Complete chronological lifecycle ledger}\label{app-timeline}" + "\n" + \
        "This ledger records execution order. A precedes relation is not evidential support or entailment.\n" + \
        _longtable(["Event ID", "Seq.", "Family", "Step", "Disposition", "Parents"], [".20\\linewidth", ".04\\linewidth", ".09\\linewidth", ".14\\linewidth", ".12\\linewidth", ".21\\linewidth"], rows, "No lifecycle events recorded.")


def _render_generic_ledger(inventory: dict[str, Any], lane: str, title: str, kind: str, id_field: str) -> str:
    items = _section_rows(inventory, lane)
    rows = []
    for item in items:
        sid = str(item.get(id_field) or item.get("print_semantic_id"))
        detail = {key: value for key, value in item.items() if key != "print_semantic_id"}
        rows.append([_target(kind, sid), _plain(detail)])
    return rf"\section{{{tex_escape(title)}}}" + "\n" + _longtable(["Semantic ID", "Complete recorded detail"], [".20\\linewidth", ".67\\linewidth"], rows, f"No {title.lower()} recorded.")


def _render_graph(inventory: dict[str, Any]) -> str:
    items = _section_rows(inventory, "graph")
    nodes = [row for row in items if row.get("graph_kind") == "node"]
    edges = [row for row in items if row.get("graph_kind") == "edge"]
    counts = {edge_type: sum(str(row.get("type")) == edge_type for row in edges) for edge_type in EDGE_TYPES}
    summary = ", ".join(f"{key}: {value}" for key, value in counts.items() if value)
    node_rows = [[_plain(row.get("id")), _plain(row.get("type")), _plain(row.get("label")), _plain(row.get("status"))] for row in nodes]
    edge_rows = [[_plain(row.get("source")), _plain(row.get("type")), _plain(row.get("target")), _plain(row.get("adapter"), "None")] for row in edges]
    return r"\section{Causal and workflow graph ledger}\label{app-graph}" + "\n" + \
        _field("Typed edge summary", summary, "No edges") + \
        "Edge meanings are explicit: precedes is chronology; supports/refutes/constrains are epistemic relations; contains/produces/branches/joins/refines/validates/blocks/hands-off are workflow relations.\n" + \
        r"\subsection{Nodes}" + "\n" + _longtable(["Node", "Type", "Label", "Status"], [".22\\linewidth", ".10\\linewidth", ".38\\linewidth", ".12\\linewidth"], node_rows, "No graph nodes recorded.") + \
        r"\subsection{Complete typed edge table}" + "\n" + _longtable(["Source", "Relation", "Target", "Adapter / detail"], [".24\\linewidth", ".12\\linewidth", ".24\\linewidth", ".20\\linewidth"], edge_rows, "No graph edges recorded.")


def _render_topology(packet: dict[str, Any], inventory: dict[str, Any], lens: dict[str, Any]) -> str:
    topology = packet.get("profile_topology", {}) if isinstance(packet.get("profile_topology"), dict) else {}
    route = _section_rows(inventory, "declared_route")
    specialist_ids = [str(x) for x in topology.get("specialist_step_ids", [])]
    observed_specialists = [str(row.get("step_id")) for row in route if str(row.get("step_id")) in specialist_ids]
    return r"\section{Profile topology and workflow-specific contrasts}\label{sec-profile-topology}" + "\n" + \
        _field("Projection lens", lens.get("lens_id")) + _field("Topology mode", lens.get("topology_mode")) + \
        _field("Required expert contrasts", lens.get("required_contrasts")) + \
        _field("Declared profile topology", topology, "No specialized topology applies") + \
        _field("Observed specialist roles", observed_specialists, "No specialist fan-out applies") + \
        "A specialist fork or join is a workflow relation, not proof that specialist conclusions are mutually consistent. Finite, endpoint, asymptotic, and continuum boundaries remain separate unless an explicit validated inference connects them.\n"


def _render_dispositions(inventory: dict[str, Any]) -> str:
    rows = [[_plain(row.get("packet_field")), _plain(row.get("disposition")), _plain(row.get("destination")), _plain(row.get("reason"))] for row in inventory.get("field_dispositions", [])]
    return r"\section{Projection completeness and omission ledger}\label{app-dispositions}" + "\n" + _longtable(
        ["Packet field", "Disposition", "Destination", "Reason"], [".18\\linewidth", ".18\\linewidth", ".22\\linewidth", ".24\\linewidth"], rows, "No field disposition records found — projection invalid.")


def render_tex(packet: dict[str, Any], inventory: dict[str, Any] | None = None, lens: dict[str, Any] | None = None) -> str:
    """Pure deterministic renderer. It performs no I/O and no compilation."""
    if not isinstance(packet, dict):
        raise TypeError("packet must be an object")
    selected_lens = dict(lens) if lens is not None else select_print_lens(packet)
    model = inventory if inventory is not None else build_print_inventory(packet, selected_lens)
    if model.get("packet_digest") != build_print_inventory(packet, selected_lens).get("packet_digest"):
        raise ValueError("inventory packet digest does not match packet")
    parts = [
        PREAMBLE,
        _render_cover(packet, model, selected_lens),
        _render_contract(model),
        _render_dashboard(packet, selected_lens),
        _render_route(model, selected_lens),
        _render_topology(packet, model, selected_lens),
        _render_inferences(packet, model),
        _render_negative_paths(model),
        _render_body_ledgers(packet, model),
        r"\appendix" + "\n",
        _render_timeline(model),
        _render_generic_ledger(model, "claims", "Claim ledger", "claim", "claim_id"),
        _render_generic_ledger(model, "evidence", "Typed evidence ledger", "evidence", "evidence_id"),
        _render_generic_ledger(model, "decisions_and_gates", "Decision and gate ledger", "gate", "event_id"),
        _render_generic_ledger(model, "artifacts_and_receipts", "Artifact and receipt ledger", "artifact", "artifact_id"),
        _render_generic_ledger(model, "specialized_projections", "Specialized projection ledger", "projection", "projection_id"),
        _render_graph(model),
        _render_dispositions(model),
        r"\section{Build provenance}\label{app-provenance}" + "\n" +
        _field("Source packet lens", packet.get("lens"), "No packet lens recorded") +
        _field("Packet SHA-256", model.get("packet_digest")) +
        _field("Renderer version", RENDERER_VERSION) +
        _field("Print inventory schema", model.get("schema_version")),
        POSTAMBLE,
    ]
    return "".join(parts)


def _atomic_write(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--packet", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path, help="Requested TeX output")
    parser.add_argument("--inventory", type=Path, help="Use a prebuilt inventory")
    parser.add_argument("--inventory-output", type=Path, help="Write deterministic inventory JSON")
    parser.add_argument("--lenses", type=Path, help="Override the declarative print-lens registry")
    args = parser.parse_args()
    packet = json.loads(args.packet.read_text(encoding="utf-8"))
    registry = json.loads(args.lenses.read_text(encoding="utf-8")) if args.lenses else None
    lens = select_print_lens(packet, registry)
    inventory = json.loads(args.inventory.read_text(encoding="utf-8")) if args.inventory else build_print_inventory(packet, lens)
    tex = render_tex(packet, inventory, lens)
    _atomic_write(args.output, tex.encode("utf-8"))
    if args.inventory_output:
        _atomic_write(args.inventory_output, canonical_json_bytes(inventory))
    print(json.dumps({"output": str(args.output), "inventory": str(args.inventory_output or args.inventory or ""), "packet_digest": inventory["packet_digest"], "bytes": len(tex.encode("utf-8"))}, sort_keys=True))


if __name__ == "__main__":
    main()
