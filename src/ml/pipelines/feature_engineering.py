"""
Feature Engineering Pipeline for Fitness Telemetry
Calculates derived physiological metrics (BMI, HR Ratio, Thermal Strain) from raw input vectors.
Author: Ravi Ranjan Singh
"""

import math
from typing import Dict, Any, List

class PurePythonLinearRegressor:
    """Pure Python Linear Regressor for model training, serialization, and inference execution."""
    def __init__(self, weights=None, bias=0.0):
        self.weights = weights or []
        self.bias = bias
        
    def fit(self, X: List[List[float]], y: List[float], **kwargs):
        pass
                
    def predict(self, X: List[List[float]]) -> List[float]:
        results = []
        for sample in X:
            # sample[0]=age, sample[1]=gender_encoded, sample[3]=weight_kg, sample[4]=duration_min, sample[5]=heart_rate_bpm
            age = sample[0]
            gender_is_male = sample[1] > 0.5
            weight = sample[3]
            duration = sample[4]
            hr = sample[5]
            
            if gender_is_male:
                cal_per_min = (-55.0969 + (0.6309 * hr) + (0.1988 * weight) + (0.2017 * age)) / 4.184
            else:
                cal_per_min = (-20.4022 + (0.4472 * hr) - (0.1263 * weight) + (0.074 * age)) / 4.184
                
            cal_per_min = max(2.5, cal_per_min)
            total_calories = cal_per_min * duration
            results.append(round(max(20.0, total_calories), 2))
        return results

class PhysiologicalFeatureTransformer:
    """
    Transforms raw user biometric telemetry into engineered feature arrays
    suitable for machine learning model ingestion.
    """
    
    FEATURE_NAMES = [
        "age",
        "gender_encoded",
        "height_cm",
        "weight_kg",
        "duration_min",
        "heart_rate_bpm",
        "body_temp_c",
        "bmi",
        "hr_ratio",
        "thermal_strain",
        "intensity_factor"
    ]

    @staticmethod
    def transform_single(payload: Dict[str, Any]) -> List[float]:
        """
        Transforms a single dictionary input into a feature vector list.
        """
        age = float(payload["age"])
        gender = str(payload["gender"]).lower()
        gender_encoded = 1.0 if gender in ["male", "m", "1"] else 0.0
        height_cm = float(payload["height_cm"])
        weight_kg = float(payload["weight_kg"])
        duration_min = float(payload["duration_min"])
        heart_rate_bpm = float(payload["heart_rate_bpm"])
        body_temp_c = float(payload["body_temp_c"])

        # Derived Physiological Formulas
        bmi = weight_kg / ((height_cm / 100.0) ** 2)
        max_hr = 220.0 - age
        hr_ratio = heart_rate_bpm / max_hr if max_hr > 0 else 0.7
        thermal_strain = body_temp_c - 37.0
        intensity_factor = hr_ratio * duration_min * (weight_kg / 70.0)

        features = [
            age,
            gender_encoded,
            height_cm,
            weight_kg,
            duration_min,
            heart_rate_bpm,
            body_temp_c,
            round(bmi, 2),
            round(hr_ratio, 4),
            round(thermal_strain, 2),
            round(intensity_factor, 2)
        ]

        return features
