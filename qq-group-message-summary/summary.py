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
from nonebot_plugin_chatrecorder import get_message_records
from nonebot_plugin_session import extract_session, SessionIdType
import zoneinfo

# matchers
matcher_summary = on_command(
    '今日群聊', priority=3, permission=GROUP_ADMIN | GROUP_OWNER | SUPERUSER)

matcher_summary_half_day = on_command(
    '半天群聊', priority=2, permission=GROUP_ADMIN | GROUP_OWNER | SUPERUSER)

matcher_product_test = on_command(
    'test', priority=3, permission=GROUP_ADMIN | GROUP_OWNER | SUPERUSER)


@matcher_summary.handle()
async def _(matcher: Matcher, bot: Bot, event: GroupMessageEvent,):
    session = extract_session(bot, event)
    beijing_tz = zoneinfo.ZoneInfo("Asia/Shanghai")
    records = await get_message_records(
        session=session,
        id_type=SessionIdType.GROUP,
        time_start=datetime.now(beijing_tz).replace(hour=0),
        time_stop=datetime.now(beijing_tz).replace(hour=22),
    )
    summary = Summary(plugin_config)
    # 将record过滤然后切割为以4500为边界的list
    records_merged_list = await summary.message_handle(records)
    total_length = sum(len(word.encode('utf-8')) for word in records_merged_list)
    if records_merged_list == "":
        await matcher.send("没有足够的数据")
    else:
        ai_summarization = ""
        used_tokens=""
        await matcher.send(f"message length(utf-8) : {total_length} slices count:{len(records_merged_list)}")
        # 逐段生成ai总结
        for record in records_merged_list:
            response = await summary.get_ai_message_res(record)
            ai_summary=response.choices[0].message.content
            ai_summarization=ai_summarization+"\n===分割===\n"+ai_summary
            used_token=response.usage
            used_tokens=used_tokens+str(used_token)
            print(f"Staging Completed!")
        print("message received!!!")
        print(f"ai message length: {len(str(ai_summarization))}")
        ai_summarization_cut=await summary.content_cutting(ai_summarization,max_byte_size=10000)
        for record in ai_summarization_cut:
            await matcher.send(str(record))
        print(f"used tokens:{used_tokens}")


@matcher_summary_half_day.handle()
async def _(matcher: Matcher, bot: Bot, event: GroupMessageEvent,):
    session = extract_session(bot, event)
    records = await get_message_records(
        session=session,
        id_type=SessionIdType.GROUP,
        time_start=datetime.now() - timedelta(days=0.5),
    )
    summary = Summary(plugin_config)
    records_merged_list = await summary.message_handle(records)
    if records_merged_list == "":
        await matcher.send("没有足够的数据")
    else:
        total_length = sum(len(word) for word in records_merged_list)
        await matcher.send(f"message length : {total_length}")
        response = await summary.get_ai_message_res(records_merged_list)
        used_token=response.usage
        ai_summary=response.choices[0].message.content
        await matcher.send(str(ai_summary))
        await matcher.send(f"used token:{used_token}")