import { useRef, useEffect } from 'react';
import { GeoJSON, useMapEvents } from 'react-leaflet';
import type { FeatureCollection, Feature, Geometry, GeoJsonProperties } from 'geojson';
import L from 'leaflet';
import routesData from '../../../data/geospatial/routes.json';

// Type assertion since TS doesn't automatically infer GeoJSON structure perfectly from JSON imports
const routes = routesData as FeatureCollection;

export default function RouteLayer() {
  const geoJsonRef = useRef<L.GeoJSON>(null);
  
  const map = useMapEvents({
    zoomend: () => {
      if (geoJsonRef.current) {
        geoJsonRef.current.setStyle((feature) => getStyle(feature as Feature<Geometry, GeoJsonProperties>, map.getZoom()));
      }
    }
  });

  const getStyle = (feature?: Feature<Geometry, GeoJsonProperties>, currentZoom?: number) => {
    const status = feature?.properties?.status || 'open';
    const highway = feature?.properties?.highway || 'unclassified';
    const source = feature?.properties?.source || '';
    const zoom = currentZoom || map.getZoom();
    
    // Default subdued network style
    let defaultStyle = {
      color: '#64748b', // slate-500
      weight: 2,
      opacity: 0.3
    };

    // Zoom-dependent visibility for non-operational routes
    if (source === 'OpenStreetMap' && status === 'open') {
      if (zoom < 14) {
        if (!['primary', 'secondary', 'tertiary'].includes(highway)) {
          return { opacity: 0, weight: 0 };
        }
        defaultStyle = { color: '#64748b', weight: 3, opacity: 0.5 };
      } else if (zoom < 16) {
        if (!['primary', 'secondary', 'tertiary', 'residential'].includes(highway)) {
          return { opacity: 0, weight: 0 };
        }
        if (highway === 'residential') {
          defaultStyle = { color: '#475569', weight: 2, opacity: 0.3 };
        } else {
          defaultStyle = { color: '#64748b', weight: 4, opacity: 0.6 };
        }
      } else {
        // High zoom, show everything
        if (['service', 'unclassified', 'minor'].includes(highway)) {
          defaultStyle = { color: '#334155', weight: 1.5, opacity: 0.3 };
        } else if (highway === 'residential') {
          defaultStyle = { color: '#475569', weight: 2.5, opacity: 0.4 };
        } else {
          defaultStyle = { color: '#64748b', weight: 5, opacity: 0.7 };
        }
      }
      return defaultStyle;
    }
    
    // Operational route styles
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

  useEffect(() => {
    if (geoJsonRef.current && map) {
       geoJsonRef.current.setStyle((feature) => getStyle(feature as Feature<Geometry, GeoJsonProperties>, map.getZoom()));
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [map]);

  return (
    <GeoJSON 
      ref={geoJsonRef}
      data={routes}
      style={(feature) => getStyle(feature as Feature<Geometry, GeoJsonProperties>, map.getZoom())}
    />
  );
}
