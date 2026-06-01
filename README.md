# SmartWaterSystem

AIoT 智慧飲水系統，結合生理與環境數據，為您量身打造最佳動態飲水計畫。

## Project Overview

此專案為 AIoT 智慧飲水系統。

透過：

- Apple HealthKit
- Weather API
- Firebase Realtime Database

即時取得：

- 步數
- 心率
- 體重
- 溫度
- 濕度

並動態計算每日建議飲水量（Target Water）。

--------------------------------------------------

## Features

- HealthKit 即時資料讀取
- Firebase 雲端同步
- Weather API 即時環境資料
- 動態飲水量計算
- SwiftUI Dashboard
- MVVM Architecture
- Real-time Data Bridge

--------------------------------------------------

## System Architecture

HealthKit
↓
DashboardViewModel
↓
WaterCalculator
↓
FirebaseManager
↓
Firebase Realtime Database

Weather API
↓
DashboardViewModel
↓
WaterCalculator
↓
FirebaseManager

--------------------------------------------------

## Technologies

- SwiftUI
- HealthKit
- Firebase Realtime Database
- Combine
- MVVM
- OpenWeather API
- Xcode
- iOS

--------------------------------------------------

## Water Calculation Formula

Base Water:
weight × 35 ml

Additional Rules:

- Every 1000 steps → +100 ml
- Temperature ≥ 30°C → +300 ml
- Temperature ≥ 35°C → additional +300 ml
- Humidity ≥ 80% → +200 ml
- Heart Rate ≥ 100 bpm → +300 ml
- Heart Rate ≥ 120 bpm → additional +300 ml

**Example:**
For an 80kg person (Base: 2800 ml) with 1000 steps (+100 ml), Temp 28.5°C (no bonus), Humidity 78% (no bonus), and HR 72 bpm (no bonus), the total Target Water is **2900 ml**.

--------------------------------------------------

## Firebase Data Structure

```json
{
  "health": {
    "today": {
      "steps": 1141,
      "heartRate": 72,
      "weight": 80,
      "temperature": 28.5,
      "humidity": 78,
      "targetWater": 2900,
      "lastSync": "2026-06-01 11:38:30",
      "timestamp": 1780284084852
    }
  }
}
```

--------------------------------------------------

## HealthKit Permissions

需要授權：

- Step Count
- Heart Rate
- Body Mass

--------------------------------------------------

## Installation

1. **Clone Repository**
   ```bash
   git clone https://github.com/ziyuli526/AIOT_ProjectProposal.git
   ```
2. **Firebase 設定**: 前往 Firebase Console 建立專案並開通 Realtime Database。
3. **GoogleService-Info.plist 放置位置**: 下載你的 `GoogleService-Info.plist`，並拖曳至 Xcode 專案導覽列的 `SmartWaterSystem` 目錄內（勾選 Copy items if needed）。
4. **HealthKit Capability 開啟**: 在 Xcode > Target > Signing & Capabilities 中新增 HealthKit。
5. **Team Signing 設定**: 選擇你的 Apple Developer Team。
6. **Run on Real Device**: 連接實體 iPhone 並 Build 專案（模擬器無法測試真實健康資料）。

--------------------------------------------------

## Demo

- [YouTube Demo Link](#)
--------------------------------------------------

## Demo Screenshots
*(Please replace these placeholders with actual screenshots of your app)*
- **Dashboard View**: `![Dashboard](link-to-image)`
- **Firebase Sync**: `![Firebase](link-to-image)`

--------------------------------------------------

## Future Extensions
- **Push Notifications**: Remind users to drink water when remaining water is high.
- **Apple Watch App**: Standalone watch app to sync heart rate in real-time.
- **Widget Support**: Home screen widget for quick water tracking.
- **Hardware Integration**: AIoT smart bottle to automatically log drank water.

--------------------------------------------------

## Authors

- Ziyu Li (及專題團隊成員)
