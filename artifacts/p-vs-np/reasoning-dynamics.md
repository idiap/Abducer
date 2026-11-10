# Reasoning Dynamics Report

## Overview

- States: 103
- Time span (s): 13.88561
- Node growth: 2 -> 104
- Edge growth: 1 -> 165
- Concept update checkpoints: 12

## Process Distribution

- event `step`: 33
- event `declared_output`: 27
- event `stage_started`: 16
- event `stage_completed`: 15
- event `log_started`: 12

## Operation Totals

- `declared_output`: 27
- `emits_output`: 52
- `invokes_agent`: 15
- `stage_completed`: 15
- `stage_started`: 16

## Conceptual Topology

- concept_graph_nodes: 256
- concept_graph_relations: 779
- coherence_global: 0.313319
- hypothesis_total: 44
- loop_open_count: 22
- concept_topology_index: 0.087147

## Interpretation Hints

- Rising `graph.edge_count` with stable or improving `concept_topology_index` indicates productive expansion.
- High `stage_started` but low `declared_output` suggests orchestration churn without artifact yield.
- Falling `loop_open_count` with non-negative `coherence_global` indicates healthier inferential convergence.
