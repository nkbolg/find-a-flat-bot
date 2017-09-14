from telegram.ext import Updater
import os

token = os.environ['find-a-flat-token']

ch_id = -1001128165084


def start_bot():
    updater = Updater(token)
    updater.start_polling()

    def sender(msg):
        if msg.startswith('http'):
            updater.bot.send_photo(ch_id, msg)
        else:
            updater.bot.send_message(ch_id, msg)

    return updater.stop, sender
