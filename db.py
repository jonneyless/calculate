from assist import get_current_time, get_created_at
from dbpool import OPMysql
import db_redis
from config import flag_up, flag_down


# ======================================================================================================================

async def user_one(chat_id, user_id):
    opm = OPMysql()

    select_sql = "select * from `ins` where chat_id = %s and user_id = %s"

    result = opm.op_safe_select_one(select_sql, (chat_id, user_id,))

    opm.dispose()

    return result


async def user_gets(chat_id):
    opm = OPMysql()

    select_sql = "select * from `ins` where chat_id = %s"

    result = opm.op_safe_select_all(select_sql, (chat_id,))

    opm.dispose()

    return result


async def user_save(chat_id, newer):
    group_user = await user_one(chat_id, newer["tg_id"])
    if group_user is not None:
        return

    opm = OPMysql()

    save_sql = "insert into `ins`(chat_id, user_id, username, first_name, last_name, created_at) values(%s, %s, %s, %s, %s, %s)"

    result = opm.op_safe_update(save_sql, (
        chat_id, newer["tg_id"], newer["username"], newer["firstname"], newer["lastname"], get_current_time(),))

    opm.dispose()

    return result


# ======================================================================================================================

async def admin_one(chat_id, admin_id):
    opm = OPMysql()

    select_sql = "select id from chat_admin where chat_id = %s and user_id = %s"

    result = opm.op_safe_select_one(select_sql, (chat_id, admin_id,))

    opm.dispose()

    return result


async def admin_one_by_username(chat_id, username):
    opm = OPMysql()

    select_sql = "select id from chat_admin where chat_id = %s and username = %s"

    result = opm.op_safe_select_one(select_sql, (chat_id, username,))

    opm.dispose()

    return result


async def admin_gets(chat_id):
    opm = OPMysql()

    select_sql = "select * from chat_admin where chat_id = %s"

    result = opm.op_safe_select_all(select_sql, (chat_id,))

    opm.dispose()

    return result


async def admin_save(chat_id, admin):
    if admin["tg_id"]:
        obj = await admin_one(chat_id, admin["tg_id"])
        if obj is not None:
            return
    else:
        if len(admin["username"]) > 0:
            obj = await admin_one_by_username(chat_id, admin["username"])
            if obj is not None:
                return

    opm = OPMysql()

    save_sql = "insert into chat_admin(chat_id, user_id, username, firstname, lastname) values(%s, %s, %s, %s, %s)"

    result = opm.op_safe_update(save_sql, (
        chat_id, admin["tg_id"], admin["username"], admin["firstname"], admin["lastname"],))

    opm.dispose()

    return result


async def admin_delete_all(chat_id):
    opm = OPMysql()

    update_sql = "delete from chat_admin where chat_id = %s"

    result = opm.op_safe_update(update_sql, (chat_id,))

    opm.dispose()

    return result


async def admin_delete(chat_id, admin_id):
    opm = OPMysql()

    update_sql = "delete from chat_admin where chat_id = %s and user_id = %s"

    result = opm.op_safe_update(update_sql, (chat_id, admin_id,))

    opm.dispose()

    return result


async def admin_delete_by_username(chat_id, username):
    opm = OPMysql()

    update_sql = "delete from chat_admin where chat_id = %s and username = %s"

    result = opm.op_safe_update(update_sql, (chat_id, username,))

    opm.dispose()

    return result


# ======================================================================================================================

async def message_user_one(chat_id, user_tg_id):
    opm = OPMysql()

    select_sql = "select * from messages where group_tg_id = %s and user_tg_id = %s"

    result = opm.op_safe_select_one(select_sql, (chat_id, user_tg_id,))

    opm.dispose()

    return result


async def message_one(chat_id, message_tg_id):
    opm = OPMysql()

    select_sql = "select * from messages where group_tg_id = %s and tg_id = %s"

    result = opm.op_safe_select_one(select_sql, (chat_id, message_tg_id,))

    opm.dispose()

    return result


async def message_save(id, chat_id, sender):
    opm = OPMysql()

    save_sql = "insert into messages(tg_id, group_tg_id, user_tg_id, username, firstname, lastname, created_at) values(%s,%s, %s, %s, %s, %s, %s)"

    result = opm.op_safe_update(save_sql, (
        id, chat_id, sender["user_tg_id"], sender["username"], sender["firstname"], sender["lastname"],
        get_current_time(),))

    opm.dispose()

    return result


# ======================================================================================================================

async def group_one(chat_id):
    opm = OPMysql()

    select_sql = "select * from chats where chat_id = %s"

    result = opm.op_safe_select_one(select_sql, (chat_id,))

    opm.dispose()

    return result


async def group_set_title(group, title):
    opm = OPMysql()

    update_sql = "update chats set title = %s where id = %s"

    result = opm.op_safe_update(update_sql, (title, group["id"],))

    opm.dispose()

    return result


async def group_delete(chat_id):
    opm = OPMysql()

    update_sql = "delete from chats where chat_id = %s"

    result = opm.op_safe_update(update_sql, (chat_id,))

    opm.dispose()

    return result


async def group_save(chat_id, title, group_type="supergroup"):
    opm = OPMysql()

    save_sql = "insert into chats(chat_id, title, group_type, created_at, welcome_info) values(%s, %s, %s, %s, %s)"

    result = opm.op_safe_update(save_sql, (
        chat_id, title, group_type, get_current_time(), ""))

    opm.dispose()

    return result


async def group_start(group):
    opm = OPMysql()

    update_sql = "update chats set status = 1 where id = %s"

    result = opm.op_safe_update(update_sql, (group["id"],))

    opm.dispose()

    return result


async def group_set_time_rate(group):
    opm = OPMysql()

    update_sql = "update chats set model = 1 where id = %s"

    result = opm.op_safe_update(update_sql, (group["id"],))

    opm.dispose()

    return result


async def group_set_seller_position(group, seller_position):
    opm = OPMysql()

    update_sql = "update chats set seller_position = %s where id = %s"

    result = opm.op_safe_update(update_sql, (seller_position, group["id"],))

    opm.dispose()

    return result


async def group_set_pay_type(group, pay_type):
    opm = OPMysql()

    update_sql = "update chats set pay_type = %s where id = %s"

    result = opm.op_safe_update(update_sql, (pay_type, group["id"],))

    opm.dispose()

    return result


async def group_add_little_price_change(group):
    opm = OPMysql()

    update_sql = "update chats set little_price_change = little_price_change + 0.01 where id = %s"

    result = opm.op_safe_update(update_sql, (group["id"],))

    opm.dispose()

    return result


async def group_sub_little_price_change(group):
    opm = OPMysql()

    update_sql = "update chats set little_price_change = little_price_change - 0.01 where id = %s"

    result = opm.op_safe_update(update_sql, (group["id"],))

    opm.dispose()

    return result


async def group_add_little_price_change_ten(group):
    opm = OPMysql()

    update_sql = "update chats set little_price_change = little_price_change + 0.1 where id = %s"

    result = opm.op_safe_update(update_sql, (group["id"],))

    opm.dispose()

    return result


async def group_sub_little_price_change_ten(group):
    opm = OPMysql()

    update_sql = "update chats set little_price_change = little_price_change - 0.1 where id = %s"

    result = opm.op_safe_update(update_sql, (group["id"],))

    opm.dispose()

    return result


async def group_set_money_rate(group, rate, model=2):
    opm = OPMysql()

    update_sql = "update chats set model = %s, money_rate = %s where id = %s"

    result = opm.op_safe_update(update_sql, (model, rate, group["id"],))

    opm.dispose()

    return result


async def group_set_profit_rate(group, rate):
    opm = OPMysql()

    update_sql = "update chats set profit_rate = %s where id = %s"

    result = opm.op_safe_update(update_sql, (rate, group["id"],))

    opm.dispose()

    return result


async def group_set_show_type(group, show_type):
    opm = OPMysql()

    update_sql = "update chats set show_type = %s where id = %s"

    result = opm.op_safe_update(update_sql, (show_type, group["id"],))

    opm.dispose()

    return result


async def group_add(group):
    opm = OPMysql()

    update_sql = "update chats set type = type + 1 where id = %s"

    result = opm.op_safe_update(update_sql, (group["id"],))

    opm.dispose()

    return result


async def group_init(group):
    opm = OPMysql()

    update_sql = "update chats set profit_rate = 0, money_rate = 0, model = 1, show_type = 1, little_price_change = 0 where id = %s"

    result = opm.op_safe_update(update_sql, (group["id"],))

    opm.dispose()

    return result


async def group_set_reset_hour(group, reset_hour):
    opm = OPMysql()

    update_sql = "update chats set reset_hour = %s where id = %s"

    result = opm.op_safe_update(update_sql, (reset_hour, group["id"],))

    opm.dispose()

    return result


# ======================================================================================================================

async def log_up_one(group):
    opm = OPMysql()

    select_sql = "select * from log_up where chat_id = %s and type = %s and is_deleted = 2 "

    result = opm.op_safe_select_one(select_sql, (
        group["id"], group["type"],))

    opm.dispose()

    return result


async def log_up_get(group, created_at):
    opm = OPMysql()

    select_sql = "select * from log_up where chat_id = %s and type = %s and is_deleted = 2 and created_at >= %s order by id desc"

    result = opm.op_safe_select_all(select_sql, (
        group["id"], group["type"], created_at,))

    opm.dispose()

    return result


async def log_up_get_by_replyer(group, replyer_tg_id, created_at):
    opm = OPMysql()

    select_sql = "select * from log_up where chat_id = %s and reply_user_id = %s and type = %s and is_deleted = 2 and created_at >= %s order by id desc"
    result = opm.op_safe_select_all(select_sql, (
        group["id"], replyer_tg_id, group["type"], created_at,))

    opm.dispose()

    return result


async def log_up_delete(chat_id):
    opm = OPMysql()

    update_sql = "update log_up set is_deleted = 1 where tg_chat_id = %s"

    result = opm.op_safe_update(update_sql, (chat_id,))

    opm.dispose()

    return result


async def log_up_save(group, money, money_rate, profit_rate, fromer, replyer=None):
    currency = ""
    if replyer is None:
        replyer = {
            "tg_id": "",
            "username": "",
            "firstname": "",
            "lastname": "",
        }

    opm = OPMysql()

    save_sql = "insert into log_up(model, type, chat_id, tg_chat_id, money, currency, money_rate, profit_rate, user_id, username, firstname, lastname, reply_user_id, reply_username, reply_firstname, reply_lastname, created_at) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    result = opm.op_safe_update(save_sql, (
        group["model"], group["type"], group["id"], group["chat_id"], money, currency, money_rate, profit_rate,
        fromer["tg_id"], fromer["username"], fromer["firstname"], fromer["lastname"],
        replyer["tg_id"], replyer["username"], replyer["firstname"], replyer["lastname"], get_current_time(),))

    opm.dispose()

    await db_redis.cal_data_set({
        "chat_id": group["id"],
        "tg_chat_id": group["chat_id"],
        "type": "up"
    })

    return result


async def log_up_clear_today(group):
    opm = OPMysql()

    update_sql = "update log_up set is_deleted = 1 where chat_id = %s and created_at >= %s"

    result = opm.op_safe_update(update_sql, (
        group["id"], get_created_at(),))

    opm.dispose()

    await db_redis.cal_data_set({
        "chat_id": group["id"],
        "tg_chat_id": group["chat_id"],
        "type": "delete"
    })

    return result


# ======================================================================================================================

async def log_down_one(group):
    opm = OPMysql()

    select_sql = "select * from log_down where chat_id = %s and type = %s and is_deleted = 2 "

    result = opm.op_safe_select_one(select_sql, (
        group["id"], group["type"],))

    opm.dispose()

    return result


async def log_down_get(group, created_at):
    opm = OPMysql()

    select_sql = "select * from log_down where chat_id = %s and type = %s and is_deleted = 2 and created_at >= %s order by id desc"

    result = opm.op_safe_select_all(select_sql, (
        group["id"], group["type"], created_at,))

    opm.dispose()

    return result


async def log_down_get_replyer(group, replyer_tg_id, created_at):
    opm = OPMysql()

    select_sql = "select * from log_down where chat_id = %s and reply_user_id = %s and type = %s and is_deleted = 2 and created_at >= %s order by id desc"

    result = opm.op_safe_select_all(select_sql, (
        group["id"], replyer_tg_id, group["type"], created_at,))

    opm.dispose()

    return result


async def log_down_delete(chat_id):
    opm = OPMysql()

    update_sql = "update log_down set is_deleted = 1 where tg_chat_id = %s"

    result = opm.op_safe_update(update_sql, (chat_id,))

    opm.dispose()

    return result


async def log_down_save(group, money, money_rate, profit_rate, fromer, replyer=None):
    currency = ""
    if replyer is None:
        replyer = {
            "tg_id": "",
            "username": "",
            "firstname": "",
            "lastname": "",
        }

    opm = OPMysql()

    save_sql = "insert into log_down(model, type, chat_id, tg_chat_id, money, currency, money_rate, profit_rate, user_id, username, firstname, lastname, reply_user_id, reply_username, reply_firstname, reply_lastname, created_at) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

    result = opm.op_safe_update(save_sql, (
        group["model"], group["type"], group["id"], group["chat_id"], money, currency, money_rate, profit_rate,
        fromer["tg_id"], fromer["username"], fromer["firstname"], fromer["lastname"],
        replyer["tg_id"], replyer["username"], replyer["firstname"], replyer["lastname"], get_current_time(),))

    opm.dispose()

    await db_redis.cal_data_set({
        "chat_id": group["id"],
        "tg_chat_id": group["chat_id"],
        "type": "down"
    })

    return result


async def log_down_clear_today(group):
    opm = OPMysql()

    update_sql = "update log_down set is_deleted = 1 where chat_id = %s and created_at >= %s"

    result = opm.op_safe_update(update_sql, (
        group["id"], get_created_at(),))

    opm.dispose()

    return result


# ======================================================================================================================

async def offical_gets():
    opm = OPMysql()

    select_sql = "select tg_id, username from offical_user"

    result = opm.op_safe_select_all(select_sql)

    opm.dispose()

    return result


async def official_one(tg_id):
    opm = OPMysql()

    select_sql = "select tg_id, username from offical_user where tg_id = %s"

    result = opm.op_safe_select_one(select_sql, (tg_id,))

    opm.dispose()

    return result


# ======================================================================================================================

async def bot_one(tg_id):
    opm = OPMysql()

    select_sql = "select id from bots where tg_id = %s"

    result = opm.op_safe_select_one(select_sql, (tg_id,))

    opm.dispose()

    return result


async def allow_one(bot_id, user_tg_id):
    opm = OPMysql()

    select_sql = "select id from allow_lists where bot_id = %s and tg_id = %s"

    result = opm.op_safe_select_one(select_sql, (bot_id, user_tg_id))

    opm.dispose()

    return result


# ======================================================================================================================

async def admin_no_one(chat_id, admin_id):
    opm = OPMysql()

    select_sql = "select id from chat_admin_no where chat_id = %s and user_id = %s"

    result = opm.op_safe_select_one(select_sql, (chat_id, admin_id,))

    opm.dispose()

    return result


async def admin_no_one_by_username(chat_id, username):
    opm = OPMysql()

    select_sql = "select id from chat_admin_no where chat_id = %s and username = %s"

    result = opm.op_safe_select_one(select_sql, (chat_id, username,))

    opm.dispose()

    return result


async def admin_no_gets(chat_id):
    opm = OPMysql()

    select_sql = "select * from chat_admin_no where chat_id = %s"

    result = opm.op_safe_select_all(select_sql, (chat_id,))

    opm.dispose()

    return result


async def admin_no_save(chat_id, admin):
    if admin["tg_id"]:
        obj = await admin_no_one(chat_id, admin["tg_id"])
        if obj is not None:
            return
    else:
        if len(admin["username"]) > 0:
            obj = await admin_no_one_by_username(chat_id, admin["username"])
            if obj is not None:
                return

    opm = OPMysql()

    save_sql = "insert into chat_admin_no(chat_id, user_id, username, firstname, lastname) values(%s, %s, %s, %s, %s)"

    result = opm.op_safe_update(save_sql, (
        chat_id, admin["tg_id"], admin["username"], admin["firstname"], admin["lastname"],))

    opm.dispose()

    return result


async def admin_no_delete_all(chat_id):
    opm = OPMysql()

    update_sql = "delete from chat_admin_no where chat_id = %s"
    print(chat_id)
    print(update_sql)

    result = opm.op_safe_update(update_sql, (chat_id,))

    opm.dispose()

    return result


async def admin_no_delete(chat_id, admin_id):
    opm = OPMysql()

    update_sql = "delete from chat_admin_no where chat_id = %s and user_id = %s"

    result = opm.op_safe_update(update_sql, (chat_id, admin_id,))

    opm.dispose()

    return result


async def admin_no_delete_by_username(chat_id, username):
    opm = OPMysql()

    update_sql = "delete from chat_admin_no where chat_id = %s and username = %s"

    result = opm.op_safe_update(update_sql, (chat_id, username,))

    opm.dispose()

    return result
    