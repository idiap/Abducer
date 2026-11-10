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

"""Validate Abducer repo-local skills against the skill-depth contract."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from agentic_common import ROOT, fail, iter_skill_dirs, load_json_object, rel, skill_name_from_dir, write_json


SCHEMA = ROOT / "agentic/spec/skill_depth_review_schema.json"
REPORT_JSON = ROOT / "agentic/reports/skill_depth/latest.json"
REPORT_MD = ROOT / "agentic/reports/skill_depth/latest.md"


def family_for(skill_dir: Path) -> str:
    return skill_dir.relative_to(ROOT / "skills").parts[0]


def section_present(text: str, heading: str) -> bool:
    pattern = re.compile(rf"^##+\s+{re.escape(heading)}\s*$", re.IGNORECASE | re.MULTILINE)
    return bool(pattern.search(text))


def signal_present(text: str, patterns: list[str]) -> bool:
    lower = text.lower()
    return any(pattern.lower() in lower for pattern in patterns)


def check_skill(skill_dir: Path, schema: dict[str, Any]) -> dict[str, Any]:
    family = family_for(skill_dir)
    role = schema["role_family_requirements"][family]
    signal_defs = schema["signal_definitions"]
    text = (skill_dir / "SKILL.md").read_text(encoding="utf-8-sig")
    all_sections = list(dict.fromkeys(schema["mandatory_for_all"]["required_sections"] + role["required_sections"]))
    all_signals = list(dict.fromkeys(schema["mandatory_for_all"]["required_signals"] + role["required_signals"]))
    optional_signals = list(role.get("optional_signals", []))
    findings = []
    present_sections = []
    present_signals = []
    for section in all_sections:
        if section_present(text, section):
            present_sections.append(section)
        else:
            findings.append(
                {
                    "severity": "critical",
                    "category": "epistemologist",
                    "kind": "missing_section",
                    "item": section,
                    "message": f"Missing required section `{section}`.",
                }
            )
    for signal in all_signals:
        definition = signal_defs[signal]
        if signal_present(text, definition["patterns"]):
            present_signals.append(signal)
        else:
            findings.append(
                {
                    "severity": definition["severity"],
                    "category": definition["category"],
                    "kind": "missing_signal",
                    "item": signal,
                    "message": f"Missing required {definition['category']} signal `{signal}`.",
                }
            )
    for signal in optional_signals:
        definition = signal_defs[signal]
        if signal_present(text, definition["patterns"]):
            present_signals.append(signal)
        else:
            findings.append(
                {
                    "severity": "low",
                    "category": definition["category"],
                    "kind": "optional_signal_absent",
                    "item": signal,
                    "message": f"Optional depth signal `{signal}` not observed.",
                }
            )
    has_scripts = (skill_dir / "scripts").exists()
    if has_scripts and "codex_exec_protocol" not in present_signals:
        findings.append(
            {
                "severity": "critical",
                "category": "epistemologist",
                "kind": "script_without_exec_protocol",
                "item": "codex_exec_protocol",
                "message": "Script-backed skill must link deterministic execution to generative interpretation.",
            }
        )
    mathematician_findings = [row for row in findings if row["category"] == "mathematician"]
    epistemologist_findings = [row for row in findings if row["category"] == "epistemologist"]
    critical_count = sum(1 for row in findings if row["severity"] == "critical")
    return {
        "skill_name": skill_name_from_dir(skill_dir),
        "family": family,
        "path": rel(skill_dir),
        "role": role["role"],
        "has_scripts": has_scripts,
        "present_sections": sorted(set(present_sections)),
        "present_signals": sorted(set(present_signals)),
        "mathematician_findings": mathematician_findings,
        "epistemologist_findings": epistemologist_findings,
        "critical_findings": critical_count,
        "status": "pass" if critical_count == 0 else "fail",
    }


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Skill Depth Audit",
        "",
        f"- Skills checked: {report['summary']['skills_checked']}",
        f"- Critical findings: {report['summary']['critical_findings']}",
        f"- Mathematician findings: {report['summary']['mathematician_findings']}",
        f"- Epistemologist findings: {report['summary']['epistemologist_findings']}",
        "",
        "## By Skill",
        "",
    ]
    for row in report["skills"]:
        lines.append(f"### {row['skill_name']}")
        lines.append("")
        lines.append(f"- Family: `{row['family']}`")
        lines.append(f"- Status: `{row['status']}`")
        lines.append(f"- Present signals: `{', '.join(row['present_signals'])}`")
        if row["mathematician_findings"]:
            lines.append("- Mathematician findings:")
            for finding in row["mathematician_findings"]:
                lines.append(f"  - `{finding['severity']}` {finding['message']}")
        if row["epistemologist_findings"]:
            lines.append("- Epistemologist findings:")
            for finding in row["epistemologist_findings"]:
                lines.append(f"  - `{finding['severity']}` {finding['message']}")
        lines.append("")
    return "\n".join(lines)


def main() -> int:
    schema = load_json_object(SCHEMA)
    allowed_families = set(schema["thematic_folders"])
    skills = []
    for skill_dir in iter_skill_dirs():
        family = family_for(skill_dir)
        if family not in allowed_families:
            fail(f"unknown skill family `{family}` for {rel(skill_dir)}")
        skills.append(check_skill(skill_dir, schema))
    report = {
        "version": 1,
        "schema": rel(SCHEMA),
        "summary": {
            "skills_checked": len(skills),
            "critical_findings": sum(row["critical_findings"] for row in skills),
            "mathematician_findings": sum(len(row["mathematician_findings"]) for row in skills),
            "epistemologist_findings": sum(len(row["epistemologist_findings"]) for row in skills),
            "script_backed_skills": sum(1 for row in skills if row["has_scripts"]),
        },
        "skills": skills,
    }
    write_json(REPORT_JSON, report)
    REPORT_MD.parent.mkdir(parents=True, exist_ok=True)
    REPORT_MD.write_text(render_markdown(report), encoding="utf-8")
    print(
        "validated "
        f"{report['summary']['skills_checked']} skills; "
        f"{report['summary']['critical_findings']} critical findings"
    )
    return 1 if report["summary"]["critical_findings"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
