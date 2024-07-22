from telethon import Button

import config
import template_private
from helpp import send, is_admin


async def index(event, text, sender_id, user):
    if text == "/start":
        msg = "汇旺记账机器人，完全免费使用，如果觉得方便，请推荐给朋友们！ 如果机器人异常，请t出群重新拉就好了。机器人使用说明: @hwjzjqr"
        buttons = [
            [
                Button.url(text="【点击这里把机器人加进群】", url=config.share_url),
            ],
        ]
        await send(event, msg, buttons)
    elif text == "说明" or text == "/说明" or text == "/shuoming":
        await send(event, template_private.template_private_explain)
    else:
        text = text.replace("/start", "")
        text = text.replace(" ", "")
        if len(text) > 0:
            chat_id = text

            admin_flag = await is_admin(chat_id, sender_id, user)
            if admin_flag:
                web_url_full = config.web_url % text
                await send(event, web_url_full)
            else:
                await send(event, "没有权限")
