from nonebot import on_command, get_bot
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent, MessageSegment,Event
from nonebot.adapters.onebot.v11.permission import GROUP_ADMIN, GROUP_OWNER
from nonebot.matcher import Matcher
from nonebot.params import CommandArg, Arg, ArgPlainText
from nonebot.permission import SUPERUSER
from nonebot.log import logger
from nonebot.rule import to_me
import random
from io import BytesIO
# Custom utils
from .utils import read_accounts_from_file, order_member_by_time_dsa
from .SDUtils import SDUtils

from .config import plugin_config


# 查询尊贵vip名单
matcher_vip_list = on_command(
    'vip', priority=4, permission=GROUP_ADMIN | GROUP_OWNER | SUPERUSER)

matcher_rebir = on_command(
    '重生', priority=1,permission=GROUP_ADMIN | GROUP_OWNER | SUPERUSER)


@matcher_rebir.handle()
async def _(bot: Bot, event: GroupMessageEvent,  args: Message = CommandArg()):
    # make sure bot is bot
    bot =  get_bot("3320741388")
    sd = SDUtils(sd_host=plugin_config.sd_host, sd_port=plugin_config.sd_port)
    gid = int(event.group_id)
    msg = await sd.generate_ai_image_msg(bot=bot, group_id=gid)
    await bot.send_group_msg(event, message=msg)


@matcher_vip_list.handle()
async def _(matcher: Matcher):
    vip_list = read_accounts_from_file()
    await matcher.send(f"💎尊享svip年费会员列表:{vip_list}")
