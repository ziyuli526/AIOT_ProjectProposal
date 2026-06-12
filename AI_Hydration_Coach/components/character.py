from nicegui import ui

@ui.refreshable
def render_character(health_data: dict):
    """
    渲染左側角色區塊
    """
    with ui.card().classes('w-full rounded-xl shadow-md bg-white items-center p-8'):
        # 根據達成率動態判斷狀態與圖片
        percentage = health_data.get('percentage', 0)
        if percentage >= 100:
            status_text = '水分充足 ✨'
            color_class = 'text-[#5A8DFF]'
            img_src = '/assets/avatar_100.png'
        elif percentage >= 50:
            status_text = '繼續保持 💧'
            color_class = 'text-green-500'
            img_src = '/assets/avatar_50.png'
        else:
            status_text = '口渴缺水中 🌵'
            color_class = 'text-red-500'
            img_src = '/assets/avatar_0.png'

        # 角色圖片
        ui.image(img_src).classes('w-40 h-40 rounded-full mb-6 shadow-sm')
        
        # 角色名稱
        ui.label('小滴').classes('text-3xl font-bold text-gray-800 mb-4')
        
        # 狀態標籤
        with ui.row().classes('items-center bg-[#EAF6FF] px-6 py-3 rounded-full'):
            ui.label(f'今日狀態：{status_text}').classes(f'{color_class} font-medium text-lg')
