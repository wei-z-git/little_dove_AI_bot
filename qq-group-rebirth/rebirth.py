from nonebot import on_command, get_bot
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent
from nonebot.adapters.onebot.v11.permission import GROUP_ADMIN, GROUP_OWNER
from nonebot.matcher import Matcher
from nonebot.params import CommandArg
from nonebot.permission import SUPERUSER
# Custom utils
from .utils import read_accounts_from_file
from .SDUtils import SDUtils
from nonebot.exception import ActionFailed

from .config import plugin_config


# 查询尊贵vip名单
matcher_vip_list = on_command(
    'vip', priority=4, permission=GROUP_ADMIN | GROUP_OWNER | SUPERUSER)

matcher_rebir = on_command(
    '重生', aliases={'投胎', '转世'}, priority=1, permission=GROUP_ADMIN | GROUP_OWNER | SUPERUSER)


@matcher_rebir.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    # make sure bot is bot
    bot = get_bot("3320741388")
    sd = SDUtils(sd_host=plugin_config.sd_host, sd_port=plugin_config.sd_port)
    gid = int(event.group_id)
    try:
        msg = await sd.generate_ai_image_msg(group_id=gid)
    except ActionFailed as e:
        await bot.send(event, e)
    await bot.send(event, message=msg)


@matcher_vip_list.handle()
async def _(matcher: Matcher):
    vip_list = read_accounts_from_file()
    await matcher.send(f"💎尊享svip年费会员列表:{vip_list}")
