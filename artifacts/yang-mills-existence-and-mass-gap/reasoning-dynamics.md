# Reasoning Dynamics Report

## Overview

- States: 97
- Time span (s): 5.933797
- Node growth: 2 -> 105
- Edge growth: 1 -> 167
- Concept update checkpoints: 12

## Process Distribution

- event `step`: 30
- event `declared_output`: 25
- event `stage_started`: 16
- event `stage_completed`: 15
- event `log_started`: 11

## Operation Totals

- `declared_output`: 25
- `emits_output`: 50
- `invokes_agent`: 17
- `stage_completed`: 15
- `stage_started`: 16

## Conceptual Topology

- concept_graph_nodes: 143
- concept_graph_relations: 842
- coherence_global: 0.320043
- hypothesis_total: 44
- loop_open_count: 36
- concept_topology_index: 0.100754

## Interpretation Hints

- Rising `graph.edge_count` with stable or improving `concept_topology_index` indicates productive expansion.
- High `stage_started` but low `declared_output` suggests orchestration churn without artifact yield.
- Falling `loop_open_count` with non-negative `coherence_global` indicates healthier inferential convergence.
