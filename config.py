from environs import Env

env = Env()
env.read_env()

mysqlInfo = {
    "host": env.str("DB_HOST", "127.0.0.1"),
    "db": env.str("DB_DATABASE", "calculate"),
    "user": env.str("DB_USER", "root"),
    "passwd": env.str("DB_PASS", "7a89afd87c0cd015"),
    "port": env.int("DB_PORT", 3306),
}

redisInfo = {
    "host": env.str("REDIS_HOST", "127.0.0.1"),
    "port": env.int("REDIS_PORT", 6379),
    "db": env.int("REDIS_DB", 0),
    "password": env.str("REDIS_PASS", 1123),
}

bot_token = env.str('BOT_TOKEN', '5995027011:AAFbO4lMOnv-AYbDYT2NTtLFJ79FkcON5jE')
bot_tg_id = env.int('BOT_TG_ID', 5995027011)
bot_username = env.str('BOT_USERNAME', 'jz99bot')
ping = env.str('CMD_PING', 'jz99botTest')
pong = env.str('CMD_PONG', 'jz99botSuccess')

web_sub_domain = env.str("SUB_DOMAIN", "https://jz.yu444.com")

bot_start_url = "https://t.me/" + bot_username + "?start=%s"
share_url = "https://t.me/" + bot_username + "?startgroup=true"
web_url = web_sub_domain + "/chat/day?chat_id=%s"

okex_url = "https://www.okx.com/v3/c2c/tradingOrders/books"

flag_up = 1
flag_down = 2
