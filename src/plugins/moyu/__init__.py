from nonebot import on_command, logger, get_driver
from nonebot.params import CommandArg
from nonebot.adapters.onebot.v11.bot import Bot
from nonebot.adapters.onebot.v11 import GroupMessageEvent, Message
from .data_source import get_moyu

moyu = on_command("摸鱼", block=True)


@moyu.handle()
async def hf(bot: Bot, event: GroupMessageEvent, msg: Message = CommandArg()):
    pic = await get_moyu()
    if pic[0]:
        try:
            await moyu.finish(message=Message(pic[2]))
        except Exception as e:
            logger.warning(e)
            await moyu.finish(
                message=Message(f"消息被风控，图发不出来\n{pic[1]}\n这是链接\n{pic[3]}"),
            )
    else:
        await moyu.finish(f"出错：{pic[1]}")
