import json
from utils.credential import CONFIG_FILE

def save_config(config):
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=4, ensure_ascii=False)

# 自动创建配置文件（如果不存在）
def load_config():
    with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def set_cache_flag(enabled: bool):
    config = load_config()
    config["use_cache"] = 1 if enabled else 0
    save_config(config)

def get_cache_flag() -> bool:
    config = load_config()
    return config.get("use_cache", 0) == 1

def save_grades_cache(grades: list[list]):
    config=load_config()
    if 'grade' not in config or not isinstance(config['grade'], dict):
        config['grade'] = {}

    for row in grades:
        if not row:
            continue
        course_name = row[0]
        config['grade'][course_name] = row

    save_config(config)

def get_grades_cache() -> list[list]:
    config = load_config()

    if 'grade' not in config or not isinstance(config['grade'], dict):
        return []

    return list(config['grade'].values())
