import math
from typing import List
from pydantic import BaseModel

class BaselineMetrics(BaseModel):
    prediction_horizon: int
    mae: float
    rmse: float
    evaluated_samples: int
    unique_edges: int
    skipped_samples: int
    min_target_load: int
    max_target_load: int
    mean_target_load: float

def evaluate_predictions(
    predictions: List[int], 
    targets: List[int], 
    edges: List[str], 
    skipped_samples: int,
    prediction_horizon: int = 15
) -> BaselineMetrics:
    """
    Evaluates baseline predictions deterministically.
    """
    if not predictions or len(predictions) != len(targets):
        return BaselineMetrics(
            prediction_horizon=prediction_horizon,
            mae=0.0, 
            rmse=0.0, 
            evaluated_samples=0, 
            unique_edges=0, 
            skipped_samples=skipped_samples,
            min_target_load=0,
            max_target_load=0,
            mean_target_load=0.0
        )
        
    n = len(predictions)
    abs_errors = [abs(p - t) for p, t in zip(predictions, targets)]
    sq_errors = [(p - t) ** 2 for p, t in zip(predictions, targets)]
    
    mae = sum(abs_errors) / n
    rmse = math.sqrt(sum(sq_errors) / n)
    unique_edges = len(set(edges))
    
    min_target = min(targets)
    max_target = max(targets)
    mean_target = sum(targets) / n
    
    return BaselineMetrics(
        prediction_horizon=prediction_horizon,
        mae=mae,
        rmse=rmse,
        evaluated_samples=n,
        unique_edges=unique_edges,
        skipped_samples=skipped_samples,
        min_target_load=min_target,
        max_target_load=max_target,
        mean_target_load=mean_target
    )
