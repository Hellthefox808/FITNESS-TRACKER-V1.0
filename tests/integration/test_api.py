"""
Integration Test Suite for REST API Controllers
Author: Ravi Ranjan Singh
"""

import sys
import os
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.backend.main import dispatch_request

class TestAPIIntegration(unittest.TestCase):

    def test_health_check_endpoint(self):
        res, status = dispatch_request("GET", "/health")
        self.assertEqual(status, 200)
        self.assertEqual(res["status"], "healthy")

    def test_register_and_login_flow(self):
        # Register User
        reg_payload = {
            "email": "testuser@example.com",
            "password": "SecretPassword123!",
            "full_name": "Test User",
            "age": 30
        }
        res_reg, status_reg = dispatch_request("POST", "/api/v1/auth/register", reg_payload)
        self.assertEqual(status_reg, 201)
        self.assertEqual(res_reg["status"], "success")

        # Login User
        login_payload = {
            "email": "testuser@example.com",
            "password": "SecretPassword123!"
        }
        res_login, status_login = dispatch_request("POST", "/api/v1/auth/login", login_payload)
        self.assertEqual(status_login, 200)
        self.assertIn("access_token", res_login)

    def test_predict_calories_endpoint(self):
        predict_payload = {
            "age": 28,
            "gender": "female",
            "height_cm": 165.0,
            "weight_kg": 60.0,
            "duration_min": 30.0,
            "heart_rate_bpm": 145.0,
            "body_temp_c": 37.8
        }
        res, status = dispatch_request("POST", "/api/v1/predict/calories", predict_payload)
        self.assertEqual(status, 200)
        self.assertEqual(res["status"], "success")
        self.assertIn("predicted_calories_burned", res["data"])

    def test_workout_logging_endpoint(self):
        workout_payload = {
            "activity_type": "Cycling",
            "duration_min": 45.0,
            "calories_burned": 380.0,
            "avg_heart_rate_bpm": 142.0
        }
        res, status = dispatch_request("POST", "/api/v1/workouts", workout_payload)
        self.assertEqual(status, 201)
        self.assertIn("workout_id", res["data"])

if __name__ == "__main__":
    unittest.main()
