# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Validate cached Prism viewer assets against the exact exported source tree.

Lunar's Prism page follows the runtime resource's `metadata.bundle` file link.
Workflow resources alone do not populate that page. The cached graph is produced
by the public Prism toolchain; export rejects missing, incomplete or stale assets.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path, PurePosixPath
from typing import Any

from .exporter import ExportError


ASSET_ROOT = 'integrations/domain_package/assets'
BUNDLE_SOURCE = ASSET_ROOT + '/bundle.json'
PROVENANCE_SOURCE = ASSET_ROOT + '/viewer-provenance.json'
WORKFLOW_MANIFEST = 'abducer-prism/workflows/manifest.json'


def viewer_catalog(bundle: dict[str, Any]) -> dict[str, Any]:
    """Populate Lunar's Repository module links from the same viewer workflows."""
    modules = []
    for project in bundle['projects']:
        for workflow in project['workflows']:
            graph = workflow['graph']
            skills = {s['name'] for n in graph['nodes'] for s in n.get('skills', [])}
            modules.append({'id': workflow['id'], 'name': workflow['label'],
                            'description': workflow['summary'], 'primary_file': 'reasoning.prism',
                            'source': workflow['source'], 'file_count': len(workflow['sources']),
                            'skill_count': len(skills), 'node_count': len(graph['nodes']),
                            'edge_count': len(graph['edges'])})
    return {'schema_version': 1, 'visibility': 'package', 'modules': modules, 'skills': []}


def selected_viewer_paths(manifest: dict[str, Any], documents: dict[str, Any]) -> tuple[str, str]:
    """Mirror Lunar's asset lookup, including resource ownership of each link."""
    resources = {r['id']: r for r in manifest['collections']['repository']}
    selected = []
    for kind in ('bundle', 'catalog'):
        owners = [d for d in documents['repository'] if d['metadata'].get(kind) is not None]
        if len(owners) != 1:
            raise ExportError(f'Lunar requires one linked viewer {kind}; found {len(owners)}')
        owner = owners[0]
        path = owner['metadata'][kind]
        if path not in resources[owner['id']]['files']:
            raise ExportError(f'Lunar viewer {kind} is not linked to its repository resource')
        selected.append(path)
    return selected[0], selected[1]


def graph_sources(root: Path, manifest: dict[str, Any]) -> list[str]:
    """Bind all typed workflow modules and linked source skill instructions."""
    paths = {WORKFLOW_MANIFEST}
    for row in manifest['workflows']:
        directory = root / 'abducer-prism/workflows' / row['module_id']
        paths.update(p.relative_to(root).as_posix() for p in directory.rglob('*.prism'))
        for ref in row.get('skill_bindings', []):
            paths.add(ref.get('skill_file') or ref['path'] + '/SKILL.md')
    return sorted(paths)


def validate_viewer(root: Path) -> dict[str, Any]:
    """Enforce the viewer route, graph coverage and source freshness contract."""
    try:
        bundle_raw = (root / BUNDLE_SOURCE).read_bytes()
        bundle = json.loads(bundle_raw)
        provenance = json.loads((root / PROVENANCE_SOURCE).read_text())
        manifest = json.loads((root / WORKFLOW_MANIFEST).read_text())
    except (OSError, ValueError) as exc:
        raise ExportError('missing or invalid viewer assets; run build_viewer first') from exc
    if provenance.get('bundle_sha256') != hashlib.sha256(bundle_raw).hexdigest():
        raise ExportError('viewer bundle digest differs from its build provenance')
    if bundle.get('kind') != 'prism-viewer-bundle' or bundle.get('schema_version') != 1:
        raise ExportError('unsupported viewer bundle format')
    if len(bundle.get('projects', [])) != 1:
        raise ExportError('Abducer viewer must declare exactly one project')
    project = bundle['projects'][0]
    if project.get('id') != 'abducer-prism':
        raise ExportError('incorrect Abducer viewer project identity')
    workflows = project.get('workflows', [])
    expected = {r['id']: r for r in manifest['workflows']}
    if len(workflows) != len(expected) or {w['id'] for w in workflows} != set(expected):
        raise ExportError('viewer does not cover every authored workflow exactly once')
    source_paths = graph_sources(root, manifest)
    if set(provenance.get('source_sha256', {})) != set(source_paths):
        raise ExportError('viewer source dependency inventory is stale')
    for path in source_paths:
        try:
            digest = hashlib.sha256((root / path).read_bytes()).hexdigest()
        except OSError as exc:
            raise ExportError(f'missing viewer source: {path}') from exc
        if provenance['source_sha256'][path] != digest:
            raise ExportError(f'stale viewer asset for {path}; run build_viewer again')
    for workflow in workflows:
        row = expected[workflow['id']]
        source = 'abducer-prism/workflows/' + row['module_id'] + '/reasoning.prism'
        if workflow.get('source') != source or workflow.get('source_text') != (root / source).read_text():
            raise ExportError('viewer reasoning source differs from authored module')
        graph = workflow.get('graph', {})
        nodes, edges = graph.get('nodes', []), graph.get('edges', [])
        identifiers = {n.get('id') for n in nodes}
        if not nodes or len(identifiers) != len(nodes) or None in identifiers:
            raise ExportError('viewer graph contains empty or duplicate nodes')
        if any(e['source'] not in identifiers or e['target'] not in identifiers for e in edges):
            raise ExportError('viewer graph contains a dangling edge')
        if not graph.get('reasoning') or not graph.get('output'):
            raise ExportError('viewer graph lacks a typed reasoning boundary')
        files = workflow.get('sources', [])
        if not {'reasoning.prism', 'types.prism', 'occurrences.prism', 'relations.prism', 'sample_outputs.prism'} <= {s['path'] for s in files}:
            raise ExportError('viewer omits a required source-navigation layer')
        for item in files:
            path = PurePosixPath(item['path'])
            if path.is_absolute() or '..' in path.parts:
                raise ExportError('unsafe viewer source-navigation path')
            local = PurePosixPath(source).parent / path
            if local.as_posix() not in source_paths or item['content'] != (root / local).read_text():
                raise ExportError('viewer browser source differs from snapshot')
    return bundle
