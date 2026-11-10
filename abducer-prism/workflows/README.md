<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Layered Abducer Prism Workflows

This directory contains the generated Prism specification layer for Abducer's 19
canonical reasoning workflows. Each workflow is now a small Prism module rather than
a monolith, following the ownership model in `examples/layered_release_review/` and
`references/layers.md`.

## The Four Generated Layers

Every workflow module has this shape:

```text
<module-id>/
  types.prism          nominal domain records and closed alternatives
  occurrences.prism    semantic joins and Input -> Generated[Output] signatures
  relations.prism      edge and certificate contracts
  reasoning.prism      imports, comments, and high-level epistemic topology only
```

Dependencies flow upward from types to occurrences/relations to reasoning. The useful
review entrypoint is `reasoning.prism`: it shows what reasoning happens and which
results depend on which earlier results without mixing in data declarations or edge
schemas.

## Sample Outputs

Each workflow also has a documentary `sample_outputs.prism` companion. It is not a
fifth semantic layer and is never imported by `reasoning.prism`, `materialization.prism`,
or `main.prism`. Instead, it gives readers one coherent simulated payload for every
named reasoning binding, in source order, using ordinary typed Prism constants.

For example, `discovery_marathon_loop/sample_outputs.prism` shows the bounded scope,
abductive hypothesis, inductive pattern, model and contrast probes, refutation, and
route assessment for one finite-to-continuum scenario. Parallel stages share a stage
number and use branch-specific names, exposing complementarity without implying a
wall-clock order.

Every block begins with a `# @sample` marker containing the canonical workflow,
reasoning declaration, binding, occurrence, `Generated[T]` output, topology stage,
branch, `mode=simulated`, and projection status. The literal demonstrates only the
payload `T`—constructing `Generated[T]` directly would forge provenance. The validator
in `validate_sample_outputs.py` compares markers against adjacent reasoning and
occurrence modules and rejects missing, extra, reordered, mistyped, or falsely observed
samples. The manifest records path, hash, count, alignment digest, and the explicit
`documentation_only` claim.

Nine unresolved projection boundaries receive shape-only simulated payloads marked
`projection_status=unresolved`; they do not imply executable materialization or new
warrant. The theorem workflow's optional failure-certificate field uses a pure static
type witness because the current frontend has no constructible `Option[T]` literal;
that limitation is retained in the sample validator and request evidence.

For example, `theorem_proof_delivery/reasoning.prism` now contains only the deduction,
refutation, and disposition-assessment graph. Its exact theorem data is in
`types.prism`, its three generative operation signatures are in `occurrences.prism`,
and the `TestsExactTheoremClaim` and `CalibratesTheoremProofDisposition` contracts are
in `relations.prism`.

`discovery_marathon_loop/reasoning.prism` makes the two parallel regions easy to see:
hypothesis/pattern formation, followed by model/contrast probing, then refutation and
routing assessment. Moving records and signatures out of that file does not change its
graph.

## Semantic Naming

Names use a concise two-part grammar: the domain referent plus its epistemic or control
role. This makes a declaration interpretable at its use site without encoding an
implementation, provider, or unsupported guarantee. For example:

- `DiscoveryCandidate` became `DiscriminatingDiscoveryHypothesis`.
- `ProofVerdict` became `ExactClaimRefutationAssessment`.
- `Calibrates` became `CalibratesDiscoveryRouting` in the discovery module and
  `CalibratesTheoremProofDisposition` in the theorem module.

Opaque payload fields follow the same rule where their old name was actively
misleading: `candidate_ref` becomes `proposal_ref` in release promotion, while ordinary
contextual identifiers such as `target_ref` remain compact. The reviewed mapping and
source-grounded rationale for every module are in
`.prism/refine-abducer-prism-semantic-names/semantic-name-ledger.json`.

## Reasoning Types

Callable occurrence aliases now make the epistemic method and domain function visible
together. For example, `DeriveExactTheoremClaim` is now
`DeductiveExactTheoremClaimDerivation`, while `AssessReviewDefeaters` is
`RefutationalReviewDefeaterAssessment`. Already exact names such as
`ModelBasedDiscoveryHypothesisProbe` remain unchanged.

The ERFL source contains 56 labelled reasoning occurrences and nine `_` projection
gaps. `_` explicitly preserves an unknown and licenses no inferred reasoning type, so
those nine callable graph boundaries use `Unresolved…Projection` names. They retain
their exact `Input -> Generated[Output]` interfaces for structural compatibility, but
have method `null`, inference class `none`, no materialization contribution, and no
execution claim. The reviewed per-occurrence decisions are in
`.prism/refine-abducer-prism-reasoning-types/reasoning-type-ledger.json`.

`Generated[T]` remains deliberately weak: method names do not imply observed evidence,
validation, support, proof, or verification.

## Materialization And Application Layers

The ten workflows with complete reviewed occurrence graphs now add:

- `materialization.prism`: exact generative agents, compiled skill imports, pure
  relation builders, and a total named instance of the existing reasoning graph.
- `main.prism`: a canonical smoke fixture and `solve` boundary.
- `generated/*.prism`: public-CLI `Skill[ExactInput]` snapshots compiled from current
  repository skill bytes. The builder does not write source skill trees; the manifest
  links every snapshot to its source path and hashes. Because the worktree predated
  this request in a dirty state, those hashes establish current identity rather than an
  independently observed request-start before/after preservation proof.

The structurally complete tranche contains 47 occurrence agents and 37 relation
bindings across ten workflows. The skill mapping is a request-authorized,
taxonomy-policy selection of candidate exemplars recorded in
`.prism/add-abducer-prism-materialization-workflows/materialization-binding-ledger.json`;
it is neither inferred source-runtime behavior nor an independently validated claim
that every prompt's entry gates fit its nominal input. Non-fake execution remains
unsupported until a per-occurrence skill-fit and input-sufficiency review exists.
Skill snapshots are input-type invariant,
so each occurrence owns an aliased compiled artifact even when another occurrence uses
the same source skill.

Nine workflows still contain an ERFL `_` projection. Those boundaries explicitly
license no reasoning method or execution, so their manifest entries are
`blocked_unresolved_projection_gap` and they have no `materialization.prism`,
`main.prism`, or generated skill directory. This omission is intentional—not an empty
placeholder—and resolving it requires a separately reviewed operational contract.

Fake-handler runs prove that the typed agents, effects, relation certificates,
reasoning configuration, fixtures, and solve boundary execute together. They do not
run source-native orchestration or linked validators and do not establish behavioral
equivalence, epistemic correctness, or the truth of the semantic relation named by a
certificate; builders construct the declared certificate shape unconditionally.

## IDs, Modules, And Links

`manifest.json` is authoritative. It maps each catalog workflow ID to a Prism-safe
module ID and all four layer paths. Hyphenated IDs are normalized only for imports:
for example, `ym-representational-dynamics-overlay` maps to
`ym_representational_dynamics_overlay/`.

Each reasoning file retains the source, contract, skill, validator, catalog-status,
and policy annotations from the former monolith. The manifest records repository-
relative target paths and SHA-256 identities. These are ordinary read-only references,
not symlinks, copies, skill activation, proof, or behavioral equivalence.

## Validation

The retired toolkit virtual environment is not required. Run the full gate from the
repository root with the transient CLI extracted from the checked-in wheel bundle:

```sh
bash .prism/refine-abducer-prism-semantic-names/with_bundled_prism.sh \
  bash abducer-prism/workflows/validate.sh
```

The gate checks and compiles the 76 immutable semantic files, 20 executable upper-layer
files, 19 documentary sample modules, and 47 compiled skill modules; fake-runs all ten mains; enforces nine blockers;
validates every link/hash; and compares every compiled reasoning graph and ordered
control-policy annotation with the reviewed topology fixture.
Its adversarial self-test must reject relation, parallelism, and policy-destination drift.
The historical reference archive defaults to `/Users/afreitas/Documents/to_prism.zip`;
set `TO_PRISM_ARCHIVE` to its relocated path on another machine. Members under the
retired `to_prism/.venv/` subtree are deliberately excluded from extraction parity.

To inspect one workflow, open a transient shell command through the same runner:

```sh
bash .prism/refine-abducer-prism-semantic-names/with_bundled_prism.sh \
  sh -c 'cd abducer-prism && "$PRISM_PATH" check workflows/theorem_proof_delivery/reasoning.prism'
```

The builder in `.prism/revisit-abducer-prism-layers/build_layered_workflows.rb` records
the one-time declaration classification. The resulting
`layer-classification.json` distinguishes domain types, semantic joins, occurrences,
relation certificates, and relations for review.

## Interpretation Boundary

Check/compile establishes syntax, typing, imports, and structural lowering. Fake runs
add typed materialization smoke. The topology fixture establishes reviewed
topology/policy correspondence. None of this runs main Abducer workflows or validators,
validates a theorem/scientific claim, establishes runtime equivalence, or upgrades
`Generated[T]` to observed, supported, validated, or proved status.
