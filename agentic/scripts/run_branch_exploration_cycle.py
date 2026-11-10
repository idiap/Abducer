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
"""Generate one content-rich branch exploration packet."""

from __future__ import annotations

import argparse
from typing import Any

from agentic_common import ROOT, clean_text, load_json_object, stable_id, utc_now, write_json
from discovery_marathon_common import dump_stdout, markdown_list, write_markdown
from target_profiles import target_profile


def branch_domain(branch: dict[str, Any]) -> dict[str, str]:
    text = clean_text(branch).lower()
    profile = target_profile(branch.get("target_id"))
    if profile["target_id"] == "p-vs-np-target":
        if "barrier" in text or "natural" in text or "relativ" in text or "algebr" in text:
            return {
                "object": "barrier-aware lower-bound proof object",
                "source": "a proposed lower-bound method with an explicit nonrelativizing, non-natural, or non-algebrizing feature",
                "target": "a target-preserving route to a circuit lower bound or class separation consequence",
                "equation": r"\mathrm{Method}\not\subseteq \mathrm{Relativizing}\cup\mathrm{Natural}\cup\mathrm{Algebrizing}",
                "valid": "The method feature is formally named and the applicable barrier hypothesis is stated for the same source and target models.",
                "failure": "The alleged barrier escape is only rhetorical or the known barrier hypothesis applies unchanged.",
            }
        if "mcsp" in text or "meta" in text or "carrier" in text:
            return {
                "object": "MCSP/meta-complexity carrier",
                "source": "an explicit meta-complexity witness with a named extraction or reduction map",
                "target": "a circuit lower-bound, PIT, derandomization, or nonuniform-separation consequence",
                "equation": r"C_{\mathrm{MCSP}}\xrightarrow[\mathrm{preserve}\ I]{\mathrm{extract}} C_{\mathrm{lb}}",
                "valid": "The carrier is explicit, the invariant I is defined, and extraction preserves the class and parameter thresholds.",
                "failure": "The carrier is not explicit or extraction loses the quantitative strength needed for the target consequence.",
            }
        return {
            "object": "hardness-magnification bridge packet",
            "source": "a barely nontrivial lower bound in a named weak model for an explicit problem",
            "target": "a magnified separation such as NP not in P/poly or another target-preserving consequence",
            "equation": r"\mathrm{LB}_{\epsilon}(\Pi,\mathcal M)\Longrightarrow \mathrm{Sep}(\mathcal C_{\mathrm{target}})",
            "valid": "The explicit problem Pi, weak model M, epsilon threshold, and target consequence are all named and preserved by the bridge theorem.",
            "failure": "The lower-bound threshold collapses, the source model changes, or the target consequence is weaker than the route claims.",
        }
    if "correlator" in text or "spectral" in text:
        return {
            "object": "gauge-invariant Euclidean two-point function",
            "source": "OS-positive Schwinger functions with a surviving observable family",
            "target": "Hamiltonian spectral measure with support bounded away from zero",
            "equation": r"\langle O(t)O(0)\rangle_c=\int_0^\infty e^{-t\lambda}\,d\mu_O(\lambda)",
            "valid": "O belongs to the reconstructed gauge-invariant observable algebra and the OS semigroup identifies Euclidean time with e^{-tH}.",
            "failure": "The observable family fails to be spectrally determining or the decay constants vanish under cutoff removal.",
        }
    if "os" in text or "reflection" in text or "hilbert" in text:
        return {
            "object": "reflection-positive limiting Schwinger function family",
            "source": "cutoff Schwinger functions whose positivity cone is closed under the limiting topology",
            "target": "physical Hilbert space, vacuum vector, and positive Hamiltonian",
            "equation": r"\sum_{i,j}\overline c_i c_j S(\Theta f_i,f_j)\ge 0",
            "valid": "The test functions f_i are gauge-invariant positive-time observables and S is the continuum limiting Schwinger family.",
            "failure": "Reflection positivity is not closed under the chosen cutoff-removal topology.",
        }
    if "nontrivial" in text or "cumulant" in text or "observable" in text:
        return {
            "object": "connected gauge-invariant cumulant witness",
            "source": "continuum observables produced by the same limiting Yang-Mills construction",
            "target": "non-Gaussian, interacting vacuum sector",
            "equation": r"\langle O_1\cdots O_k\rangle_c\ne 0",
            "valid": "Each O_i is gauge invariant, survives cutoff removal, and belongs to the same continuum theory used for reconstruction.",
            "failure": "All connected witness cumulants collapse to zero or the witness lives in a different approximation.",
        }
    return {
        "object": "regulated Yang-Mills scale-control packet",
        "source": "lattice-spacing and volume cutoff family with gauge-invariant observables",
        "target": "continuum Schwinger functions preserving construction, nontriviality, and later spectral transfer",
        "equation": r"S_n^{(a,L)}\Rightarrow S_n\quad(a\to0,\ L\to\infty)",
        "valid": "Uniform multiscale bounds, tightness, and gauge-invariant observable control hold across cutoff removal.",
        "failure": "The argument only proves fixed-cutoff, finite-volume, or small-field control.",
    }


def build_branch_output(branch: dict[str, Any], cycle_index: int) -> dict[str, Any]:
    domain = branch_domain(branch)
    profile = target_profile(branch.get("target_id"))
    consistency_prefix = "target-preserving condition:" if profile["target_id"] == "p-vs-np-target" else "same-theory condition:"
    consistency_sentence = (
        "source model, target model, reductions, barriers, and quantitative thresholds must refer to one complexity-theoretic route."
        if profile["target_id"] == "p-vs-np-target"
        else "construction, observables, reconstruction, and witnesses must refer to one limiting object."
    )
    stated_condition = "target-preserving" if profile["target_id"] == "p-vs-np-target" else "same-theory"
    target_commitment = (
        "The target commitments remain route-level progress toward P != NP, with explicit separation between hardness magnification, circuit lower bounds, proof-complexity transfer, and the main conjecture."
        if profile["target_id"] == "p-vs-np-target"
        else "The target commitments remain existence, nontriviality, OS/Wightman adequacy, continuum limit, and positive mass gap unless an accepted weakening is recorded."
    )
    typing_assumption = (
        "All transfers are typed by their source complexity model, reduction map, target class, and quantitative threshold."
        if profile["target_id"] == "p-vs-np-target"
        else "All limiting operations are typed by their source cutoff family and target continuum object."
    )
    hidden_shift = (
        "proxy substitution across complexity classes, source models, reductions, advice, or quantitative thresholds."
        if profile["target_id"] == "p-vs-np-target"
        else "importing another theory."
    )
    branch_id = branch["branch_id"]
    lemma_id = stable_id("lemma", branch_id, cycle_index, domain["object"])
    repeated = int(branch.get("consecutive_low_learning_cycles", 0))
    control = "backtrack" if repeated >= 2 else "persist_adapt"
    learning = (
        f"The branch sharpened the interface from `{branch.get('controlled_interface')}` into a concrete source object "
        f"({domain['source']}) and target object ({domain['target']}). The next proof pressure is not to add vocabulary; "
        f"it is to certify whether {domain['object']} can carry the bridge without changing the theory."
    )
    return {
        "branch_id": branch_id,
        "branch_title": branch["title"],
        "candidate_lemmas": [
            {
                "lemma_id": lemma_id,
                "statement": (
                    f"If {domain['source']} satisfies the stated uniformity and {stated_condition} conditions, then the branch may "
                    f"transport information to {domain['target']} without weakening the target object."
                ),
                "definitions": [
                    f"source object: {domain['source']}",
                    f"target object: {domain['target']}",
                    f"controlled interface: {branch.get('controlled_interface')}",
                    f"{consistency_prefix} {consistency_sentence}",
                ],
                "assumptions": [
                    target_commitment,
                    typing_assumption,
                    "Transfer claims preserve the named source object, target object, and quantitative validity regime.",
                ],
                "equations": [
                    {
                        "label": f"{domain['object']} checkpoint",
                        "latex": domain["equation"],
                        "valid_when": domain["valid"],
                    },
                {
                    "label": f"{stated_condition} transfer constraint",
                    "latex": (
                        r"(\Pi,\mathcal M,\epsilon,\mathcal C_{\mathrm{target}})\ \text{are preserved by one route}"
                        if profile["target_id"] == "p-vs-np-target"
                        else r"(S_n,\mathcal H,H,\Omega,O)\ \text{arise from one limiting construction}"
                    ),
                    "valid_when": (
                        "The source problem, weak model, threshold parameter, and target complexity class remain fixed across the transfer."
                        if profile["target_id"] == "p-vs-np-target"
                        else "The construction packet names S_n, the reconstruction theorem names H and Omega, and O is in the reconstructed observable algebra."
                    ),
                    },
                ],
                "proof_role": f"Bridge lemma for {branch.get('machinery_role')} machinery.",
                "failure_test": domain["failure"],
            }
        ],
        "attempted_derivation": {
            "derivation_id": stable_id("derivation", branch_id, cycle_index),
            "steps": [
                f"Start from {domain['source']} rather than from an untyped desired conclusion.",
                f"State the core equation `{domain['equation']}` and its validity conditions.",
                f"Ask whether the equation controls the interface `{branch.get('controlled_interface')}` without {hidden_shift}",
                f"Route the missing premise through obligation gating before promotion.",
            ],
            "blocking_gap": domain["failure"],
            "why_not_yet_a_proof": "The output is theorem-shaped but still depends on certification of uniformity, density, closedness, or nontriviality.",
        },
        "falsifiers": [
            domain["failure"],
            "The branch can only state an analogy, empirical hint, or local observation without a transfer certificate.",
            "The generated lemma drops an essential target commitment or changes the source/target object.",
        ],
        "gedanken_experiment_design": {
            "need_decision": "design_now" if control != "backtrack" else "defer_until_variable_typed",
            "rationale": (
                "The blocker is conceptual opacity in the source-target bridge; a controlled imagined situation can isolate the hidden transfer assumption "
                "before another full proof attempt is spent."
                if control != "backtrack"
                else "Repeated low-learning cycles indicate the branch must first retype variables and regimes before an imagined situation would be diagnostic."
            ),
            "situation_seed": (
                f"Vary the validity of `{domain['equation']}` across a minimal carrier for {domain['object']} while holding the target commitments, "
                f"source/target typing, and {stated_condition} construction fixed."
            ),
            "varied_variable": domain["object"],
            "held_fixed_controls": [
                "target commitments",
                "target-preserving construction" if profile["target_id"] == "p-vs-np-target" else "same-theory construction",
                "source/target object typing",
                "validity regime",
            ],
            "expected_observation": "A diagnostic shift in the bridge equation's ability to carry target information without proxy substitution.",
            "transfer_certificate_needed": domain["valid"],
        },
        "dependency_updates": [
            {
                "dependency_id": stable_id("dep", branch_id, "source-object"),
                "kind": "source_object",
                "description": domain["source"],
                "status": "open_certification",
            },
            {
                "dependency_id": stable_id("dep", branch_id, "target-object"),
                "kind": "target_object",
                "description": domain["target"],
                "status": "open_certification",
            },
        ],
        "mathematical_learning": learning,
        "control_decision": {
            "decision": control,
            "reason": (
                "Backtrack is required because repeated low-learning cycles indicate that the source/target object typing is still missing."
                if control == "backtrack"
                else "Persist with adaptation because the branch remains target-linked and this cycle produced a sharper bridge lemma candidate."
            ),
            "pivot_test": branch.get("pivot_signal", ""),
            "promotion_test": branch.get("promotion_signal", ""),
        },
        "next_experiment": (
            f"Certify the weakest condition under which `{domain['equation']}` is valid for the branch source object, then ask the "
            "entailment-gap auditor whether it reaches the target object without hidden proxy shifts. If the blocker is conceptual opacity rather than "
            "a missing calculation, design a Gedanken experiment that names the minimal imagined situation, varied variable, held-fixed controls, "
            "expected observation, disconfirming observation, and transfer certificate before allowing the insight to affect proof obligations."
        ),
    }


def output_markdown(output: dict[str, Any]) -> str:
    lemma = output["candidate_lemmas"][0]
    gedanken = output.get("gedanken_experiment_design", {})
    return (
        f"# {output['branch_title']}\n\n"
        f"## Candidate Lemma\n\n{lemma['statement']}\n\n"
        f"## Definitions\n\n{markdown_list(lemma['definitions'])}\n"
        f"## Assumptions\n\n{markdown_list(lemma['assumptions'])}\n"
        f"## Equations\n\n"
        + "".join(f"- {eq['label']}: `{eq['latex']}`. Valid when: {eq['valid_when']}\n" for eq in lemma["equations"])
        + f"\n## Attempted Derivation\n\n{markdown_list(output['attempted_derivation']['steps'])}\n"
        f"Blocking gap: {output['attempted_derivation']['blocking_gap']}\n\n"
        f"## Falsifiers\n\n{markdown_list(output['falsifiers'])}\n"
        f"## Learning\n\n{output['mathematical_learning']}\n\n"
        f"## Gedanken Experiment Design Seed\n\n"
        f"- Need decision: `{gedanken.get('need_decision', '')}`\n"
        f"- Rationale: {gedanken.get('rationale', '')}\n"
        f"- Situation seed: {gedanken.get('situation_seed', '')}\n"
        f"- Varied variable: {gedanken.get('varied_variable', '')}\n"
        f"- Held-fixed controls: {', '.join(gedanken.get('held_fixed_controls', []))}\n"
        f"- Expected observation: {gedanken.get('expected_observation', '')}\n"
        f"- Transfer certificate needed: {gedanken.get('transfer_certificate_needed', '')}\n\n"
        f"## Next Experiment\n\n{output['next_experiment']}\n"
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--branch-json", required=True)
    parser.add_argument("--cycle-index", type=int, default=1)
    parser.add_argument("--out-json")
    parser.add_argument("--out-md")
    args = parser.parse_args()
    branch = load_json_object(ROOT / args.branch_json if not args.branch_json.startswith("/") else args.branch_json)
    output = build_branch_output(branch, args.cycle_index)
    output["created_utc"] = utc_now()
    if args.out_json:
        write_json(ROOT / args.out_json, output)
    if args.out_md:
        write_markdown(ROOT / args.out_md, output_markdown(output))
    if not args.out_json:
        dump_stdout(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
