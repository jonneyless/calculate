import asyncio
import json

import redis.asyncio as redis
import requests

import assist
import config
from config import redisInfo

redis_host = redisInfo['host']
redis_port = redisInfo['port']
redis_db = redisInfo['db']
redis_password = redisInfo['password']

redis_pool = redis.ConnectionPool(host=redis_host, port=int(redis_port), db=int(redis_db), password=redis_password)
conn = redis.Redis(connection_pool=redis_pool)

loop = asyncio.get_event_loop()


async def okex_get(pay_method):
    key = "okex" + str(pay_method)
    val = await conn.get(key)
    if val is not None:
        return json.loads(val)
    else:
        return None


async def okex_set(data, pay_method):
    key = "okex" + str(pay_method)

    await conn.set(key, json.dumps(data), 300)


async def okex_get_day(pay_method):
    key = "day_okex" + str(pay_method)
    val = await conn.get(key)
    if val is not None:
        return json.loads(val)
    else:
        return None


async def okex_set_day(data, pay_method):
    key = "day_okex" + str(pay_method)

    await conn.set(key, json.dumps(data), 86400)


async def get_okex_price(pay_method=0):
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

    if len(prices) > 0:
        print("%s ok..." % pay_method)
        await okex_set_day(prices, pay_method)
        await okex_set(prices, pay_method)
    else:
        print("empty...")
        prices_day = await okex_get_day(pay_method)
        if prices_day is not None and len(prices_day) > 0:
            await okex_set_day(prices_day, pay_method)
            await okex_set(prices_day, pay_method)


loop.run_until_complete(get_okex_price(0))
loop.run_until_complete(get_okex_price(1))
loop.run_until_complete(get_okex_price(2))
loop.run_until_complete(get_okex_price(3))
