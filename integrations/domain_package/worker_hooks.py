# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Worker-only input and report boundary for the real Discovery Marathon graph.

Lunar supplies model access to its Prism engine. These hooks never call a model,
read credentials, return sample outputs, or execute scientific tools. Verification
establishes typed execution and report fidelity, not the truth of model claims.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

STEPS = (
    ('BoundedDiscoveryScope', 'Scope', 'bounded_scope'),
    ('DiscriminatingDiscoveryHypothesis', 'Hypothesis', 'hypothesis'),
    ('ProvisionalDiscoveryPattern', 'Observed pattern', 'provisional_pattern'),
    ('HypothesisModelImplications', 'Model implications', 'bounded_model_implications'),
    ('HypothesisContrastAssessment', 'Contrast test', 'controlled_contrast'),
    ('HypothesisRefutationAssessment', 'Refutation assessment', 'scoped_refutation'),
    ('DiscoveryRoutingAssessment', 'Next action', 'routing_basis'),
)


def _digest(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False,
                                     separators=(',', ':'), allow_nan=False).encode()).hexdigest()


def prepare(*, workflow_id: str, inputs: dict, mode: str, run_id: str,
            run_root: Path, network_authority: bool, on_reasoning, **kwargs) -> dict:
    """Validate the form input and preserve its exact text in the typed argument."""
    # Retain the runtime callback parameter while preparation remains read-only.
    del on_reasoning
    if workflow_id != 'discovery_marathon_loop' or mode != 'live':
        raise ValueError('Only Discovery Marathon live execution is registered')
    if network_authority:
        raise ValueError('This reasoning workflow does not use network downloads')
    if not isinstance(inputs, dict) or set(inputs) != {'context_summary'}:
        raise ValueError('Supply exactly one research context field: context_summary')
    text = inputs['context_summary']
    if not isinstance(text, str) or not text.strip() or len(text) > 16000:
        raise ValueError('Research context must contain 1 to 16000 characters of nonblank text')
    value = dict(inputs)
    digest = _digest({'workflow_id': workflow_id, 'mode': mode, 'inputs': value})
    return {'prepared_input': {'entry_argument_name': 'context', 'value': value,
                               'request_digest': digest, 'analysis_results': {}},
            'state': {'input': value, 'request_digest': digest, 'run_root': run_root},
            'events': [{'kind': 'input', 'payload': {
                'input_key': 'context_summary', 'kind': 'user_context',
                'safe_locator': 'request:context_summary',
                'content_digest': 'sha256:' + _digest(value)}},
                {'kind': 'stage', 'payload': {'stage_id': 'prepare', 'component_id': workflow_id,
                 'status': 'completed', 'safe_summary': 'Research context validated for one discovery cycle.'}}]}


def _value(value: Any) -> Any:
    """Project public Prism values without losing closed-variant identities."""
    from prism.language.core import GeneratedValue, Ok, RecordValue
    if isinstance(value, (Ok, GeneratedValue)):
        return _value(value.value)
    if isinstance(value, RecordValue):
        if not value.fields:
            return value.type_name.rsplit('.', 1)[-1]
        return {key: _value(item) for key, item in value.fields.items()}
    if isinstance(value, dict):
        return {key: _value(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_value(item) for item in value]
    if isinstance(value, (str, bool, int, float)) or value is None:
        return value
    raise ValueError('Unsupported Prism result value')


def verify(*, state: dict, execution, services) -> dict:
    """Render actual typed output only after all seven model effects succeed."""
    if execution.status != 'accepted' or execution.diagnostics:
        raise ValueError('Discovery execution did not complete cleanly')
    records = [r for r in execution.effect_records.values() if r.invocation.symbol == 'generate']
    if len(records) != 7 or any(r.observation.status != 'accepted' for r in records):
        raise ValueError('Discovery requires seven successful model effects')
    steps = {}
    for record in records:
        if execution.effect_recorder.offline_verify(record).status != 'verified':
            raise ValueError('Recorded model artifacts failed digest verification')
        stored = execution.effect_recorder.store.get(record.observation.output_artifact)['value']
        # Public effect artifacts serialize Ok and GeneratedValue as value wrappers.
        while isinstance(stored, dict) and 'value' in stored:
            stored = stored['value']
        if not isinstance(stored, dict) or set(stored) != {'type_name', 'fields'}:
            raise ValueError('Expected a typed model record in the effect artifact')
        name = stored['type_name'].rsplit('.', 1)[-1]
        if name in steps:
            raise ValueError('Duplicate discovery step output')
        steps[name] = stored['fields']
    if set(steps) != {name for name, _, _ in STEPS}:
        raise ValueError('Discovery effect artifacts do not cover the seven typed steps')
    for name, _, field in STEPS:
        if not isinstance(steps[name].get(field), str) or not steps[name][field].strip():
            raise ValueError('Discovery step output is empty')
    value = _value(execution.typed_result)
    if not isinstance(value, dict) or set(value) != {'disposition', 'routing_basis'}:
        raise ValueError('Expected a DiscoveryRoutingAssessment')
    if value['disposition'] not in {'Promotable', 'Reorient', 'TargetReset', 'Stalled'}:
        raise ValueError('Unknown discovery disposition')
    if not isinstance(value['routing_basis'], str) or not value['routing_basis'].strip():
        raise ValueError('Discovery routing requires a nonempty basis')
    if steps['DiscoveryRoutingAssessment'] != value:
        raise ValueError('Final result differs from the recorded routing output')
    provenance = {'source_hash': execution.source_hash, 'module_hashes': dict(execution.module_hashes),
                  'request_digest': state['request_digest'], 'model_effects': len(records),
                  'output_digests': [r.observation.output_digest for r in records]}
    markdown = ('# Discovery Marathon Loop\n\n## Research context\n\n' + state['input']['context_summary']
                + '\n\n## Routing decision\n\n**' + value['disposition'] + '**\n\n' + value['routing_basis']
                + '\n\n## Reasoning steps\n\n'
                + '\n\n'.join('### ' + label + '\n\n' + steps[name][field] for name, label, field in STEPS)
                + '\n\n## Interpretation\n\nThis report contains model-generated reasoning from one discovery cycle. '
                'Proposed experiments were not executed, and scientific claims were not independently verified. '
                'Promotable means a candidate for further review, not a proved or released result.\n')
    receipt = {'status': 'passed', 'scope': 'typed execution and report projection only',
               'scientific_truth_verified': False, 'markdown_sha256': hashlib.sha256(markdown.encode()).hexdigest()}
    result = {'markdown': markdown, 'structured_value': {**value, 'steps': steps, 'execution_provenance': provenance},
              'analysis_results': {}, 'compact_prism_input': state['input'],
              'narrative_slots': [], 'report_verification': receipt}
    # The host independently hashes and inventories these actual run artifacts.
    (state['run_root'] / 'report.md').write_text(markdown)
    (state['run_root'] / 'discovery-result.json').write_text(json.dumps(result, indent=2, allow_nan=False))
    return {'result': result, 'events': [{'kind': 'stage', 'payload': {
        'stage_id': 'report', 'component_id': 'discovery_marathon_loop', 'status': 'completed',
        'safe_summary': 'Seven model effects completed; typed routing report saved.'}}]}
