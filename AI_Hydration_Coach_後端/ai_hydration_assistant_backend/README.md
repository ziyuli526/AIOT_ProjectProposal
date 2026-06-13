# AI Hydration Assistant Backend

This backend project acts as the logic layer for the **AIoT Personalized Smart Hydration System**. It receives user questions from the frontend, queries the latest IoT hydration and health metrics from Firebase Realtime Database, parses the data, constructs system and user prompts, calls the OpenAI API, and returns a friendly, concise, Traditional Chinese response designed for a mobile app or dashboard.

---

## Project Background
The system tracks water intake using IoT hardware (ESP32, Load Cell, HX711, LCD1602) and stores telemetry in Firebase Realtime Database. The backend enables conversational querying of this telemetry, giving the user intelligent insights based on physical metrics (steps, heart rate, temperature, etc.) and calculations.

---

## Setup Steps

### 1. Create a Virtual Environment
Navigate to the `ai_hydration_assistant_backend` directory and create a Python virtual environment:

```bash
# Create virtual environment
python -m venv venv

# Activate on Windows (PowerShell)
venv\Scripts\Activate.ps1

# Activate on Windows (CMD)
venv\Scripts\activate.bat

# Activate on macOS / Linux
source venv/bin/activate
```

### 2. Install Packages
Install the required packages:

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables
Copy `.env.example` to `.env`:

```bash
cp .env.example .env
```

Open `.env` and fill in your values:

```ini
OPENAI_API_KEY=your_openai_api_key_here
FIREBASE_DATABASE_URL=https://your-project-default-rtdb.asia-southeast1.firebasedatabase.app/
FIREBASE_SERVICE_ACCOUNT_PATH=./serviceAccountKey.json
LLM_MODEL=gpt-4.1-mini
```

### 4. Add Firebase Service Account Key
To query Firebase Realtime Database safely:
1. Go to the **Firebase Console**.
2. Select your project, navigate to **Project settings** (gear icon) -> **Service accounts**.
3. Click **Generate new private key** and download the JSON file.
4. Rename this file to `serviceAccountKey.json` and place it in the root of the project (`ai_hydration_assistant_backend/`).

> [!WARNING]
> Do not commit `serviceAccountKey.json` or `.env` to GitHub. They are already listed in `.gitignore`.

---

## Running the Server
Run the FastAPI application with Uvicorn:

```bash
uvicorn api_server:app --reload
```

By default, the server will start on `http://127.0.0.1:8000`.

---

## Testing the API

### 1. Health Check
Open your browser or run a GET request:

* **URL**: `http://127.0.0.1:8000/`
* **Expected JSON Response**:
  ```json
  {
    "message": "AI Hydration Assistant API is running"
  }
  ```

### 2. conversational Hydration Assistant Endpoint
Submit questions to the AI assistant using curl or any API client (e.g. Postman):

* **URL**: `POST http://127.0.0.1:8000/ask`
* **Headers**: `Content-Type: application/json`
* **Request Body**:
  ```json
  {
    "question": "我今天還要喝多少水？"
  }
  ```
* **Expected JSON Response**:
  ```json
  {
    "answer": "你今天的目標是 2400 mL，目前已喝 145 mL，還需要約 2255 mL。今天氣溫較高，建議接下來分幾次慢慢補充水分。"
  }
  ```

---

## Recommended Testing Questions
You can test the assistant with the following scenarios:
1. `我今天還要喝多少水？` (Checks calculated remaining water)
2. `我今天喝了多少？` (Checks current drinking volume)
3. `我今天喝夠了嗎？` (Evaluates progress against target)
4. `為什麼今天目標水量比較高？` (Looks at temperature/steps/humidity context)
5. `我現在應該喝多少？` (Triggers calculated recommendation: usually 250 mL or remaining)
6. `幫我生成今天的飲水報告。` (Asks for a summary of steps, temperature, and target)

---

## Frontend Integration Example
Below is a simple JavaScript snippet showing how the mobile app/dashboard fetches advice from this backend:

```javascript
fetch("http://127.0.0.1:8000/ask", {
  method: "POST",
  headers: {
    "Content-Type": "application/json"
  },
  body: JSON.stringify({
    question: "我今天還要喝多少水？"
  })
})
.then(response => response.json())
.then(data => {
  console.log("AI Response:", data.answer);
})
.catch(error => {
  console.error("Error connecting to backend:", error);
});
```
