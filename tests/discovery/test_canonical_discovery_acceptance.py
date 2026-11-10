# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Integrated acceptance regressions for the exact canonical discovery run."""

from __future__ import annotations

import json
import runpy
import sys
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "agentic/scripts"))

from agentic.discovery.contracts import ContractError  # noqa: E402
from validate_canonical_discovery_acceptance import (  # noqa: E402
    validate_canonical_acceptance,
)
from canonical_discovery_publication import (  # noqa: E402
    DEFAULT_PUBLICATION_ROOT,
    validate_current_publication,
)


def _paths(tmp_path: Path, *, live: bool) -> dict:
    """Build acceptance evidence with the current canonical constructors.

    Historical report snapshots are useful documentation, but they are not a
    durable executable fixture when receipt authority evolves.  Rebuilding the
    exact six-operator lineage here keeps this regression bound to the current
    canonical request, receipt, sealing, and commit contracts.
    """

    exercise_module = runpy.run_path(
        str(Path(__file__).with_name("test_canonical_discovery_cycle.py"))
    )
    exercise_type = exercise_module["CanonicalExercise"]
    base = tmp_path / ("active-current-registry" if live else "local-only")
    base.mkdir(parents=True)
    exercise = exercise_type(
        base,
        live=live,
        experiment=live,
        registry_routes=live,
    )
    cycle = exercise_module["run_canonical_discovery_cycle"](**exercise.cycle_kwargs())
    cycle_path = base / "cycle-result.json"
    cycle_request_path = exercise.workspace / "canonical-cycle-request.json"
    cycle_path.write_text(
        json.dumps(cycle, sort_keys=True, separators=(",", ":")) + "\n",
        encoding="utf-8",
    )
    cycle_request_path.write_text(
        json.dumps(
            {
                "operator_requests": exercise.requests,
                "operator_receipts": exercise.receipts,
                "artifact_roles": exercise.roles,
            },
            sort_keys=True,
            separators=(",", ":"),
        )
        + "\n",
        encoding="utf-8",
    )
    return {
        "cycle_path": cycle_path,
        "cycle_request_path": cycle_request_path,
        "state_root": exercise.state_root,
        "workspace": exercise.workspace,
        "receipt_root": exercise.workspace / "operator-receipts",
        "target_id": exercise.target_id,
        "run_id": exercise.run_id,
    }


@pytest.mark.skip(
    reason="User-deferred: checked-in publication is v1; genuine current v2 evidence is missing. "
    "See .prism/idiap-software-disclosure/09-publication-migration.md."
)
def test_checked_in_current_cycle_passes_full_causal_acceptance() -> None:
    publication = validate_current_publication(
        publication_root=DEFAULT_PUBLICATION_ROOT
    )
    result = publication["acceptance"]

    assert result["status"] == "passed"
    assert result["operator_count"] == 6
    assert result["all_operators_feedback_effective"] is True
    assert result["literature_mode"] == "active_current"
    assert result["high_risk_candidate_count"] >= 8
    assert result["valid_parallel_branch_count"] >= 2
    assert result["retained_dissent_count"] >= 1
    assert result["experiment_subordinate"] is True


def test_incomplete_local_only_cycle_cannot_satisfy_acceptance(tmp_path: Path) -> None:
    paths = _paths(tmp_path, live=False)
    cycle = json.loads(paths["cycle_path"].read_text(encoding="utf-8"))
    assert cycle["literature_basis"]["mode"] == "local_only_incubation"
    # This local control fixture lacks the required production feedback chain,
    # so acceptance must reject it before the later investment-mode boundary.
    with pytest.raises(ContractError, match="feedback chain is incomplete"):
        validate_canonical_acceptance(**paths)
