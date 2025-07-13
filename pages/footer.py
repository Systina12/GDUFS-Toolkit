from nicegui import ui
from datetime import datetime

VERSION = "v1.4.0"
AUTHOR = "Systina12"
BUILD_DATE = "2025-07-13"

def add_footer():
    with ui.element('div').classes('w-full text-center text-sm text-gray-600 mt-8 px-4'):
        ui.separator().classes('my-2')
        ui.label(f'🔗 GitHub: https://github.com/Systina12/GDUFS-grade-ng').classes('select-text')
        ui.label(f' 作者: {AUTHOR}   |    🛠 版本: {VERSION}  |  构建日期: {BUILD_DATE}')