import os
import json
import networkx as nx
from typing import List, Dict
from datetime import datetime, timezone

from .pilgrim_model import PilgrimGroup
from ..graph.graph_builder import build_graph
from .generator import generate_pilgrim_groups
from .route_planner import plan_route
from .movement_engine import tick_movement

class SimulationStateManager:
    """
    Holds the deterministic in-memory simulation state.
    Initializes once on startup and provides read-only deep copies to the API.
    """
    def __init__(self, count: int = 85, seed: int = 42):
        self.tick = 0
        self.sim_time = datetime(2026, 8, 12, 12, 0, tzinfo=timezone.utc)
        self.groups: Dict[str, PilgrimGroup] = {}
        self.graph: nx.DiGraph = nx.DiGraph()
        
        self._initialize_state(count, seed)
        
    def _initialize_state(self, count: int, seed: int):
        osm_path = os.path.join(os.path.dirname(__file__), '../../../osm_data.json')
        zones_path = os.path.join(os.path.dirname(__file__), '../../../frontend/src/data/geospatial/zones.json')
        
        # In a test environment without OSM data, we shouldn't crash. 
        if not os.path.exists(osm_path) or not os.path.exists(zones_path):
            return
            
        with open(osm_path, 'r') as f:
            osm_data = json.load(f)
        with open(zones_path, 'r') as f:
            zones_data = json.load(f)
            
        self.graph = build_graph(osm_data)
        
        groups_list = generate_pilgrim_groups(
            graph=self.graph,
            zones_data=zones_data,
            simulation_time=self.sim_time,
            count=count,
            seed=seed
        )
        
        for g in groups_list:
            res = plan_route(self.graph, g, zones_data)
            if res.status == "routed":
                g.route = res.edge_ids
                self.groups[g.group_id] = g
                
    def get_state_snapshot(self) -> List[PilgrimGroup]:
        """
        Returns a deep copy snapshot of the groups to isolate state mutation from API responses.
        """
        return [g.model_copy(deep=True) for g in self.groups.values()]
        
    def advance(self, delta_time_s: float):
        """
        Advances the simulation deterministically.
        Never called from GET endpoints.
        """
        self.tick += 1
        for g_id, g in self.groups.items():
            tick_movement(self.graph, g, delta_time_s)
