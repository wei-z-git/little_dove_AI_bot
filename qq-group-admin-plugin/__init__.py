import nonebot

from . import (
    clear,scheduler
)

driver = nonebot.get_driver()


@driver.on_bot_connect
async def _():
    bot = nonebot.get_bot("3320741388")


"""
qq群清理
"""

__usage__ = """

"""
__help_plugin_name__ = 'qq群清理'

__permission__ = 1
__help__version__ = '0.1.0'


