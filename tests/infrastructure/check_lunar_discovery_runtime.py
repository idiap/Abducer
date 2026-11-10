# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Exercise the actual Lunar worker with explicitly controlled provider responses.

This is integration evidence, not a live-model or scientific-quality benchmark.
Use --archive with an exported ZIP and an immutable --image. No test responder
is registered in the package; deployed runs always use the selected Lunar model.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
import tempfile
from uuid import uuid4

CONTEXT = ('Plants near a window grew faster, but watering also differed. '
           'Find competing explanations and propose a controlled test; observations are preliminary.')
RESPONSES = {
    'bounded_scope': 'Preliminary plant observations confound light and watering; distinguish both causes.',
    'hypothesis': 'Greater light could cause faster growth if watering is controlled.',
    'provisional_pattern': 'Growth differs with window position, with watering an unresolved confounder.',
    'bounded_model_implications': 'A light mechanism predicts greater growth at equal water; this is not an executed experiment.',
    'controlled_contrast': 'Compare equal-water light groups and equal-light water groups; randomize positions.',
    'scoped_refutation': 'The observations cannot distinguish water from light, so the causal claim remains unsupported.',
    'routing_basis': 'Reorient to a randomized light-by-water experiment before promoting a causal claim.',
}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--archive', type=Path, required=True)
    parser.add_argument('--lunar-root', type=Path, required=True)
    parser.add_argument('--image', required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    sys.path.insert(0, str(args.lunar_root.resolve() / 'app/backend'))
    from domain_packages.archive import validate_archive, ArchiveLimits
    from domain_packages.worker.transport import invoke_worker
    from domain_packages.worker.results import validate_worker_result
    from domain_packages.worker.sandbox import WorkerLimits
    from jsonschema import Draft202012Validator

    with tempfile.TemporaryDirectory(prefix='abducer-worker-check-') as raw:
        root = Path(raw)
        archive = validate_archive(args.archive.resolve(), root / 'package', ArchiveLimits())
        workflow = next(w for w in archive.manifest['runtime']['workflows'] if w['id'] == 'discovery_marathon_loop')
        calls = []
        def value(schema):
            if 'enum' in schema:
                return 'Reorient' if 'Reorient' in schema['enum'] else schema['enum'][0]
            if 'const' in schema:
                return schema['const']
            if 'anyOf' in schema or 'oneOf' in schema:
                options = schema.get('anyOf', schema.get('oneOf'))
                return value(next((s for s in options if 'Reorient' in json.dumps(s)), options[0]))
            if schema.get('type') == 'object':
                return {key: RESPONSES[key] if key in RESPONSES else value(item)
                        for key, item in schema.get('properties', {}).items()}
            if schema.get('type') == 'string':
                return 'Reorient'
            raise AssertionError('Unhandled controlled schema: ' + json.dumps(schema))

        def model(arguments):
            schema = arguments['response_format']['json_schema']['schema']
            reply = value(schema)
            Draft202012Validator(schema).validate(reply)
            calls.append({'schema': schema, 'reply': reply, 'messages': arguments['messages']})
            return {'choices': [{'message': {'content': json.dumps(reply)}}]}

        output = root / 'output'
        output.mkdir()
        request = {'contract_version': 1, 'request_id': str(uuid4()), 'operation': 'execute',
                   'workflow_id': workflow['id'], 'hook_id': None,
                   'input': {'mode': 'live', 'inputs': {'context_summary': CONTEXT}},
                   'authority': {'network': False, 'model_access': True}}
        result = invoke_worker(image=args.image, package_root=archive.root, run_root=output,
            manifest=archive.manifest, request=request, model_handler=model,
            model_snapshot={'provider': 'controlled-test', 'model_id': 'schema-responder'},
            limits=WorkerLimits(timeout_seconds=180))
        validate_worker_result(result, request, output)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps({'kind': 'controlled-provider-integration', 'image': args.image,
            'archive_sha256': archive.archive_digest, 'model_calls': len(calls),
            'schemas': [c['schema'] for c in calls], 'result': result}, indent=2))
        assert result['status'] == 'succeeded', result['error']
        assert len(calls) == 7, len(calls)
        assert CONTEXT in json.dumps(calls[0]['messages']), 'entered context never reached first model call'
        assert 'Promotable, Reorient, TargetReset, Stalled' in json.dumps(calls[-1]['messages']), 'routing choices missing from the real model prompt'
        assert result['prepared_input']['value'] == {'context_summary': CONTEXT}
        assert result['result']['structured_value']['disposition'] == 'Reorient'
        Draft202012Validator(workflow['output_schema']).validate(result['result'])
        assert result['result']['report_verification']['status'] == 'passed'
        assert len(result['result']['structured_value']['steps']) == 7
        for text in RESPONSES.values():
            assert text in result['result']['markdown'], 'report dropped a recorded reasoning step'
        assert {'report.md', 'discovery-result.json'} <= {a['path'] for a in result['artifacts']}
        failures = []
        for label, inputs, responder in (
            ('blank-context', {'context_summary': '  '}, model),
            ('malformed-provider', {'context_summary': CONTEXT},
             lambda args: {'choices': [{'message': {'content': '{}'}}]}),
            ('invalid-disposition', {'context_summary': CONTEXT},
             lambda args: {'choices': [{'message': {'content': json.dumps(
                 {**value(args['response_format']['json_schema']['schema']), 'disposition': 'Proven'}
                 if 'disposition' in args['response_format']['json_schema']['schema'].get('properties', {})
                 else value(args['response_format']['json_schema']['schema']))}}]}),
        ):
            failed_output = root / label
            failed_output.mkdir()
            bad_request = {**request, 'request_id': str(uuid4()), 'input': {'mode': 'live', 'inputs': inputs}}
            failed = invoke_worker(image=args.image, package_root=archive.root, run_root=failed_output,
                manifest=archive.manifest, request=bad_request, model_handler=responder,
                model_snapshot={'provider': 'controlled-test', 'model_id': label},
                limits=WorkerLimits(timeout_seconds=180))
            validate_worker_result(failed, bad_request, failed_output)
            assert failed['status'] == 'failed' and failed['result'] is None, label
            assert not (failed_output / 'report.md').exists(), label
            failures.append({'probe': label, 'status': failed['status'], 'error': failed['error']})
        receipt = json.loads(args.output.read_text())
        receipt['failure_probes'] = failures
        args.output.write_text(json.dumps(receipt, indent=2))
        print(json.dumps({'status': 'pass', 'controlled_model_calls': len(calls),
                          'events': len(result['events']), 'artifacts': len(result['artifacts']),
                          'fail_closed_probes': len(failures)}))


if __name__ == '__main__':
    main()
