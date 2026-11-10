# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "agentic/scripts"))

from discovery_marathon_scheduler import select_branches


def test_scheduler_prefers_active_high_priority_branches():
    branches = [
        {"branch_id": "watch", "title": "Watch", "status": "watch", "priority": 1, "consecutive_low_learning_cycles": 0, "attempt_count": 0, "controlled_interface": "a -> b"},
        {"branch_id": "active-low", "title": "Active low", "status": "active", "priority": 3, "consecutive_low_learning_cycles": 0, "attempt_count": 0, "controlled_interface": "a -> c"},
        {"branch_id": "active-high", "title": "Active high", "status": "active", "priority": 1, "consecutive_low_learning_cycles": 0, "attempt_count": 0, "controlled_interface": "a -> d"},
    ]
    selected, decisions = select_branches(branches, max_active=2)
    assert [row["branch_id"] for row in selected] == ["active-high", "active-low"]
    assert decisions[0]["recommended_move"] == "persist_adapt"


def test_scheduler_requests_restrategy_for_repeated_low_learning():
    branches = [
        {"branch_id": "stale", "title": "Stale", "status": "active", "priority": 1, "consecutive_low_learning_cycles": 2, "attempt_count": 4, "controlled_interface": "x -> y"}
    ]
    _, decisions = select_branches(branches, max_active=1)
    assert decisions[0]["recommended_move"] == "restrategize_with_backtrack_test"
