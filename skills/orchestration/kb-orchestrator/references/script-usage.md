<!--
# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
# 
# SPDX-License-Identifier: MIT
-->

# Script Usage

## Run Deterministic Pipeline

```bash
skills/orchestration/kb-orchestrator/scripts/run_orchestrator.py \
  --intent pipeline \
  --kb KB/p-vs-np.kb.md \
  --concept artifacts/p-vs-np/concept-evolution.md \
  --export-phyp-docs \
  --phyp-doc-pattern "*.md" \
  --phyp-pdf-engine xelatex \
  --rounds 3
```

## Run Coherence Stage Only

```bash
skills/orchestration/kb-orchestrator/scripts/run_orchestrator.py \
  --intent coherence-eval \
  --kb KB/p-vs-np.kb.md \
  --analysis artifacts/p-vs-np/connection-analysis.json \
  --phyp phyp/p-vs-np.proof-hypotheses.yaml
```

## Run Cohere Mode

```bash
skills/orchestration/kb-orchestrator/scripts/run_orchestrator.py \
  --intent cohere \
  --kb KB/p-vs-np.kb.md
```

`cohere` runs the connector stage and the coherence evaluator in sequence.

## Generate Human-Readable Interpretation Reports

```bash
skills/orchestration/kb-orchestrator/scripts/run_orchestrator.py \
  --intent interpretation-reports \
  --kb KB/p-vs-np.kb.md
```

Or call the generator directly:

```bash
skills/orchestration/kb-orchestrator/scripts/generate_interpretation_reports.py \
  --artifacts-dir artifacts/p-vs-np \
  --kb KB/p-vs-np.kb.md
```

Generate a run-level reasoning-log index directly:

```bash
skills/orchestration/kb-orchestrator/scripts/generate_reasoning_log_index.py \
  --artifacts-dir artifacts/p-vs-np \
  --kb KB/p-vs-np.kb.md \
  --kb-ref p-vs-np \
  --reasoning-log-root artifacts/reasoning-logs
```

Generate dynamic typed process graph artifacts directly:

```bash
skills/orchestration/kb-orchestrator/scripts/generate_process_graph.py \
  --artifacts-dir artifacts/p-vs-np \
  --kb KB/p-vs-np.kb.md \
  --kb-ref p-vs-np \
  --reasoning-log-root artifacts/reasoning-logs
```

By default (when `--run-id` is omitted), the process graph is built from the latest end-to-end orchestrator run (`pipeline`/`abductive-loop`) for the KB. If none exist, it falls back to the latest orchestrator run.

Generate reasoning dynamics metrics + visualization dashboard directly:

```bash
skills/orchestration/kb-orchestrator/scripts/generate_reasoning_dynamics.py \
  --artifacts-dir artifacts/p-vs-np \
  --process-graph-evolution artifacts/p-vs-np/process-graph-evolution.json
```

## Run Hypothesis Evaluation Loop Only

```bash
skills/orchestration/kb-orchestrator/scripts/run_orchestrator.py \
  --intent hypothesis-loop \
  --kb KB/p-vs-np.kb.md \
  --analysis artifacts/p-vs-np/connection-analysis.json \
  --phyp phyp/p-vs-np.proof-hypotheses.yaml \
  --coherence artifacts/p-vs-np/coherence-report.json \
  --round-evidence-dir artifacts/p-vs-np/round-evidence
```

## Run Expert-Paper Synthesis Only

```bash
skills/orchestration/kb-orchestrator/scripts/run_orchestrator.py \
  --intent expert-paper \
  --kb KB/p-vs-np.kb.md
```

## Run Revision Loop Only

```bash
skills/orchestration/kb-orchestrator/scripts/run_orchestrator.py \
  --intent revision-loop \
  --kb KB/p-vs-np.kb.md \
  --phyp phyp/p-vs-np.hypotheses-reviewed.yaml \
  --coherence artifacts/p-vs-np/coherence-report.json
```

## Notes

- `abductive-loop` executes deterministic stages and reports a manual checkpoint for prompt-driven `kb-abduce` and `kb-deduce`; it now includes `coherence-eval` before hypothesis testing and `revision-loop` after testing.
- `pipeline` automatically includes `conjecture`, `strategies`, and `proof-sketch` before hypothesis evaluation.
- `pipeline` automatically includes `expert-paper` after reasoning-dynamics to produce a scientific write-up and expert hypothesis recommendations.
- `pipeline` and `abductive-loop` automatically generate `reasoning-process-report.md` and `discovery-interpretation-report.md`.
- `pipeline` and `abductive-loop` also generate `process-graph.*` and `reasoning-dynamics.*` artifacts to track inferential dynamics over time.
- All orchestrator runs generate `reasoning-log-index.md/.json` to verify that expected stage logs were emitted.
- Artifact defaults resolve under `artifacts/<kb-ref>/` and `phyp/<kb-ref>.*`, where `kb-ref` is `kb_id` in KB front matter when available.
- Optional `--kb-ref` can be used to pin the reference explicitly; when front matter contains `kb_id`, mismatches are rejected.
- When `--export-phyp-docs` is enabled (default), Markdown files in `phyp/` are exported to `.tex` and `.pdf` via `export_phyp_docs.py`.
