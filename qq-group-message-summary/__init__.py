
from nonebot.plugin import PluginMetadata

from .config import Config


from . import (
    summary,scheduler
)

__plugin_meta__ = PluginMetadata(
    name="示例插件",
    description="这是一个示例插件",
    usage="没什么用",
    type="application",
    config=Config,
    extra={},
)