#!/usr/bin/env python3
# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Build a cited target-problem and literature-evolution packet."""

from __future__ import annotations

from typing import Any

from agentic_common import ROOT, clean_text, load_optional_json, rel, utc_now, write_json
from discovery_marathon_common import write_markdown


CURRENT_TARGET = ROOT / "agentic/state/current_target.json"
ACTIVE_RUN_POINTER = ROOT / "agentic/runs/discovery_marathons/active_run.json"
LATEST_MARATHON_REPORT = ROOT / "agentic/reports/discovery_marathon/latest.json"
OUT_DIR = ROOT / "agentic/reports/target_literature_evolution"
OUT_JSON = OUT_DIR / "latest.json"
OUT_MD = OUT_DIR / "latest.md"


def yang_mills_references() -> list[dict[str, Any]]:
    return [
        {
            "ref_id": "ref.yang-mills-1954",
            "year": 1954,
            "authors": "C. N. Yang and R. L. Mills",
            "title": "Conservation of Isotopic Spin and Isotopic Gauge Invariance",
            "venue": "Physical Review 96, 191-195",
            "url": "https://link.aps.org/doi/10.1103/PhysRev.96.191",
            "role": "origin",
            "status": "primary",
            "supports": "Introduces non-abelian gauge fields and the classical Yang-Mills object that later becomes the quantum target.",
            "limitation": "It is a classical field-theoretic origin paper, not a constructive quantum existence or mass-gap proof.",
        },
        {
            "ref_id": "ref.streater-wightman-1964",
            "year": 1964,
            "authors": "R. F. Streater and A. S. Wightman",
            "title": "PCT, Spin and Statistics, and All That",
            "venue": "W. A. Benjamin; later Princeton University Press",
            "url": "https://ui.adsabs.harvard.edu/abs/2001pssa.book.....S/abstract",
            "role": "axiomatic_bridge",
            "status": "canonical",
            "supports": "Provides the Wightman-style axiomatic target standard for relativistic quantum field theory.",
            "limitation": "It supplies the standard to satisfy; it does not construct four-dimensional Yang-Mills.",
        },
        {
            "ref_id": "ref.os-1973-1975",
            "year": 1973,
            "authors": "K. Osterwalder and R. Schrader",
            "title": "Axioms for Euclidean Green's Functions I-II",
            "venue": "Communications in Mathematical Physics 31 and 42",
            "url": "https://ncatlab.org/nlab/show/Osterwalder-Schrader%2Btheorem",
            "role": "axiomatic_bridge",
            "status": "canonical",
            "supports": "Turns Euclidean Schwinger-function control, especially reflection positivity, into a route toward Wightman reconstruction.",
            "limitation": "The theorem gives a reconstruction criterion; Yang-Mills still needs Schwinger functions satisfying the hypotheses in the continuum limit.",
        },
        {
            "ref_id": "ref.gross-wilczek-1973",
            "year": 1973,
            "authors": "D. J. Gross and F. Wilczek",
            "title": "Ultraviolet Behavior of Non-Abelian Gauge Theories",
            "venue": "Physical Review Letters 30, 1343-1346",
            "url": "https://link.aps.org/doi/10.1103/PhysRevLett.30.1343",
            "role": "physics_motivation",
            "status": "primary",
            "supports": "Asymptotic freedom explains why non-abelian gauge theory can be weakly coupled at short distance while remaining nonperturbative in the infrared.",
            "limitation": "Perturbative ultraviolet control does not by itself construct the full theory or prove a positive mass gap.",
        },
        {
            "ref_id": "ref.politzer-1973",
            "year": 1973,
            "authors": "H. D. Politzer",
            "title": "Reliable Perturbative Results for Strong Interactions?",
            "venue": "Physical Review Letters 30, 1346-1349",
            "url": "https://link.aps.org/doi/10.1103/PhysRevLett.30.1346",
            "role": "physics_motivation",
            "status": "primary",
            "supports": "Independent asymptotic-freedom result reinforcing the ultraviolet side of the Yang-Mills/QCD picture.",
            "limitation": "It motivates the short-distance regime; it does not solve infrared confinement or the constructive problem.",
        },
        {
            "ref_id": "ref.wilson-1974",
            "year": 1974,
            "authors": "K. G. Wilson",
            "title": "Confinement of Quarks",
            "venue": "Physical Review D 10, 2445",
            "url": "https://link.aps.org/doi/10.1103/PhysRevD.10.2445",
            "role": "physics_motivation",
            "status": "primary",
            "supports": "Introduces lattice gauge theory and strong-coupling confinement mechanisms that make a mass gap physically plausible.",
            "limitation": "Strong-coupling lattice confinement is not the same as a continuum four-dimensional Clay-problem proof.",
        },
        {
            "ref_id": "ref.glimm-jaffe-1981",
            "year": 1981,
            "authors": "J. Glimm and A. Jaffe",
            "title": "Quantum Physics: A Functional Integral Point of View",
            "venue": "Springer",
            "url": "https://books.google.com/books/about/Quantum_Physics.html?id=VSjjBwAAQBAJ",
            "role": "constructive_program",
            "status": "canonical",
            "supports": "Shows what rigorous constructive quantum field theory can look like and why existence is a mathematical construction problem, not only a physics argument.",
            "limitation": "The classic constructive successes do not include a full four-dimensional Yang-Mills solution.",
        },
        {
            "ref_id": "ref.seiler-1982",
            "year": 1982,
            "authors": "E. Seiler",
            "title": "Gauge Theories as a Problem of Constructive Quantum Field Theory and Statistical Mechanics",
            "venue": "Springer Lecture Notes in Physics",
            "url": "https://doi.org/10.1007/BFb0090332",
            "role": "constructive_program",
            "status": "expert_survey",
            "supports": "Frames gauge theories as constructive field-theory and statistical-mechanics problems with lattice-to-continuum pressure.",
            "limitation": "It clarifies the program and obstacles rather than closing the four-dimensional continuum mass-gap problem.",
        },
        {
            "ref_id": "ref.balaban-1985",
            "year": 1985,
            "authors": "T. Balaban",
            "title": "Ultraviolet Stability of Three-Dimensional Lattice Pure Gauge Field Theories",
            "venue": "Communications in Mathematical Physics 102, 255-275",
            "url": "https://inspirehep.net/literature/16302",
            "role": "constructive_program",
            "status": "primary",
            "supports": "Represents a rigorous renormalization-group route toward ultraviolet stability for lattice gauge theories.",
            "limitation": "Ultraviolet stability and related RG control still need same-theory continuum construction, nontriviality, and spectral-gap witnesses.",
        },
        {
            "ref_id": "ref.jaffe-witten-clay",
            "year": 2000,
            "authors": "A. Jaffe and E. Witten",
            "title": "Quantum Yang-Mills Theory",
            "venue": "Clay Mathematics Institute Millennium Problem statement",
            "url": "https://www.claymath.org/wp-content/uploads/2022/06/yangmills.pdf",
            "role": "problem_statement",
            "status": "canonical",
            "supports": "Gives the Clay target: construct nontrivial quantum Yang-Mills on four-dimensional space and prove a positive mass gap for compact simple gauge group.",
            "limitation": "It defines the target and admissible rigor standard; it is not a solution.",
        },
        {
            "ref_id": "ref.douglas-2004",
            "year": 2004,
            "authors": "M. R. Douglas",
            "title": "Report on the Status of the Yang-Mills Millennium Prize Problem",
            "venue": "Clay Mathematics Institute annual report",
            "url": "https://www.claymath.org/library/annual_report/douglas_quantum_yang_mills.pdf",
            "role": "route_obstruction",
            "status": "expert_survey",
            "supports": "Explains the status and difficulty of turning physical Yang-Mills understanding into a rigorous Millennium-problem solution.",
            "limitation": "It is a status report, not a proof or definitive taxonomy of all later approaches.",
        },
    ]


def yang_mills_stages() -> list[dict[str, Any]]:
    return [
        {
            "stage_id": "stage-01-gauge-object",
            "period": "1954",
            "title": "The non-abelian gauge object is born",
            "core_shift": "Yang and Mills replace an abelian electromagnetic-style gauge field with a nonlinear non-abelian gauge field.",
            "what_became_possible": "The target object becomes a rich classical field theory with compact gauge-group structure.",
            "what_remained_open": "There is still no rigorous quantum field theory, no Hilbert space, and no mass-gap statement.",
            "refs": ["ref.yang-mills-1954"],
        },
        {
            "stage_id": "stage-02-axiomatic-standard",
            "period": "1960s-1970s",
            "title": "The rigor standard becomes axiomatic and Euclidean",
            "core_shift": "Wightman axioms set a Lorentzian QFT standard; Osterwalder-Schrader theory makes Euclidean Schwinger functions a possible reconstruction route.",
            "what_became_possible": "A proof can aim at Euclidean objects, but only if reflection positivity, covariance, regularity, clustering, and reconstruction hypotheses are preserved.",
            "what_remained_open": "The Yang-Mills Schwinger functions still have to be constructed nonperturbatively in four dimensions.",
            "refs": ["ref.streater-wightman-1964", "ref.os-1973-1975"],
        },
        {
            "stage_id": "stage-03-physics-mechanism",
            "period": "1973-1974",
            "title": "Asymptotic freedom and lattice confinement reshape expectations",
            "core_shift": "The literature clarifies the ultraviolet/infrared split: perturbation theory can work at short distances, while lattice strong coupling suggests confinement and massive glueball-like excitations.",
            "what_became_possible": "The problem stops looking physically arbitrary: a gap is expected, and lattice regularization gives concrete finite systems to analyze.",
            "what_remained_open": "Short-distance perturbation and strong-coupling lattice arguments do not bridge to the continuum Clay target by themselves.",
            "refs": ["ref.gross-wilczek-1973", "ref.politzer-1973", "ref.wilson-1974"],
        },
        {
            "stage_id": "stage-04-constructive-pressure",
            "period": "1980s",
            "title": "Constructive QFT and RG expose the real mathematical bottleneck",
            "core_shift": "The literature shows that existence means constructing measures, Schwinger functions, limits, and reconstruction data with uniform control, not merely writing a path integral.",
            "what_became_possible": "Balaban-style RG and constructive-field methods give a disciplined route language: cutoffs, ultraviolet stability, lattice-to-continuum control, and limiting objects.",
            "what_remained_open": "The full four-dimensional continuum Yang-Mills object, nontriviality, OS/Wightman adequacy, and positive spectral gap remain coupled obligations.",
            "refs": ["ref.glimm-jaffe-1981", "ref.seiler-1982", "ref.balaban-1985"],
        },
        {
            "stage_id": "stage-05-millennium-formulation",
            "period": "2000 onward",
            "title": "The Clay formulation fuses construction and mass gap into one target",
            "core_shift": "The problem becomes a same-theory requirement: construct the nontrivial theory and prove the positive gap for that reconstructed theory.",
            "what_became_possible": "Discovery work can be audited against explicit commitments: existence, nontriviality, OS/Wightman adequacy, continuum limit, and positive mass gap.",
            "what_remained_open": "Most proposed routes risk solving a regulated, perturbative, lower-dimensional, numerical, or proxy problem unless same-theory transfer is certified.",
            "refs": ["ref.jaffe-witten-clay", "ref.douglas-2004"],
        },
    ]


def build_yang_mills_report(target: dict[str, Any]) -> dict[str, Any]:
    refs = yang_mills_references()
    refs_by_id = {row["ref_id"]: row for row in refs}
    stages = []
    for stage in yang_mills_stages():
        cited = [refs_by_id[ref_id] for ref_id in stage["refs"] if ref_id in refs_by_id]
        stages.append({**stage, "citations": cited})
    return {
        "version": 1,
        "generated_utc": utc_now(),
        "target_id": target.get("target_id", "yang-mills-existence-and-mass-gap-target"),
        "problem_name": "Yang-Mills existence and mass gap",
        "problem_statement": {
            "accessible": "Construct a nontrivial four-dimensional quantum Yang-Mills theory for every compact simple gauge group and prove a strictly positive mass gap.",
            "formal_shape": r"\exists\ \mathrm{QYM}_G(\mathbb R^4)\ \mathrm{nontrivial},\quad \Delta_G>0",
            "source_ref_id": "ref.jaffe-witten-clay",
        },
        "why_it_matters": [
            "It asks for the first complete nonperturbative construction of a physically central four-dimensional interacting quantum gauge theory.",
            "It would turn the physicists' confinement and glueball mass-gap picture into a theorem in a reconstructed quantum field theory.",
            "It is a stress test for whether constructive QFT, Euclidean reconstruction, lattice gauge theory, and renormalization can meet in one same-theory proof.",
        ],
        "solution_criteria": [
            "The quantum Yang-Mills theory must be constructed, not postulated.",
            "The theory must be nontrivial and satisfy axioms at least as strong as the Wightman/OS standard required by the Clay formulation.",
            "The continuum limit must preserve the same gauge theory and observable algebra.",
            "The Hamiltonian or equivalent reconstructed spectral object must have no non-vacuum spectrum arbitrarily close to zero.",
        ],
        "literature_stages": stages,
        "workflow_implications": [
            {
                "lesson": "Every promising finite or lattice calculation must carry a same-theory transfer certificate.",
                "active_workflow_effect": "Branch ranking should reward calculations that state source object, target object, cutoff regime, and continuum handoff.",
                "refs": ["ref.wilson-1974", "ref.jaffe-witten-clay"],
            },
            {
                "lesson": "Euclidean positivity is not a cosmetic condition; it is the bridge from Schwinger data to Hilbert-space spectral claims.",
                "active_workflow_effect": "OS/reflection-positivity branches should remain central, but only when they keep reconstruction assumptions explicit.",
                "refs": ["ref.os-1973-1975", "ref.streater-wightman-1964"],
            },
            {
                "lesson": "Asymptotic freedom controls the ultraviolet story but leaves the infrared gap and construction problem alive.",
                "active_workflow_effect": "The loop should avoid mistaking perturbative UV success for nonperturbative continuum construction.",
                "refs": ["ref.gross-wilczek-1973", "ref.politzer-1973"],
            },
            {
                "lesson": "Constructive/RG work teaches that uniform estimates and limiting objects are the proof currency.",
                "active_workflow_effect": "Next analyses should prefer bounded estimates, falsifiers, and bridge lemmas over broad route enthusiasm.",
                "refs": ["ref.glimm-jaffe-1981", "ref.balaban-1985", "ref.seiler-1982"],
            },
        ],
        "open_obligations": [
            "Construct continuum Schwinger functions or equivalent fields for the same Yang-Mills object.",
            "Preserve reflection positivity and reconstruction hypotheses in the limit.",
            "Show nontriviality rather than collapse to a free, Gaussian, empty, or proxy theory.",
            "Turn Euclidean decay or Hamiltonian estimates into a positive spectral gap for the reconstructed physical Hilbert space.",
            "Certify that all steps refer to the same compact-simple-gauge Yang-Mills theory on four-dimensional space.",
        ],
        "references": refs,
        "required_skills": [
            "target-literature-source-curator",
            "target-literature-evolution-narrator",
            "prior-art-importer",
            "evidence-acquisition-planner",
        ],
        "source_artifacts": [rel(CURRENT_TARGET), "KB/yang-mills-existence-and-mass-gap.kb.md"],
    }


def pvsnp_references() -> list[dict[str, Any]]:
    return [
        {
            "ref_id": "ref.cook-1971",
            "year": 1971,
            "authors": "S. A. Cook",
            "title": "The Complexity of Theorem-Proving Procedures",
            "venue": "Proceedings of the Third Annual ACM Symposium on Theory of Computing",
            "url": "https://dl.acm.org/doi/10.1145/800157.805047",
            "role": "problem_statement",
            "status": "primary",
            "supports": "Introduces NP-completeness through satisfiability and turns efficient verification into a universal problem.",
            "limitation": "It defines the central complete problem and reduction method; it does not separate deterministic from nondeterministic polynomial time.",
        },
        {
            "ref_id": "ref.karp-1972",
            "year": 1972,
            "authors": "R. M. Karp",
            "title": "Reducibility Among Combinatorial Problems",
            "venue": "Complexity of Computer Computations",
            "url": "https://link.springer.com/chapter/10.1007/978-1-4684-2001-2_9",
            "role": "origin",
            "status": "primary",
            "supports": "Shows that many natural search and optimization problems share the same NP-complete core.",
            "limitation": "NP-completeness transfers difficulty conditionally; it does not prove that any NP-complete problem lacks polynomial algorithms.",
        },
        {
            "ref_id": "ref.baker-gill-solovay-1975",
            "year": 1975,
            "authors": "T. Baker, J. Gill, and R. Solovay",
            "title": "Relativizations of the P = ? NP Question",
            "venue": "SIAM Journal on Computing",
            "url": "https://epubs.siam.org/doi/10.1137/0204037",
            "role": "barrier",
            "status": "canonical",
            "supports": "Shows that relativizing methods alone cannot settle P vs NP, because oracle worlds exist on both sides.",
            "limitation": "Relativization is a diagnostic for proof techniques, not a proof that separation is impossible.",
        },
        {
            "ref_id": "ref.razborov-rudich-1997",
            "year": 1997,
            "authors": "A. A. Razborov and S. Rudich",
            "title": "Natural Proofs",
            "venue": "Journal of Computer and System Sciences",
            "url": "https://www.sciencedirect.com/science/article/pii/S002200009791494X",
            "role": "barrier",
            "status": "canonical",
            "supports": "Explains why many combinatorial lower-bound properties are too large and constructive to prove strong general circuit lower bounds under cryptographic hardness assumptions.",
            "limitation": "The barrier constrains a proof format; it leaves room for non-natural, nonconstructive, algebraic, or otherwise barrier-evading arguments.",
        },
        {
            "ref_id": "ref.aaronson-wigderson-2009",
            "year": 2009,
            "authors": "S. Aaronson and A. Wigderson",
            "title": "Algebrization: A New Barrier in Complexity Theory",
            "venue": "ACM Transactions on Computation Theory",
            "url": "https://dl.acm.org/doi/10.1145/1490270.1490272",
            "role": "barrier",
            "status": "canonical",
            "supports": "Shows that even many non-relativizing arithmetization methods still fall inside an algebrizing barrier.",
            "limitation": "Algebrization does not rule out all algebraic or geometric methods; it forces proof attempts to state exactly what escapes the barrier.",
        },
        {
            "ref_id": "ref.impagliazzo-paturi-zane-2001",
            "year": 2001,
            "authors": "R. Impagliazzo, R. Paturi, and F. Zane",
            "title": "Which Problems Have Strongly Exponential Complexity?",
            "venue": "Journal of Computer and System Sciences",
            "url": "https://www.sciencedirect.com/science/article/pii/S002200000191774X",
            "role": "fine_grained_pressure",
            "status": "primary",
            "supports": "Develops reduction notions that preserve subexponential complexity and clarify how quantitative hardness transfers.",
            "limitation": "Strong exponential-time hypotheses and SERF reductions illuminate hardness structure but do not by themselves separate P from NP.",
        },
        {
            "ref_id": "ref.williams-2014",
            "year": 2014,
            "authors": "R. Williams",
            "title": "Nonuniform ACC Circuit Lower Bounds",
            "venue": "Journal of the ACM",
            "url": "https://dl.acm.org/doi/10.1145/2559903",
            "role": "lower_bound_progress",
            "status": "primary",
            "supports": "Proves that NEXP does not have polynomial-size nonuniform ACC circuits and demonstrates an algorithms-to-lower-bounds bridge.",
            "limitation": "The result is a major restricted-circuit breakthrough, not a lower bound against unrestricted polynomial-size circuits for NP.",
        },
        {
            "ref_id": "ref.valiant-1979",
            "year": 1979,
            "authors": "L. G. Valiant",
            "title": "Completeness Classes in Algebra",
            "venue": "Proceedings of the Eleventh Annual ACM Symposium on Theory of Computing",
            "url": "https://dl.acm.org/doi/10.1145/800135.804419",
            "role": "algebraic_analogy",
            "status": "primary",
            "supports": "Creates an algebraic analogue of completeness and lower-bound questions, showing how representation and computation can be studied through polynomial families.",
            "limitation": "Algebraic complexity gives powerful analogues and transfer pressure, but VP vs VNP is not literally the Boolean P vs NP problem.",
        },
    ]


def pvsnp_stages() -> list[dict[str, Any]]:
    return [
        {
            "stage_id": "stage-01-completeness",
            "period": "1971-1972",
            "title": "Verification becomes a universal computational phenomenon",
            "core_shift": "Cook and Karp show that many apparently different problems are interreducible through polynomial reductions and share SAT as a complete core.",
            "what_became_possible": "The problem becomes mathematically precise: it is enough to decide whether any NP-complete language, especially SAT, has polynomial-time algorithms.",
            "what_remained_open": "Completeness explains universality of difficulty but not the source of lower bounds against all polynomial-time algorithms or circuits.",
            "refs": ["ref.cook-1971", "ref.karp-1972"],
        },
        {
            "stage_id": "stage-02-relativization",
            "period": "1975",
            "title": "Proof techniques become objects of study",
            "core_shift": "Relativization shows that any proof surviving arbitrary oracle substitution cannot settle the main question.",
            "what_became_possible": "A serious route must track what part of the argument is nonrelativizing rather than merely proving a plausible separation in an oracle-insensitive way.",
            "what_remained_open": "The barrier diagnoses broad method families but does not identify a successful nonrelativizing replacement.",
            "refs": ["ref.baker-gill-solovay-1975"],
        },
        {
            "stage_id": "stage-03-structural-and-algebraic-routes",
            "period": "Late 1970s onward",
            "title": "Complexity becomes a landscape of representations",
            "core_shift": "Algebraic, proof-complexity, descriptive, and structural viewpoints re-express computation through polynomials, proofs, reductions, and uniformity conditions.",
            "what_became_possible": "The problem can be attacked by translating Boolean hardness into more rigid mathematical objects with their own invariants.",
            "what_remained_open": "Every translation risks losing target strength: a theorem in a restricted or algebraic model must still return to Boolean P vs NP or P/poly with controlled loss.",
            "refs": ["ref.valiant-1979"],
        },
        {
            "stage_id": "stage-04-natural-proofs",
            "period": "1990s",
            "title": "Lower-bound intuitions meet pseudorandomness",
            "core_shift": "Natural proofs explain why many broad, efficiently checkable combinatorial properties are unlikely to prove strong unrestricted circuit lower bounds.",
            "what_became_possible": "Discovery can now audit lower-bound proposals for largeness, constructivity, usefulness, and cryptographic tension.",
            "what_remained_open": "The field still needs useful lower-bound properties that are either not large, not constructive, not black-box, or otherwise outside the natural-proofs template.",
            "refs": ["ref.razborov-rudich-1997"],
        },
        {
            "stage_id": "stage-05-quantitative-transfer",
            "period": "2000s onward",
            "title": "Fine-grained and magnification thinking exposes exponent debt",
            "core_shift": "Hardness transfers are judged by exact exponents, target-query counts, advice leakage, and whether a weak source lower bound really magnifies to the main target.",
            "what_became_possible": "Routes can be evaluated with precise inequalities instead of broad optimism about reductions or carriers.",
            "what_remained_open": "Most bridges lose too much exponent, import nonuniform advice, or prove a source lower bound that is already as hard as the desired conclusion.",
            "refs": ["ref.impagliazzo-paturi-zane-2001"],
        },
        {
            "stage_id": "stage-06-modern-barrier-aware-progress",
            "period": "2009 onward",
            "title": "Modern progress is real but carefully scoped",
            "core_shift": "Algebrization and restricted-circuit lower bounds clarify both the reach and limits of current techniques.",
            "what_became_possible": "Algorithmic, algebraic, and restricted-circuit breakthroughs provide templates for bridge design and falsification.",
            "what_remained_open": "The unrestricted P vs NP question still demands a target-preserving lower bound or impossibility theorem that escapes known barriers without losing the main quantifiers.",
            "refs": ["ref.aaronson-wigderson-2009", "ref.williams-2014"],
        },
    ]


def pvsnp_difficulty_narrative() -> dict[str, Any]:
    return {
        "overview": (
            "P vs NP is hard because it asks for a theorem about the limits of every efficient method, "
            "not merely about the failure of familiar algorithms. A convincing route must convert a "
            "semantic contrast between finding and checking witnesses into a uniform mathematical "
            "invariant that all polynomial-time computation must obey, while also explaining why that "
            "invariant does not collapse under reductions, advice, randomness, or alternative representations."
        ),
        "core_tension": (
            "The problem is at once universal and anti-local: NP-completeness lets one move difficulty across "
            "many problems, but lower bounds must defeat all possible polynomial-time reorganizations of the "
            "search space. The same reductions that make the problem universal also make naive structural "
            "arguments fragile, because an algorithm may exploit a representation very different from the one "
            "in which the human proof sees hardness."
        ),
        "facets": [
            {
                "lens": "Mathematical difficulty",
                "claim": "The target is an unrestricted lower bound over an enormous algorithmic or circuit universe.",
                "pressure": "Restricted lower bounds can be deep and still miss P/poly; exponent-preserving transfer from a source carrier to SAT must be exact.",
                "workflow_consequence": "Every branch must name the source model, target class, quantifier strength, and loss terms before it is allowed to count as progress toward P vs NP.",
            },
            {
                "lens": "Epistemological difficulty",
                "claim": "The field lacks direct access to the object being excluded: all polynomial-time strategies.",
                "pressure": "Evidence usually arrives indirectly through barriers, restricted models, reductions, algorithms-to-lower-bounds, or meta-complexity proxies.",
                "workflow_consequence": "The report should distinguish proof evidence, obstruction evidence, analogy, and route-level bridge pressure rather than mixing them into one optimism score.",
            },
            {
                "lens": "Philosophical difficulty",
                "claim": "The conjecture asks whether efficient verification has a fundamentally different kind of power from efficient construction.",
                "pressure": "This is not only a resource inequality; it is a question about whether certificates contain latent constructive content extractable by any general procedure.",
                "workflow_consequence": "Conceptual analyses should track what kind of witness information is hidden, leaked, compressed, queried, or reconstructed by each proposed bridge.",
            },
            {
                "lens": "Barrier difficulty",
                "claim": "Several broad styles of plausible proof are known to fail as general templates.",
                "pressure": "Relativization, natural proofs, and algebrization do not make the problem hopeless; they force the route to identify its nonrelativizing, non-natural, or non-algebrizing ingredient.",
                "workflow_consequence": "A branch should be promoted only when it carries a specific barrier-escape mechanism, not just a label saying it is barrier-aware.",
            },
            {
                "lens": "Transfer difficulty",
                "claim": "Progress often lives in nearby theories whose conclusions are easier than P vs NP.",
                "pressure": "A lower bound for AC0, formulas, monotone circuits, proof systems, algebraic circuits, or meta-complexity carriers can lose the main target through model mismatch.",
                "workflow_consequence": "The loop should treat bridge lemmas, loss accounting, and same-target handoff as first-class mathematical obligations.",
            },
        ],
        "common_false_shortcuts": [
            "Showing that known algorithms fail on SAT without ruling out all polynomial-time reorganizations.",
            "Proving a lower bound in a restricted model and silently treating it as evidence against unrestricted P/poly.",
            "Using a property of hard functions that is large and efficiently recognizable without confronting natural-proofs pressure.",
            "Relying on a relativizing or algebrizing simulation while claiming a conclusion known to require escaping that barrier family.",
            "Letting advice, padding, target-query count, or exponent loss enter the transfer theorem without charging it explicitly.",
        ],
    }


def build_pvsnp_report(target: dict[str, Any]) -> dict[str, Any]:
    refs = pvsnp_references()
    refs_by_id = {row["ref_id"]: row for row in refs}
    stages = []
    for stage in pvsnp_stages():
        cited = [refs_by_id[ref_id] for ref_id in stage["refs"] if ref_id in refs_by_id]
        stages.append({**stage, "citations": cited})
    return {
        "version": 1,
        "generated_utc": utc_now(),
        "target_id": target.get("target_id", "p-vs-np-target"),
        "problem_name": "P vs NP",
        "problem_statement": {
            "accessible": "Decide whether every efficiently verifiable decision problem is also efficiently solvable, equivalently whether SAT has a polynomial-time algorithm.",
            "formal_shape": r"\mathrm{P}\stackrel{?}{=}\mathrm{NP}\quad\text{or, equivalently,}\quad \mathrm{SAT}\in\mathrm{P}",
            "source_ref_id": "ref.cook-1971",
        },
        "why_it_matters": [
            "It is the central test of whether verification and search have the same polynomial-time power.",
            "It governs the meaning of NP-completeness: if P equals NP, thousands of complete search problems become efficiently solvable in principle; if not, their common hardness has a rigorous source.",
            "It is tied to cryptography, proof complexity, optimization, algorithms, derandomization, circuit lower bounds, and the philosophy of what counts as an efficient explanation.",
        ],
        "why_difficult": pvsnp_difficulty_narrative(),
        "solution_criteria": [
            "To prove P equals NP, exhibit a polynomial-time algorithm for an NP-complete problem such as SAT and prove its runtime and correctness.",
            "To prove P differs from NP, prove that some NP language, equivalently SAT, cannot be decided by any polynomial-time deterministic Turing machine.",
            "For nonuniform routes, a claim strong enough for NP not subset P/poly must rule out polynomial-size circuit families for an NP-complete language without uncharged advice.",
            "Any restricted-model, algebraic, proof-complexity, meta-complexity, or hardness-magnification result must include a target-preserving bridge back to the Boolean main problem.",
        ],
        "literature_stages": stages,
        "workflow_implications": [
            {
                "lesson": "Completeness gives a universal target but not a lower-bound method.",
                "active_workflow_effect": "Branches should keep SAT or an NP-complete carrier in view and avoid drifting into a nearby problem whose target transfer is unproved.",
                "refs": ["ref.cook-1971", "ref.karp-1972"],
            },
            {
                "lesson": "Barrier results are not generic pessimism; they are typing constraints on proof methods.",
                "active_workflow_effect": "Every promoted route needs a named account of relativization, naturalness, algebrization, advice leakage, and model mismatch.",
                "refs": ["ref.baker-gill-solovay-1975", "ref.razborov-rudich-1997", "ref.aaronson-wigderson-2009"],
            },
            {
                "lesson": "Quantitative transfer is often the real theorem.",
                "active_workflow_effect": "The loop should reward exact inequalities for exponent loss, target-query cost, padding overhead, and source-to-target preservation.",
                "refs": ["ref.impagliazzo-paturi-zane-2001", "ref.williams-2014"],
            },
            {
                "lesson": "Restricted breakthroughs matter when they isolate a reusable mechanism.",
                "active_workflow_effect": "A branch can be scientifically valuable as a scoped contribution if it proves a bridge criterion, no-go theorem, or model-specific lower-bound transfer with clear limitations.",
                "refs": ["ref.williams-2014", "ref.valiant-1979"],
            },
        ],
        "open_obligations": [
            "Identify a source object whose lower bound is not already as hard as P vs NP or NP not subset P/poly.",
            "Prove an exact target-preserving transfer theorem with all exponent, advice, uniformity, randomness, and query costs charged.",
            "Show how the route escapes or deliberately avoids relativization, natural-proofs, and algebrization barriers.",
            "Separate restricted-model evidence from unrestricted Boolean consequences.",
            "Convert promising meta-complexity, proof-complexity, algebraic, or hardness-magnification pressure into named theorems with falsifiable bridge conditions.",
        ],
        "references": refs,
        "required_skills": [
            "target-literature-source-curator",
            "target-literature-evolution-narrator",
            "pvsnp-conceptual-pressure-localizer",
            "pvsnp-pressure-to-bridge-abstractor",
            "pvsnp-symbolic-transfer-auditor",
            "pvsnp-impossibility-theorem-forger",
        ],
        "source_artifacts": [rel(ACTIVE_RUN_POINTER), "KB/p-vs-np.kb.md", "agentic/reports/discovery_marathon/latest.json"],
    }


def resolve_active_target() -> dict[str, Any]:
    latest = load_optional_json(LATEST_MARATHON_REPORT)
    active = load_optional_json(ACTIVE_RUN_POINTER)
    current = load_optional_json(CURRENT_TARGET)
    latest_target_id = clean_text(latest.get("target_id")) if latest else ""
    active_target_id = clean_text(active.get("target_id")) if active else ""
    if latest_target_id and (not active_target_id or latest_target_id == active_target_id):
        return {
            "target_id": latest_target_id,
            "raw_goal": latest.get("purpose") or latest.get("target_title") or latest_target_id,
            "source": rel(LATEST_MARATHON_REPORT),
        }
    if active_target_id:
        return {
            "target_id": active_target_id,
            "raw_goal": active_target_id,
            "source": rel(ACTIVE_RUN_POINTER),
        }
    return current or {}


def build_report() -> dict[str, Any]:
    target = resolve_active_target()
    target_id = clean_text(target.get("target_id")) if target else ""
    if "p-vs-np" in target_id or "pvsnp" in target_id:
        return build_pvsnp_report(target)
    if target_id and "yang-mills" in target_id:
        return build_yang_mills_report(target)
    if target_id and "yang-mills" not in target_id:
        return {
            "version": 1,
            "generated_utc": utc_now(),
            "target_id": target_id,
            "problem_name": clean_text(target.get("raw_goal")) or "active target",
            "problem_statement": {
                "accessible": "No curated literature-evolution packet exists yet for this target.",
                "formal_shape": "",
                "source_ref_id": "",
            },
            "why_it_matters": [],
            "solution_criteria": [],
            "literature_stages": [],
            "workflow_implications": [],
            "open_obligations": ["Run target-literature-source-curator for this target."],
            "references": [],
            "required_skills": ["target-literature-source-curator", "target-literature-evolution-narrator"],
            "source_artifacts": [rel(CURRENT_TARGET)],
        }
    return build_yang_mills_report(target)


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Target Problem And Literature Evolution",
        "",
        f"- Target: `{report['target_id']}`",
        f"- Problem: {report['problem_name']}",
        f"- Statement: {report['problem_statement']['accessible']}",
        "",
        "## Why It Matters",
        "",
    ]
    lines.extend(f"- {item}" for item in report.get("why_it_matters", []))
    difficulty = report.get("why_difficult") or {}
    if difficulty:
        lines.extend(["", "## Why This Is Difficult", ""])
        if difficulty.get("overview"):
            lines.extend([difficulty["overview"], ""])
        if difficulty.get("core_tension"):
            lines.extend(["### Core tension", "", difficulty["core_tension"], ""])
        for facet in difficulty.get("facets", []):
            lines.extend(
                [
                    f"### {facet.get('lens', 'Difficulty facet')}",
                    "",
                    f"- Claim: {facet.get('claim', '')}",
                    f"- Pressure: {facet.get('pressure', '')}",
                    f"- Workflow consequence: {facet.get('workflow_consequence', '')}",
                    "",
                ]
            )
        shortcuts = difficulty.get("common_false_shortcuts", [])
        if shortcuts:
            lines.extend(["### False shortcuts to avoid", ""])
            lines.extend(f"- {item}" for item in shortcuts)
    lines.extend(["", "## Literature Evolution", ""])
    for stage in report.get("literature_stages", []):
        refs = ", ".join(stage.get("refs", []))
        lines.extend(
            [
                f"### {stage['period']} - {stage['title']}",
                "",
                f"- Shift: {stage['core_shift']}",
                f"- Became possible: {stage['what_became_possible']}",
                f"- Still open: {stage['what_remained_open']}",
                f"- References: {refs}",
                "",
            ]
        )
    lines.extend(["## Workflow Implications", ""])
    for item in report.get("workflow_implications", []):
        lines.append(f"- {item['lesson']} Effect: {item['active_workflow_effect']}")
    lines.extend(["", "## References", ""])
    for ref in report.get("references", []):
        lines.append(f"- `{ref['ref_id']}` {ref['authors']} ({ref['year']}), *{ref['title']}*. {ref['url']}")
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    report = build_report()
    write_json(OUT_JSON, report)
    write_markdown(OUT_MD, render_markdown(report))
    print(f"wrote {rel(OUT_JSON)}")
    print(f"wrote {rel(OUT_MD)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
