import nonebot
from .config import plugin_config
from .SummaryUtils import Summary
from nonebot import require
require("nonebot_plugin_apscheduler")
from nonebot_plugin_apscheduler import scheduler
from nonebot.exception import ActionFailed


# 基于 add_job 方法的方式

async def send_chat_summary_daily():
    groups = plugin_config.ai_summary_groups
    bot = nonebot.get_bot()
    try:
        for gid in groups:
            summary = Summary(plugin_config, qq_group_id=gid)
            total_length = await summary.get_length()
            ai_summarization_cut, used_tokens = await summary.message_handle()
            message=f"message length(utf-8) : {total_length} slices count:{len(ai_summarization_cut)}"
            await bot.send_group_msg(group_id=gid, message=message)
            for record in ai_summarization_cut:
                await  bot.send_group_msg(group_id=gid,message=str(record))
            print(f"used tokens:{used_tokens}")
    except ActionFailed:
        await bot.send_group_msg(group_id=gid,message="执行失败了捏,请输入ac")

scheduler.add_job(
    send_chat_summary_daily, "cron", hour=plugin_config.ai_summary_hour, minute=plugin_config.ai_summary_minite, id="job_send_chat_summary_daily"
)
