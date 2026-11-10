<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# API Key Configuration

Abducer can run provider-backed branches through local API keys stored under this `config/` directory. Secret-bearing files are ignored by git.

API keys are only an execution backend. They do not replace Abducer skills, skill dispatch, target-navigation gates, obligation gating, or report validators. A provider-backed run should still route through the same skills and record the same `skill_dispatch_trace`; the API key simply lets a branch engine call a model through the configured provider.

Create either:

```bash
cp config/api_keys.example.json config/api_keys.json
```

or:

```bash
cp config/api_keys.example.env config/api_keys.env
```

Then fill in the real key locally. Do not commit `config/api_keys.json` or `config/api_keys.env`.

The default loader checks, in order:

1. `config/api_keys.json`
2. `config/api_keys.env`
3. existing process environment variables

For OpenAI-compatible runs, set `OPENAI_API_KEY`. Optional fields such as `OPENAI_ORG_ID`, `OPENAI_PROJECT_ID`, and `OPENAI_BASE_URL` are supported.

For Azure OpenAI / Azure AI Foundry OpenAI-compatible v1, use provider `azure_openai`. Store both the base endpoint and the full Responses endpoint:

```json
{
  "active_provider": "azure_openai",
  "providers": {
    "azure_openai": {
      "env": {
        "AZURE_OPENAI_API_KEY": "replace-with-local-key",
        "AZURE_OPENAI_ENDPOINT": "https://your-resource.services.ai.azure.com/openai/v1",
        "AZURE_OPENAI_RESPONSES_ENDPOINT": "https://your-resource.services.ai.azure.com/openai/v1/responses",
        "AZURE_OPENAI_MODEL": "your-deployment-or-model",
        "AZURE_OPENAI_REASONING_EFFORT": "high",
        "OPENAI_API_KEY": "replace-with-local-key",
        "OPENAI_BASE_URL": "https://your-resource.services.ai.azure.com/openai/v1",
        "OPENAI_MODEL": "your-deployment-or-model",
        "OPENAI_REASONING_EFFORT": "high",
        "AZURE_OPENAI_MAX_OUTPUT_TOKENS": "6000",
        "AZURE_OPENAI_API_TIMEOUT_SECONDS": "900"
      }
    }
  }
}
```

The loader maps `AZURE_OPENAI_API_KEY` to `OPENAI_API_KEY`, `AZURE_OPENAI_ENDPOINT` to `OPENAI_BASE_URL`, `AZURE_OPENAI_MODEL` to `OPENAI_MODEL`, and `AZURE_OPENAI_REASONING_EFFORT` to `OPENAI_REASONING_EFFORT` when those OpenAI-compatible variables are not already set.

For long-horizon discovery runs, `AZURE_OPENAI_MAX_OUTPUT_TOKENS` and `AZURE_OPENAI_API_TIMEOUT_SECONDS` tune throughput without changing the skill system. Keep reasoning effort at `high` for production discovery, but prefer a bounded output budget such as `6000` so the API branch returns compact mathematical packets instead of timing out or emitting oversized malformed JSON while trying to over-elaborate.

API-backed marathon cycles can run independent branch agents in parallel while
keeping scheduler merge, branch memory, reports, and next-queue synthesis as a
single serialized write. Configure this either from the CLI or local config:

```json
{
  "AZURE_OPENAI_MAX_CONCURRENT_BRANCHES": "3",
  "AZURE_OPENAI_BRANCH_REQUEST_SPACING_SECONDS": "2"
}
```

Use parallelism only when the selected branches are genuinely independent
interpretive tasks. A failed worker makes the whole cycle operationally failed;
successful branch packets from that attempt are recorded in the error record
but are not merged into durable state until all selected packets validate.

Validate the setup without revealing secrets:

```bash
python agentic/scripts/validate_api_key_config.py
```

## PMP Scientific Environment

The parsimonious probe layer uses the project's uv environment for exact
symbolic algebra and tiny bounded numeric probes. From the repository root:

```bash
uv sync --locked
uv run python agentic/scripts/validate_symbolic_matrix_probe.py
```

`pyproject.toml` declares `sympy`, `numpy`, and `scipy`; `uv.lock` records their
resolved versions. Symbolic builders keep exact formula fallbacks and bounded numeric
probes keep pure-Python grids where practical. QuTiP is intentionally not part
of the current PMP foundation because the active carrier is finite matrix
algebra, quotient holonomy, and analytic estimates rather than open quantum
system dynamics.

The equational/symbolic reasoning layer uses the same uv environment.
SymPy is preferred when available, but finite-interface builders include manual
fallback formulas for the current quotient determinant and holonomy packet.
Lean, Lake, mathlib, and theorem-prover proof checking are intentionally
excluded from this phase.
