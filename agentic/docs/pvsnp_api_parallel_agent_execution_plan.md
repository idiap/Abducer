<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# P vs NP API Parallel Agent Execution Plan

This plan defines the safe parallel boundary for P vs NP discovery marathons.
Parallelism is allowed only for independent branch interpretation calls. It is
not allowed for scheduler mutation, branch memory writes, run-state updates,
report generation, or queue synthesis.

## Execution Boundary

The parallel region begins after the scheduler has selected branches and ends
before the cycle packet is assembled. Each worker receives a frozen copy of one
branch, the cycle index, the per-branch budget, and the API configuration. Each
worker returns exactly one validated branch-output packet plus one execution
record.

The serialized region then:

- restores the scheduler order of branch outputs;
- rejects the whole cycle if any worker failed or returned invalid content;
- writes branch memory only after every selected branch has validated;
- builds `parallel_synthesis` as a reducer over completed branch packets;
- writes the cycle JSON/Markdown and rebuilds reports.

## P vs NP Branch Diversity

Parallel workers should not spend one cycle restating the same pressure in
three voices. The scheduler now tags P vs NP branches by pressure family:

- hardness magnification and quantitative threshold transfer;
- barrier and impossibility control;
- MCSP/MKtP and meta-complexity carriers;
- proof-complexity transfer;
- quantifier, uniformity, and nonuniform-advice lifting;
- Gedanken or finite-case intuition labs.

The selector prefers distinct pressure families before filling remaining slots.
This keeps parallelism epistemically useful: one cycle can compare an exponent
window, a carrier-transfer object, and a barrier/no-go pressure instead of
duplicating one route.

## Reducer Contract

`parallel_synthesis` is the expert-facing merge layer. It must cite the selected
branch IDs in scheduler order and state:

- common proof obligations;
- cross-branch conflicts;
- no-go or impossibility opportunities;
- queue promotions with pressure family, cited branch IDs, next analysis, and a
  promotion test.

For P vs NP, the reducer looks for concrete obligations such as beta/exponent
windows, MCSP explicitness, advice leakage, natural-proof pressure,
relativization/algebrization pressure, and all-exponent quantifier lifting.

## CLI and Config

Per-cycle runner:

```bash
python agentic/scripts/run_discovery_marathon.py \
  --resume \
  --target p-vs-np-target \
  --execution-mode research \
  --branch-engine api \
  --max-active-branches 3 \
  --parallel-branches \
  --api-max-workers 3 \
  --api-request-spacing-seconds 2
```

Time-boxed job wrapper:

```bash
python agentic/scripts/run_discovery_marathon_job.py \
  --target p-vs-np-target \
  --duration-seconds 7200 \
  --branch-engine api \
  --max-active-branches 3 \
  --parallel-branches \
  --api-max-workers 3 \
  --api-request-spacing-seconds 2
```

Equivalent local config keys:

- `AZURE_OPENAI_MAX_CONCURRENT_BRANCHES`
- `AZURE_OPENAI_BRANCH_REQUEST_SPACING_SECONDS`
- `OPENAI_MAX_CONCURRENT_BRANCHES`
- `OPENAI_BRANCH_REQUEST_SPACING_SECONDS`

## Validation

The core cycle validator checks parallel order and reducer fields whenever a
cycle includes `parallel_execution`. The focused validator
`agentic/scripts/validate_parallel_api_marathon.py` validates compact fixtures
for the enabled-parallel contract and is part of `agentic_check.py`.

Failure policy is conservative. If any worker fails, the cycle attempt fails
operationally. Successful worker packets from the same attempt may appear in
the error record for diagnosis, but they are not merged into durable state.
