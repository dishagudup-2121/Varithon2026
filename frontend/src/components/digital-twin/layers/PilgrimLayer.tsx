import { CircleMarker, FeatureGroup } from 'react-leaflet';

// Synthetic demo data representing aggregated pilgrim groups (Phase 1 placeholder)
// In Phase 2, this will be driven by real-time WebSocket state.
const mockPilgrims = [
  { id: 'G001', lat: 18.6659, lng: 73.8969, count: 150 },
  { id: 'G002', lat: 18.6500, lng: 73.8920, count: 300 },
  { id: 'G003', lat: 18.6300, lng: 73.8800, count: 75 },
  { id: 'G004', lat: 18.6100, lng: 73.8750, count: 420 },
];

export default function PilgrimLayer() {
  return (
    <FeatureGroup>
      {mockPilgrims.map((group) => (
        <CircleMarker 
          key={group.id}
          center={[group.lat, group.lng]} 
          radius={Math.max(4, Math.min(12, group.count / 30))} // Dynamically scale based on count
          pathOptions={{ 
            color: '#38bdf8', // sky-400
            fillColor: '#38bdf8', 
            fillOpacity: 0.8,
            weight: 2
          }} 
        />
      ))}
    </FeatureGroup>
  );
}
