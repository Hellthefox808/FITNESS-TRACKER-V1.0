"""
Real-Time Telemetry & WebSockets Streaming Controller
Author: Ravi Ranjan Singh
"""

from src.ml.inference import CalorieInferenceEngine

calorie_engine = CalorieInferenceEngine()

def process_telemetry_frame(frame: dict) -> dict:
    """
    Processes 1 Hz wearable telemetry frame and returns dynamic burn velocity.
    """
    heart_rate = float(frame.get("heart_rate_bpm", 140.0))
    body_temp = float(frame.get("body_temp_c", 38.0))
    weight = float(frame.get("weight_kg", 75.0))
    age = int(frame.get("age", 28))
    gender = frame.get("gender", "male")
    duration = float(frame.get("duration_min", 1.0))

    prediction = calorie_engine.predict({
        "age": age,
        "gender": gender,
        "height_cm": 175.0,
        "weight_kg": weight,
        "duration_min": duration,
        "heart_rate_bpm": heart_rate,
        "body_temp_c": body_temp
    })

    burn_rate_per_min = round(prediction["predicted_calories_burned"] / max(1.0, duration), 2)

    return {
        "event": "BURN_VELOCITY_UPDATE",
        "current_heart_rate_bpm": heart_rate,
        "burn_rate_kcal_per_min": burn_rate_per_min,
        "cumulative_calories": prediction["predicted_calories_burned"],
        "intensity_zone": prediction["derived_metrics"]["intensity_zone"]
    }
