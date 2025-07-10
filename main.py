import socket

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


# ui.run(port=24169)



####webview打包代码
def find_free_port():
    """获取系统随机空闲端口"""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', 0))  # 绑定 0 表示系统自动分配
    port = s.getsockname()[1]
    s.close()
    return port

# 获取空闲端口
free_port = find_free_port()

def start_nicegui():
    ui.run(
        port=free_port,
        reload=False,
        show=False  # 不自动打开浏览器
    )

def start_gui():
    webview.create_window('厂内工具箱', f'http://localhost:{free_port}', width=1200, height=800)
    webview.start()

if __name__ == '__main__':
    threading.Thread(target=start_nicegui, daemon=True).start()
    start_gui()
