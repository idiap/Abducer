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

from run_branch_exploration_cycle import build_branch_output


def test_branch_output_is_mathematical_not_placeholder():
    branch = {
        "branch_id": "fixture.branch",
        "title": "Cutoff-uniform correlator decay",
        "controlled_interface": "Euclidean correlator -> spectral measure",
        "machinery_role": "witness",
        "consecutive_low_learning_cycles": 0,
        "promotion_signal": "uniform decay plus observable density",
        "pivot_signal": "constants collapse",
    }
    output = build_branch_output(branch, 1)
    lemma = output["candidate_lemmas"][0]
    assert "source object" in " ".join(lemma["definitions"])
    assert "target object" in " ".join(lemma["definitions"])
    assert lemma["equations"][0]["valid_when"]
    assert output["falsifiers"]
    assert output["control_decision"]["decision"] == "persist_adapt"
