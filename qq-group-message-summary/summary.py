from .config import plugin_config
from .SummaryUtils import Summary
from nonebot import require
require("nonebot_plugin_chatrecorder")
from datetime import datetime, timedelta
from nonebot import on_command
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent
from nonebot.adapters.onebot.v11.permission import GROUP_ADMIN, GROUP_OWNER
from nonebot.matcher import Matcher
from nonebot.permission import SUPERUSER
from nonebot.exception import ActionFailed
from nonebot_plugin_session import extract_session

# matchers
matcher_summary = on_command(
    '今日群聊', priority=3, permission=GROUP_ADMIN | GROUP_OWNER | SUPERUSER)

# matcher_summary_half_day = on_command(
#     '半天群聊', priority=2, permission=GROUP_ADMIN | GROUP_OWNER | SUPERUSER)

matcher_product_test = on_command(
    'test', priority=3, permission=GROUP_ADMIN | GROUP_OWNER | SUPERUSER)


@matcher_summary.handle()
async def _(matcher: Matcher, bot: Bot, event: GroupMessageEvent,):
    summary = Summary(plugin_config,session=extract_session(bot, event))
    total_length=summary.get_length()
    if total_length == 0:
        await matcher.send("没有足够的数据")
    else:
        ai_summarization_cut, used_tokens=summary.message_handle()
        await matcher.send(f"message length(utf-8) : {total_length} slices count:{len(ai_summarization_cut)}")
        for record in ai_summarization_cut:
            await matcher.send(str(record))
        print(f"used tokens:{used_tokens}")


# @matcher_summary_half_day.handle()
# async def _(matcher: Matcher, bot: Bot, event: GroupMessageEvent,):
#     session = extract_session(bot, event)
#     records = await get_message_records(
#         session=session,
#         id_type=SessionIdType.GROUP,
#         time_start=datetime.now() - timedelta(days=0.5),
#     )
#     summary = Summary(plugin_config)
#     records_merged_list = await summary.message_handle(records)
#     if records_merged_list == "":
#         await matcher.send("没有足够的数据")
#     else:
#         total_length = sum(len(word) for word in records_merged_list)
#         await matcher.send(f"message length : {total_length}")
#         response = await summary.get_ai_message_res(records_merged_list)
#         used_token=response.usage
#         ai_summary=response.choices[0].message.content
#         await matcher.send(str(ai_summary))
#         await matcher.send(f"used token:{used_token}")