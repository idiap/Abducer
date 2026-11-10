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
"""Generate a periodic workflow health audit report."""

from __future__ import annotations

import argparse
import html
import json
import re
import subprocess
from collections import Counter
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path


TEXT_SUFFIXES = {".py", ".md", ".yml", ".yaml", ".json", ".toml", ".txt", ".rst"}
PROMPT_SUFFIXES = {".yml", ".yaml", ".md", ".txt"}
EXCLUDED_PREFIXES = (".git/", ".venv/", "__pycache__/", "runs/")
HEALTH_DIMENSION_POSTURES = {
    "leakage": {
        "label": "Blind-run boundary",
        "posture": "heuristic_context_required",
        "interpretation": "Sensitive vocabulary identifies a boundary worth reviewing; surrounding loader behavior determines whether leakage exists.",
    },
    "orphan_skills": {
        "label": "Skill integration",
        "posture": "repository_cross_reference",
        "interpretation": "Missing catalog or hook references are observable repository facts; whether the omission is intentional still requires owner confirmation.",
    },
    "prompt_control": {
        "label": "Prompt control",
        "posture": "heuristic_control_scan",
        "interpretation": "Absent control cues suggest review but may be supplied by an external schema or caller contract.",
    },
    "mock_behavior": {
        "label": "Mock and placeholder use",
        "posture": "heuristic_marker_scan",
        "interpretation": "Mock-like tokens locate possible substitutes; they do not distinguish legitimate isolation from overclaimed validation.",
    },
    "test_coverage": {
        "label": "Deterministic coverage",
        "posture": "heuristic_reference_scan",
        "interpretation": "A missing textual test reference is a coverage lead, not proof that an execution path is untested.",
    },
}


@dataclass
class Finding:
    dimension: str
    severity: str
    path: str
    line: int
    title: str
    detail: str
    recommendation: str


def run_git(repo: Path, args: list[str]) -> str:
    return subprocess.check_output(["git", *args], cwd=repo, text=True)


def is_excluded(path: str) -> bool:
    normalized = path.replace("\\", "/")
    return any(normalized.startswith(prefix) for prefix in EXCLUDED_PREFIXES)


def tracked_files(repo: Path) -> list[str]:
    output = run_git(repo, ["ls-files", "--cached", "--others", "--exclude-standard", "-z"])
    return sorted(path for path in output.split("\0") if path and not is_excluded(path))


def read_text(repo: Path, rel_path: str) -> str:
    try:
        return (repo / rel_path).read_text(encoding="utf-8")
    except (UnicodeDecodeError, FileNotFoundError):
        return ""


def text_files(paths: list[str]) -> list[str]:
    return [path for path in paths if Path(path).suffix.lower() in TEXT_SUFFIXES]


def skill_paths(paths: list[str]) -> list[str]:
    return [
        path
        for path in paths
        if re.match(
            r"^(?:skills/[^/]+/[^/]+|proj_skills/[^/]+|prism_me/[^/]+)/SKILL\.md$",
            path,
        )
    ]


def skill_name(path: str) -> str:
    return Path(path).parent.name


def line_matches(text: str, pattern: re.Pattern[str]) -> list[tuple[int, str]]:
    return [(idx, line) for idx, line in enumerate(text.splitlines(), 1) if pattern.search(line)]


def audit_leakage(repo: Path, paths: list[str]) -> list[Finding]:
    findings: list[Finding] = []
    surfaces = [
        path
        for path in text_files(paths)
        if path.startswith("agentic/evals/")
        or path.startswith("skills/")
        or path in {"agentic/shared_runner.py", "agentic/local_complex_workflow.py"}
    ]
    leakage_re = re.compile(
        r"\b(expected[_ -]?answer|evaluation[_ -]?fixture|private[_ -]?trace|hidden[_ -]?reasoning|posthoc[_ -]?answer)\b",
        re.IGNORECASE,
    )
    posthoc_re = re.compile(r"\b(post[- ]?hoc|comparison|benchmark|reference evaluation|after generation|blind|excluded)\b", re.IGNORECASE)
    for path in surfaces:
        text = read_text(repo, path)
        for lineno, line in line_matches(text, leakage_re):
            lower_line = line.lower()
            if (
                "exclude" in lower_line
                or "must not" in lower_line
                or "do not" in lower_line
                or "keeping" in lower_line and "out" in lower_line
                or re.search(r"['\"]?(evaluation_files|expected result_files)['\"]?\s*:\s*\[\s*\]", line)
            ):
                continue
            context = "post-hoc or comparison context" if posthoc_re.search(line) else "possible generation-path exposure"
            if posthoc_re.search(line) or path.endswith(".py"):
                severity = "review"
            elif path.startswith("agentic/evals/"):
                severity = "medium"
            else:
                severity = "high"
            findings.append(
                Finding(
                    "leakage",
                    severity,
                    path,
                    lineno,
                    "scientific artifact collateral vocabulary on workflow surface",
                    f"Matched leakage-sensitive wording in {context}: {line.strip()}",
                    "Confirm this surface is post-hoc/exclusion-only, or route collateral handling behind the blind-run loader policy.",
                )
            )
    return findings


def audit_orphan_skills(repo: Path, paths: list[str]) -> list[Finding]:
    findings: list[Finding] = []
    skills = skill_paths(paths)
    docs = {
        "AGENTS.md": read_text(repo, "AGENTS.md"),
        "docs/reference/skills.md": read_text(repo, "docs/reference/skills.md"),
        "prism_me/agents.md": read_text(repo, "prism_me/agents.md"),
        "proj_skills/INDEX.md": read_text(repo, "proj_skills/INDEX.md"),
    }
    for path in skills:
        name = skill_name(path)
        is_project = path.startswith("proj_skills/")
        is_prism = path.startswith("prism_me/")
        if is_project:
            if name not in docs["proj_skills/INDEX.md"]:
                findings.append(
                    Finding(
                        "orphan_skills",
                        "high",
                        path,
                        1,
                        "Project-support skill missing from proj_skills index",
                        f"{name} is defined but not listed in proj_skills/INDEX.md.",
                        "Add the skill to the project-support index and the relevant hooked stack.",
                    )
                )
        elif is_prism:
            if name not in docs["prism_me/agents.md"]:
                findings.append(Finding("orphan_skills", "high", path, 1, "Prism skill missing from its contract", f"{name} is absent from prism_me/agents.md.", "Reconcile the Prism skill contract and coverage workflow."))
        else:
            missing = [
                surface
                for surface in ("docs/reference/skills.md",)
                if name not in docs[surface]
            ]
            if missing:
                findings.append(
                    Finding(
                        "orphan_skills",
                        "high",
                        path,
                        1,
                        "Skill missing from generated catalog surface",
                        f"{name} is absent from {', '.join(missing)}.",
                        "Regenerate the skill index/catalog or repair the skill frontmatter.",
                    )
                )
        hook_text = docs["AGENTS.md"] + "\n" + docs["prism_me/agents.md"] + "\n" + docs["proj_skills/INDEX.md"]
        if f"${name}" not in hook_text:
            findings.append(
                Finding(
                    "orphan_skills",
                    "review",
                    path,
                    1,
                    "Skill not referenced by a workflow hook",
                    f"{name} is cataloged but not explicitly hooked in AGENTS.md or proj_skills/INDEX.md.",
                    "Either hook the skill into the owning workflow stack or leave a deliberate specialization note.",
                )
            )
    return findings


def audit_prompt_control(repo: Path, paths: list[str]) -> list[Finding]:
    findings: list[Finding] = []
    prompt_paths = [
        path
        for path in paths
        if path.startswith(("skills/", "proj_skills/", "prism_me/")) and Path(path).suffix.lower() in PROMPT_SUFFIXES
    ]
    for path in prompt_paths:
        text = read_text(repo, path)
        lower = text.lower()
        nonblank_lines = [line for line in text.splitlines() if line.strip()]
        weak_dimensions = []
        if "json" not in lower and "schema" not in lower and "artifact" not in lower:
            weak_dimensions.append("output-shape control")
        source_sensitive = any(token in path for token in ("ingest", "discovery", "proof", "trace", "report", "reference"))
        if source_sensitive and not any(token in lower for token in ("source", "evidence", "blind", "artifact")):
            weak_dimensions.append("source-boundary control")
        reflective = any(token in path for token in ("meta", "review", "critic", "refine", "improvement", "feedback", "reflection"))
        if reflective and not any(token in lower for token in ("iteration", "closure", "guard", "bounded", "stop")):
            weak_dimensions.append("bounded-reflection control")
        if weak_dimensions:
            severity = "medium" if len(weak_dimensions) >= 2 else "review"
            findings.append(
                Finding(
                    "prompt_control",
                    severity,
                    path,
                    1,
                    "Prompt has weak control cues",
                    f"Missing or unclear: {', '.join(weak_dimensions)}.",
                    "Confirm the prompt is controlled by an external schema or add explicit output/source/loop constraints.",
                )
            )
        if len(nonblank_lines) > 140:
            findings.append(
                Finding(
                    "prompt_control",
                    "medium",
                    path,
                    1,
                    "Prompt is large enough to deserve control review",
                    f"{path} has {len(nonblank_lines)} nonblank lines.",
                    "Check whether the prompt should be split into staged prompts, schema contracts, or referenced policy snippets.",
                )
            )
    return findings


def classify_mock_line(line: str) -> str:
    lower = line.lower()
    if "skip" in lower or "xfail" in lower:
        return "skipped validation"
    if "todo" in lower or "placeholder" in lower:
        return "placeholder implementation"
    if "synthetic" in lower or "fixture" in lower:
        return "synthetic fixture"
    if "monkeypatch" in lower or "mock" in lower or "stub" in lower or "fake" in lower:
        return "test or dependency substitute"
    return "mock-like marker"


def audit_mock_behavior(repo: Path, paths: list[str]) -> list[Finding]:
    findings: list[Finding] = []
    mock_re = re.compile(r"\b(mock|monkeypatch|stub|fake|placeholder|synthetic|pytest\.mark\.skip|skip\(|xfail|TODO)\b", re.IGNORECASE)
    for path in text_files(paths):
        if not (path.startswith("tests/") or path.startswith("agentic/") or path.startswith("proj_skills/")):
            continue
        text = read_text(repo, path)
        for lineno, line in line_matches(text, mock_re):
            category = classify_mock_line(line)
            severity = "medium" if category in {"placeholder implementation", "skipped validation"} else "review"
            findings.append(
                Finding(
                    "mock_behavior",
                    severity,
                    path,
                    lineno,
                    category.capitalize(),
                    line.strip(),
                    "Confirm this is legitimate test isolation, or add a real-path regression / explicit limitation note.",
                )
            )
    return findings


def audit_test_coverage(repo: Path, paths: list[str]) -> list[Finding]:
    findings: list[Finding] = []
    test_text = "\n".join(
        read_text(repo, path)
        for path in paths
        if re.match(r"^tests/[^/]+/test_.*\.py$", path)
    )
    script_paths = [path for path in paths if path.startswith("proj_skills/") and "/scripts/" in path and path.endswith(".py")]
    for path in script_paths:
        stem = Path(path).stem
        parent = Path(path).parents[1].name if len(Path(path).parents) > 1 else stem
        if stem not in test_text and parent not in test_text:
            findings.append(
                Finding(
                    "test_coverage",
                    "medium",
                    path,
                    1,
                    "Project-support script lacks obvious test reference",
                    f"No direct reference to {stem} or {parent} was found in tests/**/test_*.py.",
                    "Add a deterministic test that exercises JSON output and at least one HTML marker.",
                )
            )
    workflow_files = ["agentic/shared_runner.py", "agentic/local_complex_workflow.py"]
    for path in workflow_files:
        if path in paths and Path(path).stem not in test_text:
            findings.append(
                Finding(
                    "test_coverage",
                    "review",
                    path,
                    1,
                    "Core workflow file needs coverage confirmation",
                    f"No direct stem reference for {Path(path).stem} found in test text.",
                    "Confirm coverage is indirect through runner integration tests or add focused regression labels.",
                )
            )
    return findings


def severity_counts(findings: list[Finding]) -> dict[str, int]:
    counts = Counter(finding.severity for finding in findings)
    return {key: counts.get(key, 0) for key in ("high", "medium", "review")}


def build_health_conceptual_core(findings: list[Finding]) -> dict[str, object]:
    """Calibrate audit findings as triage signals rather than verdicts."""
    severity_weight = {"high": 3, "medium": 2, "review": 1}
    dimension_readings = []
    for key, definition in HEALTH_DIMENSION_POSTURES.items():
        rows = [finding for finding in findings if finding.dimension == key]
        dimension_readings.append(
            {
                "dimension": key,
                "label": definition["label"],
                "posture": definition["posture"],
                "claim_strength": "triage_signal",
                "finding_count": len(rows),
                "priority_weight": sum(
                    severity_weight.get(finding.severity, 0) for finding in rows
                ),
                "interpretation": definition["interpretation"],
            }
        )
    ranked = sorted(
        dimension_readings,
        key=lambda item: (-int(item["priority_weight"]), str(item["dimension"])),
    )
    focus = ranked[0] if ranked and int(ranked[0]["finding_count"]) else None
    if focus:
        thesis = (
            f"The strongest current triage concentration is {str(focus['label']).lower()}. "
            "The audit combines repository cross-references with pattern-based scans, so each "
            "finding identifies where to inspect next rather than establishing a workflow defect."
        )
    else:
        thesis = (
            "The configured scans emitted no triage findings. That is evidence of a quiet scan, "
            "not proof that the workflow has no architectural or behavioral risk."
        )
    return {
        "core_id": "workflow-health-conceptual-core",
        "report_family_id": "health",
        "report_kind": "health",
        "core_disposition": "full",
        "status": "complete",
        "subject": "Workflow health triage",
        "reasoning_mode": "diagnostic_audit",
        "focal_question": "Which workflow surfaces deserve confirmation, and how strong is each signal?",
        "supported_decision": "Which triage signals deserve source confirmation before workflow changes?",
        "audit_thesis": thesis,
        "dimension_readings": dimension_readings,
        "triage_focus": focus["dimension"] if focus else "none",
        "decision_rule": (
            "Confirm the matched source context and the owning workflow contract before changing "
            "core behavior; prioritize corroborated boundary or integration defects over marker-only findings."
        ),
        "evidence_boundary": (
            "The audit reports static repository signals. It does not execute workflows, establish "
            "runtime leakage, prove missing coverage, or classify every mock as invalid."
        ),
        "excluded_ledger_detail": [
            "individual finding rows",
            "path and line inventories",
            "severity metric cards",
        ],
        "maximum_narrative_words": 320,
        "visual_pattern_policy": "report_owned_no_shared_visual_pattern",
    }


def escape(value: object) -> str:
    return html.escape(str(value), quote=True)


def render_findings(findings: list[Finding], dimension: str) -> str:
    rows = [finding for finding in findings if finding.dimension == dimension]
    if not rows:
        return "<p class='empty'>No findings for this dimension.</p>"
    items = "\n".join(
        f"""
        <li class="finding {escape(finding.severity)}">
          <div><strong>{escape(finding.title)}</strong> <span>{escape(finding.severity)}</span></div>
          <p>{escape(finding.detail)}</p>
          <code>{escape(finding.path)}:{finding.line}</code>
          <p class="rec">{escape(finding.recommendation)}</p>
        </li>
        """
        for finding in rows[:80]
    )
    more = "" if len(rows) <= 80 else f"<p class='empty'>Showing 80 of {len(rows)} findings. See JSON for the full list.</p>"
    return f"<ul class='findings'>{items}</ul>{more}"


def render_html(repo: Path, model: dict[str, object]) -> str:
    generated_at = datetime.now().strftime("%Y-%m-%d %H:%M")
    counts = model["severity_counts"]
    conceptual_core = model["conceptual_core"]
    dimensions = [
        ("leakage", "Leakage And Blind-Run Boundaries"),
        ("orphan_skills", "Orphaned Or Underhooked Skills"),
        ("prompt_control", "Prompt Control"),
        ("mock_behavior", "Mocks, Stubs, And Placeholders"),
        ("test_coverage", "Testing Coverage"),
    ]
    findings = [Finding(**item) for item in model["findings"]]
    dimension_cards = "\n".join(
        f"""
        <details open>
          <summary>{escape(title)} <span>{sum(1 for f in findings if f.dimension == key)} findings</span></summary>
          {render_findings(findings, key)}
        </details>
        """
        for key, title in dimensions
    )
    stat_cards = "\n".join(
        f"<div class='stat'><span>{escape(label)}</span><strong>{value}</strong></div>"
        for label, value in [
            ("High", counts["high"]),
            ("Medium", counts["medium"]),
            ("Review", counts["review"]),
            ("Skills", model["summary"]["skills"]),
            ("Prompts", model["summary"]["prompts"]),
            ("Scripts", model["summary"]["project_support_scripts"]),
        ]
    )
    calibration_rows = "\n".join(
        f"""
        <li>
          <div><strong>{escape(item['label'])}</strong><span>{item['finding_count']} signals</span></div>
          <p>{escape(item['interpretation'])}</p>
          <code>{escape(item['posture'])}</code>
        </li>
        """
        for item in conceptual_core["dimension_readings"]
    )
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1"/>
  <title>Workflow Health Audit</title>
  <style>
    :root {{ --ink:#172033; --muted:#64748b; --line:#dbe4ef; --accent:#0f766e; }}
    * {{ box-sizing:border-box; }}
    body {{
      margin:0; color:var(--ink);
      background: radial-gradient(circle at 16% 5%, #dff8f2 0, transparent 30%), linear-gradient(180deg, #f8fbff, #eef3f8);
      font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      line-height:1.5;
    }}
    main {{ max-width:1120px; margin:0 auto; padding:48px 24px 72px; }}
    .eyebrow {{ color:var(--accent); font-weight:800; letter-spacing:.08em; text-transform:uppercase; font-size:12px; }}
    h1 {{ font-size:clamp(40px, 6vw, 76px); line-height:.94; margin:10px 0 18px; max-width:940px; }}
    .lead {{ color:var(--muted); font-size:19px; max-width:860px; }}
    section {{ margin:34px 0; }}
    h2 {{ font-size:28px; margin:0 0 18px; }}
    .stats {{ display:grid; grid-template-columns:repeat(auto-fit, minmax(145px,1fr)); gap:12px; }}
    .stat, details {{
      background:rgba(255,255,255,.9); border:1px solid rgba(203,213,225,.82); border-radius:16px;
      box-shadow:0 18px 45px rgba(15,23,42,.06);
    }}
    .stat {{ padding:16px; min-height:104px; }}
    .stat span {{ display:block; color:var(--muted); font-size:13px; }}
    .stat strong {{ display:block; font-size:32px; margin-top:10px; }}
    .audit-reading {{
      display: grid;
      grid-template-columns: minmax(250px, .85fr) minmax(420px, 1.7fr);
      gap: 34px;
      padding: 26px 0;
      border-block: 1px solid rgba(15, 118, 110, .24);
    }}
    .audit-reading h2 {{ font-size: 34px; line-height: 1.08; }}
    .audit-reading .audit-thesis p {{ color: #334155; font-size: 16px; }}
    .audit-reading .limit {{ color: var(--muted); font-size: 13px; }}
    .calibration-rails {{ list-style: none; padding: 0; margin: 0; }}
    .calibration-rails li {{ position: relative; padding: 11px 0 13px 22px; border-bottom: 1px solid var(--line); }}
    .calibration-rails li::before {{ content: ""; position: absolute; left: 0; top: 18px; width: 9px; height: 9px; border-radius: 50%; background: #0e7490; }}
    .calibration-rails li div {{ display: flex; justify-content: space-between; gap: 18px; }}
    .calibration-rails li span {{ color: var(--muted); font-size: 12px; font-weight: 800; }}
    .calibration-rails li p {{ margin: 5px 0; color: #475569; font-size: 13px; }}
    .calibration-rails li code {{ color: #0e7490; font-size: 11px; }}
    details {{ padding:16px 20px; margin:12px 0; }}
    summary {{ cursor:pointer; display:flex; justify-content:space-between; gap:18px; font-weight:850; font-size:18px; }}
    summary span {{ color:var(--muted); font-size:13px; font-weight:750; }}
    .findings {{ list-style:none; margin:16px 0 0; padding:0; display:grid; gap:10px; }}
    .finding {{ border:1px solid var(--line); border-left-width:6px; border-radius:12px; padding:12px 14px; background:#f8fafc; }}
    .finding.high {{ border-left-color:#dc2626; }}
    .finding.medium {{ border-left-color:#d97706; }}
    .finding.review {{ border-left-color:#0e7490; }}
    .finding div {{ display:flex; justify-content:space-between; gap:12px; }}
    .finding span {{ text-transform:uppercase; color:var(--muted); font-size:11px; font-weight:850; }}
    .finding p {{ margin:6px 0; color:#334155; }}
    .finding code {{ display:inline-block; background:#eef6f5; color:#0f766e; padding:2px 5px; border-radius:6px; }}
    .rec {{ color:#475569; }}
    .empty {{ color:var(--muted); }}
    footer {{ color:var(--muted); margin-top:34px; font-size:13px; }}
    @media (max-width: 760px) {{
      .audit-reading {{ grid-template-columns: 1fr; }}
    }}
  </style>
</head>
<body>
<main>
  <header>
    <div class="eyebrow">Workflow health audit</div>
    <h1>Periodic workflow review for {escape(repo.name)}.</h1>
    <p class="lead">A diagnostic sweep for leakage boundaries, skill hook coverage, prompt control, mock behavior, and deterministic testing coverage. Generated {escape(generated_at)}.</p>
  </header>
  <section class="audit-reading" data-conceptual-core="workflow-health">
    <div class="audit-thesis">
      <div class="eyebrow">Calibrated triage</div>
      <h2>What this audit can—and cannot—tell you</h2>
      <p>{escape(conceptual_core["audit_thesis"])}</p>
      <p><strong>Decision rule.</strong> {escape(conceptual_core["decision_rule"])}</p>
      <p class="limit"><strong>Evidence limit.</strong> {escape(conceptual_core["evidence_boundary"])}</p>
    </div>
    <ul class="calibration-rails">{calibration_rows}</ul>
  </section>
  <section>
    <h2>Severity Overview</h2>
    <div class="stats">{stat_cards}</div>
  </section>
  <section>
    <h2>Findings</h2>
    {dimension_cards}
  </section>
  <footer>Generated by <code>proj_skills/workflow-health-audit-orchestrator</code>. Findings are triage signals, not automatic proof of failure.</footer>
</main>
</body>
</html>
"""


def build_model(repo: Path) -> dict[str, object]:
    paths = tracked_files(repo)
    findings: list[Finding] = []
    findings.extend(audit_leakage(repo, paths))
    findings.extend(audit_orphan_skills(repo, paths))
    findings.extend(audit_prompt_control(repo, paths))
    findings.extend(audit_mock_behavior(repo, paths))
    findings.extend(audit_test_coverage(repo, paths))
    prompts = [p for p in paths if p.startswith("skills/") and Path(p).suffix.lower() in PROMPT_SUFFIXES]
    scripts = [p for p in paths if p.startswith("proj_skills/") and "/scripts/" in p and p.endswith(".py")]
    conceptual_core = build_health_conceptual_core(findings)
    return {
        "repo": str(repo),
        "conceptual_core": conceptual_core,
        "summary": {
            "files": len(paths),
            "skills": len(skill_paths(paths)),
            "prompts": len(prompts),
            "project_support_scripts": len(scripts),
            "findings": len(findings),
        },
        "severity_counts": severity_counts(findings),
        "findings": [asdict(finding) for finding in findings],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", default=".", help="Repository root to audit.")
    parser.add_argument("--output", required=True, help="HTML output path.")
    parser.add_argument("--json-output", help="Optional JSON output path.")
    args = parser.parse_args()
    repo = Path(args.repo).resolve()
    if not (repo / ".git").exists():
        raise SystemExit(f"{repo} is not a git repository root")
    model = build_model(repo)
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    rendered_html = render_html(repo, model)
    output_path.write_text(
        "\n".join(line.rstrip() for line in rendered_html.splitlines()) + "\n",
        encoding="utf-8",
    )
    if args.json_output:
        json_path = Path(args.json_output)
        json_path.parent.mkdir(parents=True, exist_ok=True)
        json_path.write_text(json.dumps(model, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {output_path}")
    if args.json_output:
        print(f"Wrote {args.json_output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
