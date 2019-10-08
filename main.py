import traceback
import time
import logging
import os
import tele_bot
import main_pars
import mapgenerator

from logging.handlers import RotatingFileHandler
from os.path import join, exists

def setup_logger():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s')

    # create console handler and set level to info
    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
 
    # create error file handler and set level to error
    target_dir = 'logs'
    if not exists(target_dir):
        os.makedirs(target_dir)

    handler = RotatingFileHandler(join(target_dir, "find-a-flat-bot.log"), encoding='utf-8', maxBytes=1024*1024*10, backupCount=5)
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(formatter)
    logger.addHandler(handler)

def main():
    setup_logger()
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
