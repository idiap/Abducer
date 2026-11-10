# Implementation map

The implementation turns the manuscript's research architecture into four
enforced layers:

1. `tdr.domain` defines immutable, versioned records and the common result
   envelope.
2. Atlas, pressure, reflection, generation, relevance, and validation modules
   implement bounded operations with explicit epistemic status.
3. `tdr.skills.catalog` binds all 17 operations to roles, required inputs,
   budgets, human gates, and output kinds.
4. The orchestration and provenance layers serialize guarded transitions,
   content hashes, events, replay, and representation-review routing.

The default generator is deterministic so the complete system can be tested
offline. Any local or hosted model can implement `GeneratorProvider`, but its
outputs remain conjectural and cannot bypass the relevance gates or independent
formal, concrete, and adversarial checks.

Optional formal tools are probed at runtime. Missing tools produce an explicit
unavailable or blocked result; the code never fabricates an external proof.

The `skills/` tree is generated from the executable catalogue and contains the
full portable contract for each skill: `SKILL.md`, input/output schemas, policy,
prompts, tests, examples, wrapper, and agent metadata.
