from nicegui import ui

@ui.refreshable
def render_dashboard(health_data: dict):
    """
    渲染右側上方的統計卡片區塊
    """
    with ui.row().classes('w-full justify-between gap-4 mb-4'):
        # Card 1: 今日飲水量
        with ui.card().classes('flex-1 rounded-xl shadow-md bg-white p-6'):
            ui.label('今日飲水量').classes('text-gray-500 text-sm mb-2')
            ui.label(f"{health_data['current_ml']} ml").classes('text-3xl font-bold text-[#A8D8FF]')

        # Card 2: 達成率
        with ui.card().classes('flex-1 rounded-xl shadow-md bg-white p-6'):
            ui.label('達成率').classes('text-gray-500 text-sm mb-2')
            ui.label(f"{health_data['percentage']}%").classes('text-3xl font-bold text-[#A8D8FF]')

        # Card 3: 剩餘飲水量
        with ui.card().classes('flex-1 rounded-xl shadow-md bg-white p-6'):
            ui.label('剩餘飲水量').classes('text-gray-500 text-sm mb-2')
            ui.label(f"{health_data['remaining_ml']} ml").classes('text-3xl font-bold text-[#A8D8FF]')
