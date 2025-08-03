import asyncio
from datetime import datetime
from nicegui import ui
from core import auth
from core.auth import auto_reload
from core.course import get_course
from core.user import get_user_info
from pages.footer import add_footer


def generate_semesters():
    current_year = datetime.now().year
    return [f'{y}-{s}' for y in range(current_year, current_year - 20, -1) for s in [1, 2]]


async def show_course():
    section_times = {
        1: "8:30 - 9:10", 2: "9:10 - 9:50", 3: "10:10 - 10:50", 4: "10:50 - 11:30",
        5: "11:35 - 12:15", 6: "12:30 - 13:10", 7: "13:10 - 13:50", 8: "14:00 - 14:40",
        9: "14:40 - 15:20", 10: "15:40 - 16:20", 11: "16:20 - 17:00", 12: "18:30 - 19:10",
        13: "19:10 - 19:50", 14: "20:00 - 20:40", 15: "20:40 - 21:20",
    }

    max_sections = max(section_times.keys())

    with ui.column().classes('w-full items-center p-4'):
        # 顶部标题 + 返回按钮



        def render_table(course_list, unarrange_course):
            table = [[[] for _ in range(7)] for _ in range(max_sections)]

            for course in course_list:
                weekday = course["星期"]
                sections = course.get('节次', [])
                for sec in sections:
                    if 1 <= sec <= max_sections and 1 <= weekday <= 7:
                        # 存储整个课程对象以便后续点击时弹出详情
                        table[sec - 1][weekday - 1].append(course)

            def show_detail(course):
                with ui.dialog().classes('fixed inset-0 flex items-center justify-center') as dialog, ui.card().classes('w-96'):
                    ui.label('📘 课程详情').classes('text-lg font-bold mb-2')
                    for key, value in course.items():
                        ui.label(f'{key}: {value}')
                    ui.button('关闭', on_click=dialog.close).classes('mt-2')
                dialog.open()

            table_area.clear()
            with table_area:
                if not course_list:
                    with ui.row().classes('w-full justify-center'):
                        ui.label('🙈 暂无课程信息').classes('text-gray-500 text-lg mt-2')
                    return

                with ui.element('table').classes(
                        'w-full border-collapse border border-gray-300 rounded shadow'
                ):
                    with ui.element('thead').classes('bg-gray-100'):
                        with ui.element('tr'):
                            with ui.element('th').classes('border p-2 text-center'):
                                ui.label('节次（时间）')
                            for i in range(1, 8):
                                with ui.element('th').classes('border p-2 text-center'):
                                    ui.label(f'星期{i}')
                    with ui.element('tbody'):
                        for i, row in enumerate(table):
                            with ui.element('tr'):
                                sec_num = i + 1
                                label = f'{sec_num}（{section_times.get(sec_num, "未知时间")}）'
                                with ui.element('td').classes('border p-2 text-center font-bold bg-gray-50'):
                                    ui.label(label)
                                for cell in row:
                                    with ui.element('td').classes(
                                            'border p-2 align-top text-sm text-center'
                                    ).style('min-width:120px'):
                                        if cell:
                                            for course in cell:
                                                display = f'{course.get("课程名", "未分配")}<br/>@{course.get("教室", "未分配")}'
                                                with ui.html(
                                                        f'<div style="padding:4px;border:1px solid #ddd;border-radius:6px;margin-bottom:4px;cursor:pointer;">{display}</div>'
                                                ).on('click', lambda e, c=course: show_detail(c)):
                                                    pass
                                        else:
                                            ui.html('')

                    # 加表尾展示未安排课程
                if unarrange_course:
                    with ui.element('div').classes(
                            'w-full p-4 text-sm text-left rounded bg-yellow-50 text-gray-800').style(
                            'margin-top:8px'):
                        ui.html(f'<b>未安排时间课程：</b> {unarrange_course}')


        async def handle_query_click(semester):
            # 异步执行 get_course，避免阻塞主线程
            course_data = await asyncio.to_thread(get_course, semester)
            render_table(*course_data)


        # 查询按钮
        with ui.row().classes('w-full justify-between items-center mb-4'):
            ui.label('📘 我的课程表').classes('text-3xl font-bold text-blue-700')
            ui.button('返回首页', on_click=lambda: ui.navigate.to('/welcome')).classes('text-md')

        with ui.row().classes('w-full justify-between items-center mb-4'):
            semester_select = ui.select(
                options=generate_semesters(),
                label='选择学年学期',
                value=None,
            ).classes('w-48')
            ui.button(
                '查询',
                on_click=lambda: handle_query_click(semester_select.value)
            ).classes('mt-2')

        table_area = ui.column().classes('w-full mt-4')

        # 初始渲染空表格
        render_table([],'')

        add_footer()