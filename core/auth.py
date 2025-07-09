import urllib.parse
from .session import session, url
from .captcha import recognize_captcha
from bs4 import BeautifulSoup
from .user import get_user_info

# 用于记录当前登录状态和缓存账号信息
cache_username = ''
cache_pwd = ''
login_flag = 1

def auto_reload():
    global cache_username, cache_pwd, login_flag
    if login_flag == 1 and cache_username and cache_pwd:
        success, _ = login(cache_username, cache_pwd)
        if success and get_user_info() != (None, None):
            return True
    return False

def login(username, password):
    headers ={
        'Cache-Control': 'max-age=0',
        'Sec-Ch-Ua': '',
        'Sec-Ch-Ua-Mobile': '?0',
        'Sec-Ch-Ua-Platform': '""',
        'Upgrade-Insecure-Requests': '1',
        'Origin': url,
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-User': '?1',
        'Sec-Fetch-Dest': 'document',
        'Referer': url + '/jsxsd/xk/LoginToXkLdap',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'close'
    } # 你之前的 loginHeader
    password = urllib.parse.quote(password)

    try:
        session.get(url + '/xk/LoginToXkLdap')
        response = session.get(url + '/verifycode.servlet')

        if response.status_code == 200:
            image = response.content
            captcha = recognize_captcha(image)
            body = f"USERNAME={username}&PASSWORD={password}&RANDOMCODE={captcha}"
            response = session.post(url + '/xk/LoginToXkLdap', headers=headers, data=body)

            if "<font color=\"red\">" in response.text:
                err = response.text.split("<font color=\"red\">")[1].split("</font>")[0]
                return False, err
            title = BeautifulSoup(response.text, "html.parser").title.string
            return True, title
    except Exception as e:
        return False, str(e)
