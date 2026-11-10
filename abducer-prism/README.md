<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# to_prism

`to_prism` converts reviewed Codex, Claude, OpenCode, and Open Agent Skill
projects into canonical, typed `.prism` projects. The external source tree is
treated as read-only. JSON inventories, decisions, reports, adapters, and
launchers are supporting evidence; they never replace the generated `.prism`
workflow.

## Run after transferring

Unzip the folder, enter it, and run the built-in diagnostic. Installation is
not required:

```sh
cd to_prism
./bootstrap
./to-prism doctor
./to-prism --help
```

`bootstrap` installs the bundled, hash-locked wheels into a folder-local
`.venv` using `--no-index`. The archive includes `to-prism`, the Prism CLI,
language, runtime, stdlib, transpiler, SDK, Codex/LiteLLM/Python adapters, and
their complete third-party dependency closure. It does not consult PyPI or the
original Prism checkout.

`doctor` validates the packaged profiles and schemas and reports whether a
compatible public `prism` executable is available. Use
`./to-prism doctor --require-prism` when Prism must be present before testing a
conversion.

## Understand the types and layers

Start with [`references/type-taxonomy.md`](references/type-taxonomy.md) for the
full type map: ordinary data, provenance, assurance, reasoning methods,
relations, workflows, capabilities, and effects. The central rule is that a
conversion retains the weakest honest type—generated output is not evidence,
material support is not proof, and successful execution is not equivalence.

[`references/layers.md`](references/layers.md) explains both architectures:

- the conversion pipeline from read-only source discovery through reviewed
  canonical `.prism` and preservation evidence; and
- the generated project's domain, reasoning, relation, materialization,
  application, adapter, and runtime layers.

The bundled [`examples/`](examples/README.md) include a checked type gallery, a
runnable layered release-review workflow, and a minimal provider-native project
that can be converted end to end using the packaged dependency closure.

For a new project, invoke `to-prism-derive-types`. It builds a validated,
source-anchored `project-semantic-taxonomy` and an approved `generation-plan`
before rendering is allowed. The procedure is specified in
[`references/semantic-typing-protocol.md`](references/semantic-typing-protocol.md),
with machine-readable induction candidates in
[`references/semantic-taxonomy.json`](references/semantic-taxonomy.json).
Examples may propose a shape, but only evidence in the target project can
justify a selected name, field, reasoning operation, critic, or assurance.
The derivation deliberately uses a type budget: it starts from example-visible
workflow ports and splits additional types only for separately consumed,
validated, branched, or differently assured values. Retrieval, database,
informal-argument, and SymPy/LaTeX seeds are included without imposing a large
universal ontology.

Reasoning granularity is not skill granularity. The derivation records a
many-to-many map: one epistemic occurrence may compose several skills, and one
skill may contribute to several occurrences. It splits only at independently
consumed/reviewed/criticized outputs, branch/join boundaries, or
provenance/assurance changes, and requires a `granularity_rationale` for every
occurrence. In the `to_prism` conversion profile every epistemic occurrence is
generative—`ExactInput -> Generated[ExactOutput]`. Retrieval, deterministic
computation/validation, assurance construction, and effects remain explicit
material operations.

## Optional installation

```sh
python3 -m venv .venv
.venv/bin/python -m pip install .
```

Installing creates the same `to-prism` console command as the root launcher.

## Conversion lifecycle

```sh
./to-prism inspect --source /external/project --output /separate/conversion
./to-prism model --source /external/project --output /separate/conversion
# Run the bundled to-prism-derive-types skill and review its taxonomy and plan.
./to-prism validate /separate/conversion/project-semantic-taxonomy.json \
  --schema project-semantic-taxonomy
./to-prism validate approved-plan.json --schema generation-plan
./to-prism baseline --source /external/project --output /separate/conversion
# Review conversion/decisions.json and an explicit generation plan.
./to-prism generate \
  --source /external/project \
  --output /separate/conversion \
  --plan approved-plan.json \
  --handler fake
./to-prism verify --source /external/project --output /separate/conversion --portable
```

Generation and verification enforce the same plan-bound layer contract. An
operational workflow cannot contain `reasoning.prism`; a mixed workflow emits
one only when its approved plan contains an explicit high-level
`reasoning_projection`. Abstract signatures live in `occurrences.prism`, edge
contracts in `relations.prism`, and `reasoning.prism` contains only imports,
comments, and the core topology. `materialization.prism` explicitly binds each
projected occurrence and relation to typed implementations and their reviewed
skill composition. For a projected mixed workflow, `main.prism` exercises that
human-scale reasoning binding while `material_main.prism` retains the detailed
operational/material pipeline as a separate supporting entrypoint.
The generation record binds the package version, reviewed-plan digest, and
canonical Prism source hashes. A hand-rendered or subsequently altered project
cannot claim package-generated conformance merely because it compiles.

Portable generation is the default. It builds the required Prism
distributions from `--prism-source` when supplied, or reuses this archive's
prebuilt Prism closure otherwise. It writes the selected closure into
`prism_project/vendor/wheels`, hashes every wheel in `dependency.lock`, emits a
CycloneDX SBOM, and creates relocation-safe `bootstrap.sh` and `prism`
launchers. Bootstrap uses `--no-index --require-hashes`; generated projects do
not need the Prism source checkout. Supplying `--wheelhouse` avoids network
resolution. `--development-no-bundle` is an explicit non-publishable escape
hatch. The bundled binary wheels target the Python/OS/architecture recorded in
`vendor/manifest.json`; bootstrap and generation fail closed on a mismatch.

## Evidence boundaries

- `prism check` and `prism compile` establish typed structural evidence.
- `prism run --handler fake` is an executability smoke test for `AI.Generate`.
- `verify-run --mode offline` verifies records and artifact integrity, not
  workflow replay.
- Behavioral and trace preservation require an independent native oracle.
- OpenCode executable plugins, dynamic model-selected tools, MCP, process,
  network, and file/data-write effects remain explicit unsupported debt unless
  a reviewed typed leaf adapter exists.
- Codex hook activation is limited to self-contained `PATH` commands in the
  adapter's isolated working directory. Claude hooks are structurally
  representable but have no public runtime handler.

See `references/` for the full conversion contract, preservation policy,
reasoning-extension protocol, type taxonomy, layer model, provider matrix, and
generated-output contract.
