import nonebot
from nonebot.adapters.onebot.v11 import Adapter as ONEBOT_V11Adapter
from fastapi import FastAPI
from nonebot import logger

nonebot.init()

driver = nonebot.get_driver()
logger.info(f"加载全局配置如下：")
for kv in driver.config:
    logger.info(f"{kv[0]}={kv[1]}")

driver.register_adapter(ONEBOT_V11Adapter)

# nonebot.load_plugin("nonebot-plugin-forwarder.nonebot_plugin_forwarder")
nonebot.load_from_toml("pyproject.toml")

# health check api
app: FastAPI = nonebot.get_app()
@app.get("/.internal/v1/health/self")
async def health_check():
    return {"service is healthy!"}


if __name__ == "__main__":
    nonebot.run()
