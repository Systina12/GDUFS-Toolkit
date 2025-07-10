import json
import re
from core.session import session,url
from bs4 import BeautifulSoup


query_url=url+'/xskb/xskb_list.do?Ves632DSdyV=NEW_XSD_PYGL'

def get_course(semester):
    header = {
        "Cache-Control": "max-age=0",
        "Origin": "https://jxgl.gdufs.edu.cn",
        "Content-Type": "application/x-www-form-urlencoded",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Referer": "https://jxgl.gdufs.edu.cn/jsxsd/xskb/xskb_list.do?Ves632DSdyV=NEW_XSD_PYGL",
        "Accept-Encoding": "gzip, deflate",  # requests 自动支持 gzip 解码
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "close"
    }

    if semester != None:
        xnxq01id = semester.split('-')[0] + '-' + str(int(semester.split('-')[0]) + 1) +'-'+ semester.split('-')[1]
    else:
        return []
    data = {
        "bodycj0701id": "",
        "zc": "",
        "demo": "",
        "xnxq01id": xnxq01id,
        "sfFD": "1"
    }
    resp=session.post(query_url, headers=header, data=data, verify=False)
    soup = BeautifulSoup(resp.text, 'html.parser')
    font_tag = soup.find('font', string='未安排时间课程：', attrs={'color': 'red'})
    unarrange_course = ''
    if font_tag and font_tag.next_sibling:
        unarrange_course = font_tag.next_sibling.strip()

    divs = soup.find_all('div', id=re.compile(r'.*-2$'))

    def parse_sections(section_str):
        """将节次字符串转为整数数组，如 01-02-03 -> [1, 2, 3]"""
        section_str = section_str.replace('节', '')
        parts = section_str.split('-')
        return [int(p.lstrip('0') or '0') for p in parts]

    results = []

    for div in divs:
        if div.decode_contents()!=" ":
            result = {}
            div_id=div.get("id")
            div_contents = div.decode_contents()

            result['课程名']=div_contents.split('<')[0]
            pattern = r'<font\s+title="(.*?)">(.*?)</font>'
            matches = re.findall(pattern, div_contents, re.DOTALL)


            for title, content in matches:
                clean_content = re.sub(r'<br\s*/?>', '', content).strip()

                if title == '周次(节次)':
                    # 提取周次，如 1-16(周)
                    week_match = re.search(r'([\d\-]+)\(周\)', clean_content)
                    # 提取节次，如 [01-02节]
                    section_match = re.search(r'\[([\d\-]+)节]', clean_content)


                    if week_match:
                        result['周次'] = week_match.group(1)  # 保持字符串格式，如 '1-16'
                    if section_match:
                        section_str = section_match.group(1)  # 如 '01-02'
                        result['节次'] = parse_sections(section_str)  # 转换为 [1, 2]
                else:
                    result[title] = clean_content

            weekday_match = re.search(r'-([1-7])-2$', div_id)
            weekday = int(weekday_match.group(1)) if weekday_match else None
            result['星期'] = weekday
            results.append(result)

    results = list({json.dumps(r, sort_keys=True): r for r in results}.values())
    return results,unarrange_course