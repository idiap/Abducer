<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# `to_prism`: repository interpretation and implementation backlog

Status: design proposal; no converter implementation exists yet.

**Resolved target:** the final converted workflow is canonical, checked,
executable `.prism` source. Provider-neutral JSON, reports, catalog records, and
diagram YAML are intermediate evidence or optional visualizations; none of them
counts as a completed conversion.

**Resolved deployment rule:** a portable conversion also carries its complete
Prism dependency closure inside the generated project. This includes the exact
public Prism distributions, required standard `.prism` library modules, selected
effect adapters, and locked transitive packages needed to check, compile, and
run the generated source. No separately installed Prism checkout is required.

This document defines a self-contained conversion kit that can inspect an
external Codex, Claude, OpenCode, or Open Agent Skills project without changing
it, recover its skills, hooks, tools, workflows, and reasoning intent, and emit
a separately runnable Prism project plus evidence about what was and was not
preserved.

The intended root is `to_prism/`. Everything needed to inspect, model, render,
and test a conversion belongs below that root. The kit may invoke the public
`prism` CLI as a toolchain, but it must not import private modules or read
templates, schemas, prompts, or implementation instructions from elsewhere in
this repository at conversion time.

## 1. Interpretation of the current repository

### 1.1 Supported Prism execution architecture

The active, documented execution path is:

```text
authored .prism source
  -> prism.language: parse, resolve, type-check, elaborate, compile
  -> backend-neutral command/workflow IR
  -> prism.runtime: execute typed workflows and effects
  -> optional effect adapters: Codex, LiteLLM, or installed Python
  -> typed result, trace, artifacts, and offline/live replay
```

The repository deliberately separates responsibilities:

- `packages/prism-language` owns syntax, types, checking, reasoning and workflow
  IR, evidence, verification, and the trusted kernel. It is provider-free.
- `packages/prism-transpiler` imports one Open Agent Skill or one native
  Codex/Claude hook configuration into a checked standalone Prism module.
- `packages/prism-runtime` executes compiled IR and records typed traces.
- `packages/prism-adapter-*` implement optional effect boundaries. Codex and
  LiteLLM handle `AI.Generate`; Python uses named `Python.Call` entry points.
- `packages/prism-sdk` resolves workspace modules and installed libraries.
- `packages/prism-cli` exposes the supported `parse`, `check`, `compile`,
  `run`, `verify-run`, `build skill`, and `build hooks` commands.
- `packages/prism-platform` contains experimental catalog, diagram, capability,
  and imported-skillset models. The root README explicitly excludes it from the
  supported execution path.
- `libs/prism` supplies the standard epistemic method and relation contracts.
- `examples/language` is the executable source of truth for current syntax.
- `.codex/skills` contains four repository-authoring skills that already
  separate epistemic topology, materialization, Python adapters, and end-to-end
  Prism program writing.

That layering must remain intact. The conversion kit should consume public CLI
contracts and produce ordinary Prism source; it should not place conversion
logic in `prism.language`, teach the runtime about vendor project layouts, or
make the language depend on the platform catalog.

### 1.2 Prism concepts that the conversion must target

A complete conversion is more than embedding prompts:

- A `reasoning` declaration represents pure epistemic intent. It contains
  occurrences, typed relations, and `sequence`, `parallel`, `choice`, or
  bounded `repeat` topology. It contains no provider, prompt, command,
  permission, effect, or failure choice.
- A materialized `workflow` provides executable functions, agents, relation
  builders, adapters, effects, failures, and capabilities for that topology.
- An `agent` is a typed callable with persistent and invocation-local tools,
  skills, and hooks.
- `Skill[Task]` is invariant in its task contract. A converter must infer or ask
  for a real task type rather than assigning every skill to `String`.
- `Hooks[Codex]` and `Hooks[Claude]` are provider-specific typed artifacts.
- Existing scripts belong behind typed tools or a `Python.Call` boundary; they
  cannot safely be smuggled into a skill artifact.
- `Generated`, `Evidence`, `Computed`, `Supported`, `Validated`, `Proof`, and
  `Verified` are different provenance or assurance states. Conversion must not
  strengthen one into another.
- Custom reasoning methods are project-local semantic function contracts. They
  are not aliases for shell commands, prompts, agents, or control-flow labels.

### 1.3 Existing conversion-related capability

The current transpiler is a useful narrow primitive, not a whole-project
scanner or a security boundary:

- It recursively discovers `SKILL.md` files.
- It validates Open Agent Skill frontmatter.
- It embeds non-script, non-symlink resource bytes in a source-independent
  generated module that still imports a caller-owned task contract.
- It rejects a finite set of credential/script shapes, empty instructions,
  unsupported skill fields, unknown hook events, and unsupported hook handler
  shapes. It does not reject every unknown top-level hook-configuration field;
  fields other than `hooks` and `description` can be omitted by the builder and
  therefore need converter-side disposition checks.
- It builds one typed `Skill[Task]` after the caller supplies a qualified Prism
  task contract.
- It builds one typed native Codex or Claude hook configuration.
- It type-checks generated source before writing it.

The language/runtime already verifies skill task types, hook providers, tool
callable contracts, invocation-local capability scoping, and agent execution.
The Codex adapter materializes built hooks in an isolated temporary directory
for each generation effect.

It builds exactly one skill or exactly one hook-containing configuration per
invocation. Skill resources are embedded as base64 payloads for model context;
their executable mode and native on-disk resource behavior are not preserved.

The platform layer also has an older, richer `ImportedSkillSpec` model with
preserved assets, runtime profiles, workspace mounts, command arguments, and
manual invocation contracts. It contains valuable vocabulary, but it is
experimental, includes project-specific inference, and does not itself produce
canonical executable Prism programs. It should inform the neutral inventory
schema, not become the converter's runtime dependency.

### 1.4 Gaps between the repository and the requested end-to-end conversion

The current implementation does not yet:

- inspect a whole external project as one unit;
- recognize vendor layouts through versioned Codex, Claude, and OpenCode
  profiles;
- discover entry points, commands, agents, subagents, MCP dependencies,
  permissions, environment requirements, or cross-skill calls;
- infer task, input, output, error, effect, or permission contracts;
- recover workflow topology or distinguish orchestration from epistemic intent;
- map operations to standard Prism reasoning methods and relations;
- create project-local reasoning method extensions when the standard eight are
  insufficient;
- turn scripts into typed tools or Python effect adapters;
- generate a complete canonical `.prism` program, normally split into
  `reasoning.prism`, `materialization.prism`, and `main.prism`;
- establish a native baseline or compare native and Prism behavior;
- prove that the source tree was not modified;
- record source hashes, decisions, losses, unsupported constructs, or a stable
  update mapping;
- convert incrementally after the upstream project changes;
- support OpenCode hooks or an OpenCode runtime provider;
- execute Claude hooks through a Prism model adapter. The transpiler can type
  and package them, but the currently available model runner that activates
  native hooks is Codex-specific.

There are also current repository consistency issues that the new kit must not
copy into its own design:

- The README and tutorial refer to `CORE_PRINCIPLES.md`, `SYNTAX.md`,
  `docs/history/projects`, and numerous canonical examples that are absent from
  the current tracked checkout.
- The four `.codex/skills` refer to ignored `notes/` documents that are not in
  the tracked repository.
- The README recommends authored `.prism` files under `.prism/`, while
  `test_repository_layout.py` permits only runtime state there in this
  repository.
- Platform diagram YAML and typed `.prism` workflows overlap conceptually but
  are not one execution contract.

Therefore `to_prism` must version and ship its own contracts and templates. It
must test against the actual public CLI rather than depend on prose or missing
files.

## 2. Product boundary and invariants

### 2.1 Definition of done

Given explicit `--source` and `--output` paths, the completed kit must:

1. fingerprint and inventory the declared semantic/source scope of the external
   project without executing it;
2. optionally run user-approved native baseline commands in an isolated test
   workspace;
3. normalize vendor artifacts into a provider-neutral conversion IR;
4. infer contracts and workflow topology, marking every uncertain inference;
5. map epistemic steps to standard or justified project-local reasoning types;
6. generate a complete, checked canonical `.prism` project in the output path,
   including its locally deployable Prism toolchain/runtime dependency closure;
7. run structural, type, compile, fixture, and differential preservation tests;
8. emit a machine-readable manifest and a human-readable conversion report;
9. detect no change to any in-scope source path, type, bytes, executable mode,
   or symlink target between stable before/after snapshots; and
10. support a later re-scan and controlled regeneration without overwriting
    manual edits silently.

### 2.2 Non-negotiable invariants

- **Source is read-only.** The converter opens the source read-only where the OS
  permits. Any executable baseline or verification runs against an isolated
  copy or read-only mount, never the original. Hooks are defense in depth;
  before/after fingerprints detect changes but are not an enforcement boundary
  or proof that no transient mutation occurred.
- **Output is separate.** Source and output roots must not overlap. Symlink and
  real-path containment checks must fail closed.
- **No implicit execution.** Discovery parses files only. Commands, hooks,
  scripts, package installation, network calls, and live model calls require a
  distinct execution phase and explicit authorization.
- **No secret capture.** Credential-shaped files, private keys, `.env` values,
  token-bearing configurations, and external credential stores are represented
  as required runtime bindings, never copied or logged.
- **No silent semantic strengthening.** Generated text is not evidence;
  evidence is not validation; material support is not proof.
- **No silent loss inside the declared scan scope.** Every discovered source
  element is mapped, preserved as an opaque asset, explicitly excluded, or
  recorded as conversion debt. Profile exclusions for VCS data, dependency
  caches, and build products are versioned and listed in the manifest.
- **Determinism before generation.** Parsing, hashing, graph construction,
  rendering, and comparison are scripts with schemas. Skills make semantic
  decisions only where deterministic extraction is insufficient.
- **Public boundary only.** The kit may invoke the public `prism` executable via
  `parse`, `check`, `compile`, `run`, `verify-run`, `build skill`, and
  `build hooks`; it must not import Prism Python modules or depend on
  undocumented in-process APIs.
- **Dependencies travel with portable output.** The generator resolves the
  minimal feature-driven Prism package/module closure, builds or acquires exact
  distributable artifacts through declared public packaging contracts, and
  places them in the generated project. It never copies arbitrary files from a
  developer environment or relies on ambient site packages.
- **Offline reproducibility.** A portable project bootstraps and runs from its
  bundled dependency artifacts with network access disabled. Every artifact has
  a version, hash, source identity, license disposition, and dependency record.
- **Provider facts are versioned.** Vendor layouts and hook event matrices live
  in explicit profiles with provenance and fixture coverage.
- **Idempotent regeneration.** Identical source, profile, decisions, and tool
  version produce byte-identical generated files.
- **Manual work is protected.** Generated files carry ownership in the lock
  manifest. User-owned files are never overwritten; divergence becomes a
  three-way-update task.

### 2.3 Preservation levels

The report must classify each claim rather than use one vague “equivalent”
label:

| Level | Meaning | Minimum evidence |
| --- | --- | --- |
| Asset | Original instructions/resources are preserved | path and content hash mapping |
| Structural | Skills, hooks, nodes, edges, conditions, and entry points correspond | graph and inventory coverage |
| Contract | Inputs, outputs, failures, effects, permissions, and providers correspond | schema/type checks and mapping records |
| Trace | Equivalent fixtures traverse corresponding logical stages | normalized native/Prism traces |
| Behavioral | Observable outputs satisfy the same declared oracle | differential or property tests |
| Epistemic | Reasoning roles, relations, provenance, and assurance are preserved | reviewed reasoning map and Prism checks |

For nondeterministic model behavior, exact output equality is normally an
invalid oracle. Use schema conformance, invariant/property checks, recorded
replay, deterministic fake handlers, and trace correspondence. Live statistical
comparison is optional evidence and must never be reported as proof of
equivalence.

## 3. Proposed self-contained layout

```text
to_prism/
├── todos.md
├── VERSION
├── skills/
│   ├── to-prism/SKILL.md
│   ├── to-prism-baseline/SKILL.md
│   ├── to-prism-model-workflows/SKILL.md
│   ├── to-prism-map-reasoning/SKILL.md
│   ├── to-prism-review-preservation/SKILL.md
│   └── to-prism-update/SKILL.md
├── integration-hooks/          # defense-in-depth hooks for the converter
│   ├── codex/hooks.json
│   ├── claude/settings.json
│   └── opencode/README-or-profile-defined-config
├── bin/to-prism
├── src/to_prism/
│   ├── cli.py
│   ├── paths.py
│   ├── inventory.py
│   ├── fingerprint.py
│   ├── profiles.py
│   ├── contracts.py
│   ├── graph.py
│   ├── render.py
│   ├── compare.py
│   └── report.py
├── profiles/
│   ├── codex.yaml
│   ├── claude.yaml
│   ├── opencode.yaml
│   └── open-agent-skill.yaml
├── schemas/
│   ├── inventory.schema.json
│   ├── contracts.schema.json
│   ├── workflow.schema.json
│   ├── reasoning-map.schema.json
│   ├── decisions.schema.json
│   ├── lock.schema.json
│   └── report.schema.json
├── references/
│   ├── conversion-contract.md
│   ├── preservation-policy.md
│   ├── reasoning-mapping.md
│   ├── provider-support.md
│   └── output-contract.md
├── templates/
│   ├── prism-project/
│   ├── python-adapter/
│   └── tests/
└── tests/
    ├── fixtures/{codex,claude,opencode,mixed}/
    ├── golden/
    ├── unit/
    ├── integration/
    └── e2e/
```

The eventual implementation may combine small modules, but it must preserve
these ownership boundaries: skills contain judgment and routing; scripts own
repeatable mechanics; profiles own vendor facts; schemas own artifact shape;
templates own generated code; tests own examples and oracles.

No file in a generated project may import from `to_prism` at runtime. The kit
is a compiler-like build tool, not a hidden runtime dependency.

`bin/to-prism` is the provider-neutral primary interface. Provider-specific
skill installation is optional integration: installation must register paths
without copying checkout-specific absolute paths into hooks, and must define
discovery, update, and uninstall behavior. Hook frontends call one installed
logical guard entry point and do not locate scripts relative to an agent's
variable working directory.

## 4. Conversion artifacts and intermediate representation

Each run uses a staging directory and publishes atomically only after required
checks pass. It emits:

```text
<output>/
├── prism_project/
│   ├── types.prism
│   ├── reasoning.prism
│   ├── relations.prism          # only when domain relations are needed
│   ├── materialization.prism
│   ├── main.prism
│   ├── generated/               # built Skill/Hook modules
│   ├── adapters/                # optional thin Python package
│   ├── prism_modules/            # project-local imported .prism dependencies
│   ├── vendor/
│   │   ├── wheels/               # exact Prism + transitive Python artifacts
│   │   ├── manifest.json
│   │   ├── sbom.json
│   │   └── licenses/
│   ├── pyproject.toml
│   ├── dependency.lock
│   ├── bootstrap.sh              # creates a local environment offline
│   ├── prism                     # launcher for the bundled toolchain
│   └── tests/
├── source_snapshot/             # optional vendored mode only
├── conversion/
│   ├── inventory.json
│   ├── contracts.json
│   ├── workflow.json
│   ├── reasoning-map.json
│   ├── decisions.json
│   ├── to-prism.lock.json
│   └── report.md
└── run.sh or equivalent portable launcher
```

Every output is labeled as one of two classes:

- **Portable conversion:** all orchestration and reasoning semantics are in
  canonical `.prism`; leaf implementations and the complete required Prism
  toolchain/runtime dependency closure are bundled in the generated project.
  It bootstraps offline and runs after the source tree, converter, original
  Prism checkout, and ambient Prism installation are removed. This is the
  standalone final target.
- **Linked conversion:** canonical `.prism` owns orchestration and reasoning,
  but one or more named typed leaf effects depend on an external source
  installation. It is useful and runnable only with those bindings present; it
  must never be reported as portable.

Both classes bundle their necessary Prism dependencies inside the generated
project. “Linked” refers only to remaining dependencies on the original
external project's leaf implementations, never to a dependency on an ambient
Prism installation.

Calling the entire upstream workflow through one opaque adapter is not a full
conversion. Source-native code may implement typed leaf effects, but `.prism`
must own workflow topology, contracts, effects, and epistemic structure before
Structural, Trace, or Epistemic preservation can be awarded.

### 4.1 Inventory model

Every item needs a stable ID derived from provider, normalized relative path,
and source-local identity—not from an absolute path. Inventory records include:

- kind: skill, hook group, hook handler, command, script, tool, agent, subagent,
  MCP capability, reference, asset, configuration, test, or entry point;
- source location, bytes hash, executable bit, and symlink policy;
- provider and format/profile version;
- declared/inferred inputs, outputs, conditions, dependencies, permissions,
  environment names, and side-effect hints;
- discovery evidence and confidence;
- credential or unsafe-content classification;
- mapping disposition: convert, wrap, copy, exclude, unsupported, or unresolved.

Absolute paths may appear in ephemeral diagnostics but never in committed
goldens, generated Prism source, or stable IDs.

Suspicious secret-bearing content is excluded by default and vendored only
through explicit allowlisting. The manifest records path-level disposition
rather than content or secret-value hashes where those hashes could themselves
be sensitive. Diagnostic excerpts are bounded and redacted before persistence.

### 4.2 Workflow IR

The neutral workflow graph must represent:

- nodes with stable identity and callable/capability references;
- typed or unresolved input/output ports;
- edges with data, control, condition, and lifecycle meanings;
- sequence, parallel/fan-out, join, choice, bounded repeat/refinement, delegation,
  aggregation, and failure/stop transitions;
- persistent versus invocation-local capabilities;
- precondition, postcondition, permission, effect, retry, timeout, and failure
  policies;
- source evidence for every inferred edge.

The graph is the preservation comparison surface. Canonical `.prism` source is
rendered from it and is the sole final workflow representation. A diagram or
catalog projection, if ever added, is a disposable visualization derived from
the same graph and cannot satisfy any conversion acceptance criterion.

### 4.3 Decision and lock records

Semantic choices must be explicit and replayable. Each record distinguishes an
`extracted` fact, `proposed` inference, `reviewed` decision, and `approved`
decision. Generation may consume an ambiguous semantic choice only after the
required approval:

- contract accepted/overridden;
- workflow boundary chosen;
- standard reasoning method selected;
- custom reasoning type or relation justified;
- script wrapping strategy selected;
- unsupported behavior accepted as debt;
- fixture and oracle selected;
- generated file ownership and content hashes.

`to-prism.lock.json` binds source fingerprint, profile versions, converter
version, decisions hash, template version, generated file hashes, and Prism CLI
version. A content-addressed copy of the prior generated base (or a reproducible
equivalent) supports real three-way updates; hashes alone only detect divergence.

Raw CLI JSON is run evidence, not stable lock identity: current commands can
contain absolute paths, timestamps, invocation IDs, and artifact locations.
Byte-identical guarantees apply to canonical generated source, normalized
manifests, and lock content from two fresh outputs with identical inputs—not to
raw execution logs.

### 4.4 Prism dependency closure and deployment

Dependency resolution is feature-driven rather than “copy the repository.” The
generator starts with the generated `.prism` imports, CLI commands, effects,
handlers, and adapters, then closes over:

- required public distributions such as language, runtime, SDK, CLI, and only
  the adapters actually used;
- required standard/domain `.prism` modules and their transitive imports;
- generated Python adapter packages and their entry-point metadata;
- exact third-party wheel dependencies for the target platform; and
- launcher/bootstrap metadata, licenses, hashes, and an SBOM.

Conversion-only dependencies such as the transpiler are omitted from the final
runtime unless a generated project actually exposes a build operation.
Experimental platform/catalog packages are excluded unless canonical `.prism`
execution demonstrably requires them.

The project-local `bootstrap.sh` creates a local environment using only
`vendor/wheels` with dependency/index access disabled. The project-local
`prism` launcher selects that environment, sets the generated project as the
workspace root, and exposes the public CLI. Dependency selection must never
fall back to an ambient package, developer checkout, or network index.

Because wheels are platform-specific, a portable output declares its target
Python/OS/architecture set. Multi-platform output carries separate locked
wheel sets or is labeled portable only for the included target. Source
distributions may be included only with an explicitly tested offline build
toolchain; otherwise missing wheels are a portability blocker.

## 5. Skill suite

### 5.1 `to-prism`

The entry point routes the end-to-end process, checks phase prerequisites, and
stops at review gates. It does not perform parsing or rendering itself.

Stages: inspect -> baseline -> model -> map reasoning -> review plan -> generate
-> verify -> publish. Default behavior stops before native execution and before
publishing unresolved high-risk mappings.

### 5.2 `to-prism-baseline`

Proposes native baseline commands and fixture capture, but runs them only with
authorization. It copies the project to an isolated temporary workspace when
tests may write, captures normalized stdout/stderr/exit status/artifacts, and
records unavailable or flaky baselines honestly.

### 5.3 `to-prism-model-workflows`

Builds typed capability contracts and workflow graphs from explicit
configuration, skill cross-references, hooks, commands, and tests. It separates
logical task boundaries from lifecycle hooks and avoids treating file order as
execution order without evidence.

### 5.4 `to-prism-map-reasoning`

Classifies epistemic operations independently of operational steps. It maps to
the standard Prism methods—Deductive, Abductive, Inductive, Analogical,
Contrastive, ModelBased, Refutational, or Evidential—only when their semantics
fit. It also selects typed relations and assurance boundaries.

When none fit, it proposes a project-local method using one exact logical input
record and one result type. The proposal must state:

- the epistemic operation;
- why all standard methods are inadequate;
- its input, output, and any relation certificate;
- whether it produces ordinary data, evidence, support, validation, or proof;
- how it will be materialized and tested.

Custom methods are emitted inside the generated project. The converter never
edits `libs/prism` automatically. Structural computation, parsing, routing,
formatting, prompting, and tool invocation are never custom reasoning methods.

### 5.5 `to-prism-review-preservation`

Reviews independently produced verification evidence, unsupported behavior,
preservation caps, critical-workflow thresholds, and publication claims. It
must not turn fake execution, artifact integrity, or absence of a baseline into
behavioral equivalence.

### 5.6 `to-prism-update`

Re-inventories a changed upstream project, computes semantic and file diffs,
reuses still-valid decisions, marks invalidated decisions, and performs a
three-way regeneration. It never treats a changed source hash as a harmless
cache miss.

Inventory, rendering, schema validation, routine verification, and publication
are deterministic `bin/to-prism` commands, not separate skills. Skills exist
only where semantic judgment, oracle selection, authorization, or conflict
review materially changes the result.

## 6. Hooks supplied by the kit

`integration-hooks/` contains converter guard integrations. These are distinct
from provider hooks discovered in the source and emitted as generated typed
`Hooks[Provider]` artifacts. Provider-native guard frontends decode events into
one versioned internal request and invoke the same deterministic guard command;
provider differences must not fork core conversion semantics.

Required lifecycle protections:

- **Pre-write/source guard:** reject visible writes whose resolved path is
  inside the registered source root. This is defense in depth, not containment;
  subprocesses and unsupported events can bypass it.
- **Pre-execution guard:** reject commands during discovery and require an
  approved baseline or verification phase.
- **Secret guard:** block capture or copy of credential-shaped paths and redact
  values in logs.
- **Post-generation check:** validate schemas and run `prism check`/`compile`
  against staged entry points.
- **Stop/checkpoint guard:** refuse a “complete” report when required artifacts,
  coverage dispositions, or preservation tests are missing.

Codex and Claude configurations can be authored once their exact supported
events are locked by fixtures. OpenCode support begins as a provider profile
and capability matrix; no hook configuration should be invented until its
native contract is verified. Unsupported lifecycle events become explicit
debt, not nearest-name mappings.

The generated Prism project's own hooks remain typed provider artifacts. A
Claude hook can be preserved and checked even if the current Prism runtime
cannot execute it; the report must label runtime activation unsupported until
an appropriate adapter exists. Current Codex activation also runs in an
otherwise empty temporary working directory: relative commands, project
resources, local executables, environment assumptions, network use, or write
requirements require explicit portability classification and generally cannot
claim behavioral preservation without adapter support and instrumented tests.

Guard protocol tests cover malformed/missing payloads, unknown events, resolved
path aliases, timeouts, exit codes, stdout/stderr discipline, and fail-closed
behavior. Similar native event names are never sufficient evidence of semantic
parity.

## 7. Generated Prism architecture

For each recoverable workflow, generation should follow:

```text
external task/input
  -> nominal Prism input records
  -> pure reasoning declaration (when genuine epistemic structure exists)
  -> concrete workflow materialization
     -> deterministic functions first
     -> typed Skill[Task] for instruction context
     -> typed Tool[Contract] for statically orchestrated callable capabilities
     -> typed Hooks[Provider] for native lifecycle behavior
     -> Python.Call or another explicit effect boundary for existing code
  -> validation/support/proof boundary
  -> useful typed domain result and trace
```

Not every external workflow deserves a `reasoning` declaration. Pure build,
formatting, deployment, or file-management flows should become ordinary Prism
functions/workflows. The reasoning mapper must record “operational only” as a
valid decision.

Generated `main.prism` receives variable capabilities and permissions. It does
not contain credentials, absolute paths, provider secrets, or machine-specific
commands. Deployment bindings live in launcher/runtime configuration or a thin
adapter package.

Attaching a tool name to an agent does not currently provide a dynamic tool-use
loop through the public Codex runner. Model-selected tools, MCP calls, process
execution, network access, file/data writes, dynamic delegation, and some
retry/timeout policies require an explicit supported handler or remain runtime
debt. Recoverable calls should be statically orchestrated in `.prism`; a
generated adapter must not hide an entire source-native orchestration.

The current CLI also has no general domain-input flag. Until a typed input
injection contract exists, each executable fixture needs its own canonical
`.prism` harness with literal typed input (or a zero-domain-argument `main`). A
launcher can claim general runnable preservation only when it accepts input
conforming to the generated nominal schema and passes it through a supported
public Prism boundary. CLI subprocesses run with the generated project as their
working directory because workspace module resolution is rooted there.

## 8. Test strategy

### 8.1 Toolkit unit tests

- provider-profile path recognition and precedence;
- frontmatter/config parsing, including malformed and mixed encodings;
- canonical relative paths, symlink escape rejection, and overlap rejection;
- deterministic stable IDs and Merkle fingerprints;
- secret classification and redaction;
- IR schema validation and dangling-reference rejection;
- graph cycle, join, choice, loop-bound, and unreachable-node checks;
- deterministic rendering and atomic publish behavior;
- lockfile and three-way-update behavior.
- deterministic Prism feature-to-distribution/module dependency closure;
- missing, conflicting, tampered, wrong-platform, and undeclared dependency
  rejection.

### 8.2 Provider contract fixtures

For Codex, Claude, OpenCode, and generic Open Agent Skills, maintain minimal and
complex fixtures covering:

- one skill with references/assets;
- multiple nested skills;
- commands/scripts requiring typed wrappers;
- every supported hook event and handler type;
- agents/subagents and local capabilities;
- cross-skill calls and shared resources;
- unknown fields/events and newer-version forward compatibility;
- credential-shaped and symlinked content;
- mixed-provider repositories.

Fixture provenance and provider version must be recorded. Synthetic fixtures
test edge cases; at least one redistributable realistic fixture per provider
tests actual layout assumptions.

### 8.3 Generated-project tests

- every generated `.prism` file parses and type-checks through the public CLI;
- each entry point compiles through a separate fixture harness when necessary;
- fake-handler runs produce values of the declared type and are labeled only as
  type/executability smoke evidence, never equivalence evidence;
- task-contract mismatches, wrong hook providers, and invalid tool contracts
  fail at check time;
- scripts cannot enter a skill artifact without a typed tool/adapter mapping;
- effects, failures, and permissions match the reviewed contracts;
- custom reasoning methods stay pure and project-local;
- all discovered elements have a disposition;
- generated files contain no absolute source paths or secrets;
- Python adapters install into a clean environment through declared
  `prism.python_effects` entry points, including absent, duplicate, wrong, and
  typed-failure cases;
- a portable output still runs after relocation with the source tree and
  converter removed, repository `PYTHONPATH` cleared, ambient Prism uninstalled,
  network disabled, and only its bundled dependency artifacts available;
- offline bootstrap installs only hash-locked bundled wheels, the project-local
  launcher reports the expected Prism capability/version set, and no import is
  satisfied by an ambient environment;
- all generated `.prism` imports resolve from the project or bundled module
  closure, and removing any declared required dependency makes the closure test
  fail with an actionable diagnostic;
- SBOM, license inventory, package hashes, executable modes, and platform tags
  match the bundled artifacts.

### 8.4 Preservation and differential tests

- source path/type/bytes/mode/symlink fingerprint is identical before and after
  every phase, including command failure and timeout paths;
- generated skill instructions and resources decode to the exact source path
  set and bytes; unsupported metadata and executable-mode losses are explicitly
  dispositioned;
- generated workflow graphs correspond to an independently reviewed provider
  graph, instrumented native trace, or fixture oracle—not another projection of
  the same conversion IR;
- deterministic native fixtures and Prism fixtures have equal normalized
  outputs;
- nondeterministic fixtures satisfy the same schema and domain invariants;
- recorded effect artifacts, digests, and checked-module integrity verify
  offline through `prism verify-run`; this is not workflow replay or behavioral
  equivalence;
- normalized traces respect declared stage correspondence, including failure
  and stop paths;
- a provider hook evidence matrix distinguishes static round-trip, adapter
  materialization, native activation, and observable outcome. Claude is capped
  at Structural/Contract under the current runtime; Codex reaches Trace or
  Behavioral only through an authorized instrumented run;
- unsupported semantics appear in the report and reduce preservation level;
- running the conversion twice is byte-identical;
- changing one upstream element invalidates only dependent mappings and output.

Preservation results use `established`, `not_applicable`, `not_tested`,
`unsupported`, and `failed`. An unavailable baseline makes Trace and Behavioral
“not established”; opaque critical nodes and unsupported required runtime
activation block publication. Results are per critical workflow and are never
averaged to hide a failure.

### 8.5 Adversarial and mutation tests

- source path aliases output through a symlink;
- a hook attempts to write to source;
- a script reads a secret or uses undeclared network access;
- an unknown provider event resembles a known event;
- a skill claims proof while producing generated prose;
- a loop has no bound or state change;
- a hidden cross-skill dependency is removed;
- a generated file is manually edited before update;
- the native baseline is flaky, nonzero, or unavailable;
- malicious instructions request disabling the preservation checks.

Tests must assert observable behavior and invariants, not generated prose or
heading text.

## 9. Phased implementation backlog

Dependencies in parentheses refer to task IDs. A phase is complete only when
its exit criteria are met.

Implementation status (2026-08-19): every backlog item below is delivered in
`to_prism/` and covered by deterministic tests or an explicit opt-in
clean-room/live test. A checked item whose underlying public Prism capability
does not exist means the required fail-closed capability classification,
preservation cap, and debt record were implemented; it does not claim that the
unsupported capability became executable.

### Phase 0 — decisions and executable contract

- [x] **TP-000** Decide and document the portability target: Python version,
  supported OS/architecture matrix, packaging form, bundled-wheel policy, and
  whether the kit may depend on PyYAML or must use a locked standalone
  executable.
- [x] **TP-001** Define the public command surface: `inspect`, `baseline`,
  `model`, `generate`, `verify`, `convert`, and `update`, each with explicit
  source/output arguments and dry-run semantics.
- [x] **TP-002** Define linked and portable/vendored-snapshot threat models, including
  subprocess, network, filesystem, credential, and package-install authority.
- [x] **TP-003** Write `references/conversion-contract.md` with phase inputs,
  outputs, failure rules, review gates, and publish semantics.
- [x] **TP-004** Write `references/preservation-policy.md` with the six
  preservation levels and workflow-specific pass thresholds.
- [x] **TP-005** Enforce canonical `.prism` as the only final workflow target in
  schemas, reports, publication gates, and tests. Exclude platform diagram and
  catalog projections from v1 conversion acceptance; any later projection must
  be derived and non-authoritative.
- [x] **TP-006** Define a public Prism capability/version handshake covering
  distribution, language/core/IR/trace versions, commands, handlers, hook
  providers, effects, and standard-library modules. Prefer a future
  `prism capabilities --json`; provisionally use executable digest, probe
  programs, and compile metadata, failing closed on mismatch.
- [x] **TP-007** Resolve typed domain-input injection. Either require/add a
  public `prism run --input` contract or explicitly scope v1 runnable testing to
  generated fixture-specific `.prism` harnesses.
- [x] **TP-008** Create a source-construct capability matrix mapping vendor
  features to Prism syntax, available public CLI handlers, and maximum
  preservation status.

Exit criteria: a reviewer can tell exactly what `convert` may read, execute,
write, and claim.

### Phase 1 — self-contained skeleton and safety foundation

- [x] **TP-010** Create the directory skeleton, version file, local package,
  launcher, and isolated test configuration (TP-000).
- [x] **TP-011** Implement canonical path resolution, source/output disjointness,
  symlink escape checks, staging, and atomic publication.
- [x] **TP-012** Implement deterministic tree fingerprinting with ignore rules
  recorded in the manifest rather than hidden in code. Cover relative path,
  entry type, bytes, executable mode, and symlink target; define treatment of
  VCS internals, sockets, mtimes, xattrs, and concurrently changing files.
- [x] **TP-013** Implement structured logging with secret redaction and no
  absolute paths in stable artifacts.
- [x] **TP-014** Implement the source-mutation guard and test failed write
  attempts through aliases and symlinks (TP-011, TP-012).
- [x] **TP-015** Define and validate all JSON schemas; add round-trip and
  forward-version rejection tests.
- [x] **TP-016** Add CI commands that exercise only `to_prism/` plus the public
  `prism` executable, proving no private repository imports. Copy the kit into
  a clean directory, clear repository `PYTHONPATH`, and use only declared
  released Prism/stdlib dependencies.
- [x] **TP-017** Author the minimal router, workflow-modeling, and
  reasoning-mapping skills needed to exercise early review gates; complete
  packaging and forward tests in Phase 8.
- [x] **TP-018** Add black-box public CLI contract tests for working directory,
  exit codes, JSON shape normalization, rejected runs, empty effect records,
  artifact-directory coupling, build preconditions, and supported versions.
- [x] **TP-019** Define the Prism dependency-closure schema and resolver inputs:
  generated imports, effects, handlers, commands, adapters, platform tags,
  package hashes, licenses, source identities, and transitive requirements.

Exit criteria: an empty conversion run is deterministic, writes only to staging
and output, detects no in-scope source change, and validates all emitted
metadata without reading implementation resources outside `to_prism`.

### Phase 2 — provider discovery and complete inventory

- [x] **TP-020** Define a provider-profile schema with layout rules, artifact
  kinds, hook vocabulary, precedence, and supported-version evidence (TP-015).
- [x] **TP-021** Implement generic Open Agent Skill discovery with nested skill
  boundaries, assets, scripts, symlinks, and credentials.
- [x] **TP-022** Implement and fixture-test the Codex profile.
- [x] **TP-023** Implement and fixture-test the Claude profile.
- [x] **TP-024** Research the exact OpenCode project and hook contracts, record
  primary-source versions, then implement and fixture-test its profile. Do not
  infer it from Codex or Claude conventions.
- [x] **TP-025** Inventory commands, tools, agents/subagents, MCP references,
  permissions, environment names, tests, and entry points.
- [x] **TP-026** Add mixed-provider ownership and conflict resolution.
- [x] **TP-027** Add coverage accounting: every discovered file and semantic
  element receives one disposition.
- [x] **TP-028** Implement the deterministic `inspect` command and its concise
  review output.

Exit criteria: realistic fixtures produce stable, complete inventories with no
execution and no unclassified executable or credential-shaped content.

### Phase 3 — native baseline harness

- [x] **TP-030** Define a baseline descriptor schema: command, workdir,
  environment names, fixture inputs, timeout, expected artifacts, normalizers,
  and oracle (TP-015).
- [x] **TP-031** Discover candidate native test/run commands but require review
  before execution.
- [x] **TP-032** Implement isolated copied-workspace execution with explicit
  filesystem/network policy and bounded output capture.
- [x] **TP-033** Implement output, artifact, and trace normalizers that remove
  timestamps, random IDs, temporary paths, and approved nondeterministic fields.
  Version/hash every normalizer and add negative controls proving it cannot
  erase meaningful success/failure or domain differences.
- [x] **TP-034** Classify baseline reliability: reproducible, flaky,
  nondeterministic, unavailable, or failed.
- [x] **TP-035** Implement `to-prism-baseline` and prove the original source
  fingerprint remains unchanged.

Exit criteria: at least one fixture per supported provider has a repeatable
native baseline or an explicit, justified “unavailable” record.

### Phase 4 — contracts and provider-neutral workflow recovery

- [x] **TP-040** Define nominal contract IR for inputs, outputs, errors,
  effects, permissions, providers, and confidence/evidence (TP-015).
- [x] **TP-041** Define workflow graph IR and validators for composition,
  lifecycle, dataflow, failure, and stop edges. Represent Prism constraints:
  choice routers are exhaustive closed sums with convergent branches; repeats
  have a static positive bound and changing state; reasoning methods are pure
  one-input contracts; relation edges require materialized certificate builders.
- [x] **TP-042** Extract explicit contracts from schemas, command interfaces,
  hook payloads, tests, and structured examples.
- [x] **TP-043** Infer unresolved contracts conservatively and generate review
  questions only when distinct answers materially change generated types.
- [x] **TP-044** Recover workflow boundaries and graph topology from explicit
  orchestration before considering documentation order or prose cues.
- [x] **TP-045** Model persistent versus invocation-local skills, tools, and
  hooks.
- [x] **TP-046** Model retries, timeouts, parallelism, joins, conditional paths,
  bounded loops, delegation, and failure propagation, but cap unsupported
  constructs according to TP-008 rather than implying they can all render or
  execute.
- [x] **TP-047** Implement `to-prism-model-workflows` with dangling-edge,
  unreachable-node, ambiguous-entrypoint, and unbounded-loop diagnostics.

Exit criteria: every supported fixture has a validated graph and typed or
explicitly unresolved ports; no inferred edge lacks source evidence.

### Phase 5 — epistemic mapping and extension protocol

- [x] **TP-050** Ship self-contained executable standard reasoning contracts
  and an assurance reference versioned against the Prism CLI, or declare and
  capability-check an exact `prism-stdlib` dependency. Prose alone is
  insufficient for clean-room generated-project checks.
- [x] **TP-051** Define the reasoning-map schema with source evidence,
  confidence, alternatives, operational-only decisions, relation selection,
  assurance transitions, and reviewer status.
- [x] **TP-052** Implement conservative standard-method classification using
  semantic role and logical inputs, not names alone.
- [x] **TP-053** Separate structural/operational nodes from epistemic
  occurrences and test common false positives such as “router,” “validator,”
  “formatter,” and “planner.”
- [x] **TP-054** Define the custom reasoning method and relation proposal
  protocol, including mandatory inadequacy analysis and project-local output.
- [x] **TP-055** Validate provenance and assurance transitions; block generated
  prose from becoming `Evidence`, `Validated`, `Supported`, or `Proof` without
  the appropriate constructor/check.
- [x] **TP-056** Implement `to-prism-map-reasoning` and a human review gate for
  all custom methods and low-confidence mappings.

Exit criteria: reviewed fixtures preserve meaningful reasoning distinctions,
and operational workflows are not forced into artificial epistemic topologies.

### Phase 6 — deterministic Prism generation

- [x] **TP-060** Define the generated project contract and module naming rules,
  avoiding hidden paths and collisions (TP-040, TP-041, TP-051).
- [x] **TP-061** Render nominal types, project-local reasoning methods,
  relations, and pure `reasoning` declarations.
- [x] **TP-062** Render functions, agents, tools, materialized workflows,
  effects, failures, permissions, and `main` entry points only where TP-008
  records a supported rendering/execution path. Statically orchestrate tool
  calls; never imply agent tool-name metadata enables dynamic tool use.
- [x] **TP-063** Integrate public `prism build skill` for compatible script-free
  Open Agent Skills with inferred/reviewed task types.
- [x] **TP-064** Integrate public `prism build hooks` for supported Codex and
  Claude configurations while retaining provider typing. Reject or disposition
  unknown top-level fields first, and classify relative-command/cwd/resource
  dependencies that the Codex temporary runtime cannot preserve.
- [x] **TP-065** Generate thin Python effect adapter packages for existing
  Python operations with logical entry-point names and ordinary typed results;
  install and test their `prism.python_effects` bindings in a clean environment.
- [x] **TP-066** Evaluate commands, MCP, network, file/data writes, retries,
  timeouts, and dynamic delegation against TP-008. If Prism lacks a typed
  intrinsic plus public CLI handler, record a core capability gap instead of
  routing it invisibly through Python.
- [x] **TP-067** Implement allowlisted vendored snapshots and linked runtime
  bindings without absolute paths in authored Prism.
- [x] **TP-068** Generate project-local fixture tests, launcher, manifest,
  report, and lockfile.
- [x] **TP-06B** Generate one canonical `.prism` fixture harness per workflow
  and fixture until TP-007 provides general input injection. Run each command
  with `cwd` set to the generated project.
- [x] **TP-06C** Resolve the minimal Prism distribution and `.prism` module
  closure from generated features; build/copy exact public artifacts into
  `vendor/` and `prism_modules/` with hashes, licenses, platform tags, and SBOM.
- [x] **TP-06D** Generate and test an offline bootstrap plus project-local
  `prism` launcher that never consults ambient packages, a network index, the
  converter, or the original Prism checkout.
- [x] **TP-069** Implement deterministic formatting, staged `prism check` and
  `prism compile`, and atomic publish.
- [x] **TP-06A** Implement the deterministic `generate` command and
  byte-identical regeneration
  tests.

Exit criteria: supported fixtures generate complete projects that check and
compile without source-project mutation or private Prism imports.

### Phase 7 — preservation verification

- [x] **TP-070** Implement inventory-to-output asset and disposition coverage.
- [x] **TP-071** Implement source/workflow graph correspondence and explainable
  mismatch reporting against an independent reviewed/observed oracle. Add edge,
  condition, ordering, and failure-branch mutations to prove sensitivity.
- [x] **TP-072** Implement contract-surface comparison for inputs, outputs,
  failures, effects, permissions, provider hooks, and entry points.
- [x] **TP-072A** Implement provider-specific hook evidence and preservation
  caps for static round-trip, adapter materialization, native activation, cwd
  portability, and observable outcomes. Test multiple-artifact merge order,
  failure, timeout, relative commands, dependencies, and environment needs.
- [x] **TP-073** Implement deterministic fixture differential tests and
  property/schema oracles for nondeterministic steps.
- [x] **TP-074** Implement normalized trace correspondence independently of
  renderer IR, including failure, stop, retry, and loop paths. Include hook
  paths only when native instrumentation actually observes them.
- [x] **TP-075** Integrate `prism run --handler fake` and persisted
  `prism verify-run --mode offline` tests, labeling them respectively as typed
  execution smoke and effect/core integrity—not behavioral or trace equivalence.
- [x] **TP-076** Add optional authorized live tests without making them a
  prerequisite for deterministic CI.
- [x] **TP-076A** Run relocation/clean-room dependency tests for every supported
  target: remove source and converter, clear environment paths, uninstall
  ambient Prism, disable network, bootstrap from bundled artifacts, then check,
  compile, run, and verify the generated `.prism` project.
- [x] **TP-077** Calculate preservation levels per workflow and an aggregate
  result that cannot hide a failed critical workflow in an average.
- [x] **TP-078** Implement the deterministic `verify` command and publication
  gates; route claim/debt judgment to `to-prism-review-preservation`.

Exit criteria: the report states precisely which workflows achieved asset,
structural, contract, trace, behavioral, and epistemic preservation, with links
to machine-readable evidence and explicit debt.

### Phase 8 — skill and hook packaging

- [x] **TP-080** Author the six `SKILL.md` files with discriminating
  descriptions, progressive references, and no duplicated schemas or generic
  coding advice.
- [x] **TP-081** Add skill metadata and validate every skill with the available
  skill validator.
- [x] **TP-081A** Define provider-neutral direct launch plus optional provider
  skill discovery/registration, update, and uninstall. Hooks invoke an installed
  logical command without hard-coded checkout paths.
- [x] **TP-082** Author Codex source/write, execution, secret, post-generation,
  and completion guards against the exact supported event contract.
- [x] **TP-083** Author equivalent Claude hooks while preserving Claude-specific
  semantics.
- [x] **TP-084** Author OpenCode hooks only after TP-024 establishes and tests
  the native contract.
- [x] **TP-085** Test every provider hook frontend against the same guard script
  conformance suite and versioned internal request protocol, including malformed
  input, timeouts, exit codes, path aliases, and fail-closed behavior.
- [x] **TP-086** Forward-test each skill on isolated realistic fixtures and
  refine only from observed failures. Assert correct routing, no unauthorized
  execution, no source mutation, escalation of ambiguity, no fabricated
  preservation claim, and minimal relevant reference loading.

Exit criteria: copying `to_prism/` to a clean conversion environment is
sufficient to generate a project whose own bundle supplies all required
Prism/stdlib runtime dependencies, with no checkout path embedded in skills,
integration hooks, output source, or launchers.

### Phase 9 — incremental update and migration safety

- [x] **TP-090** Compute semantic diffs between old/new inventories, contracts,
  workflows, and reasoning maps.
- [x] **TP-091** Track decision dependencies so upstream changes invalidate the
  minimum correct set of decisions.
- [x] **TP-092** Implement generated/user-owned file boundaries and three-way
  regeneration with conflict reports.
- [x] **TP-093** Re-run only affected baselines and preservation tests while
  retaining a full-verify option.
- [x] **TP-094** Implement `to-prism-update` with rollback-safe staging.
- [x] **TP-095** Add migrations for schema/profile/template versions and reject
  unknown incompatible lock versions.

Exit criteria: an upstream skill, hook, or workflow change can be incorporated
without redoing unrelated decisions or overwriting manual Prism work.

### Phase 10 — pilot conversions and readiness

- [x] **TP-100** Select one small, redistributable project for each provider and
  one mixed-provider project.
- [x] **TP-101** Run end-to-end linked conversions and document all unsupported
  behavior as product gaps, not fixture exceptions.
- [x] **TP-102** Run vendored-snapshot conversions and verify secret/license
  allowlists.
- [x] **TP-102A** Exercise every supported Python/OS/architecture bundle in an
  offline clean-room environment and verify dependency hashes, SBOM, licenses,
  local launcher behavior, and absence of ambient resolution.
- [x] **TP-103** Add regression fixtures for every real pilot failure.
- [x] **TP-104** Review custom reasoning types for semantic necessity and
  duplication across pilots; promote nothing into Prism core automatically.
- [x] **TP-105** Measure inventory coverage, required human decisions,
  conversion time, deterministic rerun stability, and preservation levels.
- [x] **TP-106** Publish a v1 support matrix and known-debt list.

Exit criteria: no in-scope change is detected in any pilot source tree,
generated projects run through Prism, and every preservation claim is backed by
a repeatable test.

## 10. Early vertical slice

The smallest useful implementation should deliberately exclude automatic
reasoning inference at first:

1. Accept one script-free Open Agent Skill and one Codex hook configuration.
2. Fingerprint a read-only source tree and inventory both artifacts.
3. Require a small reviewed JSON file declaring the task type and a two-node
   sequential workflow.
4. Use public `prism build skill` and `prism build hooks`.
5. Render `types.prism`, `materialization.prism`, and `main.prism`.
6. Resolve and bundle the exact Prism CLI/language/runtime/stdlib/adapter
   dependency closure plus an offline bootstrap and local launcher.
7. Run the bundled launcher for `prism check`, `prism compile`, and a
   fake-handler typed-execution smoke
   fixture without treating it as behavioral equivalence.
8. Verify the source fingerprint and asset/contract/structural preservation.
9. Relocate the output, remove ambient/source/converter access, disable network,
   bootstrap locally, and rerun it.
10. Regenerate byte-identically.

This slice validates the safety boundary, IR, public CLI integration, output
contract, and test strategy before adding ambiguous semantic inference. The
next slice adds a real `reasoning.prism`; the third adds a typed adapter for an
upstream script.

## 11. Open decisions that should remain explicit

- Whether `to_prism` is copied into external projects or invoked from a central
  checkout. The architecture supports both, but generated output must never
  depend on the kit's installed path.
- Whether non-Python command execution receives a first-class Prism effect.
  Until it does, command-heavy projects cannot claim full runtime preservation.
- Which native Codex/Claude/OpenCode versions are supported and how profiles
  are updated from primary specifications.
- Whether a Claude model adapter is in scope or Claude hooks are initially
  preserved/type-checked only.
- Whether general typed runtime input injection is added to the public Prism
  CLI or v1 execution remains fixture-harness-bound.
- Which workflows require behavioral preservation versus only structural and
  contract preservation.
- Whether vendored mode may include upstream dependencies and under which
  license/size policies.

Recommended defaults are: central or copied invocation both supported; explicit
output path; linked mode first while portable remains the standalone release
target; typed `.prism` as the sole final workflow result;
Codex execution first; Claude preservation before execution; OpenCode only
after verified profile research; deterministic tests required; live model tests
optional; no automatic Prism-core reasoning extensions.
