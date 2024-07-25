import asyncio

import db_redis

loop = asyncio.get_event_loop()


async def set_url():
    await db_redis.yule_url_set("https://t.me/hwyL88")


loop.run_until_complete(set_url())
