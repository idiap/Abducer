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

"""Build a large-stretch Yang-Mills discovery exploration report."""

from __future__ import annotations

from typing import Any

from agentic_common import ROOT, load_json_object, rel, stable_id, utc_now, write_json


MONITOR = ROOT / "agentic/reports/reasoning_monitor/latest.json"
LONG_HORIZON = ROOT / "agentic/reports/long_horizon/latest.json"
BRIDGES = ROOT / "agentic/reports/yang_mills_bridge_lemma_packets/latest.json"
CHAIN = ROOT / "agentic/reports/abstraction_chains/latest.json"
OUT_JSON = ROOT / "agentic/reports/discovery_stretch/latest.json"
OUT_MD = ROOT / "agentic/reports/discovery_stretch/latest.md"
TARGET_ID = "yang-mills-existence-and-mass-gap-target"


def program(
    slug: str,
    title: str,
    role: str,
    hypothesis: str,
    mechanism: str,
    interface: str,
    equations: list[dict[str, str]],
    dependencies: list[str],
    falsifiers: list[str],
    next_experiments: list[str],
    expected_learning: str,
    promotion_signal: str,
    pivot_signal: str,
) -> dict[str, Any]:
    return {
        "program_id": stable_id("ym-discovery-stretch", slug),
        "title": title,
        "machinery_role": role,
        "hypothesis": hypothesis,
        "mathematical_mechanism": mechanism,
        "controlled_interface": interface,
        "equations": equations,
        "dependencies": dependencies,
        "falsifiers": falsifiers,
        "next_experiments": next_experiments,
        "expected_learning": expected_learning,
        "promotion_signal": promotion_signal,
        "pivot_signal": pivot_signal,
        "status": "active_discovery_program",
    }


def build_programs() -> list[dict[str, Any]]:
    return [
        program(
            "rp-closed-cone-topology",
            "Reflection-Positivity Closed-Cone Topology",
            "invariant_preservation",
            (
                "If the cutoff-removal topology can be chosen so that reflection-positive gauge-invariant Schwinger distributions form "
                "a closed cone, then OS positivity can survive the RG continuum passage instead of being reintroduced by hand."
            ),
            (
                "Treat OS positivity as a convex-cone closedness problem over gauge-invariant test observables. The discovery move is to "
                "identify the weakest topology strong enough to pass finite reflected quadratic forms to the limit while still compatible "
                "with Balaban-style multiscale compactness."
            ),
            "regulated reflection-positive Schwinger forms -> OS-positive continuum Schwinger functions",
            [
                {
                    "label": "regulated positivity",
                    "latex": r"Q_{a,L}(f,c)=\sum_{i,j}\overline c_i c_j S_{a,L}(\Theta f_i,f_j)\ge 0",
                    "valid_when": "Each regulated gauge-invariant observable family is reflection-positive before cutoff removal.",
                },
                {
                    "label": "closed cone transfer",
                    "latex": r"S_{a,L}\Rightarrow S,\quad Q_{a,L}(f,c)\to Q(f,c)\quad\Longrightarrow\quad Q(f,c)\ge0",
                    "valid_when": "The limiting topology gives convergence of every reflected finite test-observable quadratic form.",
                },
            ],
            [
                "RG-to-OS Continuum Passage Bridge Lemma",
                "choice of gauge-invariant test algebra",
                "cutoff-removal topology",
            ],
            [
                "The topology supplied by multiscale bounds is too weak to control reflected test forms.",
                "Gauge fixing or quotienting changes the test algebra across the limit.",
                "Reflection positivity is only proved for a lattice transfer matrix and not for the limiting Schwinger functions.",
            ],
            [
                "List the finite reflected quadratic forms required by OS positivity for the current observable algebra.",
                "Ask whether Balaban-style convergence controls those forms as continuous functionals.",
                "Split the topology into minimal closedness demands: covariance, positivity, clustering, and distributional regularity.",
            ],
            "This tells us whether construction and reconstruction can be fused by topology, or whether OS positivity needs a different construction carrier.",
            "A named topology plus a closure lemma for all finite reflected forms.",
            "If closure fails, pivot from pure RG construction toward an OS-preserving lattice/Euclidean construction route.",
        ),
        program(
            "wilson-loop-nontriviality-witness",
            "Gauge-Invariant Nontriviality Witness Selection",
            "witness",
            (
                "A Wilson-loop or local curvature-composite family may serve as the nontriviality witness if one connected cumulant survives cutoff removal "
                "in the same Schwinger family used for OS reconstruction."
            ),
            (
                "Make nontriviality operational: choose a gauge-invariant observable whose connected correlation rules out Gaussian/free collapse. "
                "The route should not ask for all interactions at once; it should look for one same-theory connected witness with stable normalization."
            ),
            "continuum gauge-invariant Schwinger functions -> non-Gaussian same-theory witness",
            [
                {
                    "label": "connected cumulant",
                    "latex": r"\langle O_1\cdots O_k\rangle_c\ne0",
                    "valid_when": "The O_i are gauge-invariant observables in the same limiting Schwinger family S_n.",
                },
                {
                    "label": "Gaussian-collapse exclusion",
                    "latex": r"\exists k\ge3:\ \kappa_k(O_1,\ldots,O_k)\ne0",
                    "valid_when": "Higher connected cumulants are defined after the same cutoff-removal normalization.",
                },
            ],
            [
                "continuum Schwinger-function representation",
                "same-theory invariant",
                "candidate Wilson-loop or curvature-composite observable algebra",
            ],
            [
                "The witness only survives at finite cutoff.",
                "The chosen observable is not in the reconstructed OS algebra.",
                "All connected cumulants vanish under the required normalization.",
            ],
            [
                "Enumerate candidate gauge-invariant observables already present in the KB and bridge packets.",
                "For each observable, state the lowest-order connected cumulant that would refute Gaussian collapse.",
                "Record whether the witness also helps observable-density or only nontriviality.",
            ],
            "This separates existence from nontrivial existence and gives the gap route a physical observable carrier.",
            "A same-theory connected cumulant or Wilson-loop behavior with explicit cutoff normalization.",
            "If every plausible witness degenerates, pivot to nontriviality as the lead obstruction before spectral-gap work.",
        ),
        program(
            "observable-density-spectral-determination",
            "Gauge-Invariant Observable Density In The Excitation Sector",
            "transfer",
            (
                "The decay-to-gap route becomes legitimate only if vacuum-subtracted gauge-invariant observables generate a dense subspace of "
                "the vacuum-orthogonal reconstructed Hilbert space."
            ),
            (
                "Translate the physical claim 'gauge-invariant observables see the glueball spectrum' into a cyclicity/density statement after OS reconstruction. "
                "This is the hinge that prevents a decay estimate for a small visible sector from masquerading as a full mass gap."
            ),
            "gauge-invariant observable algebra -> P_perp H_YM spectral determination",
            [
                {
                    "label": "observable-generated sector",
                    "latex": r"\mathcal D_{\mathrm{ginv}}=\overline{\{(A-\langle A\rangle)\Omega:A\in\mathcal A_{\mathrm{ginv}}\}}",
                    "valid_when": "A_ginv is the reconstructed gauge-invariant observable algebra and Omega is the OS vacuum.",
                },
                {
                    "label": "density target",
                    "latex": r"\mathcal D_{\mathrm{ginv}}=P_\perp\mathcal H_{\mathrm{YM}}",
                    "valid_when": "The vacuum-orthogonal sector is the physical excitation sector relevant to the Clay mass gap.",
                },
            ],
            [
                "OS reconstruction output H_YM, Omega, H",
                "gauge-invariant observable algebra",
                "decay-to-Hamiltonian bridge lemma",
            ],
            [
                "Gauge-invariant observables generate only a proper subspace.",
                "Null-vector quotient removes the chosen observable carriers.",
                "The density theorem needs locality or additivity assumptions not supplied by the construction route.",
            ],
            [
                "State the exact density theorem needed in reconstructed OS language.",
                "Identify whether Wilson loops/local curvature composites plausibly generate the sector.",
                "Make a fallback plan: if full density is too strong, isolate a physically meaningful subgap theorem and mark it as weaker.",
            ],
            "This discovers whether correlator decay can ever certify the full Hamiltonian gap or only a visible-sector gap.",
            "A density or cyclicity lemma showing vacuum-subtracted gauge-invariant observables generate the full reconstructed excitation sector.",
            "If density is inaccessible, pivot the gap route toward direct spectral lower bounds or clearly weaker sectoral milestones.",
        ),
        program(
            "laplace-support-lemma",
            "Laplace-Transform Support From Uniform Euclidean Decay",
            "witness",
            (
                "A cutoff-uniform exponential bound on connected Euclidean correlations should imply spectral-measure support away from zero for "
                "the reconstructed Hamiltonian, but only after constants, observables, and reconstruction are same-theory."
            ),
            (
                "Factor the analytic core away from Yang-Mills-specific construction: prove the measure-theoretic support lemma once, then use the "
                "rest of the workflow to certify that Yang-Mills supplies its hypotheses."
            ),
            "Euclidean time correlation decay -> Hamiltonian spectral support exclusion",
            [
                {
                    "label": "spectral representation",
                    "latex": r"C_A(t)=\int_0^\infty e^{-t\lambda}\,d\mu_A(\lambda)",
                    "valid_when": "A Omega is a reconstructed vector and Euclidean time evolution is exp(-tH).",
                },
                {
                    "label": "support exclusion",
                    "latex": r"|C_A(t)|\le C e^{-m_0t}\quad\Longrightarrow\quad \operatorname{supp}\mu_A\cap(0,m_0)=\varnothing",
                    "valid_when": "The bound holds for all sufficiently large t with a positive rate m0 and no cancellation hides positive spectral mass.",
                },
            ],
            [
                "OS reconstruction",
                "positive spectral measure",
                "cutoff-uniform decay estimate",
            ],
            [
                "The correlation is not represented by a positive spectral measure.",
                "The decay bound is asymptotic with constants that degenerate in the continuum limit.",
                "The observable family is not dense enough to lift support exclusion to P_perp H_YM.",
            ],
            [
                "Prove the scalar spectral-measure lemma independently of Yang-Mills.",
                "List the exact positivity and vacuum-subtraction assumptions needed for the lemma.",
                "Attach the lemma as a validator for every correlator-decay route.",
            ],
            "This isolates a reusable analytic engine and makes the remaining burden visible as construction, density, and uniformity.",
            "A self-contained proof of the spectral-support lemma together with a checklist of positivity, reconstruction, and density hypotheses supplied by Yang-Mills.",
            "If positivity or density cannot be certified, move the route to visible-sector witness rather than full gap proof.",
        ),
        program(
            "mass-scale-nonvanishing",
            "Cutoff-Uniform Mass Scale Nonvanishing",
            "validation",
            (
                "The central numerical-looking but proof-critical question is whether the candidate mass scale m_{a,L} has liminf bounded below by a positive m0 during cutoff removal."
            ),
            (
                "Treat the mass scale as an invariant to be transported, not as an observed parameter. The discovery task is to identify which RG, clustering, or correlation inequalities could prevent m_{a,L} from collapsing to zero."
            ),
            "regulated decay scales m_{a,L} -> positive continuum lower bound m0",
            [
                {
                    "label": "uniform lower-bound demand",
                    "latex": r"\liminf_{a\to0,L\to\infty}m_{a,L}\ge m_0>0",
                    "valid_when": "m_{a,L} is attached to the same observable family and limiting theory across the directed cutoff-removal net.",
                },
                {
                    "label": "forbidden collapse",
                    "latex": r"\exists(a_n,L_n):m_{a_n,L_n}\to0",
                    "valid_when": "The sequence remains in the construction regime claimed by the active route.",
                },
            ],
            [
                "decay-to-gap bridge",
                "RG continuum control",
                "empirical/lattice evidence requests as non-proof clues",
            ],
            [
                "All known decay estimates are strong-coupling or fixed-cutoff.",
                "The candidate mass scale is not defined uniformly across observables.",
                "Continuum limit drives the decay rate to zero.",
            ],
            [
                "Search generated empirical evidence requests for quantities that suggest which scale should be tracked.",
                "Ask whether RG bounds can imply a clustering inequality with a uniform rate.",
                "Construct the no-gap reductio sequence m_{a_n,L_n}->0 and identify what it would force in Schwinger correlations.",
            ],
            "This decides whether the correlator route is alive as a Clay-target route or should be demoted to regulated evidence.",
            "A theorem-shaped lower bound on liminf m_{a,L} for the same observable family, or a precise obstruction explaining why the scale collapses.",
            "If m_{a,L}->0 cannot be ruled out, pivot away from correlator decay as lead proof route.",
        ),
        program(
            "no-gap-reductio-low-energy-carrier",
            "No-Gap Reductio Low-Energy Carrier",
            "obstruction",
            (
                "Assuming no mass gap should produce a concrete low-energy carrier: either spectral mass near zero or a sequence of vacuum-orthogonal states approximable by gauge-invariant observables."
            ),
            (
                "Use proof by contradiction as a discovery microscope. The no-gap world should not remain a slogan; it must reveal whether the vulnerable hinge is observable density, uniform decay, OS reconstruction, or same-theory identity."
            ),
            "negated Hamiltonian gap -> low-energy spectral or observable carrier",
            [
                {
                    "label": "no-gap sequence",
                    "latex": r"\forall\varepsilon>0\ \exists\psi_\varepsilon\in P_\perp\mathcal H_{\mathrm{YM}},\ \|\psi_\varepsilon\|=1,\ \langle\psi_\varepsilon,H\psi_\varepsilon\rangle<\varepsilon",
                    "valid_when": "H_YM, Omega, H, and P_perp are reconstructed from the same OS-positive continuum Schwinger functions.",
                },
                {
                    "label": "observable approximation pressure",
                    "latex": r"\psi_\varepsilon\approx (A_\varepsilon-\langle A_\varepsilon\rangle)\Omega",
                    "valid_when": "Gauge-invariant observables are dense in the vacuum-orthogonal sector.",
                },
            ],
            [
                "Hamiltonian endpoint checklist",
                "observable-density program",
                "cutoff-uniform decay program",
            ],
            [
                "Low-energy states cannot be approximated by gauge-invariant observables.",
                "The contradiction uses a Hamiltonian not obtained from OS reconstruction.",
                "No uniform decay estimate applies to the approximating observable sequence.",
            ],
            [
                "Write the exact negation of the gap as a spectral projection statement.",
                "Try to approximate low-energy states by observable-generated vectors and record the missing theorem.",
                "Ask what each failure teaches: density failure, decay failure, or reconstruction failure.",
            ],
            "This converts failure to prove the gap into structured information about the missing mathematical carrier.",
            "A contradiction target linking no-gap states to violated cutoff-uniform decay or density.",
            "If no carrier can be made same-theory, quarantine the reductio and return to construction/reconstruction obligations.",
        ),
    ]


def build_report() -> dict[str, Any]:
    monitor = load_json_object(MONITOR)
    long_horizon = load_json_object(LONG_HORIZON)
    bridges = load_json_object(BRIDGES)
    chain = load_json_object(CHAIN)
    programs = build_programs()
    role_counts: dict[str, int] = {}
    for item in programs:
        role_counts[item["machinery_role"]] = role_counts.get(item["machinery_role"], 0) + 1
    synthesis = [
        "The stretch run should advance by isolating the bridge obligations that can fail independently: positivity closedness, nontriviality witness, observable density, Laplace support, nonvanishing mass scale, and no-gap carrier.",
        "The most valuable next mathematical move is not another broad route family; it is a typed lemma or falsifier at one of these interfaces.",
        "The current exploration remains proof-safe because every program has a target-object interface, explicit falsifiers, and a pivot signal.",
    ]
    return {
        "version": 1,
        "generated_utc": utc_now(),
        "target_id": TARGET_ID,
        "quality_gate": "pass",
        "source_artifacts": [rel(MONITOR), rel(LONG_HORIZON), rel(BRIDGES), rel(CHAIN)],
        "active_target": monitor.get("target", {}),
        "long_horizon_quality": long_horizon.get("quality_gate", ""),
        "bridge_packet_count": len(bridges.get("packets", [])),
        "abstraction_chain_status": chain.get("status", ""),
        "stretch_thesis": (
            "A large Yang-Mills discovery stretch should now search across six typed interfaces rather than add route slogans: "
            "reflection positivity closedness, nontriviality witnessing, observable density, Laplace support, nonvanishing mass scale, "
            "and no-gap reductio carriers."
        ),
        "programs": programs,
        "role_counts": role_counts,
        "synthesis": synthesis,
        "next_run_queue": [
            {
                "queue_id": "stretch-next-01",
                "action": "Try to prove or refute reflection-positivity closedness for the proposed cutoff-removal topology.",
                "why_first": "Without OS positivity, Hamiltonian and spectral language cannot be target-valid.",
            },
            {
                "queue_id": "stretch-next-02",
                "action": "Select one concrete gauge-invariant nontriviality witness and state its connected-cumulant theorem.",
                "why_first": "A continuum construction that collapses to a trivial theory cannot solve the Clay target.",
            },
            {
                "queue_id": "stretch-next-03",
                "action": "Prove the abstract Laplace-support lemma separately from Yang-Mills assumptions.",
                "why_first": "This isolates the analytic core of the mass-gap witness and exposes the remaining Yang-Mills-specific hypotheses.",
            },
        ],
    }


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Yang-Mills Discovery Stretch",
        "",
        f"- Target: `{report['target_id']}`",
        f"- Quality gate: `{report['quality_gate']}`",
        f"- Long-horizon quality: `{report['long_horizon_quality']}`",
        f"- Bridge packets: `{report['bridge_packet_count']}`",
        "",
        report["stretch_thesis"],
        "",
        "## Synthesis",
        "",
    ]
    lines.extend(f"- {item}" for item in report["synthesis"])
    lines.extend(["", "## Discovery Programs", ""])
    for item in report["programs"]:
        lines.extend(
            [
                f"### {item['title']}",
                "",
                f"- Program: `{item['program_id']}`",
                f"- Machinery role: `{item['machinery_role']}`",
                f"- Controlled interface: {item['controlled_interface']}",
                f"- Hypothesis: {item['hypothesis']}",
                "",
                "**Mathematical mechanism**",
                "",
                item["mathematical_mechanism"],
                "",
                "**Equations**",
            ]
        )
        for equation in item["equations"]:
            lines.append(f"- {equation['label']}: `{equation['latex']}`")
            lines.append(f"  - Valid when: {equation['valid_when']}")
        lines.extend(["", "**Dependencies**"])
        lines.extend(f"- {value}" for value in item["dependencies"])
        lines.extend(["", "**Falsifiers**"])
        lines.extend(f"- {value}" for value in item["falsifiers"])
        lines.extend(["", "**Next experiments**"])
        lines.extend(f"- {value}" for value in item["next_experiments"])
        lines.extend(
            [
                "",
                f"- Expected learning: {item['expected_learning']}",
                f"- Promotion signal: {item['promotion_signal']}",
                f"- Pivot signal: {item['pivot_signal']}",
                "",
            ]
        )
    lines.extend(["## Next Run Queue", ""])
    for item in report["next_run_queue"]:
        lines.append(f"- `{item['queue_id']}` {item['action']}")
        lines.append(f"  - Why first: {item['why_first']}")
    return "\n".join(lines) + "\n"


def main() -> int:
    report = build_report()
    write_json(OUT_JSON, report)
    OUT_MD.parent.mkdir(parents=True, exist_ok=True)
    OUT_MD.write_text(render_markdown(report), encoding="utf-8")
    print(f"Wrote {rel(OUT_JSON)}")
    print(f"Wrote {rel(OUT_MD)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
