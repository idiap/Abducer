"""Portable JSON, LaTeX, Lean, and MMT candidate exports."""

from __future__ import annotations

import json
from typing import Any

from tdr.validation.service import _lean_skeleton, _mmt_skeleton


def _tex(text: Any) -> str:
    replacements = {
        "\\": r"\textbackslash{}", "&": r"\&", "%": r"\%", "$": r"\$",
        "#": r"\#", "_": r"\_", "{": r"\{", "}": r"\}",
        "~": r"\textasciitilde{}", "^": r"\textasciicircum{}",
    }
    return "".join(replacements.get(char, char) for char in str(text))


def export_candidate(candidate: dict[str, Any], output_format: str) -> str:
    output_format = output_format.lower()
    if output_format == "json":
        return json.dumps(candidate, indent=2, sort_keys=True, ensure_ascii=False)
    if output_format == "lean":
        return _lean_skeleton(candidate)
    if output_format == "mmt":
        return _mmt_skeleton(candidate)
    if output_format == "latex":
        lines = [
            r"\documentclass{article}",
            r"\usepackage[T1]{fontenc}",
            r"\usepackage{enumitem}",
            r"\begin{document}",
            rf"\section*{{Candidate: {_tex(candidate.get('title', candidate.get('candidate_id', 'Untitled')))}}}",
            rf"\textbf{{Mode:}} {_tex(candidate.get('mode', 'unknown'))}\\",
            rf"\textbf{{Epistemic status:}} {_tex(candidate.get('novelty_status', 'conjectural'))}",
            r"\subsection*{Formal move}",
            _tex(candidate.get("formal_move", "unspecified")),
            r"\subsection*{Consequences}", r"\begin{itemize}",
            *[rf"\item {_tex(item)}" for item in candidate.get("consequences", [])],
            r"\end{itemize}",
            r"\subsection*{Falsifiers}", r"\begin{itemize}",
            *[rf"\item {_tex(item)}" for item in candidate.get("falsifiers", [])],
            r"\end{itemize}",
            r"\end{document}",
        ]
        return "\n".join(lines)
    raise ValueError(f"unsupported export format: {output_format}")
