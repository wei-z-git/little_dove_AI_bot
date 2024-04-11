# from typing import Optional
from nonebot import get_driver
from pydantic import BaseModel, Extra


class Config(BaseModel, extra=Extra.ignore):
    sd_host: str = 'frp.runtime20.space'  # sd的host地址
    sd_port: int = 52097  # sd server的端口
    sd_groups: list = ["1170115778", "617875321",
                       "190842825", "689583064","715025692"]  # 每天需要发送sd ai图片的groups
    sd_hour: int = 2  # 每天需要发送sd ai图片时间，小时
    sd_minute: int = 59  # 每天需要发送sd ai图片时间，分钟


driver = get_driver()
global_config = driver.config
plugin_config = Config.parse_obj(global_config)
