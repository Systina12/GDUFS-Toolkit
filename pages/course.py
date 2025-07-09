from nicegui import ui

def show_course():
    with ui.row().classes('w-full h-screen items-center justify-center'):
        with ui.column().classes('items-center'):
            ui.icon('construction').classes('text-6xl text-yellow-600')
            ui.label('🚧 功能正在开发中，敬请期待！').classes('text-2xl mt-4 text-center')
            ui.button('返回首页', on_click=lambda: ui.navigate.to('/welcome')).classes('mt-6 w-40 h-14 text-lg')
