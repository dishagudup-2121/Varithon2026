from pydantic import BaseModel, Field
from datetime import datetime

class EdgeLoadPrediction(BaseModel):
    edge_id: str = Field(description="The graph edge identifier, e.g., E_R_OSM_...")
    prediction_timestamp: datetime = Field(description="The simulation time at which this prediction was made")
    forecast_horizon_ticks: int = Field(description="The number of ticks into the future for this prediction")
    predicted_load: float = Field(description="The predicted absolute pilgrim count")
    model_version: str = Field(description="The version string of the model, e.g., random_forest_v1")
    model_identifier: str = Field(description="The identifier for the model, e.g., absolute_edge_load")
