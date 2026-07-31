"""
Unit Test Suite for Machine Learning Inference Engine
Author: Ravi Ranjan Singh
"""

import sys
import os
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.ml.inference import CalorieInferenceEngine
from src.ml.pipelines.feature_engineering import PhysiologicalFeatureTransformer

class TestMLInferenceEngine(unittest.TestCase):

    def setUp(self):
        self.engine = CalorieInferenceEngine()
        self.sample_telemetry = {
            "age": 28,
            "gender": "male",
            "height_cm": 178.0,
            "weight_kg": 75.5,
            "duration_min": 45.0,
            "heart_rate_bpm": 154.0,
            "body_temp_c": 38.1
        }

    def test_feature_transformation_vector(self):
        features = PhysiologicalFeatureTransformer.transform_single(self.sample_telemetry)
        self.assertEqual(len(features), 11)
        self.assertEqual(features[0], 28.0) # Age
        self.assertEqual(features[1], 1.0)  # Gender encoded male
        self.assertAlmostEqual(features[7], 23.83, delta=0.1) # BMI

    def test_inference_prediction_bounds(self):
        result = self.engine.predict(self.sample_telemetry)
        
        self.assertIn("predicted_calories_burned", result)
        self.assertGreater(result["predicted_calories_burned"], 0.0)
        self.assertIn("confidence_interval_95", result)
        self.assertLessEqual(result["confidence_interval_95"]["lower"], result["predicted_calories_burned"])
        self.assertGreaterEqual(result["confidence_interval_95"]["upper"], result["predicted_calories_burned"])

    def test_latency_sub_50ms(self):
        result = self.engine.predict(self.sample_telemetry)
        latency = result["model_metadata"]["inference_time_ms"]
        self.assertLess(latency, 50.0, f"Inference latency {latency}ms exceeded 50ms requirement")

if __name__ == "__main__":
    unittest.main()
