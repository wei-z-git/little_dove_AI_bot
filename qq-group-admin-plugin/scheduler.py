import nonebot
from .config import plugin_config
from .SDUtils import SDUtils
require("nonebot_plugin_apscheduler")
from nonebot_plugin_apscheduler import scheduler
from nonebot import require



# 基于 add_job 方法的方式

async def send_ai_img_daily():
    bot = nonebot.get_bot("3320741388")
    sd = SDUtils(sd_host=plugin_config.sd_host, sd_port=plugin_config.sd_port)
    groups = plugin_config.sd_groups
    for group_id in groups:
        msg = await sd.generate_ai_image_msg(bot=bot, group_id=group_id)
        await bot.send_group_msg(group_id=int(group_id), message=msg)

scheduler.add_job(
    send_ai_img_daily, "cron", hour=plugin_config.sd_hour, minute=plugin_config.sd_minute, id="job_1"
)
