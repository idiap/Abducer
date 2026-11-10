# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Utilities for normalizing theorem text and extracting theorem-body-grounded claim foci."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

import yaml


YAML_BLOCK_RE = re.compile(r"```yaml\n(.*?)\n```", re.DOTALL)
_COMMAND_WITH_ARG_RE = re.compile(
    r"\\(?:text|emph|mathrm|mathsf|mathbf|operatorname|mathcal|mathbb|underline|overline)\{([^{}]*)\}"
)
_INLINE_MACRO_RE = re.compile(r"\\([A-Za-z]+)")
_SUBJECT_IS_RE = re.compile(r"^[A-Za-z][A-Za-z0-9_]*\s+is\s+", re.IGNORECASE)
_SUBJECT_ARE_RE = re.compile(r"^[A-Za-z][A-Za-z0-9_]*\s+are\s+", re.IGNORECASE)
_DISPLAY_BRACKET_RE = re.compile(r"(^|\s)[\[\]](?=\s|$)")

MOJIBAKE_REPLACEMENTS = {
    "Ã¢â‚¬Å“": '"',
    "Ã¢â‚¬Â": '"',
    "Ã¢â‚¬Ëœ": "'",
    "Ã¢â‚¬â„¢": "'",
    "Ã¢â‚¬â€œ": "-",
    "Ã¢â‚¬â€": "-",
    "Ã¢â€ â€™": "->",
    "Ã¢â€°Â¥": ">=",
    "Ã¢â€°Â¤": "<=",
    "Â": "",
    "“": '"',
    "”": '"',
    "’": "'",
    "‘": "'",
}

LATEX_REPLACEMENTS = {
    r"\Rightarrow": " implies ",
    r"\Longrightarrow": " implies ",
    r"\implies": " implies ",
    r"\rightarrow": " implies ",
    r"\to": " to ",
    r"\not\subseteq": " not in ",
    r"\subseteq": " subseteq ",
    r"\supseteq": " supseteq ",
    r"\geq": " >= ",
    r"\leq": " <= ",
    r"\varepsilon": "epsilon",
    r"\epsilon": "epsilon",
    r"\delta": "delta",
    r"\gamma": "gamma",
    r"\alpha": "alpha",
    r"\beta": "beta",
    r"\phi": "phi",
    r"\psi": "psi",
    r"\theta": "theta",
    r"\lambda": "lambda",
    r"\mu": "mu",
    r"\nu": "nu",
    r"\pi": "pi",
    r"\rho": "rho",
    r"\sigma": "sigma",
    r"\tau": "tau",
    r"\omega": "omega",
    r"\NP": "NP",
    r"\Ppoly": "P/poly",
    r"\NCone": "NC1",
    r"\NEXP": "NEXP",
    r"\EXP": "EXP",
    r"\BPP": "BPP",
    r"\P": "P",
    r"\MCSP": "MCSP",
    r"\SAT": "SAT",
    r"\TAUT": "TAUT",
    r"\poly": "poly",
    r"\ACzero": "AC0",
    r"\ACCzero": "ACC0",
    r"\TCzero": "TC0",
}

GENERIC_PREFIXES = (
    "a theorem has the form:",
    "this theorem has the form:",
    "the theorem has the form:",
    "a hardness magnification theorem has the form:",
)


def _clean_spaces(text: str) -> str:
    return " ".join(str(text or "").split())


def normalize_math_text(value: Any) -> str:
    """Convert mildly noisy informal/LaTeX statement text into readable mathematical prose."""

    text = str(value or "").strip()
    if not text:
        return ""
    stripped_original = text.rstrip()
    terminal = stripped_original[-1] if stripped_original and stripped_original[-1] in ".!?" else "."
    for src, dst in MOJIBAKE_REPLACEMENTS.items():
        text = text.replace(src, dst)
    for src, dst in LATEX_REPLACEMENTS.items():
        text = text.replace(src, dst)
    text = text.replace("\\[", " ").replace("\\]", " ").replace("\\(", " ").replace("\\)", " ")
    text = text.replace("$", " ").replace("{", " ").replace("}", " ")
    previous = None
    while previous != text:
        previous = text
        text = _COMMAND_WITH_ARG_RE.sub(r"\1", text)
    text = text.replace("^", "^").replace("_", "_")
    text = text.replace("\\,", " ").replace("\\;", " ").replace("\\:", " ").replace("\\!", " ")
    text = text.replace("\\%", "%").replace("\\&", "&").replace("\\#", "#")
    text = _INLINE_MACRO_RE.sub(lambda m: LATEX_REPLACEMENTS.get("\\" + m.group(1), m.group(1)), text)
    text = text.replace("\\", " ")
    text = re.sub(r"\bRightarrow\b", " implies ", text)
    text = text.replace("Qtext", "Q text")
    text = re.sub(r"\btext\b", " ", text)
    text = text.replace("notsubseteq", "not in")
    text = re.sub(r"([A-Za-z0-9/])not in\b", r"\1 not in", text)
    text = text.replace("Ppoly", "P/poly")
    text = text.replace("e.g.\\", "e.g.")
    text = _DISPLAY_BRACKET_RE.sub(" ", text)
    text = text.replace("subseteq", "subseteq")
    text = text.replace("  ", " ")
    text = _clean_spaces(text)
    text = text.replace('" ', '"').replace(' "', '"')
    text = text.strip(" .")
    if not text:
        return ""
    return text + terminal


def humanize_schema_label(label: Any) -> str:
    """Turn a schema/profile label into readable prose when theorem text is unavailable."""

    text = str(label or "").strip()
    if not text:
        return ""
    text = text.replace("not-in", "not in ")
    text = text.replace("notsubseteq", "not in ")
    text = text.replace("Ppoly", "P/poly")
    text = text.replace("poly", "poly")
    text = text.replace("_", " ").replace("-", " ")
    text = _clean_spaces(text)
    text = text.replace("NP vs P/poly separation", "NP versus P/poly separation")
    return text


def _statement_quality(text: str) -> float:
    lower = str(text or "").lower()
    if not lower:
        return -1.0
    words = lower.split()
    penalty = 0.0
    for bad in (" qtext", "\\", "{", "}", " rightarrow", " emph ", "mathcal", "mathbb"):
        if bad in lower:
            penalty += 6.0
    for bad in ("[ text", "q text", " text\"", " text'", " q ", " ppoly"):
        if bad in lower:
            penalty += 4.0
    if lower.count('"') % 2 == 1:
        penalty += 2.0
    return min(len(words), 42) - penalty


def statement_excerpt(statement: dict[str, Any], limit: int = 320) -> str:
    """Return a normalized excerpt for a statement, choosing the cleaner of informal and LaTeX."""

    if not isinstance(statement, dict):
        return ""
    informal = normalize_math_text(statement.get("informal", ""))
    latex = normalize_math_text(statement.get("latex", ""))
    text = informal if _statement_quality(informal) >= _statement_quality(latex) else latex
    if len(text) > limit:
        cut = text[: max(0, limit - 3)].rstrip()
        if " " in cut:
            cut = cut.rsplit(" ", 1)[0]
        text = cut + "..."
    return text


def _predicate_segment(text: str) -> str:
    out = text.strip().strip('"').strip("'")
    out = _SUBJECT_IS_RE.sub("", out)
    out = _SUBJECT_ARE_RE.sub("", out)
    return out.strip(" .,:;")


def _focus_from_text(text: str, *, role: str) -> str:
    source_text = str(text or "").strip()
    if not source_text:
        return ""
    lower = source_text.lower()
    working = source_text
    if ":" in working:
        prefix, suffix = working.split(":", 1)
        if prefix.strip().lower() in GENERIC_PREFIXES or len(prefix.strip()) <= 48:
            working = suffix.strip()
            lower = working.lower()

    for marker in (" would imply ", " imply ", " implies "):
        if marker in lower:
            idx = lower.index(marker)
            segment = working[:idx] if role == "source" else working[idx + len(marker) :]
            if role == "source" and " such that " in segment.lower():
                segment = segment.split(" such that ", 1)[1]
            return _predicate_segment(segment)

    if " such that " in lower:
        return _predicate_segment(working.split(" such that ", 1)[1])
    if role == "target":
        for marker in (" is not ", " are not ", " is ", " are "):
            if marker in lower:
                idx = lower.index(marker)
                return _predicate_segment(working[idx + 1 :])

    sentence = re.split(r"[.;]", working, maxsplit=1)[0]
    if role == "source" and " and " in sentence and len(sentence.split()) > 16:
        sentence = sentence.split(" and ", 1)[0]
    return _predicate_segment(sentence)


def statement_focus(statement: dict[str, Any], *, fallback: Any = "", role: str = "source", limit: int = 140) -> str:
    """Extract a short claim focus tied to the normalized theorem body."""

    excerpt = statement_excerpt(statement, limit=360)
    focus = _focus_from_text(excerpt, role=role)
    if not focus:
        focus = humanize_schema_label(fallback)
    if not focus:
        return ""
    if len(focus) > limit:
        cut = focus[: max(0, limit - 3)].rstrip()
        if " " in cut:
            cut = cut.rsplit(" ", 1)[0]
        focus = cut + "..."
    return focus


def load_statement_index(kb_path: Path | None) -> dict[str, dict[str, Any]]:
    """Load KB YAML statement blocks keyed by statement id."""

    if kb_path is None or not kb_path.exists():
        return {}
    try:
        text = kb_path.read_text(encoding="utf-8")
    except OSError:
        return {}
    out: dict[str, dict[str, Any]] = {}
    for match in YAML_BLOCK_RE.finditer(text):
        try:
            payload = yaml.safe_load(match.group(1))
        except yaml.YAMLError:
            continue
        if not isinstance(payload, dict):
            continue
        sid = str(payload.get("id", "")).strip()
        if sid:
            out[sid] = payload
    return out
