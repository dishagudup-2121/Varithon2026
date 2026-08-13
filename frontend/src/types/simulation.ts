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

export interface SimulationState {
  simulation_time: string;
  tick: number;
  groups: PilgrimGroupState[];
}
