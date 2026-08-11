export interface GeoPoint {
  lat: number;
  lng: number;
}

export type RiskLevel = 'low' | 'medium' | 'high' | 'critical';
export type RouteStatus = 'open' | 'restricted' | 'closed';

export interface Zone {
  zone_id: string;
  name: string;
  center: GeoPoint;
  polygon: GeoPoint[];
  risk_level?: RiskLevel;
  current_density?: number;
  eta_critical?: string;
}

export interface RouteSegment {
  segment_id: string;
  route_id: string;
  geometry: GeoPoint[];
  status: RouteStatus;
}

export interface Route {
  route_id: string;
  name: string;
  segments: RouteSegment[];
  status: RouteStatus;
}

export interface MapEntity {
  id: string;
  type: string;
  location: GeoPoint;
  metadata?: Record<string, unknown>;
}
