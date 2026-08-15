import { CircleMarker, FeatureGroup, Tooltip } from 'react-leaflet';
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
            radius={Math.max(3, Math.min(8, group.count / 40))}
            pathOptions={{ 
              color: '#38bdf8', // sky-400
              fillColor: '#38bdf8', 
              fillOpacity: 0.8,
              weight: 2,
              className: 'pilgrim-marker'
            }} 
          >
            <Tooltip direction="top" offset={[0, -10]} opacity={0.95}>
              <div className="text-xs text-[#3D2918] font-medium p-1">
                <div className="font-bold border-b border-gray-200 pb-1 mb-1 flex justify-between items-center gap-4">
                  <span>{group.group_id}</span>
                  <span className={`px-1.5 py-0.5 rounded text-[9px] uppercase ${
                    group.status === 'moving' ? 'bg-green-100 text-green-700' :
                    group.status === 'stopped' ? 'bg-gray-100 text-gray-700' :
                    'bg-red-100 text-red-700'
                  }`}>
                    {group.status}
                  </span>
                </div>
                <div className="grid grid-cols-2 gap-x-4 gap-y-1 mt-1">
                  <span className="text-[#8B735D]">Count:</span>
                  <span className="font-semibold">{group.count}</span>
                  
                  <span className="text-[#8B735D]">Actual Speed:</span>
                  <span className="font-semibold">
                    {group.status === 'moving' ? group.speed_mps.toFixed(2) : '0.00'} m/s
                  </span>
                  
                  <span className="text-[#8B735D]">Dest:</span>
                  <span className="font-semibold truncate max-w-[80px]">{group.destination_zone_id}</span>
                </div>
              </div>
            </Tooltip>
          </CircleMarker>
        );
      })}
    </FeatureGroup>
  );
}
