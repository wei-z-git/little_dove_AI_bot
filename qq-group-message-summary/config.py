# from typing import Optional
from nonebot import get_driver
from pydantic import BaseModel, Extra


class Config(BaseModel, extra=Extra.ignore):
    ai_api_key: str  # 文心一言api key
    ai_secret_key: str  #文心一言 secret key


driver = get_driver()
global_config = driver.config
plugin_config = Config.parse_obj(global_config)


