"""
Workout Logging API Controller
Author: Ravi Ranjan Singh
"""

import time
import uuid
from src.backend.core.database import db

def handle_log_workout(payload: dict) -> tuple:
    activity_type = payload.get("activity_type", "Running")
    duration_min = float(payload.get("duration_min", 30.0))
    calories_burned = float(payload.get("calories_burned", 250.0))
    avg_heart_rate = float(payload.get("avg_heart_rate_bpm", 140.0))
    
    workout_id = f"wrk_{uuid.uuid4().hex[:12]}"
    record = {
        "workout_id": workout_id,
        "activity_type": activity_type,
        "duration_min": duration_min,
        "calories_burned": calories_burned,
        "avg_heart_rate_bpm": avg_heart_rate,
        "logged_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    }
    
    db.workouts.append(record)
    
    return {
        "status": "success",
        "message": "Workout session logged successfully.",
        "data": record
    }, 201

def handle_get_workouts() -> tuple:
    return {
        "status": "success",
        "total": len(db.workouts),
        "data": db.workouts
    }, 200
