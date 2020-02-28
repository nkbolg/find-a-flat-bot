from logger_setup import setup_logger
import logging
import traceback
import time
import tele_bot
import main_pars
import mapgenerator


def main():
    setup_logger()

    logging.info('Application started')
    users, sender = tele_bot.start_bot()
    while True:
        for uid, target_url in users:
            try:
                new_ads = main_pars.get_new_ads(uid, target_url)
                for ad in new_ads:
                    logging.info(ad)
                    msg = '\n'.join([ad.loc, ad.price, ad.link])
                    sender(uid, msg)
                    loc = ' '.join(ad.loc.split(',')[1:])
                    try:
                        sender(uid, mapgenerator.get_mapimg(loc))
                    except IndexError:
                        logging.warning("Didn't get geocode results for %s", loc)
                    except ValueError:
                        pass
            except Exception as ex:
                logging.error('Error: %s', ex)
                logging.error(traceback.format_exc())
        time.sleep(60)


if __name__ == '__main__':
    main()
