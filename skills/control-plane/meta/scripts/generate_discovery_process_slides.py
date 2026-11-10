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

"""Generate a slide-style Markdown narrative of the current discovery process."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

_COMMON_DIR = Path(__file__).resolve().parents[3] / "common"
if str(_COMMON_DIR) not in sys.path:
    sys.path.insert(0, str(_COMMON_DIR))

from kb_context import kb_ref_from_artifacts_dir
from reasoning_log import ReasoningLogger


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


def _safe_int(value: Any, default: int = 0) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _safe_float(value: Any, default: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _first_nonempty(*values: Any) -> str:
    for value in values:
        text = _clean_text(value)
        if text:
            return text
    return ""


def _truncate(value: Any, limit: int = 200) -> str:
    text = _clean_text(value)
    if len(text) <= limit:
        return text
    cut = text[: max(0, limit - 3)].rstrip()
    if " " in cut:
        cut = cut.rsplit(" ", 1)[0]
    return cut + "..."


def _timeline_stage(conceptual: dict[str, Any], stage_name: str) -> dict[str, Any]:
    for row in _ensure_list(conceptual.get("timeline")):
        if isinstance(row, dict) and _clean_text(row.get("stage")) == stage_name:
            return row
    return {}


def _labels(rows: list[Any], *, limit: int = 4) -> list[str]:
    out: list[str] = []
    seen: set[str] = set()
    for row in rows:
        if len(out) >= limit:
            break
        if isinstance(row, dict):
            label = _first_nonempty(row.get("label"), row.get("title"), row.get("id"))
            if label and label not in seen:
                seen.add(label)
                out.append(label)
        else:
            text = _clean_text(row)
            if text and text not in seen:
                seen.add(text)
                out.append(text)
    return out


def _top_queue_entries(proof_queue: dict[str, Any], *, limit: int = 3) -> list[dict[str, Any]]:
    entries = [row for row in _ensure_list(proof_queue.get("entries")) if isinstance(row, dict)]
    entries.sort(key=lambda row: _safe_float(row.get("priority")), reverse=True)
    return entries[:limit]


def build_discovery_process_slides(*, artifacts_dir: Path) -> dict[str, Any]:
    kb_ref = kb_ref_from_artifacts_dir(artifacts_dir)
    if not kb_ref:
        raise ValueError("Could not resolve kb_ref from artifacts directory.")

    work_state = _load_json(artifacts_dir / "work-state.json")
    meta = _load_json(artifacts_dir / "meta-reflection-report.json")
    macro_state = _load_json(artifacts_dir / "macro-proof-state.json")
    proof_queue = _load_json(artifacts_dir / "proof-queue.json")
    promising = _load_json(artifacts_dir / "promising-directions-report.json")
    conceptual = _load_json(artifacts_dir / "conceptual-dynamics.json")

    work_meta = _ensure_dict(work_state.get("metadata"))
    latest = _ensure_dict(work_state.get("latest"))
    meta_judgment = _ensure_dict(meta.get("meta_judgment"))
    original_hardness = _ensure_dict(meta.get("original_hardness"))
    current_interpretation = _ensure_dict(meta.get("current_proof_state_interpretation"))
    main_conjecture = _ensure_dict(macro_state.get("main_conjecture"))
    leading_route = _ensure_dict(macro_state.get("leading_route"))
    status_assessment = _ensure_dict(macro_state.get("status_assessment"))

    connect_stage = _timeline_stage(conceptual, "connect.analyze")
    bridge_stage = _timeline_stage(conceptual, "bridge-plan")
    conjecture_stage = _timeline_stage(conceptual, "conjecture")
    sketch_stage = _timeline_stage(conceptual, "proof-sketch")
    expert_stage = _timeline_stage(conceptual, "expert-paper")

    connect_highlights = _ensure_dict(_ensure_dict(connect_stage.get("state")).get("highlights"))
    conjecture_highlights = _ensure_dict(_ensure_dict(conjecture_stage.get("state")).get("highlights"))
    sketch_highlights = _ensure_dict(_ensure_dict(sketch_stage.get("state")).get("highlights"))
    expert_highlights = _ensure_dict(_ensure_dict(expert_stage.get("state")).get("highlights"))

    top_direction = _ensure_dict((_ensure_list(promising.get("most_promising_directions")) or [{}])[0])
    queue_frontier = _top_queue_entries(proof_queue)

    top_targets = _labels(_ensure_list(connect_highlights.get("introduced_targets")), limit=4)
    introduced_objects = _labels(_ensure_list(conjecture_highlights.get("introduced_bridge_objects")), limit=4)
    proof_sketches = _labels(_ensure_list(sketch_highlights.get("stage_proof_sketches")), limit=3)
    supported_hypotheses = _labels(_ensure_list(expert_highlights.get("supported_hypotheses")), limit=3)

    slides = [
        {
            "title": "Current Discovery State",
            "takeaway": "After the current `work` + `meta` round, the programme is organized, auditable, and still open.",
            "narrative": [
                f"We have completed {_safe_int(work_meta.get('cycle_count'))} outer work cycle(s); the latest phase was `{_clean_text(latest.get('phase'))}` and the next phase is `{_clean_text(work_meta.get('next_phase'))}`.",
                f"The current plausibility score is {_safe_float(_ensure_dict(work_state.get('plausibility')).get('plausibility_score')):.3f}; the system does not detect a plausible full proof yet.",
                current_interpretation.get("headline", ""),
            ],
            "examples": [
                f"Latest work result: {_clean_text(latest.get('detail'))}",
                f"Meta judgment: {_clean_text(meta_judgment.get('headline'))}",
            ],
        },
        {
            "title": "Why The Problem Is Still Hard",
            "takeaway": "The framework now localizes the difficulty more sharply, but the essential hardness remains cross-regime transport under low evidence.",
            "narrative": [
                _clean_text(original_hardness.get("summary")),
                _clean_text(_ensure_list(original_hardness.get("hardness_elements"))[0].get("detail")) if _ensure_list(original_hardness.get("hardness_elements")) else "",
                _clean_text(_ensure_list(meta.get("persistent_difficulties"))[0].get("detail")) if _ensure_list(meta.get("persistent_difficulties")) else "",
            ],
            "examples": [
                "Direct proof aspiration has been replaced by a sharper nonuniform target.",
                "The current route still depends on a bridge object rather than a direct deduction from the KB.",
            ],
        },
        {
            "title": "What Changed In Framing",
            "takeaway": "The search no longer treats `P != NP` as a single undifferentiated target.",
            "narrative": [
                f"The main conjecture is `{_clean_text(main_conjecture.get('core_claim'))}`, but the active route target is `{_clean_text(main_conjecture.get('route_target_claim'))}`.",
                "This is a real perspective shift: the search first tries to prove a stronger nonuniform consequence and only then closes back to the central conjecture.",
                _clean_text(current_interpretation.get("detail")),
            ],
            "examples": [
                f"Grounding implication: {_clean_text(main_conjecture.get('grounding_implication'))}",
                f"Leading route target: {_clean_text(leading_route.get('target_claim_focus'))}",
            ],
        },
        {
            "title": "New Concepts Introduced By The Search",
            "takeaway": "The discovery process is not only ranking statements; it is adding a more explicit conceptual vocabulary for the route.",
            "narrative": [
                "Connector and conjecture stages surfaced concrete target concepts, bridge objects, and invariants that did not appear as the primary unit of reasoning at the start.",
                "The key gain is that the route is now discussed through carriers and invariants rather than only by thematic similarity.",
            ],
            "examples": [
                "Target concepts: " + ", ".join(top_targets) if top_targets else "",
                "Bridge objects: " + ", ".join(introduced_objects) if introduced_objects else "",
                f"Leading bridge object: {_clean_text(leading_route.get('candidate_object'))}",
                f"Preserved invariant: {_clean_text(leading_route.get('invariant'))}",
            ],
        },
        {
            "title": "New Connections Made Explicit",
            "takeaway": "The main novelty is in theorem-pair-specific connections, not generic topic clustering.",
            "narrative": [
                "The current bridge portfolio spells out concrete source-to-target routes together with what is supposed to be transported.",
                "These are inspectable research programmes because each route comes with a carrier, an invariant, and a missing route lemma.",
            ],
            "examples": [
                _clean_text(top_direction.get("route_synopsis")),
                "Adjacent route: "
                + _clean_text(_ensure_dict((_ensure_list(promising.get("most_promising_directions")) + [{}])[1]).get("route_synopsis")),
                "Generalization route: "
                + _clean_text(_ensure_dict((_ensure_list(promising.get("most_promising_directions")) + [{}, {}, {}])[2]).get("route_synopsis")),
            ],
        },
        {
            "title": "How The Discovery Process Evolved",
            "takeaway": "The process moved from broad structural targeting to bridge design, then to typed conjectures, then to theorem-sized proof obligations.",
            "narrative": [
                "Stage 1 identified high-pressure targets and intervention points in the concept graph.",
                "Stage 2 converted those targets into bridge programmes with explicit missing interfaces.",
                "Stage 3 conjectured candidate objects and Stage 4 formalized them into proof sketches and queue items.",
            ],
            "examples": [
                "Connect stage headline: " + _clean_text(connect_highlights.get("headline")),
                "Bridge-plan headline: " + _clean_text(_ensure_dict(_ensure_dict(bridge_stage.get('state')).get('highlights')).get("headline")),
                "Conjecture headline: " + _clean_text(conjecture_highlights.get("headline")),
                "Proof-sketch examples: " + ", ".join(proof_sketches) if proof_sketches else "",
            ],
        },
        {
            "title": "What The Queue Now Means",
            "takeaway": "The frontier is no longer a vague backlog; it is a queue of theorem-shaped claims that can be proved, disproved, or blocked.",
            "narrative": [
                f"The proof queue currently contains {_safe_int(_ensure_dict(proof_queue.get('metadata')).get('pending_count'))} pending items.",
                "Each item states a self-contained route conjecture, attaches a missing route lemma, and exposes proof obligations and failure logic.",
                "This is the main operational outcome of the `work` cycle so far.",
            ],
            "examples": [
                _clean_text(_ensure_dict(queue_frontier[0] if queue_frontier else {}).get("title")),
                _clean_text(_ensure_dict(queue_frontier[0] if queue_frontier else {}).get("claim_text")),
                _clean_text(_ensure_dict(queue_frontier[0] if queue_frontier else {}).get("missing_route_lemma")),
            ],
        },
        {
            "title": "What Still Blocks Completion",
            "takeaway": "The open problem is now narrower, but the missing mathematics is still substantial.",
            "narrative": [
                _clean_text(_ensure_list(meta.get("persistent_difficulties"))[0].get("detail")) if _ensure_list(meta.get("persistent_difficulties")) else "",
                _clean_text(_ensure_list(meta.get("persistent_difficulties"))[1].get("detail")) if len(_ensure_list(meta.get("persistent_difficulties"))) > 1 else "",
                _clean_text(status_assessment.get("assessment")),
            ],
            "examples": [
                "No terminal proved attempts yet.",
                f"Evidence count remains {_safe_int(status_assessment.get('evidence_count'))}.",
                f"Current bottleneck: {_clean_text(leading_route.get('missing_route_lemma'))}",
            ],
        },
        {
            "title": "How An External Expert Should Read The State",
            "takeaway": "This is already expert-inspectable, but it is not yet expert-endorsable as a proof claim.",
            "narrative": [
                "An external expert should read the current state as a conditional macro-proof programme with concrete bridge objects and explicit failure points.",
                "The right expert question is no longer 'what topic should we try?' but 'is this bridge object mathematically real, and can the route lemma be discharged or ruled out?'",
                _clean_text(meta_judgment.get("detail")),
            ],
            "examples": [
                "Inspect first: MCSP witness family versus Gap-MCSP promise problem.",
                "Inspect first: the source-to-object lemma and the transport claim.",
                "Supported but not decisive: " + ", ".join(supported_hypotheses) if supported_hypotheses else "",
            ],
        },
        {
            "title": "Next Governing Question",
            "takeaway": "The next cycle should be governed by one sharp mathematical question, not by generic additional search.",
            "narrative": [
                _clean_text(meta_judgment.get("next_question")),
                f"The next outer-loop phase is `{_clean_text(work_meta.get('next_phase'))}`, so the system is ready to consume the highest-priority queued route.",
                "The best immediate use of expert time is to either close the representation defect or to derive a barrier result that compresses the search space.",
            ],
            "examples": [
                "Primary route: bridge.001 toward NP not in P/poly.",
                "Next best stress test: bridge.002 through the nonuniform-circuits -> formula-size transfer.",
            ],
        },
    ]

    for slide in slides:
        slide["narrative"] = [item for item in slide.get("narrative", []) if _clean_text(item)]
        slide["examples"] = [item for item in slide.get("examples", []) if _clean_text(item)]

    return {
        "metadata": {
            "kb_ref": kb_ref,
            "cycle_count": _safe_int(work_meta.get("cycle_count")),
            "perspective": _clean_text(_ensure_dict(meta.get("metadata")).get("perspective")),
            "slide_count": len(slides),
        },
        "slides": slides,
    }


def render_markdown(deck: dict[str, Any]) -> str:
    meta = _ensure_dict(deck.get("metadata"))
    slides = [row for row in _ensure_list(deck.get("slides")) if isinstance(row, dict)]
    blocks = [
        f"# Discovery Process Slides for {meta.get('kb_ref', '')}",
        "",
        "_Audience: external mathematical experts. These slides summarize the current discovery process after the present `work` + `meta` round._",
    ]
    for index, slide in enumerate(slides, start=1):
        blocks.extend(
            [
                "",
                "---",
                "",
                f"# Slide {index} - {_clean_text(slide.get('title'))}",
                "",
                f"**Takeaway**  \n{_clean_text(slide.get('takeaway'))}",
            ]
        )
        narrative = [item for item in _ensure_list(slide.get("narrative")) if _clean_text(item)]
        if narrative:
            blocks.extend(["", "## Narrative", ""])
            blocks.extend([f"- {_clean_text(item)}" for item in narrative])
        examples = [item for item in _ensure_list(slide.get("examples")) if _clean_text(item)]
        if examples:
            blocks.extend(["", "## Concrete Examples", ""])
            blocks.extend([f"- {_clean_text(item)}" for item in examples])
    return "\n".join(blocks).strip() + "\n"


def main() -> int:
    logger = ReasoningLogger("meta-discovery-slides")
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--artifacts-dir", required=True, help="Path to artifacts/<kb-ref>.")
    ap.add_argument("--output-md", default="", help="Optional output Markdown path.")
    args = ap.parse_args()

    repo_root = Path(__file__).resolve().parents[4]
    artifacts_dir = Path(args.artifacts_dir)
    if not artifacts_dir.is_absolute():
        artifacts_dir = (repo_root / artifacts_dir).resolve()
    kb_ref = kb_ref_from_artifacts_dir(artifacts_dir)
    if not kb_ref:
        raise SystemExit("[ERROR] Could not resolve kb_ref for discovery slides.")

    output_md = Path(args.output_md) if args.output_md else artifacts_dir / "discovery-process-slides.md"
    if not output_md.is_absolute():
        output_md = (repo_root / output_md).resolve()

    deck = build_discovery_process_slides(artifacts_dir=artifacts_dir)
    output_md.parent.mkdir(parents=True, exist_ok=True)
    output_md.write_text(render_markdown(deck), encoding="utf-8")

    logger.step(
        "Generated discovery-process slides",
        "\n".join(
            [
                f"kb_ref={kb_ref}",
                f"slide_count={_safe_int(_ensure_dict(deck.get('metadata')).get('slide_count'))}",
                f"cycle_count={_safe_int(_ensure_dict(deck.get('metadata')).get('cycle_count'))}",
            ]
        ),
        surface_focus="discovery-process-slides",
        surface_stage="meta",
        surface_metrics={
            "slide_count": _safe_int(_ensure_dict(deck.get("metadata")).get("slide_count")),
            "cycle_count": _safe_int(_ensure_dict(deck.get("metadata")).get("cycle_count")),
        },
        surface_taxonomy={"reasoning_types": ["meta-analysis", "discovery-narration"]},
    )
    logger.add_output("discovery_process_slides_md", output_md)
    log_path = logger.finalize(
        "success",
        summary=f"Generated discovery-process slide deck for `{kb_ref}`.",
    )
    print(f"[OK] Wrote discovery-process slides: {output_md}")
    print(f"[LOG] {log_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
