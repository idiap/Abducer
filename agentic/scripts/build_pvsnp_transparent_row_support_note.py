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
"""Build a focused P vs NP TransparentRowSupport_N theorem-pair note."""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path
from typing import Any

from agentic_common import ROOT, clean_text, load_json_object, rel, stable_id, utc_now, write_json


PACKET_JSON = ROOT / "agentic/reports/results_ellaboration/p-vs-np-transfer-obstruction-certificate/latest.json"
OUT_DIR = ROOT / "agentic/reports/results_ellaboration/p-vs-np-transfer-obstruction-certificate"
OUT_JSON = OUT_DIR / "transparent_row_support_note.json"
OUT_MD = OUT_DIR / "transparent_row_support_note.md"
OUT_TEX = OUT_DIR / "transparent_row_support_note.tex"
OUT_PDF = OUT_DIR / "transparent_row_support_note.pdf"


def tex_escape(text: Any) -> str:
    value = clean_text(text)
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
    return "".join(replacements.get(ch, ch) for ch in value)


def md_items(items: list[str]) -> str:
    return "\n".join(f"- {clean_text(item)}" for item in items)


def tex_items(items: list[str]) -> str:
    body = "\n".join(f"\\item {tex_escape(item)}" for item in items)
    return "\\begin{itemize}\n" + body + "\n\\end{itemize}"


def build_note(packet: dict[str, Any]) -> dict[str, Any]:
    support = packet["transparent_row_support_packet"]
    positive = support["generic_positive_theorem"]
    countermodel = support["generic_countermodel_theorem"]
    readiness = packet["readiness_gate"]
    return {
        "version": 1,
        "generated_utc": utc_now(),
        "note_id": stable_id("pvsnp-transparent-row-support-note", packet.get("packet_id", "")),
        "target_id": packet["target_id"],
        "paper_project_id": packet["paper_project_id"],
        "status": "transparent_row_support_note_ready",
        "epistemic_status": "paper_scaffold_not_main_theorem",
        "title": "Transparent Row Support for FormulaEval: A Parser/Falsifier Boundary",
        "abstract_claim": (
            "This note consolidates the recent P vs NP discovery cycles into a scoped theorem pair. "
            "Transparent FormulaEval row support extends the Gamma parser ledger and yields an upper-bound falsifier; "
            "hidden semantic support is blocked by a private-row or unread-enable-bit countermodel."
        ),
        "non_claims": [
            "This does not prove P != NP.",
            "This does not prove SAT outside P/poly.",
            "This is a proof-system transfer obstruction and parser/falsifier boundary.",
        ],
        "definition_fields": support["definition_fields"],
        "positive_theorem": positive,
        "countermodel_theorem": countermodel,
        "examples_subsumed": positive["examples_subsumed"],
        "open_problems": [
            "RealSATInfluenceRealizer_N: force semantic FormulaEval influence into visible charged support.",
            "AC0PrefixNonemptiness_N or an equivalent output-sensitive enumeration theorem for AC0 selectors.",
            "Prior-art comparison against hardness magnification, MCSP/MKtP, natural proofs, relativization, and algebrization.",
        ],
        "stop_rule": support["stop_rule"],
        "next_paper_action": readiness["next_action"],
        "source_packet": rel(PACKET_JSON),
        "source_cycles": support["evidence_cycles"],
    }


def render_markdown(note: dict[str, Any]) -> str:
    fields = note["definition_fields"]
    positive = note["positive_theorem"]
    countermodel = note["countermodel_theorem"]
    lines = [
        f"# {note['title']}",
        "",
        f"- Status: `{note['status']}`",
        f"- Epistemic status: `{note['epistemic_status']}`",
        f"- Source packet: `{note['source_packet']}`",
        "",
        "## Abstract Claim",
        "",
        note["abstract_claim"],
        "",
        "## Non-Claims",
        "",
        md_items(note["non_claims"]),
        "",
        "## Definition: TransparentRowSupport_N",
        "",
        *[f"- **{key}**: {value}" for key, value in fields.items()],
        "",
        "## Theorem A: Transparent Support Gives A Gamma Falsifier",
        "",
        positive["statement"],
        "",
        "### Proof Spine",
        "",
        md_items(positive["proof_spine"]),
        "",
        "## Theorem B: Hidden Support Gives A Private-Row Countermodel",
        "",
        countermodel["statement"],
        "",
        "### Countermodel Spine",
        "",
        md_items(countermodel["countermodel_spine"]),
        "",
        "## Examples Subsumed",
        "",
        md_items(note["examples_subsumed"]),
        "",
        "## Open Problems",
        "",
        md_items(note["open_problems"]),
        "",
        "## Stop Rule",
        "",
        note["stop_rule"],
        "",
        "## Next Paper Action",
        "",
        note["next_paper_action"],
        "",
    ]
    return "\n".join(lines)


def render_tex(note: dict[str, Any]) -> str:
    fields = note["definition_fields"]
    positive = note["positive_theorem"]
    countermodel = note["countermodel_theorem"]
    definition_items = [f"{key}: {value}" for key, value in fields.items()]
    return rf"""\documentclass[11pt]{{article}}
\usepackage[margin=1in]{{geometry}}
\usepackage{{amsmath,amssymb,amsthm}}
\newtheorem{{theorem}}{{Theorem}}
\newtheorem{{definition}}{{Definition}}
\title{{{tex_escape(note['title'])}}}
\author{{ABducer P vs NP Result Elaboration}}
\date{{{tex_escape(note['generated_utc'])}}}
\begin{{document}}
\maketitle
\begin{{abstract}}
{tex_escape(note['abstract_claim'])}
\end{{abstract}}

\section{{Non-Claims}}
{tex_items(note['non_claims'])}

\section{{Definition}}
\begin{{definition}}[TransparentRowSupport\_N]
A FormulaEval mechanism satisfies TransparentRowSupport\_N when it satisfies the following interface conditions.
{tex_items(definition_items)}
\end{{definition}}

\section{{Transparent-Support Theorem}}
\begin{{theorem}}[Transparent support gives a Gamma falsifier]
{tex_escape(positive['statement'])}
\end{{theorem}}
\paragraph{{Proof spine.}}
{tex_items(positive['proof_spine'])}

\section{{Hidden-Support Countermodel}}
\begin{{theorem}}[Hidden support gives a private-row countermodel]
{tex_escape(countermodel['statement'])}
\end{{theorem}}
\paragraph{{Countermodel spine.}}
{tex_items(countermodel['countermodel_spine'])}

\section{{Examples Subsumed}}
{tex_items(note['examples_subsumed'])}

\section{{Open Problems}}
{tex_items(note['open_problems'])}

\section{{Stop Rule And Next Action}}
{tex_escape(note['stop_rule'])}

\medskip
\noindent\textbf{{Next paper action.}} {tex_escape(note['next_paper_action'])}
\end{{document}}
"""


def compile_pdf() -> str:
    engine = shutil.which("pdflatex")
    if not engine:
        return ""
    subprocess.run(
        [engine, "-interaction=nonstopmode", "-halt-on-error", OUT_TEX.name],
        cwd=OUT_DIR,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        check=True,
    )
    return rel(OUT_PDF) if OUT_PDF.exists() else ""


def main() -> int:
    packet = load_json_object(PACKET_JSON)
    note = build_note(packet)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    OUT_MD.write_text(render_markdown(note), encoding="utf-8")
    OUT_TEX.write_text(render_tex(note), encoding="utf-8")
    pdf = compile_pdf()
    note["artifacts"] = {
        "json": rel(OUT_JSON),
        "markdown": rel(OUT_MD),
        "tex": rel(OUT_TEX),
        "pdf": pdf,
    }
    write_json(OUT_JSON, note)
    print(f"Wrote {rel(OUT_JSON)}")
    print(f"Wrote {rel(OUT_MD)}")
    print(f"Wrote {rel(OUT_TEX)}")
    if pdf:
        print(f"Wrote {pdf}")
    else:
        print("PDF not built: pdflatex not available")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
