# from typing import Optional
from nonebot import get_driver
from pydantic import BaseModel, Extra


class Config(BaseModel, extra=Extra.ignore):
    tenid: str = 'xxxxxx'  # 腾讯云图片安全，开通地址： https://console.cloud.tencent.com/cms
    tenkeys: str = 'xxxxxx'  # 文档： https://cloud.tencent.com/document/product/1125
    callback_notice: bool = True  # 是否在操作完成后在 QQ 返回提示
    ban_rand_time_min: int = 60  # 随机禁言最短时间(s) default: 1分钟
    ban_rand_time_max: int = 2591999  # 随机禁言最长时间(s) default: 30天: 60*60*24*30
    group_recall: bool = False  # 是否开启防撤回功能 #TODO: 加到开关管理？
    sd_host: str = 'hb.frp.one'  # sd的host地址
    sd_port: int = 52097  # sd server的端口
    sd_groups: list = ["1170115778", "617875321",
                       "190842825", "689583064","715025692",]  # 每天需要发送sd ai图片的groups
    sd_hour: int = 2  # 每天需要发送sd ai图片时间，小时
    sd_minute: int = 59  # 每天需要发送sd ai图片时间，分钟


driver = get_driver()
global_config = driver.config
plugin_config = Config.parse_obj(global_config)
