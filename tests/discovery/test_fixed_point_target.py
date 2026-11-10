# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Keep the known-theorem target scoped across initialization and reporting."""
import importlib.util
from pathlib import Path

from agentic.discovery.bootstrap_authoring import high_risk_charter, target_context


ROOT = Path(__file__).resolve().parents[2]


def test_fixed_point_target_preserves_scope_and_repository_source():
    context = target_context('markov-kakutani-fixed-point-theorem-target')
    assert 'finite pairwise commuting' in context['statement']
    assert 'not a claim of novel discovery' in context['commitments'][0]
    assert 'st.lem.finite-family-common-fixed-point' in (
        ROOT / 'KB/markov-kakutani-fixed-point-theorem.kb.md').read_text()
    assert 'P versus NP' == target_context('p-vs-np-target')['topic']


def test_fixed_point_profile_is_readable_and_target_specific():
    spec = importlib.util.spec_from_file_location('fixed_point_profiles', ROOT / 'agentic/scripts/target_profiles.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    profile = module.target_profile('markov-kakutani-fixed-point-theorem-target')
    assert profile['target_id'] == 'markov-kakutani-fixed-point-theorem-target'
    assert 'Markov-Kakutani' in profile['display_name']
    assert 'subnets' in profile['decisive_target_invariant']
    assert module.target_profile('p-vs-np-target')['domain'] == 'computational complexity theory'


def test_known_theorem_uses_explicit_supported_wildcard_exception():
    record = {'value': {'root_tensions': [{'minimal_incompatibility_or_missing_mediation': 'Fixed-set invariance'}],
        'discovery_charter': {'target_commitments': ['Keep exact commutativity']},
        'conceptual_genealogy': {'protected_successes': ['Single-map theorem']}}}
    charter = high_risk_charter('markov-kakutani-fixed-point-theorem-target', 'digest', record)
    assert charter['wildcards_available'] is False
    assert 'established finite-family theorem' in charter['fewer_wildcards_reason']
    assert 'wildcards_available' not in high_risk_charter('p-vs-np-target', 'digest', record)
