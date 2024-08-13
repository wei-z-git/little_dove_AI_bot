# from typing import Optional
from nonebot import get_driver
from pydantic import BaseModel, Extra


class Config(BaseModel, extra=Extra.ignore):
    ai_secret_key: str  # llama中文社区 secret key
    exclude_user_list: list = [3320741388,2024085613] # 排除用户的id
    keywords_file_path: str = "config/filter_keywords.txt" # 过滤关键词的文件路径
    ai_summary_hour: int = 22  # 每天需要发送ai总结时间，小时
    ai_summary_minite: int = 00  # 每天需要发送ai总结时间，分钟
    ai_summary_groups: list = ["1170115778", "617875321",
                       "190842825", "689583064","715025692"]  # 每天需要发送ai总结的groups
driver = get_driver()
global_config = driver.config
plugin_config = Config.parse_obj(global_config)
