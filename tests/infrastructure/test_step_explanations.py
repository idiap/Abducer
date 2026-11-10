# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Adversarial integrity checks for the manual source-bound paper lane."""
import copy
import importlib.util
import json
from pathlib import Path
import tempfile
import subprocess
import sys
import unittest

SCRIPT = Path(__file__).resolve().parents[2] / 'proj_skills/framework-paper-validator/scripts/step_explanations.py'
spec = importlib.util.spec_from_file_location('step_explanations', SCRIPT)
gate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gate)


class StepExplanationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.manifest = 'native/manifest.json'
        self.native = {'workflows': [{'id': 'hyphen-workflow', 'module_id': 'different_module',
            'layers': {layer: 'different_module/' + layer + '.prism'
                       for layer in ('types', 'occurrences', 'relations', 'reasoning')}}]}
        self.write(self.manifest, json.dumps(self.native))
        self.write('native/different_module/types.prism', 'type Input\ntype Output\n')
        self.write('native/different_module/relations.prism', '# no relation needed\n')
        self.write('native/different_module/occurrences.prism',
                   'type Operation = Input -> Generated[Output]\n')
        self.write('native/different_module/reasoning.prism',
                   '# [ignored: CommentedOperation(x)]\n    [result: Operation(input)]\n')
        step = {field: 'Concrete source grounded explanation with enough substantive words.' for field in gate.FIELDS}
        step.update(binding='result', operation='Operation', signature='Input -> Generated[Output]',
                    title='Construct result', evidence=[{'path': 'native/different_module/occurrences.prism', 'start': 1, 'end': 1}],
                    posture='declaration + prescribed procedure; illustration not execution')
        row = dict(id='hyphen-workflow', case='A continuing concrete case.', contrast='Changing the premise changes the disposition.', steps=[step])
        self.packet = dict(version='1.0', manifest=self.manifest, sources={}, scope=['hyphen-workflow'], workflows=[row])
        self.freeze()
        self.review()

    def write(self, name, text):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)

    def freeze(self):
        self.packet['sources'] = {p.relative_to(self.root).as_posix(): gate.digest(p.read_bytes()) for p in (self.root / 'native').rglob('*') if p.is_file()}

    def review(self):
        for row in self.packet['workflows']:
            row['review'] = dict(verdict='pass', content_digest=gate.content_digest(row), sources_digest=gate.digest(self.packet['sources']), criteria=list(gate.FIELDS),
                rationale='Each named input and output was manually compared against its source declaration and the illustrative procedure was checked for continuity.',
                limitations='This fixture tests integrity only and establishes no semantic validity.')

    def check(self):
        return gate.validate(self.packet, self.root)

    def test_valid_manifest_paths_and_module_fallback(self):
        self.assertEqual(self.check()['steps'], 1)
        del self.native['workflows'][0]['layers']
        self.write(self.manifest, json.dumps(self.native))
        self.freeze()
        self.review()
        self.assertEqual(self.check()['workflows'], 1)

    def test_scope_cannot_be_shrunk(self):
        self.packet['scope'] = []
        self.packet['workflows'] = []
        with self.assertRaisesRegex(ValueError, 'scope differs'):
            self.check()

    def test_missing_duplicate_unknown_binding(self):
        original = copy.deepcopy(self.packet)
        for steps, message in [([], 'step count'), ([original['workflows'][0]['steps'][0]] * 2, 'duplicate step binding')]:
            self.packet = copy.deepcopy(original)
            self.packet['workflows'][0]['steps'] = steps
            with self.assertRaisesRegex(ValueError, message):
                self.check()
        self.packet = original
        self.packet['workflows'][0]['steps'][0]['binding'] = 'unknown'
        with self.assertRaisesRegex(ValueError, 'binding coverage'):
            self.check()

    def test_signature_and_operation_must_match(self):
        step = self.packet['workflows'][0]['steps'][0]
        step['signature'] = 'Different -> Generated[Output]'
        with self.assertRaisesRegex(ValueError, 'signature'):
            self.check()
        step['operation'] = 'OtherOperation'
        with self.assertRaisesRegex(ValueError, 'binding coverage'):
            self.check()

    def test_omitted_field_and_duplicate_json_key(self):
        del self.packet['workflows'][0]['steps'][0]['procedure']
        with self.assertRaisesRegex(ValueError, 'field procedure'):
            self.check()
        self.write('duplicate.json', '{"purpose":"first", "purpose":"overwritten"}')
        with self.assertRaisesRegex(ValueError, 'duplicate JSON field'):
            gate.load_json(self.root / 'duplicate.json')

    def test_stale_source_and_review(self):
        self.write('native/different_module/types.prism', 'changed source\n')
        with self.assertRaisesRegex(ValueError, 'stale source'):
            self.check()
        self.freeze()
        self.packet['workflows'][0]['steps'][0]['procedure'] += ' Authored text changed.'
        with self.assertRaisesRegex(ValueError, 'stale review'):
            self.check()

    def test_short_precise_fields_allowed_but_empty_or_nontext_rejected(self):
        step = self.packet['workflows'][0]['steps'][0]
        step.update(input='Candidate claim; retained premises.', output='Conditional assessment.')
        self.review()
        self.assertEqual(self.check()['steps'], 1)
        for field in gate.FIELDS:
            original = step[field]
            for value in ('', ' \n\t', None, [], 12):
                step[field] = value
                with self.subTest(field=field, value=value), self.assertRaisesRegex(ValueError, 'field ' + field):
                    self.check()
            step[field] = original

    def test_refreezing_changed_sources_invalidates_review(self):
        self.write('native/different_module/types.prism', 'new type contents\n')
        self.freeze()
        with self.assertRaisesRegex(ValueError, 'stale review sources'):
            self.check()

    def test_duplicate_declarations_are_not_silently_overwritten(self):
        self.write('native/different_module/occurrences.prism',
                   'type Operation = Input -> Generated[Output]\n' * 2)
        self.freeze()
        with self.assertRaisesRegex(ValueError, 'duplicate native declaration'):
            self.check()

    def test_invalid_span_types_are_rejected(self):
        self.packet['workflows'][0]['steps'][0]['evidence'][0]['start'] = 1.0
        with self.assertRaisesRegex(ValueError, 'invalid source span type'):
            self.check()

    def test_review_requires_complete_criteria_and_limitations(self):
        self.packet['workflows'][0]['review']['criteria'].append('purpose')
        with self.assertRaisesRegex(ValueError, 'incomplete review criteria'):
            self.check()
        self.review()
        del self.packet['workflows'][0]['review']['limitations']
        with self.assertRaisesRegex(ValueError, 'review limitations'):
            self.check()

    def test_missing_review_only_allowed_for_draft(self):
        del self.packet['workflows'][0]['review']
        with self.assertRaisesRegex(ValueError, 'semantic review'):
            self.check()
        self.assertEqual(gate.validate(self.packet, self.root, False)['steps'], 1)

    def test_spans_and_frozen_evidence(self):
        ref = self.packet['workflows'][0]['steps'][0]['evidence'][0]
        ref['end'] = 999
        with self.assertRaisesRegex(ValueError, 'invalid source span'):
            self.check()
        ref['path'] = 'unfrozen.md'
        with self.assertRaisesRegex(ValueError, 'unfrozen evidence'):
            self.check()

    def test_unresolved_gap_must_be_explicit(self):
        for layer in ('occurrences', 'reasoning'):
            path = self.root / ('native/different_module/' + layer + '.prism')
            path.write_text(path.read_text().replace('Operation', 'UnresolvedProjection'))
        step = self.packet['workflows'][0]['steps'][0]
        step['operation'] = 'UnresolvedProjection'
        self.freeze()
        with self.assertRaisesRegex(ValueError, 'hidden projection gap'):
            self.check()
        step['procedure'] += ' The native producer remains unresolved.'
        self.review()
        self.assertEqual(self.check()['steps'], 1)

    def test_paths_cannot_escape_through_parent_absolute_or_symlink(self):
        with tempfile.TemporaryDirectory() as outside:
            target = Path(outside) / 'secret.txt'
            target.write_text('outside')
            (self.root / 'escape').symlink_to(target)
            for name in ('../secret.txt', str(target), 'escape'):
                with self.subTest(name=name), self.assertRaisesRegex(ValueError, 'nonlocal'):
                    gate.local(self.root, name)

    def test_duplicate_native_binding_and_manifest_workflow(self):
        self.write('native/different_module/reasoning.prism', '[result: Operation(x)]\n[result: Operation(y)]\n')
        self.freeze()
        with self.assertRaisesRegex(ValueError, 'duplicate native bindings'):
            self.check()
        self.native['workflows'] *= 2
        self.write(self.manifest, json.dumps(self.native))
        self.freeze()
        with self.assertRaisesRegex(ValueError, 'duplicate manifest workflow'):
            self.check()

    def test_render_is_deterministic_inert_and_binding_visible(self):
        row = self.packet['workflows'][0]
        row['case'] = r'\input{secret} $ & % # _ ~ ^'
        rendered = gate.render(row)
        self.assertEqual(rendered, gate.render(row))
        self.assertNotIn(r'\input{secret}', rendered)
        self.assertIn(r'\textbackslash{}input\{secret\}', rendered)
        self.assertIn(r'\texttt{result}', rendered)
        row['id'] = 'id\n\\input{secret}'
        self.assertNotIn(r'\input{secret}', gate.render(row))

    def test_render_keeps_all_fields_separate_and_preserves_qualifications(self):
        row = self.packet['workflows'][0]
        step = row['steps'][0]
        for field in gate.FIELDS:
            step[field] = field + r': target_A & conditional result; \input{secret}'
        rendered = gate.render(row)
        blocks = rendered.split(r'\begin{description}', 1)[1].split(r'\end{description}', 1)[0]
        items = blocks.split(r'\item[')[1:]
        self.assertEqual(len(items), len(gate.FIELDS))
        for item, field in zip(items, gate.FIELDS):
            content = item.split('] ', 1)[1].strip()
            self.assertEqual(content, gate.tex(step[field]))
            for other in gate.FIELDS:
                if other != field:
                    self.assertNotIn(gate.tex(step[other]), content)
        self.assertNotIn(r'\input{secret}', rendered)

    def test_duplicate_scope_and_unsafe_workflow_id(self):
        self.packet['scope'] *= 2
        with self.assertRaisesRegex(ValueError, 'duplicate scope'):
            self.check()
        unsafe = '../escape'
        self.native['workflows'][0]['id'] = unsafe
        self.write(self.manifest, json.dumps(self.native))
        self.packet['scope'] = [unsafe]
        self.packet['workflows'][0]['id'] = unsafe
        self.freeze()
        with self.assertRaisesRegex(ValueError, 'unsafe workflow id'):
            self.check()

    def test_duplicate_examples_are_rejected(self):
        self.write('native/different_module/reasoning.prism',
                   '[result: Operation(input)]\n[next_result: Operation(result.value)]\n')
        extra = copy.deepcopy(self.packet['workflows'][0]['steps'][0])
        extra['binding'] = 'next_result'
        self.packet['workflows'][0]['steps'].append(extra)
        self.freeze()
        with self.assertRaisesRegex(ValueError, 'duplicate example'):
            self.check()

    def test_cli_respects_repo_for_rendering(self):
        self.write('packet.json', json.dumps(self.packet))
        self.write('paper/main.tex', '\\input{fragments/hyphen-workflow}\n')
        result = subprocess.run([sys.executable, str(SCRIPT), '--repo', str(self.root),
            '--packet', str(self.root / 'packet.json'), '--render-dir', 'paper/fragments',
            '--manuscript', 'paper/main.tex'], text=True, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)['integrity'], 'pass')
        self.assertTrue((self.root / 'paper/fragments/hyphen-workflow.tex').exists())

    def test_manuscript_must_include_exact_current_fragment(self):
        row = self.packet['workflows'][0]
        self.write('paper/fragments/hyphen-workflow.tex', gate.render(row))
        self.write('paper/main.tex', '% \\input{fragments/hyphen-workflow}\nNo inclusion.\n')
        with self.assertRaisesRegex(ValueError, 'missing manuscript inclusion'):
            gate.verify_inclusion(self.packet, self.root, 'paper/main.tex', 'paper/fragments')
        self.write('paper/main.tex', '\\input{appendix}\n')
        self.write('paper/appendix.tex', '\\input{fragments/hyphen-workflow}\n')
        self.assertIn('all exact', gate.verify_inclusion(self.packet, self.root, 'paper/main.tex', 'paper/fragments'))
        self.write('paper/fragments/hyphen-workflow.tex', 'stale')
        with self.assertRaisesRegex(ValueError, 'stale rendered fragment'):
            gate.verify_inclusion(self.packet, self.root, 'paper/main.tex', 'paper/fragments')


if __name__ == '__main__':
    unittest.main()
