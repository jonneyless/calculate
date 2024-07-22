import assist
import db
import helpp
import template


async def index(bot, event, user):
    chat_id = event.chat_id
    sender_id = event.sender_id
    msg_id = event.query.msg_id

    group = await db.group_one(chat_id)
    if group is None:
        return
    group = assist.handle_group_sql(group)

    admin_flag = await helpp.is_admin(chat_id, sender_id, user)
    if not admin_flag:
        return

    callback_data = event.query.data
    callback_data = callback_data.decode('utf-8')

    args = {}
    info = callback_data
    if callback_data.find("?") >= 0:
        arr = callback_data.split("?")
        if len(arr) == 2:
            info = arr[0]
            args_temp = arr[1]

            args_temp = args_temp.split("&")
            for item in args_temp:
                item = item.split("=")
                if len(item) == 2:
                    args[item[0]] = item[1]

    if info == "show_time_rate":
        await helpp.show_time_rate(bot, event, group, True, chat_id, msg_id, args["pay_method"])
    elif info == "change_time_rate":
        if "seller_position" in args:
            seller_position = args["seller_position"]
            await db.group_set_seller_position(group, seller_position)
        if "pay_method" in args:
            pay_method = args["pay_method"]
            await db.group_set_pay_type(group, pay_method)
        if "operation" in args:
            operation = int(args["operation"])
            if operation > 0:
                if operation == 1:
                    await db.group_add_little_price_change(group)
                elif operation == 10:
                    await db.group_add_little_price_change_ten(group)
            if operation < 0:
                if operation == -1:
                    await db.group_sub_little_price_change(group)
                elif operation == -10:
                    await db.group_sub_little_price_change_ten(group)

        await helpp.change_time_rate(bot, event, group, True, chat_id, msg_id, group["seller_position"],
                                     group["pay_type"])
    elif info == "sure_time_rate":
        await db.group_set_time_rate(group)
        current_price = await helpp.get_current_price(group)

        await helpp.send(event, template.template_time_money_rate(current_price))

        await helpp.delete(bot, chat_id, msg_id)
