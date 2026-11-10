# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Fail-closed input and verification tests without a model or Docker service."""
from pathlib import Path
from tempfile import TemporaryDirectory
from types import SimpleNamespace
import unittest

from integrations.domain_package.worker_hooks import prepare, verify
from integrations.domain_package.runtime_registration import INPUT_SCHEMA, registration
from jsonschema import Draft202012Validator, ValidationError


class DiscoveryHookTests(unittest.TestCase):
    def setUp(self):
        self.temp = TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def prepare(self, inputs, **changes):
        args = dict(workflow_id='discovery_marathon_loop', inputs=inputs, mode='live',
                    run_id='test', run_root=self.root, network_authority=False,
                    on_reasoning=lambda **kw: None)
        args.update(changes)
        return prepare(**args)

    def test_exact_input_and_digest_sensitivity(self):
        text = '  Plants differ in light and watering.\nKeep both hypotheses. '
        first = self.prepare({'context_summary': text})
        self.assertEqual(first['prepared_input']['value'], {'context_summary': text})
        second = self.prepare({'context_summary': text + 'X'})
        self.assertNotEqual(first['prepared_input']['request_digest'], second['prepared_input']['request_digest'])
        self.assertEqual(list(self.root.iterdir()), [])

    def test_invalid_inputs_never_write(self):
        for bad in ({}, {'context_summary': ''}, {'context_summary': '  \n'},
                    {'context_summary': 42}, {'context_summary': 'x' * 16001},
                    {'context_summary': 'ok', 'path': '/etc/passwd'}):
            with self.subTest(bad=str(bad)[:70]), self.assertRaises(ValueError):
                self.prepare(bad)
        self.assertEqual(list(self.root.iterdir()), [])

    def test_unregistered_workflow_mode_and_authority(self):
        for changes in ({'workflow_id': 'theorem_proof_delivery'}, {'mode': 'fixture'},
                        {'network_authority': True}):
            with self.subTest(changes=changes), self.assertRaises(ValueError):
                self.prepare({'context_summary': 'test'}, **changes)

    def test_partial_execution_cannot_release_report(self):
        state = self.prepare({'context_summary': 'test'})['state']
        for status, diagnostics, records in [('rejected', (), {}), ('accepted', ('bad',), {}), ('accepted', (), {})]:
            with self.subTest(status=status, diagnostics=diagnostics), self.assertRaises(ValueError):
                verify(state=state, execution=SimpleNamespace(status=status, diagnostics=diagnostics,
                       effect_records=records), services=None)
        self.assertEqual(list(self.root.iterdir()), [])

    def test_native_host_schema_rejects_demo_inputs_and_false_success(self):
        Draft202012Validator.check_schema(INPUT_SCHEMA)
        validator = Draft202012Validator(INPUT_SCHEMA)
        validator.validate({'target_id': 'target-a', 'run_id': 'run-a'})
        with self.assertRaises(ValidationError):
            validator.validate({'context_summary': '\n  '})
        output = registration()['output_schema']
        Draft202012Validator.check_schema(output)
        with self.assertRaises(ValidationError):
            Draft202012Validator(output).validate({'markdown': 'Proven',
                'structured_value': {'disposition': 'Proven'},
                'report_verification': {'status': 'passed', 'scientific_truth_verified': True}})


if __name__ == '__main__':
    unittest.main()
