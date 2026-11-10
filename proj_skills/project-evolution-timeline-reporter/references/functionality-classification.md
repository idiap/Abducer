<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Functionality Classification

Use these labels when summarizing commit history into milestone themes.

| Label | Strong Signals |
| --- | --- |
| Reasoning and orchestration | `skills/orchestration/`, `skills/control-plane/`, `agentic/`, `workflow`, `router`, `proof queue` |
| Mathematical discovery and proof | `skills/discovery/`, `KB/`, `InformalMathLib/`, `phyp/`, `conjecture`, `proof` |
| Skill architecture | `skills/`, `proj_skills/`, `skill`, `catalog`, `meta`, `router` |
| Reporting and visualization | `report`, `html`, `visualizer`, `workbench`, `dashboard`, `timeline` |
| Test and validation | `tests/`, `test`, `validation`, `regression`, `parity`, `smoke` |
| Knowledge and evaluation assets | `KB/`, `InformalMathLib/`, `phyp/`, `agentic/evals/`, `example`, `benchmark` |
| Integrations and runtime surfaces | `.claude`, `.opencode`, `mcp`, `sdk`, `api`, `http`, `server` |
| Executable evidence | `script`, `trace`, `evaluation`, `fixture`, `execution` |
| Source intake and normalization | `ingest`, `source`, `latex`, `parser`, `normalizer` |

Prefer the most specific label when several match. If several labels are genuinely active, keep the top two in the report.
