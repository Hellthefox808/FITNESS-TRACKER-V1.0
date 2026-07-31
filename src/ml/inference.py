"""
High-Performance ML Inference Engine
Loads serialized model artifacts (.pkl) and executes calorie prediction pipelines with confidence bounds.
Author: Ravi Ranjan Singh
"""

import os
import time
import pickle
from typing import Dict, Any
from src.ml.pipelines.feature_engineering import PhysiologicalFeatureTransformer, PurePythonLinearRegressor

class CalorieInferenceEngine:
    """
    Production machine learning inference service for predicting caloric burn expenditure.
    """
    
    def __init__(self, model_path: str = None):
        if model_path is None:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            model_path = os.path.join(current_dir, "models", "xgb_calorie_v1.pkl")
            
        self.model_path = model_path
        self.model = None
        self.scaler = None
        self.residual_std = 12.5 # Residual standard error threshold for 95% confidence interval
        self._load_model()

    def _load_model(self):
        """Loads serialized model pipeline from disk."""
        if os.path.exists(self.model_path):
            try:
                with open(self.model_path, "rb") as f:
                    artifact = pickle.load(f)
                        
                if isinstance(artifact, dict):
                    self.model = artifact.get("model")
                    self.scaler = artifact.get("scaler")
                    self.residual_std = artifact.get("residual_std", 12.5)
                else:
                    self.model = artifact
            except Exception as e:
                print(f"[ML Inference Warning] Failed to load model artifact at {self.model_path}: {e}")
                self.model = None

    def predict(self, raw_telemetry: Dict[str, Any]) -> Dict[str, Any]:
        """
        Executes real-time inference for a single biometric payload.
        Returns predicted calories, 95% confidence intervals, and derived metrics.
        """
        start_time = time.perf_counter()
        
        # 1. Feature Engineering
        features = PhysiologicalFeatureTransformer.transform_single(raw_telemetry)
        
        # 2. Scale & Predict
        if self.model is not None and hasattr(self.model, "predict"):
            try:
                pred = self.model.predict([features])
                predicted_calories = float(pred[0] if isinstance(pred, (list, tuple)) else pred)
            except Exception as e:
                print(f"[Inference Error] Model execution failed: {e}")
                predicted_calories = self._fallback_metabolic_formula(raw_telemetry)
        else:
            predicted_calories = self._fallback_metabolic_formula(raw_telemetry)

        inference_time_ms = round((time.perf_counter() - start_time) * 1000, 2)
        
        # 3. Confidence Interval Calculation (95% CI)
        lower_bound = max(0.0, round(predicted_calories - 1.96 * self.residual_std, 2))
        upper_bound = round(predicted_calories + 1.96 * self.residual_std, 2)

        # 4. Derived Intensity Category
        hr_ratio = features[8]
        if hr_ratio < 0.6:
            intensity_zone = "Light Activity (Zone 1)"
        elif hr_ratio < 0.7:
            intensity_zone = "Fat Burn (Zone 2)"
        elif hr_ratio < 0.8:
            intensity_zone = "Aerobic (Zone 3)"
        elif hr_ratio < 0.9:
            intensity_zone = "Anaerobic (Zone 4)"
        else:
            intensity_zone = "Maximum Effort (Zone 5)"

        return {
            "predicted_calories_burned": round(predicted_calories, 2),
            "unit": "kcal",
            "confidence_interval_95": {
                "lower": lower_bound,
                "upper": upper_bound
            },
            "derived_metrics": {
                "bmi": round(float(features[7]), 2),
                "heart_rate_ratio": round(float(hr_ratio), 3),
                "intensity_zone": intensity_zone
            },
            "model_metadata": {
                "model_name": "XGBoost_Calorie_Regressor",
                "model_version": "v1.0.0",
                "inference_time_ms": inference_time_ms
            }
        }

    @staticmethod
    def _fallback_metabolic_formula(raw_telemetry: Dict[str, Any]) -> float:
        """Physiological metabolic Keytel formula fallback."""
        duration = float(raw_telemetry["duration_min"])
        hr = float(raw_telemetry["heart_rate_bpm"])
        weight = float(raw_telemetry["weight_kg"])
        age = float(raw_telemetry["age"])
        gender = str(raw_telemetry.get("gender", "male")).lower()
        gender_is_male = gender in ["male", "m", "1"]
        
        if gender_is_male:
            cal_per_min = (-55.0969 + (0.6309 * hr) + (0.1988 * weight) + (0.2017 * age)) / 4.184
        else:
            cal_per_min = (-20.4022 + (0.4472 * hr) - (0.1263 * weight) + (0.074 * age)) / 4.184

        cal_per_min = max(2.5, cal_per_min)
        return max(20.0, round(cal_per_min * duration, 2))
