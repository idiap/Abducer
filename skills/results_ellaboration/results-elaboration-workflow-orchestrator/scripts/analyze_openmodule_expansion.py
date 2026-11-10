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
"""Analyze open-module result extensions in a paper draft and generate TODOs."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[4]
OUT_ROOT = ROOT / "agentic/reports/results_ellaboration"

SECTION_RE = re.compile(r"\\(section|subsection|subsubsection)\{([^{}]+)\}")
TITLE_RE = re.compile(r"\\title\{(.*?)\}", re.S)
PDFTITLE_RE = re.compile(r"pdftitle=\{([^{}]+)\}")
ABSTRACT_RE = re.compile(r"\\begin\{abstract\}(.*?)\\end\{abstract\}", re.S)
OPENMODULE_RE = re.compile(r"\\begin\{openmodule\}\{([^{}]+)\}(.*?)\\end\{openmodule\}", re.S)
LABEL_RE = re.compile(r"\\label\{([^{}]+)\}")
REF_RE = re.compile(r"\\(?:ref|eqref)\{([^{}]+)\}")


MODULE_CONFIG = {
    "G1": {
        "work_class": "geometric_collar_construction",
        "priority": 96,
        "mathematical_object": "cutoff-indexed lattice hairpin family gamma_{i,k}(delta) with locked boundary footprint",
        "depends_on": [],
        "expected_artifact": "A theorem-ready construction of paths gamma_{i,k}(delta), with support, positivity-algebra membership, footprint locking, and a_k/delta scaling.",
        "acceptance": "For each cutoff k and collar delta, the three paths are explicit lattice paths in the positive algebra, share the stated boundary footprint, converge to the intended continuum geometry, and preserve the reflected pairing.",
        "paper_target": "Replace Open module G1 with a subsection containing the path construction, a diagram, and a lemma proving positive-algebra membership and footprint locking.",
        "stop": "Keep G1 open if a single family cannot simultaneously preserve positive-time support, shared footprint, and the declared continuum scaling.",
    },
    "G2": {
        "work_class": "same_theory_renormalized_normalization",
        "priority": 94,
        "mathematical_object": "renormalized same-theory normalization map for perimeter, cusp, and boundary factors",
        "depends_on": ["G1"],
        "expected_artifact": "A positivity-preserving normalization theorem: observable rescaling, congruence, positive-kernel factorization, or direct reflected Gram realization.",
        "acceptance": "Every removed factor is implemented by same-theory observable rescaling or a proved positive-kernel/factorization theorem; no pair-dependent entrywise quotient is used without certificate.",
        "paper_target": "Insert a proposition after the geometric family showing how renormalized observables produce the normalized block.",
        "stop": "Demote the geometric application if any essential normalization remains a pair-dependent entrywise quotient without positivity-preserving realization.",
    },
    "G3": {
        "work_class": "geometric_coefficient_extraction",
        "priority": 92,
        "mathematical_object": "geometric-collar expansion q_{k,delta}=11^T+delta H_k+delta^2 K_k+R_{k,delta}",
        "depends_on": ["G1", "G2"],
        "expected_artifact": "An operator-norm coefficient theorem deriving H_k, K_k and a cutoff-uniform o(delta^2) remainder from the geometric collar.",
        "acceptance": "H_k, K_k are computed from the same normalized block q_{k,delta}; the remainder satisfies sup_k ||R_{k,delta}||/delta^2 -> 0 in the stated joint limit.",
        "paper_target": "Replace Open module G3 with a coefficient theorem and move long expansion algebra to an appendix.",
        "stop": "Do not claim geometric-collar success if only the source-amplitude collision expansion is available.",
    },
    "G4": {
        "work_class": "uniform_non_degeneracy",
        "priority": 90,
        "mathematical_object": "cutoff trajectory lower bounds for sigma_k, tau_k and the reduced Schur-Feshbach margins",
        "depends_on": ["G1", "G2", "G3"],
        "expected_artifact": "A lower-bound theorem or certified numerical/theoretical protocol proving nonvanishing reduced margins along the cutoff trajectory.",
        "acceptance": "The proof gives lower bounds, not only boundedness or nonnegativity, for the quantities that become 2 sigma_k and 2 tau_k / 3 after renormalization.",
        "paper_target": "Insert a theorem or certified finite-evaluation protocol after the coefficient theorem; update the abstract only if a true lower bound is obtained.",
        "stop": "Keep strict continuum-facing margins open if sigma_k or tau_k may vanish along the chosen trajectory.",
    },
    "E1": {
        "work_class": "endpoint_regulator_derivation",
        "priority": 86,
        "mathematical_object": "endpoint source integral, singlet projection, color factor C_col, and incidence tensor for the geometric Wilson family",
        "depends_on": ["G1", "G2", "G3"],
        "expected_artifact": "A regulator-derived endpoint estimator, not an ansatz, with boxes, sources, representation conventions, and incidence weights.",
        "acceptance": "The endpoint formula is derived from the same heat-kernel SU(2) regulator and geometric path incidence; all color and path-ordering factors are named.",
        "paper_target": "Replace E1 with an endpoint derivation subsection and cross-reference the finite null-channel identity.",
        "stop": "Do not infer endpoint signs from an incidence template that has not been derived from the regulated Wilson family.",
    },
    "E2": {
        "work_class": "endpoint_cumulant_tail_bounds",
        "priority": 84,
        "mathematical_object": "two-sided endpoint cumulant and tail error bound Delta_end",
        "depends_on": ["E1"],
        "expected_artifact": "A two-sided error theorem for fourth source derivatives, sixth-derivative stencil errors, endpoint/corner tails, and inter-box terms.",
        "acceptance": "The bound supplies |R_end - Rhat_end| <= Delta_end in the same regulator; it supports both positive and negative endpoint certificates without one-sided overclaiming.",
        "paper_target": "Replace E2 with a theorem after the endpoint estimator and update the endpoint certificate paragraph.",
        "stop": "A one-sided lower bound may certify positivity if M_G-U>0, but must not be reported as a negative obstruction.",
    },
    "M1": {
        "work_class": "continuum_reconstruction",
        "priority": 78,
        "mathematical_object": "infinite-volume continuum Schwinger functions satisfying the full OS axioms on a separating Wilson algebra",
        "depends_on": ["G1", "G2", "G3", "G4"],
        "expected_artifact": "A reconstruction theorem or a precise citation-backed handoff showing all OS axioms beyond finite reflection positivity.",
        "acceptance": "The result constructs or imports continuum Schwinger functions in the same theory and verifies the OS requirements needed for Hilbert-space reconstruction.",
        "paper_target": "Keep as a bounded future-work theorem unless the paper genuinely proves continuum reconstruction.",
        "stop": "Do not promote finite block positivity into OS reconstruction.",
    },
    "M2": {
        "work_class": "spectral_gap_estimate",
        "priority": 76,
        "mathematical_object": "same-theory Hamiltonian spectral gap estimate for the reconstructed continuum theory",
        "depends_on": ["M1"],
        "expected_artifact": "A spectral theorem or explicit same-theory decay estimate implying no spectrum in (0, Delta).",
        "acceptance": "The argument derives the gap after reconstruction and does not assume exponential clustering, mass gap, or spectral isolation as an input.",
        "paper_target": "Keep as a final open module or future-work theorem; do not include in the finite Route A claim.",
        "stop": "Quarantine any endpoint or finite-block argument that assumes the gap it is supposed to help prove.",
    },
}


def clean_tex(value: str) -> str:
    value = re.sub(r"%.*", "", value)
    value = value.replace("\n", " ")
    value = re.sub(r"\s+", " ", value).strip()
    return value


def slugify(value: str) -> str:
    value = re.sub(r"[^a-zA-Z0-9]+", "-", value.lower()).strip("-")
    return value[:80] or "openmodule-expansion"


def current_section(sections: list[dict[str, Any]], offset: int) -> str:
    active = ""
    for section in sections:
        if section["offset"] <= offset:
            active = section["title"]
        else:
            break
    return active


def module_key(title: str) -> str:
    match = re.match(r"\s*([A-Z]\d+)", title)
    return match.group(1) if match else slugify(title).upper()


def module_display_title(title: str) -> str:
    return re.sub(r"^\s*[A-Z]\d+:\s*", "", title).strip()


def extract_title(text: str, path: Path) -> str:
    pdf_title_match = PDFTITLE_RE.search(text)
    if pdf_title_match:
        return clean_tex(pdf_title_match.group(1))
    title_match = TITLE_RE.search(text)
    if not title_match:
        return path.stem
    title = title_match.group(1)
    title = re.sub(r"\\texorpdfstring\{([^{}]*)\}\{([^{}]*)\}", r"\2", title)
    return clean_tex(title)


def parse(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    title = extract_title(text, path)
    abstract_match = ABSTRACT_RE.search(text)
    abstract = clean_tex(abstract_match.group(1)) if abstract_match else ""
    sections = [
        {"level": m.group(1), "title": clean_tex(m.group(2)), "offset": m.start()}
        for m in SECTION_RE.finditer(text)
    ]
    modules = []
    for index, match in enumerate(OPENMODULE_RE.finditer(text), start=1):
        title_text = clean_tex(match.group(1))
        key = module_key(title_text)
        display_title = module_display_title(title_text)
        config = MODULE_CONFIG.get(key, {})
        body = clean_tex(match.group(2))
        modules.append(
            {
                "module_id": key,
                "title": display_title,
                "source_title": title_text,
                "section": current_section(sections, match.start()),
                "source_excerpt": body[:1400],
                "work_class": config.get("work_class", "open_module"),
                "priority": config.get("priority", 70),
                "mathematical_object": config.get("mathematical_object", "open result module"),
                "depends_on": config.get("depends_on", []),
                "expected_artifact": config.get("expected_artifact", "A manuscript-ready theorem, computation, or bounded open-module revision."),
                "acceptance_criterion": config.get("acceptance", "The module is resolved by a checkable artifact or explicitly retained as open."),
                "paper_insertion_target": config.get("paper_target", "Replace or refine the open module in its current section."),
                "stop_or_quarantine_condition": config.get("stop", "Keep open if no checkable artifact can be produced."),
            }
        )
    labels = LABEL_RE.findall(text)
    refs = REF_RE.findall(text)
    return {
        "source_path": str(path),
        "source_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
        "title": title,
        "abstract": abstract,
        "sections": sections,
        "open_modules": modules,
        "label_audit": {
            "label_count": len(labels),
            "duplicate_labels": sorted({label for label in labels if labels.count(label) > 1}),
            "missing_refs": sorted(set(refs) - set(labels)),
        },
        "deterministic_claims": [
            "TeX label/reference audit",
            "pdflatex compilation",
            "symbolic verification of H,K,A,C, determinant, and reduced eigenvalues",
            "boundedness checks for sigma in [0,1] and tau in [0,4]",
        ],
    }


def deterministic_regime(module: dict[str, Any]) -> list[str]:
    key = module["module_id"]
    if key in {"G1", "G2", "G3", "G4", "E1", "E2"}:
        return [
            "extract all equations and labels cited by the module",
            "compile the TeX after any patch",
            "check that new refs resolve and no claim-boundary warnings are introduced",
        ]
    if key == "M1":
        return ["audit finite-vs-continuum wording", "check OS axiom list is explicit", "compile after future-work edits"]
    if key == "M2":
        return ["audit no circular use of mass gap or exponential decay", "check spectral notation is defined", "compile after future-work edits"]
    return ["compile", "label audit"]


def generative_regime(module: dict[str, Any]) -> list[str]:
    key = module["module_id"]
    return {
        "G1": [
            "design a cutoff-indexed path family that locks the boundary footprint without leaving the positive-time algebra",
            "reason about the joint scaling of lattice spacing a_k and collar parameter delta",
            "identify which geometry features must survive the continuum limit",
        ],
        "G2": [
            "invent or prove the positivity-preserving renormalization mechanism for perimeter, cusp, and boundary factors",
            "separate one-body congruence factors from pair-dependent factors",
            "decide whether a positive-kernel theorem is needed",
        ],
        "G3": [
            "derive H_k and K_k from the geometric collar, not from source amplitudes",
            "choose the correct expansion parameter and topology for operator-norm convergence",
            "localize which Wilson-loop estimates control the o(delta^2) remainder",
        ],
        "G4": [
            "find a theoretical or certified computational route to nonvanishing lower margins",
            "analyze whether renormalized Wilson-loop correlations can vanish along the cutoff trajectory",
            "decide whether the finite Route A block is a useful model or needs a sharper geometry",
        ],
        "E1": [
            "derive endpoint boxes and source variables from the actual geometric paths",
            "construct the SU(2) singlet/color factor calculation from the heat-kernel measure",
            "connect incidence weights to the exact null-channel identity",
        ],
        "E2": [
            "design two-sided cumulant and tail estimates strong enough for endpoint certificates",
            "use the five-point stencil only after a sixth-derivative bound is available",
            "separate positive certificates from negative obstruction certificates",
        ],
        "M1": [
            "state the exact OS reconstruction theorem needed after finite-block positivity",
            "map finite Wilson algebra to a separating continuum Wilson algebra",
            "identify which compactness/tightness estimates are missing",
        ],
        "M2": [
            "translate finite Euclidean decay or transfer-matrix estimates into Hamiltonian spectral language",
            "avoid circular gap assumptions",
            "state what same-theory observable sector would witness the gap",
        ],
    }.get(key, ["construct a proof strategy", "state validation obligations"])


def subtasks(module: dict[str, Any]) -> list[str]:
    key = module["module_id"]
    common = [
        f"Restate {key} as a theorem/proposition target with definitions before the statement.",
        "Name every input inherited from earlier Route A sections and every new object introduced here.",
        "Specify the deterministic checks that must pass before manuscript integration.",
        "Specify the generative proof or construction work needed beyond deterministic checks.",
        "Write the paper insertion or demotion text depending on whether the module succeeds.",
    ]
    specific = {
        "G1": [
            "Give explicit vertex/edge sequences for gamma_{+,k}(delta), gamma_{-,k}(delta), and gamma_{0,k}(delta).",
            "Prove support remains in the positive-time algebra for every k,delta.",
            "Prove the reflected boundary footprint is locked while the collar collapses geometrically.",
            "State the joint scaling rule for a_k and delta.",
        ],
        "G2": [
            "Classify all perimeter, cusp, and boundary factors as one-body, block, or pair-dependent.",
            "Prove congruence for all one-body factors.",
            "For pair-dependent factors, construct a positive kernel or demote the normalization.",
        ],
        "G3": [
            "Derive entrywise expansions from the geometric-collar Wilson block.",
            "Convert entrywise/log coefficients into H_k,K_k.",
            "Prove the cutoff-uniform operator-norm remainder.",
        ],
        "G4": [
            "Express sigma_k,tau_k after renormalization on the cutoff trajectory.",
            "Prove or certify positive lower bounds.",
            "Demote strict-margin continuum language if only finite nonnegativity is known.",
        ],
        "E1": [
            "Define endpoint boxes and source variables from G1 geometry.",
            "Derive C_col and incidence weights from SU(2) heat-kernel integrals.",
            "Show the estimator is same-regulator and not imported from an ansatz.",
        ],
        "E2": [
            "Prove a sixth-derivative source bound on the stated source domain.",
            "Bound endpoint, corner, inter-box, and tail terms on both sides.",
            "State which certificate is positive, negative, or inconclusive.",
        ],
        "M1": [
            "List all OS axioms not supplied by finite block positivity.",
            "State the continuum limit topology and Wilson algebra.",
            "Identify required tightness, nontriviality, and reconstruction inputs.",
        ],
        "M2": [
            "Define the reconstructed Hamiltonian and excitation sector.",
            "State the decay or transfer estimate sufficient for a spectral gap.",
            "Audit every step for circular use of exponential decay or a gap.",
        ],
    }.get(key, [])
    return specific + common


def build_todos(parsed: dict[str, Any]) -> list[dict[str, Any]]:
    todos: list[dict[str, Any]] = []
    deterministic_todos = [
        {
            "todo_id": "todo-001",
            "source_marker": "deterministic:finite-route-a-algebra",
            "source_title": "Integrate and certify the supplied three-hairpin verification script",
            "target_section": "Coefficient extraction and the finite certificate",
            "work_class": "deterministic_symbolic_validation",
            "priority": 98,
            "depends_on": [],
            "mathematical_object": "N_eps, D_eps, q_eps, H,K,A,C, det(q_eps), z^T PKP z, z^T correction z, z^T C z, and reduced u/v margins",
            "required_inputs": [
                "verify_three_hairpin_block.py",
                "eq:N-exact",
                "eq:D-normalization",
                "eq:q-exact",
                "eq:alpha-beta",
                "eq:H-explicit",
                "eq:K-explicit",
                "thm:evaluated-gate",
            ],
            "subtasks": [
                "Import the supplied `verify_three_hairpin_block.py` logic into the result-elaboration workflow rather than leaving it in Downloads.",
                "Verify symbolically that N_eps=11^T+eps sigma bb^T+eps^2 tau cc^T and q_eps=D_eps N_eps D_eps.",
                "Differentiate q_eps at eps=0 to recover the displayed H and K matrices.",
                "Verify A=PHP=sigma bb^T and C=P(K-1/3 Hee^T H)P=-sigma^2 bb^T+(tau/9)zz^T.",
                "Verify det(q_eps)=4 eps^3 sigma tau / ((1+eps sigma)^2(1+eps^2 tau)).",
                "Verify z^T PKP z=sigma^2+4 tau, z^T(1/3 PHee^T HP)z=sigma^2, and z^T C z=4 tau.",
                "Verify u^T A u=2 sigma, v^T C v=2 tau/3, and u^T C v=0.",
                "Emit JSON and Markdown certificates that the paper can cite from the reproducibility protocol.",
                "Write any discrepancy as a paper correction TODO, not as a hidden assumption.",
            ],
            "deterministic_regime": ["sympy exact algebra", "TeX equation reference audit", "pdflatex"],
            "generative_regime": [
                "interpret whether the exact source block is scientifically strong enough or needs geometric collar replacement",
                "decide how the certificate should be narrated: as proof support for finite Route A, not as evidence for G1-G4",
            ],
            "critical_self_refinement": [
                "Does the symbolic check verify only the source-collision model, or is it being overread as geometric collar evidence?",
                "Does the determinant strictness depend only on sigma,tau > 0?",
                "Does the paper make the spurious sigma^2 cancellation visible enough for readers to understand why Schur-Feshbach matters?",
            ],
            "expected_artifact": "A repo-local `routea_three_hairpin_certificate.json` and Markdown certificate verifying all displayed finite algebra.",
            "acceptance_criterion": "The supplied script's symbolic identities pass in the repo workflow and the certificate explicitly records every scalar identity used in the Route A narrative.",
            "paper_insertion_target": "Cite the certificate in the finite evaluation and reproducibility protocol, and add one sentence explaining that it certifies only the finite source-collision block.",
            "validation_handoff": "Run `verify_routea_three_hairpin_block.py`, then `results-critical-self-refiner`.",
            "stop_or_quarantine_condition": "Do not proceed to open-module proof planning if the current finite algebra is inconsistent.",
            "recommended_skills": ["results-open-module-decomposer", "results-critical-self-refiner", "results-expansion-validator"],
            "narrative_consequence": "This protects the claim that Route A has an exact finite-cutoff block rather than a schematic one.",
        },
        {
            "todo_id": "todo-002",
            "source_marker": "deterministic:manuscript-integrity",
            "source_title": "Compile and audit manuscript integrity before expansion",
            "target_section": "whole draft",
            "work_class": "deterministic_manuscript_validation",
            "priority": 97,
            "depends_on": [],
            "mathematical_object": "TeX labels, references, citations, theorem numbering, and open-module environments",
            "required_inputs": ["full TeX draft"],
            "subtasks": [
                "Run label/reference audit and identify duplicate or missing labels.",
                "Compile the TeX to PDF.",
                "Check that all open modules are visible in the final PDF.",
                "Check that claims through Corollary implemented-route-a remain finite-cutoff claims.",
                "Record warnings that affect scientific readability.",
            ],
            "deterministic_regime": ["regex label/ref audit", "pdflatex", "openmodule count"],
            "generative_regime": ["interpret whether warnings indicate a conceptual overclaim or only formatting debt"],
            "critical_self_refinement": [
                "Does the paper hide any open module in prose rather than stating it?",
                "Does the abstract claim more than the sections prove?",
            ],
            "expected_artifact": "A compile/log and claim-boundary audit.",
            "acceptance_criterion": "The manuscript compiles, references resolve, and claim boundaries remain consistent with the open modules.",
            "paper_insertion_target": "Apply corrections globally before expanding any module.",
            "validation_handoff": "Run TeX compile and `results-expansion-validator`.",
            "stop_or_quarantine_condition": "Do not expand results on top of an uncompilable or internally inconsistent draft.",
            "recommended_skills": ["results-critical-self-refiner", "results-expansion-validator"],
            "narrative_consequence": "This ensures the finite Route A contribution is inspectable before future-module ambition is added.",
        },
    ]
    todos.extend(deterministic_todos)
    for index, module in enumerate(sorted(parsed["open_modules"], key=lambda item: (-item["priority"], item["module_id"])), start=3):
        todos.append(
            {
                "todo_id": f"todo-{index:03d}",
                "source_marker": module["module_id"],
                "source_title": module["title"],
                "target_section": module["section"],
                "work_class": module["work_class"],
                "priority": module["priority"],
                "depends_on": module["depends_on"],
                "mathematical_object": module["mathematical_object"],
                "required_inputs": ["finite Route A construction", "source open module", *module["depends_on"]],
                "subtasks": subtasks(module),
                "deterministic_regime": deterministic_regime(module),
                "generative_regime": generative_regime(module),
                "critical_self_refinement": [
                    "Does success change a theorem/proposition/table in the paper, or only restate an open module?",
                    "What would force demotion back to an explicit open module?",
                    "Does the task rely on discovery workflows or hidden target queues? If so, reject the coupling.",
                ],
                "expected_artifact": module["expected_artifact"],
                "acceptance_criterion": module["acceptance_criterion"],
                "paper_insertion_target": module["paper_insertion_target"],
                "validation_handoff": "Run deterministic checks, then `results-critical-self-refiner`, then `results-expansion-validator`.",
                "stop_or_quarantine_condition": module["stop_or_quarantine_condition"],
                "recommended_skills": [
                    "results-open-module-decomposer",
                    "results-extension-strategy-planner",
                    "results-critical-self-refiner",
                    "results-narrative-integrator",
                    "results-expansion-validator",
                ],
                "narrative_consequence": f"Resolving {module['module_id']} determines whether the paper can move beyond finite source-collision Route A toward {module['work_class']}.",
            }
        )
    return todos


def build_report(parsed: dict[str, Any]) -> dict[str, Any]:
    todos = build_todos(parsed)
    return {
        "schema": "abducer.results_elaboration.openmodule.v1",
        "context": {
            "source_path": parsed["source_path"],
            "source_sha256": parsed["source_sha256"],
            "title": parsed["title"],
            "bounded_contribution": "Finite-cutoff SU(2) heat-kernel Route A realization of a reflected Wilson-block Schur-Feshbach test, with geometric collar, endpoint, continuum, and gap steps isolated as open modules.",
            "explicit_non_claims": [
                "does not prove a continuum Yang-Mills measure",
                "does not prove full OS reconstruction",
                "does not prove a mass gap",
                "does not prove geometric collar collapse from the source-collision model",
            ],
            "abstract": parsed["abstract"],
        },
        "source_structure": {
            "section_count": len(parsed["sections"]),
            "sections": parsed["sections"],
            "open_module_count": len(parsed["open_modules"]),
            "open_modules": parsed["open_modules"],
            "slot_count": len(parsed["open_modules"]),
            "slots": parsed["open_modules"],
            "label_audit": parsed["label_audit"],
        },
        "workflow": {
            "folder": "skills/results_ellaboration",
            "independent_from_discovery": True,
            "skill_sequence": [
                "results-context-interpreter",
                "results-open-module-decomposer",
                "results-extension-strategy-planner",
                "results-critical-self-refiner",
                "results-narrative-integrator",
                "results-expansion-validator",
            ],
            "local_hooks": [
                "pre_context_interpretation",
                "post_open_module_extraction",
                "post_deterministic_regime_audit",
                "post_generative_strategy_planning",
                "post_critical_self_refinement",
                "post_narrative_integration",
                "final_results_elaboration_validation",
            ],
            "forbidden_couplings": [
                "discovery marathon jobs",
                "branch schedulers",
                "target active pointers",
                "long-horizon discovery queues",
                "global hooks/hooks.json mutation",
            ],
        },
        "todos": todos,
        "todo_review": {
            "limitations_found": [
                "The older slot workflow misses Route A because this draft uses openmodule environments.",
                "The paper already has a finite result, so TODOs must not ask to re-prove what is already implemented.",
                "Open modules mix deterministic validation, generative proof design, and manuscript narrative updates unless explicitly separated.",
            ],
            "repairs_applied": [
                "Open modules are parsed as first-class result-extension obligations.",
                "Every TODO now has deterministic_regime, generative_regime, and critical_self_refinement fields.",
                "Every TODO names how successful results feed back into the paper and how failure remains as a bounded open module.",
            ],
        },
        "narrative_integration": {
            "spine": [
                "The finite SU(2) heat-kernel source-collision block is the claimable core.",
                "The immediate paper-strengthening task is to integrate the supplied three-hairpin verification script as a citable certificate for the exact finite algebra.",
                "The next scientific step is not more source-amplitude algebra but a geometric collar family G1-G4.",
                "Endpoint and spectral modules are downstream; they should not be promoted until the geometric/cutoff modules discharge.",
            ],
            "paper_updates_after_discharge": [
                "If the verification script passes, cite `routea_three_hairpin_certificate.json` in the reproducibility protocol and state that it verifies the finite source-collision algebra only.",
                "If G1-G4 discharge, revise the abstract from source-collision realization to geometric-collar realization.",
                "If E1-E2 discharge, add endpoint theorem language with two-sided certificate logic.",
                "Keep M1-M2 as open modules unless continuum reconstruction and spectral estimates are actually proved.",
            ],
        },
    }


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Open-Module Results Elaboration Plan",
        "",
        f"- Source: `{report['context']['source_path']}`",
        f"- Title: {report['context']['title']}",
        f"- Open modules: {report['source_structure']['open_module_count']}",
        f"- Independent from discovery workflows: `{report['workflow']['independent_from_discovery']}`",
        "",
        "## Claim Boundary",
        "",
        report["context"]["bounded_contribution"],
        "",
        "Non-claims:",
    ]
    for item in report["context"]["explicit_non_claims"]:
        lines.append(f"- {item}")
    lines += ["", "## Extracted Open Modules", ""]
    for module in report["source_structure"]["open_modules"]:
        lines += [
            f"### {module['module_id']}: {module['title']}",
            "",
            f"- Section: {module['section']}",
            f"- Work class: `{module['work_class']}`",
            f"- Priority: {module['priority']}",
            f"- Mathematical object: {module['mathematical_object']}",
            f"- Acceptance criterion: {module['acceptance_criterion']}",
            "",
        ]
    lines += ["## Ordered Self-Contained TODOs", ""]
    for todo in report["todos"]:
        lines += [
            f"### {todo['todo_id']}: {todo['source_title']}",
            "",
            f"- Source marker: `{todo['source_marker']}`",
            f"- Target section: {todo['target_section']}",
            f"- Work class: `{todo['work_class']}`",
            f"- Priority: {todo['priority']}",
            f"- Mathematical object: {todo['mathematical_object']}",
            f"- Depends on: {', '.join(todo['depends_on']) if todo['depends_on'] else 'none'}",
            f"- Required inputs: {', '.join(todo['required_inputs'])}",
            "- Subtasks:",
            *[f"  - {step}" for step in todo["subtasks"]],
            "- Deterministic regime:",
            *[f"  - {step}" for step in todo["deterministic_regime"]],
            "- Generative regime:",
            *[f"  - {step}" for step in todo["generative_regime"]],
            "- Critical self-refinement:",
            *[f"  - {step}" for step in todo["critical_self_refinement"]],
            f"- Expected artifact: {todo['expected_artifact']}",
            f"- Acceptance criterion: {todo['acceptance_criterion']}",
            f"- Paper insertion target: {todo['paper_insertion_target']}",
            f"- Validation handoff: {todo['validation_handoff']}",
            f"- Stop/quarantine condition: {todo['stop_or_quarantine_condition']}",
            f"- Skills: {', '.join(todo['recommended_skills'])}",
            f"- Narrative consequence: {todo['narrative_consequence']}",
            "",
        ]
    lines += ["## Critical Self-Refinement Summary", ""]
    lines.append("Limitations found:")
    for item in report["todo_review"]["limitations_found"]:
        lines.append(f"- {item}")
    lines += ["", "Repairs applied:"]
    for item in report["todo_review"]["repairs_applied"]:
        lines.append(f"- {item}")
    lines += ["", "## Narrative Integration", ""]
    for item in report["narrative_integration"]["spine"]:
        lines.append(f"- {item}")
    lines += ["", "Paper updates after discharge:"]
    for item in report["narrative_integration"]["paper_updates_after_discharge"]:
        lines.append(f"- {item}")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("draft", type=Path)
    args = parser.parse_args()
    draft = args.draft.expanduser().resolve()
    parsed = parse(draft)
    report = build_report(parsed)
    slug = slugify(parsed["title"])
    out_dir = OUT_ROOT / slug
    out_dir.mkdir(parents=True, exist_ok=True)
    json_path = out_dir / "latest.json"
    md_path = out_dir / "latest.md"
    json_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    md_path.write_text(render_markdown(report), encoding="utf-8")
    print(f"Wrote {json_path}")
    print(f"Wrote {md_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
