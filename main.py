from nicegui import ui
from pages.login import show_login_page
from pages.welcome import show_welcome
from pages.grades import grades_page
from pages.course import show_course
from pages.schedule import show_schedule
import threading
import webview

# 注册页面路由
ui.page('/')(show_login_page)
ui.page('/welcome')(show_welcome)
ui.page('/grades')(grades_page)
ui.page('/course')(show_course)
ui.page('/schedule')(show_schedule)

ui.run(port=24169)

# def start_nicegui():
#     # 启动 NiceGUI 服务器，但不自动打开浏览器
#     ui.run(
#         port=43127,
#         # reload=False,
#         # show=False  # 不自动打开浏览器
#     )
#
# # def start_gui():
# #     # 创建 webview 窗口
# #     webview.create_window('厂内工具箱', 'http://localhost:43127', width=1200, height=800)
# #     webview.start()
#
# if __name__ == '__main__':
#     # # 启动 NiceGUI 服务器线程
#     # threading.Thread(target=start_nicegui, daemon=True).start()
#     #
#     # # 启动 pywebview GUI
#     start_nicegui()
