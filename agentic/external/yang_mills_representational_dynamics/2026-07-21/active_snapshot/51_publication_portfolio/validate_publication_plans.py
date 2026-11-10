#!/usr/bin/env python3
"""Validate the five independent Yang--Mills publication plans."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
PACKAGE = ROOT.parent
REGISTRY = ROOT / "plan_registry.json"
TASK_RE = re.compile(r"^- \[[ x]\] \*\*(P[1-5]-[A-Z][0-9]+)\b", re.MULTILINE)
COMPLETED_TASK_RE = re.compile(
    r"^- \[x\] \*\*(P[1-5]-[A-Z][0-9]+)\b", re.MULTILINE
)
SOURCE_RE = re.compile(r"`((?:0[1-9]|[1-4][0-9]|50)_[^`\n]+\.[A-Za-z0-9]+)`")
REQUIRED_SECTIONS = (
    "Self-contained todo graph",
    "Stop/go gates",
    "Definition of done",
)


def fail(message: str) -> None:
    raise ValueError(message)


def main() -> int:
    data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    papers = data.get("publications", [])
    if data.get("publication_count") != 5 or len(papers) != 5:
        fail("registry must contain exactly five publications")

    shared_skills = data.get("shared_workflow_skills", [])
    if len(shared_skills) != 5 or len(shared_skills) != len(set(shared_skills)):
        fail("registry must contain five unique shared workflow skills")

    seen_ids: set[str] = set()
    seen_tasks: set[str] = set()
    actual_total = 0
    report: list[dict[str, object]] = []

    bundle_skills = (
        PACKAGE / "11_vscode_codex_skill_bundle" / ".agents" / "skills"
    )
    for skill_name in shared_skills:
        if not (bundle_skills / skill_name / "SKILL.md").is_file():
            fail(f"missing shared bundled skill: {skill_name}")

    automation_doc = ROOT / "MANUSCRIPT_AUTOMATION.md"
    if not automation_doc.is_file():
        fail("missing manuscript automation guide")
    latex_skill = bundle_skills / "ym-build-latex-paper"
    latex_resources = [
        "scripts/scaffold_paper.py",
        "scripts/lint_manuscript.py",
        "scripts/render_paper.py",
        "references/BUILD_CONTRACT.md",
        "assets/paper_template/main.tex",
    ]
    for relative in latex_resources:
        if not (latex_skill / relative).is_file():
            fail(f"missing LaTeX automation resource: {relative}")

    for paper in papers:
        paper_id = paper["id"]
        if paper_id in seen_ids:
            fail(f"duplicate publication id: {paper_id}")
        seen_ids.add(paper_id)
        if paper.get("depends_on_publications") != []:
            fail(f"{paper_id} is not independent")

        plan = ROOT / paper["plan"]
        if not plan.is_file():
            fail(f"missing plan: {plan.name}")
        text = plan.read_text(encoding="utf-8")
        for section in REQUIRED_SECTIONS:
            if section not in text:
                fail(f"{plan.name} lacks section: {section}")

        tasks = TASK_RE.findall(text)
        completed_tasks = COMPLETED_TASK_RE.findall(text)
        if len(tasks) != paper["todo_count"]:
            fail(
                f"{paper_id} todo mismatch: found {len(tasks)}, "
                f"expected {paper['todo_count']}"
            )
        for task in tasks:
            if not task.startswith(f"{paper_id}-"):
                fail(f"cross-paper task in {plan.name}: {task}")
            if task in seen_tasks:
                fail(f"duplicate task id: {task}")
            seen_tasks.add(task)

        sources = sorted(set(SOURCE_RE.findall(text)))
        missing = [source for source in sources if not (PACKAGE / source).is_file()]
        if missing:
            fail(f"missing source paths in {plan.name}: {missing}")

        skill = (
            PACKAGE
            / "11_vscode_codex_skill_bundle"
            / ".agents"
            / "skills"
            / paper["skill"]
            / "SKILL.md"
        )
        if not skill.is_file():
            fail(f"missing bundled skill for {paper_id}: {paper['skill']}")

        actual_total += len(tasks)
        report.append(
            {
                "id": paper_id,
                "plan": plan.name,
                "todos": len(tasks),
                "completed_todos": len(completed_tasks),
                "sources_checked": len(sources),
                "skill": paper["skill"],
                "independent": True,
            }
        )

    if actual_total != data.get("total_todo_count"):
        fail(
            f"total todo mismatch: found {actual_total}, "
            f"expected {data.get('total_todo_count')}"
        )

    print(
        json.dumps(
            {
                "valid": True,
                "publication_count": len(papers),
                "total_todo_count": actual_total,
                "unique_task_ids": len(seen_tasks),
                "shared_workflow_skills": shared_skills,
                "latex_automation_resources": latex_resources,
                "publications": report,
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, KeyError, ValueError, json.JSONDecodeError) as exc:
        print(f"publication plan validation failed: {exc}", file=sys.stderr)
        raise SystemExit(1)
