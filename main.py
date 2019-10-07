# coding=utf-8
import traceback

import tele_bot
import main_pars
import mapgenerator
import time
import logging

logging.getLogger().setLevel(logging.DEBUG)
logging.basicConfig(format='%(levelname)s -- %(asctime)s -- %(message)s')

def main():
    logging.info('Started')
    users, sender = tele_bot.start_bot()
    while True:
        try:
            for uid, target_url in users:
                newAds = main_pars.get_new_ads(target_url)
                for ad in newAds:
                    logging.info(ad)
                    msg = '\n'.join([ad.loc, ad.price + ' руб.', ad.link])
                    sender(uid, msg)
                    # loc = ' '.join(ad.loc.split(',')[1:])
                    # sender(uid, mapgenerator.get_mapimg(loc))
        except Exception as ex:
            logging.info('Error: %s', ex)
            traceback.print_exc()
            continue
        finally:
            time.sleep(60)

if __name__ == '__main__':
    main()
