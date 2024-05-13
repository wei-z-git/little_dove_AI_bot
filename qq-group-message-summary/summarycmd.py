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
from nonebot.params import ArgPlainText


# matchers
matcher_summary = on_command(
    '今日群聊', priority=3, permission=GROUP_ADMIN | GROUP_OWNER | SUPERUSER)

matcher_summary_pro = on_command(
    '今日群聊pro', priority=2, permission=GROUP_ADMIN | GROUP_OWNER | SUPERUSER)

matcher_ac = on_command(
    'ac·堕', priority=3, permission=GROUP_ADMIN | GROUP_OWNER | SUPERUSER)


async def send_ai_message(matcher: Matcher, bot: Bot, event: GroupMessageEvent, prompt: str = "总结这段聊天记录,字数在300字以内"):
    '''生成并逐段发送ai消息
    '''
    try:
        gid = int(event.group_id)
        summary = Summary(plugin_config, qq_group_id=gid, prompt=prompt)
        total_length = await summary.get_length()
        ai_summarization_cut, used_tokens = await summary.message_handle()
        # await matcher.send(f"message length(utf-8) : {total_length} slices count:{len(ai_summarization_cut)}")
        for record in ai_summarization_cut:
            await matcher.send(str(record))
        print(f"used tokens:{used_tokens}")
    except ActionFailed:
        await matcher.send("执行失败了捏,请输入ac")


@matcher_summary.handle()
async def _(matcher: Matcher, bot: Bot, event: GroupMessageEvent):
    await send_ai_message(matcher, bot, event)


question = f"""洒家来啦，请哥哥请输入prompt~❤
---💞消息来自爱好物理催眠🔨的小鸠Joe猛男机器人💘-战锤版
(Default：如下是多个用户参与的聊天记录,请提取有意义的词句，)
"""


@matcher_summary_pro.got("prompt", prompt=question)
async def call_robot(bot: Bot, event: GroupMessageEvent, matcher: Matcher, prompt: str = ArgPlainText()):
    await send_ai_message(matcher, bot, event, prompt)


@matcher_ac.handle()
async def _(matcher: Matcher, bot: Bot, event: GroupMessageEvent):
    prompt = "并结合这些词句,对其他人说一句话,字数在10字以内,要求幽默风趣"
    await send_ai_message(matcher, bot, event, prompt)
