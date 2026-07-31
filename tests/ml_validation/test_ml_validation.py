"""
ML Model Validation & Accuracy Benchmark Test Suite
Author: Ravi Ranjan Singh
"""

import sys
import os
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.ml.inference import CalorieInferenceEngine

class TestMLModelValidation(unittest.TestCase):

    def setUp(self):
        self.engine = CalorieInferenceEngine()

    def test_model_artifact_loaded(self):
        self.assertIsNotNone(self.engine.model, "ML model artifact was not loaded properly")

    def test_model_benchmark_accuracy_and_bounds(self):
        holdout_cases = [
            {"age": 20, "gender": "male", "height_cm": 180.0, "weight_kg": 80.0, "duration_min": 60.0, "heart_rate_bpm": 160.0, "body_temp_c": 38.5},
            {"age": 45, "gender": "female", "height_cm": 160.0, "weight_kg": 55.0, "duration_min": 30.0, "heart_rate_bpm": 130.0, "body_temp_c": 37.5},
            {"age": 35, "gender": "male", "height_cm": 175.0, "weight_kg": 72.0, "duration_min": 45.0, "heart_rate_bpm": 150.0, "body_temp_c": 38.0}
        ]

        for case in holdout_cases:
            res = self.engine.predict(case)
            pred = res["predicted_calories_burned"]
            ci = res["confidence_interval_95"]
            
            self.assertGreater(pred, 50.0, f"Calorie prediction {pred} unrealistically low for active session")
            self.assertLess(pred, 1500.0, f"Calorie prediction {pred} unrealistically high")
            self.assertLessEqual(ci["lower"], pred)
            self.assertGreaterEqual(ci["upper"], pred)

if __name__ == "__main__":
    unittest.main()
