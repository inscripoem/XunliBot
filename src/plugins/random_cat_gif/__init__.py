from nonebot import on_command, logger, get_driver
from nonebot.params import CommandArg
from nonebot.adapters.onebot.v11.bot import Bot
from nonebot.adapters.onebot.v11 import GroupMessageEvent, Message, MessageSegment
from nonebot.plugin import PluginMetadata
from .data_source import get_cat, get_dog, get_fox, get_else

# 基于PicMenu的帮助系统
__plugin_meta__ = PluginMetadata(
    name='来个猫猫',
    description='会随机发送一张（不只）猫猫图片',
    usage='来个+后缀名',
    extra={
        'menu_data': [
            {
                'func': '猫猫',
                'trigger_method': 'on_cmd',
                'trigger_condition': '来个猫猫',
                'brief_des': '获取猫猫图片',
                'detail_des': '随机获取\n'
                              '一张猫猫的动图'
            },
            {
                'func': '狗狗',
                'trigger_method': 'on_cmd',
                'trigger_condition': '来个狗狗',
                'brief_des': '获取小狗图片',
                'detail_des': '随机获取\n'
                              '一张猫猫的图片'
            },
            {
                'func': '狐狸',
                'trigger_method': 'on_cmd',
                'trigger_condition': '来个狐狸',
                'brief_des': '获取狐狸图片',
                'detail_des': '随机获取\n'
                              '一张狐狸的图片'
            }
        ],
        'menu_template': 'default'
    }
)

setu_ban_group = get_driver().config.setu_ban_group
miao = on_command("来个", block=True)


@miao.handle()
async def hf(bot: Bot, event: GroupMessageEvent, msg: Message = CommandArg()):
    cat = msg.extract_plain_text().strip()
    gid = str(event.group_id)
    if cat == "猫猫":
        await miao.send(message=Message(f'稍等一下哦，正在搜罗{cat}图……'))
        pic = await get_cat()
    elif cat == "狗狗":
        await miao.send(message=Message(f'稍等一下哦，正在搜罗{cat}图……'))
        pic = await get_dog()
    elif cat == "狐狸":
        await miao.send(message=Message(f'稍等一下哦，正在搜罗{cat}图……'))
        pic = await get_fox()
    else:
        if gid in setu_ban_group or not cat:
            pic = [False, '', '', '']
            await miao.finish()
        else:
            await miao.send(message=Message(f'稍等一下哦，正在搜罗{cat}图……'))
            pic = await get_else(cat)
    if pic[0]:
        try:
            await miao.send(
                message=Message(f"您点的{cat}一份~"),
            )
            await miao.send(message=Message(pic[2]))
            #await miao.send(message=MessageSegment.image(pic[3],cache=1))
        except Exception as e:
            logger.warning(e)
            await miao.finish(
                message=Message(f"消息被风控，图发不出来\n{pic[1]}\n这是链接\n{pic[3]}"),
            )
    else:
        await miao.finish(f"出错：{pic[1]}")
