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
"""Generate a self-contained project evolution report from git history."""

from __future__ import annotations

import argparse
import ast
import html
import json
import re
import subprocess
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Iterable


CODE_EXTENSIONS = {
    ".py",
    ".sv",
    ".v",
    ".svh",
    ".rvr",
    ".yml",
    ".yaml",
    ".json",
    ".toml",
    ".md",
    ".rst",
    ".html",
    ".css",
    ".js",
}

EXCLUDED_PREFIXES = (
    ".git/",
    ".venv/",
    "__pycache__/",
    "runs/",
)

EXCLUDED_EXACT_PATHS = {
    "docs/reports/project_evolution_timeline.html",
    "docs/reports/project_evolution_timeline.json",
}


@dataclass(frozen=True)
class CommitInfo:
    sha: str
    date: str
    subject: str
    changed_paths: tuple[str, ...]
    skill_count: int
    categories: tuple[str, ...]

    @property
    def short_sha(self) -> str:
        return self.sha[:7]


def run_git(repo: Path, args: list[str]) -> str:
    return subprocess.check_output(["git", *args], cwd=repo, text=True)


def git_lines(repo: Path, args: list[str]) -> list[str]:
    output = run_git(repo, args)
    return [line for line in output.splitlines() if line.strip()]


def is_excluded(path: str) -> bool:
    normalized = path.replace("\\", "/")
    return normalized in EXCLUDED_EXACT_PATHS or any(normalized.startswith(prefix) for prefix in EXCLUDED_PREFIXES)


def tracked_files(repo: Path) -> list[str]:
    output = run_git(repo, ["ls-files", "--cached", "--others", "--exclude-standard", "-z"])
    return sorted(path for path in output.split("\0") if path and not is_excluded(path))


def files_at_commit(repo: Path, commit: str) -> list[str]:
    try:
        return [
            path
            for path in git_lines(repo, ["ls-tree", "-r", "--name-only", commit])
            if not is_excluded(path)
        ]
    except subprocess.CalledProcessError:
        return []


def changed_paths(repo: Path, commit: str) -> tuple[str, ...]:
    try:
        paths = git_lines(repo, ["diff-tree", "--root", "--no-commit-id", "--name-only", "-r", commit])
    except subprocess.CalledProcessError:
        return ()
    return tuple(path for path in paths if path and not is_excluded(path))


def is_skill_path(path: str) -> bool:
    return bool(
        re.match(
            r"^(?:skills/[^/]+/[^/]+|proj_skills/[^/]+|prism_me/[^/]+)/SKILL\.md$",
            path,
        )
    )


def count_skill_files(paths: Iterable[str]) -> int:
    return sum(1 for path in paths if is_skill_path(path))


def count_use_cases(paths: Iterable[str]) -> int:
    return sum(1 for path in paths if path.startswith("KB/") and path.endswith(".kb.md"))


def frontmatter_value(text: str, key: str) -> str:
    if not text.startswith("---"):
        return ""
    parts = text.split("---", 2)
    if len(parts) < 3:
        return ""
    for line in parts[1].splitlines():
        if line.startswith(f"{key}:"):
            return line.split(":", 1)[1].strip().strip('"')
    return ""


def classify_skill_theme(name: str, description: str, path: str) -> str:
    haystack = f"{name} {description} {path}".lower()
    theme_rules = [
        ("Project Support", ("proj_skills/", "project evolution", "git history", "timeline")),
        ("Prism Planning And Verification", ("prism_me/", "spec", "verification", "persona", "handoff")),
        ("Mathematical Discovery And Proof", ("proof", "conjecture", "abduce", "theorem", "mathlib", "phyp")),
        ("Source Intake And Normalization", ("ingest", "source", "latex", "parser", "normalizer")),
        ("Review, Critique, And Signoff", ("critic", "review", "signoff", "calibration", "consistency", "redundancy", "readability")),
        ("Testing And Validation", ("test", "validation", "vacuity", "coverage", "scenario", "oracle", "controllability")),
        ("Reports And Explanation", ("report", "writing", "html", "visualizer", "explain", "narrative", "discourse")),
        ("Runtime And Integration", ("agentic", "operation", "trace", "api", "runtime")),
        ("Evidence And Comparative Diagnostics", ("evidence", "prior art", "comparison", "counterexample", "audit")),
    ]
    for theme, needles in theme_rules:
        if any(needle in haystack for needle in needles):
            return theme
    return "General Workflow Skills"


def skill_theme_clusters(repo: Path, paths: Iterable[str]) -> list[dict[str, object]]:
    clusters: dict[str, list[dict[str, str]]] = defaultdict(list)
    for rel_path in paths:
        if not is_skill_path(rel_path):
            continue
        path = repo / rel_path
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            text = ""
        name = frontmatter_value(text, "name") or Path(rel_path).parent.name
        description = frontmatter_value(text, "description")
        theme = classify_skill_theme(name, description, rel_path)
        clusters[theme].append(
            {
                "name": name,
                "path": rel_path,
                "description": description,
            }
        )
    return [
        {
            "theme": theme,
            "count": len(items),
            "skills": sorted(items, key=lambda item: item["name"]),
        }
        for theme, items in sorted(clusters.items(), key=lambda item: (-len(item[1]), item[0]))
    ]


def count_lines(repo: Path, paths: Iterable[str]) -> int:
    total = 0
    for rel_path in paths:
        path = repo / rel_path
        if path.suffix.lower() not in CODE_EXTENSIONS or not path.is_file():
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        total += sum(1 for line in text.splitlines() if line.strip())
    return total


def count_prompt_files_and_lines(repo: Path, paths: Iterable[str]) -> tuple[int, int]:
    prompt_paths = [
        rel_path
        for rel_path in paths
        if rel_path.startswith("skills/")
        and Path(rel_path).suffix.lower() in {".yml", ".yaml", ".md", ".txt"}
    ]
    prompt_lines = 0
    for rel_path in prompt_paths:
        path = repo / rel_path
        if not path.is_file():
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        prompt_lines += sum(1 for line in text.splitlines() if line.strip())
    return len(prompt_paths), prompt_lines


def count_python_classes(repo: Path, paths: Iterable[str]) -> int:
    count = 0
    for rel_path in paths:
        if not rel_path.endswith(".py"):
            continue
        path = repo / rel_path
        if not path.is_file():
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        count += len(re.findall(r"^\s*class\s+[A-Za-z_][A-Za-z0-9_]*", text, flags=re.MULTILINE))
    return count


def count_python_functions_and_methods(repo: Path, paths: Iterable[str]) -> tuple[int, int]:
    functions = 0
    methods = 0
    for rel_path in paths:
        if not rel_path.endswith(".py"):
            continue
        path = repo / rel_path
        if not path.is_file():
            continue
        try:
            tree = ast.parse(path.read_text(encoding="utf-8"))
        except (SyntaxError, UnicodeDecodeError):
            continue
        for node in tree.body:
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                functions += 1
            elif isinstance(node, ast.ClassDef):
                methods += sum(
                    1
                    for child in node.body
                    if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef))
                )
    return functions, methods


def count_test_cases(repo: Path, paths: Iterable[str]) -> tuple[int, int]:
    test_files = [
        path for path in paths if re.match(r"^tests/[^/]+/test_.*\.py$", path)
    ]
    test_cases = 0
    for rel_path in test_files:
        path = repo / rel_path
        if not path.is_file():
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        test_cases += len(re.findall(r"^\s+def\s+test_[A-Za-z0-9_]+", text, flags=re.MULTILINE))
    return len(test_files), test_cases


def discover_key_functionality(paths: Iterable[str]) -> list[dict[str, str]]:
    path_set = set(paths)
    areas: list[tuple[str, str, list[str]]] = [
        (
            "Controlled scientific discovery workflow",
            "Skill-directed research loops, persistent proof queues, and governed evidence handling.",
            ["skills/orchestration/work/SKILL.md", "agentic", "phyp"],
        ),
        (
            "Specialized skill catalog",
            "Thematic scientific skills plus Prism planning and verification skills.",
            ["docs/reference/skills.md", "prism_me/agents.md"],
        ),
        (
            "Project support skills",
            "Repository-history and project-maintenance skills kept separate from scientific discovery workflow skills.",
            ["proj_skills/project-evolution-timeline-reporter/SKILL.md"],
        ),
        (
            "Knowledge and proof-state assets",
            "Problem knowledge bases, proof hypotheses, theorem memory, and evaluation assets.",
            ["KB", "InformalMathLib", "phyp", "agentic/evals"],
        ),
        (
            "Reasoning and report surfaces",
            "HTML reports, reasoning logs, comparison reports, and visualization tools.",
            ["docs/operations/logging.md", "skills/reporting", "agentic/traces"],
        ),
        (
            "Validation harness",
            "Regression tests for workflow behavior, skill contracts, integration parity, and report quality.",
            ["tests", "proj_skills/scripts/validate_proj_skills.py"],
        ),
    ]
    discovered = []
    for title, description, signals in areas:
        if any(signal in path_set or any(path.startswith(signal.rstrip("/") + "/") for path in path_set) for signal in signals):
            discovered.append({"title": title, "description": description})
    return discovered


CATEGORY_RULES: list[tuple[str, tuple[str, ...]]] = [
    ("Reasoning and orchestration", ("agentic/", "workflow", "proof queue", "orchestrat", "control-plane")),
    ("Mathematical discovery and proof", ("conjecture", "proof", "theorem", "mathlib", "phyp/", "skills/discovery")),
    ("Skill architecture", ("skills/", "proj_skills/", "prism_me/", "skill", "catalog", "router")),
    ("Reporting and visualization", ("report", "html", "visualizer", "workbench", "dashboard", "timeline")),
    ("Test and validation", ("tests/", "test", "validation", "regression", "parity", "smoke")),
    ("Knowledge and evaluation assets", ("KB/", "InformalMathLib/", "phyp/", "agentic/evals/", "benchmark")),
    ("Executable evidence", ("script", "trace", "evaluation", "fixture", "execution")),
    ("Source intake and normalization", ("ingest", "latex", "parser", "normalizer", "source")),
]


def classify_commit(subject: str, paths: Iterable[str]) -> tuple[str, ...]:
    haystack = " ".join([subject.lower(), *[path.lower() for path in paths]])
    matches = []
    for label, needles in CATEGORY_RULES:
        score = sum(1 for needle in needles if needle in haystack)
        if score:
            matches.append((score, label))
    if not matches:
        return ("General project evolution",)
    matches.sort(key=lambda item: (-item[0], item[1]))
    return tuple(label for _, label in matches[:2])


def read_commits(repo: Path) -> list[CommitInfo]:
    rows = git_lines(repo, ["log", "--reverse", "--format=%H%x1f%ad%x1f%s", "--date=short"])
    commits: list[CommitInfo] = []
    for row in rows:
        parts = row.split("\x1f", 2)
        if len(parts) != 3:
            continue
        sha, date, subject = parts
        paths = changed_paths(repo, sha)
        skill_count = count_skill_files(files_at_commit(repo, sha))
        categories = classify_commit(subject, paths)
        commits.append(
            CommitInfo(
                sha=sha,
                date=date,
                subject=subject,
                changed_paths=paths,
                skill_count=skill_count,
                categories=categories,
            )
        )
    return commits


def select_milestones(commits: list[CommitInfo], max_milestones: int) -> list[CommitInfo]:
    if not commits:
        return []
    selected: list[CommitInfo] = [commits[0]]
    seen_categories = set(commits[0].categories)
    previous_skill_count = commits[0].skill_count
    for commit in commits[1:]:
        new_category = any(category not in seen_categories for category in commit.categories)
        skill_delta = commit.skill_count - previous_skill_count
        recent_gap = selected and commit.date[:7] != selected[-1].date[:7]
        if new_category or skill_delta >= 3 or (recent_gap and skill_delta > 0):
            selected.append(commit)
            seen_categories.update(commit.categories)
        previous_skill_count = commit.skill_count
        if len(selected) >= max_milestones:
            break
    if commits[-1] not in selected:
        selected.append(commits[-1])
    return selected[: max_milestones + 1]


def current_state(repo: Path, commits: list[CommitInfo]) -> dict[str, object]:
    paths = tracked_files(repo)
    test_file_count, test_case_count = count_test_cases(repo, paths)
    function_count, method_count = count_python_functions_and_methods(repo, paths)
    prompt_count, prompt_line_count = count_prompt_files_and_lines(repo, paths)
    return {
        "tracked_files": len(paths),
        "commits": len(commits),
        "use_cases": count_use_cases(paths),
        "skills": count_skill_files(paths),
        "classes": count_python_classes(repo, paths),
        "functions": function_count,
        "methods": method_count,
        "prompts": prompt_count,
        "prompt_lines": prompt_line_count,
        "test_files": test_file_count,
        "test_cases": test_case_count,
        "lines_of_code": count_lines(repo, paths),
        "key_functionality": discover_key_functionality(paths),
        "skill_theme_clusters": skill_theme_clusters(repo, paths),
    }


def timeline_points(commits: list[CommitInfo], state: dict[str, object]) -> list[CommitInfo]:
    points = list(commits)
    current_skill_count = int(state.get("skills", 0))
    if points and current_skill_count != points[-1].skill_count:
        points.append(
            CommitInfo(
                sha="working-tree",
                date="Working tree",
                subject="Current working tree snapshot",
                changed_paths=(),
                skill_count=current_skill_count,
                categories=("Uncommitted project-support work",),
            )
        )
    return points


def monthly_counts(commits: list[CommitInfo]) -> list[dict[str, object]]:
    buckets: dict[str, int] = defaultdict(int)
    for commit in commits:
        buckets[commit.date[:7]] += 1
    return [{"month": month, "count": buckets[month]} for month in sorted(buckets)]


def category_counts(commits: list[CommitInfo]) -> Counter[str]:
    counts: Counter[str] = Counter()
    for commit in commits:
        for category in commit.categories:
            counts[category] += 1
    return counts


def scale(value: float, in_min: float, in_max: float, out_min: float, out_max: float) -> float:
    if in_max == in_min:
        return (out_min + out_max) / 2
    return out_min + (value - in_min) * (out_max - out_min) / (in_max - in_min)


def skill_timeline_svg(commits: list[CommitInfo], milestones: list[CommitInfo]) -> str:
    width, height = 980, 300
    left, right, top, bottom = 56, 28, 28, 58
    if not commits:
        return "<svg viewBox='0 0 980 300' role='img'></svg>"
    max_skill = max(commit.skill_count for commit in commits) or 1
    points = []
    for index, commit in enumerate(commits):
        x = scale(index, 0, max(1, len(commits) - 1), left, width - right)
        y = scale(commit.skill_count, 0, max_skill, height - bottom, top)
        points.append((x, y, commit))
    point_attr = " ".join(f"{x:.1f},{y:.1f}" for x, y, _ in points)
    milestone_shas = {commit.sha for commit in milestones}
    circles = []
    for x, y, commit in points:
        if commit.sha in milestone_shas:
            circles.append(
                f"<circle cx='{x:.1f}' cy='{y:.1f}' r='6' fill='#f97316'><title>{escape(commit.date)} - {escape(commit.subject)}</title></circle>"
            )
    first_date = commits[0].date
    last_date = commits[-1].date
    grid = []
    for fraction in [0, 0.25, 0.5, 0.75, 1.0]:
        y = scale(max_skill * fraction, 0, max_skill, height - bottom, top)
        grid.append(f"<line x1='{left}' x2='{width - right}' y1='{y:.1f}' y2='{y:.1f}' stroke='#e2e8f0'/>")
        grid.append(f"<text x='14' y='{y + 4:.1f}' class='axis'>{int(max_skill * fraction)}</text>")
    return f"""
<svg viewBox="0 0 {width} {height}" role="img" aria-label="Skill count over git history">
  <defs>
    <linearGradient id="skillArea" x1="0" x2="0" y1="0" y2="1">
      <stop offset="0%" stop-color="#38bdf8" stop-opacity="0.38"/>
      <stop offset="100%" stop-color="#38bdf8" stop-opacity="0.03"/>
    </linearGradient>
  </defs>
  <rect width="{width}" height="{height}" rx="18" fill="#ffffff"/>
  {''.join(grid)}
  <polyline points="{point_attr}" fill="none" stroke="#0f766e" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>
  <polygon points="{left},{height - bottom} {point_attr} {width - right},{height - bottom}" fill="url(#skillArea)"/>
  {''.join(circles)}
  <text x="{left}" y="{height - 20}" class="axis">{escape(first_date)}</text>
  <text x="{width - right - 70}" y="{height - 20}" class="axis">{escape(last_date)}</text>
  <text x="{left}" y="22" class="chart-title">Skills over time</text>
</svg>
"""


def category_bar_svg(counts: Counter[str]) -> str:
    width = 980
    bar_height = 30
    row_gap = 14
    rows = counts.most_common(9)
    height = 80 + len(rows) * (bar_height + row_gap)
    max_count = max([count for _, count in rows], default=1)
    parts = [
        f"<svg viewBox='0 0 {width} {height}' role='img' aria-label='Commit volume by functionality area'>",
        f"<rect width='{width}' height='{height}' rx='18' fill='#ffffff'/>",
        "<text x='36' y='36' class='chart-title'>Functionality themes in commit history</text>",
    ]
    for index, (label, count) in enumerate(rows):
        y = 62 + index * (bar_height + row_gap)
        bar_width = scale(count, 0, max_count, 24, width - 380)
        hue = 185 + index * 13
        parts.append(f"<text x='36' y='{y + 21}' class='bar-label'>{escape(label)}</text>")
        parts.append(f"<rect x='330' y='{y}' width='{bar_width:.1f}' height='{bar_height}' rx='8' fill='hsl({hue}, 68%, 42%)'/>")
        parts.append(f"<text x='{350 + bar_width:.1f}' y='{y + 21}' class='bar-count'>{count}</text>")
    parts.append("</svg>")
    return "\n".join(parts)


def skill_theme_bar_svg(clusters: list[dict[str, object]]) -> str:
    width = 980
    bar_height = 30
    row_gap = 14
    rows = [(str(cluster["theme"]), int(cluster["count"])) for cluster in clusters]
    height = 80 + len(rows) * (bar_height + row_gap)
    max_count = max([count for _, count in rows], default=1)
    parts = [
        f"<svg viewBox='0 0 {width} {height}' role='img' aria-label='Skills grouped by theme'>",
        f"<rect width='{width}' height='{height}' rx='18' fill='#ffffff'/>",
        "<text x='36' y='36' class='chart-title'>Skills by theme</text>",
    ]
    for index, (label, count) in enumerate(rows):
        y = 62 + index * (bar_height + row_gap)
        bar_width = scale(count, 0, max_count, 24, width - 430)
        hue = 160 + index * 18
        parts.append(f"<text x='36' y='{y + 21}' class='bar-label'>{escape(label)}</text>")
        parts.append(f"<rect x='360' y='{y}' width='{bar_width:.1f}' height='{bar_height}' rx='8' fill='hsl({hue}, 62%, 42%)'/>")
        parts.append(f"<text x='{382 + bar_width:.1f}' y='{y + 21}' class='bar-count'>{count}</text>")
    parts.append("</svg>")
    return "\n".join(parts)


def escape(value: object) -> str:
    return html.escape(str(value), quote=True)


def compact_number(value: int) -> str:
    return f"{value:,}"


def pluralize(count: int, singular: str, plural: str | None = None) -> str:
    return singular if count == 1 else (plural or f"{singular}s")


def build_evolution_conceptual_core(
    commits: list[CommitInfo],
    milestones: list[CommitInfo],
    state: dict[str, object],
) -> dict[str, object]:
    """Explain repository evolution without treating history heuristics as proof."""
    anchors = milestones or commits
    transitions = []
    for previous, current in zip(anchors, anchors[1:]):
        transitions.append(
            {
                "from_focus": previous.categories[0] if previous.categories else "General project evolution",
                "to_focus": current.categories[0] if current.categories else "General project evolution",
                "change": current.subject,
                "evidence": {
                    "commit": current.sha[:12],
                    "date": current.date,
                },
            }
        )
    transitions = transitions[-4:]
    first_focus = (
        anchors[0].categories[0]
        if anchors and anchors[0].categories
        else "the first recorded repository state"
    )
    latest_focus = (
        anchors[-1].categories[0]
        if anchors and anchors[-1].categories
        else "the current repository state"
    )
    capability_titles = [
        str(item.get("title", ""))
        for item in state.get("key_functionality", [])
        if isinstance(item, dict) and item.get("title")
    ]
    if anchors:
        thesis = (
            f"Selected history moves from {first_focus.lower()} toward "
            f"{latest_focus.lower()}. The current tree exposes "
            f"{len(capability_titles)} evidence-backed functionality areas; "
            "the transitions below identify where the repository's emphasis changed."
        )
    else:
        thesis = (
            "No committed history is available. The current tree can still be profiled, "
            "but no evidence-backed milestone transition can be claimed."
        )
    return {
        "core_id": "project-evolution-conceptual-core",
        "report_family_id": "evolution",
        "report_kind": "evolution",
        "core_disposition": "full",
        "status": "complete" if anchors else "unavailable",
        "subject": "Repository capability evolution",
        "reasoning_mode": "historical",
        "focal_question": "Which evidenced changes explain the repository's present capability shape?",
        "supported_decision": "Which repository transitions best explain the current capability shape?",
        "thesis": thesis,
        "milestone_transitions": transitions,
        "current_capabilities": capability_titles[:5],
        "reading_strategy": (
            "Read each transition as a change in repository emphasis, then use the current-state "
            "inventory and skill themes to check whether that capability remains materialized."
        ),
        "evidence_boundary": (
            "Commit subjects and changed paths support chronology and change-surface classification. "
            "They do not prove release quality, user adoption, or the author's unstated intent."
        ),
        "source_refs": [
            f"git:{item.sha[:12]}"
            for item in anchors[-5:]
            if item.sha and item.sha != "working-tree"
        ],
        "excluded_ledger_detail": [
            "full commit log",
            "current-state metric cards",
            "exhaustive skill-theme inventory",
        ],
        "maximum_narrative_words": 320,
        "visual_pattern_policy": "report_owned_no_shared_visual_pattern",
    }


def render_html(
    repo: Path,
    state: dict[str, object],
    commits: list[CommitInfo],
    milestones: list[CommitInfo],
    chart_points: list[CommitInfo],
    conceptual_core: dict[str, object] | None = None,
) -> str:
    generated_at = datetime.now().strftime("%Y-%m-%d %H:%M")
    counts = category_counts(commits)
    conceptual_core = conceptual_core or build_evolution_conceptual_core(
        commits, milestones, state
    )
    functionality = state.get("key_functionality", [])
    functionality_cards = "\n".join(
        f"<article class='function-card'><h3>{escape(item['title'])}</h3><p>{escape(item['description'])}</p></article>"
        for item in functionality
    )
    stat_cards = [
        ("Skills", state["skills"]),
        ("Use cases", state["use_cases"]),
        ("Classes", state["classes"]),
        ("Functions", state["functions"]),
        ("Methods", state["methods"]),
        ("Prompts", state["prompts"]),
        ("Prompt lines", state["prompt_lines"]),
        ("Test files", state["test_files"]),
        ("Test cases", state["test_cases"]),
        ("Source files", state["tracked_files"]),
        ("Commits", state["commits"]),
        ("Lines of code", state["lines_of_code"]),
    ]
    stats_html = "\n".join(
        f"<div class='stat-card'><span>{escape(label)}</span><strong>{compact_number(int(value))}</strong></div>"
        for label, value in stat_cards
    )
    displayed_milestones = list(milestones)
    if chart_points and chart_points[-1].sha == "working-tree":
        displayed_milestones.append(chart_points[-1])
    skill_theme_html = "\n".join(
        f"""
        <details class="skill-theme">
          <summary>{escape(cluster['theme'])} <span>{cluster['count']} {pluralize(int(cluster['count']), 'skill')}</span></summary>
          <ul>
            {''.join(
                f"<li><a href='{escape(skill['path'])}'>{escape(skill['name'])}</a><p>{escape(skill['description'])}</p></li>"
                for skill in cluster['skills']
            )}
          </ul>
        </details>
        """
        for cluster in state.get("skill_theme_clusters", [])
    )
    monthly = monthly_counts(commits)
    month_summary = ", ".join(f"{item['month']}: {item['count']}" for item in monthly)
    transition_html = "\n".join(
        f"""
        <li>
          <span>{escape(item['evidence']['date'])}</span>
          <strong>{escape(item['from_focus'])} → {escape(item['to_focus'])}</strong>
          <p>{escape(item['change'])}</p>
          <code>{escape(item['evidence']['commit'])}</code>
        </li>
        """
        for item in conceptual_core.get("milestone_transitions", [])
    )
    if not transition_html:
        transition_html = (
            "<li class='empty-transition'><strong>No milestone transition is available.</strong>"
            "<p>The current-state inventory remains descriptive rather than historical.</p></li>"
        )
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1"/>
  <title>Project Evolution Timeline</title>
  <style>
    :root {{
      color-scheme: light;
      --ink: #172033;
      --muted: #64748b;
      --line: #dbe4ef;
      --panel: #ffffff;
      --wash: #f5f7fb;
      --accent: #0f766e;
      --hot: #f97316;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      color: var(--ink);
      background: radial-gradient(circle at 16% 6%, #dff8f2 0, transparent 32%), linear-gradient(180deg, #f8fbff, #eef3f8);
      font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      line-height: 1.5;
    }}
    main {{ max-width: 1120px; margin: 0 auto; padding: 48px 24px 72px; }}
    header {{ margin-bottom: 32px; }}
    .eyebrow {{ color: var(--accent); font-weight: 700; letter-spacing: .08em; text-transform: uppercase; font-size: 12px; }}
    h1 {{ font-size: clamp(38px, 6vw, 74px); line-height: .94; margin: 10px 0 18px; letter-spacing: 0; max-width: 900px; }}
    .lead {{ color: var(--muted); font-size: 19px; max-width: 820px; }}
    section {{ margin: 34px 0; }}
    h2 {{ font-size: 28px; margin: 0 0 18px; }}
    .stats {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(140px, 1fr)); gap: 12px; }}
    .stat-card, .function-card, .milestone, details {{
      background: rgba(255,255,255,.86);
      border: 1px solid rgba(203, 213, 225, .78);
      border-radius: 16px;
      box-shadow: 0 18px 45px rgba(15, 23, 42, .06);
    }}
    .stat-card {{ padding: 16px; min-height: 104px; }}
    .stat-card span {{ display: block; color: var(--muted); font-size: 13px; }}
    .stat-card strong {{ display: block; font-size: 31px; margin-top: 10px; }}
    .function-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 14px; }}
    .function-card {{ padding: 18px; }}
    .function-card h3 {{ margin: 0 0 8px; font-size: 18px; }}
    .function-card p {{ color: var(--muted); margin: 0; }}
    .evolution-thesis {{
      display: grid;
      grid-template-columns: minmax(240px, .9fr) minmax(360px, 1.6fr);
      gap: 30px;
      align-items: start;
      padding: 24px 0 6px;
      border-top: 1px solid rgba(15, 118, 110, .24);
    }}
    .evolution-thesis h2 {{ font-size: 34px; line-height: 1.08; margin-bottom: 12px; }}
    .evolution-thesis .thesis-copy p {{ color: #334155; font-size: 17px; }}
    .evolution-thesis .limit {{ color: var(--muted); font-size: 14px; }}
    .transition-trace {{ list-style: none; padding: 0; margin: 0; border-left: 2px solid #99d8ce; }}
    .transition-trace li {{ position: relative; padding: 0 0 24px 26px; }}
    .transition-trace li:last-child {{ padding-bottom: 0; }}
    .transition-trace li::before {{
      content: "";
      position: absolute;
      left: -7px;
      top: 5px;
      width: 12px;
      height: 12px;
      border-radius: 50%;
      background: var(--accent);
      box-shadow: 0 0 0 5px #dff8f2;
    }}
    .transition-trace span {{ display: block; color: var(--hot); font-size: 12px; font-weight: 800; }}
    .transition-trace strong {{ display: block; margin-top: 3px; }}
    .transition-trace p {{ color: var(--muted); margin: 5px 0; }}
    .transition-trace code {{ font-size: 11px; }}
    .chart-shell {{ overflow-x: auto; margin: 14px 0; }}
    svg {{ width: 100%; min-width: 680px; height: auto; display: block; border-radius: 18px; box-shadow: 0 18px 45px rgba(15, 23, 42, .06); }}
    .axis {{ font-size: 12px; fill: #64748b; }}
    .chart-title {{ font-size: 18px; font-weight: 800; fill: #172033; }}
    .bar-label {{ font-size: 14px; fill: #334155; }}
    .bar-count {{ font-size: 13px; fill: #475569; font-weight: 700; }}
    .milestones {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(230px, 1fr)); gap: 14px; }}
    .milestone {{ padding: 18px; position: relative; overflow: hidden; }}
    .milestone::before {{ content: ""; position: absolute; inset: 0 0 auto; height: 5px; background: linear-gradient(90deg, var(--accent), var(--hot)); }}
    .milestone-date {{ color: var(--hot); font-size: 13px; font-weight: 800; }}
    .milestone h3 {{ margin: 8px 0; font-size: 17px; }}
    .milestone p {{ color: var(--muted); margin: 0 0 10px; }}
    .milestone small {{ color: #475569; }}
    details {{ padding: 18px 22px; }}
    summary {{ cursor: pointer; font-weight: 800; font-size: 18px; }}
    details ol, details ul {{ margin: 18px 0 0; padding-left: 22px; max-height: 520px; overflow: auto; }}
    details li {{ margin: 8px 0; color: #334155; }}
    details summary span {{ color: var(--muted); font-size: 14px; font-weight: 700; margin-left: 8px; }}
    .skill-theme {{ margin: 12px 0; }}
    .skill-theme a {{ color: var(--accent); font-weight: 800; text-decoration: none; }}
    .skill-theme p {{ color: var(--muted); margin: 3px 0 0; }}
    code {{ background: #eef6f5; color: #0f766e; padding: 2px 5px; border-radius: 6px; }}
    footer {{ color: var(--muted); margin-top: 34px; font-size: 13px; }}
    @media (max-width: 760px) {{
      .evolution-thesis {{ grid-template-columns: 1fr; }}
    }}
  </style>
</head>
<body>
<main>
  <header>
    <div class="eyebrow">Project evolution</div>
    <h1>{escape(repo.name)} grew from workflow seed to verification system.</h1>
    <p class="lead">A git-history view of the current project state, skill growth, and the functional milestones that shaped the repository. Generated {escape(generated_at)} from committed history plus the current non-ignored working tree.</p>
  </header>

  <section class="evolution-thesis" data-conceptual-core="project-evolution">
    <div class="thesis-copy">
      <div class="eyebrow">Evidence-backed change</div>
      <h2>How the project became what it is</h2>
      <p>{escape(conceptual_core["thesis"])}</p>
      <p>{escape(conceptual_core["reading_strategy"])}</p>
      <p class="limit"><strong>Evidence limit.</strong> {escape(conceptual_core["evidence_boundary"])}</p>
    </div>
    <ol class="transition-trace">{transition_html}</ol>
  </section>

  <section>
    <h2>Current State</h2>
    <div class="stats">{stats_html}</div>
  </section>

  <section>
    <h2>What Exists Now</h2>
    <div class="function-grid">{functionality_cards}</div>
  </section>

  <section>
    <h2>Evolution Timeline</h2>
    <div class="chart-shell">{skill_timeline_svg(chart_points, displayed_milestones)}</div>
    <div class="chart-shell">{skill_theme_bar_svg(state.get("skill_theme_clusters", []))}</div>
    <div class="chart-shell">{category_bar_svg(counts)}</div>
    <p class="lead">Monthly commit cadence: {escape(month_summary)}</p>
  </section>

  <section>
    <h2>Skill Themes</h2>
    {skill_theme_html}
  </section>

  <footer>Generated by <code>proj_skills/project-evolution-timeline-reporter</code>. Figures are inline SVG; no external assets are required.</footer>
</main>
</body>
</html>
"""


def build_report(repo: Path, max_milestones: int) -> dict[str, object]:
    repo = repo.resolve()
    commits = read_commits(repo)
    milestones = select_milestones(commits, max_milestones=max_milestones)
    state = current_state(repo, commits)
    points = timeline_points(commits, state)
    conceptual_core = build_evolution_conceptual_core(commits, milestones, state)
    return {
        "repo": str(repo),
        "conceptual_core": conceptual_core,
        "current_state": state,
        "skill_theme_clusters": state["skill_theme_clusters"],
        "commits": [
            {
                "sha": commit.sha,
                "date": commit.date,
                "subject": commit.subject,
                "changed_paths": list(commit.changed_paths),
                "skill_count": commit.skill_count,
                "categories": list(commit.categories),
            }
            for commit in commits
        ],
        "milestones": [
            {
                "sha": commit.sha,
                "date": commit.date,
                "subject": commit.subject,
                "skill_count": commit.skill_count,
                "categories": list(commit.categories),
            }
            for commit in milestones
        ],
        "timeline_points": [
            {
                "sha": commit.sha,
                "date": commit.date,
                "subject": commit.subject,
                "skill_count": commit.skill_count,
                "categories": list(commit.categories),
            }
            for commit in points
        ],
        "monthly_counts": monthly_counts(commits),
        "category_counts": dict(category_counts(commits)),
        "skill_theme_counts": {
            cluster["theme"]: cluster["count"] for cluster in state["skill_theme_clusters"]
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", default=".", help="Repository root to analyze.")
    parser.add_argument("--output", required=True, help="Self-contained HTML output path.")
    parser.add_argument("--json-output", help="Optional JSON metrics output path.")
    parser.add_argument("--max-milestones", type=int, default=12, help="Maximum milestone cards before the final commit.")
    args = parser.parse_args()

    repo = Path(args.repo).resolve()
    if not (repo / ".git").exists():
        raise SystemExit(f"{repo} is not a git repository root")

    report = build_report(repo, max_milestones=args.max_milestones)
    commits = [
        CommitInfo(
            sha=item["sha"],
            date=item["date"],
            subject=item["subject"],
            changed_paths=tuple(item["changed_paths"]),
            skill_count=item["skill_count"],
            categories=tuple(item["categories"]),
        )
        for item in report["commits"]
    ]
    milestones = [
        CommitInfo(
            sha=item["sha"],
            date=item["date"],
            subject=item["subject"],
            changed_paths=(),
            skill_count=item["skill_count"],
            categories=tuple(item["categories"]),
        )
        for item in report["milestones"]
    ]
    chart_points = [
        CommitInfo(
            sha=item["sha"],
            date=item["date"],
            subject=item["subject"],
            changed_paths=(),
            skill_count=item["skill_count"],
            categories=tuple(item["categories"]),
        )
        for item in report["timeline_points"]
    ]
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    rendered_html = render_html(
        repo,
        report["current_state"],
        commits,
        milestones,
        chart_points,
        report["conceptual_core"],
    )
    output_path.write_text(
        "\n".join(line.rstrip() for line in rendered_html.splitlines()) + "\n",
        encoding="utf-8",
    )

    if args.json_output:
        json_path = Path(args.json_output)
        json_path.parent.mkdir(parents=True, exist_ok=True)
        json_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")

    print(f"Wrote {output_path}")
    if args.json_output:
        print(f"Wrote {args.json_output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
