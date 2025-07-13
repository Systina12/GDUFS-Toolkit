from nicegui import ui
from nicegui.functions.navigate import navigate
from core.auth import auto_reload
from core import auth
from core.grades import check
from core.user import get_user_info
import asyncio

from pages.footer import add_footer


def grades_page():
    async def load_data():
        overlay_spinner.visible = True
        await asyncio.sleep(0.1)  # 等待 UI 完整渲染

        info = get_user_info()
        if not info or info == (None, None):
            overlay_spinner.visible = False
            if auto_reload():
                with content:
                    ui.notify('⚠️ 登录信息已失效，已自动重新登录', type='warning')
            else:
                with content:
                    ui.notify('⚠️ 登录信息已失效，请手动重新登录', type='warning')
                    auth.login_flag = 0
                    ui.timer(3, lambda: navigate.to('/'))
                    return

        try:
            result, gpa = check()
        except Exception as e:
            overlay_spinner.visible = False
            with content:
                with ui.row().classes('mt-6 gap-4'):
                    ui.button('返回', on_click=lambda: navigate.to('/welcome'))
                    # ui.button('刷新', on_click=lambda: asyncio.create_task(load_data()))
                ui.notify(f'查询失败：{e}', type='negative')
            return

        content.clear()
        overlay_spinner.visible = False

        with content:
            with ui.row().classes('mt-6 gap-4'):
                ui.button('返回', on_click=lambda: navigate.to('/welcome'))
                # ui.button('刷新', on_click=lambda: asyncio.create_task(load_data()))

            ui.label(gpa).classes('text-lg text-gray-700 mb-4')

            headers = [
                "课程名", "学分", "平时成绩", "平时成绩比例",
                "期中成绩", "期中成绩比例", "期末成绩", "期末成绩比例", "总成绩", "绩点"
            ]

            ui.table(
                columns=[{'name': h, 'label': h, 'field': h, 'sortable': False} for h in headers],
                rows=[dict(zip(headers, row)) for row in result],
                row_key='课程名'
            ).classes('w-full max-w-[1200px] mx-auto')

    # 页面标题
    ui.label('📚 成绩查询结果').classes('text-2xl font-bold my-4')

    # 内容容器
    with ui.column().classes('w-full') as container:
        content = ui.column().classes('items-center w-full')

    # 全屏加载动画
    with ui.column().classes(
        'fixed top-0 left-0 w-screen h-screen items-center justify-center z-50 bg-white/60'
    ) as overlay_spinner:
        ui.spinner(size='xl', color='primary')
        ui.label('正在加载成绩数据...').classes('text-gray-600 mt-2 text-lg')

    # 启动加载
    asyncio.create_task(load_data())

    add_footer()