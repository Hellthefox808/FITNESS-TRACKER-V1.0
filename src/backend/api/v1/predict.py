"""
Machine Learning Prediction API Route Controller
Author: Ravi Ranjan Singh
"""

from src.ml.inference import CalorieInferenceEngine

calorie_engine = CalorieInferenceEngine()

def handle_calorie_prediction(payload: dict) -> dict:
    """
    Validates ingress biometric vector and executes ML calorie prediction.
    """
    # Validation checks
    required_fields = ["age", "gender", "height_cm", "weight_kg", "duration_min", "heart_rate_bpm", "body_temp_c"]
    for field in required_fields:
        if field not in payload:
            return {"status": "error", "message": f"Missing required parameter: '{field}'"}, 400

    # Bounds validation
    if not (10 <= float(payload["age"]) <= 100):
        return {"status": "error", "message": "Age must be between 10 and 100."}, 400
    if not (30.0 <= float(payload["heart_rate_bpm"]) <= 230.0):
        return {"status": "error", "message": "Heart rate must be between 30 and 230 BPM."}, 400

    prediction_result = calorie_engine.predict(payload)
    return {
        "status": "success",
        "data": prediction_result
    }, 200
