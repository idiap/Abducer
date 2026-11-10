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
"""Shared helpers for the interpretive timeline-paper workflow."""

from __future__ import annotations

import html as html_lib
import json
import re
from pathlib import Path
from typing import Any

from agentic_common import ROOT, clean_text, load_optional_json, rel, stable_id, utc_now, write_json


FULL_TIMELINE_HTML = ROOT / "agentic/reports/discovery_marathon/full_timeline.html"
LATEST_MARATHON_JSON = ROOT / "agentic/reports/discovery_marathon/latest.json"
TARGET_LITERATURE = ROOT / "agentic/reports/target_literature_evolution/latest.json"
MACRO_STRATEGY = ROOT / "agentic/reports/macro_strategy/latest.json"
CONTRIBUTION_MONITOR = ROOT / "agentic/reports/scientific_contribution_monitor/latest.json"
STRATEGY_JUDGE = ROOT / "agentic/reports/strategy_progression_judge/latest.json"
TIMELINE_LATEX_SECTIONS = ROOT / "agentic/reports/timeline_latex_sections/latest.json"
ENDPOINT_INCIDENCE = ROOT / "agentic/reports/endpoint_incidence_certificate/latest.json"
FINITE_ALGEBRA = ROOT / "agentic/reports/finite_algebra_interfaces/latest.json"
ANALYTIC_OBLIGATIONS = ROOT / "agentic/reports/analytic_estimate_obligations/latest.json"

REPORT_FAMILIES = [
    "summary_analysis_control",
    "timeline_cycles",
    "timeline_ranked_next_experiment_queue",
    "qualitative_mechanistic_graph",
    "gedanken_experiments",
    "parsimonious_probe_layer",
    "scientific_contribution_monitor",
    "target_literature_evolution",
    "macro_strategy_report",
    "strategy_progression_judge",
    "timeline_storyline",
    "timeline_paper_report",
    "branch_summaries",
    "deep_reviews",
]


def payload_target_id(payload: dict[str, Any]) -> str:
    report = payload.get("report", {}) if isinstance(payload.get("report"), dict) else {}
    return clean_text(report.get("target_id") or payload.get("target_id"))


def target_matches(report: dict[str, Any], target_id: str) -> bool:
    declared = clean_text(report.get("target_id"))
    return not target_id or not declared or declared == target_id


def build_target_literature(target_id: str) -> dict[str, Any]:
    if target_id == "p-vs-np-target":
        from build_target_literature_evolution import build_pvsnp_report

        return build_pvsnp_report({"target_id": target_id, "raw_goal": "P vs NP", "source": "timeline paper source bundle"})
    if target_id == "yang-mills-existence-and-mass-gap-target":
        from build_target_literature_evolution import build_yang_mills_report

        return build_yang_mills_report({"target_id": target_id, "raw_goal": "Yang-Mills existence and mass gap", "source": "timeline paper source bundle"})
    return {}


def build_contribution_monitor(target_id: str) -> dict[str, Any]:
    if not target_id:
        return {}
    from build_scientific_contribution_monitor import build_report as build_contribution_report

    return build_contribution_report(target_id)


def load_embedded_payload(path: Path = FULL_TIMELINE_HTML) -> dict[str, Any]:
    if not path.exists():
        return {}
    text = path.read_text(encoding="utf-8")
    marker = '<script id="marathon-data" type="application/json">'
    if marker not in text:
        return {}
    raw = text.split(marker, 1)[1].split("</script>", 1)[0]
    payload = json.loads(html_lib.unescape(raw))
    return payload if isinstance(payload, dict) else {}


def load_source_bundle(source_report: Path = FULL_TIMELINE_HTML) -> dict[str, Any]:
    payload = load_embedded_payload(source_report)
    if not payload:
        payload = load_optional_json(LATEST_MARATHON_JSON)
    target_id = payload_target_id(payload)
    literature = payload.get("target_literature_evolution") if isinstance(payload.get("target_literature_evolution"), dict) else {}
    if not literature or not target_matches(literature, target_id):
        literature = load_optional_json(TARGET_LITERATURE)
    if not literature or not target_matches(literature, target_id):
        literature = build_target_literature(target_id)
    contribution_monitor = payload.get("scientific_contribution_monitor") if isinstance(payload.get("scientific_contribution_monitor"), dict) else {}
    if not contribution_monitor or not target_matches(contribution_monitor, target_id):
        contribution_monitor = load_optional_json(CONTRIBUTION_MONITOR)
    if not contribution_monitor or not target_matches(contribution_monitor, target_id):
        contribution_monitor = build_contribution_monitor(target_id)
    return {
        "payload": payload,
        "source_report": rel(source_report if source_report.exists() else LATEST_MARATHON_JSON),
        "target_literature": literature,
        "macro_strategy": payload.get("macro_strategy_report") or load_optional_json(MACRO_STRATEGY),
        "contribution_monitor": contribution_monitor,
        "strategy_judge": payload.get("strategy_progression_judge") or load_optional_json(STRATEGY_JUDGE),
        "timeline_latex_sections": load_optional_json(TIMELINE_LATEX_SECTIONS),
        "endpoint_incidence": load_optional_json(ENDPOINT_INCIDENCE),
        "finite_algebra": load_optional_json(FINITE_ALGEBRA),
        "analytic_obligations": load_optional_json(ANALYTIC_OBLIGATIONS),
    }


def unit(
    *,
    family: str,
    kind: str,
    title: Any,
    content: Any,
    argument_role: str,
    disposition: str,
    source: str,
    cycle_id: str = "",
    evidence_status: str = "evidence_backed",
    extra: dict[str, Any] | None = None,
) -> dict[str, Any]:
    text = clean_text(content)
    title_text = clean_text(title) or kind
    payload = {
        "unit_id": stable_id("paper-unit", family, kind, title_text, text[:240], cycle_id),
        "family": family,
        "kind": kind,
        "title": title_text,
        "content": text,
        "argument_role": argument_role,
        "disposition": disposition,
        "source": source,
        "cycle_id": cycle_id,
        "evidence_status": evidence_status,
    }
    if extra:
        payload.update(extra)
    return payload


def has_data(value: Any) -> bool:
    if isinstance(value, dict):
        return any(has_data(item) for item in value.values())
    if isinstance(value, list):
        return any(has_data(item) for item in value)
    return bool(clean_text(value))


def family_value(bundle: dict[str, Any], family: str) -> Any:
    payload = bundle["payload"]
    if family == "target_literature_evolution":
        return bundle["target_literature"]
    if family == "macro_strategy_report":
        return bundle["macro_strategy"]
    if family == "scientific_contribution_monitor":
        return bundle["contribution_monitor"]
    if family == "strategy_progression_judge":
        return bundle["strategy_judge"]
    return payload.get(family)


def coverage_from_units(bundle: dict[str, Any], units: list[dict[str, Any]]) -> dict[str, Any]:
    by_family: dict[str, list[dict[str, Any]]] = {}
    for row in units:
        by_family.setdefault(row["family"], []).append(row)
    coverage = {}
    for family in REPORT_FAMILIES:
        value = family_value(bundle, family)
        rows = by_family.get(family, [])
        dispositions: dict[str, int] = {}
        for row in rows:
            dispositions[row["disposition"]] = dispositions.get(row["disposition"], 0) + 1
        coverage[family] = {
            "present": has_data(value),
            "unit_count": len(rows),
            "dispositions": dispositions,
            "explicit_empty_reason": "" if has_data(value) else "source family absent or empty in the timeline payload",
        }
    missing = [
        family
        for family, row in coverage.items()
        if row["present"] and row["unit_count"] == 0 and not row["explicit_empty_reason"]
    ]
    return {"families": coverage, "missing_report_material": missing}


def latex_escape(value: Any) -> str:
    text = clean_text(value)
    text = (
        text.replace("–", "--")
        .replace("—", "---")
        .replace("’", "'")
        .replace("“", '"')
        .replace("”", '"')
        .replace("≥", ">=")
        .replace("≤", "<=")
        .replace("→", "->")
        .replace("Ω", r"\(\Omega\)")
        .replace("κ", r"\(\kappa\)")
    )
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
    for src, dst in replacements.items():
        text = text.replace(src, dst)
    return text


def safe_tex_math(value: Any) -> str:
    formula = clean_text(value)
    formula = html_lib.unescape(formula)
    formula = formula.replace("\\gt", ">").replace("\\lt", "<")
    formula = re.sub(r"\\mathbb\s+([A-Za-z])", r"\\mathbb{\1}", formula)
    return formula or r"\text{not recorded}"


def tex_itemize(items: list[Any], *, limit: int | None = None) -> str:
    rows = [clean_text(item) for item in items if clean_text(item)]
    if limit is not None:
        rows = rows[:limit]
    if not rows:
        return "\\begin{itemize}\n\\item None recorded.\n\\end{itemize}"
    return "\\begin{itemize}\n" + "\n".join(f"\\item {latex_escape(row)}" for row in rows) + "\n\\end{itemize}"


def write_report(path: Path, payload: Any) -> None:
    payload.setdefault("generated_utc", utc_now()) if isinstance(payload, dict) else None
    write_json(path, payload)
