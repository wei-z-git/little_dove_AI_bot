# from typing import Optional
from nonebot import get_driver
from pydantic import BaseModel, Extra


class Config(BaseModel, extra=Extra.ignore):
    ai_api_key: str  # llama中文社区 api key
    ai_secret_key: str  # llama中文社区 secret key
    exclude_user_list: list = [3320741388,2024085613] # 排除用户的id
    keywords_file_path: str = "config/filter_keywords.txt" # 过滤关键词的文件路径


driver = get_driver()
global_config = driver.config
plugin_config = Config.parse_obj(global_config)
