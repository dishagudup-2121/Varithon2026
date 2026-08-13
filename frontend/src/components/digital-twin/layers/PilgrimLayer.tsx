import { CircleMarker, FeatureGroup } from 'react-leaflet';
import { useEffect, useState, useRef } from 'react';
import { PilgrimGroupState } from '../../../types/simulation';
import { getWebSocketUrl } from '../../../config/api';

export default function PilgrimLayer() {
  const [pilgrims, setPilgrims] = useState<PilgrimGroupState[]>([]);
  const wsRef = useRef<WebSocket | null>(null);

  useEffect(() => {
    // Prevent duplicate connections in StrictMode
    if (wsRef.current) {
      wsRef.current.close();
    }

    const wsUrl = getWebSocketUrl('/api/simulation/ws');
    const ws = new WebSocket(wsUrl);
    wsRef.current = ws;

    ws.onopen = () => {
      console.log('[PilgrimLayer] WebSocket connected');
    };

    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        
        // Message validation
        if (!data || typeof data !== 'object') return;
        if (typeof data.tick !== 'number') return;
        if (!Array.isArray(data.groups)) return;

        const validGroups = data.groups.filter((g: Record<string, unknown>) => {
          if (!g || typeof g.group_id !== 'string') return false;
          if (typeof g.count !== 'number') return false;
          if (g.position !== null) {
            if (typeof g.position !== 'object') return false;
            const pos = g.position as Record<string, unknown>;
            if (typeof pos.lat !== 'number' || !Number.isFinite(pos.lat)) return false;
            if (typeof pos.lng !== 'number' || !Number.isFinite(pos.lng)) return false;
          }
          return true;
        }) as PilgrimGroupState[];

        setPilgrims(validGroups);
      } catch (err) {
        console.warn('[PilgrimLayer] Received invalid WebSocket message', err);
      }
    };

    ws.onerror = (error) => {
      console.error('[PilgrimLayer] WebSocket error:', error);
    };

    ws.onclose = () => {
      console.log('[PilgrimLayer] WebSocket closed');
      if (wsRef.current === ws) {
        wsRef.current = null;
      }
    };

    return () => {
      // Clean up connection when component unmounts (e.g. toggled off or StrictMode unmount)
      if (ws.readyState === WebSocket.OPEN || ws.readyState === WebSocket.CONNECTING) {
        ws.close();
      }
      if (wsRef.current === ws) {
        wsRef.current = null;
      }
    };
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
