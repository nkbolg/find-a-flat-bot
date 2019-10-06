from telegram.ext import Updater, CommandHandler
import signal
import pickle
import os
import sys
token = os.environ["FINDAFLATTOKEN"]
# find-a-flat channel:
# ch_id = -1001128165084
uids = set()
stop = None
if os.path.exists('uid'):
    with open('uid', 'rb') as f:
        uids = pickle.load(f)


def signal_handler(sig, frame):
    with open('uid', 'wb') as f:
        pickle.dump(uids, f)
    if stop:
        stop()
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)


def new_user(bot, update, arg):
    uids.add(update.message.chat_id)
    bot.send_message(chat_id=update.message.chat_id, text="Hello! Now you'll receive notifications." \
                                                          "Say /stop to disable")
    from main_pars import target_url
    target_url = arg


def delete_user(bot, update):
    uids.remove(update.message.chat_id)
    bot.send_message(chat_id=update.message.chat_id, text="Notifications disabled")


def start_bot():
    updater = Updater(token)
    start_handler = CommandHandler('start', new_user, pass_args=True)
    delete_handler = CommandHandler('stop', delete_user)
    updater.dispatcher.add_handler(start_handler)
    updater.dispatcher.add_handler(delete_handler)
    updater.start_polling()

    def sender(msg):
        for u in uids:
            if msg.startswith('http'):
                print(msg)
                updater.bot.send_photo(u, msg, timeout=20)
            else:
                updater.bot.send_message(u, msg, timeout=20)
    global stop
    stop = updater.stop
    return updater.stop, sender
