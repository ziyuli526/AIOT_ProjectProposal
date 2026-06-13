def calculate_remaining_water(target_water: float, drank_water: float) -> float:
    """
    Calculates remaining water to drink to reach the daily target.
    Ensures remaining water is never negative.
    """
    return max(target_water - drank_water, 0.0)

def calculate_achievement_rate(target_water: float, drank_water: float) -> float:
    """
    Calculates the drinking target achievement rate as a fraction of 1.
    If target water is 0 or less, returns 0.0.
    """
    if target_water <= 0.0:
        return 0.0
    return drank_water / target_water

def calculate_achievement_percentage(target_water: float, drank_water: float) -> float:
    """
    Calculates achievement rate percentage (0 - 100).
    """
    return calculate_achievement_rate(target_water, drank_water) * 100.0

def estimate_recommended_next_drink(remaining_water: float) -> float:
    """
    Estimates recommended intake amount for the next drink in mL.
    - If remaining is 0 or less: 0 mL
    - If remaining is 300 mL or less: remaining water
    - Otherwise: 250 mL
    """
    if remaining_water <= 0.0:
        return 0.0
    if remaining_water <= 300.0:
        return remaining_water
    return 250.0
