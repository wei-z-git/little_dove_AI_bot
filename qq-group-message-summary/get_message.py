# from nonebot_plugin_session import extract_session, SessionIdType
# from nonebot_plugin_chatrecorder import get_messages_plain_text
# from nonebot import require
# from nonebot.adapters.onebot.v11 import Bot, Event
# from datetime import datetime, timedelta

# require("nonebot_plugin_chatrecorder")

# async def get_message(bot: Bot, event: Event):
#     session = extract_session(bot, event)
#     msgs = await get_messages_plain_text(
#         session, SessionIdType.GROUP, types=["message"], time_start=datetime.utcnow() - timedelta(days=1),
#     )
#     return msgs