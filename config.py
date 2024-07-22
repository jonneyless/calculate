import ini

bot_token = ini.config.get('tg_bot', 'token')
bot_tg_id = ini.config.get('tg_bot', 'tg_id')
bot_username = ini.config.get('tg_bot', 'bot_username')
ping = ini.config.get('tg_bot', 'ping_cmd')
pong = ini.config.get('tg_bot', 'pong_cmd')

web_sub_domain = ini.config.get('web_setting', 'sub_domain')

bot_start_url = "https://t.me/" + bot_username + "?start=%s"
share_url = "https://t.me/" + bot_username + "?startgroup=true"
web_url = web_sub_domain + "/chat/day?chat_id=%s"

okex_url = "https://www.okex.com/v3/c2c/tradingOrders/books"

flag_up = 1
flag_down = 2
