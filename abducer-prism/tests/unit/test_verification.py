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

from to_prism.verification import (
    aggregate_preservation,
    canonicalize_cli_payload,
    compare_contract_surfaces,
    compare_fixture_outputs,
    compare_graphs,
    compare_traces,
    inventory_output_coverage,
    provider_hook_preservation,
)


def test_cli_normalizer_preserves_semantic_result() -> None:
    normalized = canonicalize_cli_payload(
        {
            "path": "/private/machine/main.prism",
            "timestamp": "now",
            "status": "rejected",
            "result": {"accepted": False, "path": "semantic/target", "value": 3},
        }
    )
    assert normalized == {
        "status": "rejected",
        "result": {"accepted": False, "path": "semantic/target", "value": 3},
    }


def test_graph_comparison_detects_edge_mutation() -> None:
    expected = {
        "entrypoint": "a",
        "nodes": [{"id": "a"}, {"id": "b"}],
        "edges": [{"source": "a", "target": "b", "kind": "control"}],
    }
    mutated = {
        **expected,
        "edges": [{"source": "b", "target": "a", "kind": "control"}],
    }
    assert compare_graphs(expected, expected) == []
    assert compare_graphs(expected, mutated) == ["workflow graph edges differs"]


def test_independent_oracles_detect_semantic_mutations() -> None:
    contract = {
        "input": {"type": "Task"},
        "output": {"type": "Answer"},
        "errors": ["Rejected"],
        "effects": ["AI.Generate"],
        "permissions": [],
    }
    changed_contract = {**contract, "errors": []}
    assert compare_contract_surfaces(contract, changed_contract) == [
        "contract errors differs"
    ]
    assert compare_fixture_outputs(
        {"status": "ok", "run_id": "one"},
        {"status": "failed", "run_id": "two"},
    ) == ["fixture output differs"]
    assert compare_traces(
        [{"event": "before"}, {"event": "stop", "status": "ok"}],
        [{"event": "stop", "status": "ok"}, {"event": "before"}],
    ) == ["trace correspondence differs"]


def test_coverage_and_preservation_caps_fail_closed() -> None:
    inventory = {"items": [{"id": "skill"}, {"id": "hook"}]}
    assert inventory_output_coverage(
        inventory,
        {"skill": {"disposition": "convert", "outputs": ["main.prism"]}},
    ) == ["source item has no output disposition: hook"]
    opencode = provider_hook_preservation(
        provider="opencode",
        artifact_roundtrip=True,
        materialized=True,
        native_activated=False,
        outcome_observed=False,
        instrumented_trace=False,
    )
    assert opencode == {
        "structural": "established",
        "behavioral": "unsupported",
        "trace": "unsupported",
    }
    aggregate = aggregate_preservation(
        {
            "critical-a": {
                "structural": "established",
                "behavioral": "established",
            },
            "critical-b": {
                "structural": "established",
                "behavioral": "not_tested",
            },
        },
        critical_workflows={"critical-a", "critical-b"},
    )
    assert aggregate["behavioral"] == "not_tested"
