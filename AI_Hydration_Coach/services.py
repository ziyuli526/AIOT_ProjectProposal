import requests

# 將這個變數換成你們實際的後端網址
BACKEND_URL = "http://172.20.10.4:8000"

def get_health_data():
    """
    向後端請求健康/飲水數據。
    如果後端還沒準備好對應的 API，會先回傳假資料以免畫面壞掉。
    """
    try:
        # 根據同學A的設定，路由是 /api/history
        response = requests.get(f"{BACKEND_URL}/api/history", timeout=2)
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        print(f"⚠️ 無法連接到後端取得健康數據: {e}")
        
    # 後端如果沒通或還沒寫好，就退回使用假資料
    return {
        'current_ml': 1500,
        'target_ml': 2000,
        'percentage': 75,
        'remaining_ml': 500
    }

def get_ai_response(user_message: str) -> str:
    """
    將使用者的訊息傳給後端，由後端呼叫 GPT API 後回傳結果。
    """
    try:
        # 配合後端要求：路由是 /ask，欄位是 {"question": "..."}
        payload = {"question": user_message}
        response = requests.post(f"{BACKEND_URL}/ask", json=payload, timeout=5)
        
        if response.status_code == 200:
            # 配合後端要求：回傳的答案放在 {"answer": "..."} 裡面
            data = response.json()
            return data.get("answer", "後端有回傳，但沒有找到 'answer' 欄位喔！")
        else:
            return f"後端回傳了錯誤代碼: {response.status_code}"
            
    except Exception as e:
        print(f"⚠️ 無法連接到後端取得 AI 回應: {e}")
        return "（後端連線失敗）小滴剛剛打盹了，沒有連上伺服器喔！"

def save_chat_history(role: str, message: str):
    """
    將聊天紀錄傳給後端，由後端去存入 Firebase 或資料庫。
    """
    try:
        payload = {"role": role, "message": message}
        # 假設後端有一個 /api/history 的路由
        requests.post(f"{BACKEND_URL}/api/history", json=payload, timeout=2)
    except Exception as e:
        print(f"⚠️ 歷史紀錄儲存失敗: {e}")
