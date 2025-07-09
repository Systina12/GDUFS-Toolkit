import re
from bs4 import BeautifulSoup
from .session import session, url

def check():
    headers = {
        'Cache-Control': 'max-age=0',
        'Sec-Ch-Ua': '',
        'Sec-Ch-Ua-Mobile': '?0',
        'Sec-Ch-Ua-Platform': '""',
        'Upgrade-Insecure-Requests': '1',
        'Origin': 'https://jxgl.gdufs.edu.cn',
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Referer': f'{url}/kscj/cjcx_query',
        'Connection': 'close'
    }

    data = "kksj=&kcxz=&kcmc=&fxkc=0&xsfs=all"
    response = session.post(f'{url}/kscj/cjcx_list', headers=headers, data=data)
    soup = BeautifulSoup(response.text, 'lxml')

    text_block = soup.get_text(strip=True)
    main_gpa = re.search(r'主修课程平均学分绩点\s*([0-9.]+)', text_block)
    minor_gpa = re.search(r'辅修课程平均学分绩点\s*([0-9.]+)', text_block)
    gpa_text = f"主修课程平均学分绩点 {main_gpa.group(1) if main_gpa else 'N/A'} ,辅修课程平均学分绩点  {minor_gpa.group(1) if minor_gpa else 'N/A'}"

    names, urls = [], []
    for row in soup.select('table.Nsb_table tr'):
        tds = row.select('td')
        if len(tds) < 5:
            continue
        course_name = tds[3].text.strip()
        a_tag = tds[4].select_one('a[href*="pscj_list.do"]')
        if not a_tag:
            continue
        href = a_tag.get('href', '')
        try:
            path = href.split("JsMod('")[1].split("'")[0]
            names.append(course_name)
            urls.append(path)
        except IndexError:
            continue

    results = []
    for name, path in zip(names, urls):
        detail_resp = session.get(url.split('/jsxsd')[0] + path, headers=headers)
        detail_soup = BeautifulSoup(detail_resp.text, 'lxml')
        tds = detail_soup.select('td')
        row = [name] + [td.text.strip() for td in tds]
        results.append(row[:9])

    return results, gpa_text
