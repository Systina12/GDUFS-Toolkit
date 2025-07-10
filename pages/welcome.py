from nicegui import ui
from nicegui.functions.navigate import navigate

from core import auth
from core.user import get_user_info
from core.auth import auto_reload


from utils.credential import set_auto_login_flag

def show_welcome():
    def exit_onclick():
        auth.login_flag = 0
        set_auto_login_flag(False)
        navigate.to('/')

    info = get_user_info()

    if not info or info == (None, None):
        if auto_reload():
            ui.notify('⚠️ 登录信息已失效，已自动重新登录', type='warning')
        else:
            ui.notify('⚠️ 登录信息已失效，请手动重新登录', type='warning')
            auth.login_flag = 0

            ui.timer(3, lambda: navigate.to('/'))
            return

    name, student_id = info

    ui.element('div').classes('absolute inset-0 z-[-1]').style(
        'background: linear-gradient(135deg, #8EC5FC 0%, #E0C3FC 100%);'
    )

    with ui.column().classes('w-full h-screen items-center justify-start pt-20'):
        with ui.card().classes('bg-white/90 p-6 rounded-xl shadow-lg w-[90%] max-w-[800px]'):
            ui.label('与君初相识，犹如故人归。嗨，别来无恙啊！').classes('text-xl font-medium text-gray-700 mb-2')
            with ui.row().classes('items-center'):
                ui.label(f'👋 你好，{name}（{student_id}）').classes('text-2xl font-bold text-gray-900')
                ui.button('🚪 退出', on_click=exit_onclick).classes(
                    'ml-4 text-sm text-red-500 border border-red-400 rounded px-3 py-1 hover:bg-red-50'
                )

        ui.separator().classes('my-6')

        with ui.card().classes('bg-white/95 p-8 rounded-xl shadow-md w-[90%] max-w-[800px] text-center'):
            ui.label('📚 功能导航').classes('text-xl font-semibold text-gray-800 mb-4')

            with ui.row().classes('justify-center gap-4 flex-wrap'):
                ui.button('📄 temp', on_click=lambda: navigate.to('/schedule')).classes('w-40 h-14 text-lg')
                ui.button('📚 成绩查询', on_click=lambda: navigate.to('/grades')).classes('w-40 h-14 text-lg')
                ui.button('🗓️ 课表查询', on_click=lambda: navigate.to('/course')).classes('w-40 h-14 text-lg')
