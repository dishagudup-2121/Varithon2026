export interface GeoPosition {
  lat: number;
  lng: number;
}

export interface PilgrimGroupState {
  group_id: string;
  count: number;
  speed_mps: number;
  progress: number;
  status: 'moving' | 'stopped' | 'congested';
  current_edge_id: string;
  destination_zone_id: string;
  updated_at: string;
  position: GeoPosition | null;
}

export interface CrowdEdgeLoad {
  edge_id: string;
  pilgrim_count: number;
  group_count: number;
  moving_group_count: number;
  stopped_group_count: number;
  congested_group_count: number;
}

export interface CrowdSummary {
  total_pilgrims: number;
  total_groups: number;
  active_edge_count: number;
  moving_group_count: number;
  stopped_group_count: number;
  congested_group_count: number;
  unresolved_group_count: number;
}

export interface CrowdStateSnapshot {
  summary: CrowdSummary;
  edges: CrowdEdgeLoad[];
}

export interface SimulationState {
  simulation_time: string;
  tick: number;
  groups: PilgrimGroupState[];
  crowd: CrowdStateSnapshot;
}
