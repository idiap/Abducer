#!/usr/bin/env python3
# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT

"""Generate a concise LaTeX formalization of the current framework state."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

_COMMON_DIR = Path(__file__).resolve().parents[3] / "common"
if str(_COMMON_DIR) not in sys.path:
    sys.path.insert(0, str(_COMMON_DIR))

from reasoning_log import ReasoningLogger

REPO_ROOT = Path(__file__).resolve().parents[4]
_TABLE_ROW_RE = re.compile(r"^\|(.+)\|$")
_NESTED_BULLETS_RE = re.compile(r"^- (?P<label>[^:\n]+):\n(?P<body>(?:\s+- .+\n)+)", re.M)

DEFAULT_EXAMPLE_REPORT = (
    "artifacts/markov-kakutani-fixed-point-theorem/discovery-simulation/simulation-report.md"
)

PRIMARY_STAGE_ORDER: list[str] = [
    "kb-proof-connector",
    "kb-coherence-evaluator",
    "kb-entrypoint-finder",
    "kb-entrypoint-pathfinder",
    "kb-epistemic-hardness",
    "kb-concept-bridge-planner",
    "kb-gap-abstraction-conjecturer",
    "kb-novel-proof-strategist",
    "kb-proof-sketcher",
    "kb-hypothesis-evaluator",
    "kb-hypothesis-refutation-loop",
    "kb-revision-loop",
    "kb-expert-paper-generator",
]

OPERATOR_SPECS: dict[str, dict[str, str]] = {
    "kb-proof-connector": {
        "operator": r"\mathsf{Connect}",
        "signature": r"\mathcal{K} \rightarrow (A^{\mathrm{conn}}, H_0)",
        "role": "Builds the relational proof graph, ranks intervention points, and seeds the initial proof-hypothesis set.",
    },
    "kb-coherence-evaluator": {
        "operator": r"\mathsf{Coherence}",
        "signature": r"(\mathcal{K}, A^{\mathrm{conn}}, H_0) \rightarrow A^{\mathrm{coh}}",
        "role": "Computes typed coherence, explanatory-power, and global-theory-fit signals over the current web of claims.",
    },
    "kb-entrypoint-finder": {
        "operator": r"\mathsf{Entry}",
        "signature": r"(\mathcal{K}, A^{\mathrm{conn}}, A^{\mathrm{coh}}, H_0) \rightarrow A^{\mathrm{ent}}",
        "role": "Ranks the best conceptual entry points into the current problem state.",
    },
    "kb-entrypoint-pathfinder": {
        "operator": r"\mathsf{Path}",
        "signature": r"(A^{\mathrm{ent}}, A^{\mathrm{conn}}, H_0) \rightarrow A^{\mathrm{path}}",
        "role": "Turns entry points into ordered proof-pathway agendas.",
    },
    "kb-epistemic-hardness": {
        "operator": r"\mathsf{Hardness}",
        "signature": r"(\mathcal{K}, A^{\mathrm{conn}}, A^{\mathrm{ent}}, A^{\mathrm{path}}, H_0) \rightarrow A^{\mathrm{hard}}",
        "role": "Diagnoses why the target problem remains hard in the current conceptual regime.",
    },
    "kb-concept-bridge-planner": {
        "operator": r"\mathsf{Bridge}",
        "signature": r"(A^{\mathrm{conn}}, A^{\mathrm{ent}}, A^{\mathrm{path}}, A^{\mathrm{coh}}, H_0) \rightarrow A^{\mathrm{bridge}}",
        "role": "Prioritizes bridge programs between the most consequential concepts and statements.",
    },
    "kb-gap-abstraction-conjecturer": {
        "operator": r"\mathsf{Conjecture}",
        "signature": r"(A^{\mathrm{conn}}, A^{\mathrm{path}}, A^{\mathrm{bridge}}, A^{\mathrm{hard}}, H_0) \rightarrow A^{\mathrm{conj}}",
        "role": "Conjectures the bridge objects or abstraction families that could close the strongest concept gaps.",
    },
    "kb-novel-proof-strategist": {
        "operator": r"\mathsf{Strategize}",
        "signature": r"(A^{\mathrm{ent}}, A^{\mathrm{path}}, A^{\mathrm{bridge}}, A^{\mathrm{conj}}, A^{\mathrm{coh}}, H_0) \rightarrow A^{\mathrm{strat}}",
        "role": "Designs proof strategies that trade off leverage, novelty, and barrier awareness.",
    },
    "kb-proof-sketcher": {
        "operator": r"\mathsf{Sketch}",
        "signature": r"(A^{\mathrm{conj}}, A^{\mathrm{strat}}, A^{\mathrm{bridge}}, H_0) \rightarrow A^{\mathrm{sketch}}",
        "role": "Turns conjectured bridge objects into structured proof-outline programs with obligations and abort conditions.",
    },
    "kb-hypothesis-evaluator": {
        "operator": r"\mathsf{HypEval}",
        "signature": r"(\mathcal{K}, H_0, A^{\mathrm{conn}}, A^{\mathrm{coh}}) \rightarrow A^{\mathrm{eval}}",
        "role": "Scores each hypothesis as supported, refuted, or inconclusive using structural and coherence evidence.",
    },
    "kb-hypothesis-refutation-loop": {
        "operator": r"\mathsf{HypLoop}",
        "signature": r"(\mathcal{K}, H_0, A^{\mathrm{eval}}, A^{\mathrm{coh}}) \rightarrow A^{\mathrm{loop}}",
        "role": "Iterates unresolved hypotheses and performs round-level belief revision.",
    },
    "kb-revision-loop": {
        "operator": r"\mathsf{Revise}",
        "signature": r"(\mathcal{K}, H_0, A^{\mathrm{loop}}, A^{\mathrm{coh}}) \rightarrow (\mathcal{K}', H')",
        "role": "Repairs the ontology or representation when iterative testing stagnates or damages global coherence.",
    },
    "kb-expert-paper-generator": {
        "operator": r"\mathsf{Paper}",
        "signature": r"(\mathcal{K}, A^{\mathrm{coh}}, A^{\mathrm{path}}, A^{\mathrm{bridge}}, A^{\mathrm{conj}}, A^{\mathrm{strat}}, A^{\mathrm{sketch}}, A^{\mathrm{eval}}, A^{\mathrm{loop}}) \rightarrow A^{\mathrm{paper}}",
        "role": "Produces a paper-style synthesis and an explicit expert-facing prioritization over the strongest hypotheses.",
    },
}

OBSERVABILITY_OPERATORS: list[dict[str, str]] = [
    {
        "operator": r"\mathsf{Interpret}",
        "signature": r"\mathcal{X}_t \rightarrow A^{\mathrm{interp}}",
        "role": "Generates human-readable interpretation and discovery-process reports.",
    },
    {
        "operator": r"\mathsf{ProcessGraph}",
        "signature": r"\Lambda_t \rightarrow A^{\mathrm{proc}}",
        "role": "Builds the typed dynamic process graph from run-scoped reasoning logs.",
    },
    {
        "operator": r"\mathsf{Dynamics}",
        "signature": r"\Lambda_t \rightarrow A^{\mathrm{dyn}}",
        "role": "Summarizes reasoning dynamics, operator counts, and graph-evolution metrics over a run.",
    },
]


def _read_text(path: Path) -> str:
    """
    Relevance: Operates within the framework-documentation synthesis layer.
    Concept: Controlled loading of the canonical framework sources.
    Contribution: Ensures the formalization is derived from the repository's current documented state.
    """

    return path.read_text(encoding="utf-8") if path.exists() else ""


def _extract_bullets_after_marker(text: str, marker: str) -> list[str]:
    """
    Relevance: Operates within the framework-documentation synthesis layer.
    Concept: Lightweight extraction of bullet-defined mode inventories from project documentation.
    Contribution: Keeps the generated formalization aligned with the current documented inference-mode sets.
    """

    lines = text.splitlines()
    collecting = False
    rows: list[str] = []
    for line in lines:
        stripped = line.strip()
        if stripped == marker.strip():
            collecting = True
            continue
        if not collecting:
            continue
        if stripped.startswith("- "):
            rows.append(stripped[2:].strip())
            continue
        if rows and not stripped:
            break
        if rows and not stripped.startswith("- "):
            break
    return rows


def _extract_markdown_table(text: str, section_header: str) -> list[dict[str, str]]:
    """
    Relevance: Operates within the framework-documentation synthesis layer.
    Concept: Deterministic extraction of structured rows from the skill inventory table.
    Contribution: Lets the formalization cite the actual current skill set and outputs rather than a manually duplicated list.
    """

    lines = text.splitlines()
    in_section = False
    table_lines: list[str] = []
    for line in lines:
        stripped = line.rstrip()
        if stripped == section_header:
            in_section = True
            continue
        if not in_section:
            continue
        if stripped.startswith("|"):
            table_lines.append(stripped)
            continue
        if table_lines:
            break
    if len(table_lines) < 3:
        return []
    headers = [cell.strip() for cell in table_lines[0].strip("|").split("|")]
    rows: list[dict[str, str]] = []
    for line in table_lines[2:]:
        match = _TABLE_ROW_RE.match(line)
        if not match:
            continue
        cells = [cell.strip() for cell in match.group(1).split("|")]
        if len(cells) != len(headers):
            continue
        rows.append(dict(zip(headers, cells)))
    return rows


def _inventory_lookup(rows: list[dict[str, str]]) -> dict[str, dict[str, str]]:
    """
    Relevance: Operates within the framework-documentation synthesis layer.
    Concept: Conversion from table rows to keyed skill metadata.
    Contribution: Makes operator rendering stable and order-preserving when the formalization selects only the core stages.
    """

    out: dict[str, dict[str, str]] = {}
    for row in rows:
        skill = row.get("Skill", "").strip().strip("`")
        if skill:
            out[skill] = row
    return out


def _clean_mode_item(value: str) -> str:
    """
    Relevance: Operates within the framework-documentation synthesis layer.
    Concept: Normalization of markdown-derived mode labels into formal symbols.
    Contribution: Prevents markdown quoting and explanatory notes from polluting the formal mode-set notation.
    """

    text = str(value).replace("`", "").strip()
    if " (" in text:
        text = text.split(" (", 1)[0].strip()
    return text


def _clean_output_text(value: str) -> str:
    """
    Relevance: Operates within the framework-documentation synthesis layer.
    Concept: Normalization of skill-output descriptions for TeX rendering.
    Contribution: Keeps artifact codomains readable in the formalization while preserving the documented output names.
    """

    return str(value).replace("`", "").strip()


def _match_bullet_value(text: str, label: str) -> str:
    """
    Relevance: Operates within the framework-documentation synthesis layer.
    Concept: Direct extraction of markdown bullet values from generated reports.
    Contribution: Lets the formalization cite concrete run-level quantities from a selected end-to-end example.
    """

    match = re.search(rf"^- {re.escape(label)}:\s*(.+)$", text, flags=re.M)
    return match.group(1).strip().strip("`") if match else ""


def _match_nested_bullets(text: str, label: str) -> list[str]:
    """
    Relevance: Operates within the framework-documentation synthesis layer.
    Concept: Extraction of nested markdown bullet lists from report sections.
    Contribution: Recovers hidden bridge concepts, removed statements, and discovery sequences for the worked example.
    """

    for match in _NESTED_BULLETS_RE.finditer(text):
        if match.group("label").strip() != label:
            continue
        return [
            line.strip()[2:].strip().strip("`")
            for line in match.group("body").splitlines()
            if line.strip().startswith("- ")
        ]
    return []


def _parse_concept_evolution(path: Path) -> list[dict[str, str]]:
    """
    Relevance: Operates within the framework-documentation synthesis layer.
    Concept: Extraction of theorem-specific conceptual phases from a generated evolution report.
    Contribution: Turns a generic pipeline description into a concrete discovery trajectory over a worked theorem case.
    """

    text = _read_text(path)
    if not text:
        return []
    phases: list[dict[str, str]] = []
    sections = re.split(r"^##\s+", text, flags=re.M)
    for section in sections[1:]:
        lines = section.splitlines()
        title = lines[0].strip()
        if title == "Scope" or title.lower().startswith("active "):
            continue
        summary = ""
        for line in lines[1:]:
            stripped = line.strip()
            if stripped.startswith("- "):
                summary = _clean_output_text(stripped[2:].strip())
                break
        phases.append({"title": title, "summary": summary})
    return phases


def _resolve_example_concept_evolution(report_path: Path, override: Path | None = None) -> Path | None:
    """
    Relevance: Operates within the framework-documentation synthesis layer.
    Concept: Derivation of the example phase-trace path from the selected simulation report.
    Contribution: Keeps the worked example aligned with the best iteration of the actual theorem run.
    """

    if override and override.exists():
        return override
    report_text = _read_text(report_path)
    artifact_root = _match_nested_bullets(report_text, "Artifact root")
    if artifact_root:
        candidate = Path(artifact_root[0]) / "concept-evolution.md"
        if candidate.exists():
            return candidate
    return None


def _slug_to_title(value: str) -> str:
    """
    Relevance: Operates within the framework-documentation synthesis layer.
    Concept: Lightweight conversion from KB slug to human-readable theorem title.
    Contribution: Gives the worked example a readable theorem label without hard-coding a separate title registry.
    """

    return value.replace("-", " ").title()


def _build_worked_example(example_report: Path, example_concept_evolution: Path | None) -> dict[str, Any]:
    """
    Relevance: Operates within the framework-documentation synthesis layer.
    Concept: Assembly of a single end-to-end theorem-discovery witness for the formal note.
    Contribution: Grounds the framework signature in one concrete run instead of an abstract operator table.
    """

    report_text = _read_text(example_report)
    kb_path = _match_bullet_value(report_text, "KB")
    kb_slug = Path(kb_path).name if kb_path else "worked-example.kb.md"
    kb_slug = kb_slug.removesuffix(".kb.md").removesuffix(".md")
    concept_path = _resolve_example_concept_evolution(example_report, example_concept_evolution)
    phases = _parse_concept_evolution(concept_path) if concept_path else []
    return {
        "title": _slug_to_title(kb_slug),
        "kb": kb_path,
        "working_kb": _match_bullet_value(report_text, "Working KB"),
        "target_statement": _match_bullet_value(report_text, "Target statement"),
        "knockout_profile": _match_bullet_value(report_text, "Knockout profile"),
        "iterations_executed": _match_bullet_value(report_text, "Iterations executed"),
        "best_replication_score": _match_bullet_value(report_text, "Best replication score"),
        "best_iteration": _match_bullet_value(report_text, "Iteration"),
        "hidden_bridge_concepts": _match_nested_bullets(report_text, "Hidden bridge concepts"),
        "hidden_bridge_terms": _match_nested_bullets(report_text, "Hidden bridge terms"),
        "removed_statements": _match_nested_bullets(report_text, "Removed statements"),
        "sequence": _match_nested_bullets(report_text, "Sequence"),
        "artifact_root": _match_nested_bullets(report_text, "Artifact root"),
        "report_path": str(example_report.relative_to(REPO_ROOT)) if example_report.is_relative_to(REPO_ROOT) else str(example_report),
        "concept_evolution_path": (
            str(concept_path.relative_to(REPO_ROOT)) if concept_path and concept_path.is_relative_to(REPO_ROOT) else str(concept_path)
        ) if concept_path else "",
        "phases": phases,
    }


def _operator_rows(inventory: dict[str, dict[str, str]]) -> list[dict[str, str]]:
    """
    Relevance: Operates within the framework-documentation synthesis layer.
    Concept: Construction of the formal operator list from documented skills and curated signatures.
    Contribution: Converts the current implementation into a compact algebra of stage operators.
    """

    rows: list[dict[str, str]] = []
    for skill in PRIMARY_STAGE_ORDER:
        spec = OPERATOR_SPECS.get(skill)
        inv = inventory.get(skill)
        if spec is None or inv is None:
            continue
        rows.append(
            {
                "skill": skill,
                "operator": spec["operator"],
                "signature": spec["signature"],
                "role": spec["role"],
                "outputs": _clean_output_text(inv.get("Main Outputs", "")),
            }
        )
    return rows


def _latex_escape(value: str) -> str:
    """
    Relevance: Operates within the framework-documentation synthesis layer.
    Concept: Safe rendering of repository-derived text into TeX.
    Contribution: Prevents generated documentation from failing on markdown, paths, or artifact names with special characters.
    """

    replacements = {
        "\\": r"\textbackslash{}",
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
        "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}",
    }
    out = str(value)
    for src, dst in replacements.items():
        out = out.replace(src, dst)
    return out


def _tt_set(items: list[str]) -> str:
    """
    Relevance: Operates within the framework-documentation synthesis layer.
    Concept: Compact set rendering for mode inventories.
    Contribution: Keeps the formalization mathematically concise while preserving the exact current mode labels.
    """

    return r"\{" + ", ".join(r"\texttt{" + _latex_escape(item) + "}" for item in items) + r"\}"


def _chunked(items: list[str], size: int) -> list[list[str]]:
    """
    Relevance: Operates within the framework-documentation synthesis layer.
    Concept: Deterministic chunking of long symbolic lists for TeX layout.
    Contribution: Prevents mode-set and tuple renderings from collapsing into unreadable single-line equations.
    """

    return [items[idx : idx + size] for idx in range(0, len(items), size)]


def _render_aligned_tt_set(symbol: str, items: list[str], chunk_size: int = 4) -> str:
    """
    Relevance: Operates within the framework-documentation synthesis layer.
    Concept: Multi-line rendering of long mode sets.
    Contribution: Keeps the formal notation legible while preserving exact current mode labels.
    """

    chunks = _chunked(items, chunk_size)
    lines = [r"\[", r"\begin{aligned}"]
    for idx, chunk in enumerate(chunks):
        content = ", ".join(r"\texttt{" + _latex_escape(item) + "}" for item in chunk)
        if idx == 0:
            prefix = symbol + r" &= \{"
        else:
            prefix = r"&\quad "
        suffix = r"\}" if idx == len(chunks) - 1 else ","
        terminal = r"" if idx == len(chunks) - 1 else r"\\"
        lines.append(prefix + content + suffix + terminal)
    lines.extend([r"\end{aligned}", r"\]"])
    return "\n".join(lines)


def _render_aligned_tuple(symbol: str, items: list[str], chunk_size: int = 6) -> str:
    """
    Relevance: Operates within the framework-documentation synthesis layer.
    Concept: Multi-line rendering of long tuple-valued state signatures.
    Contribution: Avoids severe overfull equations in the formal signature section.
    """

    chunks = _chunked(items, chunk_size)
    lines = [r"\[", r"\begin{aligned}"]
    for idx, chunk in enumerate(chunks):
        content = ", ".join(chunk)
        if idx == 0:
            prefix = symbol + r" &= ("
        else:
            prefix = r"&\quad "
        suffix = r")" if idx == len(chunks) - 1 else ","
        terminal = r"" if idx == len(chunks) - 1 else r"\\"
        lines.append(prefix + content + suffix + terminal)
    lines.extend([r"\end{aligned}", r"\]"])
    return "\n".join(lines)


def _render_operator_groups() -> str:
    """
    Relevance: Operates within the framework-documentation synthesis layer.
    Concept: Grouped rendering of the stage algebra by functional role.
    Contribution: Replaces a bulky stage table with a shorter explanation that is easier to read alongside the worked example.
    """

    lines = [
        r"\begin{itemize}[leftmargin=*,itemsep=0.25em]",
        r"\item \textbf{Formation layer}: $\mathsf{Connect}$, $\mathsf{Coherence}$, $\mathsf{Entry}$, and $\mathsf{Path}$ transform a raw KB into a connected, scored, and ordered inferential frontier.",
        r"\item \textbf{Discovery layer}: $\mathsf{Hardness}$, $\mathsf{Bridge}$, and $\mathsf{Conjecture}$ identify the blocking gap and propose the bridge object or abstraction family that would resolve it.",
        r"\item \textbf{Program layer}: $\mathsf{Strategize}$ and $\mathsf{Sketch}$ turn bridge objects into candidate proof programs with obligations, invariants, and abort conditions.",
        r"\item \textbf{Revision layer}: $\mathsf{HypEval}$, $\mathsf{HypLoop}$, $\mathsf{Revise}$, and $\mathsf{Paper}$ evaluate the current bridge set, revise the KB when necessary, and emit the expert-facing synthesis.",
        r"\end{itemize}",
    ]
    return "\n".join(lines)


def _render_example_sequence(sequence: list[str]) -> str:
    """
    Relevance: Operates within the framework-documentation synthesis layer.
    Concept: Ordered rendering of a recovered discovery chain.
    Contribution: Makes the end-to-end example explicit as a sequence of theorem-local inferential commitments.
    """

    lines = [r"\begin{enumerate}[leftmargin=*,itemsep=0.2em]"]
    for item in sequence:
        lines.append(r"\item \texttt{" + _latex_escape(item) + r"}")
    lines.append(r"\end{enumerate}")
    return "\n".join(lines)


def _render_example_phases(phases: list[dict[str, str]]) -> str:
    """
    Relevance: Operates within the framework-documentation synthesis layer.
    Concept: Compact rendering of theorem-local conceptual phases.
    Contribution: Shows how the framework organizes discovery as a progression of conceptual regimes rather than a flat search.
    """

    lines = [r"\begin{itemize}[leftmargin=*,itemsep=0.2em]"]
    for phase in phases:
        summary = f": {phase['summary']}" if phase.get("summary") else ""
        lines.append(
            r"\item \textbf{" + _latex_escape(phase["title"]) + r"}" + _latex_escape(summary)
        )
    lines.append(r"\end{itemize}")
    return "\n".join(lines)


def _render_output_items(rows: list[dict[str, str]]) -> str:
    """
    Relevance: Operates within the framework-documentation synthesis layer.
    Concept: Compact enumeration of the current artifact codomains.
    Contribution: Makes the formalization explicit about which typed outputs constitute the framework state.
    """

    lines = [r"\begin{itemize}[leftmargin=*,itemsep=0.2em]"]
    for row in rows:
        lines.append(
            r"\item {} produces {}.".format(
                f"${row['operator']}$",
                _latex_escape(row["outputs"] or "documented stage outputs"),
            )
        )
    for row in OBSERVABILITY_OPERATORS:
        role = str(row["role"]).strip()
        role = role[:-1] if role.endswith(".") else role
        lines.append(
            r"\item {} supports the generation of {}.".format(
                f"${row['operator']}$",
                _latex_escape(role.lower()),
            )
        )
    lines.append(r"\end{itemize}")
    return "\n".join(lines)


def _render_tex(manifest: dict[str, Any]) -> str:
    """
    Relevance: Operates within the framework-documentation synthesis layer.
    Concept: Final LaTeX realization of the framework as a typed inferential system.
    Contribution: Produces the user-requested succinct formalization artifact in a publication-ready representation.
    """

    operators = manifest["operators"]
    primary_modes = manifest["inference_modes"]["primary"]
    prompt_modes = manifest["inference_modes"]["prompt"]
    intents = manifest["inference_modes"]["orchestrator_intents"]
    source_docs = manifest["metadata"]["sources"]
    example = manifest["worked_example"]
    pipeline = (
        r"\begin{aligned}"
        r"\mathsf{Pipeline} &= \mathsf{Paper} \circ \mathsf{Revise} \circ \mathsf{HypLoop} \circ \mathsf{HypEval} \\"
        r"&\circ \mathsf{Sketch} \circ \mathsf{Strategize} \circ \mathsf{Conjecture} \circ \mathsf{Bridge} \\"
        r"&\circ \mathsf{Hardness} \circ \mathsf{Path} \circ \mathsf{Entry} \circ \mathsf{Coherence} \circ \mathsf{Connect}"
        r"\end{aligned}"
    )
    lines = [
        r"\documentclass[11pt]{article}",
        r"\usepackage[margin=1in]{geometry}",
        r"\usepackage[T1]{fontenc}",
        r"\usepackage[utf8]{inputenc}",
        r"\usepackage{lmodern}",
        r"\usepackage{amsmath,amssymb,amsthm}",
        r"\usepackage{enumitem}",
        r"\usepackage{hyperref}",
        r"\usepackage{xcolor}",
        r"\hypersetup{colorlinks=true,linkcolor=blue!50!black,urlcolor=blue!50!black,pdftitle={Current Abducer Framework State}}",
        r"\title{A Succinct Formalization of the Current Abducer Reasoning Framework}",
        r"\author{Neuro-symbolic AI Group\\Idiap Research Institute}",
        r"\date{March 12, 2026}",
        r"\newtheorem{definition}{Definition}",
        r"\begin{document}",
        r"\maketitle",
        r"\begin{abstract}",
        r"This note formalizes the current implementation state of the Abducer framework as a typed inferential system over mathematical knowledge bases, stage artifacts, and reasoning logs. The formalization is intentionally brief: it records the KB state, the implemented pipeline, the current scoring semantics, and the observability contract, then exemplifies them through one end-to-end theorem-discovery run.",
        r"\end{abstract}",
        r"\section{Framework Signature}",
        r"We model the current framework state by the tuple",
        r"\[",
        r"\mathfrak{F} = (\mathcal{K}, \mathcal{A}, \mathcal{M}, \mathcal{T}, \Lambda),",
        r"\]",
        r"where $\mathcal{K}$ is the current problem KB, $\mathcal{A}$ is the structured artifact state, $\mathcal{M}$ is the set of inference modes, $\mathcal{T}$ is the set of deterministic stage operators, and $\Lambda$ is the reasoning-log trace family.",
        r"\begin{definition}[KB state]",
        r"The current KB state is represented as",
        r"\[",
        r"\mathcal{K} = (S, C, M, B, R, H, O),",
        r"\]",
        r"where $S$ is the statement set, $C$ the concept set, $M$ the method/proof-regime set, $B$ the barrier set, $R$ the typed relation set, $H$ the proof-hypothesis set, and $O$ the current open obligations.",
        r"\end{definition}",
        r"The derived artifact state is represented as",
        _render_aligned_tuple(
            r"\mathcal{A}",
            [
                r"A^{\mathrm{conn}}",
                r"A^{\mathrm{coh}}",
                r"A^{\mathrm{ent}}",
                r"A^{\mathrm{path}}",
                r"A^{\mathrm{hard}}",
                r"A^{\mathrm{bridge}}",
                r"A^{\mathrm{conj}}",
                r"A^{\mathrm{strat}}",
                r"A^{\mathrm{sketch}}",
                r"A^{\mathrm{eval}}",
                r"A^{\mathrm{loop}}",
                r"A^{\mathrm{paper}}",
            ],
        ),
        r"\section{Current Mode Sets}",
        r"The current user-facing primary inference modes are",
        _render_aligned_tt_set(r"\mathcal{M}_{\mathrm{primary}}", primary_modes, chunk_size=4),
        r"The current prompt-driven auxiliary modes are",
        _render_aligned_tt_set(r"\mathcal{M}_{\mathrm{prompt}}", prompt_modes, chunk_size=4),
        r"The current orchestrator intents are",
        _render_aligned_tt_set(r"\mathcal{M}_{\mathrm{orch}}", intents, chunk_size=4),
        r"The composite relation \(\mathsf{Cohere} = \mathsf{Coherence} \circ \mathsf{Connect}\) remains the preferred entry operator for relational plus coherentist formation.",
        r"\section{Pipeline Semantics}",
        r"The implemented end-to-end pipeline can be written as",
        r"\[",
        pipeline,
        r"\]",
        r"with the revision operator closing the loop by returning a revised KB and revised hypothesis state whenever the hypothesis loop stalls or damages global coherence.",
        r"The current run state at step $t$ can therefore be written as",
        r"\[",
        r"\mathcal{X}_t = (\mathcal{K}_t, \mathcal{A}_t, \Lambda_t), \qquad \mathcal{X}_{t+1} = \mathsf{Revise}(\mathcal{X}_t) \ \text{when revision is triggered}.",
        r"\]",
        r"The core operator family is grouped below by function rather than by stage table, since the framework is best understood through its end-to-end execution rather than a flat catalogue of scripts.",
        _render_operator_groups(),
        r"\section{Worked End-to-End Example}",
        r"As a concrete witness of the current framework behavior, we use the masked-bridge discovery simulation for the \textit{" + _latex_escape(example["title"]) + r"}. In this run the working KB hides the central bridge concept while the pipeline attempts to recover a proof-relevant route to the target theorem.",
        r"\[",
        r"\mathcal{K}^{\mathrm{work}}_{\mathrm{ex}} = \mathcal{K}_{\mathrm{ex}} \setminus \{\text{explicit bridge-concept annotations}\},",
        r"\qquad",
        r"\mathsf{Pipeline}(\mathcal{K}^{\mathrm{work}}_{\mathrm{ex}}) \rightsquigarrow (\mathcal{A}^{\star}, H^{\star}, \Lambda^{\star}).",
        r"\]",
        r"The selected example uses target statement \texttt{" + _latex_escape(example["target_statement"]) + r"}, knockout profile \texttt{" + _latex_escape(example["knockout_profile"]) + r"}, executes " + _latex_escape(example["iterations_executed"] or "?") + r" iterations, and reaches best replication score " + _latex_escape(example["best_replication_score"] or "?") + r".",
        r"If the bridge concept is denoted by $b^{\star}$, the hidden bridge family in the current run is",
        r"\[",
        r"b^{\star} \in \{" + ", ".join(r"\texttt{" + _latex_escape(item) + r"}" for item in example["hidden_bridge_concepts"]) + r"\},",
        r"\]",
        r"with hidden bridge terms " + ", ".join(r"\texttt{" + _latex_escape(item) + r"}" for item in example["hidden_bridge_terms"]) + r".",
        r"The recovered discovery chain for the best iteration is:",
        _render_example_sequence(example["sequence"]),
        r"The theorem-local conceptual phases recovered by the framework are:",
        _render_example_phases(example["phases"]),
        r"The example operationally illustrates the full pipeline in four grouped moves:",
        r"\begin{enumerate}[leftmargin=*,itemsep=0.25em]",
        r"\item $\mathsf{Connect}$, $\mathsf{Coherence}$, $\mathsf{Entry}$, and $\mathsf{Path}$ isolate the highest-leverage statements and expose the missing bridge region rather than treating the theorem as a flat statement-retrieval task.",
        r"\item $\mathsf{Hardness}$ and $\mathsf{Bridge}$ localize the inferential bottleneck as the absent bridge object that connects single-map fixed-point extraction to the finite-family lift.",
        r"\item $\mathsf{Conjecture}$, $\mathsf{Strategize}$, and $\mathsf{Sketch}$ turn that missing bridge into explicit bridge-object proposals, strategy families, and proof obligations.",
        r"\item $\mathsf{HypEval}$, $\mathsf{HypLoop}$, and $\mathsf{Revise}$ test whether the proposed bridge improves coherence and reconstructs the target route without reintroducing hidden annotations by hand.",
        r"\end{enumerate}",
        r"This witness is the intended meaning of the framework signature: the system is not merely scoring isolated hypotheses, but reconstructing a concept-mediated route through a KB whose proof-relevant center has been partially removed.",
        r"\section{Selection and Scoring Semantics}",
        r"The framework currently uses stage-specific weighted heuristics rather than a single universal scalar objective. A concise common form is",
        r"\[",
        r"\operatorname{score}(h) = \alpha s(h) + \beta c(h) + \gamma e(h) + \delta \ell(h) + \epsilon n(h) - \rho r(h) - \sigma b(h),",
        r"\]",
        r"where $s(h)$ denotes support, $c(h)$ coherence contribution, $e(h)$ explanatory value, $\ell(h)$ structural leverage, $n(h)$ novelty or fertility, $r(h)$ refutation pressure, and $b(h)$ barrier pressure. The expert-paper stage instantiates an explicit transparent variant of this weighted policy.",
        r"\section{Observability Contract}",
        r"Each scripted operator emits a reasoning-log record of the form",
        r"\[",
        r"\lambda_i = (\mathrm{agent}_i, \mathrm{inputs}_i, \mathrm{outputs}_i, \mathrm{summary}_i), \qquad \Lambda = \{\lambda_1, \ldots, \lambda_n\}.",
        r"\]",
        r"This logging contract makes the reasoning process replayable at both the stage level and the run level.",
        _render_output_items(operators),
        r"\section{Source Basis}",
        r"This formalization was generated from the current repository documentation sources:",
        r"\begin{itemize}[leftmargin=*,itemsep=0.2em]",
    ]
    for path in source_docs:
        lines.append(r"\item \url{" + _latex_escape(path) + r"}")
    if example["report_path"]:
        lines.append(r"\item \url{" + _latex_escape(example["report_path"]) + r"}")
    if example["concept_evolution_path"]:
        lines.append(r"\item \url{" + _latex_escape(example["concept_evolution_path"]) + r"}")
    lines.extend([
        r"\end{itemize}",
        r"\end{document}",
    ])
    return "\n".join(lines) + "\n"


def _build_manifest(
    readme: Path,
    architecture: Path,
    orchestration: Path,
    skills_doc: Path,
    output_tex: Path,
    example_report: Path,
    example_concept_evolution: Path | None,
) -> dict[str, Any]:
    """
    Relevance: Operates within the framework-documentation synthesis layer.
    Concept: Assembly of the current formalization manifest from the canonical documentation set.
    Contribution: Provides a machine-readable representation of the framework state that exactly matches the generated LaTeX artifact.
    """

    readme_text = _read_text(readme)
    skills_text = _read_text(skills_doc)
    inventory_rows = _extract_markdown_table(skills_text, "## Skill Inventory")
    inventory = _inventory_lookup(inventory_rows)
    primary_modes = _extract_bullets_after_marker(
        readme_text,
        "Build one-file mathematical knowledge bases in `KB/`, then reason over them with distinct inference modes:",
    )
    prompt_modes = _extract_bullets_after_marker(
        skills_text,
        "These skills are designed for direct LLM execution from `SKILL.md` + prompt template:",
    )
    orchestrator_intents = _extract_bullets_after_marker(
        skills_text,
        "Supported in `kb-orchestrator/scripts/run_orchestrator.py`:",
    )
    operators = _operator_rows(inventory)
    worked_example = _build_worked_example(example_report, example_concept_evolution)
    return {
        "metadata": {
            "generated_from_repo": str(REPO_ROOT),
            "sources": [
                str(readme.relative_to(REPO_ROOT)),
                str(architecture.relative_to(REPO_ROOT)),
                str(orchestration.relative_to(REPO_ROOT)),
                str(skills_doc.relative_to(REPO_ROOT)),
            ],
            "skill_count": len(inventory_rows),
            "core_operator_count": len(operators),
            "output_tex": str(output_tex.relative_to(REPO_ROOT)) if output_tex.is_relative_to(REPO_ROOT) else str(output_tex),
        },
        "framework_signature": {
            "kb_state": ["S", "C", "M", "B", "R", "H", "O"],
            "artifact_state": [
                "A^conn",
                "A^coh",
                "A^ent",
                "A^path",
                "A^hard",
                "A^bridge",
                "A^conj",
                "A^strat",
                "A^sketch",
                "A^eval",
                "A^loop",
                "A^paper",
            ],
            "log_state": "Lambda",
        },
        "inference_modes": {
            "primary": [_clean_mode_item(item) for item in primary_modes],
            "prompt": [_clean_mode_item(item) for item in prompt_modes],
            "orchestrator_intents": [_clean_mode_item(item) for item in orchestrator_intents],
        },
        "operators": operators,
        "worked_example": worked_example,
    }


def main() -> int:
    """
    Relevance: Operates within the framework-documentation synthesis layer.
    Concept: CLI entrypoint for framework-state formalization.
    Contribution: Materializes the requested concise LaTeX formalization as a reproducible skill execution with logged provenance.
    """

    logger = ReasoningLogger("kb-framework-state-formalizer")
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--readme", default="README.md")
    ap.add_argument("--architecture", default="docs/architecture/architecture.md")
    ap.add_argument("--orchestration", default="docs/architecture/orchestration.md")
    ap.add_argument("--skills-doc", default="docs/reference/skills.md")
    ap.add_argument("--output-json", default="artifacts/framework/framework-state-formalization.json")
    ap.add_argument("--output-tex", default="docs/publications/framework-state-formalization.tex")
    ap.add_argument("--example-report", default=DEFAULT_EXAMPLE_REPORT)
    ap.add_argument("--example-concept-evolution", default="")
    args = ap.parse_args()

    readme = (REPO_ROOT / args.readme).resolve() if not Path(args.readme).is_absolute() else Path(args.readme)
    architecture = (REPO_ROOT / args.architecture).resolve() if not Path(args.architecture).is_absolute() else Path(args.architecture)
    orchestration = (REPO_ROOT / args.orchestration).resolve() if not Path(args.orchestration).is_absolute() else Path(args.orchestration)
    skills_doc = (REPO_ROOT / args.skills_doc).resolve() if not Path(args.skills_doc).is_absolute() else Path(args.skills_doc)
    output_json = (REPO_ROOT / args.output_json).resolve() if not Path(args.output_json).is_absolute() else Path(args.output_json)
    output_tex = (REPO_ROOT / args.output_tex).resolve() if not Path(args.output_tex).is_absolute() else Path(args.output_tex)
    example_report = (REPO_ROOT / args.example_report).resolve() if not Path(args.example_report).is_absolute() else Path(args.example_report)
    example_concept_evolution = (
        (REPO_ROOT / args.example_concept_evolution).resolve()
        if args.example_concept_evolution and not Path(args.example_concept_evolution).is_absolute()
        else Path(args.example_concept_evolution).resolve() if args.example_concept_evolution else None
    )

    manifest = _build_manifest(
        readme,
        architecture,
        orchestration,
        skills_doc,
        output_tex,
        example_report,
        example_concept_evolution,
    )
    tex_source = _render_tex(manifest)
    manifest["latex_path"] = str(output_tex.relative_to(REPO_ROOT)) if output_tex.is_relative_to(REPO_ROOT) else str(output_tex)
    manifest["latex_source"] = tex_source

    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_tex.parent.mkdir(parents=True, exist_ok=True)
    output_json.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    output_tex.write_text(tex_source, encoding="utf-8")

    logger.step(
        "Generated framework-state formalization",
        "\n".join(
            [
                f"sources={manifest['metadata']['sources']}",
                f"skill_count={manifest['metadata']['skill_count']}",
                f"core_operator_count={manifest['metadata']['core_operator_count']}",
                f"worked_example={manifest['worked_example']['report_path']}",
            ]
        ),
    )
    logger.add_output("framework_state_formalization_json", output_json)
    logger.add_output("framework_state_formalization_tex", output_tex)
    log_path = logger.finalize("ok", summary=f"Generated framework-state formalization at {output_tex.name}.")
    print(f"[OK] Wrote framework formalization JSON: {output_json}")
    print(f"[OK] Wrote framework formalization TeX: {output_tex}")
    print(f"[LOG] {log_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
