# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
# SPDX-License-Identifier: MIT
"""Exercise contract invariants with synthetic, project-inspired compositions."""

from copy import deepcopy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

import yaml
from jsonschema import Draft202012Validator

PACKAGE = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('workflow_contract_validator', PACKAGE / 'scripts/validate_workflow.py')
validator = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = validator
spec.loader.exec_module(validator)


def reference(value):
    return {'ref': value}


def call(step, operation, **arguments):
    return {'id': step, 'kind': 'call', 'operation': operation, 'arguments': arguments}


def output(type_name, value):
    return {'type': type_name, 'value': reference(value)}


class ContractTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.root = Path(self.directory.name)
        self.path = self.root / 'workflow.yaml'
        self.data = validator.load_yaml(PACKAGE / 'references/example.workflow.yaml')

    def tearDown(self):
        self.directory.cleanup()

    def check(self, valid=True, data=None, **options):
        self.path.write_text(yaml.safe_dump(self.data if data is None else data, sort_keys=False))
        result = validator.validate(self.path, **options)
        self.assertEqual(result['valid'], valid, result['errors'])
        self.assertFalse(result['runtime_bindings_verified'])
        self.assertFalse(result['source_semantics_verified'])
        return result

    def test_schema_and_internal_references(self):
        schema = json.loads(validator.SCHEMA_PATH.read_text())
        Draft202012Validator.check_schema(schema)
        result = subprocess.run([sys.executable, str(PACKAGE / 'scripts/validate_workflow.py'), '--schema-only', '--json'], text=True, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(json.loads(result.stdout)['valid'])

    def test_example(self):
        self.check()

    def test_mathformer_bounded_repair(self):
        self.data['operations']['repair'] = deepcopy(self.data['operations']['analyze'])
        self.data['operations']['repair']['inputs'] = {'candidate': {'type': 'Candidate'}}
        body = {
            'kind': 'sequence', 'steps': [
                call('repair', 'repair', candidate=reference('loop.state')),
                call('check', 'validate', candidate=reference('steps.repair.outputs.candidate')),
            ],
            'outputs': {'candidate': output('Candidate', 'steps.repair.outputs.candidate'), 'report': output('ValidationReport', 'steps.check.outputs.report')},
        }
        loop = {
            'id': 'repair', 'kind': 'loop', 'state_type': 'Candidate',
            'initial': reference('steps.analyze.outputs.candidate'), 'body': body,
            'next_state': reference('body.outputs.candidate'),
            'until': {'eq': [reference('body.outputs.report.accepted'), {'literal': True}]},
            'max_iterations': 5, 'on_exhausted': 'blocked',
            'outputs': {'candidate': output('Candidate', 'loop.state'), 'report': output('ValidationReport', 'body.outputs.report')},
        }
        self.data['flow']['steps'] = [self.data['flow']['steps'][0], loop]
        self.data['outputs'] = {'candidate': output('Candidate', 'steps.repair.outputs.candidate'), 'validation': output('ValidationReport', 'steps.repair.outputs.report')}
        self.check()
        loop.pop('max_iterations')
        self.check(False)

    def test_bioagents_parallel_review(self):
        self.data['flow']['steps'][1] = {
            'id': 'reviews', 'kind': 'parallel', 'join': 'all', 'max_concurrency': 2,
            'branches': {
                name: call(name, 'validate', candidate=reference('steps.analyze.outputs.candidate'))
                for name in ['scientific', 'provenance']
            },
            'outputs': {'report': output('ValidationReport', 'branches.scientific.outputs.report'), 'audit': output('ValidationReport', 'branches.provenance.outputs.report')},
        }
        self.data['flow']['steps'][2]['condition'] = {'all': [reference('steps.reviews.outputs.report.accepted'), reference('steps.reviews.outputs.audit.accepted')]}
        self.data['outputs']['validation']['value'] = reference('steps.reviews.outputs.report')
        self.check()
        self.data['flow']['steps'][1]['branches']['provenance']['arguments']['candidate'] = reference('branches.scientific.outputs.report')
        self.check(False)

    def test_abducer_conditional_route_and_handoff(self):
        self.data['inputs']['candidate'] = {'type': 'Candidate', 'required': False}
        existing = {'kind': 'sequence', 'steps': [call('reuse', 'validate', candidate=reference('inputs.candidate'))], 'outputs': {'candidate': output('Candidate', 'inputs.candidate')}}
        choice = {
            'id': 'choose', 'kind': 'switch',
            'cases': [{'id': 'reuse', 'when': {'exists': reference('inputs.candidate')}, 'body': existing}],
            'default': call('generate', 'analyze', request=reference('inputs.request')),
            'outputs': {'candidate': output('Candidate', 'selected.outputs.candidate')},
        }
        self.data['operations']['deliver'] = deepcopy(self.data['operations']['validate'])
        self.data['operations']['deliver']['execution'] = {'mode': 'deterministic', 'binding': {'adapter': 'example.registry', 'kind': 'workflow', 'target': 'proof_delivery_workflow', 'operation': 'run'}}
        self.data['flow']['steps'] = [choice, {'id': 'deliver', 'kind': 'handoff', 'operation': 'deliver', 'arguments': {'candidate': reference('steps.choose.outputs.candidate')}, 'continuation': 'deferred'}]
        self.data['outputs'] = {'candidate': output('Candidate', 'steps.choose.outputs.candidate'), 'validation': output('ValidationReport', 'steps.deliver.outputs.report')}
        self.check()
        existing['outputs'] = {}
        self.check(False)

    def test_ruler_solver_then_human_review(self):
        self.data['operations']['analyze']['execution'] = {'mode': 'deterministic', 'binding': {'adapter': 'example.registered_cli', 'kind': 'action', 'target': 'solve', 'operation': 'run', 'profile': 'solver-lock'}}
        self.data['operations']['validate']['execution'] = {'mode': 'human', 'binding': {'adapter': 'example.review_receipt', 'kind': 'action', 'target': 'review', 'operation': 'accept'}}
        self.check(require_declared_bindings=True)

    def test_typed_map(self):
        self.data['types']['Candidates'] = {'schema': {'type': 'array', 'items': deepcopy(self.data['types']['Candidate']['schema'])}}
        self.data['types']['Reports'] = {'schema': {'type': 'array', 'items': deepcopy(self.data['types']['ValidationReport']['schema'])}}
        self.data['inputs']['candidates'] = {'type': 'Candidates'}
        self.data['flow'] = {'kind': 'map', 'items': reference('inputs.candidates'), 'item_type': 'Candidate', 'max_concurrency': 2, 'body': call('check', 'validate', candidate=reference('map.item')), 'outputs': {'reports': output('Reports', 'items.outputs.report')}}
        self.data['outputs'] = {'reports': output('Reports', 'flow.outputs.reports')}
        self.check()
        self.data['flow']['item_type'] = 'Request'
        self.check(False)

    def test_optional_input_requires_guard(self):
        self.data['inputs']['request']['required'] = False
        self.check(False)
        self.data['flow']['steps'].insert(0, {'id': 'present', 'kind': 'gate', 'condition': {'exists': reference('inputs.request')}, 'on_false': 'needs_input'})
        self.check()

    def test_unknown_type_in_unused_operation(self):
        self.data['operations']['unused'] = deepcopy(self.data['operations']['validate'])
        self.data['operations']['unused']['outputs']['report']['type'] = 'Imaginary'
        self.check(False)

    def test_unknown_operation(self):
        self.data['flow']['steps'][0]['operation'] = 'missing'
        self.check(False)

    def test_unknown_arguments(self):
        self.data['flow']['steps'][0]['arguments']['extra'] = {'literal': 1}
        self.check(False)

    def test_missing_arguments(self):
        self.data['flow']['steps'][0]['arguments'] = {}
        self.check(False)

    def test_nominal_type_mismatch(self):
        self.data['operations']['validate']['inputs']['candidate']['type'] = 'Request'
        self.check(False)

    def test_literal_payload_mismatch(self):
        self.data['flow']['steps'][0]['arguments']['request'] = {'literal': {'text': 12}}
        self.check(False)

    def test_forward_reference(self):
        self.data['flow']['steps'].reverse()
        self.check(False)

    def test_non_boolean_gate(self):
        self.data['flow']['steps'][2]['condition'] = reference('steps.analyze.outputs.candidate.content')
        self.check(False)

    def test_equality_of_different_literals_is_well_typed(self):
        self.data['flow']['steps'][2]['condition'] = {'eq': [{'literal': 1}, {'literal': 2}]}
        self.check()

    def test_unimplemented_operations_cannot_claim_active_or_complete(self):
        self.data['lifecycle'] = 'active'
        self.check(False)
        self.data['lifecycle'] = 'draft'
        self.data['provenance'] = {'coverage': 'complete', 'sources': [{'path': 'source.md'}], 'gaps': []}
        self.check(False)

    def test_nonexistent_field(self):
        self.data['flow']['steps'][2]['condition'] = reference('steps.validate.outputs.report.missing')
        self.check(False)

    def test_nullable_object_does_not_allow_unguarded_field_access(self):
        self.data['types']['ValidationReport']['schema']['type'] = ['object', 'null']
        self.check(False)

    def test_properties_alone_do_not_guarantee_an_object(self):
        self.data['types']['ValidationReport']['schema'].pop('type')
        self.check(False)

    def test_unknown_expression_operator(self):
        self.data['flow']['steps'][2]['condition'] = {'eval': 'print(1)'}
        self.check(False)

    def test_canonical_identity(self):
        for key, value in [('id', 'analysis-workflow'), ('id', 'analysis_loop'), ('kind', 'skill'), ('schema_version', 'workflow-skill/v2')]:
            data = deepcopy(self.data)
            data[key] = value
            self.check(False, data)

    def test_unknown_core_fields(self):
        self.data['flow']['steps'][0]['silently_skip_errors'] = True
        self.check(False)

    def test_extensions_must_be_namespaced(self):
        self.data['extensions'] = {'mathformer.backend': {'engine': 'lean'}}
        self.check()
        self.data['extensions'] = {'backend': {}}
        self.check(False)

    def test_duplicate_step_ids(self):
        self.data['flow']['steps'][1]['id'] = 'analyze'
        self.check(False)

    def test_nested_scope_does_not_leak(self):
        child = {'id': 'nested', 'kind': 'sequence', 'steps': [call('hidden', 'analyze', request=reference('inputs.request'))]}
        self.data['flow']['steps'].insert(1, child)
        self.data['flow']['steps'][2]['arguments']['candidate'] = reference('steps.hidden.outputs.candidate')
        self.check(False)

    def test_operation_effects_cannot_expand_policy(self):
        self.data['operations']['analyze']['effects'] = {'filesystem': {'read': ['inputs'], 'write': ['system']}, 'network': ['provider']}
        self.check(False)

    def test_operation_authority_cannot_expand_policy(self):
        self.data['operations']['analyze']['authority'] = {'allowed': ['approve'], 'forbidden': []}
        self.check(False)

    def test_conflicting_authority(self):
        self.data['policy']['authority']['allowed'].append('approve')
        self.check(False)

    def test_specification_only_is_not_bound(self):
        self.check(False, require_declared_bindings=True)
        self.data['operations']['analyze']['execution']['binding'] = {'adapter': 'example', 'kind': 'skill', 'target': 'analyze', 'operation': 'run'}
        self.check(False)

    def test_invalid_payload_schema(self):
        self.data['types']['Candidate']['schema'] = {'type': 'invented'}
        self.check(False)

    def test_local_schema_fragment_and_transitive_ref(self):
        (self.root / 'payload.json').write_text(json.dumps({'$defs': {'candidate': self.data['types']['Candidate']['schema']}}))
        (self.root / 'wrapper.json').write_text(json.dumps({'$schema': 'https://json-schema.org/draft/2020-12/schema', '$id': 'https://example.invalid/local-only', '$ref': 'payload.json#/$defs/candidate'}))
        self.data['types']['Candidate']['schema'] = 'wrapper.json'
        self.check()
        self.data['types']['Candidate']['schema'] = 'payload.json#/$defs/missing'
        self.check(False)

    def test_remote_schema_is_not_fetched(self):
        self.data['types']['Candidate']['schema'] = 'https://example.invalid/candidate.json'
        self.check(False)

    def test_remote_payload_ref_is_not_fetched(self):
        (self.root / 'payload.json').write_text(json.dumps({'$ref': 'https://example.invalid/payload.json'}))
        self.data['types']['Candidate']['schema'] = 'payload.json'
        self.check(False)

    def test_schema_cannot_escape_root_or_follow_escaping_symlink(self):
        self.data['types']['Candidate']['schema'] = '../outside.json'
        self.check(False)
        (self.root / 'escape.json').symlink_to(PACKAGE / 'references/workflow.schema.json')
        self.data['types']['Candidate']['schema'] = 'escape.json'
        self.check(False)

    def test_source_existence_and_digest(self):
        (self.root / 'source.md').write_text('native workflow')
        self.data['provenance']['sources'] = [{'path': 'source.md'}]
        self.check(repository_root=self.root)
        self.data['provenance']['sources'][0]['digest'] = 'sha256:' + '0' * 64
        self.check(False, repository_root=self.root)
        self.data['provenance']['sources'] = [{'path': 'missing.md'}]
        self.check(False, repository_root=self.root)

    def test_incomplete_coverage_requires_gaps(self):
        self.data['provenance']['gaps'] = []
        self.check(False)

    def test_safe_yaml_rejects_ambiguous_or_recursive_documents(self):
        for text in ['id: a\nid: b\n', 'a: &a [*a]\n', 'value: !!python/object:example {}\n', 'value: .nan\n', '12: value\n']:
            self.path.write_text(text)
            self.assertFalse(validator.validate(self.path)['valid'], text)

    def test_json_compatible_yaml_boolean_words(self):
        self.path.write_text('value: on\nother: true\ndate: 2026-10-21\n')
        self.assertEqual(validator.load_yaml(self.path), {'value': 'on', 'other': True, 'date': '2026-10-21'})

    def test_cli_exit_codes(self):
        self.check()
        command = [sys.executable, str(PACKAGE / 'scripts/validate_workflow.py'), str(self.path), '--json']
        result = subprocess.run(command, text=True, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(json.loads(result.stdout)[0]['valid'])
        self.data['id'] = 'bad'
        self.check(False)
        result = subprocess.run(command, text=True, capture_output=True)
        self.assertEqual(result.returncode, 1)
        self.assertFalse(json.loads(result.stdout)[0]['valid'])


if __name__ == '__main__':
    unittest.main()
