import nonebot
from .config import plugin_config
from .SummaryUtils import Summary
from nonebot import require
require("nonebot_plugin_apscheduler")
from nonebot_plugin_apscheduler import scheduler
from nonebot_plugin_session import extract_session

# temp
from nonebot_plugin_chatrecorder import get_messages_plain_text
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent


# 基于 add_job 方法的方式

# async def send_chat_summary_daily():
#     bot = nonebot.get_bot("3320741388")
#     summary = Summary(plugin_config,session=extract_session(bot, event))
#     groups = plugin_config.sd_groups
#     for group_id in groups:
#         msg = await sd.generate_ai_image_msg(bot=bot, group_id=group_id)
#         await bot.send_group_msg(group_id=int(group_id), message=msg)

# scheduler.add_job(
#     send_chat_summary_daily, "cron", hour=plugin_config.ai_summary_hour, minute=plugin_config.ai_summary_minite, id="job_1"
# )


    # try:
    #     summary = Summary(plugin_config,session=extract_session(bot, event))
    #     total_length=await summary.get_length()
    #     ai_summarization_cut, used_tokens=await summary.message_handle()
    #     await matcher.send(f"message length(utf-8) : {total_length} slices count:{len(ai_summarization_cut)}")
    #     for record in ai_summarization_cut:
    #         await matcher.send(str(record))
    #     print(f"used tokens:{used_tokens}")
    # except ActionFailed:
    #     await matcher.send("执行失败了捏,请输入ac")


async def job_daily():
    bot = nonebot.get_bot("3320741388")
    await get_messages_plain_text(id2s=[771840868])
    print(1)

scheduler.add_job(
    job_daily, "cron", hour=20, minute=58, id="job_daily"
)