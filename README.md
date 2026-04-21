影片連結:https://youtu.be/NgHWAWfwU-o 


notebookLM:https://notebooklm.google.com/notebook/05a1b6b3-fbf8-4b4e-b2ec-efd07690463d






# 💧 Smart Hydration System
個人化智慧飲水系統（IoT + Health Data + Weather Integration）

---

## 📌 Overview
This project proposes a personalized smart hydration system that integrates IoT sensing, wearable health data, and real-time environmental information to provide adaptive hydration recommendations.

---

## 🎯 Motivation
- 人體約 50–70% 為水分  
- 脫水會影響電解質與器官功能  

### Existing Problems
- 依賴口渴（已經脫水）
- 手動記錄（低依從性）

👉 本系統將喝水轉為「數據驅動」

---

## 🧠 Key Features

### 1. Personalized Hydration
- 體重
- 心率（Apple Watch）
- 活動量（步數）
- 天氣（溫度 / 濕度）

---

### 2. Automatic Tracking (IoT)
- ESP32 + HX711 + Load Cell
- 自動記錄喝水量（無需手動）

---

### 3. Real-Time Feedback
- OLED 顯示
- App Dashboard
- 即時提醒

---

### 4. Context-Aware Adjustment
- 高溫 + 高心率 → 提高飲水量

---

## 🏗️ System Architecture

1. Data Collection  
   - HealthKit  
   - CWA API  

2. Decision Module  
   - 飲水計算  
   - 事件判斷  

3. Hardware  
   - Load Cell + HX711 + ESP32  

4. Feedback  
   - OLED + App  

---

## 📊 Hydration Model

### Target Water
TargetWater = BaseWater + WeatherAdj + ActivityAdj

- BaseWater = 體重 × 30–40 mL  

---

### Water Intake
DrankWater = Weight_before - Weight_after

- 1g ≈ 1mL  
- ΔWeight < ±2g（3秒）

---

### Event Detection
- 減少 → 喝水  
- 增加 → 補水  

---

## ⚙️ Hardware

| Component | Function |
|----------|--------|
| ESP32 | 控制 |
| HX711 | ADC |
| Load Cell | 重量 |
| OLED | 顯示 |

---

## 🔗 External Data

### Health
- Apple HealthKit

### Weather
- F-A0085-001（熱傷害）
- F-A0085-004（溫差）
- O-A0001-001（溫濕度）

---

## 🧪 Calibration

1. Tare  
2. 放砝碼  
3. 計算比例  
4. 寫入  
5. 驗證  

👉 誤差 < ±5g

---

## 🚀 Future Work
- Machine Learning
- AI 健康分析
- 行為預測

---

## 💡 Contribution
整合：
- 生理資料
- 環境資料
- IoT 感測

👉 實現「自動 + 個人化 + 即時」飲水管理

---

## 🏁 Summary
A data-driven IoT hydration system for intelligent health management.
