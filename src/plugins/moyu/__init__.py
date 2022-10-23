from nonebot import on_command, logger
from nonebot.adapters.onebot.v11.bot import Bot
from nonebot.adapters.onebot.v11 import MessageSegment, MessageEvent
import httpx
from nonebot import logger
from nonebot.plugin import PluginMetadata

# 基于PicMenu的帮助系统
__plugin_meta__ = PluginMetadata(
    name='一起摸鱼！',
    description='从“摸鱼人日历”公众号获取当天的摸鱼日历图',
    usage='摸鱼'
)

moyu = on_command("摸鱼", block=True)


@moyu.handle()
async def hf(bot:Bot, event:MessageEvent):
    async with httpx.AsyncClient() as client:
        req_url = "https://api.j4u.ink/v1/store/other/proxy/remote/moyu.json"
        try:
            res = await client.get(req_url, timeout=120)
            logger.info(res.json())
        except httpx.HTTPError as e:
            logger.warning(f'API异常{e}')
        img_url = res.json()['data']['moyu_url']
        await bot.send(event=event, message=MessageSegment.image(img_url,cache=1))