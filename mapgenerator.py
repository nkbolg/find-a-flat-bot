# coding=utf-8
import json
import requests


def get_mapimg(loc):
    prep_loc = u'+'.join(loc.split())

    url_templ = u'https://maps.google.com/maps/api/geocode/json?address=СПБ+'
    dd = requests.get(url_templ + prep_loc)
    jd = json.loads(dd.content)
    geom_loc = jd['results'][0]['geometry']['location']

    imgurl_temp = 'https://static-maps.yandex.ru/1.x/?lang=ru-RU&ll={0},{1}&z=13&l=map&size=600,300&pt={0},{1},flag'
    imgurl = imgurl_temp.format(geom_loc['lng'], geom_loc['lat'])
    return imgurl

