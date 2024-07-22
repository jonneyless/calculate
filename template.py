from telethon import Button

import assist
import config


def template_welcome():
    msg = "感谢您把我添加到贵群！\n"
    msg += "请群管输入相关命令开启机器人功能！群管输入说明可以参看操作说明。"

    return msg


def template_admins(admins, officals, flag=1):
    text = "添加不允许操作人成功！当前不允许操作人 "
    if flag == 2:
        text = "删除不允许操作人成功！当前不允许操作人 "
    elif flag == 3:
        text = "当前不允许操作人 "

    for admin in admins:
        admin = assist.handle_admin_sql(admin)

        if admin["username"]:
            is_offical = False
            for offical in officals:
                if admin["user_tg_id"] == offical["tg_id"]:
                    is_offical = True
                    break
            if is_offical:
                text += "%s" % admin["username"]
            else:
                text += "@%s" % admin["username"]
        else:
            text += "%s" % (admin["firstname"] + admin["lastname"])

        text += " "

    return text


def template_admins_no(admins, officals, flag=1):
    text = "添加不允许操作人成功！当前不允许操作人 "
    if flag == 2:
        text = "删除不允许操作人成功！当前不允许操作人 "
    elif flag == 3:
        text = "当前不允许操作人 "

    for admin in admins:
        admin = assist.handle_admin_sql(admin)

        if admin["username"]:
            is_offical = False
            for offical in officals:
                if admin["user_tg_id"] == offical["tg_id"]:
                    is_offical = True
                    break
            if is_offical:
                text += "%s" % admin["username"]
            else:
                text += "@%s" % admin["username"]
        else:
            text += "%s" % (admin["firstname"] + admin["lastname"])

        text += " "

    return text
    
    
def template_time_money_rate(num):
    return "汇率设置成功！当前实时汇率：%s" % num


def template_default_money_rate(num):
    return "汇率设置成功！当前汇率：%s" % num


def template_default_profit_rate(num):
    return "费率设置成功！当前费率：%s" % num


def template_remark_rate(num, remark):
    return "%s汇率设置成功，当前%s汇率：%s" % (remark, remark, num)


def template_show_type(num):
    return "当前显示模式：%s" % num


def template_set_reset_hour_ok(hour):
    return "调整每日更新时间为北京时间%s点整" % hour


def template_set_reset_hour_error():
    return "指令错误，请输入0-6范围内的整数数字"


async def template_show_log(group, log_ups, log_downs):
    show_type = group["show_type"]
    show_type = int(show_type)

    max_key = 3
    if show_type == 2:
        max_key = 5
    elif show_type == 3:
        max_key = 1

    money_sure = 0

    ups = []
    up_count = 0
    up_money = 0
    up_money_u = 0

    downs = []
    down_count = 0
    down_money = 0
    down_money_r = 0

    # num_len = get_num_len(money_rate)
    # num_len1 = get_num_len(profit_rate)

    # if num_len1 > num_len:
    #     num_len = num_len1

    money_rate = assist.to_num(group["money_rate"])
    profit_rate = assist.to_num(group["profit_rate"])

    money_rate_change = False

    for key in range(len(log_ups)):
        log = log_ups[key]
        log = assist.handle_log_up_sql(log)

        # if log["money"] > 0:
        if log["money"] > 0 or (log["money"] < 0 and show_type == 2):
            up_count += 1
            if len(ups) < max_key:
                ups.append(log)

        up_money += log["money"]
        up_money_u += log["money"] * (100 - log["profit_rate"]) / 100 / log["money_rate"]

        money_sure += log["money"] * (100 - log["profit_rate"]) / 100

        if assist.to_num(log["money_rate"]) != money_rate:
            money_rate_change = True

    for key in range(len(log_downs)):
        log = log_downs[key]
        log = assist.handle_log_down_sql(log)

        # if log["money"] > 0:
        if log["money"] > 0 or (log["money"] < 0 and show_type == 2):
            down_count += 1
            if len(downs) < max_key:
                downs.append(log)

        down_money += log["money"]
        down_money_r += log["money"] * log["money_rate"]

        if assist.to_num(log["money_rate"]) != money_rate:
            money_rate_change = True

    ups = list(reversed(ups))
    downs = list(reversed(downs))

    text = await assist.get_ad_text()

    text += "已入款（%s笔）：\n" % up_count
    if len(ups) == 0:
        text += " 暂无入款\n"
    else:
        for up in ups:
            money = assist.to_num(up["money"])
            money_rate_up = assist.to_num(up["money_rate"])

            temp1 = assist.to_num(up["money"] * (100 - up["profit_rate"]) / 100)
            temp2 = assist.to_num(temp1 / money_rate_up)

            text += " %s %s / %s=%s\n" % (assist.get_simple_time(up["created_at"]), temp1, money_rate_up, temp2)
    text += "\n"

    text += "已下发（%s笔）：\n" % down_count
    if len(downs) == 0:
        text += " 暂无下发"
        text += "\n"
    else:
        for down in downs:
            money = assist.to_num(down["money"])
            money_rate_down = assist.to_num(down["money_rate"])

            text += " %s %s (%s)\n" % (
                assist.get_simple_time(down["created_at"]), money, (assist.to_num(money * money_rate_down)))
    text += "\n"

    if show_type == 3:
        text = ""
        text = await assist.get_ad_text()

    up_money = assist.to_num(up_money)

    money_sure = assist.to_num(money_sure)
    money_sure_u = assist.to_num(up_money_u)

    money_down = assist.to_num(down_money_r)
    money_down_u = assist.to_num(down_money)

    money_no = assist.to_num(money_sure - money_down)
    money_no_u = assist.to_num(money_sure_u - money_down_u)

    text += "总入款金额：%s\n" % up_money
    text += "费率：%s%%\n" % profit_rate
    if group["model"] == 2:
        text += "固定汇率：%s\n" % money_rate
    else:
        text += "实时汇率：%s\n" % money_rate

    currency = "USDT"
    if money_rate == 1:
        currency = "RMB"

    if money_rate_change:
        text += "应下发：%s (%s)\n" % (money_sure_u, currency)
        text += "已下发：%s (%s)\n" % (money_down_u, currency)
        text += "未下发：%s (%s)\n" % (money_no_u, currency)
    else:
        text += "应下发：%s | %s (%s)\n" % (money_sure, money_sure_u, currency)
        text += "已下发：%s | %s (%s)\n" % (money_down, money_down_u, currency)
        text += "未下发：%s | %s (%s)\n" % (money_no, money_no_u, currency)

    return text


def buttons_show_log(chat_id):
    bot_start_url_full = config.bot_start_url % chat_id

    return [
        [
            Button.url(text="使用说明", url="https://t.me/hwjzjqr/6"),
            Button.url(text="供求信息", url="https://t.me/gongqiu"),
        ],
        [
            Button.url(text="完整账单", url=bot_start_url_full),
            Button.url(text="公群导航", url="https://t.me/hwgq"),
        ]
    ]


async def template_show_time_rate(group, prices, pay_method):
    msg = await assist.get_ad_text()

    pay_method = int(pay_method)
    if pay_method == 1:
        msg += "<b>Okex商家银行卡实时交易汇率top10</b>\n"
    elif pay_method == 2:
        msg += "<b>Okex商家支付宝实时交易汇率top10</b>\n"
    elif pay_method == 3:
        msg += "<b>Okex商家微信实时交易汇率top10</b>\n"
    else:
        msg += "<b>Okex商家实时交易汇率top10</b>\n"

    for key in range(len(prices)):
        item = prices[key]
        msg += "<code>%s) %s   %s</code>\n" % ((key + 1), item["price"], item["username"])
    msg += "\n"

    msg += "本群费率：%s%%\n" % assist.to_num2(group["profit_rate"])
    if group["model"] == 1:
        msg += "本群汇率：实时汇率"
    else:
        msg += "本群汇率：固定汇率%s" % assist.to_num2(group["money_rate"])

    return msg


async def template_change_time_rate(group, prices, pay_method):
    msg = await assist.get_ad_text()

    pay_method = int(pay_method)
    if pay_method == 1:
        msg += "<b>Okex商家银行卡实时交易汇率top10</b>\n"
    elif pay_method == 2:
        msg += "<b>Okex商家支付宝实时交易汇率top10</b>\n"
    elif pay_method == 3:
        msg += "<b>Okex商家微信实时交易汇率top10</b>\n"
    else:
        msg += "<b>Okex商家实时交易汇率top10</b>\n"

    little_change_price = assist.to_num2(group["little_price_change"])
    current_position_price = group["money_rate"]
    for key in range(len(prices)):
        item = prices[key]
        msg += "<code>%s) %s   %s</code>\n" % ((key + 1), item["price"], item["username"])

        if key == int(group["seller_position"]):
            current_position_price = item["price"]

    msg += "\n"

    current_position_price = assist.to_num2(current_position_price)

    msg += "当前档位价格：%s\n" % current_position_price
    msg += "微调价格：%s\n" % little_change_price
    msg += "价格：%s" % assist.to_num2(current_position_price + little_change_price)

    return msg


def buttons_show_time_rate(pay_method):
    pay_method = int(pay_method)

    text_0 = "所有"
    if pay_method == 0:
        text_0 = "所有✅"
    text_1 = "银行卡"
    if pay_method == 1:
        text_1 = "银行卡✅"
    text_2 = "支付宝"
    if pay_method == 2:
        text_2 = "支付宝✅"
    text_3 = "微信"
    if pay_method == 3:
        text_3 = "微信✅"

    return [
        [
            Button.inline(text=text_0, data="show_time_rate?pay_method=0"),
            Button.inline(text=text_1, data="show_time_rate?pay_method=1"),
            Button.inline(text=text_2, data="show_time_rate?pay_method=2"),
            Button.inline(text=text_3, data="show_time_rate?pay_method=3"),
        ],
    ]


def buttons_change_time_rate(seller_position=3, pay_method=0):
    seller_position = int(seller_position)
    pay_method = int(pay_method)

    num_1 = "1"
    if seller_position == 1:
        num_1 = "1✅"
    num_2 = "2"
    if seller_position == 2:
        num_2 = "2✅"
    num_3 = "3"
    if seller_position == 3:
        num_3 = "3✅"
    num_4 = "4"
    if seller_position == 4:
        num_4 = "4✅"
    num_5 = "5"
    if seller_position == 5:
        num_5 = "5✅"
    num_6 = "6"
    if seller_position == 6:
        num_6 = "6✅"
    num_7 = "7"
    if seller_position == 7:
        num_7 = "7✅"
    num_8 = "8"
    if seller_position == 8:
        num_8 = "8✅"
    num_9 = "9"
    if seller_position == 9:
        num_9 = "9✅"
    num_10 = "10"
    if num_10 == 10:
        num_10 = "1✅"

    text_0 = "所有"
    if pay_method == 0:
        text_0 = "所有✅"
    text_1 = "银行卡"
    if pay_method == 1:
        text_1 = "银行卡✅"
    text_2 = "支付宝"
    if pay_method == 2:
        text_2 = "支付宝✅"
    text_3 = "微信"
    if pay_method == 3:
        text_3 = "微信✅"

    return [
        [
            Button.inline(text=num_1, data="change_time_rate?seller_position=1"),
            Button.inline(text=num_2, data="change_time_rate?seller_position=2"),
            Button.inline(text=num_3, data="change_time_rate?seller_position=3"),
            Button.inline(text=num_4, data="change_time_rate?seller_position=4"),
            Button.inline(text=num_5, data="change_time_rate?seller_position=5"),
        ],
        [
            Button.inline(text=num_6, data="change_time_rate?seller_position=6"),
            Button.inline(text=num_7, data="change_time_rate?seller_position=7"),
            Button.inline(text=num_8, data="change_time_rate?seller_position=8"),
            Button.inline(text=num_9, data="change_time_rate?seller_position=9"),
            Button.inline(text=num_10, data="change_time_rate?seller_position=10"),
        ],
        [
            Button.inline(text=text_0, data="change_time_rate?pay_method=0"),
            Button.inline(text=text_1, data="change_time_rate?pay_method=1"),
            Button.inline(text=text_2, data="change_time_rate?pay_method=2"),
            Button.inline(text=text_3, data="change_time_rate?pay_method=3"),
        ],
        [
            Button.inline(text="减0.1", data="change_time_rate?operation=-10"),
            Button.inline(text="加0.1", data="change_time_rate?operation=10"),
        ],
        [
            Button.inline(text="减0.01", data="change_time_rate?operation=-1"),
            Button.inline(text="加0.01", data="change_time_rate?operation=1"),
        ],
        [
            Button.inline(text="确定", data="sure_time_rate"),
        ],
    ]


async def template_show_log_replyer(group, log_ups, log_downs):
    show_type = group["show_type"]
    show_type = int(show_type)

    max_key = 3
    if show_type == 2:
        max_key = 5
    elif show_type == 3:
        max_key = 1

    money_sure = 0

    ups = []
    up_count = 0
    up_money = 0
    up_money_u = 0

    downs = []
    down_count = 0
    down_money = 0
    down_money_r = 0

    # num_len = get_num_len(money_rate)
    # num_len1 = get_num_len(profit_rate)

    # if num_len1 > num_len:
    #     num_len = num_len1

    money_rate = assist.to_num(group["money_rate"])
    profit_rate = assist.to_num(group["profit_rate"])

    money_rate_change = False

    for key in range(len(log_ups)):
        log = log_ups[key]
        log = assist.handle_log_up_sql(log)

        # if log["money"] > 0:
        if log["money"] > 0 or (log["money"] < 0 and show_type == 2):
            up_count += 1
            if len(ups) < max_key:
                ups.append(log)

        up_money += log["money"]
        up_money_u += log["money"] * (100 - log["profit_rate"]) / 100 / log["money_rate"]

        money_sure += log["money"] * (100 - log["profit_rate"]) / 100

        if assist.to_num(log["money_rate"]) != money_rate:
            money_rate_change = True

    for key in range(len(log_downs)):
        log = log_downs[key]
        log = assist.handle_log_down_sql(log)

        # if log["money"] > 0:
        if log["money"] > 0 or (log["money"] < 0 and show_type == 2):
            down_count += 1
            if len(downs) < max_key:
                downs.append(log)

        down_money += log["money"]
        down_money_r += log["money"] * log["money_rate"]

        if assist.to_num(log["money_rate"]) != money_rate:
            money_rate_change = True

    ups = list(reversed(ups))
    downs = list(reversed(downs))

    text = await assist.get_ad_text()

    text += "总入（%s）：\n" % up_count
    if len(ups) == 0:
        text += " 暂无入款\n"
    else:
        for up in ups:
            money = assist.to_num(up["money"])
            money_rate_up = assist.to_num(up["money_rate"])

            temp1 = assist.to_num(up["money"] * (100 - up["profit_rate"]) / 100)
            temp2 = assist.to_num(temp1 / money_rate_up)

            text += " %s %s / %s=%su\n" % (assist.get_simple_time(up["created_at"]), temp1, money_rate_up, temp2)
    text += "\n"

    text += "总出（%s）：\n" % down_count
    if len(downs) == 0:
        text += " 暂无下发"
        text += "\n"
    else:
        for down in downs:
            money = assist.to_num(down["money"])
            money_rate_down = assist.to_num(down["money_rate"])

            text += " %s %sU (%s)\n" % (
                assist.get_simple_time(down["created_at"]), money, (assist.to_num(money * money_rate_down)))
    text += "\n"

    if show_type == 3:
        text = ""

    up_money = assist.to_num(up_money)

    money_sure = assist.to_num(money_sure)
    money_sure_u = assist.to_num(up_money_u)

    money_down = assist.to_num(down_money_r)
    money_down_u = assist.to_num(down_money)

    money_no = assist.to_num(money_sure - money_down)
    money_no_u = assist.to_num(money_sure_u - money_down_u)

    text += "总入：%s\n" % up_money
    text += "汇率：%s\n" % money_rate

    currency = "USDT"

    text += "应下：%s %s\n" % (money_sure_u, currency)
    text += "已下：%s %s\n" % (money_down_u, currency)
    text += "未下：%s %s\n" % (money_no_u, currency)

    return text


def to_num2(num):
    num_float = float(num)
    num_int = int(num_float)

    if num_int == num_float:
        return num_int

    return round(num_float, 2)
