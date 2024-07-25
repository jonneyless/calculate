import json

import redis.asyncio as redis

from config import redisInfo

redis_host = redisInfo['host']
redis_port = redisInfo['port']
redis_db = redisInfo['db']
redis_password = ""
prefix = "cal"

redis_pool = redis.ConnectionPool(
    host=redis_host, port=redis_port, db=redis_db)
conn = redis.Redis(connection_pool=redis_pool)


async def okex_get(pay_method):
    key = "okex" + str(pay_method)
    val = await conn.get(key)
    if val is not None:
        return json.loads(val)
    else:
        return None


async def okex_set(data, pay_method):
    key = "okex" + str(pay_method)

    await conn.set(key, json.dumps(data), 600)


async def price_get():
    key = "okex_price"
    val = await conn.get(key)
    if val is not None:
        return val
    else:
        return None


async def price_set(price):
    key = "okex_price"

    await conn.set(key, price, 600)


# ======================================================================================================================

async def group_z0_msg_get(group_tg_id):
    key = "z0_" + str(group_tg_id)

    data = await conn.get(key)
    if data is None:
        return data
    else:
        data = str(data, 'utf-8')
        data = int(data)

        return data


async def group_z0_msg_set(group_tg_id, m_id):
    key = "z0_" + str(group_tg_id)

    await conn.set(key, m_id, 86401)  # 1天+1秒


# ======================================================================================================================

async def yule_url_get():
    key = "yuelUrl"
    val = await conn.get(key)

    if val is not None:
        return val
    else:
        return None


async def yule_url_set(price):
    key = "yuelUrl"

    await conn.set(key, price, 864001)


# ======================================================================================================================

async def cal_data_get():
    key = prefix + "cal_data"

    data = await conn.lpop(key)
    if data is None:
        return data
    else:
        return json.loads(data)


async def cal_data_set(data):
    key = prefix + "cal_data"

    await conn.rpush(key, json.dumps(data))
