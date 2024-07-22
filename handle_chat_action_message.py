import telethon
import telethon.tl.types
from telethon import functions

import assist
import config
import db
import helpp


async def index(event, bot):
    chat_id = event.chat_id

    action_message = event.action_message
    if action_message is None:
        return

    if not hasattr(action_message, "action"):
        return

    action = action_message.action
    from_id = action_message.from_id

    if isinstance(action, telethon.tl.types.MessageActionChatAddUser):
        users = action.users
        for user_id in users:
            if int(user_id) == int(config.bot_tg_id):
                await helpp.init_chat(bot, event, chat_id)
            else:
                newer = None
                try:
                    newer = await bot.get_entity(user_id)
                except Exception as e:
                    print("get_entity error:%s" % e)
                if newer is None:
                    continue

                newer = assist.handle_user(newer)
                if newer is not None:
                    await db.user_save(chat_id, newer)
                    await helpp.set_official_user(chat_id, newer)
    elif isinstance(action, telethon.tl.types.MessageActionChatJoinedByLink):
        if not hasattr(from_id, "user_id"):
            return
        user_id = from_id.user_id

        newer = None
        try:
            newer = await bot.get_entity(user_id)
        except Exception as e:
            print("get_entity error:%s" % e)
        if newer is None:
            return

        newer = assist.handle_user(newer)
        if newer is not None:
            await db.user_save(chat_id, newer)
            await helpp.set_official_user(chat_id, newer)
