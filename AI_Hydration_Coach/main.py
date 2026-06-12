from nicegui import ui, app
from components.character import render_character
from components.dashboard import render_dashboard
from components.chatbot import Chatbot
from services import get_health_data

# 掛載靜態資源資料夾
app.add_static_files('/assets', 'assets')

# 全局樣式設定 (背景色與字體)
ui.query('body').classes('bg-[#F8FBFF] m-0 p-0 text-gray-800')

def show_daily_analysis(chatbot_instance: Chatbot, current_data: dict):
    """
    右上角「今日分析」按鈕執行的函式
    """
    remaining = current_data['remaining_ml']
    
    # 根據剩餘水量動態給予不同的鼓勵語
    if remaining <= 0:
        cheer_msg = "恭喜你！今天的水分目標已經達成囉！ 🎉"
    elif remaining <= 600:
        cheer_msg = "繼續保持喔！再喝一兩杯水就達標了！ 💪"
    elif remaining <= 1500:
        cheer_msg = "已經喝了不少囉！工作/讀書之餘別忘了多補充水分！ 🍵"
    else:
        cheer_msg = "今天喝得有點少喔！趕快先去裝一大杯水吧！ 💧"

    analysis_text = (
        f"📊 【今日分析】\n\n"
        f"今日飲水量：{current_data['current_ml']} ml\n"
        f"目標飲水量：{current_data['target_ml']} ml\n"
        f"目前完成 {current_data['percentage']}%\n"
        f"距離目標還差 {remaining} ml\n\n"
        f"{cheer_msg}"
    )
    chatbot_instance.add_system_message(analysis_text)

@ui.page('/')
def main_page():
    # 使用一個字典來保存狀態，這樣才能在定時器內動態更新它
    state = {'health_data': get_health_data()}
    chatbot = Chatbot()

    # 定義定時更新資料的邏輯
    def update_data():
        state['health_data'] = get_health_data()
        # 呼叫 refresh() 讓 UI 局部重新渲染
        render_dashboard.refresh(state['health_data'])
        render_character.refresh(state['health_data'])
        
    # 設定每 5 秒自動去後端抓一次資料並更新畫面！
    ui.timer(5.0, update_data)

    # ====== 頂部 Header 區塊 ======
    with ui.row().classes('w-full justify-between items-center px-8 py-4 bg-white shadow-sm'):
        ui.label('AI Hydration Coach').classes('text-2xl font-bold text-[#A8D8FF]')
        ui.button(
            '📊 今日分析', 
            on_click=lambda: show_daily_analysis(chatbot, state['health_data'])
        ).classes('bg-[#EAF6FF] text-[#5A8DFF] font-bold rounded-xl shadow-md px-6 py-2')

    # ====== 主畫面 Layout ======
    # 設定高度填滿螢幕 (扣除 header)，左右佔比大約是 3:9
    with ui.row().classes('w-full max-w-7xl mx-auto p-6 gap-6 items-stretch h-[calc(100vh-90px)] wrap-none'):
        
        # 左側區域：AI 角色 (約佔寬度 1/4)
        with ui.column().classes('w-1/4 min-w-[280px] h-full'):
            render_character(state['health_data'])

        # 右側區域：Dashboard 與 Chatbot (約佔寬度 3/4)
        with ui.column().classes('flex-1 h-full'):
            # 1. 頂部 Dashboard
            render_dashboard(state['health_data'])
            
            # 2. 下方 聊天介面
            # 使用 flex-1 讓聊天室自動填滿剩下的高度
            with ui.card().classes('w-full flex-1 rounded-xl shadow-md bg-white p-6 flex flex-col min-h-0'):
                chatbot.render()

if __name__ in {"__main__", "__mp_main__"}:
    # 啟動 NiceGUI
    ui.run(title='AI Hydration Coach', port=8080, language='zh-TW')
