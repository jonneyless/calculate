import assist
import config
import db
import net
import template


# ======================================================================================================================

async def send(event, msg, buttons=None):
    try:
        if buttons is None:
            return await event.respond(message=msg, parse_mode="html", link_preview=False)
        else:
            return await event.respond(message=msg, buttons=buttons, parse_mode="html", link_preview=False)
    except Exception as e:
        print("send error:%s" % e)


async def reply(event, msg):
    try:
        await event.reply(message=msg, parse_mode="html", link_preview=False)
    except Exception as e:
        print("reply error:%s" % e)


async def editMsg(bot, chat_id, msg_id, message, buttons):
    try:
        await bot.edit_message(entity=chat_id, message=msg_id, text=message, buttons=buttons, parse_mode="html")
    except Exception as e:
        print("edit error:%s" % e)


async def delete(bot, chat_id, msg_id):
    chat_id = int(chat_id)
    msg_id = int(msg_id)

    try:
        await bot.delete_messages(chat_id, msg_id)
    except Exception as e:
        print("delete error:%s" % e)


# ======================================================================================================================

async def init_chat(bot, event, chat_id):
    await db.group_delete(chat_id)
    await db.admin_delete_all(chat_id)
    await db.admin_no_delete_all(chat_id)
    await db.log_up_delete(chat_id)
    await db.log_down_delete(chat_id)

    chat = await bot.get_entity(chat_id)
    if chat is None:
        return

    group = await db.group_one(chat_id)
    if group is None:
        await db.group_save(chat_id, chat.title)

    admins = await net.get_admins(bot, chat_id)
    for admin in admins:
        await db.admin_save(chat_id, admin)

    await send(event, template.template_welcome())


def need_replyer(text):
    flag = False
    if (text == "设置不允许操作人") or (text == "删除不允许操作人") or (text.find("+") == 0) or (text.find("入款+") == 0) or (
        text.find("-") == 0) or (text.find("入款-") == 0) or (text.find("下发-") == 0) or (
        text.find("下发") == 0) or text == "账单":
        flag = True

    return flag


async def is_admin(chat_id, sender_id, user):
    flag = True

    # admin = await db.admin_one(chat_id, sender_id)
    # if admin is None:
    #     if len(user["username"]) == 0:
    #         flag = False
    #     else:
    #         admin = await db.admin_one_by_username(chat_id, user["username"])
    #         if admin is None:
    #             flag = False

    return flag


async def is_admin_no(chat_id, sender_id, user):
    flag = False

    admin = await db.admin_no_one(chat_id, sender_id)
    if admin is None:
        if len(user["username"]) == 0:
            flag = True
        else:
            admin = await db.admin_no_one_by_username(chat_id, user["username"])
            if admin is None:
                flag = True

    return flag


async def get_group(chat_id, event):
    group = await db.group_one(chat_id)
    if group is None:
        return
    else:
        chat = await event.get_chat()
        if chat is not None:
            if hasattr(chat, "title") and chat.title is not None:
                if chat.title != group["title"]:
                    await db.group_set_title(group, chat.title)

    group = assist.handle_group_sql(group)

    return group


async def set_official_user(chat_id, newer):
    is_official = await db.official_one(newer["tg_id"])
    if is_official is not None:
        await db.admin_save(chat_id, newer)


async def get_current_price(group):
    pay_method = group["pay_type"]

    prices = await net.get_okex_price(pay_method)
    price_current = 0
    for index in range(len(prices)):
        if (index + 1) == group["seller_position"]:
            item = prices[index]
            price_current = item["price"]
            break

    little_price_change = template.to_num2(group["little_price_change"])
    price_current = template.to_num2(price_current)
    if price_current > 0:
        price = template.to_num2(price_current + little_price_change)
        return price


# ======================================================================================================================

async def show_time_rate(bot, event, group, edit=False, chat_id=None, msg_id=None, pay_method=0):
    prices = await net.get_okex_price(pay_method)

    message = await template.template_show_time_rate(group, prices, pay_method)
    buttons = template.buttons_show_time_rate(pay_method)

    if edit:
        await editMsg(bot, chat_id, msg_id, message, buttons)
    else:
        await send(event, message, buttons)


async def change_time_rate(bot, event, group, edit=False, chat_id=None, msg_id=None, seller_position=3, pay_method=0):
    prices = await net.get_okex_price(pay_method)

    message = await template.template_change_time_rate(group, prices, pay_method)
    buttons = template.buttons_change_time_rate(seller_position, pay_method)

    if edit:
        await editMsg(bot, chat_id, msg_id, message, buttons)
    else:
        await send(event, message, buttons)


async def show_log(event, group):
    if group["model"] == 1:
        group["money_rate"] = await get_current_price(group)

    created_at = assist.get_created_at()

    log_ups = await db.log_up_get(group, created_at)
    log_downs = await db.log_down_get(group, created_at)

    message = await template.template_show_log(group, log_ups, log_downs)
    buttons = template.buttons_show_log(group["tg_id"])

    await send(event, message, buttons)


async def show_log_replyer(event, group, replyer):
    if group["model"] == 1:
        group["money_rate"] = await get_current_price(group)

    created_at = assist.get_created_at()

    log_ups = await db.log_up_get_by_replyer(group, replyer["tg_id"], created_at)
    log_downs = await db.log_down_get_replyer(group, replyer["tg_id"], created_at)

    if "me" in replyer:
        if len(log_ups) == 0 and len(log_downs) == 0:
            return

    message = await template.template_show_log_replyer(group, log_ups, log_downs)
    buttons = template.buttons_show_log(group["tg_id"])

    await send(event, message, buttons)


async def show_admin(event, chat_id, flag=1):
    admins = await db.admin_gets(chat_id)
    officals = await db.offical_gets()

    msg = template.template_admins(admins, officals, flag)

    await reply(event, msg)


async def show_admin_no(event, chat_id, flag=1):
    admins = await db.admin_no_gets(chat_id)
    officals = await db.offical_gets()

    msg = template.template_admins_no(admins, officals, flag)

    await reply(event, msg)


async def save_log(event, group, num, user, flag, replyer=None):
    money_rate = group["money_rate"]
    profit_rate = group["profit_rate"]
    if group["model"] == 1:
        money_rate = await get_current_price(group)

    if "money_rate_temp" in group:
        money_rate = group["money_rate_temp"]

    if flag == config.flag_up:
        await db.log_up_save(group, num, money_rate, profit_rate, user, replyer)
    else:
        await db.log_down_save(group, num, money_rate, profit_rate, user, replyer)

    await show_log(event, group)

# ======================================================================================================================
