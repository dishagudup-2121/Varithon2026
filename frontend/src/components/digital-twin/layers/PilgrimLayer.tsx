import { CircleMarker, FeatureGroup } from 'react-leaflet';
import { SimulationState } from '../../../types/simulation';

interface PilgrimLayerProps {
  state: SimulationState | null;
}

export default function PilgrimLayer({ state }: PilgrimLayerProps) {
  if (!state || !state.groups) return null;


  return (
    <FeatureGroup>
      {state.groups.map((group) => {
        if (!group.position) return null;
        
        return (
          <CircleMarker 
            key={group.group_id}
            center={[group.position.lat, group.position.lng]} 
            radius={Math.max(4, Math.min(12, group.count / 30))}
            pathOptions={{ 
              color: '#38bdf8', // sky-400
              fillColor: '#38bdf8', 
              fillOpacity: 0.8,
              weight: 2
            }} 
          />
        );
      })}
    </FeatureGroup>
  );
}
