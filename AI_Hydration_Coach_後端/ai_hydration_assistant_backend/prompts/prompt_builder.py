class PromptBuilder:
    @staticmethod
    def build_system_prompt() -> str:
        """
        Builds the system prompt that defines constraints, personality, and instructions
        for the AI Hydration Assistant.
        """
        return (
            "你是一位可愛、溫柔、貼心的 AI 飲水小助手。你的任務是根據使用者的飲水量、目標水量、剩餘水量、天氣、心率與步數等資料，給出簡短且實用的喝水建議。\n"
            "1. 只能根據後端提供的資料回答，不要編造數據。\n"
            "2. 不提供醫療診斷或疾病判斷。\n"
            "3. 語氣要可愛、溫柔、有鼓勵感，但不要過度裝可愛。\n"
            "4. 可以提供一般補水建議，例如分次補水、避免一次喝太多。\n"
            "5. 回答請使用繁體中文。\n"
            "6. 如果資料不足，請誠實說明資料不足。\n"
            "8. 若 remainingWaterFromFirebase 與 calculatedRemainingWater 不一致，請以 calculatedRemainingWater 為準，不要主動提及資料不一致。\n"
            "9. 避免每次使用相同句型，請自然變化回覆方式。\n"
            "10. 可以適度使用 1～2 個 emoji，例如 💧、✨、🥤、🌤️，但不要太多。"
        )

    @staticmethod
    def build_user_prompt(question: str, context: dict) -> str:
        """
        Builds the user prompt including context data and user question.
        Handles missing fields in the context dictionary with safe defaults.
        """
        target_water = context.get("targetWater", 0)
        drank_water = context.get("drankWater", 0)
        rem_fb = context.get("remainingWaterFromFirebase", 0)
        rem_calc = context.get("calculatedRemainingWater", 0)
        ach_pct = context.get("achievementPercentage", 0)
        temp = context.get("temperature", 0)
        hum = context.get("humidity", 0)
        steps = context.get("steps", 0)
        hr = context.get("heartRate", 0)
        weight = context.get("weight", 0)
        last_sync = context.get("lastSync", "")

        return (
            f"使用者問題：\n"
            f"{question}\n\n"
            f"今日資料：\n"
            f"targetWater: {target_water} mL\n"
            f"drankWater: {drank_water} mL\n"
            f"remainingWaterFromFirebase: {rem_fb} mL\n"
            f"calculatedRemainingWater: {rem_calc} mL\n"
            f"achievementPercentage: {ach_pct} %\n"
            f"temperature: {temp} °C\n"
            f"humidity: {hum} %\n"
            f"steps: {steps}\n"
            f"heartRate: {hr} bpm\n"
            f"weight: {weight} kg\n"
            f"lastSync: {last_sync}\n\n"
            f"請根據以上資料回答使用者問題。\n"
            f"請優先使用 calculatedRemainingWater 作為剩餘需喝水量。"
        )
