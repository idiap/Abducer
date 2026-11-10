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

"""Generate a paper-style macro-proof state report for the current KB route."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

_COMMON_DIR = Path(__file__).resolve().parents[3] / "common"
if str(_COMMON_DIR) not in sys.path:
    sys.path.insert(0, str(_COMMON_DIR))

from kb_context import kb_ref_from_artifacts_dir
from proof_queue import load_proof_queue
from reasoning_log import ReasoningLogger
from statement_text import load_statement_index
from statement_text import normalize_math_text
from statement_text import statement_excerpt


def _load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    payload = json.loads(path.read_text(encoding="utf-8"))
    return payload if isinstance(payload, dict) else {}


def _ensure_dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _ensure_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def _clean_text(value: Any) -> str:
    if value is None:
        return ""
    return " ".join(str(value).strip().split())


def _paperize_text(value: Any) -> str:
    text = _clean_text(value)
    replacements = {
        "PclassneqNP": "P != NP",
        "Pclass": "P",
        "NP-not-in-P/poly": "NP not in P/poly",
        "xin": "x in",
        "LinNP": "L in NP",
        "AinNP": "A in NP",
        "emph ": "",
        "mathrm SAT": "SAT",
    }
    for src, dst in replacements.items():
        text = text.replace(src, dst)
    return " ".join(text.split())


def _first_nonempty(*values: Any) -> str:
    for value in values:
        text = _clean_text(value)
        if text:
            return text
    return ""


def _safe_float(value: Any, default: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _safe_int(value: Any, default: int = 0) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _truncate(value: Any, limit: int = 240) -> str:
    text = _clean_text(value)
    if len(text) <= limit:
        return text
    cut = text[: max(0, limit - 3)].rstrip()
    if " " in cut:
        cut = cut.rsplit(" ", 1)[0]
    return cut + "..."


def _latex_escape(value: Any) -> str:
    text = _clean_text(value)
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
    text = text.replace("->", r"$\rightarrow$ ")
    text = text.replace("`", "'")
    return text


def _candidate_engine_paths() -> list[Path]:
    roots = [
        Path(os.environ.get("LOCALAPPDATA", "")) / "Programs" / "MiKTeX" / "miktex" / "bin" / "x64",
        Path(os.environ.get("PROGRAMFILES", "")) / "MiKTeX" / "miktex" / "bin" / "x64",
        Path.home() / "AppData" / "Local" / "Programs" / "MiKTeX" / "miktex" / "bin" / "x64",
    ]
    return [path for path in roots if str(path)]


def _find_latex_engine(preferred: str = "auto") -> list[str]:
    candidates = ["xelatex", "pdflatex", "lualatex"] if preferred == "auto" else [preferred, "pdflatex", "xelatex", "lualatex"]
    seen: set[str] = set()
    ordered = [name for name in candidates if not (name in seen or seen.add(name))]
    for name in ordered:
        found = shutil.which(name)
        if found:
            return [found]
        for root in _candidate_engine_paths():
            path = root / f"{name}.exe"
            if path.exists():
                return [str(path)]
    raise FileNotFoundError("No LaTeX engine found. Checked xelatex/pdflatex/lualatex and common MiKTeX locations.")


def compile_pdf(tex_path: Path, pdf_path: Path, preferred_engine: str = "auto") -> Path:
    engine = _find_latex_engine(preferred_engine)
    workdir = tex_path.parent
    cmd = engine + ["-interaction=nonstopmode", "-halt-on-error", tex_path.name]
    for _ in range(2):
        result = subprocess.run(
            cmd,
            cwd=workdir,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
        if result.returncode != 0:
            raise RuntimeError(
                f"LaTeX compilation failed with engine {engine[0]}:\n{result.stdout}\n{result.stderr}"
            )
    built_pdf = workdir / tex_path.with_suffix(".pdf").name
    if built_pdf != pdf_path:
        pdf_path.write_bytes(built_pdf.read_bytes())
    for suffix in (".aux", ".log", ".out", ".toc"):
        candidate = workdir / tex_path.with_suffix(suffix).name
        if candidate.exists():
            candidate.unlink()
    return pdf_path


def _statement_row(statement_index: dict[str, dict[str, Any]], statement_id: str, *, fallback_title: str = "") -> dict[str, str]:
    statement = _ensure_dict(statement_index.get(statement_id))
    manual_excerpt = {
        "st.def.item": "P is the class of languages decidable by deterministic polynomial-time Turing machines.",
        "st.def.item-2": "NP is the class of languages whose yes instances admit polynomial-size certificates verifiable in polynomial time.",
        "st.def.np-completeness": "A language is NP-complete if it lies in NP and every language in NP polynomial-time many-one reduces to it.",
        "st.thm.cook-levin-sat-is-np-complete-cook1971": "SAT is NP-complete.",
        "st.def.item-5": "P/poly is the class of languages decided by polynomial-size Boolean circuit families, equivalently polynomial-time computation with polynomial-length advice.",
        "st.thm.nonuniform-separation-target": "If NP is not contained in P/poly, then P != NP.",
    }.get(statement_id, "")
    excerpt = _first_nonempty(
        manual_excerpt,
        _paperize_text(statement_excerpt(statement, limit=420)),
        _paperize_text(normalize_math_text(statement.get("informal"))),
        _paperize_text(normalize_math_text(statement.get("latex"))),
    )
    return {
        "statement_id": statement_id,
        "title": _first_nonempty(statement.get("title"), statement.get("name"), fallback_title, statement_id),
        "excerpt": excerpt,
    }


def _normalize_bridges(expert: dict[str, Any]) -> list[dict[str, Any]]:
    bridges = [row for row in _ensure_list(expert.get("bridge_portfolio")) if isinstance(row, dict)]
    bridges.sort(key=lambda row: _safe_float(row.get("priority")), reverse=True)
    return bridges


def _sketch_index(proof_sketches: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {
        _clean_text(row.get("bridge_id")): row
        for row in _ensure_list(proof_sketches.get("proof_sketches"))
        if isinstance(row, dict) and _clean_text(row.get("bridge_id"))
    }


def _queue_frontier(queue: dict[str, Any], limit: int = 3) -> list[dict[str, Any]]:
    entries = [row for row in _ensure_list(queue.get("entries")) if isinstance(row, dict)]
    entries = [
        row
        for row in entries
        if _clean_text(row.get("status")).lower() in {"pending", "in_progress"}
    ]
    entries.sort(key=lambda row: _safe_float(row.get("priority")), reverse=True)
    return entries[:limit]


def _stringify_lemma_rows(rows: list[Any], *, limit: int = 4) -> list[str]:
    out: list[str] = []
    for row in rows[:limit]:
        if isinstance(row, dict):
            out.append(_first_nonempty(row.get("statement"), row.get("requirement"), row.get("objective")))
        else:
            out.append(_clean_text(row))
    return [item for item in out if item]


def _route_statement_reference(
    statement_index: dict[str, dict[str, Any]],
    statement_id: Any,
    *,
    role: str,
    fallback_excerpt: Any = "",
    fallback_title: str = "",
) -> dict[str, str]:
    statement_id_s = _clean_text(statement_id)
    row = _statement_row(statement_index, statement_id_s, fallback_title=fallback_title)
    if not row.get("excerpt") and _clean_text(fallback_excerpt):
        row["excerpt"] = _paperize_text(fallback_excerpt)
    row["role"] = role
    return row


def _dedupe_references(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    seen: set[str] = set()
    out: list[dict[str, str]] = []
    for row in rows:
        if not isinstance(row, dict):
            continue
        statement_id = _clean_text(row.get("statement_id"))
        key = statement_id or f"{_clean_text(row.get('role'))}|{_clean_text(row.get('title'))}"
        if key in seen:
            continue
        seen.add(key)
        out.append(row)
    return out


def build_report(*, kb_path: Path, artifacts_dir: Path) -> dict[str, Any]:
    kb_ref = kb_ref_from_artifacts_dir(artifacts_dir)
    statement_index = load_statement_index(kb_path)
    expert = _load_json(artifacts_dir / "expert-hypothesis-paper.json")
    proof_sketches = _load_json(artifacts_dir / "proof-sketches.json")
    hypothesis_evaluation = _load_json(artifacts_dir / "hypothesis-evaluation.json")
    queue = load_proof_queue(artifacts_dir / "proof-queue.json", kb_ref=kb_ref)

    bridges = _normalize_bridges(expert)
    bridge = bridges[0] if bridges else {}
    supporting = bridges[1:3]
    sketches = _sketch_index(proof_sketches)
    sketch = _ensure_dict(sketches.get(_clean_text(bridge.get("bridge_id"))))
    delta = _ensure_dict(bridge.get("statement_delta"))
    summary = _ensure_dict(hypothesis_evaluation.get("summary"))
    verdict_counts = _ensure_dict(summary.get("verdict_counts"))
    queue_frontier = _queue_frontier(queue)

    grounding_statements = [
        _statement_row(statement_index, "st.def.item", fallback_title="Definition of P"),
        _statement_row(statement_index, "st.def.item-2", fallback_title="Definition of NP"),
        _statement_row(statement_index, "st.def.np-completeness", fallback_title="Definition of NP-completeness"),
        _statement_row(statement_index, "st.thm.cook-levin-sat-is-np-complete-cook1971", fallback_title="Cook-Levin"),
        _statement_row(statement_index, "st.def.item-5", fallback_title="Definition of P/poly"),
        _statement_row(statement_index, "st.thm.nonuniform-separation-target", fallback_title="Nonuniform separation target"),
    ]
    grounding_statements = [row for row in grounding_statements if row.get("excerpt")]
    nonuniform_target = next(
        (row for row in grounding_statements if row.get("statement_id") == "st.thm.nonuniform-separation-target"),
        {"statement_id": "st.thm.nonuniform-separation-target", "title": "Nonuniform separation target", "excerpt": "If NP not in P/poly, then P != NP."},
    )

    proof_outline = _stringify_lemma_rows(_ensure_list(sketch.get("proof_outline_steps")))
    candidate_lemmas = _stringify_lemma_rows(_ensure_list(sketch.get("candidate_lemmas")) or _ensure_list(bridge.get("candidate_lemmas")))
    proof_obligations = _stringify_lemma_rows(_ensure_list(sketch.get("proof_obligations")) or _ensure_list(bridge.get("proof_obligations")))
    bridge_object = _first_nonempty(bridge.get("abstraction_label"), bridge.get("conjectured_object"))
    sketch_object = _clean_text(sketch.get("conjectured_object"))
    consistency_note = ""
    if bridge_object and sketch_object and bridge_object != sketch_object:
        consistency_note = (
            f"The bridge portfolio names the carrier as `{bridge_object}`, while the selected proof sketch "
            f"currently operationalizes the route through `{sketch_object}`. This is an unresolved representation "
            "shift inside the current macro-proof state, not a proved equivalence."
        )

    supporting_routes = []
    for item in supporting:
        item_delta = _ensure_dict(item.get("statement_delta"))
        supporting_routes.append(
            {
                "bridge_id": _clean_text(item.get("bridge_id")),
                "priority": _safe_float(item.get("priority")),
                "route_synopsis": _paperize_text(item.get("route_synopsis")),
                "candidate_object": _first_nonempty(item.get("abstraction_label"), item.get("conjectured_object")),
                "carrier_kind": _paperize_text(item.get("carrier_kind")),
                "target_claim_focus": _paperize_text(_first_nonempty(item_delta.get("target_claim_focus"), item.get("target_consequence_schema"))),
                "missing_route_lemma": _paperize_text(item.get("missing_route_lemma")),
                "target_statement_id": _clean_text(item.get("target_statement_id")),
            }
        )

    references = _dedupe_references(
        grounding_statements
        + [
            _route_statement_reference(
                statement_index,
                bridge.get("source_statement_id"),
                role="Leading-route source statement",
                fallback_excerpt=_first_nonempty(delta.get("source_theorem_excerpt"), bridge.get("source_excerpt"), bridge.get("source_preview")),
                fallback_title="Leading-route source",
            ),
            _route_statement_reference(
                statement_index,
                bridge.get("target_statement_id"),
                role="Leading-route target statement",
                fallback_excerpt=_first_nonempty(delta.get("target_theorem_excerpt"), bridge.get("target_excerpt"), bridge.get("target_preview")),
                fallback_title="Leading-route target",
            ),
        ]
        + [
            _route_statement_reference(
                statement_index,
                item.get("target_statement_id"),
                role="Supporting-route target statement",
                fallback_excerpt=item.get("target_claim_focus"),
                fallback_title=item.get("bridge_id"),
            )
            for item in supporting_routes
            if _clean_text(item.get("target_statement_id"))
        ]
    )

    route_status_clause = "The route is therefore being presented as a conditional theorem programme rather than as a proof."
    if consistency_note:
        route_status_clause += " A remaining abstraction defect is the mismatch between the witness-family presentation and the Gap-MCSP operationalization."
    paper_narrative = {
        "introduction": (
            "This document should be read as a mathematical programme note. "
            "Its purpose is to explain how the current search state grounds the main conjecture in a sharper nonuniform target and to isolate the minimal theorem package still missing."
        ),
        "reduction_strategy": (
            "The reduction strategy is deliberately high-level: prove a hardness-magnification route to `NP not in P/poly`, then close the main conjecture through the already available nonuniform implication. "
            "The mathematical substance therefore sits in the magnification bridge, not in the final reduction step."
        ),
        "leading_route_narrative": (
            f"The leading route centers on `{_clean_text(bridge.get('bridge_id'))}` and treats `{bridge_object}` as the bridge object intended to carry the source lower-bound regime into the target separation regime. "
            f"{route_status_clause}"
        ),
        "frontier_narrative": (
            "The current frontier should be interpreted as a small family of theorem-sized obligations, not as an execution backlog. "
            "Each queued item isolates one mathematically inspectable route conjecture whose proof or failure would materially change the state of the macro-proof."
        ),
    }

    return {
        "metadata": {
            "kb_ref": kb_ref,
            "generated_utc": dt.datetime.now(dt.UTC).isoformat(),
            "expert_bridge_count": len(bridges),
            "proof_sketch_count": len(_ensure_list(proof_sketches.get("proof_sketches"))),
            "queue_entry_count": len(_ensure_list(queue.get("entries"))),
            "queue_pending_count": _safe_int(_ensure_dict(queue.get("metadata")).get("pending_count")),
        },
        "main_conjecture": {
            "title": "P versus NP",
            "core_claim": "P != NP",
            "route_target_claim": "NP not in P/poly",
            "grounding_statement_id": nonuniform_target.get("statement_id", ""),
            "grounding_statement_title": nonuniform_target.get("title", ""),
            "grounding_implication": _paperize_text(nonuniform_target.get("excerpt", "If NP is not contained in P/poly, then P != NP.")),
            "narrative": "The current macro-proof does not try to prove P != NP directly. It organizes the search around a stronger nonuniform separation claim, then grounds the main conjecture by the implication NP not in P/poly implies P != NP.",
        },
        "paper_narrative": paper_narrative,
        "grounding_statements": grounding_statements,
        "conditional_macro_proof": {
            "proposition": _paperize_text(_first_nonempty(
                bridge.get("conditional_proposition"),
                "If the leading magnification bridge is realized and yields NP not in P/poly, then P != NP follows by the nonuniform separation target.",
            )),
            "implication_chain": [
                "Start from the hardness-magnification program: a barely nontrivial lower bound for an explicit MCSP-type problem in a weak model may amplify into a major separation consequence.",
                _paperize_text(_first_nonempty(
                    bridge.get("conditional_proposition"),
                    "If the leading bridge object is realized, the route aims to force NP not in P/poly.",
                )),
                "Invoke the grounding implication from the KB: if NP not in P/poly, then P != NP.",
            ],
            "status_note": "This is a conditional macro-proof program. The central unresolved step is the route-specific bridge lemma, not the final grounding implication to P != NP.",
        },
        "leading_route": {
            "bridge_id": _clean_text(bridge.get("bridge_id")),
            "priority": _safe_float(bridge.get("priority")),
            "route_synopsis": _paperize_text(bridge.get("route_synopsis")),
            "source_statement_id": _clean_text(bridge.get("source_statement_id")),
            "target_statement_id": _clean_text(bridge.get("target_statement_id")),
            "source_excerpt": _paperize_text(_first_nonempty(delta.get("source_theorem_excerpt"), bridge.get("source_excerpt"), bridge.get("source_preview"))),
            "target_excerpt": _paperize_text(_first_nonempty(delta.get("target_theorem_excerpt"), bridge.get("target_excerpt"), bridge.get("target_preview"))),
            "source_claim_focus": _paperize_text(_first_nonempty(delta.get("source_claim_focus"), bridge.get("support_antecedent_schema"))),
            "target_claim_focus": _paperize_text(_first_nonempty(delta.get("target_claim_focus"), bridge.get("target_consequence_schema"))),
            "model_shift": _paperize_text(delta.get("model_shift")),
            "threshold_shift": _paperize_text(delta.get("threshold_shift")),
            "consequence_shift": _paperize_text(delta.get("consequence_shift")),
            "candidate_object": bridge_object,
            "carrier_kind": _paperize_text(bridge.get("carrier_kind")),
            "invariant": _paperize_text(bridge.get("preserved_invariant")),
            "family": _paperize_text(bridge.get("proof_strategy_family")),
            "family_rationale": _paperize_text(bridge.get("family_rationale")),
            "conditional_proposition": _paperize_text(bridge.get("conditional_proposition")),
            "route_consistency_note": consistency_note,
            "mathematical_assumptions": [_paperize_text(item) for item in _ensure_list(bridge.get("mathematical_assumptions")) if _clean_text(item)],
            "proof_obligations": [_paperize_text(item) for item in proof_obligations],
            "candidate_lemmas": [_paperize_text(item) for item in candidate_lemmas],
            "proof_outline": [_paperize_text(item) for item in proof_outline],
            "missing_route_lemma": _paperize_text(bridge.get("missing_route_lemma")),
            "negative_route": _paperize_text(bridge.get("negative_route")),
            "failure_diagnosis": _paperize_text(bridge.get("failure_diagnosis")),
        },
        "supporting_routes": supporting_routes,
        "proof_frontier": [
            {
                "queue_id": _clean_text(item.get("queue_id")),
                "title": _clean_text(item.get("title")),
                "priority": _safe_float(item.get("priority")),
                "conjecture_statement": _paperize_text(_first_nonempty(item.get("conjecture_statement"), item.get("claim_text"))),
                "missing_route_lemma": _paperize_text(item.get("missing_route_lemma")),
                "candidate_object": _clean_text(item.get("candidate_object")),
            }
            for item in queue_frontier
        ],
        "references": references,
        "status_assessment": {
            "supported_hypotheses": _safe_int(verdict_counts.get("supported")),
            "inconclusive_hypotheses": _safe_int(verdict_counts.get("inconclusive")),
            "evidence_count": _safe_int(_ensure_dict(hypothesis_evaluation.get("metadata")).get("evidence_count")),
            "queue_pending_count": _safe_int(_ensure_dict(queue.get("metadata")).get("pending_count")),
            "assessment": "The macro-proof has a coherent leading route and a grounded implication to the main conjecture, but it remains conditional. The unresolved mass sits in the bridge object, the route lemma, and the absence of external evidence or discharged proof obligations.",
            "novelty_argument": "The novelty is not a claimed proof of P versus NP. It is a theorem-pair-specific research program: a typed witness object, a preserved invariant, an explicit lemma chain, and a falsification route organized around hardness magnification.",
        },
    }


def render_markdown(report: dict[str, Any]) -> str:
    meta = _ensure_dict(report.get("metadata"))
    main = _ensure_dict(report.get("main_conjecture"))
    narrative = _ensure_dict(report.get("paper_narrative"))
    grounding = [row for row in _ensure_list(report.get("grounding_statements")) if isinstance(row, dict)]
    macro = _ensure_dict(report.get("conditional_macro_proof"))
    leading = _ensure_dict(report.get("leading_route"))
    supporting = [row for row in _ensure_list(report.get("supporting_routes")) if isinstance(row, dict)]
    frontier = [row for row in _ensure_list(report.get("proof_frontier")) if isinstance(row, dict)]
    references = [row for row in _ensure_list(report.get("references")) if isinstance(row, dict)]
    status = _ensure_dict(report.get("status_assessment"))

    lines = [
        f"# Macro-Proof State Report for {meta.get('kb_ref', '')}",
        "",
        "## Abstract",
        "",
        main.get("narrative", ""),
        "The present state is a conditional macro-proof: the main conjecture is grounded, the leading route is explicit, and the remaining gap is localized in a small set of route-specific obligations.",
        "",
        "## Introduction",
        "",
        narrative.get("introduction", ""),
        "",
        "## Reduction Strategy",
        "",
        narrative.get("reduction_strategy", ""),
        "",
        "## Main Conjecture",
        "",
        f"- Core claim: `{main.get('core_claim', '')}`",
        f"- Stronger route target: `{main.get('route_target_claim', '')}`",
        f"- Grounding statement: `{main.get('grounding_statement_id', '')}`",
        f"- Grounding implication: {main.get('grounding_implication', '')}",
        "",
        "## Grounding in the Local KB",
        "",
    ]
    for row in grounding:
        lines.extend(
            [
                f"### {row.get('title', row.get('statement_id', 'Statement'))}",
                "",
                f"- Statement id: `{row.get('statement_id', '')}`",
                f"- Excerpt: {row.get('excerpt', '')}",
                "",
            ]
        )
    lines.extend(
        [
            "## Conditional Macro-Proof",
            "",
            f"- Proposition: {macro.get('proposition', '')}",
            "- Implication chain:",
            *[f"  - {item}" for item in _ensure_list(macro.get("implication_chain")) if _clean_text(item)],
            f"- Status note: {macro.get('status_note', '')}",
            "",
            "## Leading Route",
            "",
            narrative.get("leading_route_narrative", ""),
            "",
            f"- Bridge: `{leading.get('bridge_id', '')}`",
            f"- Priority: {leading.get('priority', 0.0):.3f}",
            f"- Route synopsis: {leading.get('route_synopsis', '')}",
            f"- Source theorem `{leading.get('source_statement_id', '')}`: {leading.get('source_excerpt', '')}",
            f"- Target theorem `{leading.get('target_statement_id', '')}`: {leading.get('target_excerpt', '')}",
            f"- Mathematical delta: {leading.get('source_claim_focus', '')} -> {leading.get('target_claim_focus', '')}",
            f"- Model shift: {leading.get('model_shift', '')}",
            f"- Threshold shift: {leading.get('threshold_shift', '')}",
            f"- Consequence shift: {leading.get('consequence_shift', '')}",
            f"- Candidate object: {leading.get('candidate_object', '')}",
            f"- Carrier kind: {leading.get('carrier_kind', '')}",
            f"- Preserved invariant: {leading.get('invariant', '')}",
            f"- Proof family: {leading.get('family', '')}",
            f"- Family rationale: {leading.get('family_rationale', '')}",
            f"- Conditional proposition: {leading.get('conditional_proposition', '')}",
            *([f"- Cross-stage consistency note: {leading.get('route_consistency_note', '')}"] if _clean_text(leading.get("route_consistency_note")) else []),
            "",
            "### Leading Route Assumptions",
            "",
            *[f"- {item}" for item in _ensure_list(leading.get("mathematical_assumptions")) if _clean_text(item)],
            "",
            "### Leading Route Obligations",
            "",
            *[f"- {item}" for item in _ensure_list(leading.get("proof_obligations")) if _clean_text(item)],
            "",
            "### Lemma Chain",
            "",
            *[f"- {item}" for item in _ensure_list(leading.get("candidate_lemmas")) if _clean_text(item)],
            "",
            "### Proof Outline",
            "",
            *[f"- {item}" for item in _ensure_list(leading.get("proof_outline")) if _clean_text(item)],
            "",
            "### Failure Analysis",
            "",
            f"- Missing route lemma: {leading.get('missing_route_lemma', '')}",
            f"- Negative route: {leading.get('negative_route', '')}",
            f"- Failure diagnosis: {leading.get('failure_diagnosis', '')}",
            "",
            "## Supporting Routes",
            "",
        ]
    )
    if supporting:
        for row in supporting:
            lines.extend(
                [
                    f"### {row.get('bridge_id', 'Bridge')}",
                    "",
                    f"- Priority: {row.get('priority', 0.0):.3f}",
                    f"- Route synopsis: {row.get('route_synopsis', '')}",
                    f"- Candidate object: {row.get('candidate_object', '')}",
                    f"- Carrier kind: {row.get('carrier_kind', '')}",
                    f"- Target focus: {row.get('target_claim_focus', '')}",
                    f"- Missing route lemma: {row.get('missing_route_lemma', '')}",
                    "",
                ]
            )
    else:
        lines.append("- No supporting routes available.")
        lines.append("")

    lines.extend(
        [
            "## Proof Frontier",
            "",
            narrative.get("frontier_narrative", ""),
            "",
        ]
    )
    if frontier:
        for row in frontier:
            lines.extend(
                [
                    f"### {row.get('queue_id', 'Queue Entry')}",
                    "",
                    f"- Title: {row.get('title', '')}",
                    f"- Priority: {row.get('priority', 0.0):.3f}",
                    f"- Candidate object: {row.get('candidate_object', '')}",
                    f"- Conjecture: {row.get('conjecture_statement', '')}",
                    f"- Missing route lemma: {row.get('missing_route_lemma', '')}",
                    "",
                ]
            )
    else:
        lines.append("- No queued proof targets available.")
        lines.append("")

    lines.extend(
        [
            "## Status Assessment",
            "",
            f"- Supported hypotheses: {status.get('supported_hypotheses', 0)}",
            f"- Inconclusive hypotheses: {status.get('inconclusive_hypotheses', 0)}",
            f"- External evidence items: {status.get('evidence_count', 0)}",
            f"- Pending proof-queue items: {status.get('queue_pending_count', 0)}",
            f"- Assessment: {status.get('assessment', '')}",
            f"- Novelty argument: {status.get('novelty_argument', '')}",
            "",
            "## Relevant Local References",
            "",
        ]
    )
    for row in references:
        lines.extend(
            [
                f"- [{row.get('role', 'Reference')}] `{row.get('statement_id', '')}` {row.get('title', '')}".rstrip(),
                f"  {row.get('excerpt', '')}",
            ]
        )
    if not references:
        lines.append("- No local references recorded.")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def render_tex(report: dict[str, Any]) -> str:
    meta = _ensure_dict(report.get("metadata"))
    main = _ensure_dict(report.get("main_conjecture"))
    narrative = _ensure_dict(report.get("paper_narrative"))
    grounding = [row for row in _ensure_list(report.get("grounding_statements")) if isinstance(row, dict)]
    macro = _ensure_dict(report.get("conditional_macro_proof"))
    leading = _ensure_dict(report.get("leading_route"))
    supporting = [row for row in _ensure_list(report.get("supporting_routes")) if isinstance(row, dict)]
    frontier = [row for row in _ensure_list(report.get("proof_frontier")) if isinstance(row, dict)]
    references = [row for row in _ensure_list(report.get("references")) if isinstance(row, dict)]
    status = _ensure_dict(report.get("status_assessment"))

    def _render_items(items: list[Any]) -> str:
        rows = [rf"\item {_latex_escape(item)}" for item in items if _clean_text(item)]
        if not rows:
            return "No items recorded."
        return "\n".join([r"\begin{itemize}[leftmargin=*,itemsep=0.2em]", *rows, r"\end{itemize}"])

    consistency_item = ""
    if _clean_text(leading.get("route_consistency_note")):
        consistency_item = rf"\item Cross-stage consistency note: {_latex_escape(leading.get('route_consistency_note'))}"

    grounding_block = "\n".join(
        [
            "\n".join(
                [
                    rf"\subsection*{{{_latex_escape(row.get('title'))}}}",
                    rf"\textbf{{Statement id.}} \texttt{{{_latex_escape(row.get('statement_id'))}}}",
                    "",
                    _latex_escape(row.get("excerpt")),
                ]
            )
            for row in grounding
        ]
    )

    supporting_block = "\n".join(
        [
            "\n".join(
                [
                    rf"\subsection*{{{_latex_escape(row.get('bridge_id'))}}}",
                    r"\begin{itemize}[leftmargin=*,itemsep=0.2em]",
                    rf"\item Priority: {_safe_float(row.get('priority')):.3f}",
                    rf"\item Route synopsis: {_latex_escape(row.get('route_synopsis'))}",
                    rf"\item Candidate object: {_latex_escape(row.get('candidate_object'))}",
                    rf"\item Carrier kind: {_latex_escape(row.get('carrier_kind'))}",
                    rf"\item Target focus: {_latex_escape(row.get('target_claim_focus'))}",
                    rf"\item Missing route lemma: {_latex_escape(row.get('missing_route_lemma'))}",
                    r"\end{itemize}",
                ]
            )
            for row in supporting
        ]
    ) or "No supporting routes recorded."

    frontier_block = "\n".join(
        [
            "\n".join(
                [
                    rf"\subsection*{{{_latex_escape(row.get('queue_id'))}}}",
                    r"\begin{itemize}[leftmargin=*,itemsep=0.2em]",
                    rf"\item Title: {_latex_escape(row.get('title'))}",
                    rf"\item Priority: {_safe_float(row.get('priority')):.3f}",
                    rf"\item Candidate object: {_latex_escape(row.get('candidate_object'))}",
                    rf"\item Conjecture: {_latex_escape(row.get('conjecture_statement'))}",
                    rf"\item Missing route lemma: {_latex_escape(row.get('missing_route_lemma'))}",
                    r"\end{itemize}",
                ]
            )
            for row in frontier
        ]
    ) or "No queued proof targets available."

    references_block = "\n".join(
        [
            "\n".join(
                [
                    rf"\subsection*{{{_latex_escape(row.get('role') or row.get('title') or row.get('statement_id'))}}}",
                    rf"\textbf{{Statement id.}} \texttt{{{_latex_escape(row.get('statement_id'))}}}",
                    rf"\textbf{{Title.}} {_latex_escape(row.get('title'))}",
                    "",
                    _latex_escape(row.get("excerpt")),
                ]
            )
            for row in references
        ]
    ) or "No local references recorded."

    report_date = dt.datetime.now().strftime("%B %d, %Y")
    return rf"""\documentclass[11pt]{{article}}
\usepackage[margin=1in]{{geometry}}
\usepackage[T1]{{fontenc}}
\usepackage[utf8]{{inputenc}}
\usepackage{{lmodern}}
\usepackage{{enumitem}}
\usepackage{{hyperref}}
\usepackage{{titlesec}}
\setlist[itemize]{{leftmargin=*,itemsep=0.2em,topsep=0.25em}}
\titleformat{{\section}}{{\large\bfseries}}{{\thesection.}}{{0.5em}}{{}}

\title{{Macro-Proof State Report for {_latex_escape(meta.get('kb_ref'))}}}
\author{{Abducer Macro-Proof Paper Writer}}
\date{{{_latex_escape(report_date)}}}

\begin{{document}}
\maketitle

\begin{{abstract}}
{_latex_escape(main.get('narrative'))} The current state is a conditional macro-proof: the main conjecture is grounded, the leading route is explicit, and the unresolved mass is localized in a small family of bridge obligations.
\end{{abstract}}

\section{{Introduction}}
{_latex_escape(narrative.get('introduction'))}

\section{{Reduction Strategy}}
{_latex_escape(narrative.get('reduction_strategy'))}

\section{{Main Conjecture}}
\begin{{itemize}}[leftmargin=*,itemsep=0.2em]
\item Core claim: {_latex_escape(main.get('core_claim'))}
\item Stronger route target: {_latex_escape(main.get('route_target_claim'))}
\item Grounding statement: \texttt{{{_latex_escape(main.get('grounding_statement_id'))}}}
\item Grounding implication: {_latex_escape(main.get('grounding_implication'))}
\end{{itemize}}

\section{{Grounding in the Local KB}}
{grounding_block}

\section{{Conditional Macro-Proof}}
\paragraph{{Proposition}}
{_latex_escape(macro.get('proposition'))}

\paragraph{{Implication Chain}}
{_render_items(_ensure_list(macro.get('implication_chain')))}

\paragraph{{Status Note}}
{_latex_escape(macro.get('status_note'))}

\section{{Leading Route}}
{_latex_escape(narrative.get('leading_route_narrative'))}

\medskip
\begin{{itemize}}[leftmargin=*,itemsep=0.2em]
\item Bridge: \texttt{{{_latex_escape(leading.get('bridge_id'))}}}
\item Priority: {_safe_float(leading.get('priority')):.3f}
\item Route synopsis: {_latex_escape(leading.get('route_synopsis'))}
\item Mathematical delta: {_latex_escape(leading.get('source_claim_focus'))} $\rightarrow$ {_latex_escape(leading.get('target_claim_focus'))}
\item Model shift: {_latex_escape(leading.get('model_shift'))}
\item Threshold shift: {_latex_escape(leading.get('threshold_shift'))}
\item Consequence shift: {_latex_escape(leading.get('consequence_shift'))}
\item Candidate object: {_latex_escape(leading.get('candidate_object'))}
\item Carrier kind: {_latex_escape(leading.get('carrier_kind'))}
\item Preserved invariant: {_latex_escape(leading.get('invariant'))}
\item Proof family: {_latex_escape(leading.get('family'))}
\item Family rationale: {_latex_escape(leading.get('family_rationale'))}
{consistency_item}
\end{{itemize}}

\paragraph{{Source Theorem}}
\texttt{{{_latex_escape(leading.get('source_statement_id'))}}} --- {_latex_escape(_truncate(leading.get('source_excerpt'), 600))}

\paragraph{{Target Theorem}}
\texttt{{{_latex_escape(leading.get('target_statement_id'))}}} --- {_latex_escape(_truncate(leading.get('target_excerpt'), 600))}

\paragraph{{Conditional Proposition}}
{_latex_escape(leading.get('conditional_proposition'))}

\paragraph{{Mathematical Assumptions}}
{_render_items(_ensure_list(leading.get('mathematical_assumptions')))}

\paragraph{{Proof Obligations}}
{_render_items(_ensure_list(leading.get('proof_obligations')))}

\paragraph{{Lemma Chain}}
{_render_items(_ensure_list(leading.get('candidate_lemmas')))}

\paragraph{{Proof Outline}}
{_render_items(_ensure_list(leading.get('proof_outline')))}

\paragraph{{Failure Analysis}}
\begin{{itemize}}[leftmargin=*,itemsep=0.2em]
\item Missing route lemma: {_latex_escape(leading.get('missing_route_lemma'))}
\item Negative route: {_latex_escape(leading.get('negative_route'))}
\item Failure diagnosis: {_latex_escape(leading.get('failure_diagnosis'))}
\end{{itemize}}

\section{{Supporting Routes}}
{supporting_block}

\section{{Proof Frontier}}
{_latex_escape(narrative.get('frontier_narrative'))}

\medskip
{frontier_block}

\section{{Status Assessment}}
\begin{{itemize}}[leftmargin=*,itemsep=0.2em]
\item Supported hypotheses: {_safe_int(status.get('supported_hypotheses'))}
\item Inconclusive hypotheses: {_safe_int(status.get('inconclusive_hypotheses'))}
\item External evidence items: {_safe_int(status.get('evidence_count'))}
\item Pending proof-queue items: {_safe_int(status.get('queue_pending_count'))}
\item Assessment: {_latex_escape(status.get('assessment'))}
\item Novelty argument: {_latex_escape(status.get('novelty_argument'))}
\end{{itemize}}

\section{{Relevant Local References}}
{references_block}

\end{{document}}
"""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--kb", required=True, help="Path to the KB markdown file.")
    parser.add_argument("--artifacts-dir", required=True, help="Artifacts directory for the target problem.")
    parser.add_argument("--no-pdf", action="store_true", help="Skip LaTeX compilation.")
    parser.add_argument("--preferred-engine", default="auto", help="LaTeX engine preference: auto, xelatex, pdflatex, or lualatex.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo_root = Path(__file__).resolve().parents[4]
    logger = ReasoningLogger("kb-macro-proof-paper-writer", repo_root=repo_root)

    kb_path = Path(args.kb).resolve()
    artifacts_dir = Path(args.artifacts_dir).resolve()
    artifacts_dir.mkdir(parents=True, exist_ok=True)

    logger.step(
        "Loaded macro-proof inputs.",
        details=f"KB: {kb_path}\nArtifacts: {artifacts_dir}",
        surface_kind="evidence_loading",
        surface_focus="macro-proof state",
    )

    report = build_report(kb_path=kb_path, artifacts_dir=artifacts_dir)
    logger.step(
        "Built macro-proof report payload.",
        details=(
            f"Leading bridge: {_ensure_dict(report.get('leading_route')).get('bridge_id', '')}\n"
            f"Frontier items: {len(_ensure_list(report.get('proof_frontier')))}"
        ),
        surface_kind="artifact_synthesis",
        surface_focus="macro-proof narrative",
    )

    json_path = artifacts_dir / "macro-proof-state.json"
    md_path = artifacts_dir / "macro-proof-state.md"
    tex_path = artifacts_dir / "macro-proof-state.tex"
    pdf_path = artifacts_dir / "macro-proof-state.pdf"

    json_path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    md_path.write_text(render_markdown(report), encoding="utf-8")
    tex_path.write_text(render_tex(report), encoding="utf-8")

    logger.add_output("macro-proof-state.json", json_path)
    logger.add_output("macro-proof-state.md", md_path)
    logger.add_output("macro-proof-state.tex", tex_path)

    if not args.no_pdf:
        compile_pdf(tex_path, pdf_path, preferred_engine=args.preferred_engine)
        logger.add_output("macro-proof-state.pdf", pdf_path)

    logger.finalize(
        "completed",
        summary=(
            f"Generated macro-proof state report for {_ensure_dict(report.get('metadata')).get('kb_ref', '')} "
            f"with leading bridge {_ensure_dict(report.get('leading_route')).get('bridge_id', '')}."
        ),
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
