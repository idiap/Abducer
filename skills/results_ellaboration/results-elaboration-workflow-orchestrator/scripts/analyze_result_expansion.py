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
"""Analyze result-expansion markers in a paper draft and generate elaboration TODOs."""

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
TITLE_RE = re.compile(r"\\title\{([^{}]+)\}")
ABSTRACT_RE = re.compile(r"\\begin\{abstract\}(.*?)\\end\{abstract\}", re.S)
SLOT_RE = re.compile(r"\\begin\{slot\}\[([^\]]+)\](.*?)\\end\{slot\}", re.S)
LABEL_RE = re.compile(r"\\label\{([^{}]+)\}")
REF_RE = re.compile(r"\\(?:ref|eqref)\{([^{}]+)\}")
TODO_RE = re.compile(r"(?i)\b(TODO|FIXME|placeholder|future theorem|missing QFT|remove before journal submission|should contain|should state|must be|must supply|must compute|must prove|needs?)\b")


WORK_CLASS_BY_TITLE = [
    ("Regulator and observable", "proof_completion"),
    ("Same-theory quotient", "same_theory_transfer"),
    ("Boundary-OPE coefficient", "coefficient_extraction"),
    ("Nontrivial finite outcome", "finite_application"),
    ("Endpoint color", "coefficient_extraction"),
    ("Uniform endpoint", "coefficient_extraction"),
    ("Prior-art", "prior_art_boundary"),
    ("Three-hairpin coefficient table", "finite_application"),
]


SKILL_BY_WORK_CLASS = {
    "draft_context": ["results-context-interpreter"],
    "proof_completion": ["results-extension-need-extractor", "finite-theorem-section-packager", "results-expansion-validator"],
    "coefficient_extraction": [
        "results-extension-need-extractor",
        "endpoint-worked-calculation-packager",
        "results-narrative-integrator",
        "results-expansion-validator",
    ],
    "same_theory_transfer": [
        "results-extension-need-extractor",
        "bridge-object-equivalence-checker",
        "finite-theorem-section-packager",
        "results-expansion-validator",
    ],
    "finite_application": [
        "results-extension-need-extractor",
        "endpoint-worked-calculation-packager",
        "finite-theorem-section-packager",
        "results-narrative-integrator",
        "results-expansion-validator",
    ],
    "prior_art_boundary": [
        "results-extension-need-extractor",
        "prior-art-positioning-packager",
        "timeline-reference-manager",
        "results-expansion-validator",
    ],
    "narrative_integration": ["results-narrative-integrator", "results-expansion-validator"],
    "submission_cleanup": ["results-expansion-validator"],
}


def clean_tex(value: str) -> str:
    value = re.sub(r"%.*", "", value)
    value = value.replace("\n", " ")
    value = re.sub(r"\s+", " ", value).strip()
    return value


def slugify(value: str) -> str:
    value = re.sub(r"[^a-zA-Z0-9]+", "-", value.lower()).strip("-")
    return value[:80] or "result-expansion"


def current_section(sections: list[dict[str, Any]], offset: int) -> str:
    active = ""
    for section in sections:
        if section["offset"] <= offset:
            active = section["title"]
        else:
            break
    return active


def work_class_for(title: str) -> str:
    for marker, work_class in WORK_CLASS_BY_TITLE:
        if marker.lower() in title.lower():
            return work_class
    return "proof_completion"


def priority_for(work_class: str, title: str) -> int:
    if work_class == "same_theory_transfer":
        return 95
    if "Boundary-OPE" in title:
        return 92
    if "Regulator" in title:
        return 90
    if "Nontrivial" in title:
        return 88
    if "Endpoint color" in title:
        return 84
    if "Uniform endpoint" in title:
        return 82
    if "Three-hairpin" in title:
        return 80
    if work_class == "prior_art_boundary":
        return 74
    return 70


def required_inputs(work_class: str, title: str) -> list[str]:
    base = {
        "proof_completion": [
            "precise theorem statement",
            "definitions and validity regime",
            "proof dependencies",
            "claim-boundary audit",
        ],
        "same_theory_transfer": [
            "regulated Wilson observable algebra",
            "normalization map",
            "positivity-preserving representation",
            "counterexample check for entrywise division",
        ],
        "coefficient_extraction": [
            "fixed regulator",
            "observable family",
            "coefficient definitions",
            "uniform remainder regime",
        ],
        "finite_application": [
            "finite Wilson geometry",
            "reflected Gram block",
            "computed H and K",
            "Schur-corrected null-sector test",
        ],
        "prior_art_boundary": [
            "finite theorem claim",
            "application claim",
            "candidate references",
            "novelty boundary language",
        ],
    }.get(work_class, ["source marker", "paper section", "validation boundary"])
    if "Endpoint color" in title:
        return base + ["gauge group", "representation normalization", "path ordering convention", "plaquette-sheet convention"]
    if "Uniform endpoint" in title:
        return base + ["source domain", "fourth/sixth derivative bound", "tail term definition"]
    if "Three-hairpin" in title:
        return base + ["three paths", "pair table", "zero-sum cancellation data", "endpoint/remainder columns"]
    return base


def expected_artifact(work_class: str, title: str) -> str:
    if work_class == "same_theory_transfer":
        return "A theorem or proposition replacing the schematic quotient with a positivity-preserving same-theory construction."
    if "Boundary-OPE" in title:
        return "A coefficient theorem giving explicit or bounded H_a and K_a with an O_a(eps^3) or stated replacement remainder."
    if "Regulator and observable" in title:
        return "A regulator theorem naming the finite lattice, gauge group, action, reflection map, positive-time algebra, Wilson collar observables, and the resulting reflected Gram block."
    if "Endpoint color" in title:
        return "A regulator-specific derivation of C_col^(G,R,reg) with all representation and path-ordering conventions exposed."
    if "Uniform endpoint" in title:
        return "A uniform endpoint/tail estimate with source domain, constants, and limit regime."
    if "Nontrivial" in title:
        return "A finite sign/margin/obstruction result obtained by applying the Schur-Feshbach theorem to computed H_a,K_a."
    if "Three-hairpin" in title:
        return "A reproducible coefficient table for the three-hairpin block, including cancellation and corrected second-order survivors."
    if work_class == "prior_art_boundary":
        return "A prior-art boundary paragraph/table that limits novelty to the proved finite packaging and coefficient calculation."
    return "A replacement theorem, proof, computation, or paragraph that discharges the source marker."


def acceptance_criterion(work_class: str, title: str) -> str:
    if "Regulator and observable" in title:
        return "A reader can construct q_{a,eps} from the stated finite regulated Wilson data and verify reflection positivity without importing unstated continuum assumptions."
    if work_class == "same_theory_transfer":
        return "The normalized block is proved to be a reflected Gram block, diagonal/block congruence, or positive-kernel factorization inside the same regulated theory."
    if "Boundary-OPE" in title:
        return "H_a and K_a are derived from q_{a,eps} in the chosen regulator, converted from log-coefficients when needed, and accompanied by an explicit operator-norm remainder."
    if "Endpoint color" in title:
        return "C_col^(G,R,reg) is derived from a named finite group/source integral with trace, representation, orientation, and path-ordering conventions fixed."
    if "Uniform endpoint" in title:
        return "The endpoint remainder and tail terms are bounded uniformly over the named finite block in the exact limit regime used by the application."
    if "Nontrivial finite outcome" in title:
        return "For one named Wilson block, the Schur-Feshbach test produces a strict margin, a null-sector scalar, a negative diagnostic vector, or a degeneracy certificate."
    if "Three-hairpin" in title:
        return "The three-hairpin section contains a reproducible pair-indexed coefficient table and the associated Schur-corrected scalar or explicit demotion to template status."
    if work_class == "prior_art_boundary":
        return "Novelty language cites prior art and excludes claims not proved in the draft."
    return "The marker can be removed and replaced by final paper text without weakening the theorem statement or hiding proof debt."


def stop_condition(work_class: str, title: str) -> str:
    if "Three-hairpin" in title:
        return "Quarantine the three-hairpin application if the path geometry, pair table, H,K entries, or Schur-corrected scalar cannot be reproduced from the draft data."
    if "Nontrivial finite outcome" in title:
        return "Demote to application template if no strict margin, null-sector scalar, negative vector, or degeneracy certificate is produced for a named finite block."
    if work_class == "same_theory_transfer":
        return "Demote the Wilson application if normalization remains pair-dependent entrywise division and no same-theory Gram realization, congruence, or positive-kernel factorization is proved."
    if "Boundary-OPE" in title:
        return "Stop coefficient expansion if H_a,K_a cannot be derived from the same q_{a,eps}; do not substitute informal OPE language for matrix coefficients."
    if "Endpoint color" in title:
        return "Keep endpoint constants conditional if the color prefactor cannot be derived from the same regulator, group integral, trace convention, and path-ordering convention."
    if "Uniform endpoint" in title:
        return "Keep endpoint algebra out of the result claim if the remainder is not uniform in the variables used by the finite Schur-Feshbach margin."
    if work_class == "prior_art_boundary":
        return "Stop when novelty language is bounded by cited prior art and unsupported broader novelty claims are removed."
    return "Quarantine the Wilson-block application if the finite regulator, reflection plane, positive-time algebra, and Wilson observable support convention cannot be fixed in one setting."


def limitation_addressed(slot: dict[str, Any]) -> str:
    title = slot["title"]
    if "Regulator and observable" in title:
        return "The draft currently names QFT data schematically; this TODO forces a concrete finite regulated setting before any quotient or coefficient theorem is allowed to rely on it."
    if "Same-theory quotient" in title:
        return "The draft warns that entrywise normalization is schematic; this TODO prevents the paper from smuggling positivity through an unsupported quotient."
    if "Boundary-OPE" in title:
        return "The draft needs H_a and K_a as matrix coefficients, not just qualitative OPE language; this TODO demands a same-regulator derivation and remainder."
    if "Nontrivial finite outcome" in title:
        return "The draft has a finite theorem but needs one concrete Wilson-block consequence; this TODO blocks narrative promotion unless a sign, margin, vector, or degeneracy is computed."
    if "Endpoint color" in title:
        return "The draft uses placeholder endpoint constants; this TODO requires the color/combinatorial factor to be derived rather than named."
    if "Uniform endpoint" in title:
        return "The endpoint algebra is conditional until tails are controlled; this TODO tests whether the asymptotic estimate is strong enough for the finite positivity margin."
    if "Prior-art" in title:
        return "The contribution boundary is fragile; this TODO prevents the manuscript from claiming novelty already covered by Schur complements, Feshbach maps, or lattice reflection positivity."
    if "Three-hairpin" in title:
        return "The application template is not yet a worked example; this TODO forces a reproducible table and Schur-corrected scalar for the three-hairpin block."
    return "The marker needs to become checked manuscript text with an explicit claim boundary."


def paper_insertion_target(slot: dict[str, Any]) -> str:
    title = slot["title"]
    if "Regulator and observable" in title:
        return "Replace the regulator slot with a proposition immediately before the same-theory quotient discussion."
    if "Same-theory quotient" in title:
        return "Replace the quotient slot with a theorem/proposition and add a short warning paragraph for quotient forms that fail the certificate."
    if "Boundary-OPE" in title:
        return "Replace the coefficient slot with a theorem and move derivational details to an appendix if they are too long for the main text."
    if "Nontrivial finite outcome" in title:
        return "Insert the resulting finite sign or degeneracy statement as the first concrete application after the coefficient theorem."
    if "Endpoint color" in title:
        return "Replace the endpoint-color slot and cross-reference it from the conditional endpoint cumulant section."
    if "Uniform endpoint" in title:
        return "Replace the uniform-remainder slot and cite it in the finite margin or obstruction inequality."
    if "Prior-art" in title:
        return "Rewrite the introduction and discussion novelty paragraphs, not only the placeholder slot."
    if "Three-hairpin" in title:
        return "Insert the table in the three-hairpin section and cite it from the nontrivial finite outcome."
    return "Replace the source marker with final manuscript text in its current section."


def dependency_labels(slot: dict[str, Any]) -> list[str]:
    title = slot["title"]
    if "Same-theory" in title:
        return ["slot:regulator-observable"]
    if "Boundary-OPE" in title:
        return ["slot:regulator-observable", "slot:same-theory-quotient"]
    if "Nontrivial" in title:
        return ["slot:HK-theorem"]
    if "Endpoint color" in title:
        return ["slot:regulator-observable", "slot:HK-theorem"]
    if "Uniform endpoint" in title:
        return ["slot:regulator-observable", "slot:color-factor"]
    if "Three-hairpin" in title:
        return ["slot:regulator-observable", "slot:same-theory-quotient", "slot:HK-theorem", "slot:nontrivial-outcome"]
    if "Prior-art" in title:
        return ["slot:regulator-observable", "slot:same-theory-quotient", "slot:HK-theorem", "slot:nontrivial-outcome"]
    return []


def subtasks_for(slot: dict[str, Any]) -> list[str]:
    title = slot["title"]
    if "Regulator and observable" in title:
        return [
            "Choose exactly one regulated setting, preferably the heat-kernel plaquette action if endpoint cumulants are part of the expansion.",
            "State the finite lattice, reflection plane, positive-time edge convention, collar support convention, group G, representation R, and Wilson observable family.",
            "Prove or cite reflection positivity for the chosen finite measure and reflection plane.",
            "Prove each Wilson observable lies in the positive-time gauge-invariant algebra.",
            "Write the theorem so it can be cited before any quotient or coefficient calculation.",
        ]
    if "Same-theory quotient" in title:
        return [
            "Write the current quotient formula entrywise and classify every normalization factor as one-body, block, or pair-dependent.",
            "For one-body factors, prove the equivalent diagonal congruence.",
            "For pair-dependent factors, either construct a positive-kernel factorization or prove the normalized observables whose reflected Gram block is q.",
            "Run a finite counterexample check showing why unsupported entrywise division cannot be assumed positivity-preserving.",
            "Replace the slot with the strongest valid theorem: congruence, factorization, direct Gram realization, or explicit demotion.",
        ]
    if "Boundary-OPE" in title:
        return [
            "Freeze the regulator, Wilson family, collar parameter, and coefficient convention.",
            "Define H_a and K_a from the actual normalized block q_{a,eps}, not from an informal log expression alone.",
            "If logarithmic coefficients are used, apply the finite log-to-matrix conversion from the appendix.",
            "State whether the formulas are exact at fixed lattice spacing, asymptotic in a heat-kernel parameter, or interval-bounded.",
            "Give an explicit operator-norm remainder and the regime in which it is valid.",
        ]
    if "Nontrivial finite outcome" in title:
        return [
            "Select the first concrete finite Wilson block to test, with n, observable labels, and geometry fixed.",
            "Compute PHP on a basis of one^perp and determine whether it is strictly positive or has a null sector.",
            "If a null sector exists, compute P(K-n^{-1}Hee^*H)P on that sector.",
            "Report a lower bound, negative diagnostic vector, or degeneracy certificate.",
            "Update the abstract/introduction only if this produces a genuine finite application result.",
        ]
    if "Endpoint color" in title:
        return [
            "Define the endpoint source partition function or finite group integral Z_v in the chosen regulator.",
            "Derive the fourth-source prefactor from the Wilson/path-ordered expansion.",
            "Track representation normalization, trace convention, plaquette-sheet orientation, and heat-kernel or Wilson-action parameter.",
            "State C_col^(G,R,reg) with all dependencies visible.",
            "Mark endpoint algebra as conditional until this prefactor is inserted into the same-theory calculation.",
        ]
    if "Uniform endpoint" in title:
        return [
            "Define r_{a,eps}, E_tail, source domain, and limit regime before bounding them.",
            "State the fourth- or sixth-derivative source estimates used for endpoint cumulant stencils.",
            "Give constants uniform in the variables required by the chosen finite Wilson block.",
            "Prove rho(a,eps)=o(eps^2) or state the exact replacement bound if the regime differs.",
            "State how the bound enters the finite margin or obstruction inequality.",
        ]
    if "Prior-art" in title:
        return [
            "List prior-art families: Schur complements, Feshbach maps, lattice reflection positivity, Wilson-loop renormalization, heat-kernel actions, constructive gauge theory.",
            "For each family, state what is standard and what the present paper packages differently.",
            "Separate the finite theorem novelty from any Wilson-block coefficient novelty.",
            "Rewrite abstract/introduction novelty language to cite only discharged results.",
            "Quarantine unsupported novelty claims into future work or remove them.",
        ]
    if "Three-hairpin" in title:
        return [
            "Specify the three hairpin paths combinatorially or with a figure-ready incidence description.",
            "Build the pair-indexed coefficient table with one-body, mixed boundary, endpoint, and remainder columns.",
            "Mark which entries vanish by zero-sum cancellation and which survive in PHP.",
            "Compute which entries survive only through the Schur-corrected second-order form.",
            "Attach the table to the nontrivial finite outcome or demote the section to an application template.",
        ]
    return [
        "Restate the marker as a replacement theorem, computation, or explanatory insertion.",
        "Name the missing inputs and proof obligations.",
        "Produce final manuscript text or quarantine the marker.",
    ]


def narrative_consequence(work_class: str, title: str) -> str:
    if "Nontrivial" in title or "Three-hairpin" in title:
        return "This is the manuscript's result-bearing upgrade from finite theorem note to worked Wilson-block application."
    if "Same-theory" in title:
        return "This protects the explanatory narrative from implying that entrywise normalization automatically preserves OS positivity."
    if "Boundary-OPE" in title:
        return "This supplies the bridge from abstract H,K theorem to actual Wilson coefficient data."
    if "Endpoint" in title:
        return "This determines whether conditional endpoint algebra can be promoted from placeholder to controlled application material."
    if "Prior-art" in title:
        return "This makes the contribution claim legible and defensible to readers familiar with Schur complements, Feshbach maps, and lattice OS positivity."
    return "This clarifies how the expansion changes the paper body, appendix, or claim boundary."


def parse_draft(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    title = clean_tex(TITLE_RE.search(text).group(1)) if TITLE_RE.search(text) else path.stem
    abstract = clean_tex(ABSTRACT_RE.search(text).group(1)) if ABSTRACT_RE.search(text) else ""
    sections = [
        {"level": m.group(1), "title": clean_tex(m.group(2)), "offset": m.start()}
        for m in SECTION_RE.finditer(text)
    ]
    slots = []
    for index, match in enumerate(SLOT_RE.finditer(text), start=1):
        slot_title = clean_tex(match.group(1))
        body = match.group(2)
        labels = LABEL_RE.findall(body)
        label = labels[0] if labels else f"slot:auto:{index}"
        work_class = work_class_for(slot_title)
        slots.append(
            {
                "slot_id": f"slot-{index:02d}",
                "title": slot_title,
                "label": label,
                "section": current_section(sections, match.start()),
                "source_excerpt": clean_tex(body)[:1200],
                "work_class": work_class,
                "priority": priority_for(work_class, slot_title),
                "required_inputs": required_inputs(work_class, slot_title),
                "expected_artifact": expected_artifact(work_class, slot_title),
                "acceptance_criterion": acceptance_criterion(work_class, slot_title),
                "stop_condition": stop_condition(work_class, slot_title),
                "narrative_consequence": narrative_consequence(work_class, slot_title),
                "recommended_skills": SKILL_BY_WORK_CLASS.get(work_class, ["results-extension-strategy-planner"]),
            }
        )
    markers = []
    for match in TODO_RE.finditer(text):
        start = max(0, match.start() - 220)
        end = min(len(text), match.end() + 320)
        markers.append(
            {
                "marker": match.group(0),
                "section": current_section(sections, match.start()),
                "offset": match.start(),
                "excerpt": clean_tex(text[start:end]),
            }
        )
    labels = LABEL_RE.findall(text)
    duplicates = sorted({label for label in labels if labels.count(label) > 1})
    refs = REF_RE.findall(text)
    missing_refs = sorted(set(refs) - set(labels))
    return {
        "source_path": str(path),
        "source_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
        "title": title,
        "abstract": abstract,
        "sections": sections,
        "slots": slots,
        "markers": markers[:120],
        "label_audit": {
            "label_count": len(labels),
            "duplicate_labels": duplicates,
            "missing_refs": missing_refs,
        },
    }


def build_todos(parsed: dict[str, Any]) -> list[dict[str, Any]]:
    todos = []
    for order, slot in enumerate(sorted(parsed["slots"], key=lambda item: (-item["priority"], item["slot_id"])), start=1):
        todos.append(
            {
                "todo_id": f"todo-{order:03d}",
                "source_marker": slot["label"],
                "source_title": slot["title"],
                "target_section": slot["section"],
                "work_class": slot["work_class"],
                "priority": slot["priority"],
                "depends_on": dependency_labels(slot),
                "mathematical_object": infer_mathematical_object(slot),
                "required_inputs": slot["required_inputs"],
                "subtasks": subtasks_for(slot),
                "action": action_for(slot),
                "expected_artifact": slot["expected_artifact"],
                "acceptance_criterion": slot["acceptance_criterion"],
                "limitation_addressed": limitation_addressed(slot),
                "paper_insertion_target": paper_insertion_target(slot),
                "validation_handoff": validation_for(slot),
                "stop_or_quarantine_condition": slot["stop_condition"],
                "recommended_skills": slot["recommended_skills"],
                "narrative_consequence": slot["narrative_consequence"],
            }
        )
    if parsed["label_audit"]["duplicate_labels"]:
        todos.append(
            {
                "todo_id": f"todo-{len(todos)+1:03d}",
                "source_marker": "label-audit",
                "source_title": "Duplicate label cleanup",
                "target_section": "whole draft",
                "work_class": "submission_cleanup",
                "priority": 72,
                "depends_on": [],
                "mathematical_object": "TeX cross-reference integrity",
                "required_inputs": parsed["label_audit"]["duplicate_labels"],
                "subtasks": [
                    "Locate every duplicate label occurrence.",
                    "Rename or remove duplicates according to the equation/proposition they actually reference.",
                    "Recompile or run a reference audit.",
                ],
                "action": "Remove or rename duplicate labels before final TeX validation.",
                "expected_artifact": "A compile-clean TeX draft with unique labels.",
                "acceptance_criterion": "No duplicate labels remain and all refs resolve.",
                "limitation_addressed": "Duplicate labels make the expansion paper unreliable because equations and propositions cannot be cited unambiguously.",
                "paper_insertion_target": "Apply directly to the TeX source before manuscript-level expansion editing.",
                "validation_handoff": "Run a TeX compile or label audit.",
                "stop_or_quarantine_condition": "Do not submit or circulate as final while duplicate labels remain.",
                "recommended_skills": ["results-expansion-validator"],
                "narrative_consequence": "Cross-reference clarity protects the reader's ability to follow the endpoint-cumulant extension.",
            }
        )
    return todos


def infer_mathematical_object(slot: dict[str, Any]) -> str:
    title = slot["title"].lower()
    if "quotient" in title:
        return "normalized reflected Wilson Gram block q and its same-theory positivity-preserving realization"
    if "boundary-ope" in title:
        return "coefficient matrices H_a and K_a in the rank-one Wilson block expansion"
    if "nontrivial" in title:
        return "finite Schur-Feshbach reduced forms PHP and P(K-n^{-1}Hee^*H)P"
    if "endpoint color" in title:
        return "endpoint color/combinatorial prefactor C_col^(G,R,reg)"
    if "uniform endpoint" in title:
        return "endpoint remainder r_{a,eps}, tail term E_tail, and uniform source-derivative bounds"
    if "three-hairpin" in title:
        return "three-hairpin reflected Wilson coefficient table and null-sector scalar"
    if "prior-art" in title:
        return "novelty boundary of the finite Schur-Feshbach Wilson/OS packaging"
    return "regulated Wilson observable family and finite reflected Gram matrix"


def action_for(slot: dict[str, Any]) -> str:
    work_class = slot["work_class"]
    if work_class == "same_theory_transfer":
        return "Prove or falsify the same-theory transfer certificate for the normalization used in the draft."
    if work_class == "coefficient_extraction":
        return "Derive the requested coefficient, prefactor, incidence, or uniform remainder in the named regulator and expose all validity conditions."
    if work_class == "finite_application":
        return "Compute the finite Schur-Feshbach test for the concrete block and report margin, null-sector result, obstruction vector, or degeneracy."
    if work_class == "prior_art_boundary":
        return "Compare the claimed contribution against named prior-art families and rewrite novelty language accordingly."
    return "Replace the slot with a theorem/proposition/lemma package including definitions, assumptions, proof route, and non-claims."


def validation_for(slot: dict[str, Any]) -> str:
    work_class = slot["work_class"]
    if work_class == "finite_application":
        return "Run an independent finite-matrix/sign check and `results-expansion-validator`."
    if work_class == "coefficient_extraction":
        return "Run symbolic/numeric reproducibility check where applicable and `results-expansion-validator`."
    if work_class == "same_theory_transfer":
        return "Run a positivity-preservation audit with `bridge-object-equivalence-checker` and `results-expansion-validator`."
    if work_class == "prior_art_boundary":
        return "Run prior-art source check and claim-boundary audit."
    return "Run proof-gap review and `results-expansion-validator`."


def build_report(parsed: dict[str, Any]) -> dict[str, Any]:
    todos = build_todos(parsed)
    return {
        "schema": "abducer.results_elaboration.v1",
        "context": {
            "source_path": parsed["source_path"],
            "source_sha256": parsed["source_sha256"],
            "title": parsed["title"],
            "bounded_contribution": "Finite Schur-Feshbach consistency test for normalized reflected Wilson Gram blocks near a rank-one collision limit.",
            "explicit_non_claims": [
                "does not construct four-dimensional Yang-Mills theory",
                "does not prove OS reconstruction for a continuum gauge field",
                "does not prove a mass gap",
            ],
            "abstract": parsed["abstract"],
        },
        "source_structure": {
            "section_count": len(parsed["sections"]),
            "sections": parsed["sections"],
            "slot_count": len(parsed["slots"]),
            "slots": parsed["slots"],
            "marker_count": len(parsed["markers"]),
            "markers": parsed["markers"],
            "label_audit": parsed["label_audit"],
        },
        "workflow": {
            "folder": "skills/results_ellaboration",
            "independent_from_discovery": True,
            "local_hooks": [
                "pre_context_interpretation",
                "post_context_interpretation",
                "post_need_extraction",
                "pre_strategy_planning",
                "post_strategy_planning",
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
            "skill_sequence": [
                "results-context-interpreter",
                "results-extension-need-extractor",
                "results-extension-strategy-planner",
                "results-narrative-integrator",
                "results-expansion-validator",
            ],
        },
        "todos": todos,
        "todo_review": {
            "limitations_found": [
                "Class-level acceptance criteria can hide the exact mathematical gate for a slot.",
                "Generic stop conditions can permit endless narrative elaboration without a theorem, coefficient, sign test, or citation boundary.",
                "Narrative consequences are useful only if they state where the manuscript changes after the result is discharged.",
            ],
            "repairs_applied": [
                "Each TODO now carries a slot-specific limitation addressed.",
                "Each TODO now names the paper insertion target where the expansion should land.",
                "Acceptance and stop criteria were specialized for regulator data, same-theory normalization, H,K extraction, endpoint constants, uniform tails, finite outcomes, prior art, and the three-hairpin table.",
            ],
        },
        "narrative_integration": {
            "spine": [
                "Finite theorem and proof are the stable core.",
                "Wilson application remains conditional until regulator, observables, same-theory quotient, H,K extraction, and uniform remainders are supplied.",
                "Three-hairpin block is the preferred first result-bearing expansion because it can turn the theorem into a worked finite application.",
                "Endpoint cumulant algebra belongs as conditional scaffolding until color factors and tail estimates are derived in the same regulator.",
            ],
            "paper_updates_after_discharge": [
                "Update abstract only when a slot is replaced by a proved theorem or reproducible calculation.",
                "Update introduction to distinguish finite theorem, worked Wilson application, and remaining continuum obligations.",
                "Move author-facing checklist material out of final body after TODOs are discharged or quarantined.",
                "Keep the discussion explicit about non-claims unless all continuum obligations are proved.",
            ],
        },
    }


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Results Elaboration Plan",
        "",
        f"- Source: `{report['context']['source_path']}`",
        f"- Title: {report['context']['title']}",
        f"- Slots: {report['source_structure']['slot_count']}",
        f"- Markers: {report['source_structure']['marker_count']}",
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
    lines += ["", "## Expansion Slots", ""]
    for slot in report["source_structure"]["slots"]:
        lines += [
            f"### {slot['title']}",
            "",
            f"- Label: `{slot['label']}`",
            f"- Section: {slot['section']}",
            f"- Work class: `{slot['work_class']}`",
            f"- Priority: {slot['priority']}",
            f"- Expected artifact: {slot['expected_artifact']}",
            f"- Acceptance criterion: {slot['acceptance_criterion']}",
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
            *[f"  - {step}" for step in todo.get("subtasks", [])],
            f"- Action: {todo['action']}",
            f"- Expected artifact: {todo['expected_artifact']}",
            f"- Acceptance criterion: {todo['acceptance_criterion']}",
            f"- Limitation addressed: {todo['limitation_addressed']}",
            f"- Paper insertion target: {todo['paper_insertion_target']}",
            f"- Validation handoff: {todo['validation_handoff']}",
            f"- Stop/quarantine condition: {todo['stop_or_quarantine_condition']}",
            f"- Skills: {', '.join(todo['recommended_skills'])}",
            f"- Narrative consequence: {todo['narrative_consequence']}",
            "",
        ]
    lines += [
        "## Local Workflow Hooks",
        "",
    ]
    for hook in report["workflow"]["local_hooks"]:
        lines.append(f"- `{hook}`")
    lines += [
        "",
        "Forbidden couplings:",
    ]
    for item in report["workflow"]["forbidden_couplings"]:
        lines.append(f"- {item}")
    lines += ["", "## TODO Review Repairs", ""]
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
    if report["source_structure"]["label_audit"]["duplicate_labels"]:
        lines += [
            "",
            "## TeX Label Audit",
            "",
            "Duplicate labels:",
        ]
        for label in report["source_structure"]["label_audit"]["duplicate_labels"]:
            lines.append(f"- `{label}`")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("draft", type=Path)
    parser.add_argument("--out-dir", type=Path)
    args = parser.parse_args()
    draft = args.draft.expanduser().resolve()
    if not draft.exists():
        raise SystemExit(f"missing draft: {draft}")
    parsed = parse_draft(draft)
    report = build_report(parsed)
    slug = slugify(draft.stem)
    out_dir = args.out_dir or OUT_ROOT / slug
    out_dir.mkdir(parents=True, exist_ok=True)
    json_path = out_dir / "latest.json"
    md_path = out_dir / "latest.md"
    json_path.write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")
    md_path.write_text(render_markdown(report), encoding="utf-8")
    print(f"Wrote {json_path.relative_to(ROOT)}")
    print(f"Wrote {md_path.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
