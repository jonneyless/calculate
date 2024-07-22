from telethon.tl.types import ChannelParticipantsAdmins
import telethon

import re
import assist
import config
import db
import db_redis
import helpp
import net
import template


async def index(bot, event, text, chat_id, sender_id, user):
    if text == config.ping:
        await helpp.send(event, config.pong)
        return

    replyer = None
    if event.reply_to is not None:
        if helpp.need_replyer(text):
            reply_message_id = event.reply_to.reply_to_msg_id
            message = await db.message_one(chat_id, reply_message_id)
            if message is not None:
                replyer = assist.handle_message_to_user_sql(message)

    group = None
    entities = event.entities

    if text == "开始记账" or text == "开始":
        group = await helpp.get_group(chat_id, event)
        if group is None:
            return

        admin_flag = await helpp.is_admin(chat_id, sender_id, user)
        if not admin_flag:
            return

        admin_no_flag = await helpp.is_admin_no(chat_id, sender_id, user)
        if not admin_no_flag:
            return

        await db.group_start(group)

        await helpp.send(event, "记账功能开始工作")

        return
    elif text == "设置群操作人":
        pass
        # group = await helpp.get_group(chat_id, event)
        # if group is None:
        #     return

        # is_official = await db.official_one(sender_id)
        # if is_official is not None:
        #     admins = await net.get_admins(bot, chat_id)
        #     for admin in admins:
        #         await db.admin_save(chat_id, admin)

        #     await helpp.send(event, "设置成功，已设置群内管理为操作人")

        # return
    elif text == "设置所有人":
        pass
        # group = await helpp.get_group(chat_id, event)
        # if group is None:
        #     return

        # admin_flag = await helpp.is_admin(chat_id, sender_id, user)
        # if not admin_flag:
        #     return
        
        # admin_no_flag = await helpp.is_admin_no(chat_id, sender_id, user)
        # if not admin_no_flag:
        #     return

        # users = await db.user_gets(chat_id)
        # for user in users:
        #     await db.admin_save(chat_id, assist.handle_user_sql(user))
        # await helpp.show_admin(event, chat_id)

        # return
    elif text == "设置不允许操作人" and replyer is not None:
        group = await helpp.get_group(chat_id, event)
        if group is None:
            return

        is_official = await db.official_one(sender_id)
        if is_official is not None:
            return

        await db.admin_no_save(chat_id, replyer)
        await helpp.show_admin_no(event, chat_id)

        return
    elif text == "删除不允许操作人" and replyer is not None:
        group = await helpp.get_group(chat_id, event)
        if group is None:
            return

        is_official = await db.official_one(sender_id)
        if is_official is not None:
            return

        await db.admin_no_delete(chat_id, replyer["id"])
        await helpp.show_admin_no(event, chat_id, 2)

        return
    elif text.find("设置不允许操作人") == 0 and entities is not None:
        group = await helpp.get_group(chat_id, event)
        if group is None:
            return

        is_official = await db.official_one(sender_id)
        if is_official is not None:
            return

        for entity in entities:
            if isinstance(entity, telethon.tl.types.MessageEntityMention):
                offset = entity.offset
                length = entity.length

                username = text[(offset + 1):(offset + length)]

                await db.admin_no_save(chat_id, {
                    "tg_id": "",
                    "username": username,
                    "firstname": "",
                    "lastname": "",
                })
            if isinstance(entity, telethon.tl.types.MessageEntityMentionName):
                user_id = entity.user_id

                tg_user_in = await db.user_one(chat_id, user_id)
                if tg_user_in is not None:
                    await db.admin_no_save(chat_id, {
                        "tg_id": user_id,
                        "username": "",
                        "firstname": tg_user_in["first_name"],
                        "lastname": tg_user_in["last_name"],
                    })
                else:
                    tg_user_msg = await db.message_user_one(chat_id, user_id)
                    if tg_user_msg is not None:
                        await db.admin_no_save(chat_id, {
                            "tg_id": user_id,
                            "username": "",
                            "firstname": tg_user_msg["firstname"],
                            "lastname": tg_user_msg["lastname"],
                        })
                    else:
                        await db.admin_no_save(chat_id, {
                            "tg_id": user_id,
                            "username": "",
                            "firstname": "",
                            "lastname": "",
                        })

        await helpp.show_admin_no(event, chat_id)

        return
    elif text.find("删除不允许操作人") == 0 and entities is not None:
        group = await helpp.get_group(chat_id, event)
        if group is None:
            return

        is_official = await db.official_one(sender_id)
        if is_official is not None:
            return

        for entity in entities:
            if isinstance(entity, telethon.tl.types.MessageEntityMention):
                offset = entity.offset
                length = entity.length

                text_temp = event.message.message
                username = text_temp[(offset + 1):(offset + length)]

                await db.admin_no_delete_by_username(chat_id, username)
            if isinstance(entity, telethon.tl.types.MessageEntityMentionName):
                user_id = entity.user_id
                await db.admin_no_delete(chat_id, user_id)

        await helpp.show_admin_no(event, chat_id)

        return
    elif text == "显示不允许操作人":
        group = await helpp.get_group(chat_id, event)
        if group is None:
            return

        is_official = await db.official_one(sender_id)
        if is_official is not None:
            return

        await helpp.show_admin_no(event, chat_id, 3)

        return
    elif text == "删除账单" or text == "清理账单" or text == "清理当日账单" or text == "删除当日账单" or text == "清理今日账单" or text == "删除今日账单":
        group = await helpp.get_group(chat_id, event)
        if group is None:
            return

        admin_flag = await helpp.is_admin(chat_id, sender_id, user)
        if not admin_flag:
            return

        admin_no_flag = await helpp.is_admin_no(chat_id, sender_id, user)
        if not admin_no_flag:
            return

        await db.group_init(group)
        await db.log_up_clear_today(group)
        await db.log_down_clear_today(group)

        await helpp.send(event, "今日账单清理完成")

        return
    elif text == "删除历史账单":
        group = await helpp.get_group(chat_id, event)
        if group is None:
            return

        admin_flag = await helpp.is_admin(chat_id, sender_id, user)
        if not admin_flag:
            return

        await db.log_up_delete(chat_id)
        await db.log_down_delete(chat_id)

        await helpp.send(event, "历史账单清理完成")

        return
    elif text == "账单" and replyer is not None:
        group = await helpp.get_group(chat_id, event)
        if group is None:
            return

        admin_flag = await helpp.is_admin(chat_id, sender_id, user)
        if not admin_flag:
            return

        admin_no_flag = await helpp.is_admin_no(chat_id, sender_id, user)
        if not admin_no_flag:
            return

        await helpp.show_log_replyer(event, group, replyer)

        return
    elif (text == "账单" and replyer is None) or (text == "/我" and replyer is None):
        group = await helpp.get_group(chat_id, event)
        if group is None:
            return

        await helpp.show_log_replyer(event, group, {
            "tg_id": sender_id,
            "me": 9
        })

        return
    elif text == "显示账单" or text == "+0":
        group = await helpp.get_group(chat_id, event)
        if group is None:
            return

        admin_flag = await helpp.is_admin(chat_id, sender_id, user)
        if not admin_flag:
            return

        admin_no_flag = await helpp.is_admin_no(chat_id, sender_id, user)
        if not admin_no_flag:
            return

        await helpp.show_log(event, group)

        return
    elif text == "保存账单":
        group = await helpp.get_group(chat_id, event)
        if group is None:
            return

        admin_flag = await helpp.is_admin(chat_id, sender_id, user)
        if not admin_flag:
            return

        admin_no_flag = await helpp.is_admin_no(chat_id, sender_id, user)
        if not admin_no_flag:
            return

        await db.group_add(group)

        await helpp.send(event, "账单保存成功")

        return
    elif text == "z0" or text == "Z0":
        group = await helpp.get_group(chat_id, event)
        if group is None:
            return

        last_m_id = await db_redis.group_z0_msg_get(chat_id)
        m = await helpp.show_time_rate(bot, event, group, False, chat_id)
        if (m is not None) and (hasattr(m, "id")):
            await db_redis.group_z0_msg_set(chat_id, m.id)
        if last_m_id is not None:
            await helpp.delete(bot, chat_id, last_m_id)

        return
    elif text == "设置实时汇率":
        group = await helpp.get_group(chat_id, event)
        if group is None:
            return

        admin_flag = await helpp.is_admin(chat_id, sender_id, user)
        if not admin_flag:
            return

        admin_no_flag = await helpp.is_admin_no(chat_id, sender_id, user)
        if not admin_no_flag:
            return

        await helpp.change_time_rate(bot, event, group, False, False, False, group["seller_position"],
                                     group["pay_type"])
        return
    elif text.find("设置汇率") == 0:
        group = await helpp.get_group(chat_id, event)
        if group is None:
            return

        admin_flag = await helpp.is_admin(chat_id, sender_id, user)
        if not admin_flag:
            return

        admin_no_flag = await helpp.is_admin_no(chat_id, sender_id, user)
        if not admin_no_flag:
            return

        num = text.replace("设置汇率", "")
        if assist.is_number(num):
            num = template.to_num2(num)
            if num > 0:
                await db.group_set_money_rate(group, num)

                msg = template.template_default_money_rate(num)

                await helpp.send(event, msg)

                return
    elif text.find("设置费率") == 0:
        group = await helpp.get_group(chat_id, event)
        if group is None:
            return

        admin_flag = await helpp.is_admin(chat_id, sender_id, user)
        if not admin_flag:
            return

        admin_no_flag = await helpp.is_admin_no(chat_id, sender_id, user)
        if not admin_no_flag:
            return

        num = text.replace("设置费率", "")
        if assist.is_number(num):
            num = template.to_num2(num)
            await db.group_set_profit_rate(group, num)

            msg = template.template_default_profit_rate(num)

            await helpp.send(event, msg)

            return
    elif text.find("显示模式") == 0:
        group = await helpp.get_group(chat_id, event)
        if group is None:
            return

        admin_flag = await helpp.is_admin(chat_id, sender_id, user)
        if not admin_flag:
            return

        admin_no_flag = await helpp.is_admin_no(chat_id, sender_id, user)
        if not admin_no_flag:
            return

        num = text.replace("显示模式", "")
        num = int(num)
        if num == 1 or num == 2 or num == 3:
            await db.group_set_show_type(group, num)

            msg = template.template_show_type(num)

            await helpp.send(event, msg)

            return
    elif text.find("+") == 0 and text.find("/") > 0:
        pattern1 = "^\+(.*?)\/(.*?)$"  # +1000/10
        result1 = re.match(pattern1, text)

        if result1 is not None:
            group = await helpp.get_group(chat_id, event)
            if group is None:
                return

            admin_flag = await helpp.is_admin(chat_id, sender_id, user)
            if not admin_flag:
                return

            admin_no_flag = await helpp.is_admin_no(chat_id, sender_id, user)
            if not admin_no_flag:
                return

            money = result1.group(1)
            rate = result1.group(2)

            if assist.is_number(money) and assist.is_number(rate):
                money = template.to_num2(money)
                rate = template.to_num2(rate)
                if money > 0 and rate > 0:
                    group["money_rate_temp"] = rate
                    await helpp.save_log(event, group, money, user, config.flag_up, replyer)
                    return
        return
    elif text.find("+") == 0 or text.find("入款+") == 0:
        group = await helpp.get_group(chat_id, event)
        if group is None:
            return

        admin_flag = await helpp.is_admin(chat_id, sender_id, user)
        if not admin_flag:
            return

        admin_no_flag = await helpp.is_admin_no(chat_id, sender_id, user)
        if not admin_no_flag:
            return

        text = text.replace("入款+", "")
        num = text.replace("+", "")
        if assist.is_number(num):
            num = template.to_num2(num)
            if num > 0:
                await helpp.save_log(event, group, num, user, config.flag_up, replyer)
                return
    elif text.find("-") == 0 or text.find("入款-") == 0:
        group = await helpp.get_group(chat_id, event)
        if group is None:
            return

        admin_flag = await helpp.is_admin(chat_id, sender_id, user)
        if not admin_flag:
            return

        admin_no_flag = await helpp.is_admin_no(chat_id, sender_id, user)
        if not admin_no_flag:
            return

        text = text.replace("入款-", "")
        num = text.replace("-", "")
        if assist.is_number(num):
            num = template.to_num2(num)
            if num > 0:
                await helpp.save_log(event, group, -num, user, config.flag_up, replyer)
                return
        else:
            num_arr = num.split("/")
            if len(num_arr) == 2:
                num = num_arr[0]
                rate = num_arr[1]

                if assist.is_number(num) and assist.is_number(rate):
                    num = template.to_num2(num)
                    rate = template.to_num2(rate)

                    if num > 0 and rate > 0:
                        group["money_rate_temp"] = rate
                        await helpp.save_log(event, group, -num, user, config.flag_up, replyer)
                        return
    elif text.find("下发-") == 0:
        group = await helpp.get_group(chat_id, event)
        if group is None:
            return

        admin_flag = await helpp.is_admin(chat_id, sender_id, user)
        if not admin_flag:
            return

        admin_no_flag = await helpp.is_admin_no(chat_id, sender_id, user)
        if not admin_no_flag:
            return

        num = text.replace("下发-", "")
        if assist.is_number(num):
            num = template.to_num2(num)
            if num > 0:
                await helpp.save_log(event, group, -num, user, config.flag_down, replyer)
                return
    elif text.find("下发") == 0:
        group = await helpp.get_group(chat_id, event)
        if group is None:
            return

        admin_flag = await helpp.is_admin(chat_id, sender_id, user)
        if not admin_flag:
            return

        admin_no_flag = await helpp.is_admin_no(chat_id, sender_id, user)
        if not admin_no_flag:
            return

        num = text.replace("下发", "")
        if assist.is_number(num):
            num = template.to_num2(num)
            if num > 0:
                await helpp.save_log(event, group, num, user, config.flag_down, replyer)
                return
    elif text.find("设置更新时间") == 0:
        group = await helpp.get_group(chat_id, event)
        if group is None:
            return

        admin_flag = await helpp.is_admin(chat_id, sender_id, user)
        if not admin_flag:
            return

        admin_no_flag = await helpp.is_admin_no(chat_id, sender_id, user)
        if not admin_no_flag:
            return

        num = text.replace("设置更新时间", "")
        if assist.is_number(num):
            num = template.to_num2(num)
            if 0 <= num <= 6:
                await db.group_set_reset_hour(group, num)

                msg = template.template_set_reset_hour_ok(num)

                await helpp.send(event, msg)

            else:
                msg = template.template_set_reset_hour_error()

                await helpp.send(event, msg)
        else:
            msg = template.template_set_reset_hour_error()

            await helpp.send(event, msg)
