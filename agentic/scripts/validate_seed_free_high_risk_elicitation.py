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
"""Compatibility-located proposal-field-free elicitation self-check."""
from __future__ import annotations
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from agentic.discovery.hypotheses import build_hidden_elicitation_prompt, replay_proposal_field_free_high_risk_elicitation, run_proposal_field_free_high_risk_elicitation
from agentic.discovery.literature import build_demo_literature_snapshot

def main() -> int:
    snapshot = build_demo_literature_snapshot(target_id="proposal-field-free-elicitation-self-check")
    charter = {"target_id": snapshot["target_id"], "target_statement": "Explain the exact target without replacing its quantifiers.", "theory_state_digest": snapshot["theory_state_digest"], "root_tensions": ["Local witnesses do not explain global recurrence.", "Repeated barriers lack one mechanism."], "target_commitments": ["Preserve exact target identity and nontriviality."], "protected_successes": ["Recover the incumbent boundary regime."], "forbidden_target_drift": "Do not substitute a finite-only or lexical proxy."}
    prompts = [build_hidden_elicitation_prompt(prompt_id=f"hidden-{index}", target_id=snapshot["target_id"], theory_state_digest=snapshot["theory_state_digest"], literature_snapshot_digest=snapshot["content_digest"], prompt_text=f"Probe an underexplored conceptual dependency number {index} without proposal seeds.") for index in range(2)]
    study = run_proposal_field_free_high_risk_elicitation(charter, snapshot, hidden_prompts=prompts, repetitions=5, counterbalance_seed="self-check-seed")
    replay = replay_proposal_field_free_high_risk_elicitation(study, charter, snapshot, hidden_prompts=prompts, counterbalance_seed="self-check-seed")
    if not replay["same_seed_exact_replay"]:
        raise SystemExit("same-seed elicitation replay failed")
    print("proposal-field-free high-risk elicitation: pass")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
