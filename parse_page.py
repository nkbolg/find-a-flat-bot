# coding=utf-8
import traceback
from collections import namedtuple
from datetime import date

import bs4
from bs4 import BeautifulSoup

avito_url = 'https://www.avito.ru'


def parse_price(price_str):
    price = 0
    try:
        for el in price_str.strip().split(' ')[:-1]:
            iprice = int(el)
            price *= 1000
            price += iprice
    finally:
        return price


def parse_time(time_str):
    tl = time_str.strip().split(' ')
    if len(tl) == 2:
        return True
    elif len(tl) == 3:
        if tl[1] == 'мая':
            return True
    return False


def get_img_link(img_tag):
    if not img_tag:
        return ''
    assert isinstance(img_tag, bs4.element.Tag)
    if img_tag.has_attr('data-srcpath'):
        return img_tag['data-srcpath']
    elif img_tag.has_attr('src'):
        return img_tag['src']


Ad = namedtuple('Ad', ['id', 'photo', 'title', 'price', 'loc', 'ubahn_dist', 'time', 'link'])


def get_metro_distance(ad_location):
    elements = ad_location.split(' ')
    distance = 0
    for i in range(len(elements)):
        el = elements[i]
        try:
            distance = float(el)
            break
        except ValueError:
            pass
    i += 1
    if elements[i].startswith(u'км'):
        distance *= 1000
    return distance



def parse_page(html_str):
    result = set()
    soup = BeautifulSoup(html_str, "html5lib")
    for div_class in ['js-catalog_after-ads', 'js-catalog_before-ads']:
        cont = soup.find('div', div_class)
        assert isinstance(cont, bs4.element.Tag)

        for elem in cont.find_all('div', recursive=False):
            assert isinstance(elem, bs4.element.Tag)
            if u'avito-ads-container' in elem['class']:
                continue
            try:
                ad_id = elem.get('id')[1:]
                ad_photo_link = get_img_link(elem.find('img', recursive=True))
                elem_title = elem.find('h3', 'title item-description-title')
                assert isinstance(elem_title, bs4.element.Tag)
                ad_link = elem_title.find('a').get('href')
                ad_title = elem_title.find('a').contents[0]
                ad_price = parse_price(elem.find('div', 'about').contents[0])

                ad_location = elem.find('p', 'address fader').text.strip()
                if 'м' not in ad_location or 'км' not in ad_location:
                    continue
                ad_metro_dist = get_metro_distance(ad_location)
                lil_descr_elem = elem.find('div', 'data')
                ad_time = lil_descr_elem.find('div', 'date c-2').contents[0]
                ad_time = ad_time.replace('Сегодня', str(date.today().day) + ' сентября')
                ad_time = ad_time.replace('Вчера', str(date.today().day - 1) + ' сентября')
                new_ad = Ad(
                    int(ad_id),
                    ad_photo_link,
                    ad_title.strip(),
                    str(ad_price),
                    ad_location,
                    ad_metro_dist,
                    ad_time.strip(),
                    avito_url + ad_link
                )
                result.add(new_ad)
            except Exception as ex:
                traceback.print_exc()
                continue
    return result


if __name__ == '__main__':
    with open('page_sample.htm', encoding='utf8') as f:
        dd = f.read()
    for element in parse_page(dd):
        print(element)
    pass
