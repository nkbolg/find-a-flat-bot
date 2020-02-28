import os
import pickle
import logging
import requests

from parse_page import parse_page
from os import path
from collections import defaultdict


def paste(data):
    oo = requests.post('https://hastebin.com/documents', data=data.encode('utf-8'))
    return 'https://hastebin.com/' + oo.json()['key']


def get_page(target_url):
    logging.debug("GET %s", target_url)
    oo = requests.get(target_url)
    logging.debug(oo.status_code)
    return oo.text


def get_ads(target_url):
    page_content = get_page(target_url)
    try:
        parse_res = parse_page(page_content)
    except AssertionError:
        paste_url = paste(page_content)
        logging.error('Failed to parse page %s', paste_url)
        raise
    return parse_res


def get_new_ads(uid, target_url):
    ads = defaultdict(set)

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
    logging.debug("Total ads: %i", len(parse_res))
    diff = parse_res.difference(ads[uid])
    logging.debug("New ads: %i", len(diff))
    if diff:
        ads[uid].update(parse_res)
        with open(dump_file_name, 'wb') as f:
            pickle.dump(ads, f)
    return diff


if __name__ == '__main__':
    _ = paste('1231231231254')
    get_new_ads(1, 'https://www.avito.ru/sankt-peterburg/kvartiry/sdam/na_dlitelnyy_srok-ASgBAgICAkSSA8gQ8AeQUg?cd=1&metro=194&f=ASgBAQICAkSSA8gQ8AeQUgFAzAgkkFmOWQ')
    get_new_ads(9, 'https://www.avito.ru/sankt-peterburg/kvartiry/sdam/na_dlitelnyy_srok/1-komnatnye-ASgBAQICAkSSA8gQ8AeQUgFAzAgUjlk?cd=1&map=e30%3D&user=1&metro=194&f=ASgBAQICAkSSA8gQ8AeQUgJA6BYU6PwBzAgUjlk')
    new_ads = get_new_ads(0, 'https://www.avito.ru/sankt-peterburg/kvartiry/sdam?cd=1&pmax=43000&pmin=0&metro=157-160-164-165-173-176-180-189-191-199-205-209-210-211-1016&f=568_14011b0.550_5702-5703-5704-5705-5706')
    pass
