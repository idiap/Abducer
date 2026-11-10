# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Validate and render the manual paper lane's source-bound step explanations.

This is an integrity gate, not a semantic judge. Authors supply explanations;
reviewers record content-bound judgments. Native inventory is reopened separately
so dropping a difficult occurrence from the packet cannot shrink the paper scope.
"""
import argparse
import hashlib
import json
import re
from pathlib import Path

FIELDS = ('purpose', 'input', 'procedure', 'criterion', 'output', 'failure_next', 'example')


def digest(data):
    """Hash bytes or canonical JSON to bind source and review to exact content."""
    if not isinstance(data, bytes):
        data = json.dumps(data, sort_keys=True, ensure_ascii=False).encode()
    return hashlib.sha256(data).hexdigest()


def content_digest(workflow):
    """Review is excluded from its own digest; all authored content is included."""
    return digest({k: v for k, v in workflow.items() if k != 'review'})


def load_json(path):
    """Reject duplicate object keys instead of silently overwriting evidence."""
    def unique(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError(f'duplicate JSON field: {key}')
            result[key] = value
        return result
    return json.loads(Path(path).read_text(), object_pairs_hook=unique)


def local(root, name):
    """Keep packet references inside the selected repository, including symlinks."""
    path = (root / name).resolve()
    if Path(name).is_absolute() or not path.is_relative_to(root.resolve()):
        raise ValueError(f'nonlocal path: {name}')
    return path


def validate(packet, root, require_review=True):
    """Reconcile source inventory, field coverage and review identity; fail closed."""
    def need(condition, message):
        if not condition:
            raise ValueError(message)

    need(packet.get('version') == '1.0', 'unsupported packet version')
    sources = packet['sources']
    for name, expected in sources.items():
        need(digest(local(root, name).read_bytes()) == expected, f'stale source: {name}')
    manifest = packet['manifest']
    need(manifest in sources, 'manifest not frozen')
    native = load_json(local(root, manifest))
    native_ids = {w['id'] for w in native['workflows']}
    need(len(native_ids) == len(native['workflows']), 'duplicate manifest workflow')
    native_by_id = {w['id']: w for w in native['workflows']}
    scope = packet['scope']
    need(len(scope) == len(set(scope)), 'duplicate scope')
    need(set(scope) == native_ids, 'scope differs from canonical manifest')
    rows = packet['workflows']
    need(len(rows) == len(scope) and {w['id'] for w in rows} == set(scope), 'workflow coverage mismatch')
    count = 0
    for w in rows:
        name = w['id']
        need(bool(re.fullmatch(r'[A-Za-z0-9_-]+', name)), f'unsafe workflow id: {name}')
        original = native_by_id[name]
        layer_paths = {}
        for layer in ('types', 'occurrences', 'relations', 'reasoning'):
            relative = original.get('layers', {}).get(layer)
            if relative is None:
                need(bool(original.get('module_id')), f'missing layer/module_id: {name}')
                relative = original['module_id'] + '/' + layer + '.prism'
            need(not Path(relative).is_absolute(), f'nonlocal layer: {relative}')
            layer_path = local(root, str(Path(manifest).parent / relative))
            layer_name = layer_path.relative_to(root.resolve()).as_posix()
            need(layer_name in sources, f'unfrozen {name}/{layer}')
            layer_paths[layer] = layer_path
        reasoning = layer_paths['reasoning'].read_text()
        reasoning = '\n'.join(line.split('#', 1)[0] for line in reasoning.splitlines())
        bindings = re.findall(r'\[(\w+):\s*(\w+)\(', reasoning)
        inventory = dict(bindings)
        need(bool(bindings) and len(inventory) == len(bindings), f'empty/duplicate native bindings: {name}')
        declared = re.findall(r'^type (\w+)\s*=\s*(.+?->\s*Generated\[.*\])\s*$', layer_paths['occurrences'].read_text(), re.M)
        declarations = dict(declared)
        need(len(declarations) == len(declared), f'duplicate native declaration: {name}')
        steps = w['steps']
        need(len({s['binding'] for s in steps}) == len(steps), f'duplicate step binding: {name}')
        need(len(steps) == len(inventory), f'step count: {name}')
        need({s['binding']: s['operation'] for s in steps} == inventory, f'binding coverage: {name}')
        examples = set()
        for s in steps:
            key = f"{name}/{s['binding']}"
            need(s['operation'] in declarations, f'undeclared operation: {key}')
            need(bool(s.get('title', '').strip()), f'missing title: {key}')
            need(s['signature'].split() == declarations[s['operation']].split(), f'signature: {key}')
            for field in FIELDS:
                # Word counts reward filler and reject precise named inputs.
                # Scientific substance belongs to the content-bound manual review.
                need(isinstance(s.get(field), str) and bool(s[field].strip()), f'missing/empty field {field}: {key}')
            need(s['example'] not in examples, f'duplicate example: {key}')
            examples.add(s['example'])
            need(bool(s['evidence']), f'missing evidence: {key}')
            for ref in s['evidence']:
                need(ref['path'] in sources, f'unfrozen evidence: {key}')
                lines = local(root, ref['path']).read_text().splitlines()
                need(type(ref.get('start')) is int and type(ref.get('end')) is int, f'invalid source span type: {key}')
                need(1 <= ref['start'] <= ref['end'] <= len(lines), f'invalid source span: {key}')
            need(s['posture'] == 'declaration + prescribed procedure; illustration not execution', f'posture: {key}')
            if s['operation'].startswith('Unresolved'):
                need('unresolved' in s['procedure'].lower(), f'hidden projection gap: {key}')
        need(bool(w.get('contrast')) and bool(w.get('case')), f'case/contrast missing: {name}')
        if require_review:
            review = w.get('review', {})
            need(review.get('verdict') == 'pass', f'missing/pending semantic review: {name}')
            need(review.get('content_digest') == content_digest(w), f'stale review: {name}')
            need(review.get('sources_digest') == digest(sources), f'stale review sources: {name}')
            need(len(review.get('criteria', [])) == len(FIELDS) and set(review.get('criteria', [])) == set(FIELDS), f'incomplete review criteria: {name}')
            need(len(review.get('rationale', '').split()) >= 15, f'review rationale: {name}')
            need(bool(review.get('limitations', '').strip()), f'review limitations: {name}')
        count += len(steps)
    return {'workflows': len(rows), 'steps': count, 'sources': len(sources),
            'integrity': 'pass', 'semantic_review': 'recorded manual review' if require_review else 'not required for draft',
            'limit': 'No automatic semantic, runtime or efficacy validation.'}


def tex(text):
    """Render authored plain text as inert TeX; no source-provided commands run."""
    escapes = {'\\': r'\textbackslash{}', '&': r'\&', '%': r'\%', '$': r'\$', '#': r'\#',
               '_': r'\_\allowbreak{}', '{': r'\{', '}': r'\}', '~': r'\textasciitilde{}', '^': r'\textasciicircum{}'}
    return ''.join(escapes.get(c, c) for c in text)


def render(w):
    """Keep each scientific field visible without merging results and routing.

    Labels are presentation aliases only: the source-bound packet and its review
    digest retain the original seven fields. The manuscript already uses enumitem.
    """
    out = ['% Generated from step-explanations.json',
           r'\paragraph{Step-by-step reconstruction.}', tex(w['case']),
           'The following is a source-guided illustrative reconstruction. Internal procedures are prescriptions; the native declarations do not establish their execution.',
           r'\begin{enumerate}[leftmargin=*,label=\arabic*.]']
    for s in w['steps']:
        out += [r'\item \textbf{' + tex(s['title']) + '} (' + r'\texttt{' + tex(s['binding']) + '}).',
                r'\begin{description}[style=standard,labelindent=0pt,leftmargin=5.5em,labelwidth=5em,labelsep=0.5em,align=left,font=\normalfont\bfseries,itemsep=0.15em,parsep=0pt,topsep=0.3em]']
        for label, field in (('Purpose', 'purpose'), ('Input', 'input'),
                             ('Method', 'procedure'), ('Check', 'criterion'),
                             ('Output', 'output'), ('Next', 'failure_next'),
                             ('Example', 'example')):
            out.append(r'\item[' + label + '] ' + tex(s[field]))
        out += [r'\end{description}']
    out += [r'\end{enumerate}', r'\paragraph{Changed-input contrast.}', tex(w['contrast']), '']
    return '\n'.join(out)


def verify_inclusion(packet, root, manuscript, render_dir):
    r"""Check reachable literal inputs and exact fragments; compilation is separate.

    This deliberately supports literal \input/\include only. Dynamic TeX inclusion
    must be checked by the build lane; it cannot silently satisfy this gate.
    """
    root = root.resolve()
    start = local(root, str(manuscript))
    directory = local(root, str(render_dir))
    reachable = set()

    def visit(path):
        if path in reachable:
            return
        reachable.add(path)
        source = path.read_text()
        source = re.sub(r'(?<!\\)%[^\n]*', '', source)
        for ref in re.findall(r'\\(?:input|include)\s*\{([^{}]+)\}', source):
            candidate = Path(ref)
            if not candidate.suffix:
                candidate = candidate.with_suffix('.tex')
            # TeX input paths are relative to the main document build directory.
            child = local(root, str((start.parent / candidate).relative_to(root)))
            if not child.is_file():
                raise ValueError(f'missing manuscript input: {ref}')
            visit(child)

    visit(start)
    for workflow in packet['workflows']:
        fragment = directory / (workflow['id'] + '.tex')
        if fragment not in reachable:
            raise ValueError(f'missing manuscript inclusion: {workflow["id"]}')
        if fragment.read_text() != render(workflow):
            raise ValueError(f'stale rendered fragment: {workflow["id"]}')
    return 'all exact rendered fragments reachable through literal TeX inputs'


def main():
    """Draft rendering is explicit; delivery always requires content-bound review."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', type=Path, default=Path.cwd())
    parser.add_argument('--packet', type=Path, required=True)
    parser.add_argument('--render-dir', type=Path)
    parser.add_argument('--draft', action='store_true')
    parser.add_argument('--manuscript', type=Path, help='Check literal inclusion after rendering; requires --render-dir')
    args = parser.parse_args()
    if args.manuscript and not args.render_dir:
        parser.error('--manuscript requires --render-dir')
    packet = load_json(args.packet)
    report = validate(packet, args.repo, not args.draft)
    if args.render_dir:
        render_dir = local(args.repo, str(args.render_dir))
        render_dir.mkdir(parents=True, exist_ok=True)
        for w in packet['workflows']:
            output = local(args.repo, str(args.render_dir / (w['id'] + '.tex')))
            output.write_text(render(w))
    if args.manuscript:
        report['manuscript_inclusion'] = verify_inclusion(packet, args.repo, args.manuscript, args.render_dir)
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
