import { create } from 'zustand';
import { StateResponse, PredictionResponse, RecommendationResponse, SimulationResult } from '../types/api';

interface DashboardState {
  systemState: StateResponse | null;
  predictions: PredictionResponse | null;
  recommendations: RecommendationResponse | null;
  simulationResult: SimulationResult | null;
  selectedZoneId: string | null;
  
  setSystemState: (state: StateResponse) => void;
  setPredictions: (preds: PredictionResponse) => void;
  setRecommendations: (recs: RecommendationResponse) => void;
  setSimulationResult: (res: SimulationResult | null) => void;
  setSelectedZoneId: (id: string | null) => void;
}

export const useDashboardStore = create<DashboardState>((set) => ({
  systemState: null,
  predictions: null,
  recommendations: null,
  simulationResult: null,
  selectedZoneId: null,
  
  setSystemState: (state) => set({ systemState: state }),
  setPredictions: (preds) => set({ predictions: preds }),
  setRecommendations: (recs) => set({ recommendations: recs }),
  setSimulationResult: (res) => set({ simulationResult: res }),
  setSelectedZoneId: (id) => set({ selectedZoneId: id }),
}));
