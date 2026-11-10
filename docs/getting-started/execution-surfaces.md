<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->

# Choosing an execution surface

This guide is for researchers deciding how to enter Abducer. Both surfaces preserve
claim boundaries, but they consume different inputs and control different state.
Do not infer that a successful stage in one authorizes a state transition in the other.

## KB theorem assistance

Use this surface when the input is a structured problem KB and the immediate task is
statement connection, hypothesis formation or evaluation, proof planning, or maintaining
proof obligations. The deterministic orchestrator lives under
`skills/orchestration/kb-orchestrator/`. Its older abductive loop retains prompt-driven
checkpoints rather than providing a fully autonomous discovery engine.

```bash
uv run python skills/orchestration/kb-orchestrator/scripts/run_orchestrator.py --help
```

The [KB pipeline guide](kb-theorem-assistance.md) preserves the full command template,
ingestion example, artifact layout, and evidence boundaries. Some modes write canonical
`artifacts/<kb-ref>/` paths: inspect the [orchestration contract](../architecture/orchestration.md)
before executing them in a working research tree.

## Canonical theory-first discovery

Use this surface when evolving typed conceptual research state. Candidate generation,
branch maturation, evaluation, reflection, receipt validation, and semantic reduction
lead to an exact, single-writer state commit. Proof and delayed descendant experiments
remain separate post-commit lanes; they do not inherit theory-selection authority.

```bash
uv run python agentic/scripts/run_canonical_discovery_cycle.py --help
```

The command requires `--request` and `--state-root`. Its optional `--workspace` selects
the artifact trust boundary and `--output` writes a result projection. A request must
contain the required exact identities, role bindings, and validated operator evidence;
this is not a free-form prompt endpoint. The authoritative state is the transaction
store, not a copied `latest` report or optional output JSON.

See the [CLI reference](../reference/cli-reference.md#canonical-discovery-runtime),
[named workflow guide](../architecture/named-workflows.md),
[discovery operations](../operations/discovery-marathon-operations.md), and
[publication contract](../architecture/canonical-discovery-publication.md).

## Choose and interpret a result

For example, connecting statements in `KB/p-vs-np.kb.md` belongs to theorem assistance;
committing an evaluated family of conceptual systems belongs to the discovery runtime.
A hypothesis, a branch failure, a proof obligation, a compiler result, and a state
commit are different outputs. Neither passing a workflow gate nor retaining a theory
establishes a proof of P vs NP or Yang–Mills.

Start from the [installation guide](README.md) and use the
[detailed project guide](../guides/project-guide.md) for the full conceptual cycle.
