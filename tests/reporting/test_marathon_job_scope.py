# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""A new target must not inherit another run's failures or job status."""
import importlib
import json
from pathlib import Path


def test_html_jobs_follow_exact_run_even_when_filename_is_misleading(tmp_path, monkeypatch):
    monkeypatch.syspath_prepend(str(Path(__file__).resolve().parents[2] / 'agentic/scripts'))
    renderer = importlib.import_module('generate_discovery_marathon_html')
    monkeypatch.setattr(renderer, 'JOB_DIR', tmp_path)
    for name, payload in {
        'requested-run-misleading': {'run_id': 'another-run', 'failed_cycle_attempts': 99},
        'matching': {'run_id': 'requested-run', 'failed_cycle_attempts': 0},
        'unidentified': {'failed_cycle_attempts': 42},
    }.items():
        (tmp_path / (name + '.json')).write_text(json.dumps(payload))
    jobs = renderer.load_job_summaries('requested-run')
    assert [job['job_id'] for job in jobs] == ['matching']
    assert renderer.quality_summary([], jobs)['failed_attempts'] == 0
    assert renderer.load_job_summaries('brand-new-run') == []


def test_generic_report_does_not_invent_historical_pvsnp_contributions(monkeypatch):
    monkeypatch.syspath_prepend(str(Path(__file__).resolve().parents[2] / 'agentic/scripts'))
    renderer = importlib.import_module('generate_discovery_marathon_html')
    monkeypatch.setattr(renderer, 'embedded_mathjax', lambda: '')
    document = renderer.render_generic_target_html({'report': {'target_id': 'fixed-point-target'}})
    assert 'Black-box substitution cap' not in document
    assert 'Projection-carrier demagnification' not in document
    assert 'No independently novel contribution is established' in document
    assert 'P vs NP' not in document
    assert 'MCSP/MKtP' not in document
    assert 'hardness magnification' not in document


def test_scoped_literature_does_not_require_replacing_global_report(tmp_path, monkeypatch):
    monkeypatch.syspath_prepend(str(Path(__file__).resolve().parents[2] / 'agentic/scripts'))
    renderer = importlib.import_module('generate_discovery_marathon_html')
    global_path = tmp_path / 'latest.json'
    global_path.write_text(json.dumps({'target_id': 'another-target'}))
    scoped = tmp_path / 'targets/fixed-point-target/latest.json'
    scoped.parent.mkdir(parents=True)
    scoped.write_text(json.dumps({'target_id': 'fixed-point-target', 'references': [{'title': 'Actual source'}]}))
    monkeypatch.setattr(renderer, 'TARGET_LITERATURE_EVOLUTION', global_path)
    assert renderer.load_target_literature_evolution('fixed-point-target')['references'][0]['title'] == 'Actual source'
