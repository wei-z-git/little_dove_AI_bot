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
        time_start=datetime.now() - timedelta(days=1),
    )
    summary = Summary(plugin_config)
    records_merged = await summary.filter(records)
    if records_merged == "":
        await matcher.send("没有足够的数据")
    else:
        ai_summary = await summary.get_ai_message_res(records_merged)
        await matcher.send(str(ai_summary))
