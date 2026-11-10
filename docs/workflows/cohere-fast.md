# Cohere-fast workflow

`cohere-fast` is an isolated, opt-in research workflow. It adapts selected methods from the Discover source archive without replacing Abducer's control plane or changing any existing workflow.

## Invocation

```text
cohere-fast <domain> [subworkflow]
```

The initial domain is `ym`:

```text
cohere-fast ym
cohere-fast ym adaptive_frontier
cohere-fast ym derivation_and_proof
cohere-fast ym independent_audit
cohere-fast ym manuscript_release
```

The command must be explicit. Generic discussion of Yang--Mills, `cohere-fast` without a domain, unknown domains, and free-text approximations do not activate the workflow. Activation produces a receipt binding the canonical workflow ID `cohere_fast`, version, domain, optional child workflow, target, and run.

## Conceptual structure

```text
DomainRunRequest(domain=ym)
        |
        v
  [scope_and_ground]
        |
        v
  [adaptive_frontier] ----(reframe/stop)----+
        |                                    |
        v                                    |
  [derivation_and_proof] --(gap/quarantine)-+
        |
        v
  [independent_audit] -----(reject/revise)---+
        |
        +-- if scientifically ready --> [manuscript_release]
        |
        `-----------------------------> DomainClosureDecision
```

Each child consumes and returns typed packets. A child cannot mutate its parent directly. A failed, quarantined, or rejected child cannot advance to manuscript release. Handoffs carry scope, provenance, uncertainty, claim ceiling, and open obligations; they do not carry proof, truth, or publication authority.

## Isolation

- Runs and artifacts live under a `cohere-fast/<domain>/<run>` namespace.
- Only skills named by the bound domain bundle can be authorized.
- No existing workflow may invoke a cohere-fast domain skill.
- Cohere-fast has no implicit handoff into an existing workflow.
- Disabling the registry removes the active route without deleting historical receipts.
- The imported `tdr` package, CLI, planner, and SQLite store are not Abducer runtime authorities.

## Yang--Mills domain bundle

The YM bundle lives under `skills/domain_specific/ym`. It is a critically adapted research-method suite, not a validated solution of the Yang--Mills existence and mass-gap problem. Existing Abducer Yang--Mills skills are not overwritten. Colliding source skills are mapped explicitly to reuse, namespaced adaptation, or rejection.

The programme separates:

- target and literature grounding;
- finite regulator, observable, and representation work;
- RG, rigidity, continuum, and Osterwalder--Schrader obligations;
- calibration and mechanized checks;
- independent frontier audit;
- conditional manuscript projection.

Claim levels `C0` through `C6` describe programme position, not epistemic truth. Artifact integrity, workflow disposition, epistemic status, and claim level remain independent. In particular, finite or restricted-model evidence cannot establish a continuum mass gap, and a valid event hash establishes integrity rather than scientific correctness.

## Reasoning trace

Public events record workflow, domain, child workflow, parent lineage, step, attempt, typed premises, public warrant, conclusion, evidence, alternatives, falsifiers, scope, uncertainty, claim level, authority, obligations, and gate outcome. They never request or store hidden chain-of-thought.

HTML and PDF reports are projections of the same validated packet. Synthetic fixtures must be labeled as such; only live execution receipts can establish runtime exercise or downstream consumption.

## Failure and recovery

- `stop`: terminate the run; no later child may execute.
- `quarantine`: retain artifacts and obligations but deny promotion.
- `retry`: create a new attempt bound to the same immutable inputs.
- `resume`: continue only from an authorized durable receipt.
- `reject`: preserve the failed claim and evidence; manuscript release remains unavailable.

The release gate requires source authorization, complete dispositions, validated skill and artifact contracts, realistic execution, hook denial coverage, live trace parity, script isolation, and noninterference regression evidence.
