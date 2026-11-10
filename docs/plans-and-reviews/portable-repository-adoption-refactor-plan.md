<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Portable repository adoption: Abducer refactor plan

This roadmap defines the bounded v1.2 adoption milestone while preserving Abducer. The original planning delivery extracted and evaluated the kit. The subsequent user-authorized implementation is tracked in [the implementation packet](../../.prism/implement-portable-repository-adoption/01-spec.md), with commands in [maintenance operations](../reference/repository-adoption.md). The kit remains source material rather than independent execution authority.

Source: [preserved guide](../../.prism/portable-repository-adoption-plan/source/docs/portable-repository-adoption.md), [archive provenance](../../.prism/portable-repository-adoption-plan/source-provenance.json), and [request packet](../../.prism/portable-repository-adoption-plan/01-spec.md). The kit's synthetic collector does not certify Abducer or supply production authority.

## Ownership and path mapping

Adopt stable discovery, operation contracts and linked provenance through existing owners. Keeping implementations in place is an acceptable completed migration; no new application, planner, provider or `catalog/` hierarchy is required.

| Portable convention | Abducer authority to preserve | Planned treatment |
| --- | --- | --- |
| Capability instructions | `skills/**/SKILL.md` | Preserve names and canonical paths; derive navigation. |
| Project maintenance | `proj_skills/`, `prism_me/` | Preserve their distinct discovery/control ownership; keep extracted kit request-local as reference. |
| Registry/descriptors | `agentic/registries/skill_registry.yaml` and existing task/route registries | Extend compatibly or use a versioned linked sidecar; no competing registry. |
| Execution/state | `agentic/discovery/`, `agentic/operations/`, `agentic/state/`, `agentic/experiments/` | Existing owners retain algorithms, transactions, authorization and provider selection. |
| Schemas | `agentic/spec/` | Use local schemas, including native public reasoning event v2; kit `repository-adoption.example/v2` is a different contract. |
| Public trace | `skills/common/reasoning_log.py`, `agentic/scripts/public_reasoning_trace_store.py` and current builders/renderers | Reuse native records; map missing portable fields compatibly into linked provenance. |
| Workflows | `agentic/discovery/workflow.py`, `agentic/orchestration/`, native registries and `abducer-prism/workflows/` | Retain runtime versus Prism representation distinctions and binding/manifest authority. |
| Host integration | Existing dispatchers and `abducer-prism/src/to_prism/` | Preserve current routes/CLI; no sibling host imports or synthetic attestations. |
| Artifacts/docs | Existing `agentic/` reports/state locations and `docs/` | Preserve consumer paths; new optional views reference immutable originals. |

Inventory every discoverable skill, classifying canonical, instruction-only, callable, retired, generated, vendored and project-support entries. Do not turn every helper into a skill. Current public names stay valid; a future scoped alias must resolve uniquely and cannot supersede an existing name silently. Roles such as reader/reasoner/writer describe responsibilities and grant no authority.

## First pilot and protected workflow

The first executable pilot is the existing `proj_skills/scripts/validate_proj_skills.py` CLI. Freeze its current arguments, stdout/stderr, exit codes and malformed-input behavior before adding any adapter. `project-state-profiler` is the instruction-only negative case: discovery metadata must not invent a callable. Public trace assembly/rendering is the provenance pilot.

M0 freezes the initial implementation set to that validator's legacy CLI and proposed registered adapter route, the selected native trace builder/renderer routes, and the release workflow's read-only semantic probe. All other inventoried capabilities receive ownership/disposition records only. M0 must name the exact supported route and fixture for each selected operation; a proposed registered adapter is not an already existing registration. Expanding this set requires an explicit scope revision. Executable workflow adoption beyond this validator/projection milestone is deferred; the milestone does not complete the kit's full A04 workflow adoption requirement.

The open `abducer-prism/workflows/release_promotion_loop/reasoning.prism` is a protected semantic probe, not the first executable adapter. It orders `UnresolvedReleaseProposalProjection` before `EvidentialReleasePromotionDispositionAssessment` through `ReleaseProposalEnablesPromotionDisposition`. Preserve symbols, types, order, claim boundary and disposition routes. An unresolved proposal projection, metadata registration or successful render does not establish execution or promotion authority.

## Dependency-ordered migration

The implementation follows M0 → M1 → M2 → M3 → M4 → M5; its [execution evidence](../../.prism/implement-portable-repository-adoption/05c-test-evidence.md) records completed checks and inherited gate limitations. Deliver one reviewable change per stage; revert individual changes or disable optional integrations while retaining evidence. Never reset unrelated work or rewrite historical records.

| Stage | Change and expected touch set | Exit gate | Rollback |
| --- | --- | --- | --- |
| M0: baseline | Record commit/dirty hashes, supported imports, CLI behavior, schemas, exact pilot bindings, workflow manifests, generated inputs and representative historical hashes in a successor request. | Reproducible commands/environment; inherited failures separated from regressions; no guessed bindings. | Supersede baseline documentation only. |
| M1: discovery/ownership | Extend existing registry/doc generation and maintenance discovery with identity, owner, operation, invocation mode, input/output and field provenance. | Every inventoried skill has disposition; one canonical source; current lookup/validators agree; instruction-only stays so. | Remove optional projection/metadata version; old registry remains usable. |
| M2: typed pilot adapter | Add a narrow adapter beside the maintenance validator's existing owner only where needed; fixed reviewed resolver invokes current behavior exactly once. | Actual registered route and CLI match results, exceptions, output bytes, exit codes and state effects; malformed inputs preserve behavior. | Disable new binding; original CLI remains exercised. |
| M3: native trace correlation | Extend existing native collector at the selected boundary; snapshot metadata before hashes; retain host-issued run/invocation/attempt IDs, parent links and exact terminal result reference/digest. | Retry, duplicate, concurrent, cancellation, crash and cross-run substitution cases preserve contracts; native v2 validation passes. | Stop optional new projections while retaining emitted records and old readers. |
| M4: workflow/historical views | Generate docs and read-only public views through current renderers; validate release-promotion representation; derive versioned historical sidecars without changing original values/status or imputing missing identity. | Original hashes unchanged; missing skill/rationale/mapping remain explicit; rendering invokes no computation/provider; workflow symbols/order unchanged. | Revert projection code/pointers, retain original evidence. |
| M5: bounded acceptance | Run compatibility matrix, two evidence-driven refinements, four persona reviews and final verification; regenerate only from canonical inputs. | Every pilot route exercised, no unexplained new failures, controls/evidence agree; inherited failing aggregate gates keep handoff conditional. | Keep previous integration selected; revert failed slice and reproduce baseline. |

No relocation is required. A later move is a separate change after checking dynamic imports, package resources/data, serialization-qualified names and installed behavior, with tested public facades where needed. Root `pyproject.toml` packages only `agentic/discovery`, `agentic/experiments`, `agentic/operations`, and `agentic/state`; source-tree maintenance scripts are not thereby wheel entrypoints. Test installed packages and alternate working directories only for supported interfaces.

The source and dependency map use A01–A08, while this roadmap uses Abducer-specific M stages. Crosswalk: A01 inventory/baseline → M0; A02 frozen scope/ownership → M0–M1; A03 local contracts → M1–M3; A04 representative adaptation → M2–M3 for the bounded validator only, with executable workflow adoption explicitly deferred; A05 lifecycle/history → M3–M4; A06 scope expansion → deferred beyond the frozen pilot; A07 generated navigation/docs → M4; A08 compatibility record → M5 for the tested pilot, not full-source adoption completion.

## Compatibility and validation

Preserve public imports, commands/options, APIs, strict schemas, serialized identities, configuration precedence, error behavior, provider choices, workflow ordering, transaction boundaries and established output paths. Separate completed execution from rejection or uncertain scientific evidence. Optional logging failures preserve results only where existing policy allows; mandatory durable receipts retain their failure policy.

Compare baseline and candidate fixtures through real entrypoints: return values, exception details, stdout/stderr/exit codes, state effects and invocation counts. Normalize only documented volatile fields, never invocation identity, digest joins or state transitions. Historical views retain source locator/hash and projection version; show “No skill recorded”, “Unassigned” and “Rationale not recorded” where appropriate, without fabricated execution or reasoning.

New independent calls receive distinct host invocation identities even for identical inputs. Retries and duplicate delivery retain native attempt/idempotency/event rules: the current store derives event IDs from its execution context and idempotency key. Do not replace deterministic replay identity with unconditional UUID generation from the kit fixture.

The [test strategy](../../.prism/portable-repository-adoption-plan/04b-test-strategy.md) names representative existing suites and future probes. Use the current locked environment and preserve pre-existing failures against the same source snapshot. Existing root notes report semantic/archive validation debt; remeasure in M0. Kit test success proves only kit behavior. Full adoption compatibility and live provider equivalence are not established by this plan.

Finish the bounded migration when inventory is accounted for, the pilot has real-route contract/provenance evidence, gates pass and limitations are documented. Broader instrumentation, code moves, host domain export and live experiments are deferred rather than prerequisites.
