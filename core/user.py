import re
from bs4 import BeautifulSoup
from .session import session, url

def get_user_info():
    headers = {
        'Cache-Control': 'max-age=0',
        'Sec-Ch-Ua': '',
        'Sec-Ch-Ua-Mobile': '?0',
        'Sec-Ch-Ua-Platform': '""',
        'Upgrade-Insecure-Requests': '1',
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-User': '?1',
        'Sec-Fetch-Dest': 'document',
        'Connection': 'close'
    }

    page_url = f'{url}/framework/xsMain.jsp'
    response = session.get(page_url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    target_div = soup.find('div', id='Top1_divLoginName', class_='Nsb_top_menu_nc')

    if target_div:
        text = target_div.get_text(strip=True)
        match = re.search(r'([\u4e00-\u9fa5]+)\((\d+)\)', text)
        if match:
            return match.group(1), match.group(2)
    return None, None
