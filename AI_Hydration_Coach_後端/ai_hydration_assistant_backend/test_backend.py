import unittest
from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient

# Add current folder to path if needed (FastAPI test execution context)
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from api_server import app
from models.hydration_data import HydrationData
from prompts.prompt_builder import PromptBuilder
from utils.hydration_calculator import (
    calculate_remaining_water,
    calculate_achievement_rate,
    calculate_achievement_percentage,
    estimate_recommended_next_drink
)

class TestHydrationCalculator(unittest.TestCase):
    def test_calculate_remaining_water(self):
        self.assertEqual(calculate_remaining_water(2400.0, 145.22), 2254.78)
        self.assertEqual(calculate_remaining_water(2400.0, 2500.0), 0.0)
        self.assertEqual(calculate_remaining_water(0.0, 100.0), 0.0)

    def test_calculate_achievement_rate(self):
        self.assertAlmostEqual(calculate_achievement_rate(2400.0, 145.22), 0.0605083, places=5)
        self.assertEqual(calculate_achievement_rate(0.0, 100.0), 0.0)

    def test_calculate_achievement_percentage(self):
        self.assertAlmostEqual(calculate_achievement_percentage(2400.0, 145.22), 6.05083, places=3)
        self.assertEqual(calculate_achievement_percentage(0.0, 100.0), 0.0)

    def test_estimate_recommended_next_drink(self):
        self.assertEqual(estimate_recommended_next_drink(0.0), 0.0)
        self.assertEqual(estimate_recommended_next_drink(-10.0), 0.0)
        self.assertEqual(estimate_recommended_next_drink(150.0), 150.0)
        self.assertEqual(estimate_recommended_next_drink(300.0), 300.0)
        self.assertEqual(estimate_recommended_next_drink(500.0), 250.0)

class TestHydrationDataModel(unittest.TestCase):
    def test_to_context_dict(self):
        data = HydrationData(
            target_water=2400.0,
            drank_water=145.22,
            remaining_water_from_firebase=3054.78,
            calculated_remaining_water=2254.78,
            temperature=32.3,
            humidity=56.0,
            steps=0,
            heart_rate=70,
            weight=60.0,
            last_sync="2026-06-02 12:06:22",
            timestamp=1780373183262
        )
        context = data.to_context_dict()
        
        self.assertEqual(context["targetWater"], 2400.0)
        self.assertEqual(context["drankWater"], 145.22)
        self.assertEqual(context["remainingWaterFromFirebase"], 3054.78)
        self.assertEqual(context["calculatedRemainingWater"], 2254.78)
        self.assertEqual(context["achievementRate"], 0.0605)
        self.assertEqual(context["achievementPercentage"], 6.05)
        self.assertEqual(context["temperature"], 32.3)
        self.assertEqual(context["humidity"], 56.0)
        self.assertEqual(context["steps"], 0)
        self.assertEqual(context["heartRate"], 70)
        self.assertEqual(context["weight"], 60.0)
        self.assertEqual(context["lastSync"], "2026-06-02 12:06:22")
        self.assertEqual(context["timestamp"], 1780373183262)

class TestPromptBuilder(unittest.TestCase):
    def test_build_system_prompt(self):
        sys_prompt = PromptBuilder.build_system_prompt()
        self.assertIn("AI Hydration Assistant", sys_prompt)
        self.assertIn("繁體中文", sys_prompt)

    def test_build_user_prompt(self):
        context = {
            "targetWater": 2400.0,
            "drankWater": 145.22,
            "remainingWaterFromFirebase": 3054.78,
            "calculatedRemainingWater": 2254.78,
            "achievementPercentage": 6.05,
            "temperature": 32.3,
            "humidity": 56.0,
            "steps": 0,
            "heartRate": 70,
            "weight": 60.0,
            "lastSync": "2026-06-02 12:06:22",
            "timestamp": 1780373183262
        }
        user_prompt = PromptBuilder.build_user_prompt("我今天還要喝多少水？", context)
        self.assertIn("使用者問題：", user_prompt)
        self.assertIn("我今天還要喝多少水？", user_prompt)
        self.assertIn("targetWater: 2400.0 mL", user_prompt)
        self.assertIn("drankWater: 145.22 mL", user_prompt)
        self.assertIn("calculatedRemainingWater: 2254.78 mL", user_prompt)

class TestAPIServer(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_health_check(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "AI Hydration Assistant API is running"})

    def test_ask_empty_question(self):
        # 1. Empty string validation (FastAPI level validation error / Pydantic parsing error)
        response = self.client.post("/ask", json={"question": ""})
        self.assertEqual(response.status_code, 422)

        # 2. Whitespace validation
        response = self.client.post("/ask", json={"question": "   "})
        self.assertEqual(response.status_code, 422)

    @patch("api_server.firebase_service")
    @patch("api_server.llm_service")
    def test_ask_success(self, mock_llm, mock_firebase):
        # Mock Firebase service response
        mock_data = HydrationData(
            target_water=2400.0,
            drank_water=145.0,
            remaining_water_from_firebase=2255.0,
            calculated_remaining_water=2255.0,
            temperature=30.0,
            humidity=50.0,
            steps=1000,
            heart_rate=72,
            weight=70.0,
            last_sync="2026-06-02 12:00:00",
            timestamp=1780373183000
        )
        mock_firebase.fetch_today_hydration_data.return_value = mock_data

        # Mock LLM service response
        mock_llm.ask_hydration_assistant.return_value = "你今天已經喝了 145 mL，還需要喝 2255 mL。"

        response = self.client.post("/ask", json={"question": "我今天還要喝多少水？"})
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"answer": "你今天已經喝了 145 mL，還需要喝 2255 mL。"})
        
        # Verify integrations were correctly triggered
        mock_firebase.fetch_today_hydration_data.assert_called_once()
        mock_llm.ask_hydration_assistant.assert_called_once_with(
            "我今天還要喝多少水？",
            mock_data.to_context_dict()
        )

    @patch("api_server.firebase_service")
    def test_get_history_success(self, mock_firebase):
        # Mock Firebase service response
        mock_data = HydrationData(
            target_water=2400.0,
            drank_water=145.0,
            remaining_water_from_firebase=2255.0,
            calculated_remaining_water=2255.0,
            temperature=30.0,
            humidity=50.0,
            steps=1000,
            heart_rate=72,
            weight=70.0,
            last_sync="2026-06-02 12:00:00",
            timestamp=1780373183000
        )
        mock_firebase.fetch_today_hydration_data.return_value = mock_data

        response = self.client.get("/api/history")
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            "current_ml": 145.0,
            "target_ml": 2400.0,
            "percentage": 6.04,
            "remaining_ml": 2255.0
        })
        mock_firebase.fetch_today_hydration_data.assert_called_once()

if __name__ == "__main__":
    unittest.main()
