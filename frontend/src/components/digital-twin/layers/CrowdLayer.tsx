import { FeatureGroup, Polyline } from 'react-leaflet';
import { SimulationState } from '../../../types/simulation';
import { useEffect, useState } from 'react';

interface CrowdLayerProps {
  state: SimulationState | null;
}

export default function CrowdLayer({ state }: CrowdLayerProps) {
  const [edgeGeometries, setEdgeGeometries] = useState<Record<string, [number, number][]>>({});

  useEffect(() => {
    // Load static geometry once
    import('../../../data/geospatial/edge_geometry.json')
      .then((module) => {
        setEdgeGeometries(module.default as unknown as Record<string, [number, number][]>);
      })
      .catch((err) => {
        console.error('[CrowdLayer] Failed to load static edge geometry:', err);
      });
  }, []);

  if (!state || !state.crowd || !state.crowd.edges || Object.keys(edgeGeometries).length === 0) {
    return null;
  }

  // Calculate max load for normalization (avoid divide by zero)
  const maxLoad = Math.max(...state.crowd.edges.map((e) => e.pilgrim_count), 1);

  return (
    <FeatureGroup>
      {state.crowd.edges.map((edge) => {
        const rawGeom = edgeGeometries[edge.edge_id];

        if (!rawGeom) {
          // Rule 2: Explicit Unresolved Edge Geometry Handling
          // Do NOT fabricate, do NOT crash, skip deterministically.
          return null;
        }

        // Backend provides [lon, lat]. Leaflet requires [lat, lon].
        const leafletPositions: [number, number][] = rawGeom.map((pt) => [pt[1], pt[0]]);

        // Relative simulated load normalization (0.0 to 1.0)
        const relativeLoad = edge.pilgrim_count / maxLoad;

        // Color gradient from blue (low) to red (high)
        let color = '#3b82f6'; // blue-500
        if (relativeLoad > 0.75) {
          color = '#ef4444'; // red-500
        } else if (relativeLoad > 0.4) {
          color = '#f59e0b'; // amber-500
        } else if (relativeLoad > 0.1) {
          color = '#eab308'; // yellow-500
        }

        return (
          <Polyline
            key={edge.edge_id}
            positions={leafletPositions}
            pathOptions={{
              color,
              weight: 5,
              opacity: 0.8,
            }}
          />
        );
      })}
    </FeatureGroup>
  );
}
