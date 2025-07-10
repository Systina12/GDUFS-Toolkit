from nicegui import ui

from pages.footer import add_footer


def show_schedule():
    with ui.row().classes('w-full min-h-60 items-center justify-center'):
        with ui.column().classes('items-center'):
            ui.icon('construction').classes('text-8xl text-yellow-600')
            ui.label('🚧 功能正在开发中，敬请期待！').classes('text-4xl mt-4 text-center')
            ui.label('如遇到问题请在Github提交Issue').classes('mt-2 text-center')
            ui.button('返回首页', on_click=lambda: ui.navigate.to('/welcome')).classes('mt-6 w-40 h-14 text-lg')


    add_footer()