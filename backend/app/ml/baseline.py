from .features import EdgeFeatures

def predict_persistence(features: EdgeFeatures) -> int:
    """
    Persistence baseline: prediction(E, T+15) = load(E, T)
    This is a deterministic baseline. It is NOT ML.
    It returns the current observed edge load as the prediction.
    """
    return features.current_load
