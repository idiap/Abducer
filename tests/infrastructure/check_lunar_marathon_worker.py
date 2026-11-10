# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Check native worker dispatch and actual exported research prerequisites.

The positive fixture proves native dispatch and the scoped model channel, not
Yang–Mills execution. The real archive must refuse its absent canonical binding
before model access. Pass a current bound archive to a separate research run.
"""
import argparse
import hashlib
import json
from pathlib import Path
import sys
import tempfile
from uuid import uuid4


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
    request = {'contract_version': 1, 'request_id': str(uuid4()), 'operation': 'execute',
               'workflow_id': 'discovery_marathon_loop', 'hook_id': None,
               'input': {'mode': 'live', 'inputs': {}},
               'authority': {'network': False, 'model_access': True}}
    with tempfile.TemporaryDirectory(prefix='native-marathon-worker-') as raw:
        root = Path(raw)
        archive = validate_archive(args.archive.resolve(), root / 'archive', ArchiveLimits())
        catalog = json.loads((archive.root / 'repository/marathon-binding.json').read_text())
        readiness = []
        for index, run in enumerate(catalog['runs']):
            run_root = root / f'real-output-{index}'
            run_root.mkdir()
            calls = []
            request['input']['inputs'] = {key: run[key] for key in ('target_id', 'run_id')}
            result = invoke_worker(image=args.image, package_root=archive.root, run_root=run_root,
                manifest=archive.manifest, request=request, model_handler=lambda value: calls.append(value),
                model_snapshot={'provider': 'controlled', 'model_id': 'test'}, limits=WorkerLimits(timeout_seconds=120))
            validate_worker_result(result, request, run_root)
            assert result['status'] == 'failed' and result['result'] is None, result
            expected = 'declared public literature reads' if run.get('initialize') else 'no committed canonical theory cycle'
            assert expected in result['error']['message'], result['error']
            assert not calls and not result['artifacts']
            readiness.append({'target_id': run['target_id'], 'run_id': run['run_id'], 'error': result['error']})

        fixture = root / 'fixture'
        for name in ('repository', 'skills', 'reports', 'data-sources'):
            (fixture / name).mkdir(parents=True)
        hook = fixture / 'repository/hooks.py'
        hook.write_text('''from pathlib import Path
def prepare(**kwargs):
    return {'prepared_input': {'entry_argument_name':'context','value':{},'request_digest':'a'*64,'analysis_results':{}}, 'state':{}}
def execute(*,state,services):
    import subprocess, sys
    subprocess.run([sys.executable,'-c','print("controlled child log")'],check=True)
    return services.completion(messages=[{'role':'user','content':'native execution probe'}],reasoning_effort='high',timeout=30)
def verify(*,state,execution,services):
    text=execution['choices'][0]['message']['content']
    Path('/output/native.txt').write_text(text)
    return {'result':{'markdown':text,'structured_value':{'native':True},'analysis_results':{},'compact_prism_input':{},'narrative_slots':[], 'report_verification':{'status':'passed'}}}
''')
        invalid_prism = fixture / 'repository/never.prism'
        invalid_prism.write_text('This must never be compiled by native dispatch.')
        manifest = {'runtime': {'entrypoints': [{'id': op, 'operation': op, 'file': 'repository/hooks.py', 'callable': op}
                    for op in ('prepare', 'execute', 'verify')], 'workflows': [{
                        'id': request['workflow_id'], 'modes': ['live'], 'prepare_hook': 'prepare',
                        'execute_hook': 'execute', 'verify_hook': 'verify', 'entry_file': 'repository/never.prism', 'entry_argument': 'context'}]},
                    'files': [{'path': 'repository/' + p.name, 'sha256': hashlib.sha256(p.read_bytes()).hexdigest()}
                              for p in (hook, invalid_prism)]}
        output = root / 'fixture-output'
        output.mkdir()
        calls = []
        def model(arguments):
            calls.append(arguments)
            return {'choices': [{'message': {'content': 'Native worker completed.'}}]}
        positive = invoke_worker(image=args.image, package_root=fixture, run_root=output,
            manifest=manifest, request=request, model_handler=model,
            model_snapshot={'provider': 'controlled', 'model_id': 'test'}, limits=WorkerLimits(timeout_seconds=60))
        validate_worker_result(positive, request, output)
        assert positive['status'] == 'succeeded', positive['error']
        assert positive['result']['structured_value']['native'] is True
        assert len(calls) == 1 and calls[0]['reasoning_effort'] == 'high'
        receipt = {'status': 'passed', 'image': args.image, 'archive_sha256': archive.archive_digest,
            'native_dispatch': 'passed with controlled fixture', 'real_package_model_calls': 0,
            'real_package_readiness': readiness, 'research_execution_verified': False}
        args.output.write_text(json.dumps(receipt, indent=2) + '\n')
        print(json.dumps(receipt, indent=2))


if __name__ == '__main__':
    main()
