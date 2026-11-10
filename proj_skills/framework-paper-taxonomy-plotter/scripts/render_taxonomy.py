#!/usr/bin/env python3
# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Render reviewed taxonomy records as membership and typed-signature vector panels.

Graphviz handles text layout; this module preserves exact model records in a sidecar.
It deliberately does not infer taxonomic hierarchy or draw workflow execution edges.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess


KINDS = {'conceptual_grouping': ('dotted', 'none'), 'declared_subtype': ('solid', 'empty')}
CLAIM_STATUSES = {'declared', 'inferred', 'proposed', 'unknown'}
SOURCE_POSTURES = {'declared', 'implemented', 'observed', 'contested', 'unknown'}


def validate(model):
    """Reject ambiguous references before any files are written."""
    if not isinstance(model, dict):
        raise ValueError('model must be an object')
    if model.get('schema_version') != '1.0.0':
        raise ValueError('schema_version must be 1.0.0')
    all_ids = set()
    indexes = {}
    for field in ('layers', 'families', 'artifact_types', 'operations', 'workflows', 'relations'):
        records = model.get(field)
        if not isinstance(records, list):
            raise ValueError(f'{field} must be a list')
        indexes[field] = {}
        for record in records:
            if not isinstance(record, dict):
                raise ValueError(f'{field} records must be objects')
            key = record.get('id')
            if not isinstance(key, str) or not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_.:-]*', key):
                raise ValueError(f'invalid {field} ID: {key!r}')
            if key in all_ids:
                raise ValueError(f'duplicate ID: {key}')
            all_ids.add(key)
            indexes[field][key] = record
            if field != 'relations' and not isinstance(record.get('label'), str):
                raise ValueError(f'{key}: missing label')
            if record.get('claim_status') not in CLAIM_STATUSES or record.get('source_posture') not in SOURCE_POSTURES:
                raise ValueError(f'{key}: invalid or missing claim_status/source_posture')
    def refs(record, field, target):
        values = record.get(field)
        if not isinstance(values, list) or any(not isinstance(v, str) for v in values) or len(set(values)) != len(values):
            raise ValueError(f'{record["id"]}: {field} must be a unique list')
        if set(values) - set(indexes[target]):
            raise ValueError(f'{record["id"]}: unresolved {field}')
    for family in model['families']:
        refs(family, 'layer_ids', 'layers')
    for operation in model['operations']:
        refs(operation, 'family_ids', 'families')
        refs(operation, 'workflow_ids', 'workflows')
    for record in model['families'] + model['operations']:
        target_field = 'layer_ids' if record['id'] in indexes['families'] else 'family_ids'
        details = record.get('membership_details', [])
        if not isinstance(details, list):
            raise ValueError('membership_details must be a list')
        for detail in details:
            if not isinstance(detail, dict) or detail.get('target_id') not in record[target_field] or detail.get('claim_status') not in CLAIM_STATUSES:
                raise ValueError('invalid membership_details target or claim status')
    for workflow in model['workflows']:
        refs(workflow, 'operation_ids', 'operations')
        for op_id in workflow['operation_ids']:
            if workflow['id'] not in indexes['operations'][op_id]['workflow_ids']:
                raise ValueError(f'{op_id}: inconsistent workflow membership')
    for operation in model['operations']:
        for wf_id in operation['workflow_ids']:
            if operation['id'] not in indexes['workflows'][wf_id]['operation_ids']:
                raise ValueError(f'{operation["id"]}: inconsistent operation membership')
    for artifact in model['artifact_types']:
        refs(artifact, 'type_arguments', 'artifact_types')
        refs(artifact, 'alternatives', 'artifact_types')
    for record in model['operations'] + model['workflows'] + model['artifact_types']:
        for direction in (('fields',) if record['id'] in indexes['artifact_types'] else ('inputs', 'outputs')):
            ports = record.get(direction)
            if not isinstance(ports, list):
                raise ValueError(f'{record["id"]}: {direction} must be a list')
            names = set()
            for port in ports:
                if not isinstance(port, dict):
                    raise ValueError(f'{record["id"]}: ports must be objects')
                name = port.get('name')
                expression = port.get('source_type_expression')
                if not isinstance(name, str) or not name or name in names:
                    raise ValueError(f'{record["id"]}: missing or duplicate port name')
                names.add(name)
                if not isinstance(expression, str) or not expression:
                    raise ValueError(f'{record["id"]}: missing source_type_expression')
                if port.get('type_id') is None:
                    if not port.get('unknown_reason'):
                        raise ValueError(f'{record["id"]}: unknown type needs unknown_reason')
                elif port['type_id'] not in indexes['artifact_types']:
                    raise ValueError(f'{record["id"]}: unresolved type_id')
    node_ids = all_ids - set(indexes['relations'])
    for relation in model['relations']:
        if relation.get('kind') not in KINDS:
            raise ValueError('unsupported taxonomy relation kind')
        if relation.get('source_id') not in node_ids or relation.get('target_id') not in node_ids:
            raise ValueError(f'{relation["id"]}: unresolved relation endpoint')
        if relation['kind'] == 'declared_subtype' and any(relation[key] not in indexes['artifact_types'] for key in ('source_id', 'target_id')):
            raise ValueError('declared_subtype endpoints must be artifact types')
    # Multiple parents are legitimate; a subtype cycle needs upstream equality
    # treatment instead of silently masquerading as a taxonomy hierarchy.
    subtype_edges = {}
    for relation in model['relations']:
        if relation['kind'] == 'declared_subtype':
            subtype_edges.setdefault(relation['source_id'], []).append(relation['target_id'])
    visiting, finished = set(), set()
    def visit(key):
        if key in visiting:
            raise ValueError('declared subtype cycle requires upstream resolution')
        if key in finished:
            return
        visiting.add(key)
        for target in subtype_edges.get(key, []):
            visit(target)
        visiting.remove(key)
        finished.add(key)
    for key in subtype_edges:
        visit(key)
    scope = model.get('scope', {}).get('requested_workflow_ids')
    if not isinstance(scope, list) or len(scope) != len(set(scope)) or not scope:
        raise ValueError('scope requires unique, nonempty requested_workflow_ids')
    if set(scope) != set(indexes['workflows']):
        raise ValueError('workflow inventory must match requested scope')
    coverage = model.get('coverage', [])
    if len(coverage) != len(scope) or {row.get('workflow_id') for row in coverage} != set(scope):
        raise ValueError('coverage must account for every scoped workflow exactly once')
    if any(row.get('disposition') not in {'modeled', 'partial', 'excluded', 'blocked'} or not isinstance(row.get('reason'), str) for row in coverage):
        raise ValueError('coverage requires valid disposition and reason')
    return indexes


def quote(value):
    """Quote DOT data as literal strings, never executable DOT fragments."""
    return json.dumps(str(value), ensure_ascii=False)


def wrap(value, width=18):
    """Break at words, CamelCase and punctuation without splitting Generated.

    Delimiters remain intact and no spaces are inserted inside source identifiers;
    the exact unwrapped expression is independently retained in the manifest.
    """
    lines = []
    for paragraph in str(value).splitlines():
        tokens = re.split(r'(?<=[a-z0-9])(?=[A-Z])|(?<=[\[\],;:])|(?=\s)|(?<=\s)', paragraph)
        current = ''
        for token in tokens:
            if current and len(current + token) > width:
                lines.append(current.rstrip())
                current = token.lstrip()
            else:
                current += token
        lines.append(current.rstrip())
    return '\n'.join(lines)


def label(record):
    """Expose epistemic qualifications in figures, not only their sidecars."""
    status = record.get('claim_status', 'unknown')
    return wrap(record['label']) + f'\n[{status}]'


def node(key, value, shape='box'):
    return f'{quote(key)} [label={quote(value)}, shape={shape}];'


def membership_label(record, target, kind):
    """An inferred assignment must not inherit a stronger node-level status."""
    status = next((d['claim_status'] for d in record.get('membership_details', []) if d['target_id'] == target), record['claim_status'])
    return kind + '\n[' + status + ']'


def graph(title, statements):
    return '\n'.join(['digraph taxonomy {', 'graph [rankdir=LR, bgcolor="white", pad=0.2, nodesep=0.28, ranksep=0.3];', 'node [fontname="Helvetica", fontsize=12, margin="0.08,0.06"];', 'edge [fontname="Helvetica", fontsize=12];', f'label={quote(wrap(title, 55))}; labelloc="t"; fontsize=14;', *statements, '}']) + '\n'


def port_label(ports, unresolved=None):
    """Retain names, exact expressions and wrapper annotations independently."""
    if not ports:
        return wrap('(no ports listed; unresolved facts remain)' if unresolved else '(none declared)')
    parts = []
    for port in ports:
        text = port['name'] + ': ' + port['source_type_expression']
        if port.get('wrapper'):
            text += '\nwrapper: ' + str(port['wrapper'])
        if port.get('type_id') is None:
            text += '\nunknown: ' + str(port['unknown_reason'])
        parts.append(wrap(text, 24))
    return '\n\n'.join(parts)


def pages(records, size):
    return [records[i:i + size] for i in range(0, len(records), size)] or [[]]


def tex_escape(value):
    table = {'\\': r'\textbackslash{}', '&': r'\&', '%': r'\%', '$': r'\$', '#': r'\#', '_': r'\_', '{': r'\{', '}': r'\}', '~': r'\textasciitilde{}', '^': r'\textasciicircum{}'}
    return ''.join(table.get(c, c) for c in value)


def render(model, raw, output, taxonomy_size=4, io_size=2):
    """Emit stable vector sources, figure fragments and exact semantic mappings."""
    if min(taxonomy_size, io_size) < 1:
        raise ValueError('page sizes must be positive')
    indexes = validate(model)
    if output.exists() and any(output.iterdir()):
        raise ValueError('output directory must be empty to prevent stale successful manifests')
    dot = shutil.which('dot')
    if not dot:
        raise ValueError('Graphviz dot is required; no files written')
    panels = []
    for page, operations in enumerate(pages(model['operations'], taxonomy_size), 1):
        statements = []
        family_ids = {key for op in operations for key in op['family_ids']}
        families = [r for r in model['families'] if r['id'] in family_ids]
        layer_ids = {key for family in families for key in family['layer_ids']}
        for layer in [r for r in model['layers'] if r['id'] in layer_ids]:
            statements.append(node(layer['id'], label(layer), 'ellipse'))
        for family in families:
            statements.append(node(family['id'], label(family), 'box'))
            for layer in family['layer_ids']:
                statements.append(f'{quote(layer)} -> {quote(family["id"])} [style=dashed, label={quote(membership_label(family, layer, "layer"))}];')
        for operation in operations:
            qualification = '\n(unclassified)' if not operation['family_ids'] else ''
            statements.append(node(operation['id'], label(operation) + qualification))
            for family in operation['family_ids']:
                statements.append(f'{quote(family)} -> {quote(operation["id"])} [style=solid, label={quote(membership_label(operation, family, "family"))}];')
        panels.append((f'taxonomy-{page:02}', graph('Reasoning membership', statements), operations, [], 'Reasoning membership. Dashed arrows denote layer membership; solid arrows denote family membership. Labels retain claim status. This is not execution order.'))
    # Inventory panels ensure unused concepts remain visible without repeating
    # every concept on every operation page and forcing unreadable reduction.
    for page, concepts in enumerate(pages(model['layers'] + model['families'], taxonomy_size), 1):
        if not concepts:
            continue
        statements = []
        for record in concepts:
            text = label(record)
            if 'layer_ids' in record:
                names = [membership_label(record, key, indexes['layers'][key]['label']) for key in record['layer_ids']]
                text += '\nLayers: ' + wrap(', '.join(names) or '(none declared)')
            statements.append(node(record['id'], text))
        panels.append((f'concepts-{page:02}', graph('Reasoning concept inventory', statements), concepts, [], 'Reasoning concept inventory, including concepts without selected operation occurrences. Position is for readability and implies no execution order or subtype relation.'))
    records_by_id = {r['id']: r for name, rows in indexes.items() if name != 'relations' for r in rows.values()}
    for page, relations in enumerate(pages(model['relations'], taxonomy_size), 1):
        if not relations:
            continue
        involved = sorted({r[k] for r in relations for k in ('source_id', 'target_id')})
        statements = [node(key, label(records_by_id[key])) for key in involved]
        for relation in relations:
            style, arrow = KINDS[relation['kind']]
            text = relation['kind'].replace('_', ' ') + '\n[' + relation.get('claim_status', 'unknown') + ']'
            statements.append(f'{quote(relation["source_id"])} -> {quote(relation["target_id"])} [style={style}, arrowhead={arrow}, label={quote(text)}];')
        panels.append((f'relations-{page:02}', graph('Explicit taxonomy relations', statements), [records_by_id[k] for k in involved], relations, 'Explicit relations. Dotted lines denote conceptual grouping; open arrowheads denote declared subtyping in the direction supplied by the model. Status labels qualify each claim.'))
    # Nominal records need a visible inventory, including fields not promoted to
    # native operation arguments and types which occur only in the taxonomy.
    for page, types in enumerate(pages(model['artifact_types'], io_size), 1):
        if not types:
            continue
        statements = []
        for record in types:
            text = label(record) + '\n' + wrap(record.get('source_name', record['id']))
            if record.get('fields'):
                text += '\nRecord fields:\n' + port_label(record['fields'])
            if record.get('type_arguments'):
                text += '\nType arguments:\n' + wrap(', '.join(indexes['artifact_types'][key].get('source_name') or indexes['artifact_types'][key]['label'] for key in record['type_arguments']), 32)
            if record.get('alternatives'):
                text += '\nAlternatives:\n' + wrap(', '.join(indexes['artifact_types'][key].get('source_name') or indexes['artifact_types'][key]['label'] for key in record['alternatives']), 32)
            statements.append(node(record['id'], text))
        panels.append((f'types-{page:02}', graph('Artifact type inventory', statements), types, [], 'Artifact type inventory. Nominal names, declared record fields and type arguments remain distinct. Record fields are not additional native operation arguments; proximity implies no subtype relation.'))
    for wf_number, workflow in enumerate(model['workflows'], 1):
        operations = [indexes['operations'][key] for key in workflow['operation_ids']]
        for page, chunk in enumerate(pages(operations, io_size), 1):
            statements = []
            # Workflow boundary signatures are distinct from each constituent operation.
            rows = [workflow] + chunk
            for row_number, record in enumerate(rows):
                prefix = f'r{row_number}'
                op_label = label(record)
                if row_number == 0:
                    op_label = 'Workflow boundary\n' + op_label
                statements.extend([node(prefix + 'i', port_label(record['inputs'], record.get('unknowns'))), node(prefix + 'op', op_label), node(prefix + 'o', port_label(record['outputs'], record.get('unknowns'))), f'{prefix}i -> {prefix}op [label="input"];', f'{prefix}op -> {prefix}o [label="output"];'])
            title = 'Input/output signatures: ' + wrap(workflow['label'])
            caption = 'Input/output signatures for ' + workflow['label'] + '. Arrows denote consumption and production, not temporal order or proof of successful generation. The workflow boundary is shown separately; port names, wrappers and unknowns are retained.'
            panels.append((f'io-{wf_number:02}-{page:02}', graph(title, statements), rows, [], caption))
    output.mkdir(parents=True, exist_ok=True)
    manifest = {key: model.get(key) for key in ('packet_id', 'input_digest', 'source_packet_id', 'scope', 'coverage', 'unknowns', 'evidence_refs')}
    manifest.update({'model_sha256': hashlib.sha256(raw).hexdigest(), 'semantic_model': model, 'graphviz': subprocess.run([dot, '-V'], capture_output=True, text=True, check=True).stderr.strip(), 'figures': []})
    tex = ['% Requires graphicx; paths are relative to the compilation directory.']
    for name, content, records, relations, caption in panels:
        path = output / (name + '.dot')
        path.write_text(content, encoding='utf-8')
        for extension in ('svg', 'pdf'):
            subprocess.run([dot, '-T' + extension, str(path), '-o', str(output / (name + '.' + extension))], check=True, capture_output=True)
        manifest['figures'].append({'id': name, 'files': [name + '.' + ext for ext in ('dot', 'svg', 'pdf')], 'records': records, 'relations': relations, 'caption': caption})
        tex.extend([r'\begin{figure}[p]', r'\centering', r'\includegraphics[width=\linewidth,height=.8\textheight,keepaspectratio]{' + name + '.pdf}', r'\caption{' + tex_escape(caption) + '}', r'\label{fig:reasoning-' + name + '}', r'\end{figure}'])
    (output / 'taxonomy-figures.tex').write_text('\n'.join(tex) + '\n', encoding='utf-8')
    manifest['output_sha256'] = {path.name: hashlib.sha256(path.read_bytes()).hexdigest() for path in sorted(output.iterdir()) if path.is_file()}
    (output / 'figure-manifest.json').write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    return manifest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('model', type=Path)
    parser.add_argument('--output-dir', type=Path, required=True)
    parser.add_argument('--taxonomy-per-page', type=int, default=4)
    parser.add_argument('--operations-per-page', type=int, default=2)
    args = parser.parse_args()
    if min(args.taxonomy_per_page, args.operations_per_page) < 1:
        parser.error('page sizes must be positive')
    try:
        raw = args.model.read_bytes()
        result = render(json.loads(raw), raw, args.output_dir, args.taxonomy_per_page, args.operations_per_page)
    except (ValueError, KeyError, TypeError, OSError, subprocess.CalledProcessError) as error:
        parser.exit(2, f'render_taxonomy: {error}\n')
    print(f'Rendered {len(result["figures"])} figures into {args.output_dir}')


if __name__ == '__main__':
    main()
