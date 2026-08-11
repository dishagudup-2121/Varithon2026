import { GeoJSON } from 'react-leaflet';
import type { FeatureCollection, Feature, Geometry, GeoJsonProperties } from 'geojson';
import type { Layer } from 'leaflet';
import zonesData from '../../../data/geospatial/zones.json';

const zones = zonesData as FeatureCollection;

export default function ZoneLayer() {
  
  const getStyle = (feature?: Feature<Geometry, GeoJsonProperties>) => {
    const risk = feature?.properties?.risk_level || 'low';
    
    let color = '#22c55e'; // green
    if (risk === 'critical') color = '#ef4444'; // red
    else if (risk === 'high') color = '#f97316'; // orange
    else if (risk === 'medium') color = '#f59e0b'; // amber

    return {
      color: color,
      fillColor: color,
      fillOpacity: 0.2,
      weight: 2
    };
  };

  const onEachFeature = (feature: Feature<Geometry, GeoJsonProperties>, layer: Layer) => {
    if (feature.properties) {
      const { name, zone_id, risk_level, current_density, eta_critical } = feature.properties;
      
      const popupContent = `
        <div class="bg-slate-900 border border-slate-700 rounded-lg p-3 w-56 text-white custom-popup-container">
          <div class="flex justify-between items-start mb-2">
            <div>
              <h4 class="font-bold text-sm leading-tight">${name}</h4>
              <span class="text-[10px] text-slate-400 uppercase tracking-wide">${zone_id}</span>
            </div>
            <span class="inline-flex items-center px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider border ${
              risk_level === 'critical' ? 'bg-red-500/20 text-red-400 border-red-500/30' :
              risk_level === 'high' ? 'bg-orange-500/20 text-orange-400 border-orange-500/30' :
              risk_level === 'medium' ? 'bg-amber-500/20 text-amber-400 border-amber-500/30' :
              'bg-green-500/20 text-green-400 border-green-500/30'
            }">${risk_level}</span>
          </div>
          <div class="space-y-2 mt-3">
            <div class="flex justify-between text-xs">
              <span class="text-slate-400">Crowd Density</span>
              <span class="font-bold">${current_density}%</span>
            </div>
            <div class="flex justify-between text-xs">
              <span class="text-slate-400">ETA to Critical</span>
              <span class="font-bold">${eta_critical}</span>
            </div>
          </div>
          <button class="text-xs text-orange-400 mt-3 hover:text-orange-300 w-full text-left">View Details →</button>
        </div>
      `;
      layer.bindPopup(popupContent);
    }
  };

  return (
    <GeoJSON 
      data={zones}
      style={getStyle}
      onEachFeature={onEachFeature}
    />
  );
}
