from nicegui import ui
from nicegui.functions.navigate import navigate
from core.auth import auto_reload
from core import auth
from core.grades import check
from core.user import get_user_info


def grades_page():
    ui.label('📚 成绩查询结果').classes('text-2xl font-bold my-4')



    content = ui.column().classes('items-center w-full')


    def load_data():
        info = get_user_info()
        if not info or info == (None, None):
            if auto_reload():
                ui.notify('⚠️ 登录信息已失效，已自动重新登录', type='warning')
            else:
                ui.notify('⚠️ 登录信息已失效，请手动重新登录', type='warning')
                auth.login_flag = 0
                ui.timer(3, lambda: navigate.to('/'))
                return
        content.clear()
        try:
            result, gpa = check()
        except Exception as e:
            ui.notify(f'查询失败：{e}', type='negative')
            return

        if not result:
            ui.label('未查到成绩数据').classes('text-lg text-gray-600')
            return

        with content:
            with ui.row().classes('mt-6 gap-4'):
                ui.button('返回', on_click=lambda: navigate.to('/welcome'))
                ui.button('刷新', on_click=load_data)

            ui.label(gpa).classes('text-lg text-gray-700 mb-4')

            headers = [
                "课程名", "序号", "平时成绩", "平时成绩比例",
                "期中成绩", "期中成绩比例", "期末成绩", "期末成绩比例", "总成绩"
            ]

            ui.table(
                columns=[{'name': h, 'label': h, 'field': h, 'sortable': False} for h in headers],
                rows=[dict(zip(headers, row)) for row in result],
                row_key='课程名'
            ).classes('w-full max-w-[1200px] mx-auto')

    load_data()

