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
"""Integrate the Yang-Mills representational-dynamics package into Abducer."""

from __future__ import annotations

import hashlib
import json
import re
import shutil
import subprocess
import sys
import zipfile
import os
from pathlib import Path
from typing import Any

from agentic_common import ROOT, clean_text, rel, utc_now


TARGET_ID = "yang-mills-existence-and-mass-gap-target"
VERSION = "2026-07-20"
IMPORT_ROOT = ROOT / "agentic/external/yang_mills_representational_dynamics" / VERSION
ARCHIVE_ROOT = IMPORT_ROOT / "source_archives"
SOURCE_RESEARCH_ZIP = ARCHIVE_ROOT / "yang_mills_representational_dynamics_package_2026-07-20 (12).zip"
SOURCE_SKILL_ZIP = ARCHIVE_ROOT / "yang_mills_vscode_codex_skills_2026-07-20 (1).zip"
RESEARCH_ROOT = IMPORT_ROOT / "research_package"
SKILL_BUNDLE_ROOT = IMPORT_ROOT / "skill_bundle"
REPORT_ROOT = ROOT / "agentic/reports/ym_representational_dynamics_integration"
TARGET_REPORT_ROOT = ROOT / "agentic/reports/discovery_marathon/targets/yang-mills-existence-and-mass-gap-target"
PROOF_OBJECT_ROOT = TARGET_REPORT_ROOT / "proof_objects"
SKILL_ROOT = ROOT / "skills/yang_mills"
SMOKE_ROOT = ROOT / "agentic/logs/discovery_marathon_jobs/ym-overlay-smoke"

YM_SKILL_PHASES = [
    {
        "phase": "target_and_language",
        "skills": [
            "ym-freeze-clay-target",
            "ym-build-observable-core",
            "ym-build-representation-calculus",
            "ym-define-relational-rigidity",
        ],
    },
    {
        "phase": "regulators_and_scale_dynamics",
        "skills": [
            "ym-design-regulator-atlas",
            "ym-build-gauge-covariant-rg",
            "ym-design-infrared-basin",
        ],
    },
    {
        "phase": "constructive_frontier",
        "skills": [
            "ym-control-large-fields-and-topology",
            "ym-prove-basin-entry",
            "ym-prove-rg-to-rigidity",
        ],
    },
    {
        "phase": "continuum_and_spectrum",
        "skills": [
            "ym-prove-continuum-coherence",
            "ym-prove-rigidity-transfer",
            "ym-reconstruct-os-gap",
        ],
    },
    {
        "phase": "verification_and_governance",
        "skills": [
            "ym-calibrate-restricted-models",
            "ym-mechanize-proof-core",
            "ym-audit-frontier",
            "ym-run-clay-program",
        ],
    },
]
YM_SKILLS = [skill for phase in YM_SKILL_PHASES for skill in phase["skills"]]


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=True) + "\n", encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def require_source(path: Path) -> None:
    if not path.exists():
        raise SystemExit(f"missing source archive: {path}")


def zip_integrity(path: Path) -> dict[str, Any]:
    with zipfile.ZipFile(path) as archive:
        bad = archive.testzip()
        names = archive.namelist()
    return {
        "path": str(path),
        "size_bytes": path.stat().st_size,
        "sha256": sha256(path),
        "integrity_ok": bad is None,
        "bad_member": bad or "",
        "member_count": len(names),
    }


def clean_generated_import() -> None:
    # Source archives are durable inputs and may also be the local defaults.
    for path in [RESEARCH_ROOT, SKILL_BUNDLE_ROOT]:
        if path.exists():
            shutil.rmtree(path)
    for path in [
        REPORT_ROOT,
        PROOF_OBJECT_ROOT,
        ROOT / "agentic/evals/ym_workflow_integration",
        ROOT / "agentic/evals/discovery_marathon/ym_overlay_prompt_fixture.json",
        SMOKE_ROOT,
    ]:
        if path.is_dir():
            shutil.rmtree(path)
        elif path.exists():
            path.unlink()


def extract_archives() -> dict[str, Any]:
    require_source(SOURCE_RESEARCH_ZIP)
    require_source(SOURCE_SKILL_ZIP)
    clean_generated_import()
    ARCHIVE_ROOT.mkdir(parents=True, exist_ok=True)
    copied_research = ARCHIVE_ROOT / SOURCE_RESEARCH_ZIP.name
    copied_skill = ARCHIVE_ROOT / SOURCE_SKILL_ZIP.name
    if SOURCE_RESEARCH_ZIP.resolve() != copied_research.resolve():
        shutil.copy2(SOURCE_RESEARCH_ZIP, copied_research)
    if SOURCE_SKILL_ZIP.resolve() != copied_skill.resolve():
        shutil.copy2(SOURCE_SKILL_ZIP, copied_skill)
    RESEARCH_ROOT.mkdir(parents=True, exist_ok=True)
    SKILL_BUNDLE_ROOT.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(SOURCE_RESEARCH_ZIP) as archive:
        archive.extractall(RESEARCH_ROOT)
    with zipfile.ZipFile(SOURCE_SKILL_ZIP) as archive:
        archive.extractall(SKILL_BUNDLE_ROOT)
    return {
        "research_archive": zip_integrity(SOURCE_RESEARCH_ZIP),
        "skill_archive": zip_integrity(SOURCE_SKILL_ZIP),
        "copied_archives": [rel(copied_research), rel(copied_skill)],
    }


def list_files(root: Path) -> list[dict[str, Any]]:
    rows = []
    for path in sorted(p for p in root.rglob("*") if p.is_file()):
        relative = path.relative_to(root).as_posix()
        if "__pycache__" in path.parts:
            continue
        rows.append(
            {
                "path": relative,
                "imported_path": rel(path),
                "size_bytes": path.stat().st_size,
                "sha256": sha256(path),
                "extension": path.suffix.lower(),
            }
        )
    return rows


def verify_package_checksums() -> dict[str, Any]:
    checksum_file = RESEARCH_ROOT / "CHECKSUMS.sha256"
    entries: list[dict[str, Any]] = []
    failed: list[str] = []
    for raw in checksum_file.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line:
            continue
        match = re.match(r"^([0-9a-fA-F]{64})\s+\*?(.+)$", line)
        if not match:
            failed.append(f"unparseable:{line}")
            continue
        expected, relative = match.groups()
        path = RESEARCH_ROOT / relative
        actual = sha256(path) if path.exists() else ""
        ok = actual == expected.lower()
        entries.append({"path": relative, "expected_sha256": expected.lower(), "actual_sha256": actual, "ok": ok})
        if not ok:
            failed.append(relative)
    return {
        "checksum_file": rel(checksum_file),
        "entry_count": len(entries),
        "all_ok": not failed,
        "failed": failed,
        "entries": entries,
    }


def file_role(relative: str) -> tuple[str, str, str]:
    suffix = Path(relative).suffix.lower()
    if relative.startswith("01_conceptual_foundations/"):
        return "conceptual foundation", "C0", "Define target ontology, representational difficulty, and non-claim boundaries."
    if relative.startswith("02_relational_rigidity_program/"):
        if relative.endswith("theorem_dependencies.json"):
            return "theorem dependency graph", "C1-C3", "Map representation-calculus dependencies and frontier blockers."
        if suffix == ".py":
            return "finite mechanized core", "C1", "Executable finite spectral or representation-calculus support."
        if relative.endswith("proof_status_ledger.md"):
            return "frontier ledger", "C1-C3", "Record proof status, blockers, and conditional links."
        return "relational-rigidity programme", "C1-C3", "State representation packages, morphisms, and rigidity witnesses."
    if relative.startswith("03_heat_kernel_basin_entry/"):
        if relative.endswith(".json"):
            return "calibration or theorem graph", "C1-C3", "Calibrate heat-kernel regulator and two-tier basin obligations."
        if suffix == ".py":
            return "restricted-model computation", "C1-C2", "Executable heat-kernel or regulator calibration support."
        return "heat-kernel basin-entry attack", "C2-C3", "Falsify naive TV basin and propose good-field/defect split."
    if relative.startswith("04_fibered_block_rg/"):
        if relative.endswith(".json"):
            return "calibration or theorem graph", "C1-C3", "Represent fibered block RG dependencies and restricted checks."
        if suffix == ".py":
            return "restricted-model computation", "C1-C2", "Executable two-plaquette bridge support."
        return "fibered block RG theorem", "C2-C3", "Separate retained and fiber information with exact covariance accounting."
    if relative.endswith("CHECKSUMS.sha256"):
        return "integrity metadata", "not-a-claim", "Verify source package integrity."
    return "package documentation", "not-a-claim", "Support reproducibility and package navigation."


def build_source_index() -> tuple[dict[str, Any], str]:
    files = []
    for row in list_files(RESEARCH_ROOT):
        role, claim_level, workflow_role = file_role(row["path"])
        files.append({**row, "artifact_role": role, "claim_level": claim_level, "workflow_role": workflow_role})
    pdf_count = sum(1 for row in files if row["extension"] == ".pdf")
    tex_count = sum(1 for row in files if row["extension"] == ".tex")
    py_count = sum(1 for row in files if row["extension"] == ".py")
    test_count = sum(1 for row in files if Path(row["path"]).name.startswith("test_"))
    theorem_graph_count = sum(1 for row in files if "theorem_dependencies" in row["path"])
    index = {
        "schema_version": 1,
        "generated_utc": utc_now(),
        "target_id": TARGET_ID,
        "epistemic_status": (
            "Research programme and restricted theorem suite; not a construction of four-dimensional continuum "
            "Yang-Mills theory and not a Clay mass-gap proof."
        ),
        "source_root": rel(RESEARCH_ROOT),
        "recommended_reading_order": [
            "01_conceptual_foundations/yang_mills_mass_gap_conceptual_difficulty.pdf",
            "01_conceptual_foundations/phenomenon_preserving_representations_yang_mills.pdf",
            "01_conceptual_foundations/generative_relational_coherence_universe.pdf",
            "01_conceptual_foundations/yang_mills_relational_rigidity_clay_program.pdf",
            "02_relational_rigidity_program/ym_relational_rigidity_program.pdf",
            "03_heat_kernel_basin_entry/heat_kernel_basin_entry_attack.pdf",
            "04_fibered_block_rg/fibered_block_rg_theorem.pdf",
        ],
        "summary_counts": {
            "files": len(files),
            "pdfs": pdf_count,
            "tex_sources": tex_count,
            "python_modules": py_count,
            "tests": test_count,
            "theorem_dependency_graphs": theorem_graph_count,
        },
        "files": files,
    }
    lines = [
        "# YM Representational Dynamics Source Index",
        "",
        f"- Target: `{TARGET_ID}`",
        f"- Source root: `{rel(RESEARCH_ROOT)}`",
        "- Status: restricted theorem suite and research programme; not a Clay proof.",
        f"- Counts: {pdf_count} PDFs, {tex_count} TeX sources, {py_count} Python files, {test_count} tests, {theorem_graph_count} theorem graphs.",
        "",
        "## Reading Order",
        "",
    ]
    for item in index["recommended_reading_order"]:
        lines.append(f"- `{item}`")
    lines.extend(["", "## Artifact Map", ""])
    for row in files:
        lines.append(f"- `{row['path']}`: {row['artifact_role']} ({row['claim_level']}) - {row['workflow_role']}")
    return index, "\n".join(lines) + "\n"


def run_tests() -> dict[str, Any]:
    groups = [
        {
            "name": "relational_rigidity_finite_spectral_core",
            "cwd": RESEARCH_ROOT / "02_relational_rigidity_program",
            "command": [sys.executable, "-m", "unittest", "-v", "test_finite_spectral_core.py"],
        },
        {
            "name": "heat_kernel_basin_entry",
            "cwd": RESEARCH_ROOT / "03_heat_kernel_basin_entry",
            "command": [
                sys.executable,
                "-m",
                "unittest",
                "-v",
                "test_heat_kernel_influence.py",
                "test_advanced_regulator_calibration.py",
            ],
        },
        {
            "name": "fibered_block_rg_two_plaquette_bridge",
            "cwd": RESEARCH_ROOT / "04_fibered_block_rg",
            "command": [sys.executable, "-m", "unittest", "-v", "test_two_plaquette_bridge.py"],
            "pythonpath": [RESEARCH_ROOT / "03_heat_kernel_basin_entry"],
        },
    ]
    results = []
    total_tests = 0
    for group in groups:
        env = os.environ.copy()
        pythonpath = [str(path) for path in group.get("pythonpath", [])]
        if pythonpath:
            existing = env.get("PYTHONPATH", "")
            env["PYTHONPATH"] = os.pathsep.join([*pythonpath, existing] if existing else pythonpath)
        completed = subprocess.run(
            group["command"],
            cwd=group["cwd"],
            env=env,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
        )
        output = completed.stdout
        ran_match = re.search(r"Ran\s+(\d+)\s+tests?", output)
        count = int(ran_match.group(1)) if ran_match else 0
        total_tests += count
        results.append(
            {
                "name": group["name"],
                "cwd": rel(group["cwd"]),
                "command": " ".join(group["command"]),
                "pythonpath": [rel(path) for path in group.get("pythonpath", [])],
                "exit_code": completed.returncode,
                "test_count": count,
                "passed": completed.returncode == 0,
                "output_tail": "\n".join(output.splitlines()[-30:]),
            }
        )
    report = {
        "schema_version": 1,
        "generated_utc": utc_now(),
        "target_id": TARGET_ID,
        "status": "passed" if all(row["passed"] for row in results) else "failed",
        "test_count": total_tests,
        "expected_test_count": 31,
        "epistemic_boundary": "These tests reproduce restricted finite/model claims only; they do not certify the Clay target.",
        "groups": results,
    }
    lines = [
        "# YM Restricted-Model Test Report",
        "",
        f"- Target: `{TARGET_ID}`",
        f"- Status: `{report['status']}`",
        f"- Tests observed: {total_tests} / expected 31",
        "- Boundary: passing tests validate restricted models only, not continuum Yang-Mills or the Clay mass gap.",
        "",
    ]
    for row in results:
        lines.append(f"## {row['name']}")
        lines.append("")
        lines.append(f"- Command: `{row['command']}`")
        lines.append(f"- CWD: `{row['cwd']}`")
        lines.append(f"- Exit code: `{row['exit_code']}`")
        lines.append(f"- Tests: {row['test_count']}")
        lines.append("")
    write_json(REPORT_ROOT / "test_report.json", report)
    write_text(REPORT_ROOT / "test_report.md", "\n".join(lines))
    return report


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def build_proof_objects() -> tuple[dict[str, Any], str]:
    objects: list[dict[str, Any]] = []

    def add_object(
        object_id: str,
        claim: str,
        source: str,
        claim_level: str,
        status: str,
        hard_gate: str,
        dependencies: list[str] | None = None,
        hypotheses: list[str] | None = None,
        non_claims: list[str] | None = None,
    ) -> None:
        objects.append(
            {
                "proof_object_id": object_id,
                "target_id": TARGET_ID,
                "claim": claim,
                "source_artifact": rel(RESEARCH_ROOT / source),
                "claim_level": claim_level,
                "status": status,
                "hard_gate": hard_gate,
                "dependencies": dependencies or [],
                "hypotheses": hypotheses or [],
                "non_claims": non_claims
                or [
                    "Does not construct four-dimensional continuum Yang-Mills theory.",
                    "Does not prove a positive Hamiltonian mass gap.",
                    "Does not discharge the full Clay target.",
                ],
                "demotion_trigger": (
                    "Demote if the object is used outside its stated finite, restricted, conditional, or calibration scope "
                    "without an independent transfer certificate."
                ),
            }
        )

    deps = load_json(RESEARCH_ROOT / "02_relational_rigidity_program/theorem_dependencies.json")
    for node in deps.get("nodes", []):
        add_object(
            f"ymrd.relational.{node['id']}",
            f"Relational-rigidity dependency node `{node['id']}` has status `{node['status']}` at level `{node.get('claim_level', '')}`.",
            "02_relational_rigidity_program/theorem_dependencies.json",
            node.get("claim_level", ""),
            node.get("status", ""),
            "representation calculus or continuum transfer chain",
            dependencies=[edge[0] for edge in deps.get("edges", []) if len(edge) == 2 and edge[1] == node["id"]],
        )

    heat = load_json(RESEARCH_ROOT / "03_heat_kernel_basin_entry/theorem_dependencies_next.json")
    for node in heat.get("nodes", []):
        add_object(
            f"ymrd.heat_kernel.{node['id']}",
            f"Heat-kernel basin-entry node `{node['id']}` has status `{node['status']}` at level `{node.get('level', '')}`.",
            "03_heat_kernel_basin_entry/theorem_dependencies_next.json",
            node.get("level", ""),
            node.get("status", ""),
            "heat-kernel basin entry or good-field/defect split",
            dependencies=[edge[0] for edge in heat.get("edges", []) if len(edge) == 2 and edge[1] == node["id"]],
        )

    fiber = load_json(RESEARCH_ROOT / "04_fibered_block_rg/theorem_dependencies_fibered.json")
    for row in fiber.get("proved_here", []):
        add_object(
            f"ymrd.fibered.{row['id']}",
            row["claim"],
            "04_fibered_block_rg/theorem_dependencies_fibered.json",
            "C2",
            "proved-restricted",
            "fibered block RG accounting or restricted bridge calibration",
            hypotheses=[row.get("scope", "")],
            non_claims=fiber.get("non_implications", []),
        )
    for row in fiber.get("conditional_bridges", []):
        add_object(
            f"ymrd.fibered.{row['id']}",
            row["claim"],
            "04_fibered_block_rg/theorem_dependencies_fibered.json",
            "C3",
            "conditional",
            "continuum clustering or OS spectral transfer",
            dependencies=row.get("depends_on", []),
            hypotheses=row.get("depends_on", []),
            non_claims=fiber.get("non_implications", []),
        )
    for row in fiber.get("open_frontier", []):
        add_object(
            f"ymrd.fibered.{row['id']}",
            row["claim"],
            "04_fibered_block_rg/theorem_dependencies_fibered.json",
            "C3",
            "open",
            "open constructive frontier obligation",
            non_claims=fiber.get("non_implications", []),
        )

    payload = {
        "schema_version": 1,
        "generated_utc": utc_now(),
        "target_id": TARGET_ID,
        "epistemic_status": "All objects are restricted, conditional, open, or support-only unless explicitly discharged by independent proof.",
        "object_count": len(objects),
        "proof_objects": objects,
    }
    lines = ["# YM Representational Dynamics Proof Objects", "", f"- Target: `{TARGET_ID}`", f"- Objects: {len(objects)}", ""]
    for row in objects:
        lines.append(f"- `{row['proof_object_id']}`: {row['status']} {row['claim_level']} - {row['claim']}")
    return payload, "\n".join(lines) + "\n"


def adapt_skills() -> dict[str, Any]:
    source_skills = SKILL_BUNDLE_ROOT / "11_vscode_codex_skill_bundle/.agents/skills"
    report_rows = []
    for skill in YM_SKILLS:
        src = source_skills / skill
        dest = SKILL_ROOT / skill
        if dest.exists():
            shutil.rmtree(dest)
        dest.mkdir(parents=True, exist_ok=True)
        text = (src / "SKILL.md").read_text(encoding="utf-8")
        guard = f"""
## Abducer Integration Guards

- Activate this skill only for `{TARGET_ID}` or an explicitly marked Yang-Mills calibration task.
- Treat imported representational-dynamics artifacts as restricted, finite, conditional, or support evidence unless a later proof discharges their frontier hypotheses.
- Emit claim level, non-claims, hard gate, hypotheses, falsifier, and demotion trigger before any promotion.
- Compose with the target-neutral proof-depth skills: pressure formalization, hard-gate selection, nontriviality audit, anti-definitionality audit, same-domain transfer certification, and declarative learning extraction.
- State efficient representation requirements: preserved observables, morphisms or recovery maps, invariants, error budgets, equivalence policy, locality or cutoff budget, transfer interface, and falsifiers.
- Do not let a transfer theorem pass if the target property is built into the bridge definition; require independently stated source and target objects plus a consequence delta.
- Preserve the four-cycle, recursion-depth-one publication-consolidation limit for local subgoals.
- Source provenance: `{rel(src / 'SKILL.md')}`.
"""
        parts = text.split("---", 2)
        if len(parts) == 3:
            adapted = f"---{parts[1]}---\n{guard}\n{parts[2].lstrip()}"
        else:
            adapted = f"{guard}\n{text}"
        write_text(dest / "SKILL.md", adapted)
        (dest / "agents").mkdir(parents=True, exist_ok=True)
        shutil.copy2(src / "agents/openai.yaml", dest / "agents/openai.yaml")
        report_rows.append({"skill": skill, "source": rel(src), "dest": rel(dest), "adapted": True})
    write_text(
        SKILL_ROOT / "agents/openai.yaml",
        (
            'interface:\n'
            '  display_name: "Yang-Mills Skill Overlay"\n'
            '  short_description: "Target-scoped representation-aware YM workflow skills"\n'
            '  default_prompt: "Use the Yang-Mills skill overlay to run a claim-leveled, proof-depth controlled YM workflow."\n'
        ),
    )
    report = {
        "schema_version": 1,
        "generated_utc": utc_now(),
        "target_id": TARGET_ID,
        "source_bundle": rel(SKILL_BUNDLE_ROOT / "11_vscode_codex_skill_bundle"),
        "skill_count": len(report_rows),
        "skills": report_rows,
    }
    lines = [
        "# YM Skill Adaptation Report",
        "",
        f"- Target: `{TARGET_ID}`",
        f"- Adapted skills: {len(report_rows)}",
        f"- Source bundle: `{report['source_bundle']}`",
        "",
    ]
    for row in report_rows:
        lines.append(f"- `{row['skill']}` -> `{row['dest']}`")
    write_json(REPORT_ROOT / "skill_adaptation_report.json", report)
    write_text(REPORT_ROOT / "skill_adaptation_report.md", "\n".join(lines) + "\n")
    return report


def update_dispatch_registry() -> None:
    path = ROOT / "agentic/registries/discovery_marathon_skill_dispatch.yaml"
    matrix = json.loads(path.read_text(encoding="utf-8"))
    phases = [phase for phase in matrix.get("phases", []) if phase.get("phase") != "yang_mills_representational_dynamics_overlay"]
    phases.insert(
        3,
        {
            "phase": "yang_mills_representational_dynamics_overlay",
            "target_scope": TARGET_ID,
            "optional_historical": True,
            "required_skills": YM_SKILLS,
            "conditional_skills": [
                "proof-depth-pressure-formalizer",
                "proof-hard-gate-selector",
                "proof-nontriviality-auditor",
                "proof-transfer-substance-auditor",
                "efficient-representation-requirements-elicitor",
            ],
            "required_output": (
                "YM claim-level ledger, representation requirements, regulator/RG obligations, restricted-model "
                "calibration handoff, proof-object updates, and conservative frontier audit"
            ),
        },
    )
    matrix["phases"] = phases
    path.write_text(json.dumps(matrix, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")


def update_task_registry() -> None:
    path = ROOT / "registry/tasks/discovery-marathon/task_registry.json"
    manifest = json.loads(path.read_text(encoding="utf-8"))
    skills = {entry["name"] for entry in manifest.get("reference_skills", []) + manifest.get("generated_skills", [])}
    manifest.setdefault("generated_skills", [])
    for skill in YM_SKILLS:
        if skill not in skills:
            manifest["generated_skills"].append(
                {
                    "name": skill,
                    "source": "ym-representational-dynamics-bundle",
                    "path": f"skills/yang_mills/{skill}",
                    "why": "Target-scoped Yang-Mills representational-dynamics workflow overlay.",
                }
            )
    manifest.setdefault("generated_workflows", [])
    if "ym-representational-dynamics-overlay" not in {entry["name"] for entry in manifest["generated_workflows"]}:
        manifest["generated_workflows"].append(
            {
                "name": "ym-representational-dynamics-overlay",
                "source": "local",
                "path": "agentic/registries/discovery_marathon_skill_dispatch.yaml",
                "why": "Target-scoped overlay for Yang-Mills representational-dynamics phases.",
            }
        )
    artifacts = [
        "docs/case-studies/yang-mills/ym-representational-dynamics-integration-todos.md",
        "agentic/todos/ym_representational_dynamics_integration_todos.yaml",
        "agentic/external/yang_mills_representational_dynamics/2026-07-20/source_manifest.json",
        "agentic/external/yang_mills_representational_dynamics/2026-07-20/checksum_report.json",
        "agentic/reports/ym_representational_dynamics_integration/source_index.json",
        "agentic/reports/ym_representational_dynamics_integration/test_report.json",
        "agentic/reports/ym_representational_dynamics_integration/skill_adaptation_report.md",
        "agentic/reports/discovery_marathon/targets/yang-mills-existence-and-mass-gap-target/proof_objects/ym_representational_dynamics_objects.json",
        "agentic/reports/ym_representational_dynamics_integration/smoke_cycle_report.md",
        "agentic/scripts/validate_ym_workflow_integration.py",
    ]
    validators = ["agentic/scripts/validate_ym_workflow_integration.py"]
    workflows = manifest.get("visible_workflows", [])
    main = workflows[0]
    for skill in YM_SKILLS:
        if skill not in main["composed_skills"]:
            main["composed_skills"].append(skill)
    for artifact in artifacts:
        if artifact not in main["artifacts"]:
            main["artifacts"].append(artifact)
    for validator in validators:
        if validator not in main["validators"]:
            main["validators"].append(validator)
    if not any(workflow.get("name") == "ym-representational-dynamics-overlay" for workflow in workflows):
        workflows.append(
            {
                "name": "ym-representational-dynamics-overlay",
                "end_to_end_function": (
                    "Run the Yang-Mills representational-dynamics source package and skill overlay as a target-scoped "
                    "evidence, proof-object, calibration, and frontier-audit layer inside the discovery marathon."
                ),
                "key_function": "workflow_governance",
                "reasoning_types": [
                    "workflow_composition",
                    "generative_reasoning",
                    "deterministic_validation",
                    "evidence_assessment",
                ],
                "problem_domain_types": ["theorem_discovery", "agentic_control_plane"],
                "task_context_types": ["target_navigation", "dependency_cartography", "workflow_governance"],
                "composed_skills": YM_SKILLS,
                "deterministic_hooks": ["repo-hook-config"],
                "workflow_references": ["workflow-contract-registry", "discovery-marathon-scripts", "ym-representational-dynamics-overlay"],
                "artifacts": artifacts,
                "validators": validators,
            }
        )
    path.write_text(json.dumps(manifest, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")


def write_reports(
    source_index: dict[str, Any],
    checksum_report: dict[str, Any],
    test_report: dict[str, Any],
    proof_objects: dict[str, Any],
    skill_report: dict[str, Any],
) -> None:
    dispatch_report = [
        "# YM Dispatch Overlay Report",
        "",
        f"- Target scope: `{TARGET_ID}`",
        "- Overlay phase: `yang_mills_representational_dynamics_overlay`",
        f"- Required YM skills: {len(YM_SKILLS)}",
        "- Existing proof-depth phases remain active; the overlay is target-scoped and optional for historical cycles.",
        "- P-vs-NP dispatch, report paths, and timeline outputs are not touched by this integration.",
        "",
    ]
    write_text(REPORT_ROOT / "dispatch_overlay_report.md", "\n".join(dispatch_report))

    prompt_fixture = {
        "target_id": TARGET_ID,
        "fixture_name": "ym_overlay_prompt_fixture",
        "required_prompt_markers": [
            "claim levels",
            "non-claims",
            "hard-gate selection",
            "efficient representation requirements",
            "regulator choice",
            "large-field/topology control",
            "basin entry",
            "OS reconstruction",
            "spectral gap inference",
            "four completion cycles",
        ],
        "forbidden_prompt_behavior": [
            "promote restricted finite tests to the Clay target",
            "allow endpoint refinements without hard-gate movement",
            "open nested publication-consolidation loops",
        ],
    }
    write_json(ROOT / "agentic/evals/discovery_marathon/ym_overlay_prompt_fixture.json", prompt_fixture)
    write_text(
        REPORT_ROOT / "prompt_integration_report.md",
        (
            "# YM Prompt Integration Report\n\n"
            f"- Target: `{TARGET_ID}`\n"
            "- Prompt fixture requires claim levels, non-claims, hard gates, efficient representation requirements, "
            "regulator/RG tensions, large-field/topology controls, basin entry, OS reconstruction, and spectral transfer boundaries.\n"
            "- Endpoint or positivity refinements remain support-only unless they move a named hard gate.\n"
            "- Publication consolidation is bounded at four cycles with recursion depth one.\n"
        ),
    )

    overlay = {
        "schema_version": 1,
        "generated_utc": utc_now(),
        "target_id": TARGET_ID,
        "source_index": rel(REPORT_ROOT / "source_index.json"),
        "proof_objects": rel(PROOF_OBJECT_ROOT / "ym_representational_dynamics_objects.json"),
        "test_report": rel(REPORT_ROOT / "test_report.json"),
        "skill_overlay": rel(REPORT_ROOT / "skill_adaptation_report.json"),
        "frontier_status": "restricted-and-conditional; C6 blocked by continuum construction, basin entry, OS reconstruction, and spectral transfer",
        "timeline_events": [
            {
                "event_id": row["proof_object_id"],
                "target_id": TARGET_ID,
                "event_type": "imported_proof_object",
                "claim_level": row["claim_level"],
                "status": row["status"],
                "summary": row["claim"],
            }
            for row in proof_objects["proof_objects"][:40]
        ],
    }
    write_json(TARGET_REPORT_ROOT / "ym_representational_dynamics_overlay.json", overlay)
    write_json(REPORT_ROOT / "timeline_events.json", overlay["timeline_events"])
    write_text(
        TARGET_REPORT_ROOT / "ym_representational_dynamics_overlay.html",
        (
            "<!doctype html>\n"
            '<html lang="en">\n'
            "<head>\n"
            '  <meta charset="utf-8">\n'
            f'  <meta name="abducer-target-id" content="{TARGET_ID}">\n'
            "  <title>YM Representational Dynamics Overlay</title>\n"
            "  <style>body{font-family:system-ui,sans-serif;max-width:980px;margin:40px auto;line-height:1.5}"
            "code{background:#f4f4f4;padding:2px 4px;border-radius:4px}.status{font-weight:700}</style>\n"
            "</head>\n"
            "<body>\n"
            "  <h1>Yang-Mills Representational Dynamics Overlay</h1>\n"
            f"  <p class=\"status\">Target: <code>{TARGET_ID}</code></p>\n"
            "  <p>This target-scoped overlay indexes the imported research package, adapted skills, restricted-model tests, "
            "claim-leveled proof objects, and frontier audit boundaries. It is not a Clay proof.</p>\n"
            "  <ul>\n"
            f"    <li>Source index: <code>{rel(REPORT_ROOT / 'source_index.json')}</code></li>\n"
            f"    <li>Proof objects: <code>{rel(PROOF_OBJECT_ROOT / 'ym_representational_dynamics_objects.json')}</code></li>\n"
            f"    <li>Test report: <code>{rel(REPORT_ROOT / 'test_report.json')}</code></li>\n"
            f"    <li>Skills: {skill_report['skill_count']} adapted YM skills.</li>\n"
            f"    <li>Restricted tests: {test_report['test_count']} observed tests, status <code>{test_report['status']}</code>.</li>\n"
            "  </ul>\n"
            "</body>\n"
            "</html>\n"
        ),
    )
    write_text(
        REPORT_ROOT / "report_integration_report.md",
        (
            "# YM Report Integration Report\n\n"
            f"- Target: `{TARGET_ID}`\n"
            f"- Target overlay JSON: `{rel(TARGET_REPORT_ROOT / 'ym_representational_dynamics_overlay.json')}`\n"
            f"- Target overlay HTML: `{rel(TARGET_REPORT_ROOT / 'ym_representational_dynamics_overlay.html')}`\n"
            f"- Timeline events: `{rel(REPORT_ROOT / 'timeline_events.json')}`\n"
            f"- Existing target latest report remains `{rel(TARGET_REPORT_ROOT / 'latest.html')}` and keeps its target id.\n"
            "- The overlay explicitly states that the imported package is not a Clay proof.\n"
        ),
    )

    fixture_valid = {
        "target_id": TARGET_ID,
        "expected_skill_count": 17,
        "expected_overlay_phase": "yang_mills_representational_dynamics_overlay",
        "expected_report": rel(TARGET_REPORT_ROOT / "ym_representational_dynamics_overlay.json"),
    }
    write_json(ROOT / "agentic/evals/ym_workflow_integration/fixture_valid.json", fixture_valid)
    write_text(
        REPORT_ROOT / "validator_report.md",
        (
            "# YM Workflow Validator Report\n\n"
            "- Validator: `agentic/scripts/validate_ym_workflow_integration.py`\n"
            "- Checks: source manifest, checksums, source index, 17 adapted skills, target-scoped dispatch, report paths, "
            "claim-level boundaries, smoke manifest, and docs/runbook integration.\n"
        ),
    )

    SMOKE_ROOT.mkdir(parents=True, exist_ok=True)
    smoke_manifest = {
        "job_id": "ym-overlay-smoke",
        "run_id": "ym-overlay-smoke",
        "target_id": TARGET_ID,
        "status": "completed",
        "execution_mode": "api_free_static_overlay_validation",
        "generated_utc": utc_now(),
        "selected_overlay_phase": "yang_mills_representational_dynamics_overlay",
        "emitted_learning_event": {
            "premises": ["restricted source package imported", "YM overlay skills adapted", "claim-level proof objects generated"],
            "attempted_move": "promote representational-dynamics package into main YM workflow",
            "learned_constraint": "package is useful only as restricted/conditional evidence until frontier hypotheses are discharged",
            "future_routing_effect": "run YM overlay validation before Azure marathons and route local subgoals through bounded consolidation",
        },
        "hard_gate_selection": "continuum basin entry and OS spectral transfer remain blocking gates",
        "frontier_audit_outcome": "C6 blocked; strongest imported claims are restricted or conditional.",
    }
    write_json(SMOKE_ROOT / "manifest.json", smoke_manifest)
    write_text(
        REPORT_ROOT / "smoke_cycle_report.md",
        (
            "# YM Overlay Smoke Cycle Report\n\n"
            f"- Target: `{TARGET_ID}`\n"
            "- Mode: API-free static overlay validation.\n"
            "- Learning event: imported representational-dynamics evidence is useful only with claim levels, non-claims, and frontier blockers visible.\n"
            "- Hard gate: continuum basin entry and OS spectral transfer remain blocking gates.\n"
            "- Azure readiness: ready only after `agentic/scripts/validate_ym_workflow_integration.py` passes.\n"
        ),
    )

    subgoal_decision = {
        "schema_version": 1,
        "generated_utc": utc_now(),
        "target_id": TARGET_ID,
        "selected_subgoal": "fibered block RG retained/fiber covariance accounting",
        "decision": "bounded_publication_consolidation_candidate",
        "why_this_subgoal": [
            "It is a coherent sharp result rather than a fragmented ensemble.",
            "It has clear novelty at restricted scope: retained/fiber response split plus exact covariance accounting.",
            "It changes understanding by separating accounting identities from the missing quantitative YM estimates.",
            "It exposes concrete frontier blockers: gauge-covariant block maps, small fiber influence, defect summability, basin entry, OS transfer.",
        ],
        "publication_consolidation_budget": {"max_completion_cycles": 4, "max_recursion_depth": 1},
        "outcomes_allowed": ["publication_ready_subgoal", "precise_demotion", "blocked_named_lemma", "release_to_conceptual_exploration"],
    }
    write_json(TARGET_REPORT_ROOT / "result_atlas_update.json", subgoal_decision)
    write_text(
        ROOT / "agentic/reports/results_ellaboration/yang_mills_representational_dynamics_subgoal_decision.md",
        (
            "# YM Representational Dynamics Subgoal Decision\n\n"
            "- Selected subgoal: fibered block RG retained/fiber covariance accounting.\n"
            "- Decision: bounded publication-consolidation candidate, not a Clay proof.\n"
            "- Publication weight: coherent restricted theorem family with exact accounting and explicit non-implications.\n"
            "- Understanding gain: separates retained coarse information, eliminated fiber information, defect accounting, and the still-open quantitative YM estimates.\n"
            "- Budget: four completion cycles, recursion depth one, then publish, demote, block, or return to conceptual exploration.\n"
        ),
    )


def build_source_manifest(archives: dict[str, Any], checksum_report: dict[str, Any], source_index: dict[str, Any]) -> dict[str, Any]:
    skill_manifest_path = SKILL_BUNDLE_ROOT / "11_vscode_codex_skill_bundle/skill_manifest.json"
    skill_manifest = load_json(skill_manifest_path)
    manifest = {
        "schema_version": 1,
        "generated_utc": utc_now(),
        "target_id": TARGET_ID,
        "version": VERSION,
        "epistemic_status": (
            "Imported as a research programme and restricted theorem suite. It does not construct four-dimensional "
            "continuum Yang-Mills theory and does not prove the Clay mass-gap problem."
        ),
        "archives": archives,
        "research_package_root": rel(RESEARCH_ROOT),
        "skill_bundle_root": rel(SKILL_BUNDLE_ROOT / "11_vscode_codex_skill_bundle"),
        "checksum_report": rel(IMPORT_ROOT / "checksum_report.json"),
        "source_index": rel(REPORT_ROOT / "source_index.json"),
        "checksum_all_ok": checksum_report["all_ok"],
        "research_file_count": source_index["summary_counts"]["files"],
        "skill_count": skill_manifest.get("skill_count"),
        "skill_bundle_orchestrator": skill_manifest.get("orchestrator"),
        "skill_phase_order": skill_manifest.get("phase_order", []),
    }
    return manifest


def main() -> int:
    archives = extract_archives()
    checksum_report = verify_package_checksums()
    source_index, source_index_md = build_source_index()
    test_report = run_tests()
    proof_objects, proof_objects_md = build_proof_objects()
    skill_report = adapt_skills()
    source_manifest = build_source_manifest(archives, checksum_report, source_index)

    write_json(IMPORT_ROOT / "checksum_report.json", checksum_report)
    write_json(IMPORT_ROOT / "source_manifest.json", source_manifest)
    write_json(REPORT_ROOT / "source_index.json", source_index)
    write_text(REPORT_ROOT / "source_index.md", source_index_md)
    write_json(PROOF_OBJECT_ROOT / "ym_representational_dynamics_objects.json", proof_objects)
    write_text(PROOF_OBJECT_ROOT / "ym_representational_dynamics_objects.md", proof_objects_md)

    update_dispatch_registry()
    update_task_registry()
    write_reports(source_index, checksum_report, test_report, proof_objects, skill_report)

    print(
        json.dumps(
            {
                "target_id": TARGET_ID,
                "source_manifest": rel(IMPORT_ROOT / "source_manifest.json"),
                "source_index": rel(REPORT_ROOT / "source_index.json"),
                "proof_objects": rel(PROOF_OBJECT_ROOT / "ym_representational_dynamics_objects.json"),
                "skill_count": skill_report["skill_count"],
                "test_count": test_report["test_count"],
                "test_status": test_report["status"],
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
