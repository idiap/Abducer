# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Regression tests for portable source snapshots and honest Lunar projections.

The fixture is a small committed repository, not a mock of the archive format.
Every successful export is reopened by the real pinned payload validator.
"""
from pathlib import Path
import json
import hashlib
import subprocess
import tempfile
import unittest
import zipfile

from integrations.domain_package.export import export_package, runtime_path
from integrations.domain_package.exporter import ArchiveBuilder, ExportError
from integrations.domain_package.format.contract import validate_payloads
from integrations.domain_package.viewer import graph_sources, selected_viewer_paths


class DomainExportTests(unittest.TestCase):
    """Exercise evidence boundaries, complete bytes and atomic failure modes."""

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name).resolve()
        self.root = self.base / 'repo'
        self.root.mkdir()
        files = {
            'README.md': '# Research\n', 'pyproject.toml': '[project]\nname = "fixture"\n',
            'uv.lock': '# Historical source lock\n',
            'skills/reasoning/example/SKILL.md': '---\nname: example\ndescription: Exact description\n---\n# Example\nKeep uncertainty.\n',
            'skills/reasoning/example/references/guide.md': '# Supporting instructions\n',
            'skills/other/example/SKILL.md': '---\nname: example\n---\n# Separate skill\n',
            'KB/test.kb.md': '# Research state\n',
            'InformalMathLib/test/result.md': 'Unproved claim.\n',
            'agentic/reports/demo/latest.md': '# Test report\nSee [figure](figure.svg).\n',
            'agentic/reports/demo/figure.svg': '<svg xmlns="http://www.w3.org/2000/svg"/>',
            'agentic/reports/demo/latest.pdf': '%PDF-1.4\nfixture bytes',
            'abducer-prism/workflows/demo/reasoning.prism': '# Documentation only\n',
            'abducer-prism/workflows/demo/types.prism': '# Types\n',
            'abducer-prism/workflows/demo/occurrences.prism': '# Occurrences\n',
            'abducer-prism/workflows/demo/relations.prism': '# Relations\n',
            'abducer-prism/workflows/demo/sample_outputs.prism': '# Authored samples\n',
            'config/api_keys.json': '{"example": "must never be exported"}',
        }
        for path, text in files.items():
            target = self.root / path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(text)
        manifest = {'evidence_level': 'typed smoke only', 'workflows': [{
            'id': 'demo', 'module_id': 'demo', 'function': 'Reason about a claim',
            'materialization': {'status': 'blocked_unresolved_projection_gap'},
            'skill_bindings': [{'path': 'skills/reasoning/example'}],
        }]}
        (self.root / 'abducer-prism/workflows/manifest.json').write_text(json.dumps(manifest))
        self.viewer_assets()
        self.git('init', '-q')
        self.git('add', '.')
        self.git('-c', 'user.name=Export Fixture', '-c', 'user.email=fixture@example.invalid', 'commit', '-qm', 'fixture')

    def git(self, *args):
        subprocess.run(['git', '-C', str(self.root), *args], check=True, capture_output=True)

    def viewer_assets(self):
        """Create an explicit small graph fixture without a compiler dependency."""
        directory = self.root / 'abducer-prism/workflows/demo'
        source = 'abducer-prism/workflows/demo/reasoning.prism'
        graph = {'reasoning': 'Demo', 'topology': 'sequence', 'input': [{'name': 'claim', 'type': 'Claim'}],
                 'output': 'Claim', 'nodes': [{'id': 'claim', 'kind': 'input', 'output_type': 'Claim'},
                                            {'id': '__result__', 'kind': 'result', 'output_type': 'Claim'}],
                 'edges': [{'source': 'claim', 'target': '__result__', 'kind': 'return'}]}
        bundle = {'kind': 'prism-viewer-bundle', 'schema_version': 1, 'projects': [{
            'id': 'abducer-prism', 'label': 'Abducer', 'workflows': [{
                'id': 'demo', 'label': 'Demo', 'summary': 'Reason about a claim', 'source': source,
                'source_text': (self.root / source).read_text(), 'graph': graph,
                'sources': [{'path': p.name, 'content': p.read_text(), 'file_type': p.stem}
                            for p in sorted(directory.glob('*.prism'))],
            }]}]}
        assets = self.root / 'integrations/domain_package/assets'
        assets.mkdir(parents=True, exist_ok=True)
        raw = json.dumps(bundle).encode()
        (assets / 'bundle.json').write_bytes(raw)
        manifest = json.loads((self.root / 'abducer-prism/workflows/manifest.json').read_text())
        provenance = {'bundle_sha256': hashlib.sha256(raw).hexdigest(),
                      'source_sha256': {p: hashlib.sha256((self.root / p).read_bytes()).hexdigest()
                                        for p in graph_sources(self.root, manifest)}}
        (assets / 'viewer-provenance.json').write_text(json.dumps(provenance))

    def export(self, name='package.zip'):
        destination = self.base / name
        manifest = export_package(destination, repository_root=self.root, enable_demo=False)
        with zipfile.ZipFile(destination) as archive:
            payloads = {p['path']: archive.read(p['path']) for p in manifest['files']}
            documents = validate_payloads(manifest, payloads)
            self.assertEqual(set(archive.namelist()), {'manifest.json', *[k + '/' for k in manifest['collections']], *payloads})
        return destination, manifest, documents, payloads

    def test_complete_snapshot_and_honest_collections(self):
        _, manifest, documents, payloads = self.export()
        self.assertEqual(manifest['runtime']['workflows'], [])
        self.assertEqual(manifest['runtime']['entrypoints'], [])
        self.assertEqual(len(documents['skills']), 2)
        self.assertEqual(len({s['id'] for s in documents['skills']}), 2)
        for skill in documents['skills']:
            path = skill['metadata']['source_directory'] + '/SKILL.md'
            self.assertEqual(skill['instructions'], (self.root / path).read_text())
        self.assertNotIn(runtime_path('config/api_keys.json'), payloads)
        report = documents['reports'][0]
        self.assertEqual(report['runs'], [])
        self.assertEqual(report['revisions'], [])
        self.assertEqual(report['provenance'], [])
        original = report['metadata']['original_text_file']
        self.assertEqual(payloads[original], (self.root / 'agentic/reports/demo/latest.md').read_bytes())
        figure = next(a for a in report['attachments'] if a['link'] == 'figure.svg')
        self.assertEqual(payloads[figure['file']], (self.root / 'agentic/reports/demo/figure.svg').read_bytes())
        self.assertEqual(len(documents['data-sources'][0]['local_files']), 2)
        workflow = next(r for r in documents['repository'] if r['kind'] == 'workflow')
        self.assertEqual(workflow['metadata']['source_materialization_status'], 'blocked_unresolved_projection_gap')
        bundle, catalog = selected_viewer_paths(manifest, documents)
        self.assertEqual(json.loads(payloads[bundle])['projects'][0]['workflows'][0]['id'], 'demo')
        self.assertEqual(json.loads(payloads[catalog])['modules'][0]['id'], 'demo')

    def test_repeated_archives_are_identical_and_existing_output_is_preserved(self):
        first, *_ = self.export('first.zip')
        second, *_ = self.export('second.zip')
        self.assertEqual(first.read_bytes(), second.read_bytes())
        with self.assertRaises(ExportError):
            export_package(first, repository_root=self.root)
        self.assertEqual(first.read_bytes(), second.read_bytes())

    def test_missing_selected_source_fails_without_publication(self):
        (self.root / 'KB/test.kb.md').unlink()
        with self.assertRaises(ExportError):
            self.export()
        self.assertFalse((self.base / 'package.zip').exists())

    def test_source_symlink_is_rejected(self):
        path = self.root / 'KB/test.kb.md'
        path.unlink()
        path.symlink_to(self.root / 'README.md')
        with self.assertRaises(ExportError):
            self.export()

    def test_source_change_blocks_atomic_publication(self):
        builder = ArchiveBuilder(self.base / 'snapshot', package_key='test', display_name='Test')
        source = self.root / 'README.md'
        builder.add_file('repository/readme.md', source, source_root=self.root)
        source.write_text('changed after snapshot')
        with self.assertRaises(ExportError):
            builder.publish(self.base / 'changed.zip')
        self.assertFalse((self.base / 'changed.zip').exists())

    def test_nonconforming_source_header_keeps_exact_instructions(self):
        source = self.root / 'skills/reasoning/example/SKILL.md'
        instructions = '---\nname: example\ndescription: Explain the route: preserve limits.\n---\n# Body\n'
        source.write_text(instructions)
        self.viewer_assets()
        _, _, documents, _ = self.export()
        skill = next(s for s in documents['skills'] if s['metadata']['source_directory'] == 'skills/reasoning/example')
        self.assertEqual(skill['instructions'], instructions)
        self.assertEqual(skill['metadata']['descriptor']['description'], 'Explain the route: preserve limits.')
        self.assertEqual(skill['metadata']['front_matter_status'], 'literal_fields_from_nonconforming_yaml')

    def test_historical_absolute_links_bind_only_to_known_inventory(self):
        report = self.root / 'agentic/reports/demo/latest.md'
        old = '/old/author/repository/agentic/reports/demo/figure.svg:12'
        unavailable = '/old/author/private-data.csv'
        report.write_text(f'# Portable report\n[Plot]({old}) [Absent]({unavailable})\n')
        _, _, documents, payloads = self.export()
        row = documents['reports'][0]
        attachment = next(a for a in row['attachments'] if a['link'] == old)
        self.assertEqual(payloads[attachment['file']], (self.root / 'agentic/reports/demo/figure.svg').read_bytes())
        self.assertEqual(row['metadata']['unresolved_historical_links'], [unavailable])

    def test_skill_line_endings_remain_exact(self):
        source = self.root / 'skills/reasoning/example/SKILL.md'
        raw = source.read_bytes().replace(b'\n', b'\r\n')
        source.write_bytes(raw)
        self.viewer_assets()
        _, _, documents, _ = self.export()
        skill = next(s for s in documents['skills'] if s['metadata']['source_directory'] == 'skills/reasoning/example')
        self.assertEqual(skill['instructions'].encode(), raw)

    def test_missing_bundle_metadata_reproduces_lunar_empty_page(self):
        _, manifest, documents, _ = self.export()
        runtime = next(d for d in documents['repository'] if d['id'] == 'abducer-runtime')
        del runtime['metadata']['bundle']
        with self.assertRaisesRegex(ExportError, 'one linked viewer bundle'):
            selected_viewer_paths(manifest, documents)

    def test_unlinked_viewer_asset_is_rejected(self):
        _, manifest, documents, _ = self.export()
        runtime = next(d for d in documents['repository'] if d['id'] == 'abducer-runtime')
        row = next(r for r in manifest['collections']['repository'] if r['id'] == 'abducer-runtime')
        row['files'].remove(runtime['metadata']['bundle'])
        with self.assertRaisesRegex(ExportError, 'not linked'):
            selected_viewer_paths(manifest, documents)

    def test_stale_graph_source_prevents_export(self):
        (self.root / 'abducer-prism/workflows/demo/reasoning.prism').write_text('# Changed reasoning\n')
        with self.assertRaisesRegex(ExportError, 'stale viewer asset'):
            self.export()


if __name__ == '__main__':
    unittest.main()
