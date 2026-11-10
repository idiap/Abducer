<!--
# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
-->

# P vs NP Runbook

This runbook documents the integrated workflow for `KB/p-vs-np.kb.md`.

## 1) Parse Deep Research Report into P vs NP KB

Input file example:

- `/Users/user/Downloads/deep-research-report.md`

Command:

```bash
python3 skills/ingest/pvsnp-kb-parser/scripts/parse_report.py \
  --input /Users/user/Downloads/deep-research-report.md \
  --output-statements artifacts/p-vs-np/deep-research-report.statements.json \
  --source-id src.deep-research-report \
  --citation /Users/user/Downloads/deep-research-report.md \
  --kb KB/p-vs-np.kb.md \
  --section-policy status
```

Notes:

- `--dry-run` performs validation without mutating KB.
- If `--kb` is missing, parser can initialize from `KB/problem-template.kb.md`.

## 2) Build Concept Evolution Narrative

Create or update:

- `artifacts/p-vs-np/concept-evolution.md`

Format expectation:

- phase headings using `## ...`
- statement IDs referenced in backticks, e.g. `` `st.thm.example` ``.

## 3) Run Deterministic Pipeline

Command:

```bash
python3 skills/orchestration/kb-orchestrator/scripts/run_orchestrator.py \
  --intent pipeline \
  --kb KB/p-vs-np.kb.md \
  --concept artifacts/p-vs-np/concept-evolution.md \
  --rounds 3
```

Primary outputs:

- `artifacts/p-vs-np/connection-analysis.json`
- `phyp/p-vs-np.proof-hypotheses.yaml`
- `artifacts/p-vs-np/coherence-report.json`
- `artifacts/p-vs-np/entrypoints.json`
- `artifacts/p-vs-np/entrypoint-pathways.json`
- `artifacts/p-vs-np/epistemic-hardness.json`
- `artifacts/p-vs-np/bridge-plan.json`
- `artifacts/p-vs-np/concept-gap-abstractions.json`
- `artifacts/p-vs-np/proof-strategies.json`
- `artifacts/p-vs-np/proof-sketches.json`
- `artifacts/p-vs-np/novelty-maximizing-prompt.txt`
- `artifacts/p-vs-np/hypothesis-evaluation.json`
- `artifacts/p-vs-np/hypothesis-refutation-loop.json`
- `artifacts/p-vs-np/revision-loop.json`
- `artifacts/p-vs-np/reasoning-process-report.md`
- `artifacts/p-vs-np/discovery-interpretation-report.md`
- `artifacts/p-vs-np/process-graph.json`
- `artifacts/p-vs-np/process-graph-evolution.json`
- `artifacts/p-vs-np/process-graph.html`
- `artifacts/p-vs-np/process-graph-states/state-*.json`
- `artifacts/p-vs-np/reasoning-dynamics.json`
- `artifacts/p-vs-np/reasoning-dynamics.md`
- `artifacts/p-vs-np/reasoning-dynamics.html`
- `artifacts/p-vs-np/reasoning-log-index.json`
- `artifacts/p-vs-np/reasoning-log-index.md`
- `phyp/p-vs-np.hypotheses-evaluated.md`
- `phyp/p-vs-np.hypotheses-reviewed.md`
- `phyp/p-vs-np.hypotheses-evaluated.tex`
- `phyp/p-vs-np.hypotheses-evaluated.pdf`
- `phyp/p-vs-np.hypotheses-reviewed.tex`
- `phyp/p-vs-np.hypotheses-reviewed.pdf`
- `phyp/p-vs-np.hypotheses-reviewed.yaml`

## 4) Optional: Run Integrated Test Script

Command:

```bash
python3 skills/discovery/kb-novel-proof-strategist/scripts/run_integrated_pvsnp.py
```

This script executes the later integrated reasoning stages, exports `phyp/*.md` to `.tex/.pdf`, and writes stage logs.

## 5) Optional: Evidence-Guided Hypothesis Loop

Directory convention:

- `artifacts/p-vs-np/round-evidence/round-1.json`
- `artifacts/p-vs-np/round-evidence/round-2.json`
- `artifacts/p-vs-np/round-evidence/round-3.json`

Run:

```bash
python3 skills/orchestration/kb-orchestrator/scripts/run_orchestrator.py \
  --intent hypothesis-loop \
  --kb KB/p-vs-np.kb.md \
  --analysis artifacts/p-vs-np/connection-analysis.json \
  --phyp phyp/p-vs-np.proof-hypotheses.yaml \
  --coherence artifacts/p-vs-np/coherence-report.json \
  --round-evidence-dir artifacts/p-vs-np/round-evidence \
  --rounds 3
```

## 6) Validate and Regressions

Run tests:

```bash
pytest -q
```

Important current tests:

- `tests/discovery/test_hypothesis_eval.py`
- `tests/domains/test_connector_status_filter.py`
- `tests/formal/test_pvsnp_parser_dry_run.py`

## 7) Inspect Reasoning Logs

Look under:

- `artifacts/reasoning-logs/kb-orchestrator/`
- `artifacts/reasoning-logs/kb-proof-connector/`
- `artifacts/reasoning-logs/kb-coherence-evaluator/`
- `artifacts/reasoning-logs/kb-hypothesis-evaluator/`
- `artifacts/reasoning-logs/kb-hypothesis-refutation-loop/`
- `artifacts/reasoning-logs/kb-revision-loop/`

Each log contains the agent name, steps, and output file declarations.

## 8) Azure API Discovery Marathon with Parallel Branch Agents

For long P vs NP runs, use Azure/API branch execution when the aim is to run
several independent route probes in the same cycle. Parallel workers are used
only for branch interpretation; scheduler merge, branch memory, reports, and
the next-analysis queue remain serialized.

Before a marathon, refresh the route-specific negative-tactic packet:

```bash
python agentic/scripts/build_pvsnp_negative_tactic_packet.py
python agentic/scripts/validate_pvsnp_negative_tactics.py
```

This packet is consumed by the scheduler, branch prompts, Strategy Judge report
panel, and scientific contribution monitor. It chooses between:

- constructive bridge-building when a real escape condition remains;
- proof by contradiction when a negated local subclaim has a carrier and an
  accepted conflict target;
- scoped impossibility/no-go theorem formation when a method class has stable
  parameters and escape conditions;
- falsifier search when a finite or symbolic failure mode is visible;
- backtrack, quarantine, or stop only when the branch cannot name source object,
  target class, transfer inequality, conflict target, barrier status, and
  escape condition after sharpening.

Do not use global "assume P=NP" rhetoric. The packet must stay local to route
families such as black-box substitution, padding/projection, natural properties,
MCSP/MKtP carriers, proof-complexity transfer, and all-exponent uniformity
lifting.

Before choosing the next route family, refresh the cumulative result atlas:

```bash
python agentic/scripts/build_result_subgoal_atlas.py
python agentic/scripts/validate_result_subgoal_atlas.py
python agentic/scripts/build_problem_space_map.py
python agentic/scripts/validate_problem_space_map.py
python agentic/scripts/build_derivation_vault.py
python agentic/scripts/validate_derivation_vault.py
python agentic/scripts/update_subgoal_state_from_cycle.py
```

For P vs NP, the atlas is the authoritative memory of which subgoals have
already produced content-specific results. Use it to distinguish durable
progress from repeated analysis. Continue a branch when it can close an atlas
obligation: for example, compute a transfer exponent, prove a no-go lemma for a
named method class, isolate advice leakage, or turn a barrier diagnosis into a
formal obstruction. Demote or backtrack when the next action only restates a
known hardness-magnification, naturalness, padding, proof-complexity, MCSP/MKtP,
or all-exponent-uniformity pressure without changing the proof state.

The generated report exposes this state under **Result Atlas**. See
[Cumulative Result And Subgoal Atlas](../../research-methods/result-subgoal-atlas.md) for how to read
the achievement states, derivation vault, and problem-space map.

Initialize or resume the target-specific run, then launch a time-boxed job:

```bash
python agentic/scripts/run_discovery_marathon_job.py \
  --target p-vs-np-target \
  --duration-seconds 7200 \
  --branch-engine api \
  --min-cycle-seconds 600 \
  --max-active-branches 3 \
  --parallel-branches \
  --api-max-workers 3 \
  --api-request-spacing-seconds 2
```

The scheduler diversifies selected branches across P vs NP pressure families:
hardness-magnification thresholds, barrier/impossibility control, MCSP or
meta-complexity carriers, proof-complexity transfer, uniformity/advice lifting,
and Gedanken-style concrete cases.

Every completed parallel cycle writes:

- `parallel_execution`: worker count, engine, request spacing, and serialized
  merge policy;
- `branch_execution_records`: one completed record per selected branch in
  scheduler order;
- `parallel_synthesis`: cited branches, common proof obligations,
  cross-branch conflicts, no-go opportunities, and queue promotions.

Validate the parallel contract:

```bash
python agentic/scripts/validate_parallel_api_marathon.py
python agentic/scripts/validate_discovery_marathon_cycle.py
```
