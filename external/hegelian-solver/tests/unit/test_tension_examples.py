# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT

from pathlib import Path

from hegelian_solver.io import read_structured


ROOT = Path(__file__).resolve().parents[2]


def test_realistic_tension_examples_are_structured():
    payload = read_structured(
        ROOT / "hegelian_solver/examples/tensions/realistic_tension_formalizations.yaml"
    )
    examples = payload["tension_examples"]

    assert len(examples) >= 4
    for example in examples:
        packet = example["tension_formalization_packet"]
        assert packet["exact_crisis_statement"]
        assert packet["crisis_types"]
        assert len(packet["minimal_incompatible_commitments"]) >= 3
        assert packet["formal_core"]["predicates"]
        assert packet["formal_core"]["failed_obligations"]
        assert packet["material_conditions"]["stakes"]
        assert packet["candidate_transformation_pressures"]
        assert packet["epistemic_status"]["possible_falsifiers"]
