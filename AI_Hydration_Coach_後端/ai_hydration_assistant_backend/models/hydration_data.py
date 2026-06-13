from dataclasses import dataclass
from utils.hydration_calculator import (
    calculate_achievement_rate,
    calculate_achievement_percentage
)

@dataclass
class HydrationData:
    target_water: float
    drank_water: float
    remaining_water_from_firebase: float
    calculated_remaining_water: float
    temperature: float
    humidity: float
    steps: int
    heart_rate: int
    weight: float
    last_sync: str
    timestamp: int

    @property
    def achievement_rate(self) -> float:
        """
        Calculates achievement rate (e.g., 0.0605 for 6.05%).
        """
        return calculate_achievement_rate(self.target_water, self.drank_water)

    @property
    def achievement_percentage(self) -> float:
        """
        Calculates achievement percentage (e.g., 6.05).
        """
        return calculate_achievement_percentage(self.target_water, self.drank_water)

    def to_context_dict(self) -> dict:
        """
        Returns a clean dictionary matching the frontend-friendly camelCase format.
        """
        return {
            "targetWater": self.target_water,
            "drankWater": self.drank_water,
            "remainingWaterFromFirebase": self.remaining_water_from_firebase,
            "calculatedRemainingWater": self.calculated_remaining_water,
            "achievementRate": round(self.achievement_rate, 4),
            "achievementPercentage": round(self.achievement_percentage, 2),
            "temperature": self.temperature,
            "humidity": self.humidity,
            "steps": self.steps,
            "heartRate": self.heart_rate,
            "weight": self.weight,
            "lastSync": self.last_sync,
            "timestamp": self.timestamp
        }
