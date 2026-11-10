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
"""Validate the independent timeline-paper TeX/PDF workflow."""

from __future__ import annotations

from pathlib import Path

from agentic_common import clean_text, fail, load_json_object, rel, repo_path
from build_timeline_paper import LATEST_JSON, LATEST_STEP_COUNT, OUT_JSON, PAPER_SKILLS


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def artifact(report: dict, key: str) -> Path:
    raw = report.get("artifacts", {}).get(key)
    require(clean_text(raw), f"{rel(OUT_JSON)} missing artifact {key}")
    return repo_path(str(raw), must_exist=True)


def main() -> int:
    require(OUT_JSON.exists(), f"missing {rel(OUT_JSON)}")
    report = load_json_object(OUT_JSON)
    target_id = clean_text(report.get("target_id"))
    require(report.get("independent_workflow") is True, "timeline paper must be independent from main discovery loop")
    require(set(PAPER_SKILLS).issubset(set(report.get("invoked_skills", []))), "timeline paper missing required paper skills")
    if target_id == "p-vs-np-target":
        marathon = load_json_object(LATEST_JSON)
        latest_steps = report.get("latest_steps", {})
        latest_rows = latest_steps.get("cycles", []) if isinstance(latest_steps.get("cycles"), list) else []
        total_research_cycles = int(marathon.get("research_cycle_count", 0))
        expected_latest_count = min(LATEST_STEP_COUNT, total_research_cycles)
        expected_latest_ids = [
            f"cycle-{idx:04d}"
            for idx in range(total_research_cycles - expected_latest_count + 1, total_research_cycles + 1)
        ]
        require(latest_steps.get("requested_count") == LATEST_STEP_COUNT, f"P vs NP paper must request the latest {LATEST_STEP_COUNT} steps")
        require(latest_steps.get("cycle_count") == expected_latest_count, f"P vs NP paper must carry the latest {expected_latest_count} steps")
        require([clean_text(row.get("cycle_id")) for row in latest_rows] == expected_latest_ids, "P vs NP paper latest steps do not match the current marathon tail")
        interpretation = report.get("timeline_paper_interpretation", {})
        require(interpretation.get("status") == "timeline_paper_interpretation_ready", "P vs NP paper missing interpretation artifact")
        require(int(interpretation.get("unit_count", 0)) >= 40, "P vs NP paper interpretation must have substantive unit coverage")
        blueprint = report.get("timeline_paper_blueprint", {})
        require(blueprint.get("status") == "timeline_paper_blueprint_ready", "P vs NP paper missing ready blueprint")
        require("P != NP" in " ".join(blueprint.get("non_claims", [])), "P vs NP paper must explicitly avoid claiming P != NP")
        require("P vs NP" in clean_text(report.get("title")), "P vs NP paper title must name the target")
        sections_packet = report.get("timeline_paper_sections", {})
        require(sections_packet.get("status") == "timeline_paper_sections_ready", "P vs NP paper missing synthesized sections")
        formal_artifact = report.get("timeline_formal_derivation", {})
        require(formal_artifact.get("status") == "timeline_formal_derivation_ready", "P vs NP paper missing formal derivation")
        require(formal_artifact.get("target_family") == "pvsnp_transfer_obstruction", "P vs NP formal derivation has wrong target family")
        for field in ["definitions", "assumptions", "propositions", "unresolved_obligations"]:
            require(formal_artifact.get(field), f"P vs NP formal derivation missing {field}")
        latex_sections = report.get("timeline_latex_sections", {})
        require(latex_sections.get("status") == "timeline_latex_sections_ready", "P vs NP paper missing ready LaTeX section packet")
        require(latex_sections.get("target_id") == "p-vs-np-target", "LaTeX appendix packet target mismatch")
        contract = latex_sections.get("report_document_contract", {})
        labels = " ".join(clean_text(row.get("tab_label")) + " " + clean_text(row.get("section_title")) for row in contract.get("tab_sections", []) if isinstance(row, dict))
        require("Complexity Strategy" in labels and "Proof Strategy Story" in labels, "P vs NP appendix must use target-specific strategy/story labels")
        lock = report.get("paper_narrative_goal_lock", {})
        require("P vs NP" in clean_text(lock.get("subgoal_title")), "P vs NP narrative goal lock must name the target")
        require("transfer" in clean_text(lock.get("coherent_narrative_thesis")).lower(), "P vs NP narrative thesis must center transfer control")
        derivation = report.get("formal_derivation", {})
        require("transfer" in clean_text(derivation.get("object")).lower(), "P vs NP formal derivation summary must name transfer")
        proof_queue = report.get("proof_delivery_queue", {})
        require(proof_queue.get("status") == "pvsnp_proof_delivery_queue_ready", "P vs NP timeline paper missing proof-delivery queue status")
        require(clean_text(proof_queue.get("source_artifact")), "P vs NP timeline paper missing proof-delivery queue source artifact")
        proof_objects = report.get("proof_objects", [])
        require(isinstance(proof_objects, list) and len(proof_objects) >= 4, "P vs NP timeline paper must carry proof objects from the queue")
        required_proof_ids = {
            "pvsnp.paper.l1201-least-closed-support-proof-audit",
            "pvsnp.paper.realsat-influence-realizer-boundary",
            "pvsnp.paper.l120-theorem-countermodel-package",
            "pvsnp.paper.l120-inference-quality-gate-closure",
        }
        present_proof_ids = {clean_text(row.get("proof_object_id")) for row in proof_objects if isinstance(row, dict)}
        missing_proof_ids = sorted(required_proof_ids - present_proof_ids)
        require(not missing_proof_ids, f"P vs NP timeline paper missing proof objects: {missing_proof_ids}")
        for row in proof_objects:
            if isinstance(row, dict):
                require(clean_text(row.get("theorem_goal")), f"P vs NP proof object {row.get('proof_object_id')} missing theorem goal")
                require(clean_text(row.get("source_object")), f"P vs NP proof object {row.get('proof_object_id')} missing source object")
                require(clean_text(row.get("target_object")), f"P vs NP proof object {row.get('proof_object_id')} missing target object")
                require(row.get("proof_outputs"), f"P vs NP proof object {row.get('proof_object_id')} missing proof outputs")
        refs = report.get("references", [])
        require(len(refs) >= 6, "P vs NP timeline paper needs literature and artifact references")
        require(any(row.get("kind") == "artifact" for row in refs), "P vs NP timeline paper needs artifact references")
        require(any(row.get("kind") == "literature" for row in refs), "P vs NP timeline paper needs literature references")
        tex_path = artifact(report, "tex")
        pdf_path = artifact(report, "pdf")
        md_path = artifact(report, "markdown")
        require(pdf_path.stat().st_size > 1000, f"{rel(pdf_path)} is too small to be a rendered PDF")
        tex = tex_path.read_text(encoding="utf-8")
        md = md_path.read_text(encoding="utf-8")
        for phrase in [
            "Formal Complexity Derivation",
            "Bounded-window transfer obstruction",
            "All-exponent lift gate",
            "Searchable certificate gate",
            "Complexity Strategy",
            "Accumulated Proof Strategy Story",
            "P vs NP",
            "SAT",
            "P/poly",
            "thebibliography",
        ]:
            require(phrase in tex, f"{rel(tex_path)} missing P vs NP phrase `{phrase}`")
        for phrase in [
            "Timeline Proof Objects",
            f"Latest {LATEST_STEP_COUNT} Timeline Steps",
            "LeastClosedTransparentSupport",
            "RealSATInfluenceRealizer",
            "proof-delivery queue",
        ]:
            require(phrase in tex, f"{rel(tex_path)} missing proof-object phrase `{phrase}`")
        for cycle_id in expected_latest_ids:
            require(cycle_id in tex, f"{rel(tex_path)} missing latest-step cycle `{cycle_id}`")
        for phrase in ["The paper does not prove P != NP", "route-level transfer obstruction", "prior-art boundary"]:
            require(phrase in tex, f"{rel(tex_path)} missing non-claim/boundary phrase `{phrase}`")
        forbidden = ["Yang-Mills", "mass gap", "Wilson", "Schwinger", "Wightman", "gauge-invariant", "hairpin", "collar", "Formal Physics"]
        for term in forbidden:
            require(term not in tex, f"{rel(tex_path)} contains cross-target term `{term}`")
        for bad in ["<span", "</span>", "Misplaced &", "Missing argument", "Missing superscript", r"\textbackslash{}mathrm", r"\textbackslash{}mathbb"]:
            require(bad not in tex, f"{rel(tex_path)} contains LaTeX/rendering error marker `{bad}`")
        for phrase in ["Timeline Paper Draft", "Paper Narrative Goal Lock", "Validation Handoff"]:
            require(phrase in md, f"{rel(md_path)} missing `{phrase}`")
        require("Timeline Proof Objects" in md, f"{rel(md_path)} missing proof-object markdown section")
        require(f"Latest {LATEST_STEP_COUNT} Timeline Steps" in md, f"{rel(md_path)} missing latest-step markdown section")
        require(clean_text(report.get("epistemic_status")) == "paper_draft_validation_needed", "P vs NP paper status must remain validation-needed")
        require(report.get("compile", {}).get("engine"), "P vs NP timeline paper missing compile engine info")
        print(f"validated P vs NP timeline paper: {rel(pdf_path)}")
        return 0
    if target_id != "yang-mills-existence-and-mass-gap-target":
        print(f"validated generic timeline paper shell for target {target_id}")
        return 0
    require(len(report.get("source_artifacts", [])) >= 7, "timeline paper needs source artifacts")
    interpretation = report.get("timeline_paper_interpretation", {})
    require(interpretation.get("status") == "timeline_paper_interpretation_ready", "timeline paper missing interpretation artifact")
    require(int(interpretation.get("unit_count", 0)) >= 40, "timeline paper interpretation must have substantive unit coverage")
    functions = interpretation.get("required_argument_functions", {})
    for field in ["has_active_object", "has_contribution_candidate", "has_formal_derivation_material", "has_validation_boundary"]:
        require(functions.get(field) is True, f"timeline paper interpretation missing required function {field}")
    coverage = interpretation.get("report_family_coverage", {}).get("families", {})
    require(len(coverage) >= 12, "timeline paper must record report-family coverage")
    for family, row in coverage.items():
        if row.get("present"):
            require(row.get("unit_count", 0) > 0, f"report family {family} was present but unused")
    blueprint = report.get("timeline_paper_blueprint", {})
    require(blueprint.get("status") == "timeline_paper_blueprint_ready", "timeline paper missing ready blueprint")
    require(blueprint.get("paper_mode") in {"theorem_note", "worked_calculation_note", "obstruction_note", "method_note", "negative_result_note", "survey_positioning_note"}, "invalid paper mode")
    require(blueprint.get("contribution_claims"), "blueprint needs contribution claims")
    require(blueprint.get("sections"), "blueprint needs section responsibilities")
    require(blueprint.get("non_claims"), "blueprint needs non-claims")
    sections_packet = report.get("timeline_paper_sections", {})
    require(sections_packet.get("status") == "timeline_paper_sections_ready", "timeline paper missing synthesized sections")
    require(len(sections_packet.get("sections", [])) >= 6, "timeline paper needs synthesized main sections")
    recon = sections_packet.get("cross_section_reconciliation", {})
    require(recon.get("accepted_claims"), "timeline paper sections need accepted claims")
    formal_artifact = report.get("timeline_formal_derivation", {})
    require(formal_artifact.get("status") == "timeline_formal_derivation_ready", "timeline paper missing formal derivation artifact")
    for field in ["definitions", "assumptions", "propositions", "unresolved_obligations"]:
        require(formal_artifact.get(field), f"formal derivation artifact missing {field}")
    diagrams = report.get("timeline_paper_diagrams", {})
    require(diagrams.get("status") == "timeline_paper_diagrams_ready", "timeline paper missing diagram artifact")
    manifest = report.get("paper_build_manifest", {})
    require(manifest.get("validation_status") == "interpretive_artifacts_consumed", "paper build did not consume interpretive artifacts")
    latex_sections = report.get("timeline_latex_sections", {})
    require(latex_sections.get("status") == "timeline_latex_sections_ready", "timeline paper missing ready LaTeX section packet")
    require(len(latex_sections.get("sections", [])) == 12, "timeline paper must carry the report-shaped translated section set")
    expected_tab_sections = [
        ("overview", "Summary", "Summary"),
        ("physics_math_strategy", "Physics & Maths Strategy", "Physics And Maths Strategy"),
        ("timeline", "Timeline From cycle window", "Content-Specific Full Timeline"),
        ("ranked_queue", "Ranked Analyses", "Current Ranked Next-Analysis Queue"),
        ("qualitative", "Qualitative Graph", "Qualitative Mechanistic Graph"),
        ("gedanken", "Gedanken Experiments", "Gedanken Experiments"),
        ("parsimonious", "PMP Probes", "Parsimonious Probe Control"),
        ("contributions", "Contributions", "Scientific Contribution Monitor"),
        ("literature", "Problem & Literature", "Target Problem And Literature Evolution"),
        ("macro_strategy", "Macro Strategies", "Macro Strategies"),
        ("strategy_judge", "Strategy Judge", "Strategy Progression Judge"),
        ("story", "Physics Story", "Accumulated Physics Story"),
    ]
    contract = latex_sections.get("report_document_contract", {})
    require(contract.get("mapping_rule") == "each visible timeline report tab is translated into one LaTeX section in the same tab order", "timeline paper missing tab-to-section appendix contract")
    tab_sections = contract.get("tab_sections", [])
    require(isinstance(tab_sections, list) and len(tab_sections) == len(expected_tab_sections), "timeline paper appendix contract missing tab section list")
    require([row.get("tab_id") for row in tab_sections] == [row[0] for row in expected_tab_sections], "timeline paper appendix tab order mismatch")
    require(all(row.get("present") for row in tab_sections), "timeline paper appendix contract has missing tabs")
    latex_artifacts = latex_sections.get("artifacts", {})
    report_tex_artifact = clean_text(latex_artifacts.get("report_tex"))
    require(report_tex_artifact, "timeline paper missing standalone report TeX artifact")
    window = report.get("timeline_window", {})
    require(int(window.get("cycle_count", 0)) >= 8, "timeline paper needs a substantive timeline window")
    require(clean_text(window.get("start_cycle_id")) and clean_text(window.get("end_cycle_id")), "timeline paper needs window endpoints")
    require(len(report.get("contributions", [])) >= 3, "timeline paper needs at least three contribution statements")
    lock = report.get("paper_narrative_goal_lock", {})
    require(clean_text(lock.get("subgoal_title")), "timeline paper missing narrative goal lock subgoal")
    require("finite" in clean_text(lock.get("subgoal_title")).lower(), "narrative goal lock must keep a finite paper subgoal")
    require("coherent narrative" in clean_text(lock.get("coherent_narrative_thesis")).lower(), "narrative goal lock missing coherent narrative thesis")
    require("Do not add more timeline detail" in clean_text(lock.get("anti_infinite_exploration_rule")), "narrative goal lock missing anti-infinite exploration rule")
    require(len(lock.get("narrative_spine", [])) >= 6, "narrative goal lock needs a substantive narrative spine")
    require(len(lock.get("included_material_policy", [])) >= 4, "narrative goal lock needs inclusion policy")
    require(len(lock.get("excluded_detail_policy", [])) >= 4, "narrative goal lock needs exclusion/demotion policy")
    require(len(lock.get("stop_or_demote_when", [])) >= 3, "narrative goal lock needs stop or demote criteria")
    decisive_text = " ".join(lock.get("decisive_next_work", []))
    require("Schur-Feshbach" in decisive_text and "H and K" in decisive_text, "narrative goal lock missing decisive theorem/example work")
    judgement = report.get("strategy_judgement", {})
    for field in ["decision", "payoff_potential", "next_decisive_test", "when_to_stop", "alignment_class"]:
        require(clean_text(judgement.get(field)), f"strategy judgement missing {field}")
    derivation = report.get("formal_derivation", {})
    for field in ["object", "core_conditions", "local_result", "remaining_obligations"]:
        require(derivation.get(field), f"formal derivation missing {field}")
    refs = report.get("references", [])
    require(len(refs) >= 10, "timeline paper needs literature and artifact references")
    require(any(row.get("kind") == "artifact" for row in refs), "timeline paper needs artifact references")
    require(any(row.get("kind") == "literature" for row in refs), "timeline paper needs literature references")
    tex_path = artifact(report, "tex")
    pdf_path = artifact(report, "pdf")
    md_path = artifact(report, "markdown")
    if report_tex_artifact:
        require(repo_path(report_tex_artifact, must_exist=True).exists(), "standalone report TeX artifact missing")
    require(pdf_path.stat().st_size > 1000, f"{rel(pdf_path)} is too small to be a rendered PDF")
    tex = tex_path.read_text(encoding="utf-8")
    md = md_path.read_text(encoding="utf-8")
    for phrase in [
        "Paper Build Manifest",
        "Problem Pressure And Paper Claim",
        "Literature And Novelty Boundary",
        "Route Narrowing And Scientific Learning",
        "Formal Physics Derivation",
        "Worked Calculation And Falsifier Tests",
        "Mechanism And Organizing Diagram",
        "Claim Boundary And Validation Handoff",
        "Appendix Evidence Map",
        "Full Timeline Report Translation: Orientation",
        "Physics And Maths Strategy",
        "Content-Specific Full Timeline",
        "Qualitative Mechanistic Graph",
        "Target Problem And Literature Evolution",
        "Tab-to-section contract",
        "thebibliography",
    ]:
        require(phrase in tex, f"{rel(tex_path)} missing `{phrase}`")
    for _tab_id, tab_label, section_title in expected_tab_sections:
        latex_tab_label = tab_label.replace("&", r"\&")
        require(latex_tab_label in tex, f"{rel(tex_path)} missing appendix tab label `{tab_label}`")
        require(f"\\section{{{section_title}}}" in tex, f"{rel(tex_path)} missing appendix section `{section_title}`")
    require(tex.count("cycle-") >= 80, "paper TeX must preserve the translated timeline evidence in appendix material")
    for phrase in ["Timeline Paper Draft", "Invoked Skills", "Paper Narrative Goal Lock", "Validation Handoff"]:
        require(phrase in md, f"{rel(md_path)} missing `{phrase}`")
    require("proof of Yang--Mills" in tex or "does not claim" in tex, "paper must include proof-safety boundary")
    require(clean_text(report.get("epistemic_status")) == "paper_draft_validation_needed", "paper status must remain validation-needed")
    require(report.get("compile", {}).get("engine"), "timeline paper missing compile engine info")
    print(f"validated timeline paper: {rel(pdf_path)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
