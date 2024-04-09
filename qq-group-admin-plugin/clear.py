from nonebot import on_command, get_bot
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent, MessageSegment
from nonebot.adapters.onebot.v11.permission import GROUP_ADMIN, GROUP_OWNER
from nonebot.matcher import Matcher
from nonebot.params import CommandArg, Arg, ArgPlainText
from nonebot.permission import SUPERUSER
from nonebot.log import logger
from nonebot.exception import ActionFailed
from nonebot.rule import to_me
import random
from io import BytesIO
# Custom utils
from .utils import order_member_by_time, read_accounts_from_file, order_member_by_time_dsa
from .SDUtils import SDUtils

from .config import plugin_config



async def search_group_mem_list_detail(bot: Bot, matcher: Matcher, event: GroupMessageEvent) -> None:
    """
        查询不活跃的成员明细
    """
    gid = int(event.group_id)
    try:
        member_list = await get_bot("1141560393").call_api("get_group_member_list", group_id=gid, no_cache=True)
        fly_list = order_member_by_time(member_list)
        await matcher.send("冷库食材详细清单: \n"+str(fly_list)+"\n --消息来自小鸠Joe机器人")

    except ActionFailed:
        await matcher.finish(f"error")


async def search_group_mem_list(bot: Bot, matcher: Matcher, event: GroupMessageEvent) -> None:
    """
        查询不活跃的成员
    """
    gid = int(event.group_id)
    try:
        member_list = await get_bot().call_api("get_group_member_list", group_id=gid, no_cache=True)
        fly_list = order_member_by_time(member_list)
        await matcher.send("")
        fly_list_simple = ",\n".join(
            [f"{d['nickname']}:{d['user_id']}" for d in fly_list])
        await matcher.send("请查阅冷库食材清单:\n"+fly_list_simple+"\n -- 消息来自小鸠Joe机器人")

    except ActionFailed as e:
        await matcher.finish(f"error")


async def kicker_group_mem(bot: Bot, matcher: Matcher, event: GroupMessageEvent) -> None:
    """
        踢出不活跃的成员
    """
    gid = int(event.group_id)
    try:
        member_list = await get_bot("1141560393").call_api("get_group_member_list", group_id=gid, no_cache=True)
        fly_list = order_member_by_time(member_list)
        for member in fly_list:
            qq_num = member['user_id']
            qq_nickname = member['nickname']
            print(qq_num)
            await bot.set_group_kick(group_id=gid, user_id=qq_num, reject_add_request="false")
            await matcher.send("已将 " + str(qq_nickname)+":"+str(qq_num) + " 折跃去冷库！嗖~~\n --消息来自小鸠Joe机器人")

    except ActionFailed as e:
        print(e)
        await matcher.finish(f"机器人权限不足捏")


async def send_ai_image(bot: Bot, matcher: Matcher, event: GroupMessageEvent) -> None:
    """查询活跃成员,并随机获取1人,返回其qq头像
        经过处理,返回ai生成的头像
    """
    sd = SDUtils(sd_host=plugin_config.sd_host, sd_port=plugin_config.sd_port)
    gid = int(event.group_id)
    try:
        member_list = await get_bot("1141560393").call_api("get_group_member_list", group_id=gid, no_cache=True)
        # 选择最近发言10人
        top10_list = order_member_by_time_dsa(member_list)

        # 随机抽取一人
        selected_user = random.choice(top10_list)
        avatar_url = f"https://q2.qlogo.cn/headimg_dl?dst_uin={selected_user['user_id']}&spec=640"
        # x = str([(user['user_id'], user['nickname']) for user in top10_list])
        # await matcher.send)
        pil_image, image_base64 = await sd.download_img(avatar_url)
        tags = await sd.img2tags(image_base64)
        images = []
        # 生成4张图片
        for _ in range(4):
            img_new = await sd.img2img(tags, pil_image)
            images.append(img_new)
        image_BytesIO = await sd.combine4p(images)
        text = (f"""信徒抽取中(10/10)...:
{[(user['user_id'], user['nickname']) for user in top10_list]}
""")
        # 消息段只接受BytesIO, 理论上也支持bytes，但懒得看了
        img_byte_array = BytesIO()
        pil_image.save(img_byte_array, format='PNG')
        msg = Message([MessageSegment.text(text)])
        msg.append(MessageSegment.text(
            f"\n少女祈祷中...\n将被重生的人为: {selected_user['nickname']}\n"))
        msg.append(MessageSegment.image(img_byte_array))
        msg.append(MessageSegment.text(f"\n重生中...\n\n新造的人:\n"))
        msg.append(MessageSegment.image(image_BytesIO))
        await matcher.send(msg)

    except ActionFailed:
        await matcher.finish(f"error")

# 交互式
matcher_call_robot = on_command('call', aliases={'召唤小鸠机器人', '召唤'}, priority=1,
                                permission=GROUP_ADMIN | GROUP_OWNER | SUPERUSER)

# 给ac的
matcher_ac_message = on_command('ac', aliases={
                                '更新音声', '开始直播'}, priority=4, permission=GROUP_ADMIN | GROUP_OWNER | SUPERUSER)

# # Interative command
question = "洒家来啦~~，哥哥有何吩咐:\n  1.查询冷库食材\n  2.查询冷库食材详细\n  3.发送食材！！！\n  0.退出\n请哥哥选择！\n ---消息来自小鸠Joe机器人"

# 查询尊贵vip名单
matcher_vip_list = on_command(
    'vip', priority=4, permission=GROUP_ADMIN | GROUP_OWNER | SUPERUSER)

matcher_rebir = on_command(
    '重生', priority=1)


@matcher_rebir.handle()
async def _(bot: Bot, matcher: Matcher, event: GroupMessageEvent,  args: Message = CommandArg()):
    await send_ai_image(bot, matcher, event)


@matcher_ac_message.handle()
async def _(matcher: Matcher, args: Message = CommandArg()):
    answer_list = ['不语大笨蛋!', 'a宝小可爱么么哒~', '我要吃鸠鸠！嘎嘣..嘎嘣！', 'ac来了吗？如-来-', '你被催眠了，砰砰！',
                   '......', '你个老六', '明年再说', '收到', 'ac是小天使~', '结婚去了，勿扰', '蜜月中，勿扰']
    random_str = random.choice(answer_list)
    await matcher.send(random_str)


@matcher_call_robot.got("option", prompt=question)
async def call_robot(bot: Bot, matcher: Matcher, event: GroupMessageEvent, option: Message = Arg(), answer: str = ArgPlainText("option")):
    match answer:
        case "1":
            # 1.查询冷库食材
            await search_group_mem_list(bot, matcher, event)
            await matcher_call_robot.finish()
        case "2":
            # 2.查询冷库食材详细
            await search_group_mem_list_detail(bot, matcher, event)
            await matcher_call_robot.finish()
        case "3":
            # 3.发送食材!!!
            await kicker_group_mem(bot, matcher, event)
            await matcher_call_robot.finish()
        case "0":
            # 0.退出
            await matcher_call_robot.finish(f"拜拜了您嘞~")
        case _:
            # 可以使用平台的 Message 类直接构造模板消息
            await matcher_call_robot.reject(option.template("哥哥，泥在说些甚么！洒家听不懂！请再说一遍！ok?"))


@matcher_vip_list.handle()
async def _(matcher: Matcher):
    vip_list = read_accounts_from_file()
    await matcher.send(f"💎尊享svip年费会员列表:{vip_list}")
