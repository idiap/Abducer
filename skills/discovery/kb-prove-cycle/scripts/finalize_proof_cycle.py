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

"""Finalize a proof attempt, update InformalMathLib, and refresh proof-cycle summary."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

_COMMON_DIR = Path(__file__).resolve().parents[3] / "common"
if str(_COMMON_DIR) not in sys.path:
    sys.path.insert(0, str(_COMMON_DIR))

from kb_context import canonical_artifacts_dir
from discovery_branch_queue import discovery_branch_paths
from discovery_branch_queue import load_discovery_branch_state
from discovery_branch_queue import materialize_discovery_branches
from discovery_branch_queue import save_discovery_branch_state
from discovery_branch_queue import write_discovery_branch_dossiers
from high_reward_watch import append_high_reward_signal
from high_reward_watch import high_reward_watch_paths
from high_reward_watch import load_high_reward_watch
from high_reward_watch import save_high_reward_watch
from inference_diagnosis import refresh_attempt_inference_diagnosis
from problem_mathlib import append_mathlib_result
from problem_mathlib import load_mathlib_index
from problem_mathlib import mathlib_paths
from problem_mathlib import render_mathlib_catalog
from problem_mathlib import write_mathlib_entry_file
from problem_mathlib import write_mathlib_result_file
from proof_queue import enqueue_entries
from proof_queue import finalize_queue_entry
from proof_queue import load_proof_queue
from proof_queue import make_queue_key
from proof_queue import proof_queue_paths
from proof_queue import save_proof_queue
from reasoning_log import ReasoningLogger
from start_proof_cycle import render_attempt_markdown

from generate_proof_queue_report import compile_pdf
from generate_proof_cycle_summary import build_summary
from generate_proof_cycle_summary import write_summary


TERMINAL_OUTCOMES = {"proved", "disproved", "blocked", "deferred", "prior_art_found"}
EXTERNAL_REFERENCE_TYPES = {"theorem", "definition", "axiom"}
MAJOR_SUBRESULT_GATES = (
    "self_contained_statement",
    "mathematical_inspectability",
    "nontrivial_frontier_relation",
    "independent_value",
)
MAJOR_SUBRESULT_AXES = (
    "frontier_shift",
    "independence",
    "transferability",
    "barrier_clarity",
    "proof_closure",
    "search_compression",
)
MAJOR_SUBRESULT_KEY_AXES = ("frontier_shift", "independence", "barrier_clarity")
MAJOR_SUBRESULT_SCORE_THRESHOLD = 11
DEFAULT_HIGH_REWARD_EXTENSION_CYCLES = 4


def _load_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"Expected JSON object at {path}")
    return payload


def _clean_text(value: Any) -> str:
    return " ".join(str(value or "").strip().split())


def _ensure_dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _ensure_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def _safe_int(value: Any, default: int = 0) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _slugify(text: Any) -> str:
    return re.sub(r"[^a-z0-9]+", "-", _clean_text(text).lower()).strip("-")


def _boolish(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    lowered = _clean_text(value).lower()
    if lowered in {"true", "yes", "y", "1", "pass", "passed"}:
        return True
    if lowered in {"false", "no", "n", "0", "fail", "failed", ""}:
        return False
    return bool(value)


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


def _render_itemize(items: list[str]) -> str:
    rows = [rf"\item {_latex_escape(item)}" for item in items if _clean_text(item)]
    if not rows:
        return "No items were recorded."
    return "\n".join(
        [
            r"\begin{itemize}[leftmargin=*,itemsep=0.2em]",
            *rows,
            r"\end{itemize}",
        ]
    )


def _render_stepwise_argument(steps: list[dict[str, Any]]) -> str:
    rows: list[str] = []
    for row in steps:
        if not isinstance(row, dict):
            continue
        claim = _clean_text(row.get("claim"))
        justification = _clean_text(row.get("justification"))
        depends = [
            _clean_text(value)
            for value in _ensure_list(row.get("depends_on"))
            if _clean_text(value)
        ]
        if not claim and not justification:
            continue
        parts = [rf"\item \textbf{{Claim.}} {_latex_escape(claim)}"]
        if justification:
            parts.append(rf"\textbf{{Justification.}} {_latex_escape(justification)}")
        if depends:
            parts.append(rf"\textbf{{Depends on.}} {_latex_escape(', '.join(depends))}")
        rows.append(" ".join(parts))
    if not rows:
        return "No stepwise argument was recorded."
    return "\n".join(
        [
            r"\begin{enumerate}[leftmargin=*,itemsep=0.35em]",
            *rows,
            r"\end{enumerate}",
        ]
    )


def _normalize_major_subresult_assessment(attempt: dict[str, Any]) -> dict[str, Any]:
    raw = _ensure_dict(attempt.get("major_subresult_assessment"))
    gates_raw = _ensure_dict(raw.get("mandatory_gates"))
    axes_raw = _ensure_dict(raw.get("axes"))
    justifications_raw = _ensure_dict(raw.get("justifications"))
    gates = {
        gate: _boolish(gates_raw.get(gate))
        for gate in MAJOR_SUBRESULT_GATES
    }
    axes = {
        axis: max(0, min(3, _safe_int(axes_raw.get(axis))))
        for axis in MAJOR_SUBRESULT_AXES
    }
    score_total = sum(axes.values())
    gate_pass = all(gates.values())
    key_axis_max = max((axes.get(axis, 0) for axis in MAJOR_SUBRESULT_KEY_AXES), default=0)
    qualifies = gate_pass and score_total >= MAJOR_SUBRESULT_SCORE_THRESHOLD and key_axis_max >= 3
    return {
        "mandatory_gates": gates,
        "axes": axes,
        "justifications": {
            axis: _clean_text(justifications_raw.get(axis))
            for axis in MAJOR_SUBRESULT_AXES
        },
        "overall_judgment": _clean_text(raw.get("overall_judgment")),
        "paper_candidate_title": _clean_text(raw.get("paper_candidate_title")),
        "paper_candidate_summary": _clean_text(raw.get("paper_candidate_summary")),
        "score_total": score_total,
        "score_threshold": MAJOR_SUBRESULT_SCORE_THRESHOLD,
        "gate_pass": gate_pass,
        "key_axis_max": key_axis_max,
        "qualifies": qualifies,
    }


def _next_result_title(target: dict[str, Any], *, outcome: str) -> str:
    """Describe the next dependent task that should exploit a high-value intermediate result."""

    candidate_object = _clean_text(target.get("candidate_object")) or "bridge object"
    target_excerpt = _clean_text(target.get("target_excerpt")) or _clean_text(target.get("target_statement_id"))
    route_lemma = _clean_text(target.get("missing_route_lemma"))
    if outcome == "disproved":
        return _clean_text(
            f"Use the negative subresult around `{candidate_object}` to derive a sharper barrier or route-impossibility theorem"
        )
    return _clean_text(
        f"Use the high-value `{candidate_object}` subresult to discharge the next route theorem toward `{target_excerpt}`"
    )


def _build_high_reward_followup_entry(
    *,
    result: dict[str, Any],
    target: dict[str, Any],
    attempt: dict[str, Any],
    outcome: str,
    signal_id: str,
) -> dict[str, Any]:
    """Build a deterministic proof-queue item that exploits the new intermediate result."""

    candidate_object = _clean_text(target.get("candidate_object")) or "bridge object"
    route_lemma = _clean_text(target.get("missing_route_lemma"))
    target_excerpt = _clean_text(target.get("target_excerpt")) or _clean_text(target.get("target_statement_id"))
    result_statement = _clean_text(result.get("statement"))
    if outcome == "disproved":
        claim_text = _clean_text(
            f"Assuming the negative intermediate result `{result_statement}`, derive the strongest local barrier "
            f"theorem showing why `{candidate_object}` cannot currently realize the route toward `{target_excerpt}`."
        )
    else:
        claim_text = _clean_text(
            f"Using the intermediate theorem `{result_statement}`, prove the next dependent route theorem "
            f"needed to upgrade `{candidate_object}` toward `{target_excerpt}`."
        )
    return {
        "queue_key": make_queue_key(
            bridge_id=_clean_text(target.get("bridge_id")),
            target_statement_id=_clean_text(target.get("target_statement_id")),
            claim_text=claim_text,
            claim_slug=f"high-reward-followup-{_clean_text(result.get('result_id'))}",
        ),
        "title": _next_result_title(target, outcome=outcome),
        "priority": min(0.999, float(target.get("priority", 0.85) or 0.85) + 0.05),
        "bridge_id": _clean_text(target.get("bridge_id")),
        "claim_type": "high-reward-followup",
        "claim_text": claim_text,
        "conjecture_statement": claim_text,
        "source_statement_id": _clean_text(target.get("source_statement_id")),
        "target_statement_id": _clean_text(target.get("target_statement_id")),
        "candidate_object": candidate_object,
        "carrier_kind": _clean_text(target.get("carrier_kind")),
        "preserved_invariant": _clean_text(target.get("preserved_invariant")),
        "proof_strategy_family": _clean_text(target.get("proof_strategy_family")),
        "route_synopsis": _clean_text(target.get("route_synopsis")),
        "missing_route_lemma": route_lemma or _next_result_title(target, outcome=outcome),
        "source_excerpt": _clean_text(target.get("source_excerpt")),
        "target_excerpt": target_excerpt,
        "exploration_policy": "capitalize-on-high-reward-subresult",
        "dependency_result_ids": [_clean_text(result.get("result_id"))],
        "high_reward_signal_id": signal_id,
        "high_reward_origin_queue_id": _clean_text(attempt.get("metadata", {}).get("queue_id")),
        "high_reward_origin_attempt_id": _clean_text(attempt.get("metadata", {}).get("attempt_id")),
    }


def _build_high_reward_discovery_layer(
    *,
    kb_ref: str,
    result: dict[str, Any],
    target: dict[str, Any],
    signal_id: str,
    follow_up_queue_ids: list[str],
    outcome: str,
) -> dict[str, Any]:
    """Build one discovery branch that asks how to capitalize on the high-value subresult."""

    candidate_object = _clean_text(target.get("candidate_object")) or "bridge object"
    target_excerpt = _clean_text(target.get("target_excerpt")) or _clean_text(target.get("target_statement_id"))
    negative = outcome == "disproved"
    branch_slug = _slugify(signal_id) or "high-reward"
    result_statement = _clean_text(result.get("statement"))
    required_move = (
        "Turn the negative intermediate result into a tighter barrier theorem or a route-changing reformulation."
        if negative
        else "Exploit the intermediate result to isolate the smallest remaining abstraction or transfer theorem."
    )
    minimal_theorem_shape = (
        f"If `{result_statement}`, then no admissible realization of `{candidate_object}` can satisfy the current route obligations."
        if negative
        else f"If `{result_statement}`, then it suffices to prove one reduced theorem that upgrades `{candidate_object}` toward `{target_excerpt}`."
    )
    return {
        "layer_id": f"disclayer.{kb_ref}.high-reward.{branch_slug}",
        "layer_kind": "high-reward-followup",
        "target_id": signal_id,
        "target_label": _next_result_title(target, outcome=outcome),
        "routing_priority": 0.995,
        "dispatch_rank": 1,
        "dispatch_round": 1,
        "spawn_reason": "A high-value intermediate result justifies a bounded continuation window.",
        "rationale": _clean_text(
            f"The result `{_clean_text(result.get('title'))}` is strong enough to justify targeted follow-up search "
            f"around `{candidate_object}` without reopening the whole frontier."
        ),
        "linked_queue_ids": follow_up_queue_ids,
        "linked_breakthrough_families": [_clean_text(target.get("breakthrough_family"))] if _clean_text(target.get("breakthrough_family")) else [],
        "linked_obstruction_classes": [_clean_text(target.get("obstruction_class"))] if _clean_text(target.get("obstruction_class")) else [],
        "required_move": required_move,
        "abstraction_required": _clean_text(
            f"Find the smallest additional abstraction, transfer law, or barrier sharpening that lets `{result_statement}` materially change the route."
        ),
        "minimal_theorem_shape": minimal_theorem_shape,
        "system_prompt": _clean_text(
            "Treat the new intermediate result as trusted local progress. Do not rediscover the whole route; "
            "search only for the next theorem or abstraction whose value depends on this result."
        ),
        "user_task": _clean_text(
            f"Given the high-value subresult `{result_statement}`, propose the next theorem-sized dependent task "
            f"that would most efficiently advance `{candidate_object}` toward `{target_excerpt}`."
        ),
        "required_questions": [
            "What exact proof debt became smaller because of the new result?",
            "Which remaining theorem is now the smallest dependent target?",
            "Would a positive continuation or a barrier continuation be more informative next?",
        ],
        "expected_deliverables": [
            "One dependent theorem-shaped claim.",
            "One explanation of why the new result changes the search state.",
            "One stop condition for abandoning this continuation line.",
        ],
        "stop_criteria": [
            "Stop if the branch only restates the existing result.",
            "Stop if no remaining theorem becomes smaller or sharper because of the result.",
            "Stop if the continuation requires reopening unrelated bridge families.",
        ],
        "search_modes": ["mathlib-first", "local-theorem-reduction", "targeted-foundation-search"],
        "anti_patterns": [
            "Do not promote the intermediate result into a claimed full proof.",
            "Do not reopen the whole search frontier without showing dependency on the result.",
        ],
        "sample_theorem_targets": [
            _clean_text(target.get("missing_route_lemma")),
            _clean_text(target.get("target_excerpt")),
        ],
        "external_framework_search": {
            "recommended": False,
            "mode": "local-first",
            "justification": "The continuation should first exploit the newly proved local structure before importing fresh external foundations.",
            "candidate_framework_regions": [],
            "local_prerequisites": [
                "Record how the new intermediate result changes the smallest remaining route obligation.",
            ],
            "query_templates": [],
        },
    }


def _seed_high_reward_followups(
    *,
    repo_root: Path,
    artifacts_dir: Path,
    kb_ref: str,
    queue: dict[str, Any],
    result: dict[str, Any],
    target: dict[str, Any],
    attempt: dict[str, Any],
    outcome: str,
    signal_id: str,
) -> tuple[list[str], list[str]]:
    """Seed one proof and one discovery continuation target from a high-value subresult."""

    follow_up_entry = _build_high_reward_followup_entry(
        result=result,
        target=target,
        attempt=attempt,
        outcome=outcome,
        signal_id=signal_id,
    )
    _added, _updated = enqueue_entries(queue, [follow_up_entry])
    follow_up_prove_queue_ids = [
        _clean_text(row.get("queue_id"))
        for row in _ensure_list(queue.get("entries"))
        if isinstance(row, dict) and _clean_text(row.get("queue_key")) == _clean_text(follow_up_entry.get("queue_key"))
    ]

    branch_json, branch_md = discovery_branch_paths(artifacts_dir)
    branch_state = load_discovery_branch_state(branch_json, kb_ref=kb_ref)
    routing = {
        "metadata": {"kb_ref": kb_ref},
        "discovery_layers": [
            _build_high_reward_discovery_layer(
                kb_ref=kb_ref,
                result=result,
                target=target,
                signal_id=signal_id,
                follow_up_queue_ids=follow_up_prove_queue_ids,
                outcome=outcome,
            )
        ],
    }
    branch_state = materialize_discovery_branches(
        routing=routing,
        existing_state=branch_state,
        artifacts_dir=artifacts_dir,
        activate_top_k=4,
    )
    branch_outputs = write_discovery_branch_dossiers(branch_state, artifacts_dir=artifacts_dir)
    save_discovery_branch_state(branch_state, json_path=branch_json, md_path=branch_md)
    follow_up_discovery_branch_ids = [
        _clean_text(row.get("branch_id"))
        for row in branch_outputs
        if _clean_text(row.get("branch_id")).startswith(f"disclayer.{kb_ref}.high-reward.")
    ]
    return follow_up_prove_queue_ids, follow_up_discovery_branch_ids


def _produced_paper_paths(artifacts_dir: Path, *, result_id: str, title: str) -> tuple[Path, Path]:
    slug = _slugify(title)[:96] or "intermediate-result"
    produced_dir = artifacts_dir / "produced_papers"
    return produced_dir / f"{result_id}-{slug}.tex", produced_dir / f"{result_id}-{slug}.pdf"


def _render_produced_paper_tex(
    *,
    kb_ref: str,
    attempt: dict[str, Any],
    target: dict[str, Any],
    result: dict[str, Any],
    assessment: dict[str, Any],
) -> str:
    proof_attempt = _ensure_dict(attempt.get("proof_attempt"))
    final_assessment = _ensure_dict(attempt.get("final_assessment"))
    local_context = _ensure_dict(attempt.get("local_context"))
    negative_argument = _ensure_dict(proof_attempt.get("negative_argument"))
    web_search_gate = _ensure_dict(attempt.get("web_search_gate"))
    judges = [row for row in _ensure_list(attempt.get("critique_judges")) if isinstance(row, dict)]
    external_references = [row for row in _ensure_list(attempt.get("external_references")) if isinstance(row, dict)]
    assumptions = [_clean_text(item) for item in _ensure_list(proof_attempt.get("assumptions")) if _clean_text(item)]
    local_results = [_clean_text(item) for item in _ensure_list(proof_attempt.get("local_results_used")) if _clean_text(item)]
    obligations = [_clean_text(item) for item in _ensure_list(target.get("proof_obligations")) if _clean_text(item)]
    lemmas = [_clean_text(item) for item in _ensure_list(target.get("candidate_lemmas")) if _clean_text(item)]
    stepwise = [row for row in _ensure_list(proof_attempt.get("stepwise_argument")) if isinstance(row, dict)]
    gate_rows = [
        rf"{_latex_escape(gate.replace('_', ' ').title())} & {'pass' if passed else 'fail'} \\"
        for gate, passed in assessment.get("mandatory_gates", {}).items()
    ]
    axis_rows = [
        rf"{_latex_escape(axis.replace('_', ' ').title())} & {assessment.get('axes', {}).get(axis, 0)} & {_latex_escape(assessment.get('justifications', {}).get(axis, ''))} \\"
        for axis in MAJOR_SUBRESULT_AXES
    ]
    judge_rows = []
    for judge in judges:
        verdict = _clean_text(judge.get("verdict")) or "pending"
        notes = "; ".join(_clean_text(item) for item in _ensure_list(judge.get("notes")) if _clean_text(item))
        blockers = "; ".join(_clean_text(item) for item in _ensure_list(judge.get("blocking_issues")) if _clean_text(item))
        detail = notes or blockers or "No additional notes recorded."
        judge_rows.append(rf"{_latex_escape(judge.get('title'))} & {_latex_escape(verdict)} & {_latex_escape(detail)} \\")
    if not judge_rows:
        judge_rows.append(r"No critique judges recorded & pending & No critique data available. \\")
    reference_rows = [
        rf"\item [Main route source] \texttt{{{_latex_escape(target.get('source_statement_id'))}}}: {_latex_escape(local_context.get('source_excerpt') or target.get('source_excerpt'))}",
        rf"\item [Main route target] \texttt{{{_latex_escape(target.get('target_statement_id'))}}}: {_latex_escape(local_context.get('target_excerpt') or target.get('target_excerpt'))}",
        rf"\item [Queue conjecture] \texttt{{{_latex_escape(result.get('queue_id'))}}}: {_latex_escape(target.get('conjecture_statement') or target.get('claim_text'))}",
    ]
    for row in external_references:
        reference_rows.append(
            rf"\item [External { _latex_escape(row.get('reference_type') or 'reference') }] "
            rf"{_latex_escape(row.get('title'))}: {_latex_escape(row.get('statement'))}"
        )
    title = _clean_text(assessment.get("paper_candidate_title")) or _clean_text(result.get("title")) or "Intermediate Result Paper"
    abstract = _clean_text(assessment.get("paper_candidate_summary")) or _clean_text(result.get("summary")) or _clean_text(final_assessment.get("summary"))
    return rf"""\documentclass[11pt]{{article}}

\usepackage[margin=1in]{{geometry}}
\usepackage[T1]{{fontenc}}
\usepackage[utf8]{{inputenc}}
\usepackage{{lmodern}}
\usepackage{{amsmath,amssymb}}
\usepackage{{booktabs}}
\usepackage{{enumitem}}
\usepackage{{hyperref}}
\usepackage{{longtable}}
\usepackage{{xcolor}}

\hypersetup{{
  colorlinks=true,
  linkcolor=blue!50!black,
  urlcolor=blue!50!black,
  citecolor=blue!50!black,
  pdftitle={{ {_latex_escape(title)} }},
}}

\title{{{_latex_escape(title)}}}
\author{{Neuro-symbolic AI Group\\Idiap Research Institute}}
\date{{}}

\begin{{document}}
\maketitle

\begin{{abstract}}
{_latex_escape(abstract)}
\end{{abstract}}

\section{{Introduction}}
This note records a potentially publishable intermediate result extracted from the current proof cycle for \texttt{{{_latex_escape(kb_ref)}}}. It should be read as a standalone route-level theorem note: the goal is to state the result, explain where it sits in the main programme, and make the informal argument inspectable at the mathematical level rather than at the workflow level.

\section{{Problem Setting}}
\begin{{itemize}}[leftmargin=*,itemsep=0.25em]
\item KB ref: \texttt{{{_latex_escape(kb_ref)}}}
\item Outcome: {_latex_escape(result.get('outcome'))}
\item Queue id: \texttt{{{_latex_escape(result.get('queue_id'))}}}
\item Attempt id: \texttt{{{_latex_escape(result.get('attempt_id'))}}}
\item Bridge: \texttt{{{_latex_escape(target.get('bridge_id'))}}}
\item Route: \texttt{{{_latex_escape(target.get('source_statement_id'))}}} $\rightarrow$ \texttt{{{_latex_escape(target.get('target_statement_id'))}}}
\item Candidate object: {_latex_escape(target.get('candidate_object'))}
\item Carrier kind: {_latex_escape(target.get('carrier_kind'))}
\item Preserved invariant: {_latex_escape(target.get('preserved_invariant'))}
\item Route synopsis: {_latex_escape(target.get('route_synopsis'))}
\end{{itemize}}

\section{{Main Statement}}
\textbf{{Queued conjecture.}} {_latex_escape(target.get('conjecture_statement') or target.get('claim_text'))}

\medskip
\textbf{{Final result statement.}} {_latex_escape(result.get('statement'))}

\medskip
\textbf{{Result summary.}} {_latex_escape(result.get('summary'))}

\section{{Context And Grounding}}
\textbf{{Source excerpt.}} {_latex_escape(local_context.get('source_excerpt') or target.get('source_excerpt'))}

\medskip
\textbf{{Target excerpt.}} {_latex_escape(local_context.get('target_excerpt') or target.get('target_excerpt'))}

\medskip
\textbf{{Route lemma under test.}} {_latex_escape(target.get('missing_route_lemma') or proof_attempt.get('route_lemma_under_test'))}

\section{{Why This Intermediate Result Matters}}
\textbf{{Overall judgment.}} {_latex_escape(assessment.get('overall_judgment') or 'No explicit judgment recorded.')}

\medskip
\textbf{{Relation to the main route.}} {_latex_escape(target.get('conditional_proposition') or target.get('route_synopsis'))}

\section{{Major Subresult Assessment}}
\textbf{{Qualification rule.}} All mandatory gates pass, total score at least {assessment.get('score_threshold', MAJOR_SUBRESULT_SCORE_THRESHOLD)}, and at least one of frontier shift / independence / barrier clarity equals 3.

\medskip
\textbf{{Qualification outcome.}} {'Qualified for produced paper generation.' if assessment.get('qualifies') else 'Did not qualify for produced paper generation.'}

\medskip
\textbf{{Total score.}} {assessment.get('score_total', 0)} / 18

\subsection*{{Mandatory Gates}}
\begin{{tabular}}{{ll}}
\toprule
Gate & Verdict \\
\midrule
{chr(10).join(gate_rows)}
\bottomrule
\end{{tabular}}

\subsection*{{Axis Breakdown}}
\begin{{longtable}}{{p{{0.22\linewidth}}p{{0.08\linewidth}}p{{0.6\linewidth}}}}
\toprule
Axis & Score & Justification \\
\midrule
{chr(10).join(axis_rows)}
\bottomrule
\end{{longtable}}

\section{{Informal Argument Narrative}}
\textbf{{Strategy family.}} {_latex_escape(proof_attempt.get('strategy'))}

\subsection*{{Assumptions}}
{_render_itemize(assumptions)}

\subsection*{{Local Results Used}}
{_render_itemize(local_results)}

\subsection*{{Proof Obligations}}
{_render_itemize(obligations)}

\subsection*{{Candidate Lemmas}}
{_render_itemize(lemmas)}

\subsection*{{Stepwise Argument}}
{_render_stepwise_argument(stepwise)}

\section{{Negative Route And Obstruction Check}}
\textbf{{Designated negative route.}} {_latex_escape(target.get('negative_route') or negative_argument.get('obstruction_candidate'))}

\medskip
\textbf{{Barrier or counterexample analysis.}} {_latex_escape(negative_argument.get('counterexample_or_barrier') or target.get('failure_diagnosis'))}

\medskip
\textbf{{Effect on claim.}} {_latex_escape(negative_argument.get('effect_on_claim') or final_assessment.get('verdict'))}

\section{{Critique Judges}}
\begin{{longtable}}{{p{{0.28\linewidth}}p{{0.14\linewidth}}p{{0.5\linewidth}}}}
\toprule
Judge & Verdict & Notes \\
\midrule
{chr(10).join(judge_rows)}
\bottomrule
\end{{longtable}}

\section{{Epistemic Status}}
\begin{{itemize}}[leftmargin=*,itemsep=0.25em]
\item Novelty assessment: {_latex_escape(final_assessment.get('novelty_assessment'))}
\item Confidence: {_latex_escape(final_assessment.get('confidence'))}
\item Web search used: {_latex_escape(bool(web_search_gate.get('sources')))}
\item External references imported: {_latex_escape(len(_ensure_list(attempt.get('external_references'))))}
\end{{itemize}}

\section{{References}}
\begin{{itemize}}[leftmargin=*,itemsep=0.25em]
{chr(10).join(reference_rows)}
\end{{itemize}}

\end{{document}}
"""


def _maybe_generate_produced_paper(
    *,
    artifacts_dir: Path,
    kb_ref: str,
    attempt: dict[str, Any],
    target: dict[str, Any],
    result: dict[str, Any],
    compile_result_pdf: bool,
    latex_engine: str,
) -> dict[str, Any]:
    assessment = _normalize_major_subresult_assessment(attempt)
    if _clean_text(result.get("outcome")) not in {"proved", "disproved"}:
        return assessment
    if not assessment.get("qualifies"):
        return assessment
    output_tex, output_pdf = _produced_paper_paths(
        artifacts_dir,
        result_id=_clean_text(result.get("result_id")) or "result",
        title=_clean_text(assessment.get("paper_candidate_title")) or _clean_text(result.get("title")),
    )
    output_tex.parent.mkdir(parents=True, exist_ok=True)
    tex_source = _render_produced_paper_tex(
        kb_ref=kb_ref,
        attempt=attempt,
        target=target,
        result=result,
        assessment=assessment,
    )
    output_tex.write_text(tex_source, encoding="utf-8")
    if compile_result_pdf:
        compile_pdf(output_tex, output_pdf, preferred_engine=latex_engine)
    result["produced_paper_tex"] = str(output_tex)
    if compile_result_pdf:
        result["produced_paper_pdf"] = str(output_pdf)
    assessment["produced_paper_tex"] = str(output_tex)
    if compile_result_pdf:
        assessment["produced_paper_pdf"] = str(output_pdf)
    return assessment


def _next_result_id(index: dict[str, Any], *, kb_ref: str) -> str:
    prefix = f"mathlib.{kb_ref}."
    current = 0
    for row in index.get("results", []) if isinstance(index.get("results"), list) else []:
        if not isinstance(row, dict):
            continue
        result_id = _clean_text(row.get("result_id"))
        if not result_id.startswith(prefix):
            continue
        suffix = result_id[len(prefix) :]
        if suffix.isdigit():
            current = max(current, int(suffix))
    return f"{prefix}{current + 1:03d}"


def _next_external_reference_id(index: dict[str, Any], *, kb_ref: str) -> str:
    prefix = f"mathlibref.{kb_ref}."
    current = 0
    for row in index.get("results", []) if isinstance(index.get("results"), list) else []:
        if not isinstance(row, dict):
            continue
        result_id = _clean_text(row.get("result_id"))
        if not result_id.startswith(prefix):
            continue
        suffix = result_id[len(prefix) :]
        if suffix.isdigit():
            current = max(current, int(suffix))
    return f"{prefix}{current + 1:03d}"


def _external_reference_key(reference: dict[str, Any]) -> str:
    return "|".join(
        [
            _clean_text(reference.get("reference_type")).lower(),
            _clean_text(reference.get("title")).lower(),
            _clean_text(reference.get("source_url")).lower(),
            _clean_text(reference.get("statement")).lower(),
        ]
    )


def _normalize_external_references(attempt: dict[str, Any]) -> list[dict[str, Any]]:
    references = attempt.get("external_references", [])
    if not isinstance(references, list):
        return []
    normalized: list[dict[str, Any]] = []
    for row in references:
        if not isinstance(row, dict):
            continue
        reference_type = _clean_text(row.get("reference_type")).lower()
        title = _clean_text(row.get("title"))
        statement = _clean_text(row.get("statement"))
        if reference_type not in EXTERNAL_REFERENCE_TYPES:
            continue
        if not title or not statement:
            continue
        normalized.append(
            {
                "reference_type": reference_type,
                "title": title,
                "statement": statement,
                "source_name": _clean_text(row.get("source_name")),
                "source_url": _clean_text(row.get("source_url")),
                "search_query": _clean_text(row.get("search_query")),
                "used_for": _clean_text(row.get("used_for")),
                "notes": _clean_text(row.get("notes")),
            }
        )
    return normalized


def _persist_external_references(
    *,
    repo_root: Path,
    kb_ref: str,
    mathlib: dict[str, Any],
    attempt: dict[str, Any],
    target: dict[str, Any],
) -> list[str]:
    normalized_refs = _normalize_external_references(attempt)
    if not normalized_refs:
        return []
    existing_by_key = {
        _clean_text(row.get("external_reference_key")): row
        for row in mathlib.get("results", [])
        if isinstance(row, dict) and _clean_text(row.get("external_reference_key"))
    }
    persisted: list[str] = []
    for reference in normalized_refs:
        reference_key = _external_reference_key(reference)
        existing = existing_by_key.get(reference_key)
        result_id = _clean_text(existing.get("result_id")) if isinstance(existing, dict) else ""
        if not result_id:
            result_id = _next_external_reference_id(mathlib, kb_ref=kb_ref)
        result = {
            "result_id": result_id,
            "entry_kind": "external-reference",
            "outcome": "external_reference",
            "queue_id": _clean_text(attempt.get("metadata", {}).get("queue_id")),
            "attempt_id": _clean_text(attempt.get("metadata", {}).get("attempt_id")),
            "bridge_id": _clean_text(target.get("bridge_id")),
            "source_statement_id": _clean_text(target.get("source_statement_id")),
            "target_statement_id": _clean_text(target.get("target_statement_id")),
            "reference_type": reference["reference_type"],
            "title": reference["title"],
            "statement": reference["statement"],
            "summary": (
                f"Imported external {reference['reference_type']} used in proof attempt "
                f"`{_clean_text(attempt.get('metadata', {}).get('attempt_id'))}`."
            ),
            "source_name": reference["source_name"],
            "source_url": reference["source_url"],
            "search_query": reference["search_query"],
            "used_for": reference["used_for"],
            "external_reference_key": reference_key,
            "tags": [
                reference["reference_type"],
                _clean_text(target.get("bridge_id")),
                _clean_text(target.get("target_statement_id")),
            ],
            "web_search_used": bool(reference["source_url"]),
        }
        reference_notes = "\n".join(
            [
                f"Used for: {reference['used_for']}" if reference["used_for"] else "",
                f"Notes: {reference['notes']}" if reference["notes"] else "",
            ]
        ).strip()
        artifact_path = write_mathlib_entry_file(
            repo_root,
            kb_ref=kb_ref,
            result=result,
            proof_markdown=reference_notes,
        )
        result["artifact_path"] = str(artifact_path)
        append_mathlib_result(mathlib, result)
        existing_by_key[reference_key] = result
        persisted.append(result_id)
    return persisted


def _validate_attempt_for_terminal_outcome(attempt: dict[str, Any], *, outcome: str) -> None:
    if outcome not in TERMINAL_OUTCOMES:
        raise ValueError(f"Unsupported outcome `{outcome}`.")
    if outcome in {"proved", "disproved", "prior_art_found"}:
        proof_attempt = attempt.get("proof_attempt", {})
        if not isinstance(proof_attempt, dict):
            raise ValueError("Attempt is missing `proof_attempt`.")
        result_statement = _clean_text(proof_attempt.get("result_statement"))
        result_summary = _clean_text(proof_attempt.get("result_summary"))
        if not result_statement:
            raise ValueError("Terminal positive/negative outcomes require `proof_attempt.result_statement`.")
        if not result_summary:
            raise ValueError("Terminal positive/negative outcomes require `proof_attempt.result_summary`.")
        judges = attempt.get("critique_judges", [])
        if not isinstance(judges, list) or not judges:
            raise ValueError("Terminal outcomes require completed critique judges.")
        pending = [
            _clean_text(row.get("judge_id"))
            for row in judges
            if isinstance(row, dict) and _clean_text(row.get("verdict")) in {"", "pending"}
        ]
        if pending:
            raise ValueError(f"Terminal outcomes require judge verdicts; pending: {pending}")


def main() -> int:
    logger = ReasoningLogger("kb-prove-cycle-finalizer")
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--kb-ref", required=True, help="KB reference for this proof cycle.")
    ap.add_argument("--attempt-json", required=True, help="Proof-attempt JSON path.")
    ap.add_argument("--attempt-md", default="", help="Optional proof-attempt Markdown path.")
    ap.add_argument("--artifacts-dir", default="", help="Optional artifacts/<kb-ref> path.")
    ap.add_argument("--queue-json", default="", help="Optional proof-queue JSON path.")
    ap.add_argument("--mathlib-json", default="", help="Optional InformalMathLib index JSON path.")
    ap.add_argument("--outcome", required=True, help="One of proved, disproved, blocked, deferred, prior_art_found.")
    ap.add_argument(
        "--produce-paper",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Generate a produced paper for high-value proved/disproved intermediate results.",
    )
    ap.add_argument("--latex-engine", default="auto", help="LaTeX engine preference for produced papers.")
    args = ap.parse_args()

    repo_root = Path(__file__).resolve().parents[4]
    kb_ref = _clean_text(args.kb_ref)
    artifacts_dir = Path(args.artifacts_dir) if args.artifacts_dir else canonical_artifacts_dir(repo_root, kb_ref)
    if not artifacts_dir.is_absolute():
        artifacts_dir = (repo_root / artifacts_dir).resolve()
    attempt_json = Path(args.attempt_json)
    if not attempt_json.is_absolute():
        attempt_json = (repo_root / attempt_json).resolve()
    attempt_md = Path(args.attempt_md) if args.attempt_md else attempt_json.with_suffix(".md")
    if not attempt_md.is_absolute():
        attempt_md = (repo_root / attempt_md).resolve()

    queue_json, queue_md = proof_queue_paths(repo_root, kb_ref)
    mathlib_json, mathlib_md = mathlib_paths(repo_root, kb_ref)
    if args.queue_json:
        queue_json = Path(args.queue_json)
    if args.mathlib_json:
        mathlib_json = Path(args.mathlib_json)
    if not queue_json.is_absolute():
        queue_json = (repo_root / queue_json).resolve()
    if not mathlib_json.is_absolute():
        mathlib_json = (repo_root / mathlib_json).resolve()

    attempt = _load_json(attempt_json)
    outcome = _clean_text(args.outcome).lower()
    _validate_attempt_for_terminal_outcome(attempt, outcome=outcome)

    attempt.setdefault("metadata", {})
    attempt.setdefault("final_assessment", {})
    attempt["metadata"]["status"] = outcome
    attempt["final_assessment"]["outcome"] = outcome
    refresh_attempt_inference_diagnosis(attempt)
    attempt_json.write_text(json.dumps(attempt, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    attempt_md.write_text(render_attempt_markdown(attempt), encoding="utf-8")

    queue = load_proof_queue(queue_json, kb_ref=kb_ref)
    mathlib = load_mathlib_index(mathlib_json, kb_ref=kb_ref)
    watch_json, watch_md = high_reward_watch_paths(artifacts_dir)
    high_reward_watch = load_high_reward_watch(watch_json, kb_ref=kb_ref)
    result_id = ""
    external_reference_ids: list[str] = []
    high_reward_signal: dict[str, Any] = {}
    proof_markdown = attempt_md.read_text(encoding="utf-8") if attempt_md.exists() else ""
    target = _ensure_dict(attempt.get("target"))
    proof_attempt = _ensure_dict(attempt.get("proof_attempt"))
    final_assessment = _ensure_dict(attempt.get("final_assessment"))
    major_subresult_assessment = _normalize_major_subresult_assessment(attempt)

    if outcome in {"proved", "disproved", "prior_art_found", "blocked"}:
        result_id = _next_result_id(mathlib, kb_ref=kb_ref)
        theorem_statement = (
            _clean_text(proof_attempt.get("result_statement"))
            or _clean_text(proof_attempt.get("theorem_statement"))
            or _clean_text(target.get("conjecture_statement"))
            or _clean_text(target.get("claim_text"))
        )
        result_summary = (
            _clean_text(proof_attempt.get("result_summary"))
            or _clean_text(final_assessment.get("summary"))
            or _clean_text(_ensure_dict(proof_attempt.get("negative_argument")).get("effect_on_claim"))
            or _clean_text(target.get("resolution_summary"))
        )
        result = {
            "result_id": result_id,
            "queue_id": _clean_text(attempt.get("metadata", {}).get("queue_id")),
            "attempt_id": _clean_text(attempt.get("metadata", {}).get("attempt_id")),
            "bridge_id": _clean_text(target.get("bridge_id")),
            "source_statement_id": _clean_text(target.get("source_statement_id")),
            "target_statement_id": _clean_text(target.get("target_statement_id")),
            "outcome": outcome,
            "title": _clean_text(target.get("title")) or _clean_text(proof_attempt.get("result_statement")),
            "entry_kind": "negative-local-theorem" if outcome == "blocked" else "result",
            "statement": theorem_statement,
            "summary": result_summary,
            "tags": [
                _clean_text(target.get("candidate_object")),
                _clean_text(target.get("preserved_invariant")),
                _clean_text(target.get("proof_strategy_family")),
            ],
            "web_search_used": bool(attempt.get("web_search_gate", {}).get("sources")),
            "major_subresult_score": major_subresult_assessment.get("score_total", 0),
            "major_subresult_candidate": bool(major_subresult_assessment.get("qualifies")),
        }
        if outcome in {"proved", "disproved", "prior_art_found"} and args.produce_paper:
            major_subresult_assessment = _maybe_generate_produced_paper(
                artifacts_dir=artifacts_dir,
                kb_ref=kb_ref,
                attempt=attempt,
                target=target,
                result=result,
                compile_result_pdf=True,
                latex_engine=args.latex_engine,
            )
        attempt["major_subresult_assessment"] = {
            **_ensure_dict(attempt.get("major_subresult_assessment")),
            **major_subresult_assessment,
        }
        if outcome in {"proved", "disproved", "prior_art_found"} and bool(major_subresult_assessment.get("qualifies")):
            provisional_signal = append_high_reward_signal(
                high_reward_watch,
                {
                    "result_id": result_id,
                    "queue_id": _clean_text(attempt.get("metadata", {}).get("queue_id")),
                    "attempt_id": _clean_text(attempt.get("metadata", {}).get("attempt_id")),
                    "bridge_id": _clean_text(target.get("bridge_id")),
                    "outcome": outcome,
                    "title": _clean_text(result.get("title")),
                    "statement": _clean_text(result.get("statement")),
                    "summary": _clean_text(result.get("summary")),
                    "major_subresult_score": int(major_subresult_assessment.get("score_total", 0) or 0),
                    "key_axis_max": int(major_subresult_assessment.get("key_axis_max", 0) or 0),
                    "gate_pass": bool(major_subresult_assessment.get("gate_pass")),
                    "qualifies": True,
                    "produced_paper_tex": _clean_text(major_subresult_assessment.get("produced_paper_tex")),
                    "produced_paper_pdf": _clean_text(major_subresult_assessment.get("produced_paper_pdf")),
                    "recommended_extension_cycles": DEFAULT_HIGH_REWARD_EXTENSION_CYCLES,
                    "continuation_rationale": _clean_text(
                        f"The intermediate result `{_clean_text(result.get('title'))}` cleared the major-subresult gate "
                        f"with score {int(major_subresult_assessment.get('score_total', 0) or 0)} and produced a paper-ready artifact."
                    ),
                    "follow_up_prove_queue_ids": [],
                    "follow_up_discovery_branch_ids": [],
                },
                kb_ref=kb_ref,
            )
            follow_up_prove_queue_ids, follow_up_discovery_branch_ids = _seed_high_reward_followups(
                repo_root=repo_root,
                artifacts_dir=artifacts_dir,
                kb_ref=kb_ref,
                queue=queue,
                result=result,
                target=target,
                attempt=attempt,
                outcome=outcome,
                signal_id=_clean_text(provisional_signal.get("signal_id")),
            )
            high_reward_signal = append_high_reward_signal(
                high_reward_watch,
                {
                    **provisional_signal,
                    "follow_up_prove_queue_ids": follow_up_prove_queue_ids,
                    "follow_up_discovery_branch_ids": follow_up_discovery_branch_ids,
                },
                kb_ref=kb_ref,
            )
            result["high_reward_signal_id"] = _clean_text(high_reward_signal.get("signal_id"))
            result["follow_up_prove_queue_ids"] = follow_up_prove_queue_ids
            result["follow_up_discovery_branch_ids"] = follow_up_discovery_branch_ids
            attempt["high_reward_signal"] = high_reward_signal
            save_high_reward_watch(high_reward_watch, json_path=watch_json, md_path=watch_md)
        refresh_attempt_inference_diagnosis(attempt)
        attempt_json.write_text(json.dumps(attempt, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        attempt_md.write_text(render_attempt_markdown(attempt), encoding="utf-8")
        artifact_path = write_mathlib_result_file(repo_root, kb_ref=kb_ref, result=result, proof_markdown=proof_markdown)
        result["artifact_path"] = str(artifact_path)
        append_mathlib_result(mathlib, result)

    external_reference_ids = _persist_external_references(
        repo_root=repo_root,
        kb_ref=kb_ref,
        mathlib=mathlib,
        attempt=attempt,
        target=target,
    )
    if result_id or external_reference_ids:
        mathlib_json.parent.mkdir(parents=True, exist_ok=True)
        mathlib_json.write_text(json.dumps(mathlib, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        mathlib_md.write_text(render_mathlib_catalog(mathlib), encoding="utf-8")

    finalize_queue_entry(
        queue,
        queue_id=_clean_text(attempt.get("metadata", {}).get("queue_id")),
        outcome=outcome,
        result_id=result_id,
        attempt_id=_clean_text(attempt.get("metadata", {}).get("attempt_id")),
        summary=_clean_text(proof_attempt.get("result_summary")) or _clean_text(final_assessment.get("summary")),
    )
    save_proof_queue(queue, json_path=queue_json, md_path=queue_md)

    summary = build_summary(kb_ref=kb_ref, queue=queue, mathlib=mathlib)
    write_summary(
        summary,
        output_json=artifacts_dir / "proof-cycle-summary.json",
        output_md=artifacts_dir / "proof-cycle-summary.md",
    )

    logger.add_kv("kb_ref", kb_ref)
    logger.add_kv("queue_id", _clean_text(attempt.get("metadata", {}).get("queue_id")))
    logger.step(
        "Finalized proof cycle",
        "\n".join(
            [
                f"kb_ref={kb_ref}",
                f"attempt_id={attempt.get('metadata', {}).get('attempt_id', '')}",
                f"queue_id={attempt.get('metadata', {}).get('queue_id', '')}",
                f"outcome={outcome}",
                f"result_id={result_id}",
                f"external_references_imported={len(external_reference_ids)}",
                f"major_subresult_score={major_subresult_assessment.get('score_total', 0)}",
                f"high_reward_signal_id={_clean_text(high_reward_signal.get('signal_id'))}",
                f"high_reward_follow_up_prove={len(_ensure_list(high_reward_signal.get('follow_up_prove_queue_ids')))}",
                f"high_reward_follow_up_discovery={len(_ensure_list(high_reward_signal.get('follow_up_discovery_branch_ids')))}",
                f"produced_paper={_clean_text(major_subresult_assessment.get('produced_paper_pdf') or major_subresult_assessment.get('produced_paper_tex'))}",
            ]
        ),
        surface_focus="proof-attempt-finalization",
        surface_stage="prove-cycle",
        surface_metrics={
            "result_recorded": 1 if result_id else 0,
            "external_references_imported": len(external_reference_ids),
            "major_subresult_score": int(major_subresult_assessment.get("score_total", 0) or 0),
            "high_reward_signal": 1 if _clean_text(high_reward_signal.get("signal_id")) else 0,
            "high_reward_follow_up_prove": len(_ensure_list(high_reward_signal.get("follow_up_prove_queue_ids"))),
            "high_reward_follow_up_discovery": len(_ensure_list(high_reward_signal.get("follow_up_discovery_branch_ids"))),
            "produced_paper": 1 if _clean_text(major_subresult_assessment.get("produced_paper_tex")) else 0,
        },
        surface_taxonomy={"reasoning_types": ["prove-cycle", "mathlib-update"]},
        surface_pdl={
            "program": _ensure_dict(attempt.get("pdl_program")),
            "operations": [
                {
                    "id": "persist",
                    "detail": "Persisted the terminal proof outcome into InformalMathLib and refreshed the queue summary.",
                },
                {
                    "id": "route",
                    "detail": "Routed the finished attempt into queue finalization, summary refresh, and optional continuation control.",
                },
            ]
            + (
                [
                    {
                        "id": "obstruct",
                        "detail": "The finalized outcome sharpens the route as a negative local theorem or barrier result.",
                    }
                ]
                if outcome in {"blocked", "disproved"}
                else []
            ),
            "judgments": [
                {
                    "form": "R |-m M",
                    "detail": "The terminal attempt result has been consolidated into durable problem memory.",
                },
                {
                    "form": "P ; G @ next",
                    "detail": "Queue state, summary state, and optional high-reward follow-ups are now synchronized.",
                },
            ],
            "control_objects": ["mathlib", "proof_queue", "high_reward_watch"],
            "epistemic_state": {
                "outcome": outcome,
                "external_references_imported": len(external_reference_ids),
                "high_reward_signal": 1 if _clean_text(high_reward_signal.get("signal_id")) else 0,
            },
        },
    )
    logger.add_output("proof_queue_json", queue_json)
    if result_id or external_reference_ids:
        logger.add_output("mathlib_json", mathlib_json)
    if _clean_text(major_subresult_assessment.get("produced_paper_tex")):
        logger.add_output("produced_paper_tex", Path(_clean_text(major_subresult_assessment.get("produced_paper_tex"))))
    if _clean_text(major_subresult_assessment.get("produced_paper_pdf")):
        logger.add_output("produced_paper_pdf", Path(_clean_text(major_subresult_assessment.get("produced_paper_pdf"))))
    if _clean_text(high_reward_signal.get("signal_id")):
        logger.add_output("high_reward_watch_json", watch_json)
        logger.add_output("high_reward_watch_md", watch_md)
    logger.add_output("proof_cycle_summary_md", artifacts_dir / "proof-cycle-summary.md")
    log_path = logger.finalize(
        "success",
        summary=f"Finalized proof attempt `{attempt.get('metadata', {}).get('attempt_id', '')}` with outcome `{outcome}`.",
    )
    print(f"[OK] Updated proof queue JSON: {queue_json}")
    if result_id or external_reference_ids:
        print(f"[OK] Updated InformalMathLib index JSON: {mathlib_json}")
    if _clean_text(major_subresult_assessment.get("produced_paper_tex")):
        print(f"[OK] Wrote produced paper TeX: {major_subresult_assessment.get('produced_paper_tex')}")
    if _clean_text(major_subresult_assessment.get("produced_paper_pdf")):
        print(f"[OK] Wrote produced paper PDF: {major_subresult_assessment.get('produced_paper_pdf')}")
    if _clean_text(high_reward_signal.get("signal_id")):
        print(f"[OK] Wrote high-reward watch JSON: {watch_json}")
        print(f"[OK] Wrote high-reward watch Markdown: {watch_md}")
    print(f"[OK] Wrote proof cycle summary Markdown: {artifacts_dir / 'proof-cycle-summary.md'}")
    print(f"[LOG] {log_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
