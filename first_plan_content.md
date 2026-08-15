# Phase 2A: Road Network Graph Foundation

This plan outlines the steps to build the backend graph foundation for the Digital Twin using the verified OpenStreetMap dataset, as specified in the Phase 2A requirements.

## Proposed Architecture

I will introduce a new module under `backend/app/graph/` dedicated to constructing, modeling, and validating the road network graph.

### Module Structure
- **[NEW]** `backend/app/graph/__init__.py` - Exports public methods.
- **[NEW]** `backend/app/graph/graph_model.py` - Core classes for the node and edge types if necessary, though NetworkX attributes will be the primary data store.
- **[NEW]** `backend/app/graph/graph_builder.py` - Contains the `build_graph(osm_data)` function.
- **[NEW]** `backend/app/graph/graph_validator.py` - Contains validation checks for connectivity and attributes.
- **[NEW]** `backend/tests/test_graph.py` - Contains isolated unit tests testing the builder, one-way paths, disconnected networks, and coordinates.

### Graph Characteristics
- **Type**: `networkx.DiGraph`
- **Nodes**: Each unique OSM node reference inside the ways becomes a graph node. Attributes: `lat`, `lng`, `osm_node_id`. Nodes are identified deterministically (e.g., `N_{osm_node_id}`).
- **Edges**: We iterate through each OSM way's node sequence `[N1, N2, ..., N_k]`. For each adjacent pair `(N_i, N_{i+1})`, we create a directed edge.
- **Directionality**: 
  - If `oneway=yes`, `oneway=true`, or `oneway=1` is found in the way's tags, we add one directed edge `N_i -> N_{i+1}`.
  - Otherwise, we add two directed edges `N_i -> N_{i+1}` and `N_{i+1} -> N_i`.
- **Distance Calculation**: I will implement a standard Haversine formula in Python `math` to calculate edge lengths in meters, satisfying the geospatial requirement without adding heavy dependencies.

## Verification Plan

### Automated Tests
I will add `backend/tests/test_graph.py` which will be executed via `pytest`. The tests will cover:
1. Bidirectional way creation.
2. One-way way creation.
3. Intersection node connectivity.
4. Haversine distance accuracy.
5. Deterministic ID generation.

### Graph Diagnostics script
I will create a temporary diagnostics script `backend/scripts/phase2a_diagnostics.py` to load `osm_data.json`, construct the graph, run validations, and print the required final statistics.

### Build & Lint
I will run the frontend build and lint commands as requested to prove that the existing Phase 1 components remain unaffected.

## Open Questions
- Is placing the `graph` module under `backend/app/graph/` acceptable based on your current backend architecture?
- Are there any other specific "oneway" tag values used locally in the Pune region that you want handled explicitly? (e.g., `oneway=-1` for reversed one-way streets).

Please review the proposed approach above. Once approved, I will proceed with the implementation.
