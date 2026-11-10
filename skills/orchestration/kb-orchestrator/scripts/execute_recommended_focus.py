#!/usr/bin/env python3
# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT

"""Execute recommended-focus actions from epistemic-hardness outputs.

This stage operationalizes the four recommendations emitted by
`kb-epistemic-hardness`:
1) prioritize top-2 hardness elements,
2) convert top bridge hypotheses into scratch dependency tests,
3) check/backfill dependency coverage on top entrypoints,
4) retain coherence-positive anti-barrier re-encodings.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import deque
from pathlib import Path
from typing import Any

import yaml

_COMMON_DIR = Path(__file__).resolve().parents[3] / "common"
if str(_COMMON_DIR) not in sys.path:
    sys.path.insert(0, str(_COMMON_DIR))

from kb_context import canonical_artifacts_dir
from kb_context import resolve_kb_reference
from reasoning_log import ReasoningLogger

BLOCK_RE = re.compile(r"```yaml\n(.*?)\n```", re.DOTALL)
SEVERITY_RANK = {"critical": 4.0, "high": 3.0, "medium-high": 2.5, "moderate": 2.0, "low": 1.0}


def _load_json(path: Path) -> dict[str, Any]:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: Loading and structuring external artifacts for deterministic processing.
    Contribution: Provides clean, typed inputs so downstream recommendation execution stays auditable.
    """

    if not path.exists():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}
    return payload if isinstance(payload, dict) else {}


def _load_phyp(path: Path) -> dict[str, Any]:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: Loading and structuring external artifacts for deterministic processing.
    Contribution: Provides clean, typed hypothesis inputs for bridge-test synthesis.
    """

    if not path.exists():
        return {"hypotheses": []}
    try:
        payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    except Exception:
        return {"hypotheses": []}
    if not isinstance(payload, dict):
        return {"hypotheses": []}
    if not isinstance(payload.get("hypotheses"), list):
        payload["hypotheses"] = []
    return payload


def _load_statements(kb_path: Path) -> dict[str, dict[str, Any]]:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: Extraction of structured signals from raw text or artifact payloads.
    Contribution: Supplies deterministic statement/dependency structure for scratch deduction checks.
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
        deps = payload.get("depends_on", [])
        payload["depends_on"] = [str(x).strip() for x in deps if str(x).strip()] if isinstance(deps, list) else []
        out[sid] = payload
    return out


def _has_path(src: str, dst: str, adjacency: dict[str, set[str]]) -> bool:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: Internal helper implementing one deterministic step of this stage.
    Contribution: Enables transitive dependency checks used in scratch deduce classification.
    """

    if src == dst:
        return True
    if src not in adjacency or dst not in adjacency:
        return False
    queue = deque([src])
    seen = {src}
    while queue:
        cur = queue.popleft()
        for nxt in adjacency.get(cur, set()):
            if nxt == dst:
                return True
            if nxt in seen:
                continue
            seen.add(nxt)
            queue.append(nxt)
    return False


def _top_two_hardness(hardness: dict[str, Any]) -> list[dict[str, Any]]:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: Selection/retrieval of the most relevant candidates for reasoning.
    Contribution: Focuses downstream tests on the highest-impact hardness elements first.
    """

    rows = hardness.get("essential_elements", []) if isinstance(hardness.get("essential_elements"), list) else []
    typed = [row for row in rows if isinstance(row, dict)]
    typed.sort(
        key=lambda row: (
            SEVERITY_RANK.get(str(row.get("severity", "")).strip().lower(), 0.0),
            float(row.get("score", 0.0) or 0.0),
        ),
        reverse=True,
    )
    return typed[:2]


def _scratch_evidence(
    bridges: dict[str, Any],
    phyp: dict[str, Any],
    statements: dict[str, dict[str, Any]],
    focus_statement_ids: set[str],
    max_bridge_tests: int,
) -> dict[str, Any]:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: Construction of derived graph/model structures used by later stages.
    Contribution: Converts top bridge programs into round-evidence consumable by hypothesis-loop.
    """

    hypotheses = [h for h in phyp.get("hypotheses", []) if isinstance(h, dict)]
    by_id = {str(h.get("id", "")).strip(): h for h in hypotheses if str(h.get("id", "")).strip()}
    bridge_rows = bridges.get("bridge_programs", []) if isinstance(bridges.get("bridge_programs"), list) else []

    selected: list[tuple[str, str, str, float, str]] = []
    for row in bridge_rows:
        if not isinstance(row, dict):
            continue
        commit = row.get("inferential_commitment", {}) if isinstance(row.get("inferential_commitment"), dict) else {}
        hid = str(commit.get("hypothesis_id", "")).strip()
        src = str(row.get("from_id", "")).strip()
        dst = str(row.get("to_id", "")).strip()
        if not hid or not src or not dst or hid not in by_id:
            continue
        score = float(row.get("bridge_score", 0.0) or 0.0)
        selected.append((hid, src, dst, score, str(row.get("bridge_id", "")).strip()))

    selected.sort(
        key=lambda item: ((1 if (item[1] in focus_statement_ids or item[2] in focus_statement_ids) else 0), item[3]),
        reverse=True,
    )
    selected = selected[: max(1, max_bridge_tests)]

    adjacency: dict[str, set[str]] = {sid: set() for sid in statements}
    for sid, stmt in statements.items():
        for dep in stmt.get("depends_on", []) if isinstance(stmt.get("depends_on"), list) else []:
            if dep in statements:
                adjacency[dep].add(sid)

    evidence_rows: list[dict[str, Any]] = []
    for hid, src, dst, score, bridge_id in selected:
        target = statements.get(dst, {})
        deps = target.get("depends_on", []) if isinstance(target.get("depends_on"), list) else []
        direct = src in deps
        transitive = _has_path(src, dst, adjacency)
        if direct:
            deduce_class = "entailed"
            residual_delta = -1.0
        elif transitive:
            deduce_class = "conditionally-entailed"
            residual_delta = -0.5
        else:
            deduce_class = "not-derived"
            residual_delta = 0.6

        evidence_rows.append(
            {
                "hypothesis_id": hid,
                "deduce_class": deduce_class,
                "abduce_residual_delta": residual_delta,
                "experimental_success": deduce_class != "not-derived",
                "contradiction": False,
                "scratch_test": {
                    "bridge_id": bridge_id,
                    "from_id": src,
                    "to_id": dst,
                    "direct_dependency": direct,
                    "transitive_dependency": transitive,
                    "bridge_score": round(score, 4),
                },
                "notes": (
                    "Generated from structural scratch dependency tests on prioritized bridge "
                    "hypotheses (recommended-focus continuation)."
                ),
            }
        )

    return {
        "selected": selected,
        "evidence_rows": evidence_rows,
        "counts": {
            "entailed": sum(1 for row in evidence_rows if row.get("deduce_class") == "entailed"),
            "conditionally-entailed": sum(1 for row in evidence_rows if row.get("deduce_class") == "conditionally-entailed"),
            "not-derived": sum(1 for row in evidence_rows if row.get("deduce_class") == "not-derived"),
        },
    }


def _entrypoint_dependency_coverage(
    entrypoints: dict[str, Any],
    statements: dict[str, dict[str, Any]],
    top_k: int = 8,
) -> dict[str, Any]:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: Quantitative coverage check on dependency explicitness.
    Contribution: Verifies whether top entrypoint clusters already have explicit formal dependencies.
    """

    rows = entrypoints.get("ranked_entrypoints", []) if isinstance(entrypoints.get("ranked_entrypoints"), list) else []
    selected = [row for row in rows if isinstance(row, dict)][: max(1, top_k)]
    detail: list[dict[str, Any]] = []
    for row in selected:
        sid = str(row.get("statement_id", "")).strip()
        stmt = statements.get(sid, {})
        kind = str(stmt.get("kind", "")).strip().lower()
        deps = stmt.get("depends_on", []) if isinstance(stmt.get("depends_on"), list) else []
        needs_deps = kind in {"theorem", "lemma", "corollary", "proposition", "derived-construction"}
        detail.append(
            {
                "statement_id": sid,
                "kind": kind,
                "depends_on_count": len(deps),
                "dependency_coverage_ok": (len(deps) > 0) if needs_deps else True,
                "depends_on": deps,
            }
        )
    return {
        "top_entrypoints_checked": len(detail),
        "coverage_ok_count": sum(1 for row in detail if row.get("dependency_coverage_ok")),
        "rows": detail,
    }


def _barrier_coherence_filter(
    phyp: dict[str, Any],
    coherence: dict[str, Any],
    coherence_revised: dict[str, Any] | None,
) -> dict[str, Any]:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: Coherence-gated retention for barrier-facing hypotheses.
    Contribution: Enforces 'keep only coherence-positive re-encodings' as an explicit filter.
    """

    rows = coherence.get("hypothesis_coherence", []) if isinstance(coherence.get("hypothesis_coherence"), list) else []
    index = {str(row.get("hypothesis_id", "")).strip(): row for row in rows if isinstance(row, dict)}

    retained: list[dict[str, Any]] = []
    rejected: list[dict[str, Any]] = []
    for hyp in phyp.get("hypotheses", []) if isinstance(phyp.get("hypotheses"), list) else []:
        if not isinstance(hyp, dict):
            continue
        hid = str(hyp.get("id", "")).strip()
        if not hid:
            continue
        scope = str(hyp.get("barrier_scope", "")).strip().lower()
        if not scope or scope == "none":
            continue
        delta = float((index.get(hid, {}) or {}).get("coherence_delta_global", 0.0) or 0.0)
        row = {
            "hypothesis_id": hid,
            "barrier_scope": scope,
            "coherence_delta_global": round(delta, 6),
            "target_statement_id": str(hyp.get("target_statement_id", "")).strip(),
        }
        if delta >= 0.0:
            retained.append(row)
        else:
            rejected.append(row)

    original_gc = float(((coherence.get("coherence_profile") if isinstance(coherence.get("coherence_profile"), dict) else {}) or {}).get("global_coherence", 0.0) or 0.0)
    revised_gc = None
    if coherence_revised:
        revised_gc = float(((coherence_revised.get("coherence_profile") if isinstance(coherence_revised.get("coherence_profile"), dict) else {}) or {}).get("global_coherence", 0.0) or 0.0)

    out: dict[str, Any] = {
        "retained_count": len(retained),
        "rejected_count": len(rejected),
        "retained": retained,
        "rejected": rejected,
        "global_coherence_original": round(original_gc, 6),
    }
    if revised_gc is not None:
        out["global_coherence_revised"] = round(revised_gc, 6)
        out["global_coherence_delta_revised_minus_original"] = round(revised_gc - original_gc, 6)
        if revised_gc >= original_gc:
            out["decision"] = "promote-revised-reencoding"
            out["decision_reason"] = "Revised re-encoding preserved or improved global coherence."
        else:
            out["decision"] = "reject-global-reencoding-keep-local-positive"
            out["decision_reason"] = (
                "Revised re-encoding decreased global coherence; keep original KB and "
                "retain only local coherence-positive barrier hypotheses."
            )
    return out


def _to_markdown(report: dict[str, Any]) -> str:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: Rendering internal outputs into human-readable artifacts.
    Contribution: Makes recommendation execution outcomes interpretable for researchers.
    """

    lines: list[str] = []
    lines.append("# Recommended Focus Execution")
    lines.append("")
    lines.append("## 1) Prioritize Top-2 High-Severity Hardness Elements")
    lines.append("")
    for row in report.get("top2_hardness_elements", []):
        lines.append(f"- {row.get('name', '')} ({row.get('severity', '')}, score={float(row.get('score', 0.0) or 0.0):.4f})")
        evidence_ids = row.get("evidence_ids", []) if isinstance(row.get("evidence_ids"), list) else []
        if evidence_ids:
            lines.append(f"  - Evidence IDs: {', '.join(str(x) for x in evidence_ids[:8])}")
    lines.append("")

    lines.append("## 2) Scratch Dependency Tests + Deduce Checks")
    lines.append("")
    scratch = report.get("scratch_dependency_tests", {}) if isinstance(report.get("scratch_dependency_tests"), dict) else {}
    counts = scratch.get("deduce_class_counts", {}) if isinstance(scratch.get("deduce_class_counts"), dict) else {}
    lines.append(f"- Selected bridge hypotheses: {scratch.get('selected_bridge_hypotheses', 0)}")
    lines.append(
        "- entailed: {e}, conditionally-entailed: {c}, not-derived: {n}".format(
            e=int(counts.get("entailed", 0) or 0),
            c=int(counts.get("conditionally-entailed", 0) or 0),
            n=int(counts.get("not-derived", 0) or 0),
        )
    )
    lines.append(f"- Round evidence: `{scratch.get('round_evidence_path', '')}`")
    post_loop = scratch.get("post_loop", {}) if isinstance(scratch.get("post_loop"), dict) else {}
    if post_loop:
        lines.append(
            f"- Post-loop status: supported={post_loop.get('supported_count', 0)}, "
            f"refuted={post_loop.get('refuted_count', 0)}, open={post_loop.get('open_count', 0)}"
        )
    lines.append("")

    lines.append("## 3) Backfill Explicit depends_on for Top Entrypoints")
    lines.append("")
    backfill = report.get("dependency_backfill_check", {}) if isinstance(report.get("dependency_backfill_check"), dict) else {}
    lines.append(f"- Checked top entrypoints: {backfill.get('top_entrypoints_checked', 0)}")
    lines.append(
        f"- Dependency coverage OK: {backfill.get('coverage_ok_count', 0)}/"
        f"{backfill.get('top_entrypoints_checked', 0)}"
    )
    lines.append("- Rows:")
    for row in backfill.get("rows", []) if isinstance(backfill.get("rows"), list) else []:
        deps = row.get("depends_on", []) if isinstance(row.get("depends_on"), list) else []
        lines.append(
            f"  - {row.get('statement_id', '')} ({row.get('kind', '')}): "
            f"deps={row.get('depends_on_count', 0)} -> {', '.join(str(x) for x in deps) if deps else '[]'}"
        )
    lines.append("")

    lines.append("## 4) Anti-Barrier Program: Keep Coherence-Positive Re-Encodings")
    lines.append("")
    anti = report.get("anti_barrier_coherence_filter", {}) if isinstance(report.get("anti_barrier_coherence_filter"), dict) else {}
    lines.append(f"- Retained (coherence delta >= 0): {anti.get('retained_count', 0)}")
    lines.append(f"- Rejected (coherence delta < 0): {anti.get('rejected_count', 0)}")
    lines.append(f"- Global coherence (original): {float(anti.get('global_coherence_original', 0.0) or 0.0):.6f}")
    if "global_coherence_revised" in anti:
        lines.append(f"- Global coherence (revised): {float(anti.get('global_coherence_revised', 0.0) or 0.0):.6f}")
        lines.append(
            f"- Revised delta: {float(anti.get('global_coherence_delta_revised_minus_original', 0.0) or 0.0):+.6f}"
        )
    if str(anti.get("coherence_positive_phyp_path", "")).strip():
        lines.append(
            f"- Coherence-positive revised PHYP: `{anti.get('coherence_positive_phyp_path', '')}` "
            f"({anti.get('coherence_positive_hypothesis_count', 0)} hypotheses)"
        )
    if str(anti.get("decision", "")).strip():
        lines.append(f"- Decision: {anti.get('decision', '')} ({anti.get('decision_reason', '')})")
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: CLI entrypoint orchestration for this script.
    Contribution: Executes recommendation continuation in a reproducible, logged stage.
    """

    logger = ReasoningLogger("kb-recommended-focus")
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--kb", required=True, help="Path to KB markdown.")
    ap.add_argument("--kb-ref", default="", help="Optional canonical KB reference.")
    ap.add_argument("--artifacts-dir", default="", help="Optional canonical artifacts dir.")
    ap.add_argument("--phyp", default="", help="Optional PHYP path override.")
    ap.add_argument("--hardness", default="", help="Optional hardness JSON override.")
    ap.add_argument("--bridge-plan", default="", help="Optional bridge-plan JSON override.")
    ap.add_argument("--entrypoints", default="", help="Optional entrypoints JSON override.")
    ap.add_argument("--coherence", default="", help="Optional coherence-report JSON override.")
    ap.add_argument("--coherence-revised", default="", help="Optional revised coherence-report JSON override.")
    ap.add_argument("--hypothesis-loop", default="", help="Optional hypothesis-loop JSON for post-loop summary.")
    ap.add_argument("--round-evidence-out", default="", help="Optional round-evidence output file path.")
    ap.add_argument("--output-json", default="", help="Optional output report JSON path.")
    ap.add_argument("--output-md", default="", help="Optional output report markdown path.")
    ap.add_argument(
        "--output-coherence-positive-phyp",
        default="",
        help="Optional output path for coherence-positive PHYP subset.",
    )
    ap.add_argument("--max-bridge-tests", type=int, default=12)
    args = ap.parse_args()

    repo = Path(__file__).resolve().parents[4]
    kb_path = Path(args.kb)
    if not kb_path.exists():
        log_path = logger.finalize("error", summary=f"KB not found: {kb_path}")
        print(f"[LOG] {log_path}", file=sys.stderr)
        raise SystemExit(f"[ERROR] KB not found: {kb_path}")

    try:
        kb_ctx = resolve_kb_reference(kb_path, explicit_kb_ref=args.kb_ref)
    except ValueError as exc:
        log_path = logger.finalize("error", summary=str(exc))
        print(f"[LOG] {log_path}", file=sys.stderr)
        raise SystemExit(f"[ERROR] {exc}")
    kb_ref = str(kb_ctx.get("kb_ref", "")).strip()
    artifacts_dir = canonical_artifacts_dir(repo, kb_ref)
    if args.artifacts_dir:
        requested = Path(args.artifacts_dir)
        if not requested.is_absolute():
            requested = (repo / requested).resolve()
        if requested != artifacts_dir:
            log_path = logger.finalize(
                "error",
                summary=(
                    "Non-canonical artifacts directory rejected. "
                    f"expected={artifacts_dir} requested={requested}"
                ),
            )
            print(f"[LOG] {log_path}", file=sys.stderr)
            raise SystemExit(
                "[ERROR] artifacts are associated with the reference KB name. "
                f"Use canonical path: {artifacts_dir}"
            )

    phyp_path = Path(args.phyp) if args.phyp else repo / "phyp" / f"{kb_ref}.proof-hypotheses.yaml"
    hardness_path = Path(args.hardness) if args.hardness else artifacts_dir / "epistemic-hardness.json"
    bridge_plan_path = Path(args.bridge_plan) if args.bridge_plan else artifacts_dir / "bridge-plan.json"
    entrypoints_path = Path(args.entrypoints) if args.entrypoints else artifacts_dir / "entrypoints.json"
    coherence_path = Path(args.coherence) if args.coherence else artifacts_dir / "coherence-report.json"
    coherence_revised_path = Path(args.coherence_revised) if args.coherence_revised else artifacts_dir / "coherence-report.revised.json"
    hypothesis_loop_path = Path(args.hypothesis_loop) if args.hypothesis_loop else artifacts_dir / "hypothesis-refutation-loop.json"
    round_evidence_out = Path(args.round_evidence_out) if args.round_evidence_out else artifacts_dir / "round-evidence" / "round-1.json"
    output_json = Path(args.output_json) if args.output_json else artifacts_dir / "recommended-focus-execution.json"
    output_md = Path(args.output_md) if args.output_md else artifacts_dir / "recommended-focus-execution.md"
    output_positive_phyp = (
        Path(args.output_coherence_positive_phyp)
        if args.output_coherence_positive_phyp
        else artifacts_dir / "phyp.revised.coherence-positive.yaml"
    )

    logger.step(
        "Parsed recommended-focus arguments",
        "\n".join(
            [
                f"kb={kb_path}",
                f"kb_ref={kb_ref}",
                f"artifacts_dir={artifacts_dir}",
                f"phyp={phyp_path}",
                f"hardness={hardness_path}",
                f"bridge_plan={bridge_plan_path}",
                f"entrypoints={entrypoints_path}",
                f"coherence={coherence_path}",
                f"coherence_revised={coherence_revised_path}",
                f"hypothesis_loop={hypothesis_loop_path}",
                f"round_evidence_out={round_evidence_out}",
                f"output_json={output_json}",
                f"output_md={output_md}",
                f"output_coherence_positive_phyp={output_positive_phyp}",
                f"max_bridge_tests={max(1, args.max_bridge_tests)}",
            ]
        ),
    )

    for path in [phyp_path, hardness_path, bridge_plan_path, entrypoints_path, coherence_path]:
        if not path.exists():
            log_path = logger.finalize("error", summary=f"Missing input: {path}")
            print(f"[LOG] {log_path}", file=sys.stderr)
            raise SystemExit(f"[ERROR] Missing input: {path}")

    statements = _load_statements(kb_path)
    phyp = _load_phyp(phyp_path)
    hardness = _load_json(hardness_path)
    bridges = _load_json(bridge_plan_path)
    entrypoints = _load_json(entrypoints_path)
    coherence = _load_json(coherence_path)
    coherence_revised = _load_json(coherence_revised_path) if coherence_revised_path.exists() else {}
    top_two = _top_two_hardness(hardness)

    focus_statement_ids: set[str] = set()
    for row in top_two:
        for sid in row.get("evidence_ids", []) if isinstance(row.get("evidence_ids"), list) else []:
            sid_s = str(sid).strip()
            if sid_s:
                focus_statement_ids.add(sid_s)

    scratch = _scratch_evidence(
        bridges=bridges,
        phyp=phyp,
        statements=statements,
        focus_statement_ids=focus_statement_ids,
        max_bridge_tests=max(1, args.max_bridge_tests),
    )
    round_evidence_out.parent.mkdir(parents=True, exist_ok=True)
    round_evidence_out.write_text(json.dumps({"hypotheses": scratch["evidence_rows"]}, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    dep_cov = _entrypoint_dependency_coverage(entrypoints=entrypoints, statements=statements, top_k=8)
    anti = _barrier_coherence_filter(phyp=phyp, coherence=coherence, coherence_revised=coherence_revised)

    if coherence_revised:
        rev_hyp_rows = coherence_revised.get("hypothesis_coherence", []) if isinstance(coherence_revised.get("hypothesis_coherence"), list) else []
        rev_idx = {str(row.get("hypothesis_id", "")).strip(): row for row in rev_hyp_rows if isinstance(row, dict)}
        kept: list[dict[str, Any]] = []
        for hyp in phyp.get("hypotheses", []) if isinstance(phyp.get("hypotheses"), list) else []:
            if not isinstance(hyp, dict):
                continue
            hid = str(hyp.get("id", "")).strip()
            if not hid:
                continue
            delta = float((rev_idx.get(hid, {}) or {}).get("coherence_delta_global", 0.0) or 0.0)
            if delta >= 0.0:
                kept.append(hyp)
        positive_payload = dict(phyp)
        positive_payload["hypotheses"] = kept
        output_positive_phyp.parent.mkdir(parents=True, exist_ok=True)
        output_positive_phyp.write_text(yaml.safe_dump(positive_payload, sort_keys=False), encoding="utf-8")
        anti["coherence_positive_phyp_path"] = str(output_positive_phyp)
        anti["coherence_positive_hypothesis_count"] = len(kept)

    report: dict[str, Any] = {
        "kb_ref": kb_ref,
        "top2_hardness_elements": [
            {
                "name": str(row.get("name", "")).strip(),
                "severity": str(row.get("severity", "")).strip(),
                "score": float(row.get("score", 0.0) or 0.0),
                "evidence_ids": [str(x).strip() for x in row.get("evidence_ids", []) if str(x).strip()]
                if isinstance(row.get("evidence_ids"), list)
                else [],
            }
            for row in top_two
        ],
        "scratch_dependency_tests": {
            "selected_bridge_hypotheses": len(scratch["selected"]),
            "round_evidence_path": str(round_evidence_out),
            "deduce_class_counts": scratch["counts"],
        },
        "dependency_backfill_check": dep_cov,
        "anti_barrier_coherence_filter": anti,
    }

    if hypothesis_loop_path.exists():
        hypothesis_loop = _load_json(hypothesis_loop_path)
        final_summary = hypothesis_loop.get("final_summary", {}) if isinstance(hypothesis_loop.get("final_summary"), dict) else {}
        report["scratch_dependency_tests"]["post_loop"] = {
            "supported_count": int(final_summary.get("supported_count", 0) or 0),
            "refuted_count": int(final_summary.get("refuted_count", 0) or 0),
            "open_count": int(final_summary.get("open_count", 0) or 0),
            "hypothesis_loop_json": str(hypothesis_loop_path),
        }

    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_md.parent.mkdir(parents=True, exist_ok=True)
    output_json.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    output_md.write_text(_to_markdown(report), encoding="utf-8")

    logger.add_output("recommended_focus_json", output_json)
    logger.add_output("recommended_focus_md", output_md)
    logger.add_output("round_evidence_json", round_evidence_out)
    if str(anti.get("coherence_positive_phyp_path", "")).strip():
        logger.add_output("coherence_positive_phyp", Path(str(anti.get("coherence_positive_phyp_path"))))

    logger.step(
        "Executed recommended-focus continuation",
        "\n".join(
            [
                "top2_hardness="
                + "; ".join(
                    f"{str(row.get('name', '')).strip()}:{str(row.get('severity', '')).strip()}:{float(row.get('score', 0.0) or 0.0):.4f}"
                    for row in report.get("top2_hardness_elements", [])
                ),
                "scratch_counts="
                + ",".join(
                    [
                        f"entailed={report.get('scratch_dependency_tests', {}).get('deduce_class_counts', {}).get('entailed', 0)}",
                        f"conditional={report.get('scratch_dependency_tests', {}).get('deduce_class_counts', {}).get('conditionally-entailed', 0)}",
                        f"not_derived={report.get('scratch_dependency_tests', {}).get('deduce_class_counts', {}).get('not-derived', 0)}",
                    ]
                ),
                f"dependency_coverage={report.get('dependency_backfill_check', {}).get('coverage_ok_count', 0)}/"
                f"{report.get('dependency_backfill_check', {}).get('top_entrypoints_checked', 0)}",
                f"anti_barrier_retained={report.get('anti_barrier_coherence_filter', {}).get('retained_count', 0)}",
                f"anti_barrier_rejected={report.get('anti_barrier_coherence_filter', {}).get('rejected_count', 0)}",
            ]
        ),
    )

    print(f"[OK] Wrote recommended-focus JSON: {output_json}")
    print(f"[OK] Wrote recommended-focus Markdown: {output_md}")
    print(f"[OK] Wrote round evidence: {round_evidence_out}")
    if str(anti.get('coherence_positive_phyp_path', '')).strip():
        print(f"[OK] Wrote coherence-positive PHYP: {anti.get('coherence_positive_phyp_path', '')}")
    log_path = logger.finalize("success", summary="Executed recommended-focus continuation outputs.")
    print(f"[LOG] {log_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
