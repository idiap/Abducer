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


def test_abductive_mechanism_examples_are_structured():
    payload = read_structured(
        ROOT / "hegelian_solver/examples/mechanisms/abductive_mechanism_requirements.yaml"
    )
    examples = payload["mechanism_examples"]

    assert len(examples) >= 3
    for example in examples:
        abduction = example["mechanism_abduction_packet"]
        requirements = example["mechanism_requirements_packet"]
        critique = example["mechanism_counterfactual_critique"]
        todos = example["mechanism_todo_packet"]

        assert abduction["crisis_ref"] == example["source_tension_ref"]
        assert abduction["required_mediation_shape"]["commitments_to_preserve"]
        assert abduction["required_mediation_shape"]["missing_relation_or_process"]
        assert abduction["required_mediation_shape"]["inference_commitments"]
        assert abduction["mechanism_hypotheses"]

        assert requirements["selected_hypothesis_refs"]
        assert len(requirements["requirements"]) >= 5
        assert requirements["mediation_maps"]
        assert requirements["validation_obligations"]
        assert requirements["residual_limits"]
        for requirement in requirements["requirements"]:
            assert requirement["kind"]
            assert requirement["necessity_status"]
            assert requirement["statement"]
            assert requirement["validation_method"]
            assert requirement["failure_mode_if_missing"]

        assert critique["counterfactual_tests"]
        assert critique["collapse_risks"]
        assert critique["evidence_or_experiment_priorities"]

        assert todos["todo_groups"]
        assert todos["stop_conditions"]
        for group in todos["todo_groups"]:
            assert group["purpose"]
            assert group["todos"]
            for todo in group["todos"]:
                assert todo["class"]
                assert todo["why_needed"]
                assert todo["artifact_expected"]
                assert todo["acceptance_criterion"]
