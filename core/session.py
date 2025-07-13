import requests

# urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
# hostname = "jxgl.gdufs.edu.cn"
#
# # 手动解析 IPv4 地址
# ip_address = socket.gethostbyname(hostname)
#
# url = f"https://{ip_address}/jsxsd"
session = requests.Session()
url = 'https://jxgl.gdufs.edu.cn/jsxsd'
