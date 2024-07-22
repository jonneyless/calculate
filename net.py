from telethon.tl.types import ChannelParticipantsAdmins

import json
import requests
import db_redis
import assist
import config


async def get_admins(bot, group_tg_id):
    group_tg_id = int(group_tg_id)

    admins = []
    async for user in bot.iter_participants(group_tg_id, filter=ChannelParticipantsAdmins):
        admins.append(assist.handle_user(user))

    return admins


async def get_okex_price(pay_method=0):
    pay_method = int(pay_method)
    prices = await db_redis.okex_get(pay_method)
    if prices is not None:
        return prices

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.1.6)",
        "Content-Type": "application/json",
    }

    data = {
        "t": int(assist.get_current_timestamp() * 1000),
        "quoteCurrency": "cny",
        "baseCurrency": "usdt",
        "side": "sell",
        "paymentMethod": "all",
        "userType": "all",
        "showTrade": False,
        "receivingAds": False,
        "noShowSafetyLimit": False,
        "showFollow": False,
        "showAlreadyTraded": False,
        "isAbleFilter": False,
    }
    if pay_method == 0:
        data["paymentMethod"] = "all"
    elif pay_method == 1:
        data["paymentMethod"] = "bank"
    elif pay_method == 2:
        data["paymentMethod"] = "aliPay"
    elif pay_method == 3:
        data["paymentMethod"] = "wxPay"

    prices = []
    response = requests.get(config.okex_url, headers=headers, params=data)

    result = json.loads(response.text)
    if (result is not None) and ("code" in result) and result["code"] == 0:
        items = result["data"]["sell"]
        for item in items:
            if len(prices) < 10:
                prices.append({
                    "username": item["nickName"],
                    "price": item["price"],
                })
            else:
                break

    await db_redis.okex_set(prices, pay_method)

    return prices
