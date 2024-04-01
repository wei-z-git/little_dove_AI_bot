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
from nonebot.log import logger
from nonebot.exception import ActionFailed
from nonebot_plugin_chatrecorder import get_message_records
from nonebot_plugin_session import extract_session, SessionIdType


# matchers
matcher_summary = on_command(
    '今日群聊', priority=3, permission=GROUP_ADMIN | GROUP_OWNER | SUPERUSER)

matcher_product_test = on_command(
    'test', priority=3, permission=GROUP_ADMIN | GROUP_OWNER | SUPERUSER)


@matcher_summary.handle()
async def _(matcher: Matcher, bot: Bot, event: GroupMessageEvent,):
    session = extract_session(bot, event)
    records = await get_message_records(
        session=session,
        id_type=SessionIdType.GROUP,
        time_start=datetime.utcnow() - timedelta(days=1),
    )
    records_list = []
    for record in records:
        # 1.去除空消息 2.过滤指令"今日群聊" 3.去除机器人id
        if record.plain_text != "" and "今日群聊" not in record.plain_text and record.session.id1 != "2838376057":
            records_str = f"{record.plain_text}"
            records_list.append(records_str)
    records_merged = '\n'.join(records_list)
    if records_merged == "":
        await matcher.send("没有足够的数据")
    else:
        ai_summary = await Summary(plugin_config.ai_api_key, plugin_config.ai_secret_key).get_ai_message_res(records_merged)
        await matcher.send(str(ai_summary))
