# Essential Concept Bridge Plan

## Stats

- Input connection candidates: 40
- Bridge programs: 20
- Concept axes: 7

## Top Bridge Programs

| bridge_id | from_id | to_id | type | tier | score | expl | coh | concept | commit | concept_evidence |
|---|---|---|---|---|---|---|---|---|---|---|
| bridge.009 | st.def.os-euclidean-qft | st.def.osterwalder-schrader-os-euclidean-qft | OS-to-Wightman-to-gap bridge | B | 0.5981 | 0.7843 | 0.0135 | 0.87 | 0.85 | reflection-positivity-and-transfer-matrix, reflection-positive-transfer-matrix, OS-axioms-and-reflection-positivity, positive-self-adjoint-Hamiltonian |
| bridge.001 | st.def.os-euclidean-qft | st.thm.os-reconstruction-and-equivalence-with-wightman- | OS-to-Wightman-to-gap bridge | B | 0.5612 | 0.5068 | 0.0062 | 0.5904 | 1.0 | reflection-positivity-and-transfer-matrix, reflection-positive-transfer-matrix, OS-axioms-and-reflection-positivity, positive-self-adjoint-Hamiltonian |
| bridge.004 | st.def.wightman-qft | st.thm.constructive-qft-in-low-dimension-examples-with- | OS-to-Wightman-to-gap bridge | B | 0.5444 | 0.5549 | 0.0135 | 0.2525 | 1.0 | rigorous-Yang-Mills-construction, constructive-existence, Hamiltonian-mass-gap, constructive-qft |
| bridge.006 | st.def.mass-gap | st.thm.euclidean-correlator-decay-as-a-mass-gap-signatu | transfer-matrix-to-gap bridge | B | 0.5399 | 0.4881 | 0.0061 | 0.4713 | 1.0 | transfer-matrix-gap-implies-correlator-decay, exponential-correlation-decay, reflection-positivity-and-transfer-matrix, reflection-positive-transfer-matrix |
| bridge.003 | st.def.os-euclidean-qft | st.thm.euclidean-correlator-decay-as-a-mass-gap-signatu | correlator-decay-to-gap bridge | B | 0.5339 | 0.4613 | 0.0061 | 0.409 | 1.0 | reflection-positivity-and-transfer-matrix, reflection-positive-transfer-matrix, OS-axioms-and-reflection-positivity, positive-self-adjoint-Hamiltonian |
| bridge.005 | st.def.wightman-qft | st.thm.os-reconstruction-and-equivalence-with-wightman- | OS-to-Wightman-to-gap bridge | B | 0.5316 | 0.4844 | 0.0061 | 0.2297 | 1.0 | rigorous-Yang-Mills-construction, classical-Yang-Mills-PDE, constructive-existence, classical-pde-analysis |
| bridge.011 | st.def.wightman-qft | st.thm.balaban-s-rigorous-renormalisation-group-analysi | OS-to-Wightman-to-gap bridge | B | 0.5206 | 0.5123 | 0.006 | 0.2094 | 1.0 | rigorous-Yang-Mills-construction, constructive-existence, Hamiltonian-mass-gap, constructive-qft |
| bridge.012 | st.def.mass-gap | st.thm.strong-coupling-exponential-decay-and-a-lattice- | transfer-matrix-to-gap bridge | B | 0.5178 | 0.4478 | 0.006 | 0.5102 | 0.85 | transfer-matrix-gap-implies-correlator-decay, exponential-correlation-decay, reflection-positivity-and-transfer-matrix, reflection-positive-transfer-matrix |
| bridge.013 | st.def.osterwalder-schrader-os-euclidean-qft | st.thm.os-reconstruction | OS-to-Wightman-to-gap bridge | B | 0.5141 | 0.5214 | 0.006 | 0.5867 | 0.85 | OS-axioms-and-reflection-positivity, rigorous-Yang-Mills-construction, OS-axioms-imply-Wightman-QFT, Wightman-QFT-realization |
| bridge.014 | st.def.mass-gap | st.thm.os-reconstruction-and-equivalence-with-wightman- | transfer-matrix-to-gap bridge | B | 0.5036 | 0.4124 | 0.006 | 0.2939 | 1.0 | reflection-positivity-and-transfer-matrix, reflection-positive-transfer-matrix, positive-self-adjoint-Hamiltonian, rigorous-Yang-Mills-construction |
| bridge.016 | st.def.os-euclidean-qft | st.thm.reflection-positivity-and-transfer-matrix-for-la | transfer-matrix-to-gap bridge | B | 0.4987 | 0.3744 | 0.006 | 0.3363 | 1.0 | reflection-positivity-and-transfer-matrix, reflection-positive-transfer-matrix, OS-axioms-and-reflection-positivity, positive-self-adjoint-Hamiltonian |
| bridge.019 | st.def.wightman-qft | st.thm.two-dimensional-abelian-higgs-model-without-cuto | OS-to-Wightman-to-gap bridge | B | 0.4928 | 0.3022 | 0.006 | 0.2949 | 1.0 | rigorous-Yang-Mills-construction, constructive-existence, constructive-qft |
| bridge.018 | st.def.wightman-qft | st.thm.four-dimensional-yang-mills-with-an-infrared-cut | OS-to-Wightman-to-gap bridge | B | 0.4907 | 0.338 | 0.006 | 0.1979 | 1.0 | rigorous-Yang-Mills-construction, constructive-existence, Hamiltonian-mass-gap, constructive-qft |
| bridge.002 | st.def.compact-simple-gauge-group | st.thm.donaldson-s-gauge-theoretic-constraints-on-smoot | barrier-aware transfer bridge | B | 0.488 | 0.4934 | 0.0135 | 0.0955 | 0.6 | geometric-analysis, gauge-theory, Yang-Mills |
| bridge.007 | st.def.compact-simple-gauge-group | st.thm.adhm-classification-all-instantons-on-s-4 | barrier-aware transfer bridge | B | 0.4856 | 0.4589 | 0.0061 | 0.122 | 0.75 | compact-simple-gauge-group, geometric-analysis, gauge-theory |
| bridge.008 | st.def.compact-simple-gauge-group | st.thm.uhlenbeck-gauge-fixing-and-compactness | barrier-aware transfer bridge | B | 0.4826 | 0.48 | 0.0135 | 0.0576 | 0.75 | geometric-analysis, gauge-theory, Yang-Mills |
| bridge.010 | st.def.compact-simple-gauge-group | st.thm.bpst-instanton-existence-prototype-instanton | barrier-aware transfer bridge | B | 0.4753 | 0.4761 | 0.0061 | 0.128 | 0.6 | compact-simple-gauge-group, geometric-analysis, gauge-theory, Yang-Mills |
| bridge.015 | st.def.compact-simple-gauge-group | st.thm.two-dimensional-abelian-higgs-model-without-cuto | barrier-aware transfer bridge | B | 0.4735 | 0.4004 | 0.006 | 0.1825 | 0.75 | compact-simple-gauge-group, gauge-theory, Yang-Mills |
| bridge.035 | st.def.mass-gap | st.def.mass-gap-in-hamiltonian-wightman-terms | transfer-matrix-to-gap bridge | B | 0.4646 | 0.6954 | 0.0 | 0.7602 | 0.0 | transfer-matrix-gap-implies-correlator-decay, exponential-correlation-decay, reflection-positivity-and-transfer-matrix, reflection-positive-transfer-matrix |
| bridge.020 | st.def.compact-simple-gauge-group | st.thm.yang-mills-on-riemann-surfaces-atiyah-bott | barrier-aware transfer bridge | B | 0.4598 | 0.3857 | 0.006 | 0.082 | 0.75 | geometric-analysis, gauge-theory, Yang-Mills |

## Mathematical Commitments

### bridge.009 (st.def.os-euclidean-qft -> st.def.osterwalder-schrader-os-euclidean-qft)
- Antecedent schema: reflection-positivity-and-transfer-matrix
- Target consequence: positive-self-adjoint-Hamiltonian
- Preserved invariant: OS-to-Wightman mass-gap transfer in Wightman-QFT
- Barrier scope: none
- Invariant basis: reflection-positivity-and-transfer-matrix, reflection-positive-transfer-matrix, OS-axioms-and-reflection-positivity, positive-self-adjoint-Hamiltonian, rigorous-Yang-Mills-construction, reflection-positivity-transfer

### bridge.001 (st.def.os-euclidean-qft -> st.thm.os-reconstruction-and-equivalence-with-wightman-)
- Antecedent schema: reflection-positivity-and-transfer-matrix
- Target consequence: positive-self-adjoint-Hamiltonian
- Preserved invariant: OS-to-Wightman mass-gap transfer in Hamiltonian-mass-gap
- Barrier scope: continuum-limit
- Invariant basis: reflection-positivity-and-transfer-matrix, reflection-positive-transfer-matrix, OS-axioms-and-reflection-positivity, positive-self-adjoint-Hamiltonian, rigorous-Yang-Mills-construction, reflection-positivity-transfer

### bridge.004 (st.def.wightman-qft -> st.thm.constructive-qft-in-low-dimension-examples-with-)
- Antecedent schema: constructive-existence
- Target consequence: rigorous-Yang-Mills-construction
- Preserved invariant: OS-to-Wightman mass-gap transfer in Hamiltonian-mass-gap
- Barrier scope: ultraviolet-control
- Invariant basis: rigorous-Yang-Mills-construction, constructive-existence, Hamiltonian-mass-gap, positive-mass-gap, Wightman-QFT

### bridge.006 (st.def.mass-gap -> st.thm.euclidean-correlator-decay-as-a-mass-gap-signatu)
- Antecedent schema: reflection-positivity-and-transfer-matrix
- Target consequence: positive-self-adjoint-Hamiltonian
- Preserved invariant: transfer-matrix spectral witness in reflection-positive-transfer-matrix
- Barrier scope: continuum-limit
- Invariant basis: transfer-matrix-gap-implies-correlator-decay, reflection-positivity-and-transfer-matrix, reflection-positive-transfer-matrix, positive-self-adjoint-Hamiltonian, correlator-decay-signals-mass-gap, rigorous-Yang-Mills-construction

### bridge.003 (st.def.os-euclidean-qft -> st.thm.euclidean-correlator-decay-as-a-mass-gap-signatu)
- Antecedent schema: reflection-positivity-and-transfer-matrix
- Target consequence: positive-self-adjoint-Hamiltonian
- Preserved invariant: correlator-decay mass-gap witness in Schwinger-function-decay
- Barrier scope: continuum-limit
- Invariant basis: reflection-positivity-and-transfer-matrix, reflection-positive-transfer-matrix, OS-axioms-and-reflection-positivity, positive-self-adjoint-Hamiltonian, rigorous-Yang-Mills-construction, reflection-positivity-transfer

### bridge.005 (st.def.wightman-qft -> st.thm.os-reconstruction-and-equivalence-with-wightman-)
- Antecedent schema: constructive-existence
- Target consequence: positive-self-adjoint-Hamiltonian
- Preserved invariant: OS-to-Wightman mass-gap transfer in Hamiltonian-mass-gap
- Barrier scope: continuum-limit
- Invariant basis: positive-self-adjoint-Hamiltonian, rigorous-Yang-Mills-construction, continuum-limit-candidate, classical-Yang-Mills-PDE, Wightman-QFT-realization, constructive-existence

### bridge.011 (st.def.wightman-qft -> st.thm.balaban-s-rigorous-renormalisation-group-analysi)
- Antecedent schema: constructive-existence
- Target consequence: rigorous-Yang-Mills-construction
- Preserved invariant: OS-to-Wightman mass-gap transfer in Hamiltonian-mass-gap
- Barrier scope: open-construction-gap + ultraviolet-control
- Invariant basis: rigorous-Yang-Mills-construction, constructive-existence, Hamiltonian-mass-gap, positive-mass-gap, Wightman-QFT

### bridge.012 (st.def.mass-gap -> st.thm.strong-coupling-exponential-decay-and-a-lattice-)
- Antecedent schema: reflection-positivity-and-transfer-matrix
- Target consequence: positive-self-adjoint-Hamiltonian
- Preserved invariant: transfer-matrix spectral witness in reflection-positive-transfer-matrix
- Barrier scope: none
- Invariant basis: transfer-matrix-gap-implies-correlator-decay, reflection-positivity-and-transfer-matrix, reflection-positive-transfer-matrix, positive-self-adjoint-Hamiltonian, correlator-decay-signals-mass-gap, reflection-positivity-transfer

### bridge.013 (st.def.osterwalder-schrader-os-euclidean-qft -> st.thm.os-reconstruction)
- Antecedent schema: reflection-positivity-and-transfer-matrix
- Target consequence: rigorous-Yang-Mills-construction
- Preserved invariant: OS-to-Wightman mass-gap transfer in Hamiltonian-mass-gap
- Barrier scope: none
- Invariant basis: reflection-positivity-and-transfer-matrix, OS-axioms-and-reflection-positivity, rigorous-Yang-Mills-construction, OS-axioms-imply-Wightman-QFT, Wightman-QFT-realization, Schwinger-function-decay

### bridge.014 (st.def.mass-gap -> st.thm.os-reconstruction-and-equivalence-with-wightman-)
- Antecedent schema: reflection-positivity-and-transfer-matrix
- Target consequence: positive-self-adjoint-Hamiltonian
- Preserved invariant: transfer-matrix spectral witness in reflection-positive-transfer-matrix
- Barrier scope: continuum-limit
- Invariant basis: reflection-positivity-and-transfer-matrix, reflection-positive-transfer-matrix, positive-self-adjoint-Hamiltonian, rigorous-Yang-Mills-construction, reflection-positivity-transfer, continuum-limit-candidate

## Bridge Axes

### euclidean-os-framework -> euclidean-os-framework
- Count: 1
- bridge.009: st.def.os-euclidean-qft -> st.def.osterwalder-schrader-os-euclidean-qft (score=0.5981)

### euclidean-os-framework -> wightman-hamiltonian-framework
- Count: 2
- bridge.001: st.def.os-euclidean-qft -> st.thm.os-reconstruction-and-equivalence-with-wightman- (score=0.5612)
- bridge.013: st.def.osterwalder-schrader-os-euclidean-qft -> st.thm.os-reconstruction (score=0.5141)

### wightman-hamiltonian-framework -> Bottlenecks, Barriers, and Open Gaps
- Count: 4
- bridge.004: st.def.wightman-qft -> st.thm.constructive-qft-in-low-dimension-examples-with- (score=0.5444)
- bridge.011: st.def.wightman-qft -> st.thm.balaban-s-rigorous-renormalisation-group-analysi (score=0.5206)
- bridge.019: st.def.wightman-qft -> st.thm.two-dimensional-abelian-higgs-model-without-cuto (score=0.4928)

### wightman-hamiltonian-framework -> mass-gap-and-spectral-transfer
- Count: 2
- bridge.006: st.def.mass-gap -> st.thm.euclidean-correlator-decay-as-a-mass-gap-signatu (score=0.5399)
- bridge.012: st.def.mass-gap -> st.thm.strong-coupling-exponential-decay-and-a-lattice- (score=0.5178)

### euclidean-os-framework -> mass-gap-and-spectral-transfer
- Count: 2
- bridge.003: st.def.os-euclidean-qft -> st.thm.euclidean-correlator-decay-as-a-mass-gap-signatu (score=0.5339)
- bridge.016: st.def.os-euclidean-qft -> st.thm.reflection-positivity-and-transfer-matrix-for-la (score=0.4987)

### wightman-hamiltonian-framework -> wightman-hamiltonian-framework
- Count: 3
- bridge.005: st.def.wightman-qft -> st.thm.os-reconstruction-and-equivalence-with-wightman- (score=0.5316)
- bridge.014: st.def.mass-gap -> st.thm.os-reconstruction-and-equivalence-with-wightman- (score=0.5036)
- bridge.035: st.def.mass-gap -> st.def.mass-gap-in-hamiltonian-wightman-terms (score=0.4646)

### Foundational Gauge-Theoretic Definitions -> Bottlenecks, Barriers, and Open Gaps
- Count: 6
- bridge.002: st.def.compact-simple-gauge-group -> st.thm.donaldson-s-gauge-theoretic-constraints-on-smoot (score=0.488)
- bridge.007: st.def.compact-simple-gauge-group -> st.thm.adhm-classification-all-instantons-on-s-4 (score=0.4856)
- bridge.008: st.def.compact-simple-gauge-group -> st.thm.uhlenbeck-gauge-fixing-and-compactness (score=0.4826)

## Recommended Run Order

1. bridge.009
2. bridge.001
3. bridge.004
4. bridge.006
5. bridge.003
6. bridge.005
