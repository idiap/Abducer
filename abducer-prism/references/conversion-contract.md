<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Conversion contract

This contract defines the behavior of the self-contained `to_prism` conversion
kit. The canonical interface is `bin/to-prism`; skills may interpret evidence
and record decisions, but must not replace its deterministic inspection,
validation, rendering, or comparison operations.

## Invocation boundary

Every command that examines a project takes an explicit `--source`. Every
command that creates or updates conversion state takes an explicit `--output`.
Both paths are resolved before work begins. Their real paths must be disjoint,
including through symlinks. An existing source is always treated as read-only.

The public phases are:

| Command | Reads | May execute source code | Writes |
| --- | --- | --- | --- |
| `inspect` | source files and provider profiles | no | staged inventory and fingerprint under output |
| `baseline` | reviewed baseline descriptor and isolated source copy | only with explicit user authorization | normalized baseline evidence under output |
| `model` | inventory, source text, baseline evidence, reviewed decisions | no | contracts and workflow IR under output |
| `generate` | reviewed conversion IR and decisions | public Prism checks only | a staged generated project and metadata |
| `verify` | source, generated project, reviewed or observed oracles | only explicitly selected test modes | verification evidence and report |
| `convert` | all preceding phase inputs | never native or live execution by default | an atomically published conversion |
| `update` | source, prior lock/base, current output, reviewed decisions | no by default | a staged three-way regeneration or conflict report |

Use `bin/to-prism <command> --help` as the authority for concrete flags. Do not
invent flags or edit intermediate JSON to bypass a failed validation. A dry run
may calculate and report changes, but must not publish them.

## Phase state

Each phase consumes schema-valid artifacts from earlier phases. Facts and
judgments have different states:

- `extracted`: deterministically supported by a source artifact;
- `proposed`: inferred but not accepted;
- `reviewed`: considered by a reviewer, with evidence and alternatives;
- `approved`: authorized for generation when an approval gate applies.

An ambiguous contract, topology edge, custom reasoning method, unsupported
critical behavior, baseline command, or preservation oracle cannot be promoted
silently. Record the choice in `conversion/decisions.json`, including its
evidence and the IDs of artifacts that depend on it. A rejected proposal stays
in the record so that later updates remain explainable.

## Read and execution authority

Inspection parses bytes and metadata only. It must not import project modules,
source shell configuration, invoke package managers, resolve MCP servers, call
models, access a network service, run hooks, or execute discovered scripts.

Native baseline execution is a separate authority grant. Before it runs:

1. show the exact command, working directory, environment-name allowlist,
   timeout, network policy, expected writes, captured artifacts, normalizers,
   and oracle;
2. obtain explicit authorization for that descriptor;
3. copy the declared project scope to an isolated temporary workspace (or use
   an equivalently enforced read-only-source arrangement);
4. omit secret values and ambient credentials unless the user separately
   authorizes named bindings; and
5. retain the before/after source fingerprint as evidence.

Authorization for one descriptor does not authorize discovered alternatives,
retries with changed arguments, package installation, live model calls, or
network access. Stop on the declared timeout or attempt limit and report the
actual outcome.

Verification modes have the same authority boundary. Public `prism check` and
`prism compile` of staged generated source are deterministic generation checks.
Fake-handler runs are executable type smoke tests. Native, networked, or live
provider tests require their own authorization and must be labeled accordingly.

## Source and secret safety

The source fingerprint covers normalized relative path, entry kind, file
bytes, executable bit, and symlink target for every in-scope entry. Profile
exclusions are versioned and recorded. The kit checks the fingerprint after
each phase and after failure paths. This detects persistent mutation; it is not
proof that transient mutation was impossible.

Credential-shaped files, private keys, token-bearing configuration, `.env`
values, and external credential stores are runtime requirements, not assets.
Persist only a redacted path-level disposition. Never copy a secret, include
its value or value-derived hash in stable artifacts, or quote it in a
diagnostic.

## Modeling and generation gates

Model explicit configuration, calls, schemas, command interfaces, hook
contracts, and tests before interpreting prose or file order. Every graph edge
needs source evidence. Unresolved ports stay unresolved until a reviewed choice
defines them.

Canonical `.prism` is the only authoritative final workflow representation.
JSON IR, Markdown reports, and diagrams are evidence or projections. An opaque
adapter around the whole source workflow is not a converted workflow: Prism
must own the topology, contracts, effects, and any epistemic structure. A
source-native implementation may remain behind a typed leaf effect.

Generation is permitted only when all critical mappings needed by the selected
output class are approved or explicitly accepted as conversion debt. It occurs
in staging. The kit then validates schemas, checks and compiles each generated
entry point through the public Prism CLI, verifies dependency locks and source
fingerprints, and publishes atomically. A failure leaves the previous published
output intact.

## Portable and linked outputs

A portable conversion contains canonical `.prism`, all required project-local
modules, the exact supported Prism/Python dependency closure, an offline
bootstrap, and a local launcher. It must work for its declared platform after
the source, converter, Prism checkout, ambient Prism installation, repository
`PYTHONPATH`, and network are unavailable.

A linked conversion also bundles the complete Prism dependency closure but may
depend on named source-native leaf bindings. Those bindings and their authority
requirements are declared. “Linked” never permits an ambient Prism dependency.

Do not publish an output as portable when a required wheel, module, license
disposition, platform match, input boundary, or runtime effect handler is
missing.

## Failure and publication rules

Fail closed for path overlap, a changing source tree, schema/version mismatch,
unknown incompatible profile or lock versions, missing dispositions, dangling
graph references, unbounded loops, invalid reasoning assurance, dependency
hash mismatch, required unsupported runtime behavior, Prism check/compile
failure, or an update conflict in a generated file.

Absence of a baseline is not itself a converter failure. Record it as
`unavailable` or `not_tested` and cap preservation claims. Flaky and nonzero
baselines are evidence, not grounds to normalize away meaningful differences.

Publication requires:

- a complete inventory disposition for the declared scan scope;
- schema-valid conversion artifacts and lock metadata;
- no unresolved critical decision hidden from the report;
- checked/compiled generated entry points;
- a verified dependency closure for the claimed output class;
- unchanged source fingerprints; and
- preservation claims no stronger than the evidence permits.

## Incremental updates

`update` re-inventories the source and compares semantic artifacts, not only
file hashes. Reuse a decision only if all evidence and dependencies that made
it valid are unchanged. Regenerate into staging using the content-addressed
prior generated base. Preserve user-owned files. If both the new generator and
the user changed the same generated region, emit a conflict and do not publish.

An identical source fingerprint, profile set, decisions hash, template version,
converter version, and Prism capability identity must reproduce byte-identical
canonical sources, normalized manifests, and lock content. Raw logs containing
timestamps, invocation IDs, or temporary paths are excluded from this claim.
