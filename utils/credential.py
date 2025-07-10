import json
import os

DEFAULT_CONFIG = {
    "username": "",
    "password": "",
    "autoLogin": 0,
    'use_cache':0
}
CONFIG_FILE = "config.json"

def save_config(config):
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=4, ensure_ascii=False)

# ✅ 自动创建配置文件（如果不存在）
def load_config():
    if not os.path.exists(CONFIG_FILE):
        save_config(DEFAULT_CONFIG)  # 自动新建
        return DEFAULT_CONFIG.copy()
    with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def set_auto_login_flag(enabled: bool):
    config = load_config()
    config["autoLogin"] = 1 if enabled else 0
    save_config(config)

def get_auto_login_flag() -> bool:
    config = load_config()
    return config.get("autoLogin", 0) == 1

def save_credentials(username: str, password: str):
    config = load_config()
    config["username"] = username
    config["password"] = password
    save_config(config)

def load_credentials():
    config = load_config()
    return config.get("username", ""), config.get("password", "")

