from nicegui import ui
from core.auth import login
from utils.credential import load_credentials, save_credentials, get_auto_login_flag, set_auto_login_flag
from nicegui.functions.navigate import navigate
from core.cache import set_cache_flag,get_cache_flag

def show_login_page():
    # 背景图层，覆盖整个页面
    ui.element('div').classes(
        'absolute inset-0 z-[-1]'
    ).style(
        'background: linear-gradient(135deg, #8EC5FC 0%, #E0C3FC 100%);'
    )

    ui.element('div').classes(
        'absolute inset-0 z-[-1] bg-black opacity-10'
    )

    with ui.row().classes('w-full h-screen justify-center items-center'):
        with ui.card().classes('w-[400px] shadow-lg p-8'):
            ui.label('🎓 教务系统登录').classes('text-2xl font-bold mb-6 text-center')

            saved_username, saved_password = load_credentials()
            username_input = ui.input('学号 / 用户名', value=saved_username).props('outlined').classes('mb-4 w-full')
            password_input = ui.input('密码', value=saved_password).props('outlined type=password').classes('mb-4 w-full')
            with ui.row().classes('items-center mb-2'):
                remember_password = ui.checkbox('记住密码').classes()
                ui.tooltip('勾选后账号密码会被保存在本地，下次登录时自动填充')
            with ui.row().classes('items-center mb-2'):
                auto_login = ui.checkbox('自动登录').classes()
                ui.tooltip('勾选后下次启动软件时将自动登录')
            with ui.row().classes('items-center mb-2'):
                use_cache = ui.checkbox('使用缓存加速访问', value=get_cache_flag()).classes()
                ui.tooltip('一般在校园网内无需启用，外网访问缓慢时才需要开启。开启后会将资源和部分查询结果存在本地，经过校验后直接输出，减少网络需求。')


            status_label = ui.label('').classes('text-red text-sm mb-2 text-center')

            # 自动登录函数，必须放在 status_label 定义之后！
            def autoLogin():
                for i in range(3):
                    username, password = load_credentials()
                    success, message = login(username, password)
                    if success:
                        ui.notify(f'✅ 登录成功：{message}', type='positive')
                        status_label.text = ''
                        navigate.to('/welcome')
                        return
                    else:
                        if message == "验证码错误!!":
                            message = "验证码自动识别出错，正在自动重试"
                        ui.notify(f'❌ 登录失败：{message}', type='negative')
                        status_label.text = f'错误：{message}'
                return

            def on_login():
                username = username_input.value.strip()
                password = password_input.value.strip()

                if not username or not password:
                    status_label.text = '⚠️ 请输入用户名和密码'
                    return

                status_label.text = '🔄 正在尝试登录...'

                success, message = login(username, password)

                if success:
                    ui.notify(f'✅ 登录成功：{message}', type='positive')
                    status_label.text = ''

                    if remember_password.value:
                        save_credentials(username, password)
                    if auto_login.value:
                        set_auto_login_flag(True)

                    set_cache_flag(use_cache.value)

                    navigate.to('/welcome')
                else:
                    if message == "验证码错误!!":
                        message = "验证码自动识别出错，请再次点击登录"
                    ui.notify(f'❌ 登录失败：{message}', type='negative')
                    status_label.text = f'错误：{message}'

            ui.button('登录', on_click=on_login).classes('w-full bg-primary text-white text-lg')

            # 页面加载完再判断是否自动登录（放在按钮之后）
            if get_auto_login_flag():
                autoLogin()