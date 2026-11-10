#!/usr/bin/env python3
# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Project captured sources and labeled proof guidance into the original report.

The context supplements live cycle results; it never creates a cycle, canonical
receipt, model judgment or new theorem claim. All source metadata comes from the
run's immutable acquisition. Strategy prose is explicit coordinator guidance.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from agentic_common import ROOT, write_json
from agentic.discovery.bootstrap_literature import reopen_acquisition


TARGET = 'markov-kakutani-fixed-point-theorem-target'


def build_context(initialization: Path) -> tuple[dict, dict]:
    capture = initialization / 'acquisition'
    manifest = json.loads((capture / 'acquisition.json').read_text())
    if manifest['target_id'] != TARGET:
        raise ValueError('This context belongs only to the fixed-point target')
    snapshot = reopen_acquisition(capture, expected_digest=manifest['content_digest'],
        target_id=TARGET, run_id=manifest['run_id'], theory_state_digest=manifest['theory_state_digest'])
    assessed = json.loads((initialization / 'authorship/source-assessment/result.json').read_text())['value']
    assessments = {row['source_id']: row for row in assessed['assessments']}
    references = []
    by_work = {}
    for source in snapshot['sources']:
        assessment = assessments.get(source['source_id'], {})
        work = source.get('work_identity') or source['url']
        if work in by_work:
            by_work[work]['source_ids'].append(source['source_id'])
            continue
        reference = {
            'source_id': source['source_id'], 'title': source['title'], 'url': source['url'],
            'source_ids': [source['source_id']], 'work_identity': work,
            'authors': ', '.join(source.get('authors', [])), 'year': source.get('publication_date', ''),
            'role': assessment.get('relevance', 'unassessed'), 'status': 'captured metadata; claims unverified',
            'supports': assessment.get('reason', 'Metadata establishes source identity only.'),
            'limitation': ' '.join(source.get('limitations', []) + assessment.get('credibility_concerns', [])),
        }
        references.append(reference)
        by_work[work] = reference
    provenance = {'target_id': TARGET, 'run_id': manifest['run_id'],
        'snapshot_id': snapshot['snapshot_id'], 'acquisition_digest': manifest['content_digest'],
        'authorship': 'Coordinator-written explanatory context plus captured sources and model relevance assessments',
        'scientific_novelty_claim': False, 'formal_proof_verification_claim': False}
    literature = {**provenance, 'problem_name': 'Markov–Kakutani: finite commuting families',
        'source_record_count': len(snapshot['sources']), 'unique_work_count': len(references),
        'problem_statement': {
            'accessible': 'A finite family of commuting continuous affine maps on one nonempty compact convex set has a point fixed by every map. This run reconstructs that known result.',
            'formal_shape': r'\bigcap_{i=1}^{m}\operatorname{Fix}(T_i)\ne\varnothing',
        },
        'why_difficult': {
            'overview': 'Separate fixed points need not coincide. Commutativity must preserve earlier fixed sets, and compactness needs subnets in the general ambient topology.',
            'core_tension': 'The central bridge is an invariant compact convex fixed set, not a numerical limit of arbitrary iterates.',
        },
        'literature_stages': [
            {'period': 'repository baseline', 'title': 'Known theorem and explicit proof obligations',
             'core_shift': 'The repository KB isolates Cesaro averages, single-map existence and commuting fixed-set invariance.',
             'what_became_possible': 'A bounded reconstruction with individual proof obligations.',
             'what_remained_open': 'The run must supply and check each argument rather than count the KB statement as its own proof.'},
            {'period': snapshot['search_completed_at'], 'title': 'Actual bounded source capture',
             'core_shift': f"Six public search lanes returned {len(snapshot['sources'])} source records representing {len(references)} distinct works. Duplicate metadata records are grouped here; the original capture retains all records.",
             'what_became_possible': 'Inspect exact titles, metadata and available abstracts with separate relevance assessments.',
             'what_remained_open': 'Full-text validation and exhaustive correction/retraction coverage are not established.'},
        ],
        'references': references,
        'why_it_matters': ['This small known theorem makes a complete discovery workflow inspectable: the proof has distinct averaging, compactness and invariance steps, plus elementary failure examples.'],
        'solution_criteria': [
            'State all domain, topology, compactness, convexity, continuity, affinity and commutativity assumptions.',
            'Derive the Cesaro telescoping identity and show every continuous seminorm of its residual tends to zero.',
            'Use compact subnet extraction and continuity to obtain a single-map fixed point.',
            'Prove fixed sets are compact convex and invariant under the remaining commuting maps; conclude by finite induction.',
            'Keep finite examples, known-theorem reconstruction, formal verification and novelty distinct.',
        ],
        'workflow_implications': [
            {'lesson': 'Known-theorem reconstruction does not require speculative scientific novelty.',
             'active_workflow_effect': 'Use the explicitly reasoned wildcard exception while retaining canonical, mathematical and report checks.'},
            {'lesson': 'A fixed point of an average of maps need not be a common fixed point.',
             'active_workflow_effect': 'Test the constant-map counterexample and demand the fixed-set invariance argument.'},
        ],
        'open_obligations': ['Check the actual model proof against the separate mathematical review.',
            'General arbitrary-family and quantitative approximate-commutation extensions are outside this bounded target.'],
        'required_skills': ['kb-deduce', 'counterexample-hunter', 'epistemic-status-ledger'],
        'coverage_limits': snapshot['coverage_limits'],
    }
    strategies = {**provenance, 'status': 'explanatory proof guidance, not additional executed branches',
        'strategies': [
            {'title': 'Cesaro averaging and finite induction',
             'macro_thesis': 'Affinity makes the residual telescope. Compactness supplies a cluster point; commutativity preserves the fixed set at every induction step.',
             'validation': 'Check the seminorm bound, subnet indices, continuity and invariance before restricting the next map.'},
            {'title': 'Simultaneous finite box averaging',
             'macro_thesis': 'Average T_1^k1 ... T_m^km x over a finite rectangular index box. Commutativity turns each residual into two boundary faces. This is an alternative proof route for comparison.',
             'validation': 'Show all orbit points remain in K and bound each face-average difference by a compact-set seminorm diameter divided by N; use one common subnet.'},
            {'title': 'Assumption and counterexample audit',
             'macro_thesis': 'Separate existence from uniqueness and test what changes when compactness, convexity or commutativity is removed.',
             'validation': 'Use exact commuting projections, noncommuting constants, translation on R and reflection of {-1,1}; do not generalize a finite computation into the full theorem.'},
        ]}
    return literature, strategies


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--initialization', type=Path, required=True)
    args = parser.parse_args()
    literature, strategies = build_context(args.initialization)
    for kind, value in [('target_literature_evolution', literature), ('macro_strategy', strategies)]:
        write_json(ROOT / 'agentic/reports' / kind / 'targets' / TARGET / 'latest.json', value)
    print(json.dumps({'target_id': TARGET, 'source_records': literature['source_record_count'],
                      'distinct_works': literature['unique_work_count']}))


if __name__ == '__main__':
    main()
