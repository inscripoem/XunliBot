import base64
import random
from re import findall
from sys import exc_info
import httpx
from httpx import AsyncClient
from nonebot import logger


async def get_cat():
    async with AsyncClient() as client:
        req_url = "https://api.thecatapi.com/v1/images/search"
        params = {'mime_types': 'gif'}
        try:
            res = await client.get(req_url, params=params, timeout=120)
            logger.info(res.json())
        except httpx.HTTPError as e:
            logger.warning(e)
            return [False, f"API异常{e}", '', '']
        try:
            img_url = res.json()[0]['url']
            pic_cq = ""
            content = await down_pic(img_url)
            img_base64 = convert_b64(content)
            if type(img_base64) == str:
                pic_cq = "[CQ:image,file=base64://" + img_base64 + "]"
            return [True, '', pic_cq, img_url]
        except:
            logger.warning(f"{exc_info()[0]}, {exc_info()[1]}")
            return [False, f"{exc_info()[0]} {exc_info()[1]}。", '', '']


async def get_dog():
    async with AsyncClient() as client:
        req_url = "https://dog.ceo/api/breeds/image/random"
        try:
            res = await client.get(req_url, timeout=120)
            logger.info(res.json())
        except httpx.HTTPError as e:
            logger.warning(e)
            return [False, f"API异常{e}", '', '']
        try:
            img_url = res.json()['message']
            pic_cq = ""
            content = await down_pic(img_url.replace("\\", ''))
            img_base64 = convert_b64(content)
            if type(img_base64) == str:
                pic_cq = "[CQ:image,file=base64://" + img_base64 + "]"
            return [True, '', pic_cq, img_url]
        except:
            logger.warning(f"{exc_info()[0]}, {exc_info()[1]}")
            return [False, f"{exc_info()[0]} {exc_info()[1]}。", '', '']


async def get_fox():
    async with AsyncClient() as client:
        req_url = "https://randomfox.ca/floof/"
        try:
            res = await client.get(req_url, timeout=120)
            logger.info(res.json())
        except httpx.HTTPError as e:
            logger.warning(e)
            return [False, f"API异常{e}", '', '']
        try:
            img_url = res.json()['image']
            pic_cq = ""
            content = await down_pic(img_url)
            img_base64 = convert_b64(content)
            if type(img_base64) == str:
                pic_cq = "[CQ:image,file=base64://" + img_base64 + "]"
            return [True, '', pic_cq, img_url]
        except:
            logger.warning(f"{exc_info()[0]}, {exc_info()[1]}")
            return [False, f"{exc_info()[0]} {exc_info()[1]}。", '', '']

'''     
async def get_else(cat: str):
    async with AsyncClient() as client:
        req_url = "https://api.lolicon.app/setu/v2"
        json = {
            "r18": 0,
            "tag": cat,
            "proxy": "i.pixiv.re"
        }
        try:
            res = await client.post(url=req_url, json=json, timeout=120)
            logger.info(res.json())
            if not res.json()['data']:
                return [False, f'没有搜索到和{cat}有关的图捏']
        except httpx.HTTPError as e:
            logger.warning(e)
            return [False, f"API异常{e}", '', '']
        try:
            img_url = res.json()['data'][0]['urls']['original']
            content = await down_pic(img_url)
            img_base64 = convert_b64(content)
            if type(img_base64) == str:
                pic_cq = "[CQ:image,file=base64://" + img_base64 + "]"
            return [True, '', pic_cq, img_url]
        except:
            logger.warning(f"{exc_info()[0]}, {exc_info()[1]}")
            return [False, f"{exc_info()[0]} {exc_info()[1]}。", '', '']
'''

async def get_else(cat: str):
    if cat == 'R-18':
        return [False, '请不要搜索限制级图片!']
    async with AsyncClient() as client:
        req_url = "http://api.kyomotoi.moe/api/pixiv/search"
        params = {
            "word": cat,
            "size": 50
        }
        try:
            res = await client.get(url=req_url, params=params, timeout=120)
            logger.info(res.json())
            if not res.json()['illusts']:
                return [False, f'没有搜索到和{cat}有关的图捏']
        except httpx.HTTPError as e:
            logger.warning(e)
            return [False, f"API异常{e}", '', '']
        try:
            illusts_list = []
            # 筛选全年龄图片
            for illusts in res.json()['illusts']:
                r18_flag = 0
                for tags in illusts['tags']:
                    if tags["name"] == "R-18":
                        r18_flag = 1
                if r18_flag == 0:
                    illusts_list.append(illusts)
            logger.info(illusts_list)
            if not illusts_list:
                return [False, '全是不能看的，请换个搜索词再试一遍（']
            # 从全年龄图片中随机选取一张
            illust_len = len(illusts_list)
            random_illust = random.randint(0, illust_len - 1)
            if illusts_list[random_illust]['meta_single_page']:
                original_url = illusts_list[random_illust]['meta_single_page']['original_image_url']
            else:
                page_len = len(illusts_list[random_illust]['meta_pages'])
                random_page = random.randint(0, page_len - 1)
                original_url = illusts_list[random_illust]['meta_pages'][random_page]['image_urls']['original']
            img_url = original_url.replace("i.pximg.net", "i.pixiv.re")
            pic_cq = ""
            content = await down_pic(img_url)
            img_base64 = convert_b64(content)
            if type(img_base64) == str:
                pic_cq = "[CQ:image,file=base64://" + img_base64 + "]"
            return [True, '', pic_cq, img_url]
        except:
            logger.warning(f"{exc_info()[0]}, {exc_info()[1]}")
            return [False, f"{exc_info()[0]} {exc_info()[1]}。", '', '']

async def down_pic(url):
    async with AsyncClient() as client:
        headers = {
            "User-Agent":
            "Mozilla/5.0 (Windows NT 10.0; WOW64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
        }
        re = await client.get(url=url, headers=headers, timeout=120)
        if re.status_code == 200:
            logger.success("成功获取图片")
            return re.content
        else:
            logger.error(f"获取图片失败: {re.status_code}")
            return re.status_code


def convert_b64(content) -> str:
    ba = str(base64.b64encode(content))
    pic = findall(r"\'([^\"]*)\'", ba)[0].replace("'", "")
    return pic

