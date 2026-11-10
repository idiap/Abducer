# Recommended Focus Execution

## 1) Prioritize Top-2 High-Severity Hardness Elements

- Barrier Stack Constraints (high, score=1.0000)
  - Evidence IDs: st.thm.hille-yosida-general, st.thm.hille-yosida-contraction, st.thm.lumer-phillips, st.thm.cauchy-problem-equivalence
- Bridge-Hypothesis Dependence (high, score=1.0000)
  - Evidence IDs: st.thm.hille-yosida-general, st.def.c0-semigroup, st.thm.hille-yosida-contraction, st.thm.lumer-phillips, st.def.generator, st.thm.cauchy-problem-equivalence

## 2) Scratch Dependency Tests + Deduce Checks

- Selected bridge hypotheses: 12
- entailed: 9, conditionally-entailed: 1, not-derived: 2
- Round evidence: `/Users/user/files/abducer/abducer/artifacts/hille-yosida-theorem/round-evidence/round-1.json`
- Post-loop status: supported=13, refuted=0, open=31

## 3) Backfill Explicit depends_on for Top Entrypoints

- Checked top entrypoints: 8
- Dependency coverage OK: 8/8
- Rows:
  - st.thm.hille-yosida-general (theorem): deps=4 -> st.def.c0-semigroup, st.def.generator, st.def.resolvent, st.prop.generator-closed-dense
  - st.def.c0-semigroup (definition): deps=0 -> []
  - st.def.generator (definition): deps=1 -> st.def.c0-semigroup
  - st.thm.cauchy-problem-equivalence (theorem): deps=2 -> st.def.c0-semigroup, st.def.generator
  - st.thm.hille-yosida-contraction (theorem): deps=2 -> st.thm.hille-yosida-general, st.def.resolvent
  - st.thm.lumer-phillips (theorem): deps=1 -> st.thm.hille-yosida-contraction
  - st.def.resolvent (definition): deps=0 -> []
  - st.prop.generator-closed-dense (proposition): deps=2 -> st.def.c0-semigroup, st.def.generator

## 4) Anti-Barrier Program: Keep Coherence-Positive Re-Encodings

- Retained (coherence delta >= 0): 17
- Rejected (coherence delta < 0): 0
- Global coherence (original): 0.608311
- Global coherence (revised): 0.573588
- Revised delta: -0.034723
- Coherence-positive revised PHYP: `/Users/user/files/abducer/abducer/artifacts/hille-yosida-theorem/phyp.revised.coherence-positive.yaml` (43 hypotheses)
- Decision: reject-global-reencoding-keep-local-positive (Revised re-encoding decreased global coherence; keep original KB and retain only local coherence-positive barrier hypotheses.)
