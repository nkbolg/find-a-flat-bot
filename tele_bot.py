from telegram.ext import Updater
import os

token = ''

ch_id = -1001128165084

# os.environ['HTTPS_PROXY'] = 'socks5://127.0.0.1:52820'
# os.environ['HTTPS_PROXY'] = 'socks5://127.0.0.1:52821'
proxy = {
    'proxy_url': 'socks5://127.0.0.1:52820',
    'read_timeout': 26, 'connect_timeout': 27
}


def start_bot():
    updater = Updater(token, request_kwargs=proxy)
    updater.start_polling()

    def sender(msg):
        if msg.startswith('http'):
            updater.bot.send_photo(ch_id, msg)
        else:
            updater.bot.send_message(ch_id, msg)

    return updater.stop, sender
