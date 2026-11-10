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
"""Validate generated timeline LaTeX section packet."""

from __future__ import annotations

from agentic_common import clean_text, fail, load_json_object, rel
from build_timeline_latex_sections import LATEST_JSON, OUT_JSON, OUT_MD, OUT_REPORT_TEX, OUT_TEX, TRANSLATOR_SKILLS, report_tab_sections, tex_escape_mathish


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def main() -> int:
    require(OUT_JSON.exists(), f"missing {rel(OUT_JSON)}")
    report = load_json_object(OUT_JSON)
    marathon = load_json_object(LATEST_JSON) if LATEST_JSON.exists() else {}
    target_id = clean_text(report.get("target_id") or marathon.get("target_id"))
    expected_sections = report_tab_sections(target_id)
    require(report.get("status") == "timeline_latex_sections_ready", "timeline latex section packet must be ready")
    require(set(TRANSLATOR_SKILLS).issubset(set(report.get("translator_skills", []))), "missing translator skills")
    sections = report.get("sections", [])
    require(isinstance(sections, list) and len(sections) == len(expected_sections), "expected report-shaped translated sections")
    expected_order = [row["section_id"] for row in expected_sections]
    require([section.get("section_id") for section in sections] == expected_order, "section ids must match report tab order")
    contract = report.get("report_document_contract", {})
    require(contract.get("mapping_rule") == "each visible timeline report tab is translated into one LaTeX section in the same tab order", "missing tab-to-section mapping rule")
    tab_sections = contract.get("tab_sections", [])
    require(isinstance(tab_sections, list) and len(tab_sections) == len(expected_sections), "missing report tab section contract")
    require([row.get("tab_id") for row in tab_sections] == [row["tab_id"] for row in expected_sections], "tab ids mismatch")
    require(all(row.get("present") for row in tab_sections), "not every report tab is present as a LaTeX section")
    for section in sections:
        text = clean_text(section)
        require("\\section" in section.get("latex", ""), f"{section.get('section_id')} missing LaTeX section")
        tab = next((row for row in expected_sections if row["section_id"] == section.get("section_id")), {})
        require(section.get("source_tab_id") == tab.get("tab_id"), f"{section.get('section_id')} missing source tab id")
        require(section.get("source_tab_label") == tab.get("tab_label"), f"{section.get('section_id')} missing source tab label")
        require(clean_text(section.get("translator_skill")), f"{section.get('section_id')} missing translator skill")
        require(clean_text(section.get("epistemic_status")), f"{section.get('section_id')} missing epistemic status")
        for bad in ["<span", "</span>", "Misplaced &"]:
            require(bad not in text, f"{section.get('section_id')} contains raw HTML/math error marker {bad}")
    require(OUT_TEX.exists(), f"missing {rel(OUT_TEX)}")
    tex = OUT_TEX.read_text(encoding="utf-8")
    require(not any(ord(ch) < 32 and ch not in "\n\t\r" for ch in tex), f"{rel(OUT_TEX)} contains control characters")
    for bad in [r"\textbackslash{}exists", r"\textbackslash{}mathrm", r"\textbackslash{}mathbb"]:
        require(bad not in tex, f"{rel(OUT_TEX)} contains literalized LaTeX command {bad}")
    required_phrases = [
        "Content-Specific Full Timeline",
        "Current Ranked Next-Analysis Queue",
        "Qualitative Mechanistic Graph",
        "Gedanken Experiments",
        "Parsimonious Probe Control",
        "Scientific Contribution Monitor",
        "Target Problem And Literature Evolution",
        "Macro Strategies",
        "Strategy Progression Judge",
        "Accumulated Physics Story",
        "Summary",
        "claim",
        "validation",
    ]
    if target_id == "p-vs-np-target":
        required_phrases = [
            phrase
            for phrase in required_phrases
            if phrase not in {"Physics And Maths Strategy", "Accumulated Physics Story"}
        ]
        required_phrases.extend(["Complexity Strategy", "Accumulated Proof Strategy Story"])
    for phrase in required_phrases:
        require(phrase in tex, f"{rel(OUT_TEX)} missing `{phrase}`")
    for table_marker in ["\\begin{longtable}", "\\begin{tabular}", "\\begin{table}"]:
        require(table_marker not in tex, f"translated report packet must not use table environment {table_marker}")
    expected_cycles = 80 if target_id == "yang-mills-existence-and-mass-gap-target" else max(1, int(marathon.get("completed_cycles", 0) or 0))
    require(tex.count("cycle-") >= expected_cycles, "timeline section must preserve the full report timeline window")
    if target_id == "p-vs-np-target":
        forbidden = ["Yang-Mills", "mass gap", "Wilson", "Schwinger", "Wightman", "gauge-invariant", "hairpin", "collar"]
        for term in forbidden:
            require(term not in tex, f"{rel(OUT_TEX)} contains cross-target term `{term}` for P vs NP")
    require(OUT_REPORT_TEX.exists(), f"missing {rel(OUT_REPORT_TEX)}")
    report_tex = OUT_REPORT_TEX.read_text(encoding="utf-8")
    require("\\documentclass" in report_tex and "\\begin{document}" in report_tex and "\\end{document}" in report_tex, "standalone report TeX must be a full document")
    require("Report Translation Contract" in report_tex, "standalone report TeX missing translation contract")
    for tab in expected_sections:
        require(tex_escape_mathish(tab["tab_label"]) in report_tex, f"standalone report TeX missing tab label {tab['tab_label']}")
        require(f"\\section{{{tab['section_title']}}}" in report_tex, f"standalone report TeX missing tab section {tab['section_title']}")
    require(OUT_MD.exists(), f"missing {rel(OUT_MD)}")
    print(f"validated {rel(OUT_JSON)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
