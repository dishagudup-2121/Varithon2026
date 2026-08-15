import { GeoJSON } from 'react-leaflet';
import type { FeatureCollection, Feature, Geometry, GeoJsonProperties } from 'geojson';
import type { Layer } from 'leaflet';
import zonesData from '../../../data/geospatial/zones.json';

const zones = zonesData as FeatureCollection;

export default function ZoneLayer() {
  
  const getStyle = () => {
    // Neutral administrative boundary styling
    return {
      color: '#475569', // slate-600
      fillColor: '#64748b', // slate-500
      fillOpacity: 0.08,
      weight: 2,
      dashArray: '5, 5'
    };
  };

  const onEachFeature = (feature: Feature<Geometry, GeoJsonProperties>, layer: Layer) => {
    if (feature.properties) {
      const { name, zone_id } = feature.properties;
      
      const popupContent = `
        <div class="bg-white border border-slate-200 rounded-lg p-3 w-48 shadow-sm">
          <div class="flex flex-col">
            <h4 class="font-bold text-sm leading-tight text-slate-800">${name}</h4>
            <span class="text-[10px] text-slate-500 uppercase tracking-wide mt-1 font-semibold">Zone ID: ${zone_id}</span>
          </div>
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
