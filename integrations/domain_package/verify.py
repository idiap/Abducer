# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Check an export with the target Lunar reader and Abducer fidelity oracles.

The target checkout is explicit and read-only. Validation extracts into a private
temporary directory, imports only Lunar's validator code, and never executes any
archive entrypoint, connects to a database or installs runtime dependencies.
"""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import importlib
import json
from pathlib import Path
import sys
import tempfile

from .viewer import selected_viewer_paths, validate_viewer, viewer_catalog
from .runtime_registration import ENTRY_FILE, runtime_declaration


def verify_archive(archive: Path, lunar_root: Path) -> dict:
    """Require target-reader acceptance and exact source-to-resource fidelity."""
    lunar_root = lunar_root.resolve(strict=True)
    sys.path.insert(0, str(lunar_root))
    reader = importlib.import_module('app.backend.domain_packages.archive')
    expected = lunar_root / 'app/backend/domain_packages/archive.py'
    if Path(reader.__file__).resolve() != expected:
        raise ValueError('loaded archive reader is not from the requested Lunar checkout')
    records = importlib.import_module('app.backend.domain_packages.records')
    pinned = Path(__file__).parent / 'format'
    pin = json.loads((pinned / 'FORMAT-PIN.json').read_text())
    for name, digest in pin['files'].items():
        canonical = expected.parent / 'format' / name
        if hashlib.sha256(canonical.read_bytes()).hexdigest() != digest:
            raise ValueError(f'target Lunar contract differs from export pin: {name}')
        if hashlib.sha256((pinned / name).read_bytes()).hexdigest() != digest:
            raise ValueError(f'local pinned contract changed: {name}')

    with tempfile.TemporaryDirectory(prefix='abducer-lunar-validation-') as temporary:
        validated = reader.validate_archive(archive.resolve(strict=True), Path(temporary) / 'snapshot', reader.ArchiveLimits())
        records.historical_facts(validated.documents)
        root, manifest, documents = validated.root, validated.manifest, validated.documents
        bundle_path, catalog_path = selected_viewer_paths(manifest, documents)
        viewer = validate_viewer(root / 'repository/runtime')
        if json.loads((root / bundle_path).read_text()) != viewer:
            raise ValueError('Lunar-selected bundle differs from validated viewer')
        if json.loads((root / catalog_path).read_text()) != viewer_catalog(viewer):
            raise ValueError('Lunar-selected catalog differs from viewer workflows')
        inventory = {r['path']: r for r in manifest['files']}
        index = json.loads((root / 'repository/export-index.json').read_text())
        for row in index['source_files']:
            actual = inventory['repository/runtime/' + row['path']]['sha256']
            if row['sha256'] != actual:
                raise ValueError('source-index digest mismatch')
        skill_files = 0
        resource_rows = {r['id']: r for r in manifest['collections']['skills']}
        for skill in documents['skills']:
            source_dir = 'repository/runtime/' + skill['metadata']['source_directory']
            raw = (root / source_dir / 'SKILL.md').read_bytes()
            if skill['instructions'].encode('utf-8') != raw:
                raise ValueError('skill instructions differ from source bytes')
            prefix = 'skills/' + skill['id'] + '/files/'
            for file in resource_rows[skill['id']]['files']:
                source = source_dir + '/' + file.removeprefix(prefix)
                if inventory[file]['sha256'] != inventory[source]['sha256']:
                    raise ValueError('skill support file differs from source')
                skill_files += 1
        for report in documents['reports']:
            metadata = report['metadata']
            if metadata['source_sha256'] != inventory['repository/runtime/' + metadata['source_path']]['sha256']:
                raise ValueError('report source digest differs from snapshot')
            if metadata['original_text_file']:
                original = inventory[metadata['original_text_file']]['sha256']
                if original != metadata['source_sha256']:
                    raise ValueError('original Markdown attachment differs from source')
            if any(report[key] for key in ('runs', 'outputs', 'revisions', 'provenance')):
                raise ValueError('repository export invented execution or database history')
        source_workflows = json.loads((root / 'repository/runtime/abducer-prism/workflows/manifest.json').read_text())
        workflows = [r for r in documents['repository'] if r['kind'] == 'workflow']
        actual = {r['metadata']['source_evidence']['id']: r['metadata']['source_evidence'] for r in workflows}
        if actual != {r['id']: r for r in source_workflows['workflows']}:
            raise ValueError('workflow evidence differs from original manifest')
        runtime = manifest['runtime']
        demo = index['lunar_execution'] in {'source_yang_mills_marathon', 'source_discovery_marathon'}
        if demo:
            binding = json.loads((root / 'repository/marathon-binding.json').read_text())
            runs = binding.get('runs') if binding.get('version') == 2 else None
            if any(runtime[key] != value for key, value in runtime_declaration(runs).items()):
                raise ValueError('runtime differs from the reviewed native marathon declaration')
            original = 'repository/runtime/integrations/domain_package/discovery.prism'
            if inventory[ENTRY_FILE]['sha256'] != inventory[original]['sha256']:
                raise ValueError('runtime wrapper differs from the source snapshot')
            if binding != index['marathon_binding']:
                raise ValueError('marathon binding differs from the source index')
            for run in runs or []:
                if run.get('initialize') is True:
                    if (run.get('run_id') != 'new' or run.get('cycle_count') != 0
                            or run.get('canonical_theory_cycle') is not None):
                        raise ValueError('new-run catalog entry invents prior execution or authority')
                    continue
                state = json.loads((root / f"repository/runtime/agentic/runs/discovery_marathons/{run['run_id']}/run_state.json").read_text())
                if any(state.get(key) != run[key] for key in ('target_id', 'run_id', 'cycle_count')):
                    raise ValueError('catalog differs from its source run state')
        elif any(runtime[key] for key in ('workflows', 'entrypoints', 'planning_hooks')):
            raise ValueError('browse-only export registered executable runtime capabilities')
        return {
            'status': 'pass', 'reader': str(expected),
            'archive_sha256': validated.archive_digest, 'archive_bytes': archive.stat().st_size,
            'expanded_payload_bytes': sum(r['size'] for r in manifest['files']),
            'payload_files': len(inventory), 'source_files': len(index['source_files']),
            'collections': {k: len(v) for k, v in documents.items()},
            'workflow_materialization_statuses': dict(Counter(r['metadata']['source_materialization_status'] for r in workflows)),
            'skill_instructions_compared': len(documents['skills']), 'skill_support_files_compared': skill_files,
            'skill_header_statuses': dict(Counter(r['metadata']['front_matter_status'] for r in documents['skills'])),
            'reports_with_unresolved_historical_links': sum(bool(r['metadata']['unresolved_historical_links']) for r in documents['reports']),
            'live_execution_registered': demo, 'execution_tested_by_archive_reader': False,
            'research_prerequisites_bound': bool(demo and (binding.get('canonical_theory_cycle') or
                any(run.get('canonical_theory_cycle') for run in binding.get('runs', [])))),
            'marathon_runs': binding.get('runs', []) if demo else [],
            'executable_workflows': len(runtime['workflows']), 'database_import_executed': False,
            'viewer_projects': len(viewer['projects']),
            'visible_workflows': sum(len(p['workflows']) for p in viewer['projects']),
            'viewer_bundle_linked': True, 'viewer_catalog_linked': True,
        }


def main() -> None:
    """Print a machine-readable validation receipt without changing either repo."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('archive', type=Path)
    parser.add_argument('--lunar-root', type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(verify_archive(args.archive, args.lunar_root), indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
