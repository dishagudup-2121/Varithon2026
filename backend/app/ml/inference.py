import os
import json
import logging
from typing import Optional, List
import joblib

from ..schemas.prediction import EdgeLoadPrediction
from ..simulation.temporal_manager import TemporalStateManager
from .features import extract_features

logger = logging.getLogger(__name__)

class PredictionEngine:
    def __init__(self):
        self.model = None
        self.metadata = {}
        self.model_loaded = False
        self._load_model()
        
    def _load_model(self):
        try:
            model_dir = os.path.join(os.path.dirname(__file__), '../../models')
            model_path = os.path.join(model_dir, 'edge_load_model.joblib')
            meta_path = os.path.join(model_dir, 'edge_load_metadata.json')
            
            if os.path.exists(model_path) and os.path.exists(meta_path):
                self.model = joblib.load(model_path)
                with open(meta_path, 'r') as f:
                    self.metadata = json.load(f)
                self.model_loaded = True
                logger.info(f"Successfully loaded model {self.metadata.get('model_version')} for inference.")
            else:
                logger.warning("No trained model found for inference. Inference will return None.")
        except Exception as e:
            logger.error(f"Failed to load prediction model safely: {e}")
            self.model_loaded = False

    def predict_edge_load(self, temporal_manager: TemporalStateManager, edge_id: str, forecast_horizon_ticks: int = 900) -> Optional[EdgeLoadPrediction]:
        """
        Safely predicts the load for an edge at T + horizon.
        Never throws an exception to the caller.
        """
        if not self.model_loaded:
            return None
            
        try:
            history = temporal_manager.history
            if not history:
                return None
                
            current_snap = temporal_manager.get_latest_tick()
            if not current_snap:
                return None
                
            features = extract_features(list(history), edge_id, current_snap.tick)
            if not features:
                # E.g., not enough history
                return None
                
            # Prepare feature vector strictly according to saved metadata
            feature_cols = self.metadata.get("features", [])
            feature_dict = features.model_dump()
            
            X = [[feature_dict[col] for col in feature_cols]]
            
            # Predict
            pred = self.model.predict(X)[0]
            
            # Guard against NaNs
            import math
            if not math.isfinite(pred):
                logger.warning(f"Model returned non-finite prediction for edge {edge_id}")
                return None
                
            # Ensure no negative crowd
            pred = max(0.0, float(pred))
            
            # Current time
            sim_time_str = current_snap.simulation_time
            from datetime import datetime
            
            # Depending on how sim_time_str is formatted, we'll parse or just keep as is
            return EdgeLoadPrediction(
                edge_id=edge_id,
                prediction_timestamp=datetime.fromisoformat(sim_time_str.replace("Z", "+00:00")),
                forecast_horizon_ticks=forecast_horizon_ticks,
                predicted_load=pred,
                model_version=self.metadata.get("model_version", "unknown"),
                model_identifier=self.metadata.get("model_identifier", "unknown")
            )
            
        except Exception as e:
            logger.error(f"Inference exception for edge {edge_id}: {e}")
            return None

# Single singleton for inference
prediction_engine = PredictionEngine()
