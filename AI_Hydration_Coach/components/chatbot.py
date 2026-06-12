from nicegui import ui
import asyncio
from services import get_ai_response, save_chat_history

class Chatbot:
    def __init__(self):
        # 預設對話紀錄
        self.messages = [
            {'role': 'ai', 'text': '嗨！我是你的飲水健康助手小滴～\n有任何關於飲水習慣或健康問題都可以問我喔！'}
        ]

    def render(self):
        """
        渲染聊天室主體與輸入框
        """
        with ui.column().classes('w-full h-full justify-between'):
            # 對話紀錄顯示區 (Scrollable)
            self.message_container = ui.column().classes('w-full flex-1 overflow-y-auto pr-2 space-y-4 no-wrap')
            with self.message_container:
                for msg in self.messages:
                    self.render_message(msg)
            
            # 使用者輸入區 (固定於底部)
            with ui.row().classes('w-full items-center gap-4 mt-4 bg-[#F8FBFF] p-2 rounded-xl'):
                self.text_input = ui.input(placeholder='跟小滴說點什麼...').classes('flex-1 text-lg').on('keydown.enter', self.send_message)
                self.text_input.props('rounded outlined')
                
                ui.button('Send', on_click=self.send_message).classes(
                    'bg-[#A8D8FF] hover:bg-[#85c4ff] text-white rounded-xl shadow-md px-6 py-2 font-bold'
                )
    
    def render_message(self, msg):
        """
        根據角色渲染單筆對話
        """
        is_user = msg['role'] == 'user'
        
        ui.chat_message(
            text=msg['text'],
            name='小滴' if not is_user else '你',
            stamp='剛剛',
            sent=is_user
        ).classes('w-full text-lg')

    async def send_message(self):
        """
        處理使用者傳送訊息的邏輯
        """
        text = self.text_input.value
        if not text:
            return
        
        # 清空輸入框
        self.text_input.value = ''
        
        # 1. 記錄並渲染使用者訊息
        user_msg = {'role': 'user', 'text': text}
        self.messages.append(user_msg)
        save_chat_history('user', text)
        
        with self.message_container:
            self.render_message(user_msg)
            
        # Optional: 捲動到底部 (NiceGUI 寫法)
        self.message_container.update()
            
        # 2. 獲取 AI 回應
        # 使用 asyncio.sleep 模擬 API 延遲
        await asyncio.sleep(0.5) 
        ai_text = get_ai_response(text)
        ai_msg = {'role': 'ai', 'text': ai_text}
        
        self.messages.append(ai_msg)
        save_chat_history('ai', ai_text)
        
        # 3. 渲染 AI 訊息
        with self.message_container:
            self.render_message(ai_msg)
            
        self.message_container.update()
            
    def add_system_message(self, text):
        """
        提供外部 (如按鈕) 呼叫，直接插入 AI 訊息
        """
        ai_msg = {'role': 'ai', 'text': text}
        self.messages.append(ai_msg)
        save_chat_history('ai', text)
        
        with self.message_container:
            self.render_message(ai_msg)
        self.message_container.update()
