# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
# 
# SPDX-License-Identifier: MIT

"""Generate and execute concept/ontology revision actions from loop and coherence artifacts."""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any

import yaml

_COMMON_DIR = Path(__file__).resolve().parents[3] / "common"
if str(_COMMON_DIR) not in sys.path:
    sys.path.insert(0, str(_COMMON_DIR))

from contracts import validate_coherence_report
from contracts import validate_phyp
from reasoning_log import ReasoningLogger


BLOCK_RE = re.compile(r"```yaml\n(.*?)\n```", re.DOTALL)
ID_SAFE_RE = re.compile(r"[^A-Za-z0-9._:-]+")


def _load_kb_statements(kb_path: Path) -> dict[str, dict[str, Any]]:
    """
    Relevance: Operates within the ontology revision layer.
    Concept: Loading and structuring external artifacts for deterministic processing.
    Contribution: Provides clean, typed inputs so downstream reasoning steps remain auditable.
    """

    out: dict[str, dict[str, Any]] = {}
    for match in BLOCK_RE.finditer(kb_path.read_text(encoding="utf-8")):
        try:
            payload = yaml.safe_load(match.group(1))
        except yaml.YAMLError:
            continue
        if not isinstance(payload, dict):
            continue
        sid = str(payload.get("id", "")).strip()
        if not sid:
            continue
        out[sid] = payload
    return out


def _coherence_index(coherence: dict[str, Any]) -> dict[str, dict[str, Any]]:
    """
    Relevance: Operates within the ontology revision layer.
    Concept: Quantitative evaluation of hypotheses or theory-graph properties.
    Contribution: Produces the quantitative signals used for retention, revision, and route prioritization.
    """

    out: dict[str, dict[str, Any]] = {}
    if isinstance(coherence.get("hypothesis_coherence_index"), dict):
        for hid, row in coherence.get("hypothesis_coherence_index", {}).items():
            if isinstance(row, dict):
                out[str(hid).strip()] = row
        return out
    for row in coherence.get("hypothesis_coherence", []) if isinstance(coherence.get("hypothesis_coherence"), list) else []:
        if not isinstance(row, dict):
            continue
        hid = str(row.get("hypothesis_id", "")).strip()
        if hid:
            out[hid] = row
    return out


def _build_revision_actions(
    statements: dict[str, dict[str, Any]],
    phyp: dict[str, Any],
    loop_report: dict[str, Any],
    coherence: dict[str, Any],
    hardness: dict[str, Any],
) -> dict[str, Any]:
    """
    Relevance: Operates within the ontology revision layer.
    Concept: Construction of derived graph/model structures used by later stages.
    Contribution: Creates the structural substrate that enables cross-stage scoring and interpretation.
    """

    final_summary = loop_report.get("final_summary", {}) if isinstance(loop_report.get("final_summary"), dict) else {}
    unresolved_ids = [str(x).strip() for x in final_summary.get("unresolved_ids", []) if str(x).strip()]
    provisional_ids = [str(x).strip() for x in final_summary.get("provisionally_refuted_ids", []) if str(x).strip()]
    unresolved_open = unresolved_ids + provisional_ids

    hypotheses = [h for h in phyp.get("hypotheses", []) if isinstance(h, dict)]
    hypothesis_by_id = {str(h.get("id", "")).strip(): h for h in hypotheses if str(h.get("id", "")).strip()}
    target_frequency: Counter[str] = Counter()
    for hid in unresolved_open:
        h = hypothesis_by_id.get(hid, {})
        target = str(h.get("target_statement_id", "")).strip()
        if target:
            target_frequency[target] += 1

    coherence_map = _coherence_index(coherence)
    low_coherence_hids = [
        hid
        for hid, row in coherence_map.items()
        if float(row.get("coherence_delta_global", 0.0) or 0.0) < -0.08
    ]

    conceptual_kinds = {
        "definition-introduction",
        "representation-shift",
        "intermediate-invariant",
        "barrier-escape-principle",
        "analogy-transfer",
        "normal-form-reduction",
    }
    conceptual_unresolved = [
        hid
        for hid in unresolved_open
        if str(hypothesis_by_id.get(hid, {}).get("kind", "")).strip().lower() in conceptual_kinds
    ]

    revision_actions: list[dict[str, Any]] = []
    idx = 1

    if target_frequency:
        top_targets = [sid for sid, _ in target_frequency.most_common(5)]
        revision_actions.append(
            {
                "revision_id": f"rev.{idx:03d}",
                "revision_type": "concept-splitting",
                "priority": "high",
                "trigger": "unresolved-hypothesis-clusters",
                "target_statement_ids": top_targets,
                "action": "Split overloaded target concepts into finer-grained definitions and rerun connector + abduce.",
                "success_criteria": "Reduced unresolved cluster size and non-negative coherence delta.",
            }
        )
        idx += 1

    if low_coherence_hids:
        revision_actions.append(
            {
                "revision_id": f"rev.{idx:03d}",
                "revision_type": "definition-repair",
                "priority": "high",
                "trigger": "negative-global-coherence",
                "target_hypothesis_ids": low_coherence_hids[:10],
                "action": "Repair definitions and hidden assumptions behind coherence-negative hypotheses.",
                "success_criteria": "coherence_delta_global >= 0 for repaired hypotheses.",
            }
        )
        idx += 1

    anti_barrier = hardness.get("anti_barrier_programs", []) if isinstance(hardness.get("anti_barrier_programs"), list) else []
    if anti_barrier:
        families = [str(x.get("barrier_family", "")).strip() for x in anti_barrier if isinstance(x, dict)]
        revision_actions.append(
            {
                "revision_id": f"rev.{idx:03d}",
                "revision_type": "regime-switch",
                "priority": "high",
                "trigger": "barrier-program-activation",
                "barrier_families": [f for f in families if f][:6],
                "action": "Switch to alternate proof regimes suggested by anti-barrier programs and re-encode targets.",
                "success_criteria": "At least one pathway with positive entailment gain and no coherence degradation.",
            }
        )
        idx += 1

    missing_dependency_refs = 0
    known_ids = set(statements.keys())
    for stmt in statements.values():
        for dep in stmt.get("depends_on", []) if isinstance(stmt.get("depends_on"), list) else []:
            dep_s = str(dep).strip()
            if dep_s and dep_s not in known_ids:
                missing_dependency_refs += 1
    if missing_dependency_refs > 0:
        revision_actions.append(
            {
                "revision_id": f"rev.{idx:03d}",
                "revision_type": "kb-reencoding",
                "priority": "medium",
                "trigger": "missing-dependency-refs",
                "missing_dependency_refs": missing_dependency_refs,
                "action": "Backfill missing dependencies and normalize statement IDs before next abductive cycle.",
                "success_criteria": "missing_dependency_refs reduced to zero on the next connector pass.",
            }
        )
        idx += 1

    if conceptual_unresolved:
        revision_actions.append(
            {
                "revision_id": f"rev.{idx:03d}",
                "revision_type": "representation-rotation",
                "priority": "medium",
                "trigger": "stalled-conceptual-hypotheses",
                "target_hypothesis_ids": conceptual_unresolved[:10],
                "action": "Rotate representation/normal-form assumptions for unresolved conceptual hypotheses.",
                "success_criteria": "Increase in explanatory_power_local and reduced unresolved conceptual count.",
            }
        )
        idx += 1

    priority_program = revision_actions[:3]
    return {
        "revision_summary": {
            "revision_count": len(revision_actions),
            "unresolved_hypotheses": len(unresolved_ids),
            "provisionally_refuted_hypotheses": len(provisional_ids),
            "low_coherence_hypotheses": len(low_coherence_hids),
            "conceptual_unresolved_hypotheses": len(conceptual_unresolved),
        },
        "priority_program": priority_program,
        "revision_actions": revision_actions,
        "revision_context": {
            "unresolved_open_ids": unresolved_open,
            "low_coherence_hypothesis_ids": low_coherence_hids,
            "conceptual_unresolved_hypothesis_ids": conceptual_unresolved,
        },
    }


def _safe_revision_id(raw: str) -> str:
    """
    Relevance: Operates within the ontology revision layer.
    Concept: Internal helper implementing one deterministic step of this stage.
    Contribution: Contributes a deterministic transformation that supports end-to-end reasoning reproducibility.
    """

    clean = ID_SAFE_RE.sub("-", str(raw).strip())
    clean = clean.strip("-")
    return clean or "x"


def _make_generated_statement_id(prefix: str, anchor: str, existing_ids: set[str]) -> str:
    """
    Relevance: Operates within the ontology revision layer.
    Concept: Internal helper implementing one deterministic step of this stage.
    Contribution: Contributes a deterministic transformation that supports end-to-end reasoning reproducibility.
    """

    base = f"st.rev.{_safe_revision_id(prefix)}.{_safe_revision_id(anchor)}"
    candidate = base
    idx = 1
    while candidate in existing_ids:
        idx += 1
        candidate = f"{base}.{idx}"
    existing_ids.add(candidate)
    return candidate


def _next_hypothesis_id(seed: str, existing_ids: set[str]) -> str:
    """
    Relevance: Operates within the ontology revision layer.
    Concept: Internal helper implementing one deterministic step of this stage.
    Contribution: Contributes a deterministic transformation that supports end-to-end reasoning reproducibility.
    """

    base = f"{seed}.rot"
    idx = 1
    candidate = f"{base}{idx}"
    while candidate in existing_ids:
        idx += 1
        candidate = f"{base}{idx}"
    existing_ids.add(candidate)
    return candidate


def _apply_revision_actions(
    kb_path: Path,
    statements: dict[str, dict[str, Any]],
    phyp: dict[str, Any],
    report: dict[str, Any],
) -> tuple[str, dict[str, Any], dict[str, Any]]:
    """
    Relevance: Operates within the ontology revision layer.
    Concept: Primary callable implementing a stage-level behavior.
    Contribution: Closes the revision loop by producing concrete transformed artifacts for subsequent reasoning rounds.
    """

    original_kb = kb_path.read_text(encoding="utf-8")
    patched_phyp = yaml.safe_load(yaml.safe_dump(phyp, sort_keys=False))
    if not isinstance(patched_phyp, dict):
        patched_phyp = {"hypotheses": []}
    hypotheses = patched_phyp.get("hypotheses")
    if not isinstance(hypotheses, list):
        hypotheses = []
        patched_phyp["hypotheses"] = hypotheses

    hypothesis_by_id: dict[str, dict[str, Any]] = {}
    existing_hyp_ids: set[str] = set()
    for hyp in hypotheses:
        if not isinstance(hyp, dict):
            continue
        hid = str(hyp.get("id", "")).strip()
        if not hid:
            continue
        hypothesis_by_id[hid] = hyp
        existing_hyp_ids.add(hid)

    generated_statements: list[dict[str, Any]] = []
    generated_hypothesis_ids: list[str] = []
    touched_hypotheses: set[str] = set()
    existing_statement_ids = set(statements.keys())

    for action in report.get("revision_actions", []) if isinstance(report.get("revision_actions"), list) else []:
        if not isinstance(action, dict):
            continue
        revision_id = str(action.get("revision_id", "rev.unknown")).strip()
        revision_type = str(action.get("revision_type", "")).strip().lower()

        if revision_type == "definition-repair":
            for hid in action.get("target_hypothesis_ids", []) if isinstance(action.get("target_hypothesis_ids"), list) else []:
                hid_s = str(hid).strip()
                if not hid_s or hid_s not in hypothesis_by_id:
                    continue
                hyp = hypothesis_by_id[hid_s]
                touched_hypotheses.add(hid_s)
                old_priority = float(hyp.get("priority", 0.0) or 0.0)
                hyp["priority"] = round(max(0.05, old_priority * 0.82), 4)
                hyp["status"] = "needs-testing"
                notes = hyp.get("notes", "")
                notes_s = str(notes).strip()
                tag = f"[{revision_id}] definition-repair applied due to coherence tension."
                hyp["notes"] = f"{notes_s}\n{tag}".strip() if notes_s else tag

        elif revision_type == "representation-rotation":
            target_hids = action.get("target_hypothesis_ids", []) if isinstance(action.get("target_hypothesis_ids"), list) else []
            for hid in target_hids[:12]:
                hid_s = str(hid).strip()
                src_hyp = hypothesis_by_id.get(hid_s)
                if not src_hyp:
                    continue
                new_id = _next_hypothesis_id(hid_s, existing_hyp_ids)
                new_kind = "representation-shift"
                old_kind = str(src_hyp.get("kind", "")).strip().lower()
                if old_kind == "representation-shift":
                    new_kind = "normal-form-reduction"
                new_hyp = {
                    **src_hyp,
                    "id": new_id,
                    "kind": new_kind,
                    "status": "needs-testing",
                    "priority": round(max(0.05, float(src_hyp.get("priority", 0.0) or 0.0) * 0.75), 4),
                    "provenance": {
                        **(src_hyp.get("provenance", {}) if isinstance(src_hyp.get("provenance"), dict) else {}),
                        "generated_by": "kb-revision-loop",
                        "revision_id": revision_id,
                        "origin_hypothesis_id": hid_s,
                    },
                }
                hypotheses.append(new_hyp)
                hypothesis_by_id[new_id] = new_hyp
                generated_hypothesis_ids.append(new_id)

        elif revision_type == "concept-splitting":
            targets = action.get("target_statement_ids", []) if isinstance(action.get("target_statement_ids"), list) else []
            for sid in targets[:6]:
                sid_s = str(sid).strip()
                if not sid_s:
                    continue
                gen_id = _make_generated_statement_id("split", sid_s, existing_statement_ids)
                generated_statements.append(
                    {
                        "id": gen_id,
                        "kind": "definition",
                        "status": "tentative",
                        "depends_on": [sid_s],
                        "used_symbols": [],
                        "source_ids": [f"auto:{revision_id}"],
                        "informal": f"Refined sub-definition introduced to split overloaded concept around {sid_s}.",
                        "notes": f"Auto-generated by {revision_id} (concept-splitting).",
                    }
                )

        elif revision_type == "kb-reencoding":
            missing_refs: set[str] = set()
            for stmt in statements.values():
                deps = stmt.get("depends_on", [])
                if not isinstance(deps, list):
                    continue
                for dep in deps:
                    dep_s = str(dep).strip()
                    if dep_s and dep_s not in existing_statement_ids:
                        missing_refs.add(dep_s)
            for dep in sorted(missing_refs)[:10]:
                if not re.fullmatch(r"[A-Za-z0-9._:-]+", dep):
                    continue
                gen_id = _make_generated_statement_id("placeholder", dep, existing_statement_ids)
                generated_statements.append(
                    {
                        "id": gen_id,
                        "kind": "assumption",
                        "status": "tentative",
                        "depends_on": [],
                        "used_symbols": [],
                        "source_ids": [f"auto:{revision_id}"],
                        "informal": f"Placeholder assumption to close missing dependency reference `{dep}`.",
                        "notes": f"Auto-generated by {revision_id} (kb-reencoding).",
                    }
                )

        elif revision_type == "regime-switch":
            families = action.get("barrier_families", []) if isinstance(action.get("barrier_families"), list) else []
            meta = patched_phyp.get("revision_metadata")
            if not isinstance(meta, dict):
                meta = {}
                patched_phyp["revision_metadata"] = meta
            existing = meta.get("regime_switch_families")
            if not isinstance(existing, list):
                existing = []
                meta["regime_switch_families"] = existing
            for fam in families:
                fam_s = str(fam).strip()
                if fam_s and fam_s not in existing:
                    existing.append(fam_s)

    patched_kb_lines: list[str] = [original_kb.rstrip(), "", "## Auto-Generated Revision Patch", ""]
    patched_kb_lines.append("This section was generated by `kb-revision-loop` to seed the next orchestrated cycle.")
    patched_kb_lines.append("")
    if generated_statements:
        patched_kb_lines.append("### Generated Statements")
        patched_kb_lines.append("")
        for stmt in generated_statements:
            patched_kb_lines.append("```yaml")
            patched_kb_lines.append(yaml.safe_dump(stmt, sort_keys=False).strip())
            patched_kb_lines.append("```")
            patched_kb_lines.append("")
    else:
        patched_kb_lines.append("- No new statements were generated in this revision pass.")
        patched_kb_lines.append("")

    patched_kb_lines.append("### Patched Hypothesis Summary")
    patched_kb_lines.append("")
    patched_kb_lines.append(f"- Touched hypotheses: {len(touched_hypotheses)}")
    patched_kb_lines.append(f"- Generated hypotheses: {len(generated_hypothesis_ids)}")
    patched_kb_lines.append("")

    executable = {
        "applied": True,
        "touched_hypotheses": sorted(touched_hypotheses),
        "generated_hypothesis_ids": generated_hypothesis_ids,
        "generated_statement_ids": [str(x.get("id", "")) for x in generated_statements],
        "operator_counts": {
            "definition_repair_touches": len(touched_hypotheses),
            "representation_rotations_generated": len(generated_hypothesis_ids),
            "generated_statements": len(generated_statements),
        },
    }
    return "\n".join(patched_kb_lines).rstrip() + "\n", patched_phyp, executable


def _to_markdown(report: dict[str, Any]) -> str:
    """
    Relevance: Operates within the ontology revision layer.
    Concept: Rendering internal outputs into human-readable artifacts.
    Contribution: Improves interpretability by exposing machine results in analyst-friendly form.
    """

    lines: list[str] = []
    lines.append("# Ontology Revision Loop")
    lines.append("")
    summary = report.get("revision_summary", {})
    lines.append("## Summary")
    lines.append("")
    lines.append(f"- Revision actions: {summary.get('revision_count', 0)}")
    lines.append(f"- Unresolved hypotheses: {summary.get('unresolved_hypotheses', 0)}")
    lines.append(f"- Provisionally refuted hypotheses: {summary.get('provisionally_refuted_hypotheses', 0)}")
    lines.append(f"- Low-coherence hypotheses: {summary.get('low_coherence_hypotheses', 0)}")
    lines.append(f"- Conceptual unresolved hypotheses: {summary.get('conceptual_unresolved_hypotheses', 0)}")
    lines.append("")
    lines.append("## Priority Program")
    lines.append("")
    for item in report.get("priority_program", []):
        lines.append(f"- {item.get('revision_id', '')}: {item.get('revision_type', '')} ({item.get('priority', '')})")
    if not report.get("priority_program"):
        lines.append("- none")
    lines.append("")
    lines.append("## Revision Actions")
    lines.append("")
    for item in report.get("revision_actions", []):
        lines.append(f"### {item.get('revision_id', '')} - {item.get('revision_type', '')}")
        lines.append(f"- Priority: {item.get('priority', '')}")
        lines.append(f"- Trigger: {item.get('trigger', '')}")
        lines.append(f"- Action: {item.get('action', '')}")
        lines.append(f"- Success criteria: {item.get('success_criteria', '')}")
        lines.append("")
    if not report.get("revision_actions"):
        lines.append("- none")
        lines.append("")
    executable = report.get("executable_revision", {}) if isinstance(report.get("executable_revision"), dict) else {}
    lines.append("## Executable Revision Outputs")
    lines.append("")
    if executable.get("applied", False):
        lines.append(f"- Patched KB: {executable.get('patched_kb_path', '')}")
        lines.append(f"- Patched PHYP: {executable.get('patched_phyp_path', '')}")
        lines.append(
            f"- Touched hypotheses: {len(executable.get('touched_hypotheses', [])) if isinstance(executable.get('touched_hypotheses'), list) else 0}"
        )
        lines.append(
            f"- Generated hypotheses: {len(executable.get('generated_hypothesis_ids', [])) if isinstance(executable.get('generated_hypothesis_ids'), list) else 0}"
        )
        lines.append(
            f"- Generated statements: {len(executable.get('generated_statement_ids', [])) if isinstance(executable.get('generated_statement_ids'), list) else 0}"
        )
    else:
        lines.append("- executable patching disabled")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    """
    Relevance: Operates within the ontology revision layer.
    Concept: CLI entrypoint orchestration for this script.
    Contribution: Binds parsing, computation, and artifact emission into a reproducible script execution.
    """

    logger = ReasoningLogger("kb-revision-loop")
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--kb", required=True)
    ap.add_argument("--phyp", required=True)
    ap.add_argument("--hypothesis-loop", required=True)
    ap.add_argument("--coherence-report")
    ap.add_argument("--hardness")
    ap.add_argument("--output-json")
    ap.add_argument("--output-md")
    ap.add_argument("--output-patched-kb")
    ap.add_argument("--output-patched-phyp")
    ap.add_argument(
        "--apply-actions",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Apply executable revision operators and emit patched KB/PHYP artifacts.",
    )
    args = ap.parse_args()
    logger.step(
        "Parsed revision-loop arguments",
        "\n".join(
            [
                f"kb={args.kb}",
                f"phyp={args.phyp}",
                f"hypothesis_loop={args.hypothesis_loop}",
                f"coherence_report={args.coherence_report or ''}",
                f"hardness={args.hardness or ''}",
                f"output_json={args.output_json or ''}",
                f"output_md={args.output_md or ''}",
                f"output_patched_kb={args.output_patched_kb or ''}",
                f"output_patched_phyp={args.output_patched_phyp or ''}",
                f"apply_actions={args.apply_actions}",
            ]
        ),
    )

    kb_path = Path(args.kb)
    phyp_path = Path(args.phyp)
    loop_path = Path(args.hypothesis_loop)
    coherence_path = Path(args.coherence_report) if args.coherence_report else None
    hardness_path = Path(args.hardness) if args.hardness else None

    for p in [kb_path, phyp_path, loop_path]:
        if not p.exists():
            log_path = logger.finalize("error", summary=f"Missing input: {p}")
            print(f"[LOG] {log_path}", file=sys.stderr)
            raise SystemExit(f"[ERROR] Missing input: {p}")
    if coherence_path and not coherence_path.exists():
        log_path = logger.finalize("error", summary=f"Missing input: {coherence_path}")
        print(f"[LOG] {log_path}", file=sys.stderr)
        raise SystemExit(f"[ERROR] Missing input: {coherence_path}")
    if hardness_path and not hardness_path.exists():
        log_path = logger.finalize("error", summary=f"Missing input: {hardness_path}")
        print(f"[LOG] {log_path}", file=sys.stderr)
        raise SystemExit(f"[ERROR] Missing input: {hardness_path}")

    statements = _load_kb_statements(kb_path)
    phyp = validate_phyp(yaml.safe_load(phyp_path.read_text(encoding="utf-8")), name="phyp")
    loop_report = json.loads(loop_path.read_text(encoding="utf-8"))
    coherence = (
        validate_coherence_report(json.loads(coherence_path.read_text(encoding="utf-8")), name="coherence")
        if coherence_path
        else {}
    )
    hardness = json.loads(hardness_path.read_text(encoding="utf-8")) if hardness_path else {}

    report = _build_revision_actions(
        statements=statements,
        phyp=phyp,
        loop_report=loop_report if isinstance(loop_report, dict) else {},
        coherence=coherence if isinstance(coherence, dict) else {},
        hardness=hardness if isinstance(hardness, dict) else {},
    )
    report["metadata"] = {
        "kb": str(kb_path),
        "phyp": str(phyp_path),
        "hypothesis_loop": str(loop_path),
        "coherence": str(coherence_path) if coherence_path else "",
        "hardness": str(hardness_path) if hardness_path else "",
        "apply_actions": bool(args.apply_actions),
    }

    if args.output_json:
        out_json = Path(args.output_json)
    else:
        out_json = Path("artifacts") / "revision-loop.json"
    if args.output_md:
        out_md = Path(args.output_md)
    else:
        out_md = Path("artifacts") / "revision-loop.md"
    if args.output_patched_kb:
        out_patched_kb = Path(args.output_patched_kb)
    else:
        out_patched_kb = out_json.parent / "kb.revised.md"
    if args.output_patched_phyp:
        out_patched_phyp = Path(args.output_patched_phyp)
    else:
        out_patched_phyp = out_json.parent / "phyp.revised.yaml"

    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_md.parent.mkdir(parents=True, exist_ok=True)
    out_patched_kb.parent.mkdir(parents=True, exist_ok=True)
    out_patched_phyp.parent.mkdir(parents=True, exist_ok=True)

    executable: dict[str, Any] = {"applied": False}
    if args.apply_actions:
        patched_kb_text, patched_phyp, executable = _apply_revision_actions(
            kb_path=kb_path,
            statements=statements,
            phyp=phyp,
            report=report,
        )
        out_patched_kb.write_text(patched_kb_text, encoding="utf-8")
        out_patched_phyp.write_text(yaml.safe_dump(patched_phyp, sort_keys=False), encoding="utf-8")
        executable["patched_kb_path"] = str(out_patched_kb)
        executable["patched_phyp_path"] = str(out_patched_phyp)
        report["next_round_inputs"] = {"kb": str(out_patched_kb), "phyp": str(out_patched_phyp)}
        logger.add_output("patched_kb", out_patched_kb)
        logger.add_output("patched_phyp", out_patched_phyp)
    report["executable_revision"] = executable

    out_json.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    out_md.write_text(_to_markdown(report), encoding="utf-8")
    print(f"[OK] Wrote JSON: {out_json}")
    print(f"[OK] Wrote Markdown: {out_md}")
    if args.apply_actions:
        print(f"[OK] Wrote patched KB: {out_patched_kb}")
        print(f"[OK] Wrote patched PHYP: {out_patched_phyp}")
    logger.add_output("revision_loop_json", out_json)
    logger.add_output("revision_loop_md", out_md)

    log_path = logger.finalize(
        "success",
        summary=f"Generated {report.get('revision_summary', {}).get('revision_count', 0)} revision actions.",
    )
    print(f"[LOG] {log_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
