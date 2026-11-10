# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Regression tests for drift-checked dynamic-experiment authority reuse.

The performance contract is deliberately stricter than ordinary memoization:
warm calls may skip AST/schema reconstruction only while exact dependency
bytes, runtime versions, and positive/negative import-resolution facts remain
unchanged.  An explicit operation context additionally performs one full
terminal replay, including observed environment and executable authority.
"""

from __future__ import annotations

import copy
from pathlib import Path
from typing import Iterator

import pytest

import agentic.experiments.authority as experiment_authority
from agentic.experiments.authority import (
    ExperimentAuthorityRunContext,
    build_experiment_authority,
    build_experiment_dependency_authority,
    experiment_authority_run_context,
    validate_experiment_authority,
)
from agentic.experiments.errors import ExperimentAuthorityError


@pytest.fixture
def minimal_authority_profile(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> Iterator[tuple[Path, dict[str, int]]]:
    """Install a complete tiny profile so drift cases never mutate repo files."""

    root = tmp_path / "repository"
    root.mkdir()
    (root / "entry.py").write_text("import json\nVALUE = 1\n", encoding="utf-8")
    (root / "contract.schema.json").write_text(
        '{"type":"object"}\n', encoding="utf-8"
    )
    monkeypatch.setattr(experiment_authority, "ROOT", root)
    monkeypatch.setattr(
        experiment_authority,
        "_ENTRY_PATHS",
        {"entry.py": ("test_entry",)},
    )
    monkeypatch.setattr(
        experiment_authority,
        "_SEMANTIC_PATHS",
        {"contract.schema.json": ("test_contract",)},
    )
    monkeypatch.setattr(experiment_authority, "_RUNTIME_DISTRIBUTIONS", {})
    original_builder = experiment_authority.build_dependency_authority
    calls = {"full_builds": 0}

    def counted_builder(**kwargs: object) -> dict:
        calls["full_builds"] += 1
        return original_builder(**kwargs)

    monkeypatch.setattr(
        experiment_authority, "build_dependency_authority", counted_builder
    )
    experiment_authority._reset_experiment_authority_memo_for_tests()
    try:
        yield root, calls
    finally:
        experiment_authority._reset_experiment_authority_memo_for_tests()


def test_standalone_memo_reuses_only_unchanged_exact_closure(
    minimal_authority_profile: tuple[Path, dict[str, int]],
) -> None:
    root, calls = minimal_authority_profile

    first = build_experiment_dependency_authority()
    second = build_experiment_dependency_authority()

    assert second == first
    assert second is not first
    assert calls == {"full_builds": 1}

    (root / "entry.py").write_text("import json\nVALUE = 2\n", encoding="utf-8")
    changed = build_experiment_dependency_authority()
    assert changed["content_digest"] != first["content_digest"]
    assert calls == {"full_builds": 2}

    # A new file can change an existing import from stdlib to repository-local
    # without changing entry.py.  Negative resolution sentinels must notice it.
    (root / "json.py").write_text("LOCAL = True\n", encoding="utf-8")
    shadowed = build_experiment_dependency_authority()
    assert calls == {"full_builds": 3}
    assert "json.py" in shadowed["import_boundary"][
        "repository_local_python_paths"
    ]


def test_operation_context_reuses_immutable_authority_and_fully_closes(
    minimal_authority_profile: tuple[Path, dict[str, int]],
) -> None:
    _, calls = minimal_authority_profile
    model = {"operation": "equality", "left": "1", "right": "1"}

    with experiment_authority_run_context() as context:
        first = build_experiment_authority(adapter="exact", model=model)
        validated = validate_experiment_authority(
            first, adapter="exact", model=model
        )
        detached = build_experiment_authority(adapter="exact", model=model)
        detached["dependency_authority"]["scope"] = "caller-mutation"
        assert validated == first
        assert build_experiment_authority(adapter="exact", model=model) == first
        assert context.replay_counts == {
            "dependency_full_replays": 1,
            "environment_observations": 1,
            "authority_cache_hits": 3,
            "final_dependency_replays": 0,
            "final_environment_replays": 0,
        }

    assert calls == {"full_builds": 2}
    assert context.replay_counts["final_dependency_replays"] == 1
    assert context.replay_counts["final_environment_replays"] == 1


def test_operation_context_terminal_replay_rejects_source_drift(
    minimal_authority_profile: tuple[Path, dict[str, int]],
) -> None:
    root, calls = minimal_authority_profile

    with pytest.raises(ExperimentAuthorityError) as caught:
        with experiment_authority_run_context() as context:
            build_experiment_authority(
                adapter="exact",
                model={"operation": "equality", "left": "1", "right": "1"},
            )
            (root / "entry.py").write_text(
                "import json\nVALUE = 'drifted'\n", encoding="utf-8"
            )

    assert caught.value.reason_code == "execution_authority_stale"
    assert calls == {"full_builds": 2}
    with pytest.raises(ExperimentAuthorityError) as poisoned:
        context.dependency_snapshot()
    assert poisoned.value.reason_code == "authority_context_finalized"


def test_operation_context_terminal_replay_rejects_environment_drift(
    minimal_authority_profile: tuple[Path, dict[str, int]],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _, calls = minimal_authority_profile

    with pytest.raises(ExperimentAuthorityError) as caught:
        with experiment_authority_run_context():
            build_experiment_authority(
                adapter="exact",
                model={"operation": "equality", "left": "1", "right": "1"},
            )
            monkeypatch.setattr(
                experiment_authority.platform,
                "machine",
                lambda: "drifted-machine",
            )

    assert caught.value.reason_code == "execution_authority_stale"
    assert calls == {"full_builds": 2}


def test_run_context_cannot_be_constructed_from_caller_mapping() -> None:
    with pytest.raises(ExperimentAuthorityError) as caught:
        ExperimentAuthorityRunContext(
            copy.deepcopy({"content_digest": "caller-self-digest"}),
            _construction_key=object(),
        )
    assert caught.value.reason_code == "authority_context_construction_forbidden"
