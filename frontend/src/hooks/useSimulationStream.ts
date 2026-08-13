import { useState, useEffect, useRef } from 'react';
import { SimulationState } from '../types/simulation';
import { getWebSocketUrl } from '../config/api';

export function useSimulationStream() {
  const [simulationState, setSimulationState] = useState<SimulationState | null>(null);
  const [isConnected, setIsConnected] = useState(false);
  const wsRef = useRef<WebSocket | null>(null);

  useEffect(() => {
    // Prevent duplicate connections in React StrictMode
    if (wsRef.current) {
      wsRef.current.close();
    }

    const wsUrl = getWebSocketUrl('/api/simulation/ws');
    const ws = new WebSocket(wsUrl);
    wsRef.current = ws;

    ws.onopen = () => {
      console.log('[SimulationStream] WebSocket connected');
      setIsConnected(true);
    };

    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        
        // Basic validation
        if (!data || typeof data !== 'object') return;
        if (typeof data.tick !== 'number') return;
        if (!Array.isArray(data.groups)) return;
        if (!data.crowd || !data.crowd.summary || !Array.isArray(data.crowd.edges)) return;

        setSimulationState(data as SimulationState);
      } catch (err) {
        console.warn('[SimulationStream] Received invalid WebSocket message', err);
      }
    };

    ws.onerror = (error) => {
      console.error('[SimulationStream] WebSocket error:', error);
      setIsConnected(false);
    };

    ws.onclose = () => {
      console.log('[SimulationStream] WebSocket closed');
      setIsConnected(false);
      if (wsRef.current === ws) {
        wsRef.current = null;
      }
    };

    return () => {
      // Clean up connection when component unmounts (e.g. DigitalTwinMap unmounted)
      if (ws.readyState === WebSocket.OPEN || ws.readyState === WebSocket.CONNECTING) {
        ws.close();
      }
      if (wsRef.current === ws) {
        wsRef.current = null;
      }
    };
  }, []);

  return { simulationState, isConnected };
}
