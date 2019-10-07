# coding=utf-8
import traceback

import tele_bot
import main_pars
import mapgenerator
import time
import logging

def setup_logger():
	format_str = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
	logging.basicConfig(level=logging.DEBUG,
                    format=format_str,
                    filename='find-a-flat-bot.log')
	console = logging.StreamHandler()
	console.setLevel(logging.INFO)
	console.setFormatter(logging.Formatter(format_str))
	logging.getLogger('').addHandler(console)

def main():
    # setup_logger()
    logging.info('Started')
    users, sender = tele_bot.start_bot()
    while True:
        try:
            for uid, target_url in users:
                newAds = main_pars.get_new_ads(uid, target_url)
                for ad in newAds:
                    logging.info(ad)
                    msg = '\n'.join([ad.loc, ad.price + ' руб.', ad.link])
                    sender(uid, msg)
        except Exception as ex:
            logging.info('Error: %s', ex)
            traceback.print_exc()
            continue
        finally:
            time.sleep(60)

if __name__ == '__main__':
    main()
