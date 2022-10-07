from nonebot import on_command, logger, get_driver
from nonebot.params import CommandArg
from nonebot.adapters.onebot.v11.bot import Bot
from nonebot.adapters.onebot.v11 import MessageSegment, Message, MessageEvent
import base64
from re import findall
from sys import exc_info
import httpx
from httpx import AsyncClient
from nonebot import logger

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