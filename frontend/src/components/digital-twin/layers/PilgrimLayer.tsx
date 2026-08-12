import { CircleMarker, FeatureGroup } from 'react-leaflet';
import { useEffect, useState } from 'react';

// Using a localized interface to satisfy TS/ESLint without needing full api type if it's missing or unused
interface PilgrimPosition {
  lat: number;
  lng: number;
}
interface PilgrimGroupResponseData {
  group_id: string;
  count: number;
  position: PilgrimPosition | null;
}
interface SimStateResponseData {
  groups: PilgrimGroupResponseData[];
}

export default function PilgrimLayer() {
  const [pilgrims, setPilgrims] = useState<PilgrimGroupResponseData[]>([]);

  useEffect(() => {
    fetch('http://localhost:8000/api/simulation/state')
      .then(res => res.json())
      .then((data: SimStateResponseData) => {
        if (data && data.groups) {
          setPilgrims(data.groups);
        }
      })
      .catch(err => console.error("Failed to fetch simulation state", err));
  }, []);

  return (
    <FeatureGroup>
      {pilgrims.map((group) => {
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
