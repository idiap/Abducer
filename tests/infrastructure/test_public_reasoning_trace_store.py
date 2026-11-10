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

import json
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import pytest

from agentic.scripts.public_reasoning_trace_store import TraceStoreError, append_event, read_events


def event(run_id: str, key: str, *, parent: list[str] | None = None) -> dict:
    return {
        "run_id": run_id,
        "workflow_id": "theorem_proof_delivery",
        "workflow_version": "1.0.0",
        "target": "theorem:x",
        "phase": "proof",
        "event_family": "public_inference",
        "idempotency_key": key,
        "event_id": f"evt-{run_id}-{key}",
        "causal_parent_event_ids": parent or [],
        "claim_epistemic_status": "conjectural",
    }


def test_store_is_run_isolated_causal_and_idempotent(tmp_path: Path) -> None:
    root = tmp_path / "trace"
    a1 = append_event(event("run-a", "one"), store_root=root)
    a2 = append_event(event("run-a", "two", parent=[a1["event_id"]]), store_root=root)
    b1 = append_event(event("run-b", "one"), store_root=root)
    retry = append_event(event("run-a", "two", parent=[a1["event_id"]]), store_root=root)
    assert retry == a2
    assert [row["sequence"] for row in read_events("run-a", store_root=root)] == [1, 2]
    assert [row["event_id"] for row in read_events("run-b", store_root=root)] == [b1["event_id"]]
    with pytest.raises(TraceStoreError, match="unknown causal parent"):
        append_event(event("run-a", "bad", parent=[b1["event_id"]]), store_root=root)


def test_store_serializes_concurrent_appends_and_latest_view(tmp_path: Path) -> None:
    root = tmp_path / "trace"
    with ThreadPoolExecutor(max_workers=4) as pool:
        rows = list(pool.map(lambda i: append_event(event("parallel", str(i)), store_root=root, latest_name="test"), range(12)))
    stored = read_events("parallel", store_root=root)
    assert len(stored) == len(rows) == 12
    assert sorted(row["sequence"] for row in stored) == list(range(1, 13))
    latest = json.loads((root / "latest/test.json").read_text())
    assert latest["event_id"] in {row["event_id"] for row in stored}
    assert json.loads((root / "runs/parallel/manifest.json").read_text())["event_count"] == 12


def test_link_to_latest_builds_a_correlated_lifecycle(tmp_path: Path) -> None:
    root = tmp_path / "trace"
    first = append_event(event("linked", "activation"), store_root=root, link_to_latest=True)
    second = append_event(event("linked", "authorization"), store_root=root, link_to_latest=True)
    third = append_event(event("linked", "exit"), store_root=root, link_to_latest=True)
    assert second["causal_parent_event_ids"] == [first["event_id"]]
    assert third["causal_parent_event_ids"] == [second["event_id"]]

