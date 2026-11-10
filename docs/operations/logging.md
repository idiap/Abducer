<!--
# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
-->

# Reasoning Logs

Every scripted skill run now creates two clearly separated observability artifacts:

- internal reasoning logs for auditability and deterministic trace/debug work,
- surfaced reasoning logs for human-oriented conceptual inspection of the reasoning dynamics.

Both are defined by `skills/common/reasoning_log.py`.

## Internal Reasoning Logs

Location:

- `artifacts/reasoning-logs/<agent-name>/<timestamp>-<pid>.md`

Examples:

- `artifacts/reasoning-logs/kb-orchestrator/20260311T081915Z-29182.md`
- `artifacts/reasoning-logs/kb-hypothesis-evaluator/20260311T083806Z-68890.md`

Purpose:

- audit which stage ran,
- trace exact commands, arguments, and declared outputs,
- support run-level indexing, process-graph generation, and failure debugging.

Format:

1. Header:
   - `Reasoning Log: <agent-name>`
   - started UTC timestamp
   - run ID
   - log file path
   - paired surfaced-log paths
2. Step trace:
   - `## Step @ <utc-iso>`
   - title and details
3. Run result:
   - status
   - ended timestamp
   - duration seconds
   - summary
4. Declared outputs:
   - label -> path mapping

## Surfaced Reasoning Logs

Location:

- `artifacts/reasoning-surfaces/<agent-name>/<timestamp>-<pid>.md`
- `artifacts/reasoning-surfaces/<agent-name>/<timestamp>-<pid>.json`

Purpose:

- make the reasoning dynamics readable in human terms,
- expose conceptual moves, stage handoffs, and artifact-emission moments,
- give generative/IDE-based stages a place to write explicit epistemic interpretation via `ReasoningLogger.surface(...)`.

Format:

- Markdown:
  - run context
  - conceptual dynamics timeline
  - surfaced outputs
- JSON:
  - run metadata
  - context fields
  - outputs
  - ordered surfaced moments with `kind`, `focus`, `significance`, and optional `stage`

## Minimum Logging Expectations per Skill

Each scripted skill should still log:

- parsed input arguments,
- loading/validation summary,
- at least one computed top result or key metric,
- all produced output files via `add_output`,
- final status (`success` or `error`).

If a stage has a richer conceptual interpretation than its operational step titles already capture, it should also add surfaced moments with:

- `ReasoningLogger.surface(...)`

This is especially encouraged for IDE/generative stages where the human-facing epistemic shape matters as much as the raw execution trace.

## Live Display Environment

The interactive `show reasoning` terminal UI uses `rich`, which is declared in
`pyproject.toml` and resolved in `uv.lock` with the other runtime dependencies.

From the repository root, install the locked environment and run the UI with:

```bash
uv sync --locked
uv run python skills/orchestration/show-reasoning/scripts/show_reasoning.py --help
```

## Cross-Stage Correlation

- The orchestrator injects `ABDUCER_RUN_ID` into child stages.
- `ReasoningLogger` records this in both internal and surfaced artifacts.
- This allows exact run-level grouping across all agents and stages.

## Run-Level Indexes

The orchestrator now refreshes two run-level indexes automatically:

- internal log index:
  - `artifacts/<kb-slug>/reasoning-log-index.json`
  - `artifacts/<kb-slug>/reasoning-log-index.md`
- surfaced reasoning index:
  - `artifacts/<kb-slug>/reasoning-surface-index.json`
  - `artifacts/<kb-slug>/reasoning-surface-index.md`

The internal index is for coverage, status, and timeline auditing.
The surfaced index is for conceptual movement, dominant foci, and human-readable reasoning dynamics.

The optional `show reasoning` dashboard reads these surfaced JSON files directly and renders the current epistemic process as a Rich terminal UI. When a surfaced moment carries a PDL payload, the dashboard prioritizes its LaTeX-style notation and material-inference operations.

## Practical Use

Use internal reasoning logs to:

- audit which stage produced which artifact,
- trace failures to exact command and parameters,
- verify stage coverage and output provenance.

Use surfaced reasoning logs to:

- inspect the conceptual movement of a run,
- review how bridge/proof/hardness reasoning is being framed,
- support planning meetings, notebooks, and visualization layers.

## Reading During Debug

Recommended sequence:

1. read the orchestrator internal log first,
2. open the failed or target stage internal log next,
3. inspect the run-level `reasoning-surface-index.md` for the conceptual timeline,
4. inspect stage-local surfaced logs if you need the human-facing per-agent view,
5. inspect output JSON/MD files referenced by the internal log.
