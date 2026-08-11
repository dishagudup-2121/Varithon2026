import { GeoJSON } from 'react-leaflet';
import type { FeatureCollection, Feature, Geometry, GeoJsonProperties } from 'geojson';
import routesData from '../../../data/geospatial/routes.json';

// Type assertion since TS doesn't automatically infer GeoJSON structure perfectly from JSON imports
const routes = routesData as FeatureCollection;

export default function RouteLayer() {
  
  const getStyle = (feature?: Feature<Geometry, GeoJsonProperties>) => {
    const status = feature?.properties?.status || 'open';
    
    switch (status) {
      case 'restricted':
        return {
          color: '#f59e0b', // amber-500
          weight: 4,
          opacity: 0.8,
          dashArray: '10, 10'
        };
      case 'closed':
        return {
          color: '#ef4444', // red-500
          weight: 5,
          opacity: 0.9,
          dashArray: '5, 5'
        };
      case 'open':
      default:
        return {
          color: '#3b82f6', // blue-500
          weight: 4,
          opacity: 0.6
        };
    }
  };

  return (
    <GeoJSON 
      data={routes}
      style={getStyle}
    />
  );
}
