"""
Main Application Entry Point (FastAPI / WSGI Dispatcher)
Author: Ravi Ranjan Singh
"""

import sys
import os
from typing import Dict, Any

# Ensure project root is in sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.backend.core.config import settings
from src.backend.api.v1.auth import handle_register, handle_login
from src.backend.api.v1.predict import handle_calorie_prediction
from src.backend.api.v1.workouts import handle_log_workout, handle_get_workouts
from src.backend.api.v1.telemetry import process_telemetry_frame

def health_check() -> Dict[str, Any]:
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "environment": settings.ENVIRONMENT
    }

def dispatch_request(method: str, path: str, body: Dict[str, Any] = None) -> tuple:
    """Central router dispatcher for API requests."""
    method = method.upper()
    body = body or {}

    if path == "/health" or path == "/api/v1/health":
        return health_check(), 200

    if path == "/api/v1/auth/register" and method == "POST":
        return handle_register(body)

    if path == "/api/v1/auth/login" and method == "POST":
        return handle_login(body)

    if path == "/api/v1/predict/calories" and method == "POST":
        return handle_calorie_prediction(body)

    if path == "/api/v1/workouts":
        if method == "POST":
            return handle_log_workout(body)
        elif method == "GET":
            return handle_get_workouts()

    if path == "/api/v1/telemetry/stream" and method == "POST":
        return process_telemetry_frame(body), 200

    return {"status": "error", "message": f"Endpoint not found: {method} {path}"}, 404

# FastAPI App Exposure if fastapi is installed
try:
    from fastapi import FastAPI, HTTPException
    from fastapi.middleware.cors import CORSMiddleware
    
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.VERSION,
        description="AI-powered fitness tracking & calorie prediction backend service."
    )
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    @app.get("/health")
    def api_health():
        return health_check()
        
    @app.post("/api/v1/predict/calories")
    def api_predict(payload: dict):
        res, status_code = handle_calorie_prediction(payload)
        if status_code != 200:
            raise HTTPException(status_code=status_code, detail=res.get("message"))
        return res
        
except ImportError:
    app = None

if __name__ == "__main__":
    print(f"[{settings.PROJECT_NAME}] Starting local API server...")
    print(f"Health Check: {health_check()}")
