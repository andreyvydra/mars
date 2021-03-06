import sys
from io import BytesIO

import requests
from PIL import Image


def geocode(address):
    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

    geocoder_params = {
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "geocode": address,
        "format": "json"}

    response = requests.get(geocoder_api_server, params=geocoder_params)

    if not response:
        # обработка ошибочной ситуации
        pass

    # Преобразуем ответ в json-объект
    json_response = response.json()
    # Получаем первый топоним из ответа геокодера.
    toponym = json_response["response"]["GeoObjectCollection"][
        "featureMember"][0]["GeoObject"]
    return toponym


def get_coordinates(address):
    toponym = geocode(address)
    toponym_coodrinates = toponym["Point"]["pos"]
    toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")
    return float(toponym_longitude), float(toponym_lattitude)


def get_points(address):
    toponym = geocode(address)
    toponym_dots = toponym["boundedBy"]["Envelope"]
    left_point, right_point = toponym_dots['lowerCorner'], toponym_dots['upperCorner']
    left_point = list(map(float, left_point.split()))
    right_point = list(map(float, right_point.split()))
    return left_point, right_point


def get_city(address):
    toponym = geocode(address)
    city_name = toponym['metaDataProperty']['GeocoderMetaData']['Address']['Components'][-1]['name']
    return city_name


def save_map(ll, spn, l='map', pt=None):
    map_params = {
        "ll": ll,
        "spn": spn,
        "l": l
    }
    if pt is not None:
        map_params['pt'] = pt

    map_api_server = "http://static-maps.yandex.ru/1.x/"
    response = requests.get(map_api_server, params=map_params)

    with open('static/img/map.png', 'wb') as file:
        file.write(response.content)


def get_spn(point1, point2):
    spn_x = abs(point1[0] - point2[0]) / 2
    spn_y = abs(point1[1] - point2[1]) / 2
    return ','.join([str(spn_x), str(spn_y)])
