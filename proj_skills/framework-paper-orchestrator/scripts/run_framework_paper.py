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
"""Run the evidence-qualified repository-to-paper pipeline with stage receipts."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[3]
PACK = ROOT / "proj_skills"
SECTIONS = (
    "abstract", "introduction", "related-work", "method", "architecture",
    "implementation", "evaluation", "limitations", "conclusion",
)


def digest(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def repository_digest(root: Path) -> str:
    """Bind resume decisions to source contents while excluding generated/cache state."""
    value = hashlib.sha256()
    excluded = {".git", "__pycache__", ".pytest_cache", ".mypy_cache"}
    for path in sorted(root.rglob("*")):
        relative = path.relative_to(root)
        if any(part in excluded for part in relative.parts) or relative.parts[:2] == ("artifacts", "project-papers"):
            continue
        if path.is_symlink() or not path.is_file() or path.suffix == ".pyc":
            continue
        value.update(relative.as_posix().encode()); value.update(b"\0"); value.update(path.read_bytes()); value.update(b"\0")
    return "sha256:" + value.hexdigest()


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def dump(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def run_stage(name: str, command: list[str], inputs: list[Path], outputs: list[Path], receipts: Path, resume: bool, context: dict[str, str] | None = None) -> None:
    receipt = receipts / f"{name}.json"
    signature = {
        "command": command,
        "inputs": {str(path): digest(path) for path in inputs},
        "tool_digest": digest(Path(command[1])) if len(command) > 1 and Path(command[1]).is_file() else None,
        "context": context or {},
    }
    if resume and receipt.is_file() and all(path.is_file() for path in outputs):
        previous = load(receipt)
        if previous.get("status") == "pass" and previous.get("signature") == signature:
            expected = previous.get("outputs", {})
            if all(expected.get(str(path)) == digest(path) for path in outputs):
                return
    receipts.mkdir(parents=True, exist_ok=True)
    dump(receipt, {"stage": name, "status": "running", "signature": signature, "outputs": {}})
    environment = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1"}
    result = subprocess.run(command, cwd=ROOT, text=True, capture_output=True, env=environment, check=False)
    record = {
        "stage": name,
        "status": "pass" if result.returncode == 0 and all(path.is_file() for path in outputs) else "fail",
        "signature": signature,
        "outputs": {str(path): digest(path) for path in outputs if path.is_file()},
        "returncode": result.returncode,
        "stdout": result.stdout[-4000:],
        "stderr": result.stderr[-4000:],
    }
    dump(receipt, record)
    if record["status"] != "pass":
        raise RuntimeError(f"stage {name} failed; see {receipt}")


def script(skill: str, filename: str) -> str:
    return str(PACK / skill / "scripts" / filename)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, required=True, help="Frozen repository snapshot to interpret")
    parser.add_argument("--output-root", type=Path, default=ROOT / "artifacts" / "project-papers")
    parser.add_argument("--slug", default="framework-paper")
    parser.add_argument("--run-id", default=datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ"))
    parser.add_argument("--literature", type=Path)
    parser.add_argument("--result-packet", type=Path)
    parser.add_argument("--resume", action="store_true")
    args = parser.parse_args()
    repo = args.repo.resolve()
    if not repo.is_dir():
        parser.error("--repo must be an existing directory")
    for label, path in (("--literature", args.literature), ("--result-packet", args.result_packet)):
        if path and not path.is_file():
            parser.error(f"{label} must be an existing file")
    run = (args.output_root / args.slug / args.run_id).resolve()
    if run.exists() and any(run.iterdir()) and not args.resume:
        parser.error("run directory exists and is non-empty; use --resume or a new --run-id")
    models, sections, bundle, receipts = run / "models", run / "sections", run / "bundle", run / "receipts"
    models.mkdir(parents=True, exist_ok=True)
    py = sys.executable
    evidence, functional, workflow = models / "evidence-index.json", models / "functional-model.json", models / "workflow-model.json"
    execution, abstraction, notation = models / "execution-model.json", models / "framework-model.json", run / "notation.tex"
    claims, blueprint, figures = models / "claim-ledger.json", models / "blueprint.json", models / "figures.json"
    run_stage("01-evidence-index", [py, script("framework-evidence-indexer", "build_evidence_index.py"), "--repo", str(repo), "--output", str(evidence)], [], [evidence], receipts, args.resume, {"repository_digest": repository_digest(repo)})
    run_stage("02-functional-model", [py, script("framework-functional-modeler", "build_functional_model.py"), str(evidence), str(functional)], [evidence], [functional], receipts, args.resume)
    run_stage("03-workflow-model", [py, script("framework-workflow-modeler", "build_workflow_model.py"), str(evidence), str(workflow)], [evidence], [workflow], receipts, args.resume)
    run_stage("04-execution-model", [py, script("framework-execution-evidence-assessor", "assess_execution_evidence.py"), str(evidence), str(execution)], [evidence], [execution], receipts, args.resume)
    run_stage("05-abstraction", [py, script("framework-abstraction-synthesizer", "synthesize_framework_abstraction.py"), str(functional), str(workflow), str(execution), str(abstraction), str(notation)], [functional, workflow, execution], [abstraction, notation], receipts, args.resume)
    claim_command = [py, script("framework-paper-claim-curator", "curate_claim_ledger.py"), str(abstraction), str(claims)]
    claim_inputs = [abstraction]
    for flag, path in (("--literature", args.literature), ("--results", args.result_packet)):
        if path:
            claim_command.extend([flag, str(path.resolve())]); claim_inputs.append(path.resolve())
    run_stage("06-claim-ledger", claim_command, claim_inputs, [claims], receipts, args.resume)
    blueprint_command = [py, script("framework-paper-blueprint-author", "generate_paper_packets.py"), "blueprint", "--ledger", str(claims), "--abstraction", str(abstraction), "--blueprint-id", args.slug, "--output", str(blueprint)]
    blueprint_inputs = [claims, abstraction]
    for flag, path in (("--literature", args.literature), ("--result-packet", args.result_packet)):
        if path:
            blueprint_command.extend([flag, str(path.resolve())]); blueprint_inputs.append(path.resolve())
    run_stage("07-blueprint", blueprint_command, blueprint_inputs, [blueprint], receipts, args.resume)
    bp, ledger = load(blueprint), load(claims)
    claim_map = {item.get("claim_id", item.get("id")): item for item in ledger.get("claims", [])}
    body_claims = sorted({cid for item in bp["sections"] if item["section_id"] not in {"abstract", "conclusion"} for cid in item["allowed_claim_ids"]})
    for index, sid in enumerate(SECTIONS, 8):
        spec = next(item for item in bp["sections"] if item["section_id"] == sid)
        licensed_sentences = []
        for cid in spec["allowed_claim_ids"]:
            claim = claim_map.get(cid, {})
            text = claim.get("exact_claim") or claim.get("claim_text") or claim.get("text")
            if text:
                licensed_sentences.append((cid, text))
        ids = [item[0] for item in licensed_sentences]
        joined = " ".join(item[1] for item in licensed_sentences)
        leads = {
            "abstract": "We present an evidence-qualified abstraction of a repository-governed AI workflow. The abstraction separates declared structure from execution evidence and preserves traceability to a frozen snapshot.",
            "introduction": "AI workflow repositories intertwine functional capabilities, control topology, executable evidence, and publication-facing claims. This paper describes those layers under explicit epistemic constraints.",
            "method": "The method compiles bounded repository evidence into functional, workflow, and execution models before constructing paper-level abstractions and licensed claims.",
            "architecture": "At the architectural level, the framework is represented as traceable constructs connected to declared workflow and evidence postures.",
            "implementation": "The implementation uses deterministic, digest-bound artifacts and fail-closed stage handoffs so each paper statement remains auditable.",
            "limitations": "The source snapshot supports structural description, not claims of novelty, comparative advantage, causal efficacy, or universal runtime reachability.",
            "conclusion": "The resulting description exposes the framework's essential responsibilities while retaining explicit evidence and scope boundaries.",
        }
        paragraphs = [] if sid in {"related-work", "evaluation"} else [{"text": (leads[sid] + (" " + joined if joined else "")).strip(), "claim_ids": ids, "citation_keys": []}]
        draft = sections / f"{sid}.draft.json"
        dump(draft, {"paragraphs": paragraphs, "accepted_body_claim_ids": body_claims, "warnings": []})
        command = [py, script("framework-paper-blueprint-author", "generate_paper_packets.py"), "section", "--blueprint", str(blueprint), "--ledger", str(claims), "--model", str(abstraction), "--draft", str(draft), "--section-id", sid, "--output", str(sections / f"{sid}.section.json"), "--tex-output", str(sections / f"{sid}.tex")]
        section_inputs = [blueprint, claims, abstraction, draft]
        for flag, path in (("--literature", args.literature), ("--result-packet", args.result_packet)):
            if path:
                command.extend([flag, str(path.resolve())]); section_inputs.append(path.resolve())
        run_stage(f"{index:02d}-section-{sid}", command, section_inputs, [sections / f"{sid}.section.json", sections / f"{sid}.tex"], receipts, args.resume)
    run_stage("17-figures", [py, script("framework-paper-figure-planner", "plan_figures.py"), "--workflow-model", str(workflow), "--framework-model", str(abstraction), "--output", str(figures)], [workflow, abstraction], [figures], receipts, args.resume)
    review = run / "consistency-review.json"
    run_stage("18-consistency", [py, script("framework-paper-consistency-adjudicator", "adjudicate_paper.py"), "--claim-ledger", str(claims), "--blueprint", str(blueprint), "--sections-dir", str(sections), "--output", str(review)], [claims, blueprint, *sorted(sections.glob("*.section.json"))], [review], receipts, args.resume)
    run_stage("19-assemble", [py, script("framework-paper-latex-assembler", "assemble_paper.py"), "--blueprint", str(blueprint), "--sections-dir", str(sections), "--review", str(review), "--figures", str(figures), "--output-dir", str(bundle)], [blueprint, review, figures, *sorted(sections.glob("*.section.json")), *sorted(sections.glob("*.tex"))], [bundle / "main.tex", bundle / "build-manifest.json"], receipts, args.resume)
    validation = bundle / "validation.json"
    run_stage("20-validate", [py, script("framework-paper-validator", "validate_paper.py"), "--bundle", str(bundle), "--output", str(validation)], [bundle / "main.tex", bundle / "build-manifest.json"], [validation], receipts, args.resume)
    dump(run / "run-manifest.json", {"schema_version": 1, "status": "pass", "repo": str(repo), "run_id": args.run_id, "promotion_status": "not_promoted", "validation": str(validation.relative_to(run))})
    print(run)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
