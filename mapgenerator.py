import logging
import json
import requests
import os

token = None
try:
    token = os.environ["GEOCODETOKEN"]
except KeyError:
    logging.info("No GEOCODETOKEN environment variable found")

def get_mapimg(loc):
    if token is None:
        raise ValueError("No GEOCODETOKEN environment variable found")
    prep_loc = '+'.join(loc.split())

    url_templ = 'https://geocode-maps.yandex.ru/1.x/?format=json&apikey='+token+'&geocode=СПБ+'
    dd = requests.get(url_templ + prep_loc)
    if dd.status_code != requests.codes['ok']:
        raise RuntimeError(dd.text)
    jd = json.loads(dd.content.decode('utf-8'))
    geom_loc = jd['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos']
    imgurl_temp = 'https://static-maps.yandex.ru/1.x/?lang=ru-RU&ll={0},{1}&z=13&l=map&size=600,300&pt={0},{1},flag'
    imgurl = imgurl_temp.format(*geom_loc.split())
    return imgurl

