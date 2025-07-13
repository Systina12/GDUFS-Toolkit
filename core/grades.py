import re
import time

from bs4 import BeautifulSoup
from .session import session, url
from core.cache import get_cache_flag, set_cache_flag, save_grades_cache, get_grades_cache
import asyncio
from concurrent.futures import ThreadPoolExecutor

def calc_gpa(score: float) -> float:
    score = float(score)
    if score >= 90:
        return 4.0
    elif score >= 85:
        return 3.7
    elif score >= 82:
        return 3.3
    elif score >= 78:
        return 3.0
    elif score >= 75:
        return 2.7
    elif score >= 71:
        return 2.3
    elif score >= 66:
        return 2.0
    elif score >= 62:
        return 1.7
    elif score > 60:
        return 1.3
    elif score == 60:
        return 1.0
    else:
        return 0.0



def check():
    headers = {
        'Cache-Control': 'max-age=0',
        'Sec-Ch-Ua': '',
        'Sec-Ch-Ua-Mobile': '?0',
        'Sec-Ch-Ua-Platform': '""',
        'Upgrade-Insecure-Requests': '1',
        'Origin': 'https://jxgl.gdufs.edu.cn',
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.5672.127 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Referer': f'{url}/kscj/cjcx_query',
        'Connection': 'close'
    }

    data = "kksj=&kcxz=&kcmc=&fxkc=0&xsfs=all"
    response = session.post(f'{url}/kscj/cjcx_list', headers=headers, data=data, verify=False)
    soup = BeautifulSoup(response.text, 'lxml')

    text_block = soup.get_text(strip=True)
    main_gpa = re.search(r'主修课程平均学分绩点\s*([0-9.]+)', text_block)
    minor_gpa = re.search(r'辅修课程平均学分绩点\s*([0-9.]+)', text_block)
    gpa_text = f"主修课程平均学分绩点 {main_gpa.group(1) if main_gpa else 'N/A'} ,辅修课程平均学分绩点  {minor_gpa.group(1) if minor_gpa else 'N/A'}"
    print(gpa_text)
    names, urls, scores, credits = [], [], [], []

    for row in soup.select('table.Nsb_table tr'):
        tds = row.select('td')
        if len(tds) < 6:
            continue

        course_name = tds[3].text.strip()
        total_score_tag = tds[4].select_one('a[href*="pscj_list.do"]')
        credit_text = tds[5].text.strip()  # 学分在第6列

        if not total_score_tag:
            continue

        href = total_score_tag.get('href', '')
        total_score = total_score_tag.text.strip()

        try:
            path = href.split("JsMod('")[1].split("'")[0]
            names.append(course_name)
            urls.append(path)
            scores.append(total_score)
            credits.append(credit_text)
        except IndexError:
            continue

    results = []

    # 加载缓存字典：课程名 → 成绩列表
    cache_data = {}
    if get_cache_flag():
        for row in get_grades_cache():
            if row and isinstance(row, list):
                course = row[0]
                cache_data[course] = row

    for name, path, score, credit in zip(names, urls, scores, credits):
        # 使用缓存且命中且总成绩一致 → 直接使用缓存
        if get_cache_flag() and name in cache_data:
            print("正在读取缓存")
            cached_row = cache_data[name]
            cached_score = cached_row[-2]  # 默认最后一项是总成绩
            if str(cached_score) == str(score):
                print(f'缓存命中 {cached_row}')
                results.append(cached_row)
                continue  # 跳过查询

        # 否则执行查询
        print(f"正在查询  {url.split('/jsxsd')[0] + path}")
        time.sleep(0.1)
        detail_resp = session.get(url.split('/jsxsd')[0] + path, headers=headers, verify=False)
        detail_soup = BeautifulSoup(detail_resp.text, 'lxml')
        tds = detail_soup.select('td')
        row = [name] + [td.text.strip() for td in tds]
        row=row[:9]
        row[1] = credit
        row.append(str(calc_gpa(score)))
        print(f"查询成功 {row}")

        results.append(row)  # 只保留前9项


    # 保存新缓存
    executor = ThreadPoolExecutor()
    # 在 check 函数中异步调用保存函数
    asyncio.get_event_loop().run_in_executor(executor, save_grades_cache, results)

    return results, gpa_text
