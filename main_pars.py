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


def get_page(target_url):
    oo = urlopen(target_url)
    logging.info(oo.getcode())
    return oo.read()


def get_ads(target_url):
    page_content = get_page(target_url)
    parse_res = parse_page(page_content)
    return parse_res


def get_new_ads(target_url):
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

    parse_res = get_ads(target_url)
    diff = parse_res.difference(ads)
    if diff:
        ads.update(parse_res)
        with open(dump_file_name, 'wb') as f:
            pickle.dump(ads, f)
    return diff


if __name__ == '__main__':
    new_ads = get_new_ads('https://www.avito.ru/sankt-peterburg/kvartiry/sdam?cd=1&pmax=43000&pmin=0&metro=157-160-164-165-173-176-180-189-191-199-205-209-210-211-1016&f=568_14011b0.550_5702-5703-5704-5705-5706')
    pass
