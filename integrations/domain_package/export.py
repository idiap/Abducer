# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Build a portable Abducer catalog without inventing execution authority.

The Git inventory defines source membership; payloads come from the current
worktree and are checked for stability before atomic publication. Collection
metadata is derived only from the private snapshot. Existing research runtimes
are preserved as source. An explicit native adapter invokes selected marathons
with their original report pipeline; other graphs remain browse-only.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import subprocess
import tempfile
from typing import Any
from urllib.parse import unquote, urlsplit

import yaml

from .exporter import ArchiveBuilder, ExportError, json_bytes
from .viewer import BUNDLE_SOURCE, PROVENANCE_SOURCE, validate_viewer, viewer_catalog
from .runtime_registration import ENTRY_FILE, WORKFLOW_ID, runtime_declaration
from .marathon_runtime import confined


SOURCE_ROOTS = {
    'AbducerFormal', 'agentic', 'abducer-prism', 'docs', 'external', 'hooks',
    'skills', 'proj_skills', 'prism_me', 'registry', 'config', 'tests',
    'KB', 'InformalMathLib', 'phyp', 'output', 'paper-workflow-representations',
    'integrations', 'artifacts',
}
ROOT_FILES = {
    'README.md', 'AGENTS.md', 'pyproject.toml', 'uv.lock', 'AbducerFormal.lean',
    'lakefile.toml', 'lake-manifest.json', 'lean-toolchain',
    'reasoning-as-typed-epistemic-composition.pdf',
    'reasoning-as-typed-epistemic-composition.tex', 'all-reasoning-flows.md',
}
INTEGRATION_TESTS = {
    'tests/infrastructure/check_lunar_marathon_initialization.py',
    'tests/infrastructure/check_lunar_marathon_reports.py',
    'tests/infrastructure/test_lunar_marathon_parity.py',
    'tests/infrastructure/check_lunar_marathon_worker.py',
    'tests/infrastructure/lunar_html_report_frontend.mjs',
    'tests/infrastructure/test_domain_package_export.py',
    'tests/infrastructure/test_lunar_discovery_hooks.py',
    'tests/infrastructure/check_lunar_discovery_runtime.py',
    'tests/infrastructure/lunar_runtime_frontend.mjs',
    'tests/infrastructure/lunar_viewer_frontend.mjs',
}
INITIALIZATION_SOURCES = {
    'agentic/discovery/' + name + '.py' for name in (
        'bootstrap_adjudication', 'bootstrap_authoring', 'bootstrap_dispatch', 'bootstrap_literature',
        'bootstrap_pipeline', 'bootstrap_production', 'bootstrap_reflection', 'bootstrap_routing', 'model_author')
}
INITIALIZATION_TESTS = {
    'tests/discovery/test_' + name + '.py' for name in (
        'bootstrap_authoring', 'bootstrap_literature', 'bootstrap_pipeline',
        'bootstrap_routing', 'model_author')
}
EXCLUDED_PREFIXES = (
    'agentic/runs/', 'agentic/logs/', 'agentic/traces/',
    'agentic/reports/canonical_discovery_cycle/acceptance/',
    'abducer-prism/build/', 'abducer-prism/vendor/',
)
EXCLUDED_PARTS = {'.git', '.venv', 'venv', '__pycache__', '.pytest_cache', '.DS_Store'}
EXCLUDED_SUFFIXES = {'.zip', '.whl', '.pyc', '.pyo', '.pid', '.aux', '.log', '.tmp'}
REPORT_ROOTS = ('agentic/reports/', 'docs/publications/', 'docs/generated/', 'phyp/', 'output/')
REPORT_SUFFIXES = {'.md', '.html', '.pdf', '.tex'}
MANIFEST_SOURCE = 'abducer-prism/workflows/manifest.json'
LINK = re.compile(r'\]\((?:<([^>]+)>|([^\s)]+))(?:\s+"[^"]*")?\)')


def excluded(path: str) -> bool:
    """Keep host configuration, secrets, transient state and nested exports out."""
    p = PurePosixPath(path)
    return (
        path.startswith(EXCLUDED_PREFIXES)
        or bool(set(p.parts) & EXCLUDED_PARTS)
        or p.suffix.lower() in EXCLUDED_SUFFIXES
        or p.name.startswith('.env') or '.local.' in p.name
        or p.name in {'api_keys.json', 'api_keys.env'} or 'secrets' in p.parts
        or p.suffix.lower() in {'.pem', '.key', '.p12'}
    )


def source_inventory(root: Path) -> tuple[list[str], str]:
    """Select tracked authored files plus this integration and its focused tests.

    Git membership deliberately excludes unrelated untracked files. The exporter
    tree is included before its first commit, so the resulting archive carries
    the command that produced it. Required input bytes may never disappear.
    """
    def git(*args: str) -> str:
        return subprocess.check_output(['git', '-C', str(root), *args]).decode()

    try:
        tracked = set(filter(None, git('ls-files', '-z').split('\0')))
        revision = git('rev-parse', 'HEAD').strip()
    except (subprocess.CalledProcessError, OSError) as exc:
        raise ExportError('repository root must be a Git worktree with a commit') from exc
    for required in ('README.md', 'pyproject.toml', 'uv.lock', MANIFEST_SOURCE):
        if required not in tracked:
            raise ExportError(f'missing required tracked source: {required}')
    paths = {p for p in tracked if p in ROOT_FILES or PurePosixPath(p).parts[0] in SOURCE_ROOTS}
    paths.update(p for p in INTEGRATION_TESTS if (root / p).is_file() or (root / p).is_symlink())
    paths.update(p for p in INITIALIZATION_SOURCES if (root / p).is_file() or (root / p).is_symlink())
    paths.update(p for p in INITIALIZATION_TESTS if (root / p).is_file() or (root / p).is_symlink())
    for p in (root / 'integrations').rglob('*'):
        if p.is_file() or p.is_symlink():
            paths.add(p.relative_to(root).as_posix())
    return sorted(p for p in paths if not excluded(p)), revision


def resource_id(prefix: str, path: str) -> str:
    """Use a readable path and full digest to disambiguate portable logical IDs."""
    slug = re.sub(r'[^a-z0-9]+', '-', path.lower()).strip('-')[:100]
    return prefix + '-' + slug + '-' + hashlib.sha256(path.encode()).hexdigest()


def runtime_path(path: str) -> str:
    """Retain repository-relative layout in the selected version's source tree."""
    return 'repository/runtime/' + path


def read_json(builder: ArchiveBuilder, path: str) -> Any:
    """Read metadata from frozen bytes, never from a second live source read."""
    return json.loads((builder.root / runtime_path(path)).read_text())


def skill_header(instructions: str) -> tuple[dict[str, Any], str]:
    """Preserve permissive authored front matter without rewriting instructions.

    Some source skills use an unquoted colon in a one-line description. Treat
    those as documented text, retain the raw header and explicitly label the
    limited projection. YAML dates are historical metadata strings in JSON.
    """
    match = re.match(r'\A---\s*\n(.*?)\n---\s*\n', instructions, flags=re.S)
    if not match:
        return {}, 'absent'
    raw = match.group(1)
    try:
        header = yaml.safe_load(raw)
        if not isinstance(header, dict):
            raise ValueError('front matter is not a mapping')
        return json.loads(json.dumps(header, default=str)), 'parsed_yaml'
    except (yaml.YAMLError, ValueError):
        header = {}
        for key in ('name', 'description'):
            field = re.search(r'^' + key + r':\s*(.+)$', raw, re.M)
            if field:
                header[key] = field.group(1).strip().strip('\"\'')
        header['raw_front_matter'] = raw
        return header, 'literal_fields_from_nonconforming_yaml'


def add_skills(builder: ArchiveBuilder, paths: list[str]) -> dict[str, str]:
    """Publish full skill trees with distinct identities and exact instructions."""
    roots = ('skills/', 'proj_skills/', 'prism_me/', 'abducer-prism/skills/', 'external/')
    candidates = [p for p in paths if p.endswith('/SKILL.md') and p.startswith(roots)]
    by_path = {}
    for path in candidates:
        directory = str(PurePosixPath(path).parent)
        instructions = (builder.root / runtime_path(path)).read_bytes().decode('utf-8')
        header, header_status = skill_header(instructions)
        name = str(header.get('name') or PurePosixPath(directory).name)
        description = str(header.get('description') or name)
        identity = resource_id('skill', directory)
        by_path[directory] = identity
        files = []
        for source in paths:
            if source.startswith(directory + '/'):
                target = f'skills/{identity}/files/' + source[len(directory) + 1:]
                builder.add_file(target, builder.root / runtime_path(source), source_root=builder.root)
                files.append(target)
        groups = list(PurePosixPath(directory).parts[:-1])
        builder.add_resource('skills', {
            'id': identity, 'name': name, 'instructions': instructions,
            'capabilities': [{'name': name, 'description': description, 'evidence': 'source_instructions'}],
            'invocation': {'mode': 'instruction_only', 'source_directory': runtime_path(directory)},
            'groups': groups,
            'metadata': {'source_directory': directory, 'source_file': runtime_path(path),
                         'descriptor': {'description': description, 'aliases': [name],
                                        'invocation_posture': 'instruction_only'},
                         'front_matter': header, 'front_matter_status': header_status,
                         'execution_claim': False},
        }, files=files)
    return by_path


def add_workflows(builder: ArchiveBuilder, paths: list[str], skills: dict[str, str], *, enable_demo: bool = False) -> None:
    """Keep authored workflow evidence visible without registering live hooks."""
    manifest = read_json(builder, MANIFEST_SOURCE)
    for row in manifest['workflows']:
        prefix = 'abducer-prism/workflows/' + row['module_id'] + '/'
        source_paths = {p for p in paths if p.startswith(prefix)}
        source_paths.add(MANIFEST_SOURCE)
        # Bind the repository resource to the reviewed source/validator closure.
        for ref in [row.get('source_workflow', {}), *row.get('contract_sources', []),
                    *row.get('validator_bindings', [])]:
            if ref.get('path') in paths:
                source_paths.add(ref['path'])
        references = [{'collection': 'skills', 'id': skills[ref['path']]}
                      for ref in row.get('skill_bindings', []) if ref['path'] in skills]
        material = row.get('materialization', {})
        runnable = enable_demo and row['id'] == WORKFLOW_ID
        builder.add_resource('repository', {
            'id': 'workflow-' + row['id'].replace('_', '-'),
            'name': row['id'].replace('_', ' ').replace('-', ' ').title(), 'kind': 'workflow',
            'metadata': {'path': runtime_path(prefix.rstrip('/')), 'description': row['function'],
                         'browse_only': not runnable,
                         'lunar_execution': 'source_yang_mills_marathon' if runnable else 'unsupported',
                         'source_materialization_status': material.get('status', 'not_materialized'),
                         'source_evidence': row, 'claim_ceiling': manifest['evidence_level']},
        }, files=[*[runtime_path(p) for p in sorted(source_paths)], *([ENTRY_FILE] if runnable else [])], references=references)


def add_data_sources(builder: ArchiveBuilder, paths: list[str]) -> None:
    """Expose each authored KB and its problem-scoped mathematical memory."""
    for path in paths:
        if not path.startswith('KB/') or not path.endswith('.kb.md'):
            continue
        key = PurePosixPath(path).name.removesuffix('.kb.md')
        local = [path, *[p for p in paths if p.startswith(f'InformalMathLib/{key}/')]]
        files = []
        for source in local:
            target = 'data-sources/local/' + source
            builder.add_file(target, builder.root / runtime_path(source), source_root=builder.root)
            files.append(target)
        builder.add_resource('data-sources', {
            'id': 'kb-' + key, 'name': key.replace('-', ' ').title(),
            'descriptor': {'category': 'mathematical-knowledge-base', 'scope': 'package',
                           'posture': 'descriptor_only', 'source_path': path,
                           'claim_ceiling': 'authored research state; no new mathematical verification'},
            'local_files': [{'id': resource_id('file', p), 'file': f} for p, f in zip(local, files)],
            'remote_references': [],
        }, files=files)


def report_groups(paths: list[str]) -> dict[str, list[str]]:
    """Group authored text and rendered companions into one saved document."""
    groups: dict[str, list[str]] = {}
    for path in paths:
        p = PurePosixPath(path)
        if (path.startswith(REPORT_ROOTS) or p.name.startswith('reasoning-as-typed-epistemic-composition.')):
            if p.suffix in REPORT_SUFFIXES and p.name.lower() not in {'readme.md', 'index.md'}:
                groups.setdefault(str(p.with_suffix('')), []).append(path)
    return groups


def local_link(source: str, link: str, available: set[str]) -> str | None:
    """Resolve a Markdown attachment only to selected repository bytes.

    Historical absolute author paths may name the same repository member. Match
    only a unique multi-segment suffix in the selected inventory, never read the
    old host path. Preserve the original link text in the attachment mapping.
    """
    uri = urlsplit(link)
    if uri.scheme or uri.netloc or not uri.path:
        return None
    path = unquote(uri.path)
    if path.startswith('/'):
        path = re.sub(r':\d+(?::\d+)?$', '', path)
        matches = [p for p in available if '/' in p and path.endswith('/' + p)]
        return matches[0] if len(matches) == 1 else None
    for candidate in [str(PurePosixPath(source).parent / path), path]:
        parts: list[str] = []
        for part in PurePosixPath(candidate).parts:
            if part == '..':
                if not parts:
                    break
                parts.pop()
            else:
                parts.append(part)
        else:
            normalized = '/'.join(parts)
            if normalized in available:
                return normalized
    return None


def add_reports(builder: ArchiveBuilder, paths: list[str]) -> None:
    """Save report text and byte-exact companions without fabricating run facts."""
    available = set(paths)
    for stem, sources in sorted(report_groups(paths).items()):
        identity = resource_id('report', stem)
        markdown = next((p for p in sources if p.endswith('.md')), None)
        primary = markdown or sources[0]
        content = (builder.root / runtime_path(markdown)).read_text() if markdown else ''
        # A 40 MiB HTML viewer is an attachment, not a 40 MiB database document.
        # Same-stem JSON is the source report's structured companion, if present.
        companions = set(sources)
        if stem + '.json' in available:
            companions.add(stem + '.json')
        links: dict[str, str] = {}
        unresolved = []
        for match in LINK.finditer(content):
            link = match.group(1) or match.group(2)
            target = local_link(primary, link, available)
            if target:
                companions.add(target)
                links[link] = target
            elif not urlsplit(link).scheme and not link.startswith('#'):
                unresolved.append(link)
        files = []
        targets = {}
        for source in sorted(companions):
            target = 'reports/files/' + source
            builder.add_file(target, builder.root / runtime_path(source), source_root=builder.root)
            files.append(target)
            targets[source] = target
        if not markdown:
            content = ('# ' + PurePosixPath(stem).name.replace('_', ' ').replace('-', ' ').title()
                       + '\n\nRepository-authored document. Original files are attached; '
                       'this index does not assert a new execution or verification.\n')
        # Every companion has a visible link, including the unchanged original
        # Markdown. Lunar remaps attachment links after import using this table.
        content += '\n\n## Exported source files\n\n'
        for source in sorted(companions):
            link = targets[source]
            links[link] = source
            content += f'- [{PurePosixPath(source).name}](<{link}>)\n'
        title = re.search(r'^#\s+(.+)$', content, re.M)
        builder.add_resource('reports', {
            'id': identity, 'name': (title.group(1).strip() if title else stem) + f' [{stem}]',
            'content': content, 'version': 1, 'revisions': [],
            'attachments': [{'link': link, 'file': targets[source]} for link, source in sorted(links.items())],
            'sections': [], 'runs': [], 'outputs': [], 'provenance': [], 'template_snapshot': None,
            'metadata': {'source_kind': 'repository_authored_document', 'source_path': primary,
                         'source_sha256': builder.files[runtime_path(primary)]['sha256'],
                         'original_text_file': targets.get(markdown), 'version_basis': 'first_exported_snapshot',
                         'history': 'no database revision or run history supplied',
                         'unresolved_historical_links': sorted(set(unresolved)),
                         'claim_ceiling': 'historical source assertions only; not a Lunar execution receipt'},
        }, files=files)


def selected_state_files(root: Path, directories: list[Path]) -> set[str]:
    """Inventory exact selected state trees, retaining secret/cache exclusions."""
    paths = set()
    for directory in directories:
        if not directory.is_dir():
            continue
        for file in directory.rglob('*'):
            relative = file.relative_to(root).as_posix()
            if file.is_symlink():
                raise ExportError('marathon state contains a symlink: ' + relative)
            if file.is_file() and not excluded('selected-state/' + file.relative_to(directory).as_posix()):
                paths.add(relative)
    return paths


def marathon_catalog(root: Path, run_id: str | None, cycle_path: str | None,
                     state_root: str, bindings: dict | None = None) -> tuple[dict, list[Path], set[str]]:
    """Select existing runs without fabricating canonical authority for history."""
    if cycle_path and not run_id:
        raise ExportError('--canonical-theory-cycle requires one explicit --marathon-run-id')
    if bindings is not None and (not isinstance(bindings, dict) or cycle_path):
        raise ExportError('Use a run binding map or --canonical-theory-cycle, not both')
    base = root / 'agentic/runs/discovery_marathons'
    states = [confined(root, f'agentic/runs/discovery_marathons/{run_id}/run_state.json')] if run_id else sorted(base.glob('*/run_state.json'))
    if not states:
        raise ExportError('No marathon runs are available; initialize source run state before exporting')
    runs, directories, additions = [], [], set()
    for path in states:
        path = confined(root, path.relative_to(root).as_posix())
        state = json.loads(path.read_text())
        identity, target = state.get('run_id'), state.get('target_id')
        if not all(isinstance(value, str) and re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9._-]*', value)
                   for value in (identity, target)) or identity != path.parent.name:
            raise ExportError('Invalid target/run identity in ' + str(path))
        if type(state.get('cycle_count')) is not int or state['cycle_count'] < 0:
            raise ExportError('Invalid cycle count in ' + str(path))
        directories.extend([path.parent, confined(root, f'agentic/state/discovery_transactions/targets/{target}/runs/{identity}')])
        configured = (bindings or {}).get(identity, {})
        if not isinstance(configured, dict) or set(configured) - {'canonical_theory_cycle', 'canonical_theory_state_root'}:
            raise ExportError('Run bindings may contain only canonical cycle and state-root paths')
        if any(not isinstance(value, str) or not value for value in configured.values()):
            raise ExportError('Configured canonical paths must be nonempty strings')
        selected_cycle = configured.get('canonical_theory_cycle', cycle_path)
        selected_root = configured.get('canonical_theory_state_root', state_root)
        confined(root, selected_root)
        binding = {'target_id': target, 'run_id': identity, 'cycle_count': state['cycle_count'],
                   'canonical_theory_cycle': selected_cycle, 'canonical_theory_state_root': selected_root,
                   'readiness': {'status': 'blocked', 'reason': 'This run needs a current committed canonical theory cycle before research can start.'}}
        if selected_cycle:
            cycle = json.loads(confined(root, selected_cycle).read_text())
            if (cycle.get('target_id'), cycle.get('run_id')) != (target, identity):
                raise ExportError('canonical cycle does not belong to the selected target/run')
            directory = confined(root, selected_root)
            if not directory.is_dir():
                raise ExportError('canonical theory transaction root is missing')
            directories.append(directory)
            additions.add(selected_cycle)
            binding['readiness'] = {'status': 'requires_validation',
                'reason': 'Canonical state is packaged. The source runner will verify its current authority before using the model.'}
        runs.append(binding)
    if set(bindings or {}) - {run['run_id'] for run in runs}:
        raise ExportError('Binding map references a run outside the selected catalog')
    # New runs have no inherited research state. Their exact run ID is assigned
    # by the host request; initialization must produce canonical authority.
    for target in ('p-vs-np-target', 'yang-mills-existence-and-mass-gap-target'):
        runs.append({'target_id': target, 'run_id': 'new', 'cycle_count': 0, 'initialize': True,
            'canonical_theory_cycle': None, 'canonical_theory_state_root': None,
            'readiness': {'status': 'initialization_available',
                'reason': 'Start a new run: acquire current literature, initialize theory, and execute one research cycle.'}})
    return {'version': 2, 'runs': runs}, directories, additions


def export_package(destination: Path, *, repository_root: Path, enable_demo: bool = True,
                   marathon_run_id: str | None = None, canonical_theory_cycle: str | None = None,
                   canonical_theory_state_root: str = 'agentic/state/canonical_discovery_transactions',
                   marathon_bindings: dict | None = None) -> dict[str, Any]:
    """Publish a complete validated Abducer catalog and source snapshot."""
    root = repository_root.resolve(strict=True)
    if destination.exists() or destination.is_symlink():
        raise ExportError(f'export destination already exists: {destination}')
    paths, revision = source_inventory(root)
    initial_inventory = (list(paths), revision)
    binding = None
    if enable_demo:
        # The catalog owns selection. Other run/log trees remain excluded.
        binding, state_directories, additions = marathon_catalog(
            root, marathon_run_id, canonical_theory_cycle, canonical_theory_state_root, marathon_bindings)
        state_inventory = selected_state_files(root, state_directories)
        additions.update(state_inventory)
        paths = sorted(set(paths) | additions)
    with tempfile.TemporaryDirectory(prefix='abducer-domain-export-') as directory:
        builder = ArchiveBuilder(Path(directory) / 'snapshot', package_key='abducer', display_name='Abducer')
        for path in paths:
            builder.add_file(runtime_path(path), root / path, source_root=root)
        viewer = validate_viewer(builder.root / 'repository/runtime')
        runtime_files = []
        if enable_demo:
            if not any(w['id'] == WORKFLOW_ID for w in viewer['projects'][0]['workflows']):
                raise ExportError('Discovery Marathon is required for the native runtime')
            wrapper = builder.root / runtime_path('integrations/domain_package/discovery.prism')
            builder.add_file(ENTRY_FILE, wrapper, source_root=builder.root)
            runtime_files.append(ENTRY_FILE)
            # Derive UI metadata from the same frozen run-state bytes as execution.
            for run in binding['runs']:
                if run.get('initialize') is True:
                    continue
                frozen = read_json(builder, f"agentic/runs/discovery_marathons/{run['run_id']}/run_state.json")
                if any(frozen.get(key) != run[key] for key in ('target_id', 'run_id', 'cycle_count')):
                    raise ExportError('marathon state changed during export')
            builder.manifest['runtime'].update(runtime_declaration(binding['runs']))
            runtime_files.append(builder.add_bytes('repository/marathon-binding.json', json_bytes(binding)))
        catalog_path = builder.add_bytes('repository/viewer-catalog.json', json_bytes(viewer_catalog(viewer)))
        skills = add_skills(builder, paths)
        add_workflows(builder, paths, skills, enable_demo=enable_demo)
        add_data_sources(builder, paths)
        if enable_demo:
            from agentic.discovery.bootstrap_literature import RESOURCE_ID, public_query_routes
            builder.add_resource('data-sources', {
                'id': RESOURCE_ID, 'name': 'Current discovery literature',
                'descriptor': {'category': 'scholarly-metadata', 'scope': 'public',
                    'public_queries': public_query_routes(),
                    'claim_ceiling': 'Bounded source abstracts and metadata; no source truth certification'},
                'local_files': [], 'remote_references': [],
            }, files=[])
        add_reports(builder, paths)
        index = {'source_revision': revision, 'snapshot_basis': 'selected current worktree bytes',
                 'source_files': [{'path': p, 'sha256': builder.files[runtime_path(p)]['sha256']} for p in paths],
                 'excluded_prefixes': list(EXCLUDED_PREFIXES),
                 'exclusions': 'untracked files except integration code and named integration tests, dot controls, secrets, caches, environments, nested archives',
                 'lunar_execution': 'source_discovery_marathon' if enable_demo else 'browse_only',
                 'marathon_binding': binding if enable_demo else None,
                 'workflow_count': len(builder.manifest['collections']['repository'])}
        index_path = builder.add_bytes('repository/export-index.json', json_bytes(index))
        builder.add_resource('repository', {
            'id': 'abducer-runtime', 'name': 'Abducer source and research policies', 'kind': 'runtime',
            'metadata': {'python_root': 'repository/runtime', 'source_revision': revision,
                         'bundle': runtime_path(BUNDLE_SOURCE),
                         'catalog': catalog_path,
                         'viewer_provenance': runtime_path(PROVENANCE_SOURCE),
                         'export_index': index_path, 'browse_only': not enable_demo,
                         'environment_lock': 'repository/runtime/uv.lock',
                         'workflow_manifest': runtime_path(MANIFEST_SOURCE)},
        }, files=[index_path, catalog_path, *runtime_files, *[runtime_path(p) for p in paths]], references=[
            {'collection': kind, 'id': row['id']} for kind in ('skills', 'data-sources', 'reports')
            for row in builder.manifest['collections'][kind]
        ])
        # Recheck inventory as well as individual file stamps: a concurrent Git
        # addition/deletion must not publish a silently incomplete source set.
        if source_inventory(root) != initial_inventory:
            raise ExportError('source inventory changed during export')
        if enable_demo and selected_state_files(root, state_directories) != state_inventory:
            raise ExportError('selected marathon state inventory changed during export')
        return builder.publish(destination)


def main() -> None:
    """Provide an explicit-root CLI suitable for repeatable local exports."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repository-root', type=Path, default=Path.cwd())
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--browse-only', action='store_true', help='Omit native marathon registration')
    parser.add_argument('--marathon-run-id', help='Include only this run; default includes all locally initialized marathons')
    parser.add_argument('--canonical-theory-cycle', help='Exact repository-relative committed projection for this run')
    parser.add_argument('--canonical-theory-state-root', default='agentic/state/canonical_discovery_transactions')
    parser.add_argument('--marathon-bindings', type=Path, help='JSON map from run IDs to exact canonical cycle and state-root paths')
    args = parser.parse_args()
    try:
        manifest = export_package(args.output, repository_root=args.repository_root, enable_demo=not args.browse_only,
            marathon_run_id=args.marathon_run_id, canonical_theory_cycle=args.canonical_theory_cycle,
            canonical_theory_state_root=args.canonical_theory_state_root,
            marathon_bindings=json.loads(args.marathon_bindings.read_text()) if args.marathon_bindings else None)
    except (ExportError, ValueError, OSError) as exc:
        parser.exit(1, f'Export failed: {exc}\n')
    with args.output.open('rb') as stream:
        digest = hashlib.file_digest(stream, 'sha256').hexdigest()
    print(json.dumps({'archive': str(args.output.resolve()), 'sha256': digest,
                      'bytes': args.output.stat().st_size, 'files': len(manifest['files']),
                      'collections': {k: len(v) for k, v in manifest['collections'].items()},
                      'executable_workflows': len(manifest['runtime']['workflows'])}, indent=2))


if __name__ == '__main__':
    main()
