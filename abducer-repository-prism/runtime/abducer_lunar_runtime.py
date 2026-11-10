"""Lunar hooks for all source-grounded Abducer PRISM workflows.

Preparation validates the exact closed contract and preserves the UI value. Execution
always traverses the packaged PRISM graph with the host reasoning callback. Verification
requires complete source occurrence coverage and renders runtime validity separately
from any scientific disposition contained in the generated result.
"""
from __future__ import annotations

import html
import hashlib
import json
from pathlib import Path
import re
from types import SimpleNamespace


def _encoded(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)


CONTRACTS = json.loads('{\n  "abducer_work_loop": {\n    "argument": "proof_gap",\n    "entry_file": "repository/projects/abducer_work_loop/prism_project/material_main.prism",\n    "expected_steps": [\n      "route_hypothesis",\n      "derived_claim",\n      "refutation_assessment",\n      "work_routing"\n    ],\n    "material_workflow": "MaterializedAbducerWorkLoop",\n    "provenance_contract": {\n      "agent_invocations": [\n        {\n          "activated_skill_ids": [\n            "kb-abduce"\n          ],\n          "agent_name": "route_hypothesis_material_agent",\n          "workflow_occurrence": "route_hypothesis"\n        },\n        {\n          "activated_skill_ids": [\n            "kb-deduce"\n          ],\n          "agent_name": "derived_claim_material_agent",\n          "workflow_occurrence": "derived_claim"\n        },\n        {\n          "activated_skill_ids": [\n            "counterexample-hunter"\n          ],\n          "agent_name": "refutation_assessment_material_agent",\n          "workflow_occurrence": "refutation_assessment"\n        },\n        {\n          "activated_skill_ids": [\n            "epistemic-status-ledger"\n          ],\n          "agent_name": "work_routing_material_agent",\n          "workflow_occurrence": "work_routing"\n        }\n      ],\n      "required_source_reads": []\n    },\n    "reasoning_workflow": "AbducerWorkLoop",\n    "schema": {\n      "additionalProperties": false,\n      "default": {\n        "obligation": "Identify a testable induction route for extending a common fixed point from n commuting affine maps to n+1 maps."\n      },\n      "properties": {\n        "obligation": {\n          "default": "Identify a testable induction route for extending a common fixed point from n commuting affine maps to n+1 maps.",\n          "maxLength": 16000,\n          "minLength": 1,\n          "type": "string"\n        }\n      },\n      "required": [\n        "obligation"\n      ],\n      "type": "object"\n    },\n    "variant_constraints": {\n      "disposition": [\n        "ReadyForReleasePromotion",\n        "Reframe",\n        "Retarget",\n        "Refuted"\n      ]\n    }\n  },\n  "cohere_fast": {\n    "argument": "domain_target",\n    "entry_file": "repository/projects/cohere_fast/prism_project/material_main.prism",\n    "expected_steps": [\n      "scope_activation",\n      "intake_disposition"\n    ],\n    "material_workflow": "MaterializedCohereFast",\n    "provenance_contract": {\n      "agent_invocations": [\n        {\n          "activated_skill_ids": [\n            "ym-run-clay-program"\n          ],\n          "agent_name": "scope_activation_material_agent",\n          "workflow_occurrence": "scope_activation"\n        },\n        {\n          "activated_skill_ids": [\n            "epistemic-status-ledger"\n          ],\n          "agent_name": "intake_disposition_material_agent",\n          "workflow_occurrence": "intake_disposition"\n        }\n      ],\n      "required_source_reads": []\n    },\n    "reasoning_workflow": "CohereFast",\n    "schema": {\n      "additionalProperties": false,\n      "default": {\n        "domain_id": "yang-mills",\n        "target_ref": "finite-regulator-to-continuum-mass-gap-route"\n      },\n      "properties": {\n        "domain_id": {\n          "default": "yang-mills",\n          "maxLength": 16000,\n          "minLength": 1,\n          "type": "string"\n        },\n        "target_ref": {\n          "default": "finite-regulator-to-continuum-mass-gap-route",\n          "maxLength": 16000,\n          "minLength": 1,\n          "type": "string"\n        }\n      },\n      "required": [\n        "domain_id",\n        "target_ref"\n      ],\n      "type": "object"\n    },\n    "variant_constraints": {\n      "__value__": [\n        "Ready",\n        "Blocked",\n        "Stalled"\n      ]\n    }\n  },\n  "cohere_fast_adaptive_frontier": {\n    "argument": "scope_grounding",\n    "entry_file": "repository/projects/cohere_fast_adaptive_frontier/prism_project/material_main.prism",\n    "expected_steps": [\n      "bounded_frontier",\n      "frontier_readiness"\n    ],\n    "material_workflow": "MaterializedCohereFastAdaptiveFrontier",\n    "provenance_contract": {\n      "agent_invocations": [\n        {\n          "activated_skill_ids": [\n            "ym-build-observable-core",\n            "ym-build-representation-calculus",\n            "ym-calibrate-restricted-models",\n            "ym-design-regulator-atlas"\n          ],\n          "agent_name": "bounded_frontier_material_agent",\n          "workflow_occurrence": "bounded_frontier"\n        },\n        {\n          "activated_skill_ids": [\n            "epistemic-status-ledger"\n          ],\n          "agent_name": "frontier_readiness_material_agent",\n          "workflow_occurrence": "frontier_readiness"\n        }\n      ],\n      "required_source_reads": []\n    },\n    "reasoning_workflow": "CohereFastAdaptiveFrontier",\n    "schema": {\n      "additionalProperties": false,\n      "default": {\n        "claim_ceiling": "conditional finite-regulator statements only",\n        "domain_id": "yang-mills",\n        "target_ref": "finite-regulator-frontier"\n      },\n      "properties": {\n        "claim_ceiling": {\n          "default": "conditional finite-regulator statements only",\n          "maxLength": 16000,\n          "minLength": 1,\n          "type": "string"\n        },\n        "domain_id": {\n          "default": "yang-mills",\n          "maxLength": 16000,\n          "minLength": 1,\n          "type": "string"\n        },\n        "target_ref": {\n          "default": "finite-regulator-frontier",\n          "maxLength": 16000,\n          "minLength": 1,\n          "type": "string"\n        }\n      },\n      "required": [\n        "domain_id",\n        "target_ref",\n        "claim_ceiling"\n      ],\n      "type": "object"\n    },\n    "variant_constraints": {\n      "__value__": [\n        "Accepted",\n        "Quarantined"\n      ]\n    }\n  },\n  "cohere_fast_derivation_and_proof": {\n    "argument": "bounded_frontier",\n    "entry_file": "repository/projects/cohere_fast_derivation_and_proof/prism_project/material_main.prism",\n    "expected_steps": [\n      "conditional_derivation",\n      "derivation_readiness"\n    ],\n    "material_workflow": "MaterializedCohereFastDerivationAndProof",\n    "provenance_contract": {\n      "agent_invocations": [\n        {\n          "activated_skill_ids": [\n            "ym-develop-paper-proofs",\n            "ym-draft-finite-block-certificate",\n            "ym-prove-state-weighted-defect-transfer",\n            "ym-reconstruct-os-gap"\n          ],\n          "agent_name": "conditional_derivation_material_agent",\n          "workflow_occurrence": "conditional_derivation"\n        },\n        {\n          "activated_skill_ids": [\n            "epistemic-status-ledger"\n          ],\n          "agent_name": "derivation_readiness_material_agent",\n          "workflow_occurrence": "derivation_readiness"\n        }\n      ],\n      "required_source_reads": []\n    },\n    "reasoning_workflow": "CohereFastDerivationAndProof",\n    "schema": {\n      "additionalProperties": false,\n      "default": {\n        "claim_ceiling": "conditional derivation with explicit open obligations",\n        "domain_id": "yang-mills",\n        "frontier_ref": "finite-regulator-frontier"\n      },\n      "properties": {\n        "claim_ceiling": {\n          "default": "conditional derivation with explicit open obligations",\n          "maxLength": 16000,\n          "minLength": 1,\n          "type": "string"\n        },\n        "domain_id": {\n          "default": "yang-mills",\n          "maxLength": 16000,\n          "minLength": 1,\n          "type": "string"\n        },\n        "frontier_ref": {\n          "default": "finite-regulator-frontier",\n          "maxLength": 16000,\n          "minLength": 1,\n          "type": "string"\n        }\n      },\n      "required": [\n        "domain_id",\n        "frontier_ref",\n        "claim_ceiling"\n      ],\n      "type": "object"\n    },\n    "variant_constraints": {\n      "__value__": [\n        "Accepted",\n        "Quarantined"\n      ]\n    }\n  },\n  "cohere_fast_independent_audit": {\n    "argument": "conditional_derivation",\n    "entry_file": "repository/projects/cohere_fast_independent_audit/prism_project/material_main.prism",\n    "expected_steps": [\n      "refutation_assessment",\n      "audit_disposition"\n    ],\n    "material_workflow": "MaterializedCohereFastIndependentAudit",\n    "provenance_contract": {\n      "agent_invocations": [\n        {\n          "activated_skill_ids": [\n            "counterexample-hunter"\n          ],\n          "agent_name": "refutation_assessment_material_agent",\n          "workflow_occurrence": "refutation_assessment"\n        },\n        {\n          "activated_skill_ids": [\n            "epistemic-status-ledger"\n          ],\n          "agent_name": "audit_disposition_material_agent",\n          "workflow_occurrence": "audit_disposition"\n        }\n      ],\n      "required_source_reads": []\n    },\n    "reasoning_workflow": "CohereFastIndependentAudit",\n    "schema": {\n      "additionalProperties": false,\n      "default": {\n        "claim_ceiling": "no continuum mass-gap claim without discharged obligations",\n        "derivation_ref": "conditional-finite-regulator-derivation",\n        "domain_id": "yang-mills",\n        "open_obligations_ref": "continuum-limit-and-uniformity-obligations"\n      },\n      "properties": {\n        "claim_ceiling": {\n          "default": "no continuum mass-gap claim without discharged obligations",\n          "maxLength": 16000,\n          "minLength": 1,\n          "type": "string"\n        },\n        "derivation_ref": {\n          "default": "conditional-finite-regulator-derivation",\n          "maxLength": 16000,\n          "minLength": 1,\n          "type": "string"\n        },\n        "domain_id": {\n          "default": "yang-mills",\n          "maxLength": 16000,\n          "minLength": 1,\n          "type": "string"\n        },\n        "open_obligations_ref": {\n          "default": "continuum-limit-and-uniformity-obligations",\n          "maxLength": 16000,\n          "minLength": 1,\n          "type": "string"\n        }\n      },\n      "required": [\n        "domain_id",\n        "derivation_ref",\n        "open_obligations_ref",\n        "claim_ceiling"\n      ],\n      "type": "object"\n    },\n    "variant_constraints": {\n      "__value__": [\n        "Accepted",\n        "Quarantined"\n      ]\n    }\n  },\n  "cohere_fast_manuscript_release": {\n    "argument": "independent_audit",\n    "entry_file": "repository/projects/cohere_fast_manuscript_release/prism_project/material_main.prism",\n    "expected_steps": [\n      "claim_bounded_presentation",\n      "release_disposition"\n    ],\n    "material_workflow": "MaterializedCohereFastManuscriptRelease",\n    "provenance_contract": {\n      "agent_invocations": [\n        {\n          "activated_skill_ids": [\n            "ym-build-latex-paper",\n            "ym-build-proof-appendix",\n            "ym-frame-paper-narrative"\n          ],\n          "agent_name": "claim_bounded_presentation_material_agent",\n          "workflow_occurrence": "claim_bounded_presentation"\n        },\n        {\n          "activated_skill_ids": [\n            "epistemic-status-ledger"\n          ],\n          "agent_name": "release_disposition_material_agent",\n          "workflow_occurrence": "release_disposition"\n        }\n      ],\n      "required_source_reads": []\n    },\n    "reasoning_workflow": "CohereFastManuscriptRelease",\n    "schema": {\n      "additionalProperties": false,\n      "default": {\n        "audit_ref": "independent-audit-finite-regulator-01",\n        "claim_ceiling": "claim-bounded presentation of conditional results",\n        "domain_id": "yang-mills"\n      },\n      "properties": {\n        "audit_ref": {\n          "default": "independent-audit-finite-regulator-01",\n          "maxLength": 16000,\n          "minLength": 1,\n          "type": "string"\n        },\n        "claim_ceiling": {\n          "default": "claim-bounded presentation of conditional results",\n          "maxLength": 16000,\n          "minLength": 1,\n          "type": "string"\n        },\n        "domain_id": {\n          "default": "yang-mills",\n          "maxLength": 16000,\n          "minLength": 1,\n          "type": "string"\n        }\n      },\n      "required": [\n        "domain_id",\n        "audit_ref",\n        "claim_ceiling"\n      ],\n      "type": "object"\n    },\n    "variant_constraints": {\n      "__value__": [\n        "Accepted",\n        "Stopped"\n      ]\n    }\n  },\n  "cohere_fast_scope_and_ground": {\n    "argument": "grounding_request",\n    "entry_file": "repository/projects/cohere_fast_scope_and_ground/prism_project/material_main.prism",\n    "expected_steps": [\n      "scope_grounding",\n      "grounding_disposition"\n    ],\n    "material_workflow": "MaterializedCohereFastScopeAndGround",\n    "provenance_contract": {\n      "agent_invocations": [\n        {\n          "activated_skill_ids": [\n            "ym-ground-paper-literature",\n            "ym-freeze-clay-target"\n          ],\n          "agent_name": "scope_grounding_material_agent",\n          "workflow_occurrence": "scope_grounding"\n        },\n        {\n          "activated_skill_ids": [\n            "epistemic-status-ledger"\n          ],\n          "agent_name": "grounding_disposition_material_agent",\n          "workflow_occurrence": "grounding_disposition"\n        }\n      ],\n      "required_source_reads": []\n    },\n    "reasoning_workflow": "CohereFastScopeAndGround",\n    "schema": {\n      "additionalProperties": false,\n      "default": {\n        "domain_id": "yang-mills",\n        "sources_ref": "KB/yang-mills-existence-and-mass-gap.kb.md",\n        "target_ref": "finite-regulator-to-continuum-mass-gap-route"\n      },\n      "properties": {\n        "domain_id": {\n          "default": "yang-mills",\n          "maxLength": 16000,\n          "minLength": 1,\n          "type": "string"\n        },\n        "sources_ref": {\n          "default": "KB/yang-mills-existence-and-mass-gap.kb.md",\n          "maxLength": 16000,\n          "minLength": 1,\n          "type": "string"\n        },\n        "target_ref": {\n          "default": "finite-regulator-to-continuum-mass-gap-route",\n          "maxLength": 16000,\n          "minLength": 1,\n          "type": "string"\n        }\n      },\n      "required": [\n        "domain_id",\n        "target_ref",\n        "sources_ref"\n      ],\n      "type": "object"\n    },\n    "variant_constraints": {\n      "__value__": [\n        "Accepted",\n        "Blocked"\n      ]\n    }\n  },\n  "conceptual_frontier_deepening": {\n    "argument": "context",\n    "entry_file": "repository/projects/conceptual_frontier_deepening/prism_project/material_main.prism",\n    "expected_steps": [\n      "conceptual_frontier",\n      "conceptual_hypothesis",\n      "refutation_assessment",\n      "hypothesis_selection",\n      "conceptual_bridge",\n      "formal_claim",\n      "calibrated_candidate"\n    ],\n    "material_workflow": "MaterializedConceptualFrontierDeepening",\n    "provenance_contract": {\n      "agent_invocations": [\n        {\n          "activated_skill_ids": [\n            "epistemic-status-ledger"\n          ],\n          "agent_name": "conceptual_frontier_material_agent",\n          "workflow_occurrence": "conceptual_frontier"\n        },\n        {\n          "activated_skill_ids": [\n            "kb-abduce"\n          ],\n          "agent_name": "conceptual_hypothesis_material_agent",\n          "workflow_occurrence": "conceptual_hypothesis"\n        },\n        {\n          "activated_skill_ids": [\n            "counterexample-hunter"\n          ],\n          "agent_name": "refutation_assessment_material_agent",\n          "workflow_occurrence": "refutation_assessment"\n        },\n        {\n          "activated_skill_ids": [\n            "epistemic-status-ledger"\n          ],\n          "agent_name": "hypothesis_selection_material_agent",\n          "workflow_occurrence": "hypothesis_selection"\n        },\n        {\n          "activated_skill_ids": [\n            "proof-bridge-object-forger"\n          ],\n          "agent_name": "conceptual_bridge_material_agent",\n          "workflow_occurrence": "conceptual_bridge"\n        },\n        {\n          "activated_skill_ids": [\n            "kb-deduce"\n          ],\n          "agent_name": "formal_claim_material_agent",\n          "workflow_occurrence": "formal_claim"\n        },\n        {\n          "activated_skill_ids": [\n            "epistemic-status-ledger"\n          ],\n          "agent_name": "calibrated_candidate_material_agent",\n          "workflow_occurrence": "calibrated_candidate"\n        }\n      ],\n      "required_source_reads": []\n    },\n    "reasoning_workflow": "ConceptualFrontierDeepening",\n    "schema": {\n      "additionalProperties": false,\n      "default": {\n        "frozen_context": "Work only with a finite commuting family first; distinguish compactness, convexity, affinity, and commutativity obligations."\n      },\n      "properties": {\n        "frozen_context": {\n          "default": "Work only with a finite commuting family first; distinguish compactness, convexity, affinity, and commutativity obligations.",\n          "maxLength": 16000,\n          "minLength": 1,\n          "type": "string"\n        }\n      },\n      "required": [\n        "frozen_context"\n      ],\n      "type": "object"\n    },\n    "variant_constraints": {\n      "disposition": [\n        "FormalReady",\n        "NotFormalReadyOrNonDominated",\n        "Refuted"\n      ]\n    }\n  },\n  "conceptual_hypothesis_exploration_loop": {\n    "argument": "failure_state",\n    "entry_file": "repository/projects/conceptual_hypothesis_exploration_loop/prism_project/material_main.prism",\n    "expected_steps": [\n      "obstruction_pressure",\n      "mediation_hypothesis",\n      "conceptual_bridge",\n      "bridge_consequence",\n      "refutation_assessment",\n      "refinement_routing"\n    ],\n    "material_workflow": "MaterializedConceptualHypothesisExplorationLoop",\n    "provenance_contract": {\n      "agent_invocations": [\n        {\n          "activated_skill_ids": [\n            "epistemic-status-ledger"\n          ],\n          "agent_name": "obstruction_pressure_material_agent",\n          "workflow_occurrence": "obstruction_pressure"\n        },\n        {\n          "activated_skill_ids": [\n            "kb-abduce"\n          ],\n          "agent_name": "mediation_hypothesis_material_agent",\n          "workflow_occurrence": "mediation_hypothesis"\n        },\n        {\n          "activated_skill_ids": [\n            "proof-bridge-object-forger"\n          ],\n          "agent_name": "conceptual_bridge_material_agent",\n          "workflow_occurrence": "conceptual_bridge"\n        },\n        {\n          "activated_skill_ids": [\n            "kb-deduce"\n          ],\n          "agent_name": "bridge_consequence_material_agent",\n          "workflow_occurrence": "bridge_consequence"\n        },\n        {\n          "activated_skill_ids": [\n            "counterexample-hunter"\n          ],\n          "agent_name": "refutation_assessment_material_agent",\n          "workflow_occurrence": "refutation_assessment"\n        },\n        {\n          "activated_skill_ids": [\n            "epistemic-status-ledger"\n          ],\n          "agent_name": "refinement_routing_material_agent",\n          "workflow_occurrence": "refinement_routing"\n        }\n      ],\n      "required_source_reads": []\n    },\n    "reasoning_workflow": "ConceptualHypothesisExplorationLoop",\n    "schema": {\n      "additionalProperties": false,\n      "default": {\n        "obstruction": "The current route does not justify why the fixed-point set of the first n maps is preserved by the remaining commuting map."\n      },\n      "properties": {\n        "obstruction": {\n          "default": "The current route does not justify why the fixed-point set of the first n maps is preserved by the remaining commuting map.",\n          "maxLength": 16000,\n          "minLength": 1,\n          "type": "string"\n        }\n      },\n      "required": [\n        "obstruction"\n      ],\n      "type": "object"\n    },\n    "variant_constraints": {\n      "disposition": [\n        "WorkReady",\n        "ReadyForReleasePromotion",\n        "Refuted"\n      ]\n    }\n  },\n  "deep_review_and_reorientation": {\n    "argument": "evidence",\n    "entry_file": "repository/projects/deep_review_and_reorientation/prism_project/material_main.prism",\n    "expected_steps": [\n      "review_state",\n      "defeater_assessment",\n      "repair_options",\n      "reorientation_decision"\n    ],\n    "material_workflow": "MaterializedDeepReviewAndReorientation",\n    "provenance_contract": {\n      "agent_invocations": [\n        {\n          "activated_skill_ids": [\n            "epistemic-status-ledger"\n          ],\n          "agent_name": "review_state_material_agent",\n          "workflow_occurrence": "review_state"\n        },\n        {\n          "activated_skill_ids": [\n            "counterexample-hunter"\n          ],\n          "agent_name": "defeater_assessment_material_agent",\n          "workflow_occurrence": "defeater_assessment"\n        },\n        {\n          "activated_skill_ids": [\n            "kb-abduce"\n          ],\n          "agent_name": "repair_options_material_agent",\n          "workflow_occurrence": "repair_options"\n        },\n        {\n          "activated_skill_ids": [\n            "epistemic-status-ledger"\n          ],\n          "agent_name": "reorientation_decision_material_agent",\n          "workflow_occurrence": "reorientation_decision"\n        }\n      ],\n      "required_source_reads": []\n    },\n    "reasoning_workflow": "DeepReviewAndReorientation",\n    "schema": {\n      "additionalProperties": false,\n      "default": {\n        "review_evidence_summary": "The finite-family induction route is plausible, but preservation of the intermediate fixed-point set and the infinite-family limit remain separate."\n      },\n      "properties": {\n        "review_evidence_summary": {\n          "default": "The finite-family induction route is plausible, but preservation of the intermediate fixed-point set and the infinite-family limit remain separate.",\n          "maxLength": 16000,\n          "minLength": 1,\n          "type": "string"\n        }\n      },\n      "required": [\n        "review_evidence_summary"\n      ],\n      "type": "object"\n    },\n    "variant_constraints": {\n      "disposition": [\n        "RepairWorkflowAssigned",\n        "ConceptualReorientationRequired",\n        "Stalled"\n      ]\n    }\n  },\n  "discovery_marathon_loop": {\n    "argument": "run_context",\n    "entry_file": "repository/projects/discovery_marathon_loop/prism_project/material_main.prism",\n    "expected_steps": [\n      "search_scope",\n      "discovery_hypothesis",\n      "discovery_pattern",\n      "model_implications",\n      "contrast_assessment",\n      "refutation_assessment",\n      "routing_assessment",\n      "typed_report"\n    ],\n    "material_workflow": "MaterializedDiscoveryMarathonLoop",\n    "provenance_contract": {\n      "agent_invocations": [\n        {\n          "activated_skill_ids": [\n            "epistemic-status-ledger"\n          ],\n          "agent_name": "search_scope_material_agent",\n          "workflow_occurrence": "search_scope"\n        },\n        {\n          "activated_skill_ids": [\n            "kb-abduce"\n          ],\n          "agent_name": "discovery_hypothesis_material_agent",\n          "workflow_occurrence": "discovery_hypothesis"\n        },\n        {\n          "activated_skill_ids": [\n            "kb-induce"\n          ],\n          "agent_name": "discovery_pattern_material_agent",\n          "workflow_occurrence": "discovery_pattern"\n        },\n        {\n          "activated_skill_ids": [\n            "dynamic-symbolic-simulation-experimenter"\n          ],\n          "agent_name": "model_implications_material_agent",\n          "workflow_occurrence": "model_implications"\n        },\n        {\n          "activated_skill_ids": [\n            "counterfactual-route-prober"\n          ],\n          "agent_name": "contrast_assessment_material_agent",\n          "workflow_occurrence": "contrast_assessment"\n        },\n        {\n          "activated_skill_ids": [\n            "counterexample-hunter"\n          ],\n          "agent_name": "refutation_assessment_material_agent",\n          "workflow_occurrence": "refutation_assessment"\n        },\n        {\n          "activated_skill_ids": [\n            "epistemic-status-ledger"\n          ],\n          "agent_name": "routing_assessment_material_agent",\n          "workflow_occurrence": "routing_assessment"\n        }\n      ],\n      "required_source_reads": []\n    },\n    "reasoning_workflow": "DiscoveryMarathonLoop",\n    "schema": {\n      "additionalProperties": false,\n      "default": {\n        "context_summary": "Compare fixed-point proof routes for a commuting finite family of affine self-maps on a compact convex set; retain every unproved premise."\n      },\n      "properties": {\n        "context_summary": {\n          "default": "Compare fixed-point proof routes for a commuting finite family of affine self-maps on a compact convex set; retain every unproved premise.",\n          "maxLength": 16000,\n          "minLength": 1,\n          "type": "string"\n        }\n      },\n      "required": [\n        "context_summary"\n      ],\n      "type": "object"\n    },\n    "variant_constraints": {\n      "disposition": [\n        "Promotable",\n        "Reorient",\n        "TargetReset",\n        "Stalled"\n      ]\n    }\n  },\n  "evidence_to_proof_route_onramp": {\n    "argument": "source",\n    "entry_file": "repository/projects/evidence_to_proof_route_onramp/prism_project/material_main.prism",\n    "expected_steps": [\n      "e0",\n      "a0",\n      "d0",\n      "e1",\n      "a1",\n      "r0",\n      "e2"\n    ],\n    "material_workflow": "MaterializedEvidenceToProofRouteOnramp",\n    "provenance_contract": {\n      "agent_invocations": [\n        {\n          "activated_skill_ids": [\n            "epistemic-status-ledger"\n          ],\n          "agent_name": "e0_material_agent",\n          "workflow_occurrence": "e0"\n        },\n        {\n          "activated_skill_ids": [\n            "kb-abduce"\n          ],\n          "agent_name": "a0_material_agent",\n          "workflow_occurrence": "a0"\n        },\n        {\n          "activated_skill_ids": [\n            "kb-deduce"\n          ],\n          "agent_name": "d0_material_agent",\n          "workflow_occurrence": "d0"\n        },\n        {\n          "activated_skill_ids": [\n            "epistemic-status-ledger"\n          ],\n          "agent_name": "e1_material_agent",\n          "workflow_occurrence": "e1"\n        },\n        {\n          "activated_skill_ids": [\n            "proof-bridge-object-forger"\n          ],\n          "agent_name": "a1_material_agent",\n          "workflow_occurrence": "a1"\n        },\n        {\n          "activated_skill_ids": [\n            "counterexample-hunter"\n          ],\n          "agent_name": "r0_material_agent",\n          "workflow_occurrence": "r0"\n        },\n        {\n          "activated_skill_ids": [\n            "epistemic-status-ledger"\n          ],\n          "agent_name": "e2_material_agent",\n          "workflow_occurrence": "e2"\n        }\n      ],\n      "required_source_reads": []\n    },\n    "reasoning_workflow": "EvidenceToProofRouteOnramp",\n    "schema": {\n      "additionalProperties": false,\n      "default": {\n        "source_id": "markov-kakutani-kb-route"\n      },\n      "properties": {\n        "source_id": {\n          "default": "markov-kakutani-kb-route",\n          "maxLength": 16000,\n          "minLength": 1,\n          "type": "string"\n        }\n      },\n      "required": [\n        "source_id"\n      ],\n      "type": "object"\n    },\n    "variant_constraints": {\n      "disposition": [\n        "RouteReady",\n        "RequiresConceptualRefinement",\n        "Refuted"\n      ]\n    }\n  },\n  "manuscript_result_elaboration": {\n    "argument": "paper",\n    "entry_file": "repository/projects/manuscript_result_elaboration/prism_project/material_main.prism",\n    "expected_steps": [\n      "e0",\n      "a0",\n      "r0",\n      "e1"\n    ],\n    "material_workflow": "MaterializedManuscriptResultElaboration",\n    "provenance_contract": {\n      "agent_invocations": [\n        {\n          "activated_skill_ids": [\n            "epistemic-status-ledger"\n          ],\n          "agent_name": "e0_material_agent",\n          "workflow_occurrence": "e0"\n        },\n        {\n          "activated_skill_ids": [\n            "kb-abduce"\n          ],\n          "agent_name": "a0_material_agent",\n          "workflow_occurrence": "a0"\n        },\n        {\n          "activated_skill_ids": [\n            "counterexample-hunter"\n          ],\n          "agent_name": "r0_material_agent",\n          "workflow_occurrence": "r0"\n        },\n        {\n          "activated_skill_ids": [\n            "epistemic-status-ledger"\n          ],\n          "agent_name": "e1_material_agent",\n          "workflow_occurrence": "e1"\n        }\n      ],\n      "required_source_reads": []\n    },\n    "reasoning_workflow": "ManuscriptResultElaboration",\n    "schema": {\n      "additionalProperties": false,\n      "default": {\n        "draft_id": "mk-fixed-point-method-note"\n      },\n      "properties": {\n        "draft_id": {\n          "default": "mk-fixed-point-method-note",\n          "maxLength": 16000,\n          "minLength": 1,\n          "type": "string"\n        }\n      },\n      "required": [\n        "draft_id"\n      ],\n      "type": "object"\n    },\n    "variant_constraints": {\n      "disposition": [\n        "ProofRequired",\n        "PaperReady",\n        "Stalled"\n      ]\n    }\n  },\n  "release_promotion_loop": {\n    "argument": "promotion_evidence",\n    "entry_file": "repository/projects/release_promotion_loop/prism_project/material_main.prism",\n    "expected_steps": [\n      "release_proposal",\n      "promotion_disposition"\n    ],\n    "material_workflow": "MaterializedReleasePromotionLoop",\n    "provenance_contract": {\n      "agent_invocations": [\n        {\n          "activated_skill_ids": [\n            "looper-release-promoter"\n          ],\n          "agent_name": "release_proposal_material_agent",\n          "workflow_occurrence": "release_proposal"\n        },\n        {\n          "activated_skill_ids": [\n            "epistemic-status-ledger"\n          ],\n          "agent_name": "promotion_disposition_material_agent",\n          "workflow_occurrence": "promotion_disposition"\n        }\n      ],\n      "required_source_reads": []\n    },\n    "reasoning_workflow": "ReleasePromotionLoop",\n    "schema": {\n      "additionalProperties": false,\n      "default": {\n        "evidence_ref": "KB/markov-kakutani-fixed-point-theorem.kb.md",\n        "run_id": "markov-kakutani-review-01"\n      },\n      "properties": {\n        "evidence_ref": {\n          "default": "KB/markov-kakutani-fixed-point-theorem.kb.md",\n          "maxLength": 16000,\n          "minLength": 1,\n          "type": "string"\n        },\n        "run_id": {\n          "default": "markov-kakutani-review-01",\n          "maxLength": 16000,\n          "minLength": 1,\n          "type": "string"\n        }\n      },\n      "required": [\n        "run_id",\n        "evidence_ref"\n      ],\n      "type": "object"\n    },\n    "variant_constraints": {\n      "__value__": [\n        "Promoted",\n        "RepairTarget",\n        "RepairConcept",\n        "Rejected"\n      ]\n    }\n  },\n  "scientific_contribution_cultivation": {\n    "argument": "result",\n    "entry_file": "repository/projects/scientific_contribution_cultivation/prism_project/material_main.prism",\n    "expected_steps": [\n      "a0",\n      "r0",\n      "e0"\n    ],\n    "material_workflow": "MaterializedScientificContributionCultivation",\n    "provenance_contract": {\n      "agent_invocations": [\n        {\n          "activated_skill_ids": [\n            "kb-abduce"\n          ],\n          "agent_name": "a0_material_agent",\n          "workflow_occurrence": "a0"\n        },\n        {\n          "activated_skill_ids": [\n            "counterexample-hunter"\n          ],\n          "agent_name": "r0_material_agent",\n          "workflow_occurrence": "r0"\n        },\n        {\n          "activated_skill_ids": [\n            "epistemic-status-ledger"\n          ],\n          "agent_name": "e0_material_agent",\n          "workflow_occurrence": "e0"\n        }\n      ],\n      "required_source_reads": []\n    },\n    "reasoning_workflow": "ScientificContributionCultivation",\n    "schema": {\n      "additionalProperties": false,\n      "default": {\n        "result_id": "mk-finite-family-proof-route"\n      },\n      "properties": {\n        "result_id": {\n          "default": "mk-finite-family-proof-route",\n          "maxLength": 16000,\n          "minLength": 1,\n          "type": "string"\n        }\n      },\n      "required": [\n        "result_id"\n      ],\n      "type": "object"\n    },\n    "variant_constraints": {\n      "disposition": [\n        "PaperReady",\n        "Refuted",\n        "Stalled"\n      ]\n    }\n  },\n  "target_navigation_loop": {\n    "argument": "unscoped_target",\n    "entry_file": "repository/projects/target_navigation_loop/prism_project/material_main.prism",\n    "expected_steps": [\n      "dependency_frontier",\n      "target_disposition"\n    ],\n    "material_workflow": "MaterializedTargetNavigationLoop",\n    "provenance_contract": {\n      "agent_invocations": [\n        {\n          "activated_skill_ids": [\n            "looper-target-dependency-cartographer"\n          ],\n          "agent_name": "dependency_frontier_material_agent",\n          "workflow_occurrence": "dependency_frontier"\n        },\n        {\n          "activated_skill_ids": [\n            "epistemic-status-ledger"\n          ],\n          "agent_name": "target_disposition_material_agent",\n          "workflow_occurrence": "target_disposition"\n        }\n      ],\n      "required_source_reads": []\n    },\n    "reasoning_workflow": "TargetNavigationLoop",\n    "schema": {\n      "additionalProperties": false,\n      "default": {\n        "target_id": "markov-kakutani-fixed-point-theorem"\n      },\n      "properties": {\n        "target_id": {\n          "default": "markov-kakutani-fixed-point-theorem",\n          "maxLength": 16000,\n          "minLength": 1,\n          "type": "string"\n        }\n      },\n      "required": [\n        "target_id"\n      ],\n      "type": "object"\n    },\n    "variant_constraints": {\n      "__value__": [\n        "WorkReady",\n        "ReadyForReleasePromotion",\n        "Stalled"\n      ]\n    }\n  },\n  "theorem_proof_delivery": {\n    "argument": "item",\n    "entry_file": "repository/projects/theorem_proof_delivery/prism_project/material_main.prism",\n    "expected_steps": [\n      "d0",\n      "r0",\n      "e0"\n    ],\n    "material_workflow": "MaterializedTheoremProofDelivery",\n    "provenance_contract": {\n      "agent_invocations": [\n        {\n          "activated_skill_ids": [\n            "kb-deduce"\n          ],\n          "agent_name": "d0_material_agent",\n          "workflow_occurrence": "d0"\n        },\n        {\n          "activated_skill_ids": [\n            "counterexample-hunter"\n          ],\n          "agent_name": "r0_material_agent",\n          "workflow_occurrence": "r0"\n        },\n        {\n          "activated_skill_ids": [\n            "epistemic-status-ledger"\n          ],\n          "agent_name": "e0_material_agent",\n          "workflow_occurrence": "e0"\n        }\n      ],\n      "required_source_reads": []\n    },\n    "reasoning_workflow": "TheoremProofDelivery",\n    "schema": {\n      "additionalProperties": false,\n      "default": {\n        "premises": {\n          "exact_statement": "A finite commuting family of continuous affine self-maps of a nonempty compact convex subset of a locally convex space has a common fixed point.",\n          "premise_set_id": "mk-standard-premises"\n        },\n        "queue_item_id": "mk-finite-family-induction"\n      },\n      "properties": {\n        "premises": {\n          "additionalProperties": false,\n          "default": {\n            "exact_statement": "A finite commuting family of continuous affine self-maps of a nonempty compact convex subset of a locally convex space has a common fixed point.",\n            "premise_set_id": "mk-standard-premises"\n          },\n          "properties": {\n            "exact_statement": {\n              "default": "A finite commuting family of continuous affine self-maps of a nonempty compact convex subset of a locally convex space has a common fixed point.",\n              "maxLength": 16000,\n              "minLength": 1,\n              "type": "string"\n            },\n            "premise_set_id": {\n              "default": "mk-standard-premises",\n              "maxLength": 16000,\n              "minLength": 1,\n              "type": "string"\n            }\n          },\n          "required": [\n            "premise_set_id",\n            "exact_statement"\n          ],\n          "type": "object"\n        },\n        "queue_item_id": {\n          "default": "mk-finite-family-induction",\n          "maxLength": 16000,\n          "minLength": 1,\n          "type": "string"\n        }\n      },\n      "required": [\n        "queue_item_id",\n        "premises"\n      ],\n      "type": "object"\n    },\n    "variant_constraints": {\n      "disposition": [\n        "ProofAccepted",\n        "FailureCertificateIssued",\n        "Quarantined"\n      ]\n    }\n  },\n  "timeline-paper-independent-workflow": {\n    "argument": "timeline_outputs",\n    "entry_file": "repository/projects/timeline-paper-independent-workflow/prism_project/material_main.prism",\n    "expected_steps": [\n      "bounded_claim_set",\n      "paper_disposition"\n    ],\n    "material_workflow": "MaterializedTimelinePaperIndependentWorkflow",\n    "provenance_contract": {\n      "agent_invocations": [\n        {\n          "activated_skill_ids": [\n            "timeline-paper-workflow-orchestrator"\n          ],\n          "agent_name": "bounded_claim_set_material_agent",\n          "workflow_occurrence": "bounded_claim_set"\n        },\n        {\n          "activated_skill_ids": [\n            "epistemic-status-ledger"\n          ],\n          "agent_name": "paper_disposition_material_agent",\n          "workflow_occurrence": "paper_disposition"\n        }\n      ],\n      "required_source_reads": []\n    },\n    "reasoning_workflow": "TimelinePaperIndependentWorkflow",\n    "schema": {\n      "additionalProperties": false,\n      "default": {\n        "timeline_ref": "mk-reasoning-timeline-01"\n      },\n      "properties": {\n        "timeline_ref": {\n          "default": "mk-reasoning-timeline-01",\n          "maxLength": 16000,\n          "minLength": 1,\n          "type": "string"\n        }\n      },\n      "required": [\n        "timeline_ref"\n      ],\n      "type": "object"\n    },\n    "variant_constraints": {\n      "__value__": [\n        "PaperReady",\n        "ClaimBoundaryFailure",\n        "Stalled"\n      ]\n    }\n  },\n  "ym-representational-dynamics-overlay": {\n    "argument": "yang_mills_target",\n    "entry_file": "repository/projects/ym-representational-dynamics-overlay/prism_project/material_main.prism",\n    "expected_steps": [\n      "continuum_audit_input",\n      "overlay_disposition"\n    ],\n    "material_workflow": "MaterializedYmRepresentationalDynamicsOverlay",\n    "provenance_contract": {\n      "agent_invocations": [\n        {\n          "activated_skill_ids": [\n            "ym-run-clay-program"\n          ],\n          "agent_name": "continuum_audit_input_material_agent",\n          "workflow_occurrence": "continuum_audit_input"\n        },\n        {\n          "activated_skill_ids": [\n            "epistemic-status-ledger"\n          ],\n          "agent_name": "overlay_disposition_material_agent",\n          "workflow_occurrence": "overlay_disposition"\n        }\n      ],\n      "required_source_reads": []\n    },\n    "reasoning_workflow": "YmRepresentationalDynamicsOverlay",\n    "schema": {\n      "additionalProperties": false,\n      "default": {\n        "continuum_boundary_ref": "KB/yang-mills-existence-and-mass-gap.kb.md",\n        "target_id": "yang-mills-existence-and-mass-gap"\n      },\n      "properties": {\n        "continuum_boundary_ref": {\n          "default": "KB/yang-mills-existence-and-mass-gap.kb.md",\n          "maxLength": 16000,\n          "minLength": 1,\n          "type": "string"\n        },\n        "target_id": {\n          "default": "yang-mills-existence-and-mass-gap",\n          "maxLength": 16000,\n          "minLength": 1,\n          "type": "string"\n        }\n      },\n      "required": [\n        "target_id",\n        "continuum_boundary_ref"\n      ],\n      "type": "object"\n    },\n    "variant_constraints": {\n      "__value__": [\n        "Accepted",\n        "Quarantined",\n        "Stalled"\n      ]\n    }\n  }\n}\n')

DISCOVERY_REPORT_SECTIONS = (
    ("overview", "Summary"),
    ("physics_math_strategy", "Mathematical Strategy"),
    ("timeline", "Timeline"),
    ("ranked_queue", "Ranked Analyses"),
    ("skills", "Skill Use"),
    ("contributions", "Contributions"),
    ("result_atlas", "Result Atlas"),
    ("literature", "Problem & Literature"),
    ("macro_strategy", "Macro Strategies"),
    ("strategy_judge", "Strategy Judge"),
    ("artifact_or_stop", "Artifact-Or-Stop"),
    ("story", "Story"),
    ("branches", "Branches"),
    ("reviews", "Deep Reviews"),
)

DISCOVERY_STEP_FIELDS = {
    "search_scope": "bounded_scope",
    "discovery_hypothesis": "hypothesis",
    "discovery_pattern": "provisional_pattern",
    "model_implications": "bounded_model_implications",
    "contrast_assessment": "controlled_contrast",
    "refutation_assessment": "scoped_refutation",
    "routing_assessment": "routing_basis",
    "typed_report": "prism.reporting.report.Report",
}

DISCOVERY_SKILL_BINDINGS = (
    ("search_scope", "epistemic-status-ledger"),
    ("discovery_hypothesis", "kb-abduce"),
    ("discovery_pattern", "kb-induce"),
    ("model_implications", "dynamic-symbolic-simulation-experimenter"),
    ("contrast_assessment", "counterfactual-route-prober"),
    ("refutation_assessment", "counterexample-hunter"),
    ("routing_assessment", "epistemic-status-ledger"),
)


def _contracts():
    return CONTRACTS


def _validate(value, schema, path="input"):
    kind = schema.get("type")
    if kind == "object":
        if not isinstance(value, dict):
            raise ValueError(path + " must be an object")
        expected = set(schema.get("properties", {}))
        if set(value) != expected:
            raise ValueError(path + " fields must be exactly: " + ", ".join(sorted(expected)))
        for name, child in schema.get("properties", {}).items():
            _validate(value[name], child, path + "." + name)
    elif kind == "string":
        if not isinstance(value, str) or not value.strip():
            raise ValueError(path + " must be a nonblank string")
        if len(value) > schema.get("maxLength", 16000):
            raise ValueError(path + " exceeds its maximum length")
        if "enum" in schema and value not in schema["enum"]:
            raise ValueError(path + " is outside the declared alternatives")
    elif kind == "array":
        if not isinstance(value, list) or len(value) < schema.get("minItems", 0):
            raise ValueError(path + " must be a nonempty array")
        for index, item in enumerate(value):
            _validate(item, schema["items"], path + "[" + str(index) + "]")
    elif kind == "integer":
        if not isinstance(value, int) or isinstance(value, bool):
            raise ValueError(path + " must be an integer")
    elif kind == "number":
        if not isinstance(value, (int, float)) or isinstance(value, bool):
            raise ValueError(path + " must be a number")
    elif kind == "boolean":
        if not isinstance(value, bool):
            raise ValueError(path + " must be a boolean")
    elif "anyOf" in schema:
        if value is None:
            return
        _validate(value, schema["anyOf"][1], path)
    else:
        raise ValueError(path + " uses an unsupported schema type")


def prepare(*, workflow_id, inputs, run_root, network_authority, **unused):
    """Validate one exact input record and retain a content-addressed run state."""
    contracts = _contracts()
    if workflow_id not in contracts:
        raise ValueError("Unknown Abducer workflow: " + workflow_id)
    if network_authority:
        raise ValueError("Abducer repository workflows do not request network authority")
    contract = contracts[workflow_id]
    _validate(inputs, contract["schema"])
    digest = hashlib.sha256(_encoded(inputs).encode("utf-8")).hexdigest()
    prepared = {
        "entry_argument_name": contract["argument"],
        "value": inputs,
        "request_digest": digest,
        "analysis_results": {
            "execution_scope": "source-grounded-model-reasoning",
            "scientific_truth_verified": False,
        },
    }
    return {
        "prepared_input": prepared,
        "state": {
            "workflow_id": workflow_id,
            "inputs": inputs,
            "prepared": prepared,
            "contract": contract,
            "run_root": str(run_root),
        },
        "events": [{"kind": "input", "payload": {
            "input_key": "inputs",
            "kind": "inline-json",
            "safe_locator": "run-input:" + workflow_id,
            "content_digest": "sha256:" + digest,
            "metadata": {"workflow_id": workflow_id, "status": "validated"},
        }}],
    }


def _plain_value(value):
    while hasattr(value, "value"):
        value = value.value
    if hasattr(value, "fields"):
        value = value.fields
    return json.loads(json.dumps(value, default=_encoded_result, ensure_ascii=False, allow_nan=False))


def _plain_result(execution):
    return _plain_value(execution.typed_result)


def _encoded_result(value):
    if hasattr(value, "fields"):
        if value.fields:
            return value.fields
        return value.type_name.rsplit(".", 1)[-1]
    if hasattr(value, "value"):
        return value.value
    raise TypeError("unsupported PRISM result value")


def _trace_step_results(execution, expected):
    """Recover each accepted occurrence output from the real PRISM trace."""
    results = {}
    for event in execution.trace:
        outcome = getattr(event, "outcome", None)
        name = getattr(event, "name", None)
        if (
            getattr(event, "kind", None) != "workflow-node"
            or name not in expected
            or outcome is None
            or outcome.execution != "completed"
            or outcome.contract != "satisfied"
        ):
            continue
        metadata = getattr(event, "metadata", {})
        if "result" not in metadata:
            raise ValueError("Completed reasoning occurrence omitted its typed result")
        value = _plain_value(metadata["result"])
        if name in results and results[name] != value:
            raise ValueError("A reasoning occurrence emitted conflicting typed results")
        results[name] = value
    if set(results) != set(expected):
        raise ValueError("Typed results are missing for a declared reasoning occurrence")
    return results


def _emit_agent_receipts(execution, contract, services):
    """Project native PRISM agent trace entries into Lunar worker stage receipts.

    Custom package hooks own this bridge.  Merely returning ``execution.trace`` from
    the hook does not persist it, so every expected invocation is checked against the
    native trace before a UI-visible receipt is emitted.
    """
    expected = contract["provenance_contract"]["agent_invocations"]
    agents = [event for event in execution.trace if event.kind == "agent-invoked"]
    effects = [event for event in execution.trace if event.kind == "effect"]
    if len(agents) != len(expected):
        raise ValueError("Native PRISM agent trace does not match the provenance contract")
    if len(effects) != len(agents):
        raise ValueError("Native PRISM agent trace has incomplete effect linkage")
    receipts = []
    for expected_row, agent, effect in zip(expected, agents, effects, strict=True):
        skills = list(agent.metadata.get("skills", ()))
        if agent.name != expected_row["agent_name"]:
            raise ValueError("Native PRISM agent trace changed invocation order or identity")
        if skills != expected_row["activated_skill_ids"]:
            raise ValueError("Native PRISM agent trace changed activated skill bindings")
        record_id = effect.metadata.get("record")
        record = execution.effect_records.get(record_id)
        if record is None:
            raise ValueError("Native PRISM agent trace references a missing effect record")
        detail = {
            "event_kind": "agent-invoked",
            "agent_name": agent.name,
            "workflow_occurrence": expected_row["workflow_occurrence"],
            "activated_skill_ids": skills,
            "selected_model": services.model.safe_snapshot,
            "effect_record_id": record_id,
            "input_digest": record.invocation.input_digest,
            "output_digest": record.observation.output_digest,
        }
        services.event("stage", {
            "stage_id": expected_row["workflow_occurrence"],
            "component_id": agent.name,
            "status": agent.status,
            "safe_summary": "Activated skills: " + ", ".join(skills),
            "detail": detail,
        })
        receipts.append(detail)
    return receipts


def execute(*, state, services):
    """Execute the complete PRISM graph and forward normalized reasoning events."""
    from prism_engine import execute_prism

    observed = []
    contract = state["contract"]
    expected_workflow = contract["reasoning_workflow"]
    material_workflow = contract["material_workflow"]

    def reasoning(**payload):
        step = payload.get("reasoning_step")
        if isinstance(step, dict) and step.get("workflow") in {
            material_workflow,
            "material_main." + material_workflow,
        }:
            payload = dict(payload)
            payload["reasoning_step"] = {**step, "workflow": expected_workflow}
        observed.append(payload)
        services.event("reasoning", payload)

    root = Path(state["run_root"])
    reasoning_root = root / "reasoning"
    reasoning_root.mkdir(exist_ok=False)
    prism_execution = execute_prism(
        source=Path("/package") / contract["entry_file"],
        entry_argument=contract["argument"],
        prepared_input=state["prepared"],
        selected_model=services.model,
        artifact_root=reasoning_root,
        completion=services.completion,
        on_reasoning=reasoning,
    )
    if prism_execution.status != "accepted" or prism_execution.diagnostics:
        raise ValueError("The complete Abducer PRISM graph did not finish cleanly")
    agent_receipts = _emit_agent_receipts(prism_execution, contract, services)
    transitions = {}
    for payload in observed:
        step = payload.get("reasoning_step")
        if not isinstance(step, dict) or step.get("workflow") != expected_workflow:
            continue
        name = step.get("name")
        status = payload.get("status")
        occurrence = str(payload.get("source_event_key", "")).rpartition(":")[0]
        if name and status in {"running", "completed"}:
            row = transitions.setdefault(occurrence, {"name": name, "statuses": []})
            if row["name"] != name:
                raise ValueError("A reasoning occurrence changed identity")
            row["statuses"].append(status)
    expected = contract["expected_steps"]
    if sorted(row["name"] for row in transitions.values()) != sorted(expected):
        raise ValueError("Reasoning completion is missing a declared source occurrence")
    if any(row["statuses"] != ["running", "completed"] for row in transitions.values()):
        raise ValueError("Reasoning occurrence transitions are incomplete")
    step_results = _trace_step_results(prism_execution, expected)
    # Discovery Marathon returns a genuine PRISM Report.  Its scientific routing
    # result remains the final reasoning occurrence, not the report container.
    result_value = (
        step_results["routing_assessment"]
        if state["workflow_id"] == "discovery_marathon_loop"
        else _plain_result(prism_execution)
    )
    for field, alternatives in contract.get("variant_constraints", {}).items():
        candidate = result_value if field == "__value__" else (
            result_value.get(field) if isinstance(result_value, dict) else None
        )
        if candidate not in alternatives:
            raise ValueError(
                "Generated result violates the closed source variant for "
                + ("value" if field == "__value__" else field)
            )
    return SimpleNamespace(
        prism_execution=prism_execution,
        reasoning_result=result_value,
        reasoning_event_count=len(observed),
        completed_steps=expected,
        transitions=transitions,
        step_results=step_results,
        agent_receipts=agent_receipts,
    )


def _markdown(workflow_id, value):
    final = value["final_disposition"]
    return (
        "# " + workflow_id.replace("_", " ").replace("-", " ").title() + "\n\n"
        "## Final disposition\n\n"
        "Runtime status: **" + final["status"] + "**\n\n"
        + final["summary"] + "\n\n"
        "## Completed reasoning steps\n\n"
        + "\n".join("- `" + step + "`" for step in final["completed_reasoning_steps"])
        + "\n\n## Typed reasoning result\n\n```json\n"
        + json.dumps(value["reasoning_result"], indent=2, ensure_ascii=False, allow_nan=False)
        + "\n```\n\n## Execution provenance\n\n```json\n"
        + json.dumps(value["execution_provenance"], indent=2, ensure_ascii=False, allow_nan=False)
        + "\n```\n\n## Interpretation and limits\n\n"
        + "\n".join("- " + item for item in final["limitations"])
        + "\n"
    )


def _digest_text(value):
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _quote(value):
    text = str(value).strip()
    return "\n".join("> " + line if line else ">" for line in text.splitlines())


def _step_text(step_results, step):
    value = step_results[step]
    field = DISCOVERY_STEP_FIELDS[step]
    if not isinstance(value, dict) or field not in value:
        raise ValueError("Discovery report input is missing " + step + "." + field)
    text = value[field]
    if not isinstance(text, str) or not text.strip():
        raise ValueError("Discovery report input contains an empty " + step + "." + field)
    return text.strip()


def _discovery_sections(state, execution, structured):
    """Map live typed results into the repository's fourteen report surfaces."""
    steps = execution.step_results
    context = state["inputs"]["context_summary"].strip()
    scope = _step_text(steps, "search_scope")
    hypothesis = _step_text(steps, "discovery_hypothesis")
    pattern = _step_text(steps, "discovery_pattern")
    implications = _step_text(steps, "model_implications")
    contrast = _step_text(steps, "contrast_assessment")
    refutation = _step_text(steps, "refutation_assessment")
    routing = _step_text(steps, "routing_assessment")
    disposition = structured["reasoning_result"]["disposition"]
    final = structured["final_disposition"]
    provenance = structured["execution_provenance"]
    completed = "\n".join("- `" + step + "`" for step in final["completed_reasoning_steps"])
    limits = "\n".join("- " + item for item in final["limitations"])
    step_rows = "\n".join(
        "| " + str(index) + " | `" + step + "` | completed | `" + DISCOVERY_STEP_FIELDS[step] + "` |"
        for index, step in enumerate(final["completed_reasoning_steps"], start=1)
    )
    skill_rows = "\n".join(
        "| `" + step + "` | `" + skill + "` | model-generated typed result |"
        for step, skill in DISCOVERY_SKILL_BINDINGS
    )
    atlas = json.dumps(steps, indent=2, ensure_ascii=False, allow_nan=False, sort_keys=True)
    typed = json.dumps(structured["reasoning_result"], indent=2, ensure_ascii=False, allow_nan=False, sort_keys=True)
    evidence = json.dumps(provenance, indent=2, ensure_ascii=False, allow_nan=False, sort_keys=True)
    artifact_action = {
        "Promotable": "Promote the candidate to source validation and proof-obligation discharge.",
        "Reorient": "Return the candidate to conceptual reorientation before promotion.",
        "TargetReset": "Reset the target boundary before another discovery cycle.",
        "Stalled": "Stop and record the unresolved blocker before spending another cycle.",
    }[disposition]
    bodies = {
        "overview": (
            "This report projects one complete live PRISM Discovery Marathon run into the "
            "same fourteen-section information architecture used by the repository report.\n\n"
            "### Run scope\n\n" + _quote(context) + "\n\n"
            "## Final disposition\n\nRuntime status: **" + final["status"] + "**  \n"
            "Discovery disposition: **" + disposition + "**\n\n" + final["summary"] + "\n\n"
            "## Completed reasoning steps\n\n" + completed + "\n\n"
            "## Typed reasoning result\n\n```json\n" + typed + "\n```\n\n"
            "## Execution provenance\n\n```json\n" + evidence + "\n```\n\n"
            "## Interpretation and limits\n\n" + limits
        ),
        "physics_math_strategy": (
            "### Bounded scope\n\n" + _quote(scope) + "\n\n"
            "### Candidate hypothesis\n\n" + _quote(hypothesis) + "\n\n"
            "### Provisional pattern\n\n" + _quote(pattern) + "\n\n"
            "### Bounded model implications\n\n" + _quote(implications)
        ),
        "timeline": (
            "The ordered runtime trace completed every declared reasoning occurrence. "
            "Parallel declarations retain their PRISM semantics; this table records their released order.\n\n"
            "| # | Reasoning stage | Runtime status | Typed evidence field |\n"
            "| ---: | --- | --- | --- |\n" + step_rows
        ),
        "ranked_queue": (
            "1. **Validate sources and exact theorem hypotheses.** " + routing + "\n"
            "2. **Discharge the strongest refutation pressure.** " + refutation + "\n"
            "3. **Test the controlled contrast.** " + contrast + "\n"
            "4. **Check the bounded implications.** " + implications
        ),
        "skills": (
            "These packaged skills were bound to the seven executed occurrences. Skill use "
            "supports generation and critique; it is not independent scientific verification.\n\n"
            "| Reasoning stage | Packaged skill | Evidence class |\n"
            "| --- | --- | --- |\n" + skill_rows
        ),
        "contributions": (
            "- Preserved the user-supplied problem boundary through all seven typed stages.\n"
            "- Produced separate abductive and inductive formation records.\n"
            "- Produced separate model-based and contrastive probes before refutation.\n"
            "- Retained a closed routing disposition with explicit limitations.\n"
            "- Scientific novelty remains **not claimed**; all substantive content is model-generated."
        ),
        "result_atlas": (
            "The atlas preserves the complete typed output of every reasoning occurrence.\n\n"
            "```json\n" + atlas + "\n```"
        ),
        "literature": (
            "### Problem statement\n\n" + _quote(context) + "\n\n"
            "### Literature status\n\n"
            "This workflow requested no public-network authority and performed no live literature "
            "acquisition. Any titles or references mentioned by model outputs are leads requiring "
            "source retrieval, identity checks, and exact-locator validation before use as evidence."
        ),
        "macro_strategy": (
            "### Formation route\n\n" + _quote(hypothesis) + "\n\n"
            "### Pattern route\n\n" + _quote(pattern) + "\n\n"
            "### Model-pressure route\n\n" + _quote(implications)
        ),
        "strategy_judge": (
            "### Controlled contrast\n\n" + _quote(contrast) + "\n\n"
            "### Refutation assessment\n\n" + _quote(refutation) + "\n\n"
            "### Routing judgment\n\n**" + disposition + "**\n\n" + _quote(routing)
        ),
        "artifact_or_stop": (
            "**Decision:** " + disposition + "\n\n" + artifact_action + "\n\n"
            "Released artifacts: `report.md`, `result.json`, `latest.md`, `latest.json`, "
            "`latest.html`, and `full_timeline.html`. A passed runtime is not a proof certificate."
        ),
        "story": (
            "The run began by bounding the search:\n\n" + _quote(scope) + "\n\n"
            "It then formed a hypothesis and a pattern:\n\n" + _quote(hypothesis) + "\n\n"
            + _quote(pattern) + "\n\n"
            "The two probe lanes supplied implications and contrast pressure, which were merged "
            "by the refutation stage before the final routing judgment:\n\n" + _quote(routing)
        ),
        "branches": (
            "### Formation branch · abductive\n\n" + _quote(hypothesis) + "\n\n"
            "### Formation branch · inductive\n\n" + _quote(pattern) + "\n\n"
            "### Probe branch · model implications\n\n" + _quote(implications) + "\n\n"
            "### Probe branch · controlled contrast\n\n" + _quote(contrast) + "\n\n"
            "### Merge · refutation\n\n" + _quote(refutation)
        ),
        "reviews": (
            "### Epistemology\n\nThe run separates generated hypotheses, probes, refutation, and routing. "
            "No generated statement is promoted to established fact by runtime success.\n\n"
            "### Mathematics\n\nThe mathematical content remains conditional until its hypotheses, proof steps, "
            "counterexamples, and cited sources are independently checked.\n\n"
            "### AI research\n\nThe seven typed calls completed under a closed schema. One successful run does not "
            "measure stability, calibration, or cross-model agreement.\n\n"
            "### Software engineering\n\nThe PRISM graph, ordered reasoning events, source/module hashes, report layout, and "
            "artifact digests are retained for replay and inspection."
        ),
    }
    return [(slug, label, bodies[slug]) for slug, label in DISCOVERY_REPORT_SECTIONS]


def _assemble_native_report(sections):
    chunks = []
    blocks = []
    groups = []
    cursor = 0

    def add(text, kind, group_keys):
        nonlocal cursor
        value = text.strip() + "\n\n"
        block = {
            "id": "block-" + str(len(blocks) + 1),
            "kind": kind,
            "start": cursor,
            "end": cursor + len(value),
            "group_keys": group_keys,
            "source_text_sha256": _digest_text(" ".join(value.split())),
        }
        if kind == "heading":
            block["heading_key"] = block["id"]
        blocks.append(block)
        chunks.append(value)
        cursor += len(value)

    add("# Discovery Marathon Report", "heading", [])
    add(
        "Live PRISM execution report with repository-compatible Discovery Marathon sections.",
        "prose",
        [],
    )
    for index, (slug, label, body) in enumerate(sections, start=1):
        key = "tab-" + slug
        groups.append({"key": key, "kind": "tab", "label": label})
        add("## " + label, "heading", [key])
        for paragraph in body.strip().split("\n\n"):
            kind = "heading" if re.fullmatch(r"#{1,6} .+", paragraph.strip()) else "prose"
            add(paragraph, kind, [key])
    markdown = "".join(chunks)
    layout = {
        "schema_version": "lunar.native-report/v1",
        "groups": groups,
        "blocks": blocks,
        "content_sha256": _digest_text(markdown),
    }
    layout["metadata_sha256"] = _digest_text(
        json.dumps(layout, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)
    )
    return markdown, layout


def _markdown_fragment_html(value):
    rendered = []
    for paragraph in value.strip().split("\n\n"):
        lines = paragraph.splitlines()
        if len(lines) == 1 and re.fullmatch(r"#{1,6} .+", lines[0]):
            marker, title = lines[0].split(" ", 1)
            level = min(6, len(marker) + 1)
            rendered.append("<h" + str(level) + ">" + html.escape(title) + "</h" + str(level) + ">")
        elif lines and lines[0].startswith("```") and lines[-1] == "```":
            rendered.append("<pre><code>" + html.escape("\n".join(lines[1:-1])) + "</code></pre>")
        elif lines and all(line.startswith("- ") for line in lines):
            rendered.append("<ul>" + "".join("<li>" + html.escape(line[2:]) + "</li>" for line in lines) + "</ul>")
        elif lines and all(re.match(r"^\d+\. ", line) for line in lines):
            rendered.append("<ol>" + "".join("<li>" + html.escape(line.split(". ", 1)[1]) + "</li>" for line in lines) + "</ol>")
        elif lines and all(line.startswith(">") for line in lines):
            rendered.append("<blockquote>" + "<br>".join(html.escape(line[1:].lstrip()) for line in lines) + "</blockquote>")
        elif lines and lines[0].startswith("|"):
            rendered.append("<pre class=\"table\">" + html.escape(paragraph) + "</pre>")
        else:
            rendered.append("<p>" + "<br>".join(html.escape(line) for line in lines) + "</p>")
    return "".join(rendered)


def _discovery_html(sections, active_slug):
    buttons = []
    panels = []
    for slug, label, body in sections:
        active = slug == active_slug
        buttons.append(
            '<button class="tab' + (" active" if active else "") + '" data-tab="'
            + slug + '" aria-selected="' + ("true" if active else "false") + '">'
            + html.escape(label) + "</button>"
        )
        panels.append(
            '<section class="panel' + (" active" if active else "") + '" data-panel="'
            + slug + '"><h2>' + html.escape(label) + "</h2>"
            + _markdown_fragment_html(body) + "</section>"
        )
    return (
        "<!doctype html><html lang=\"en\"><head><meta charset=\"utf-8\">"
        "<meta name=\"viewport\" content=\"width=device-width,initial-scale=1\">"
        "<title>Discovery Marathon Report</title><style>"
        ":root{color-scheme:light dark;font-family:Inter,system-ui,sans-serif}body{margin:0;background:#10141d;color:#edf2f7}"
        "header,main{max-width:1180px;margin:auto;padding:24px}nav{display:flex;gap:8px;overflow:auto;padding:0 24px 16px}"
        ".tab{border:1px solid #526071;background:#202938;color:inherit;border-radius:999px;padding:8px 13px;white-space:nowrap}"
        ".tab.active{background:#2563eb;border-color:#60a5fa}.panel{display:none;background:#171e2a;border:1px solid #384457;border-radius:14px;padding:22px}"
        ".panel.active{display:block}blockquote,pre{white-space:pre-wrap;background:#0d121a;border-left:3px solid #60a5fa;padding:12px;overflow:auto}"
        "h1,h2,h3{color:#f8fafc}p,li{line-height:1.55}.table{font-size:.9rem}</style></head><body>"
        "<header><h1>Discovery Marathon Report</h1><p>Live typed PRISM execution · repository-compatible report contract</p></header>"
        "<nav aria-label=\"Report sections\">" + "".join(buttons) + "</nav><main>" + "".join(panels) + "</main>"
        "<script>document.querySelectorAll('.tab').forEach(function(button){button.addEventListener('click',function(){"
        "document.querySelectorAll('.tab').forEach(function(item){item.classList.remove('active');item.setAttribute('aria-selected','false')});"
        "document.querySelectorAll('.panel').forEach(function(item){item.classList.remove('active')});button.classList.add('active');"
        "button.setAttribute('aria-selected','true');document.querySelector('[data-panel=\"'+button.dataset.tab+'\"]').classList.add('active')})});</script>"
        "</body></html>\n"
    )


def _validate_discovery_report(markdown, layout, latest_html, timeline_html):
    labels = [label for unused, label in DISCOVERY_REPORT_SECTIONS]
    if [group["label"] for group in layout["groups"]] != labels:
        raise ValueError("Discovery report layout omitted a required native section")
    if layout["content_sha256"] != _digest_text(markdown):
        raise ValueError("Discovery report layout content digest is invalid")
    metadata = {key: value for key, value in layout.items() if key != "metadata_sha256"}
    if layout["metadata_sha256"] != _digest_text(
        json.dumps(metadata, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)
    ):
        raise ValueError("Discovery report layout metadata digest is invalid")
    required = [
        "## " + label for label in labels
    ] + [
        "## Final disposition",
        "## Completed reasoning steps",
        "## Typed reasoning result",
        "## Execution provenance",
        "## Interpretation and limits",
    ]
    missing = [heading for heading in required if heading not in markdown]
    if missing:
        raise ValueError("Discovery report is missing required headings: " + ", ".join(missing))
    for document in (latest_html, timeline_html):
        if document.count('<button class="tab') != len(labels) or document.count('<section class="panel') != len(labels):
            raise ValueError("Discovery HTML report omitted a required tab or panel")


def _validate_typed_discovery_report(typed_report):
    """Require the PRISM Report value to carry the compatible fourteen-tab surface."""
    labels = [label for unused, label in DISCOVERY_REPORT_SECTIONS]
    if typed_report.get("version") != "1":
        raise ValueError("Discovery PRISM Report uses an unsupported codec version")
    report = typed_report.get("report")
    if not isinstance(report, dict) or report.get("id") != "discovery-marathon-report":
        raise ValueError("Discovery PRISM Report identity is invalid")
    sections = report.get("sections")
    if not isinstance(sections, list) or len(sections) != 1:
        raise ValueError("Discovery PRISM Report must contain one typed tab group")
    tab_group = sections[0]
    if tab_group.get("kind") != "tabs" or tab_group.get("id") != "discovery-sections":
        raise ValueError("Discovery PRISM Report omitted its typed tab group")
    tabs = tab_group.get("tabs")
    if not isinstance(tabs, list) or [tab.get("label") for tab in tabs] != labels:
        raise ValueError("Discovery PRISM Report omitted a required compatible tab")
    for (slug, unused), tab in zip(DISCOVERY_REPORT_SECTIONS, tabs):
        content = tab.get("sections")
        if (
            tab.get("id") != slug
            or not isinstance(content, list)
            or len(content) != 1
            or content[0].get("kind") != "markdown"
            or content[0].get("id") != slug + "-content"
            or not str(content[0].get("text", "")).strip()
        ):
            raise ValueError("Discovery PRISM Report contains an invalid typed tab: " + slug)
    template = report.get("template")
    template_sections = template.get("sections") if isinstance(template, dict) else None
    if (
        not isinstance(template_sections, list)
        or len(template_sections) != 1
        or template_sections[0].get("kind") != "tabs"
        or [tab.get("id") for tab in template_sections[0].get("tabs", [])]
        != [slug for slug, unused in DISCOVERY_REPORT_SECTIONS]
    ):
        raise ValueError("Discovery PRISM Report template is incompatible")


def verify(*, state, execution, **unused):
    """Reject incomplete reasoning and render a runtime-only passing disposition."""
    expected = state["contract"]["expected_steps"]
    if execution.prism_execution.status != "accepted":
        raise ValueError("PRISM execution was not accepted")
    if execution.completed_steps != expected or execution.reasoning_event_count < len(expected) * 2:
        raise ValueError("Reasoning completion evidence is incomplete")
    result_value = execution.reasoning_result
    if not isinstance(result_value, dict):
        result_value = {"value": result_value}
    provenance = {
        "request_digest": state["prepared"]["request_digest"],
        "source_hash": execution.prism_execution.source_hash,
        "module_hashes": dict(execution.prism_execution.module_hashes),
        "reasoning_event_count": execution.reasoning_event_count,
        "agent_invocations": execution.agent_receipts,
    }
    final = {
        "status": "passed",
        "summary": (
            "The complete declared PRISM reasoning graph ran to acceptance and its "
            "typed generated result was retained."
        ),
        "reasoning_complete": True,
        "blockers": [],
        "completed_reasoning_steps": expected,
        "limitations": [
            "Runtime completion does not prove a theorem or validate a scientific claim.",
            "No native theorem prover, experiment, source validator, or release backend was executed.",
            "Any domain disposition inside the typed result remains model-generated and must be reviewed on its own evidence.",
        ],
    }
    structured = {
        "final_disposition": final,
        "reasoning_result": result_value,
        "execution_provenance": provenance,
    }
    root = Path(state["run_root"])
    report_checks = [
        "complete_reasoning_trace",
        "typed_prism_result",
        "deterministic_report_projection",
    ]
    if state["workflow_id"] == "discovery_marathon_loop":
        from dataclasses import replace
        from prism_stdlib.report_codec import decode_report, export_report

        report_output = execution.prism_execution.run_output
        report_value = report_output.result
        report_provenance = report_output.provenance
        references = {
            item.identity: item for item in report_provenance.values
        } if report_provenance is not None else {}
        report_reference = report_provenance.result if report_provenance is not None else None
        # The effectful entrypoint returns Result[Report, ModelFailure].  The report
        # codec requires the accepted inner named Report and its matching native graph
        # root. Select the already-recorded ``value`` child without synthesizing or
        # deleting any provenance values, activities, trace entries, or effects.
        while not hasattr(report_value, "fields") and hasattr(report_value, "value"):
            report_value = report_value.value
            parent = references.get(report_reference)
            report_reference = dict(parent.children).get("value") if parent else None
        if not hasattr(report_value, "fields"):
            raise ValueError("Discovery workflow did not return a named PRISM Report")
        if report_provenance is None or report_reference not in references:
            raise ValueError("Discovery PRISM Report has no native provenance reference")
        typed_report = export_report(replace(
            report_output,
            result=report_value,
            provenance=replace(report_provenance, result=report_reference),
        ))
        decode_report(typed_report, attachments={})
        _validate_typed_discovery_report(typed_report)
        sections = _discovery_sections(state, execution, structured)
        markdown, layout = _assemble_native_report(sections)
        latest_html = _discovery_html(sections, "overview")
        timeline_html = _discovery_html(sections, "timeline")
        _validate_discovery_report(markdown, layout, latest_html, timeline_html)
        report_artifacts = [
            "report.md",
            "result.json",
            "latest.md",
            "latest.json",
            "latest.html",
            "full_timeline.html",
        ]
        structured.update(
            {
                "report_layout": layout,
                "typed_report": typed_report,
                "report_contract": {
                    "schema_version": "abducer.discovery-marathon-report/v1",
                    "presentation": "prism-typed-report/v1",
                    "terminal_output_type": "prism.reporting.report.Report",
                    "compatibility": "repository-section-compatible",
                    "required_sections": [label for unused, label in DISCOVERY_REPORT_SECTIONS],
                    "artifacts": report_artifacts,
                    "typed_report_artifact": "typed-report.json",
                },
                "discovery_report": {
                    "context_summary": state["inputs"]["context_summary"],
                    "stages": execution.step_results,
                    "routing": result_value,
                },
            }
        )
        payload = json.dumps(structured, indent=2, sort_keys=True, ensure_ascii=False, allow_nan=False) + "\n"
        (root / "latest.md").write_text(markdown, encoding="utf-8")
        (root / "latest.json").write_text(payload, encoding="utf-8")
        (root / "latest.html").write_text(latest_html, encoding="utf-8")
        (root / "full_timeline.html").write_text(timeline_html, encoding="utf-8")
        (root / "typed-report.json").write_text(
            json.dumps(typed_report, indent=2, sort_keys=True, ensure_ascii=False, allow_nan=False) + "\n",
            encoding="utf-8",
        )
        report_checks.extend(
            [
                "repository_compatible_sections",
                "prism_typed_report",
                "native_report_layout",
                "self_contained_html_reports",
            ]
        )
    else:
        markdown = _markdown(state["workflow_id"], structured)
    (root / "report.md").write_text(markdown, encoding="utf-8")
    (root / "result.json").write_text(
        json.dumps(structured, indent=2, sort_keys=True, ensure_ascii=False, allow_nan=False) + "\n",
        encoding="utf-8",
    )
    return {
        "result": {
            "markdown": markdown,
            "structured_value": structured,
            "analysis_results": {
                "execution_scope": "source-grounded-model-reasoning",
                "reasoning_complete": True,
                "scientific_truth_verified": False,
                "report_compatibility": (
                    "abducer.discovery-marathon-report/v1"
                    if state["workflow_id"] == "discovery_marathon_loop"
                    else "generic-runtime-report/v1"
                ),
                "report_type": (
                    "prism.reporting.report.Report"
                    if state["workflow_id"] == "discovery_marathon_loop"
                    else "runtime-markdown"
                ),
            },
            "compact_prism_input": state["inputs"],
            "narrative_slots": [],
            "report_verification": {
                "status": "passed",
                "reasoning_complete": True,
                "repository_report_compatible": state["workflow_id"] == "discovery_marathon_loop",
                "checks": report_checks,
            },
        },
        "events": [{"kind": "artifact", "payload": {
            "workflow_id": state["workflow_id"],
            "status": "rendered",
        }}],
    }
