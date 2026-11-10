# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Regenerate source-bound viewer assets with the existing Prism graph exporter.

Only regeneration needs the explicit prism-viewer checkout and Prism CLI. Normal
ZIP export uses these committed assets and verifies their dependency hashes. All
parse/check/compile commands run against an isolated copy, never a research run.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import shutil
import sys
import tempfile

from .exporter import ExportError, json_bytes
from .viewer import ASSET_ROOT, WORKFLOW_MANIFEST, graph_sources, validate_viewer


def build_viewer(root: Path, viewer_root: Path, prism: Path) -> dict:
    """Compile every current workflow and retain exact sources and examples."""
    root, viewer_root, prism = (p.resolve(strict=True) for p in (root, viewer_root, prism))
    sys.path.insert(0, str(viewer_root / 'src'))
    from prism_viewer.examples import extract_sample_examples, _snippet
    from prism_viewer.graph import build_reasoning_graph
    from prism_viewer.materialization import extract_materialization_skills
    from prism_viewer.prism_client import inspect_reasoning

    manifest = json.loads((root / WORKFLOW_MANIFEST).read_text())
    source_paths = graph_sources(root, manifest)
    hashes = {p: hashlib.sha256((root / p).read_bytes()).hexdigest() for p in source_paths}
    workflows = []
    with tempfile.TemporaryDirectory(prefix='abducer-viewer-build-') as temporary:
        snapshot = Path(temporary).resolve()
        for path in source_paths:
            destination = snapshot / path
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(root / path, destination)
        project_root = snapshot / 'abducer-prism'

        def inspect(source: Path):
            return inspect_reasoning(source, project_root=project_root, prism_executable=str(prism), timeout=120)

        for row in sorted(manifest['workflows'], key=lambda r: r['id']):
            directory = project_root / 'workflows' / row['module_id']
            source_label = f'abducer-prism/workflows/{row["module_id"]}/reasoning.prism'
            inspection = inspect(directory / 'reasoning.prism')
            initial = build_reasoning_graph(inspection.parsed, inspection.compiled, source=source_label)
            aliases = [n.id for n in initial.nodes if n.kind == 'occurrence']
            samples = inspect(directory / 'sample_outputs.prism')
            examples = extract_sample_examples(samples.parsed, input_names=[i['name'] for i in initial.inputs], occurrence_aliases=aliases)
            # Some documentary outputs are pure type-witness builders. Preserve
            # their authored code verbatim; never execute or invent a value.
            declarations = {d.get('name'): d for d in samples.parsed['declarations']}
            for alias in aliases:
                name = f'sample_{alias}_value_builder'
                if alias not in examples and name in declarations:
                    examples[alias] = _snippet(samples.parsed['source'], declarations[name]['span'], name)
            if set(aliases) - set(examples):
                raise ExportError(f'missing authored occurrence examples: {row["id"]}')
            skills = None
            if (directory / 'materialization.prism').is_file():
                material = inspect(directory / 'materialization.prism')
                skills = extract_materialization_skills(material.compiled, reasoning=initial.reasoning, occurrence_aliases=aliases)
            graph = build_reasoning_graph(inspection.parsed, inspection.compiled, source=source_label,
                                          skills_by_occurrence=skills, examples_by_node=examples).to_dict()
            sources = []
            order = {'reasoning': 0, 'types': 1, 'occurrences': 2, 'relations': 3, 'materialization': 4, 'sample_outputs': 5, 'main': 6}
            for path in sorted(directory.rglob('*.prism'), key=lambda p: (order.get(p.stem, 7), p.as_posix())):
                sources.append({'path': path.relative_to(directory).as_posix(), 'file_type': path.stem,
                                'content': path.read_text()})
            workflows.append({'id': row['id'], 'label': row['id'].replace('_', ' ').replace('-', ' ').title(),
                              'source': source_label, 'source_text': (directory / 'reasoning.prism').read_text(),
                              'summary': row['function'], 'graph': graph, 'sources': sources,
                              'skill_metadata': 'checked-materialization' if skills else 'unavailable'})
            print(f'Checked viewer: {row["id"]} ({len(aliases)} occurrences)', file=sys.stderr, flush=True)
    for path, digest in hashes.items():
        if hashlib.sha256((root / path).read_bytes()).hexdigest() != digest:
            raise ExportError(f'source changed during viewer build: {path}')
    bundle = {'kind': 'prism-viewer-bundle', 'schema_version': 1,
              'projects': [{'id': 'abducer-prism', 'label': 'Abducer', 'workflows': workflows}]}
    bundle_raw = json_bytes(bundle)
    provenance = {'generator': 'prism_viewer public parse/check/compile graph projection',
                  'bundle_sha256': hashlib.sha256(bundle_raw).hexdigest(), 'source_sha256': hashes,
                  'viewer_tool_sha256': {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                                        for p in sorted((viewer_root / 'src/prism_viewer').glob('*.py'))},
                  'workflow_count': len(workflows), 'execution_claim': False}
    assets = root / ASSET_ROOT
    assets.mkdir(parents=True, exist_ok=True)
    (assets / 'bundle.json').write_bytes(bundle_raw)
    (assets / 'viewer-provenance.json').write_bytes(json_bytes(provenance))
    validate_viewer(root)
    return {'workflows': len(workflows), 'bundle_bytes': len(bundle_raw), 'bundle_sha256': provenance['bundle_sha256']}


def main() -> None:
    """Refresh assets using explicit generation dependencies."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repository-root', type=Path, default=Path.cwd())
    parser.add_argument('--viewer-root', type=Path, required=True)
    parser.add_argument('--prism', type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(build_viewer(args.repository_root, args.viewer_root, args.prism), indent=2))


if __name__ == '__main__':
    main()
