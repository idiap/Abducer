<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Generated output contract

The generated output is an independently inspectable Prism project plus the
evidence that produced it. Canonical `.prism` files are the sole authoritative
workflow representation. Conversion JSON and reports do not execute the
workflow and cannot replace those sources.

## Required shape

```text
<output>/
├── prism_project/
│   ├── types.prism
│   ├── occurrences.prism           # abstract epistemic operation signatures
│   ├── reasoning.prism             # only for genuine epistemic topology
│   ├── relations.prism             # only when domain relations are needed
│   ├── materialization.prism
│   ├── main.prism
│   ├── generated/                  # public Prism skill/hook build outputs
│   ├── adapters/                   # optional thin leaf-effect packages
│   ├── prism_modules/              # exact project-local module closure
│   ├── vendor/
│   │   ├── wheels/
│   │   ├── manifest.json
│   │   ├── sbom.json
│   │   └── licenses/
│   ├── pyproject.toml
│   ├── dependency.lock
│   ├── bootstrap.sh
│   ├── prism
│   └── tests/
├── source_snapshot/                # optional allowlisted vendored mode
├── conversion/
│   ├── inventory.json
│   ├── contracts.json
│   ├── workflow.json
│   ├── reasoning-map.json
│   ├── decisions.json
│   ├── to-prism.lock.json
│   └── report.md
└── run.sh                          # or an equivalent portable launcher
```

Omit conditional source modules rather than emitting empty placeholders. Every
import, declaration, generated module, adapter, fixture, and dependency must
have a consumer or recorded reason.

## Prism module ownership

- `types.prism` owns nominal domain inputs, outputs, errors, and policies.
- `occurrences.prism` owns pure generative operation signatures and meaningful
  semantic join types; every converted epistemic occurrence returns
  `Generated[T]`.
- `reasoning.prism` owns only imports, concise comments, and the high-level
  epistemic composition. It declares no types or relations.
- `relations.prism` owns substantial relation and certificate contracts.
- `materialization.prism` owns functions, agents, skills, tools, effects,
  failures, permissions, relation builders, concrete workflow topology, and
  the explicit occurrence-by-occurrence implementation of any reviewed
  reasoning projection.
- `main.prism` owns application wiring and exposes the useful typed result.
- `material_main.prism` conditionally preserves the detailed mixed material
  pipeline when `main.prism` exposes an approved high-level reasoning
  projection.

Not every workflow needs reasoning or relation modules. Operational workflows
remain ordinary Prism functions/workflows. Source scripts may implement named
typed leaf effects, but `.prism` must own orchestration. Generated sources must
contain no credentials, absolute source paths, machine-specific commands, or
provider secrets.

Reasoning occurrences and skills have a many-to-many relationship. Generated
materialization may attach several reviewed skills to one occurrence or reuse
one skill across occurrences. The plan must record `granularity_rationale` for
each occurrence; renderer output must never infer reasoning count from skill,
file, prompt, or agent count.

For every projected reasoning occurrence, materialization must emit a concrete
implementation with the exact abstract input/output signature, compile the
deduplicated reviewed skills identified through its `material_steps`, attach
every required relation builder, and instantiate the named reasoning workflow.
A plan-only cross-reference or a collection of low-level hook agents is not a
materialization of the high-level reasoning graph.

Until the public Prism CLI supports general typed domain-input injection, emit
one canonical `.prism` fixture harness per workflow/fixture. A general launcher
may claim variable-input support only when it validates a nominal schema and
passes the value through a supported public Prism boundary.

## Dependency closure

Resolve dependencies from generated imports, CLI commands, effects, handlers,
adapters, and declared target platform. Bundle only the public Prism
distributions and standard/project modules that are transitively required,
plus exact third-party wheels. Conversion-only and experimental platform
packages are excluded unless generated runtime behavior demonstrably needs
them.

For every bundled artifact record name, version, hash, source identity,
platform/Python tags, transitive requirements, license disposition, and SBOM
relationship. Do not copy arbitrary files from a checkout or developer
environment. Reject missing or incompatible wheels unless a complete,
explicitly tested offline source-build toolchain is included.

`bootstrap.sh` creates a project-local environment using only bundled,
hash-locked artifacts with indexes and dependency fallback disabled. The local
`prism` launcher selects only that environment, sets the generated project as
workspace root, and must not consult ambient packages, the converter, the
original checkout, or a network index.

## Portable versus linked

A portable output declares its supported Python/OS/architecture target set and
passes a clean-room relocation test after removing source/converter/checkout
access, clearing repository paths, disabling the network, and excluding ambient
Prism. All required leaf implementations and Prism dependencies are bundled.

A linked output meets the same Prism dependency rule but declares named
external source-native leaf bindings. Its manifest records their contracts,
versions, and authority requirements. It must not be labeled portable and must
not hide source-native orchestration behind a leaf binding.

## Determinism and ownership

Canonical generated sources, normalized manifests, reports derived solely from
stable data, and lock content are byte-identical for identical source,
profiles, decisions, converter/template versions, and Prism capability
identity. Stable artifacts contain normalized relative paths, never temporary
or absolute source paths. Raw logs with timestamps or invocation IDs are
separate run evidence.

The lock records source fingerprint, profile versions, converter and template
versions, decisions hash, Prism capability identity, dependency hashes,
generated-file ownership, and generated-file hashes. Retain a
content-addressed prior generated base (or reproducible equivalent) for
three-way updates. User-owned files are never overwritten. Divergent generated
files produce conflicts instead of silent replacement.

## Required validation

Before publication:

1. validate every conversion and vendor manifest against its shipped schema;
2. ensure every discovered element has a disposition;
3. check every generated `.prism` module and compile every entry point through
   the public project-local Prism CLI;
4. run fixture harnesses selected by the reviewed policy, labeling fake-handler
   runs only as executable type smoke evidence;
5. verify dependency hashes, import closure, platform tags, licenses, SBOM, and
   executable modes;
6. rerun source fingerprint comparison;
7. calculate preservation per workflow under `preservation-policy.md`; and
8. publish staging atomically only if all selected gates pass.

Portable publication additionally requires offline bootstrap, relocation,
check, compile, selected run, and offline verification tests with ambient
resolution unavailable. Removing any declared required dependency must fail
the closure test with an actionable diagnostic.

## Report and lock semantics

The report names output class and target platforms; identifies every workflow,
decision, unsupported construct, and external binding; links preservation
claims to machine-readable evidence; distinguishes smoke/integrity results from
equivalence; and gives a publication decision. It never claims “equivalent”
without naming the level and oracle.

The lock is build identity, not a dump of CLI output. Absolute paths,
timestamps, invocation IDs, and artifact-directory locations are normalized or
excluded. Unknown incompatible lock, schema, profile, or template versions are
rejected rather than guessed.
