# coding=utf-8
import os
import pickle
import urllib
import logging

from urllib.request import urlopen
from parse_page import parse_page
from os import path


def generate_url(base_url, *args):
    joined_args = '&'.join(args)
    return base_url + '?' + joined_args


def get_page():
    target_url = 'https://www.avito.ru/sankt-peterburg/kvartiry/sdam/na_dlitelnyy_srok?pmax=40000&pmin=0&user=1&s_trg' \
                 '=3&metro=181-189&f=550_5702-5703.501_5153b&i=1 '
    # target_url = 'https://www.avito.ru/sankt-peterburg/kvartiry/sdam/na_dlitelnyy_srok'
    while True:
        try:
            oo = urlopen(target_url)
            break
        except urllib.error.URLError as ex:
            print("Error while urlopen: ", ex)

    logging.info(oo.getcode())
    return oo.read()


def get_ads():
    page_content = get_page()
    parse_res = parse_page(page_content)
    return parse_res


def get_new_ads():
    ads = set()

    target_dir = 'scan_results'
    if not path.exists(target_dir):
        os.makedirs(target_dir)

    dump_file_name = path.join(target_dir, 'scan.dump')
    try:
        with open(dump_file_name, 'rb') as f:
            ads = pickle.load(f)
    except (IOError, EOFError):
        pass

    parse_res = get_ads()
    diff = parse_res.difference(ads)
    if diff:
        ads.update(parse_res)
        with open(dump_file_name, 'wb') as f:
            pickle.dump(ads, f)

    return diff


if __name__ == '__main__':
    new_ads = get_new_ads()
    pass
