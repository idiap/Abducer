# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Behavioral checks for preservation, reproducibility and invalid model rejection."""
import copy
import json
from pathlib import Path
import shutil
import tempfile
import unittest

from render_taxonomy import render, validate


def fixture():
    """Use an illustrative typed calibration case, not a claimed runtime trace."""
    def port(name, expression='Generated[Assessment]'):
        return {'name': name, 'type_id': 'type:generated' if expression.startswith('Generated') else 'type:observations', 'source_type_expression': expression, 'wrapper': 'Generated' if expression.startswith('Generated') else None}
    model = {'schema_version': '1.0.0', 'packet_id': 'test', 'layers': [], 'families': [],
            'artifact_types': [{'id': 'type:assessment', 'label': 'Assessment'}, {'id': 'type:generated', 'label': 'Generated[Assessment]', 'type_arguments': ['type:assessment']}, {'id': 'type:observations', 'label': 'Observations'}],
            'operations': [{'id': 'op:calibrate', 'label': 'Calibrate assessment with observations', 'family_ids': [], 'workflow_ids': ['workflow:calibration'], 'inputs': [port('assessment'), port('observations', 'Observations')], 'outputs': [port('updated')]}],
            'workflows': [{'id': 'workflow:calibration', 'label': 'Illustrative calibration', 'operation_ids': ['op:calibrate'], 'inputs': [port('assessment')], 'outputs': [port('updated')]}],
            'relations': [], 'scope': {'requested_workflow_ids': ['workflow:calibration']},
            'coverage': [{'workflow_id': 'workflow:calibration', 'disposition': 'modeled', 'reason': 'Illustrative test scope'}]}
    for entity in model['operations'] + model['workflows'] + model['artifact_types']:
        entity.update(claim_status='declared', source_posture='declared')
    for artifact in model['artifact_types']:
        for field in ('fields', 'alternatives', 'type_arguments'):
            artifact.setdefault(field, [])
    return model


class RendererTests(unittest.TestCase):
    def test_invalid_references_fail_before_writes(self):
        for mutate in (
            lambda m: m['operations'][0]['family_ids'].append('missing'),
            lambda m: m['operations'][0]['inputs'][0].update(type_id='missing'),
            lambda m: m['operations'][0].update(id=m['workflows'][0]['id']),
            lambda m: m['coverage'].clear(),
            lambda m: m['operations'][0]['inputs'][0].pop('source_type_expression'),
        ):
            model = fixture()
            mutate(model)
            with tempfile.TemporaryDirectory() as directory:
                output = Path(directory) / 'output'
                with self.assertRaises(ValueError):
                    render(model, b'{}', output)
                self.assertFalse(output.exists())

    def test_subtypes_reject_wrong_endpoints_and_cycles(self):
        model = fixture()
        relation = {'id': 'relation:bad', 'source_id': 'op:calibrate', 'target_id': 'type:assessment', 'kind': 'declared_subtype', 'claim_status': 'declared', 'source_posture': 'declared'}
        model['relations'] = [relation]
        with self.assertRaises(ValueError):
            validate(model)
        relation['source_id'] = 'type:assessment'
        with self.assertRaisesRegex(ValueError, 'cycle'):
            validate(model)

    def test_multiple_family_memberships_and_unknown_ports_survive(self):
        model = fixture()
        model['families'] = [{'id': name, 'label': name, 'layer_ids': [], 'claim_status': 'declared', 'source_posture': 'declared'} for name in ('family:a', 'family:b')]
        model['operations'][0]['family_ids'] = ['family:a', 'family:b']
        model['operations'][0]['inputs'][0].update(type_id=None, unknown_reason='Unavailable contract')
        validate(model)

    @unittest.skipUnless(shutil.which('dot'), 'Graphviz required for vector rendering')
    def test_output_semantics_hashes_and_reproducibility(self):
        model = fixture()
        raw = json.dumps(model).encode()
        with tempfile.TemporaryDirectory() as directory:
            first, second = Path(directory) / 'first', Path(directory) / 'second'
            manifest = render(model, raw, first)
            render(copy.deepcopy(model), raw, second)
            for path in first.iterdir():
                if path.suffix in ('.dot', '.svg', '.tex'):
                    self.assertEqual(path.read_bytes(), (second / path.name).read_bytes())
            dot = (first / 'io-01-01.dot').read_text()
            for expected in ('assessment:', 'observations:', 'Generated[Assessment]', 'label="input"', 'label="output"'):
                self.assertIn(expected, dot.replace(r'\n', ''))
            self.assertIn('(unclassified)', (first / 'taxonomy-01.dot').read_text())
            self.assertEqual(manifest['semantic_model'], model)
            self.assertIn('taxonomy-figures.tex', manifest['output_sha256'])
            self.assertTrue((first / 'io-01-01.pdf').read_bytes().startswith(b'%PDF'))
            with self.assertRaisesRegex(ValueError, 'empty'):
                render(model, raw, first)


if __name__ == '__main__':
    unittest.main()
