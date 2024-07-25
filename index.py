from telethon import TelegramClient, events

import assist
import config
import db
import handle_callbackquery_message
import handle_chat_action_message
import handle_group_message
import handle_private_message
import simple_math
from helpp import reply

bot = TelegramClient('botCal', 28288600, 'b5b9051373853427d541dbd124e0202b').start(
    bot_token=config.bot_token)


@bot.on(events.NewMessage(incoming=True))
async def new_message(event):
    message = event.message
    text_full = message.text
    text = event.message.message
    chat_id = event.chat_id
    sender_id = event.sender_id

    sender = await event.get_sender()
    user = assist.handle_user(sender)
    if user is None:
        return

    if chat_id == sender_id and sender_id > 0:
        try:
            await handle_private_message.index(event, text, chat_id, user)
        except Exception as e:
            print("handle_group_message %s" % e)
    else:
        if hasattr(message, "id"):
            await db.message_save(message.id, chat_id, user)

        result_simple_math = None
        try:
            result_simple_math = simple_math.calculate_math(text)
        except Exception as e:
            print("simple_math %s" % e)

        if result_simple_math is not None:
            await reply(event, str(result_simple_math))

        await handle_group_message.index(bot, event, text, chat_id, sender_id, user)
        # try:
        #     await handle_group_message.index(bot, event, text, chat_id, sender_id, user)
        # except Exception as e:
        #     print("handle_group_message %s" % e)


@bot.on(events.ChatAction())
async def chat_action(event):
    await handle_chat_action_message.index(event, bot)


@bot.on(events.CallbackQuery())
async def callback(event):
    sender = await event.get_sender()
    user = assist.handle_user(sender)
    if user is None:
        return

    await handle_callbackquery_message.index(bot, event, user)


def main():
    bot.run_until_disconnected()


if __name__ == '__main__':
    print("init...")
    main()
