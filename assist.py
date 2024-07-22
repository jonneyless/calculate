import time
import db_redis
import html


# ======================================================================================================================

async def get_ad_text():
    yule_url = await db_redis.yule_url_get()
    if yule_url is None:
        yule_url = "https://t.me/+g3LX67Ox4pQyOGQy"
    else:
        yule_url = str(yule_url, encoding="utf-8")

    yule_text = "<a href='%s'>汇旺娱乐</a>\n" % yule_url
    text = "<a href='https://t.me/kefu'>汇旺客服</a> "
    text += yule_text
    text += "\n"

    return text


# ======================================================================================================================

def htmlspecialchars_php(temp):
    return html.escape(temp)


def handle_text(text):
    text = text.replace("'", "")
    text = text.replace("\\", "")
    text = htmlspecialchars_php(text)

    return text


def is_number(s):
    if len(s) == 0:
        return False

    try:
        float(s)
        return True
    except ValueError:
        pass
    try:
        import unicodedata
        for i in s:
            unicodedata.numeric(i)
        return True
    except (TypeError, ValueError):
        pass
    return False


def to_num(num, temp=0):
    num_float = float(num)
    num_int = int(num_float)

    if num_int == num_float:
        return num_int

    return round(num_float, 2)


def to_num2(num):
    num_float = float(num)
    num_int = int(num_float)

    if num_int == num_float:
        return num_int

    return round(num_float, 2)


def get_num_len(num):
    return 2


def get_current_time():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


def get_today_time():
    return time.strftime("%Y-%m-%d", time.localtime())


def get_current_six_time():
    today = time.strftime("%Y-%m-%d", time.localtime())
    return today + " 06:00:00"


def get_yesterday_six_time():
    today = get_today_timestamp()
    yesterday = today - 3600 * 18

    return timestamp2time(yesterday)


def get_simple_time(created_at):
    created_at = str(created_at)
    space = created_at.find(" ")
    return created_at[(space + 1):]


def time2timestamp(t, flag=True):
    if flag:
        return int(time.mktime(time.strptime(t, '%Y-%m-%d %H:%M:%S')))
    else:
        return int(time.mktime(time.strptime(t, '%Y-%m-%d')))


def timestamp2time(t):
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(t))


def get_today_timestamp():
    return time2timestamp(get_today_time(), False)


def get_current_timestamp():
    return int(time.time())


def get_created_at():
    created_at = get_current_six_time()
    now_timestamp = get_current_timestamp()
    if now_timestamp - get_today_timestamp() < 3600 * 6:
        created_at = get_yesterday_six_time()

    return created_at


def get_datetime_folder():
    return time.strftime("%Y%m%d", time.localtime())


# ======================================================================================================================

# 处理从bot接口中获得数据
def handle_user_arr(user_temp):
    user = {
        "id": user_temp["id"],
        "tg_id": user_temp["id"],
        "user_tg_id": user_temp["id"],
        "username": "",
        "firstname": "",
        "lastname": "",
        "fullname": "",
        "full_name": "",
    }

    if "username" in user_temp:
        user["username"] = user_temp["username"]
    if "first_name" in user_temp:
        user["firstname"] = user_temp["first_name"]
    if "last_name" in user_temp:
        user["lastname"] = user_temp["last_name"]

    firstname = user["firstname"]
    lastname = user["lastname"]

    firstname = handle_text(firstname)
    lastname = handle_text(lastname)
    fullname = firstname + lastname

    user["firstname"] = firstname
    user["lastname"] = lastname
    user["first_name"] = firstname
    user["last_name"] = lastname
    user["fullname"] = fullname
    user["full_name"] = fullname

    return user


# 处理telethon数据
def handle_user(user_temp):
    if not hasattr(user_temp, "id"):
        return None

    user = {
        "id": user_temp.id,
        "tg_id": user_temp.id,
        "user_tg_id": user_temp.id,
        "username": "",
        "firstname": "",
        "lastname": "",
        "fullname": "",
        "full_name": "",
    }

    if user_temp.username is not None:
        user["username"] = user_temp.username

    if hasattr(user_temp, "first_name") and (user_temp.first_name is not None):
        user["firstname"] = user_temp.first_name

    if hasattr(user_temp, "last_name") and (user_temp.last_name is not None):
        user["lastname"] = user_temp.last_name

    firstname = user["firstname"]
    lastname = user["lastname"]

    firstname = handle_text(firstname)
    lastname = handle_text(lastname)
    fullname = firstname + lastname

    user["firstname"] = firstname
    user["lastname"] = lastname
    user["first_name"] = firstname
    user["last_name"] = lastname
    user["fullname"] = fullname
    user["full_name"] = fullname

    return user


# ======================================================================================================================


def handle_user_sql(user_temp):
    user = user_temp
    user["user_tg_id"] = user_temp["user_id"]
    user["tg_id"] = user_temp["user_id"]
    user["firstname"] = user_temp["first_name"]
    user["lastname"] = user_temp["last_name"]

    return user


def handle_message_to_user_sql(message_temp):
    user = {
        "id": message_temp["user_tg_id"],
        "user_tg_id": message_temp["user_tg_id"],
        "tg_id": message_temp["user_tg_id"],
        "username": message_temp["username"],
        "firstname": message_temp["firstname"],
        "lastname": message_temp["lastname"],
    }

    firstname = user["firstname"]
    lastname = user["lastname"]

    firstname = handle_text(firstname)
    lastname = handle_text(lastname)

    user["firstname"] = firstname
    user["lastname"] = lastname

    return user


def handle_admin_sql(admin_temp):
    admin = admin_temp
    admin["user_tg_id"] = admin_temp["user_id"]
    admin["tg_id"] = admin_temp["user_id"]

    return admin


def handle_group_sql(group_temp):
    group = group_temp
    group["tg_id"] = group_temp["chat_id"]
    group["model"] = int(group_temp["model"])
    group["pay_type"] = int(group_temp["pay_type"])
    group["status"] = int(group_temp["status"])

    return group


def handle_log_up_sql(log_temp):
    return log_temp


def handle_log_down_sql(log_temp):
    return log_temp

# ======================================================================================================================
