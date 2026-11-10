# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""A first-round failure must be repairable before later rounds freeze it."""
import copy

import pytest

from agentic.discovery import bootstrap_reflection as bootstrap
from agentic.discovery.reflection import (
    ReflectionInvariantError, validate_reflection_round, validate_reflection_rounds,
)


def round_value():
    return {'round_id': 'round.first', 'system_ids': ['system.one'],
        'result': 'no_change', 'no_change_reason': 'No warranted structural change.',
        'strongest_objections': ['Exact objection.'], 'correction_tests': ['Exact test.'],
        'semantic_patch_links': [{'candidate_ref': 'system.one',
            'objection': 'Exact objection.', 'correction_test': 'Exact test.'}]}


@pytest.mark.parametrize('field,replacement', [
    ('objection', 'A paraphrase.'), ('correction_test', 'A different test.'),
    ('candidate_ref', 'system.absent'),
])
def test_first_round_rejects_broken_reference(field, replacement):
    value = round_value()
    value['semantic_patch_links'][0][field] = replacement
    with pytest.raises(ReflectionInvariantError):
        validate_reflection_round(value)


def test_single_round_validation_does_not_waive_two_round_gate():
    value = round_value()
    validate_reflection_round(value)
    with pytest.raises(ReflectionInvariantError, match='at least two'):
        validate_reflection_rounds([value], {})
    with pytest.raises(ReflectionInvariantError, match='plateau'):
        validate_reflection_rounds([value, copy.deepcopy(value)], {})
    validate_reflection_rounds([value, copy.deepcopy(value)],
        {'materially_empty_rounds': 2, 'action': 'reframe'})


def test_bootstrap_checks_first_round_before_accepting_history(monkeypatch):
    system = {'system_id': 'system.one'}
    value = round_value()
    value['semantic_patch_links'][0]['objection'] = 'Paraphrase wrongly accepted before.'
    monkeypatch.setattr(bootstrap, 'compile_system', lambda row: row)
    monkeypatch.setattr(bootstrap, 'authored_system_view', lambda row: row)
    monkeypatch.setattr(bootstrap, '_typed_unification_assessment', lambda row: None)

    class ProbeAuthor:
        def author(self, stage_id, **kwargs):
            kwargs['validator']({'systems': [system], 'round': value})
            pytest.fail('Invalid first round became accepted history')

    with pytest.raises(ReflectionInvariantError, match='exact objection'):
        bootstrap.author_reflection_round(ProbeAuthor(), stage_id='parent-reflection-1',
            systems=[system], rounds=[], charter={})
