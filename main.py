# coding=utf-8
import traceback
from operator import attrgetter

import tele_bot
import main_pars
import mapgenerator
import time


if __name__ == '__main__':
    print('Started')
    _, sender = tele_bot.start_bot()
    while True:
        try:
            newAds = list(main_pars.get_new_ads())
            # newAds.sort(key=timeSorter)
            for ad in newAds:
                if ad.ubahn_dist > 1500:
                    continue
                msg = '\n'.join([ad.loc, ad.price + ' руб.', ad.link])
                sender(msg)
                loc = ' '.join(ad.loc.split(',')[1:])
                sender(mapgenerator.get_mapimg(loc))
        except Exception as ex:
            print('Error: ', ex)
            traceback.print_exc()
            continue
        finally:
            time.sleep(60)
