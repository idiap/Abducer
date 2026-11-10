# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

from rich.console import Console


def _load_module():
    root = Path(__file__).resolve().parents[2]
    module_path = root / "skills" / "orchestration" / "show-reasoning" / "scripts" / "show_reasoning.py"
    spec = importlib.util.spec_from_file_location("show_reasoning", module_path)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_latex_renderer_prefers_terminal_math_symbols() -> None:
    mod = _load_module()
    rendered = mod._latex_to_terminal(r"\mathsf{route}(P \Rightarrow \text{next})")
    assert rendered == "route(P ⇒ next)"


def test_surface_snapshot_uses_kb_ref_context_and_latex_operations(tmp_path: Path) -> None:
    mod = _load_module()
    surfaces = tmp_path / "artifacts" / "reasoning-surfaces" / "work"
    surfaces.mkdir(parents=True)
    payload = {
        "agent": "work",
        "run_id": "run-123",
        "started_utc": "2026-03-17T18:00:00+00:00",
        "context": {"kb_ref": "p-vs-np"},
        "outputs": [],
        "status": "running",
        "moments": [
            {
                "timestamp": "2026-03-17T18:00:01+00:00",
                "kind": "conceptual_move",
                "title": "Completed work prove phase",
                "focus": "work::prove",
                "significance": "Records the epistemic result of the selected work phase.",
                "details": [],
                "tags": ["work-loop", "prove"],
                "stage": "work",
                "taxonomy": {},
                "metrics": {},
                "pdl": {
                    "program": {
                        "metadata": {
                            "program_id": "attempt.p-vs-np.001",
                            "kind": "proof-attempt",
                            "stage": "prove",
                        },
                        "target": {"statement": "Prove the current theorem."},
                    },
                    "operations": [
                        {
                            "id": "route",
                            "form": "route(P => next)",
                            "latex_form": r"\mathsf{route}(P \Rightarrow \text{next})",
                            "title": "Route",
                            "detail": "Dispatch the next proof step.",
                        }
                    ],
                    "judgments": [{"form": "P ; G @ next", "detail": "Continue to prove."}],
                    "control_objects": [{"id": "proof_queue", "title": "Proof Queue", "role": "Frontier"}],
                    "epistemic_state": {"pending_count": 3},
                },
            }
        ],
    }
    (surfaces / "run.json").write_text(json.dumps(payload), encoding="utf-8")

    records = mod.load_surface_records(tmp_path / "artifacts" / "reasoning-surfaces")
    filtered = mod.filter_surface_records(records, kb_ref="p-vs-np")
    snapshot = mod.build_snapshot(filtered, max_moments=10)

    assert snapshot["kb_ref"] == "p-vs-np"
    assert snapshot["latest_pdl"]["program"]["metadata"]["program_id"] == "attempt.p-vs-np.001"
    display = mod._operation_display_text(snapshot["latest_pdl"]["operations"][0])
    assert "route(P ⇒ next)" in display


def test_snapshot_surfaces_content_specific_topic_and_bridge_context(tmp_path: Path) -> None:
    mod = _load_module()
    surfaces = tmp_path / "artifacts" / "reasoning-surfaces" / "work"
    surfaces.mkdir(parents=True)
    payload = {
        "agent": "work",
        "run_id": "run-456",
        "started_utc": "2026-03-17T18:40:00+00:00",
        "context": {"kb_ref": "p-vs-np"},
        "outputs": [],
        "status": "running",
        "moments": [
            {
                "timestamp": "2026-03-17T18:40:01+00:00",
                "kind": "result_synthesis",
                "title": "Completed work discovery phase",
                "focus": "work::discovery",
                "significance": "Records the epistemic result of the selected work phase.",
                "details": [
                    "status=completed",
                    "detail=Queued or refreshed 24 proof targets and promoted the strongest MCSP route back into prove.",
                ],
                "tags": ["work-loop", "discovery"],
                "stage": "work",
                "taxonomy": {},
                "metrics": {"queue_updated": 24},
                "pdl": {
                    "program": {
                        "metadata": {
                            "program_id": "proofq.p-vs-np.033",
                            "kind": "queue-entry",
                            "stage": "discovery-to-prove",
                            "title": "Commutative factorization theorem for MCSP obstruction family",
                        },
                        "target": {
                            "label": "Commutative factorization theorem for MCSP obstruction family",
                            "statement": "Build the mediating object needed for the MCSP magnification route.",
                        },
                        "bridge_object": {
                            "label": "MCSP obstruction family",
                            "kind": "family of hard instances",
                            "invariant": "MCSP complexity profile in nonuniform-circuits",
                        },
                        "tensions": ["Missing route lemma: Commutative factorization theorem for MCSP obstruction family"],
                        "anchors": [
                            {
                                "anchor_id": "source-statement",
                                "content": "A hardness magnification theorem starts from a barely nontrivial lower bound.",
                            },
                            {
                                "anchor_id": "target-statement",
                                "content": "The target payoff is NP not in P/poly under the refined Gap-MCSP regime.",
                            },
                        ],
                    },
                    "operations": [],
                    "judgments": [],
                    "control_objects": [],
                    "epistemic_state": {"queue_updated": 24, "top_k": 8},
                },
            }
        ],
    }
    (surfaces / "run.json").write_text(json.dumps(payload), encoding="utf-8")

    records = mod.load_surface_records(tmp_path / "artifacts" / "reasoning-surfaces")
    snapshot = mod.build_snapshot(records, max_moments=10)

    assert snapshot["latest_topic"] == "Commutative factorization theorem for MCSP obstruction family"
    assert snapshot["latest_semantic"]["bridge_label"] == "MCSP obstruction family"
    assert "Queued or refreshed 24 proof targets" in snapshot["agent_rows"][0]["summary"]


def test_render_pdl_panel_shows_specific_semantic_context(tmp_path: Path) -> None:
    mod = _load_module()
    surfaces = tmp_path / "artifacts" / "reasoning-surfaces" / "work"
    surfaces.mkdir(parents=True)
    payload = {
        "agent": "work",
        "run_id": "run-789",
        "started_utc": "2026-03-17T19:00:00+00:00",
        "context": {"kb_ref": "p-vs-np"},
        "outputs": [],
        "status": "running",
        "moments": [
            {
                "timestamp": "2026-03-17T19:00:01+00:00",
                "kind": "reasoning_move",
                "title": "Ran work cycle",
                "focus": "work-loop",
                "significance": "Records a meaningful step in the ongoing discovery trajectory.",
                "details": ["detail=Compiled branch-level discoveries into an MCSP magnification route."],
                "tags": [],
                "stage": "work",
                "taxonomy": {},
                "metrics": {},
                "pdl": {
                    "program": {
                        "metadata": {
                            "program_id": "proofq.p-vs-np.033",
                            "kind": "queue-entry",
                            "stage": "discovery-to-prove",
                            "title": "Commutative factorization theorem for MCSP obstruction family",
                        },
                        "target": {"label": "Commutative factorization theorem for MCSP obstruction family"},
                        "bridge_object": {
                            "label": "MCSP obstruction family",
                            "kind": "family of hard instances",
                            "invariant": "MCSP complexity profile in nonuniform-circuits",
                        },
                        "positive_route": {"route_lemma": "Commutative factorization theorem for MCSP obstruction family"},
                        "tensions": ["Missing route lemma: Commutative factorization theorem for MCSP obstruction family"],
                        "conceptual_nexus": {
                            "summary": "Move from magnification premises toward NP not in P/poly through the MCSP obstruction family."
                        },
                        "anchors": [
                            {"anchor_id": "source-statement", "content": "A hardness magnification theorem starts from a barely nontrivial lower bound."},
                            {"anchor_id": "target-statement", "content": "The target payoff is NP not in P/poly under the refined Gap-MCSP regime."},
                        ],
                        "control_objects": ["kb", "mathlib", "proof_queue"],
                    },
                    "operations": [{"id": "route", "detail": "Route the MCSP programme into prove."}],
                    "judgments": [],
                    "control_objects": [{"id": "proof_queue", "title": "Proof Queue"}],
                    "epistemic_state": {"queue_updated": 24, "top_k": 8},
                },
            }
        ],
    }
    (surfaces / "run.json").write_text(json.dumps(payload), encoding="utf-8")

    records = mod.load_surface_records(tmp_path / "artifacts" / "reasoning-surfaces")
    snapshot = mod.build_snapshot(records, max_moments=10)
    panel = mod._render_pdl(snapshot)
    console = Console(width=140, record=True)
    console.print(panel)
    rendered = console.export_text()

    assert "Commutative factorization theorem for MCSP obstruction family" in rendered
    assert "MCSP obstruction family" in rendered
    assert "MCSP complexity profile in nonuniform-circuits" in rendered
    assert "Move from magnification premises toward NP not in P/poly" in rendered
