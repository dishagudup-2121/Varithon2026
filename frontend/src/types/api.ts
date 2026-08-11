export interface Zone {
  zone_id: string;
  name: string;
  lat: number;
  lng: number;
  crowd_count: number;
  temperature_c: number;
  humidity_percent: number;
  water_availability_percent: number;
}

export interface Agent {
  agent_id: string;
  count: number;
  lat: number;
  lng: number;
  route_id: string;
  status: string;
}

export interface Resource {
  resource_id: string;
  resource_type: string;
  zone_id: string;
  available: boolean;
}

export interface StateResponse {
  timestamp: string;
  zones: Zone[];
  agents: Agent[];
  resources: Resource[];
}

export interface Prediction {
  zone_id: string;
  risk_probability: number;
  risk_level: string;
  horizon_minutes: number;
  confidence_source: string;
}

export interface PredictionResponse {
  predictions: Prediction[];
  model_version: string;
}

export interface Assignment {
  resource_id: string;
  resource_type: string;
  from_zone_id: string;
  to_zone_id: string;
  eta_minutes: number;
  reason: string;
}

export interface RecommendationResponse {
  target_zone_id: string;
  assignments: Assignment[];
  optimization_method: string;
}

export interface SimulationResult {
  scenario: Record<string, unknown>;
  before: { congestion_percent: number; avg_eta_minutes: number; medical_access_percent: number };
  after: { congestion_percent: number; avg_eta_minutes: number; medical_access_percent: number };
  delta: { congestion_percent: number; avg_eta_minutes: number; medical_access_percent: number };
}
