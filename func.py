import math
import requests
import sys
import pygame
from PyQt5.QtWidgets import *
from pprint import pprint

koef = {17: 2.3177083333333332e-05}


def save_picture(addr, s, m, pt=''):
    map_request = f"http://static-maps.yandex.ru/1.x/?" \
        f"ll={','.join(map(str, addr))}&" \
        f"l={m}&" \
        f"z={s}"
    if pt != '':
        map_request += f'&pt={pt}'
    response = requests.get(map_request)
    if not response:
        print("Ошибка выполнения запроса:")
        print(map_request)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        sys.exit(1)
    map_f = f"map.png"
    with open(map_f, "wb") as file:
        file.write(response.content)


def get_coords(place):
    apikey = "40d1649f-0493-4b70-98ba-98533de7710b"
    map_request = f"https://geocode-maps.yandex.ru/1.x/?geocode={place}&apikey={apikey}&format=json"
    response = requests.get(map_request)
    if not response:
        print('Try again...')
        exit(0)
    json_response = response.json()
    try:
        toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
    except IndexError:
        print('Try again...')
        exit(0)
    x, y = map(float, toponym["Point"]["pos"].split())
    return x, y


def render(screen, map_f, m, address, postal_index=False, org_info=False):
    y = 10
    screen.blit(pygame.image.load(map_f), (0, 0))
    font = pygame.font.Font(None, 38)
    text = m
    # тип карты
    string_rendered = font.render(f'Текущий тип карты: {text}', 0, pygame.Color('white'))
    intro_rect = string_rendered.get_rect()
    intro_rect.x = 610
    intro_rect.y = y
    screen.blit(string_rendered, intro_rect)
    y += 30
    # Смена режима показа
    string_rendered = font.render(f'Для смены нажмите T', 0, pygame.Color('white'))
    intro_rect = string_rendered.get_rect()
    intro_rect.x = 610
    intro_rect.y = y
    screen.blit(string_rendered, intro_rect)
    y += 30
    # включение/выключение почтового индекса
    string_rendered = font.render(f'Почтовый индекс(I)', 0, pygame.Color('white'))
    intro_rect = string_rendered.get_rect()
    intro_rect.x = 610
    intro_rect.y = y
    screen.blit(string_rendered, intro_rect)
    y += 30
    # Поиск по карте
    string_rendered = font.render(f'Для поиска нажмите F', 0, pygame.Color('white'))
    intro_rect = string_rendered.get_rect()
    intro_rect.x = 610
    intro_rect.y = y
    screen.blit(string_rendered, intro_rect)
    y += 30
    # Сброс поискового результата
    string_rendered = font.render(f'Сброс поискового результата (Q)', 0, pygame.Color('white'))
    intro_rect = string_rendered.get_rect()
    intro_rect.x = 610
    intro_rect.y = y
    screen.blit(string_rendered, intro_rect)
    y += 30
    # Полный адрес
    string_rendered = font.render(f'Полный адрес объекта:', 0, pygame.Color('white'))
    intro_rect = string_rendered.get_rect()
    intro_rect.x = 610
    intro_rect.y = y
    screen.blit(string_rendered, intro_rect)
    y += 30
    for i in range(0, len(address), 32):
        string_rendered = font.render(f'{address[i:i + 32]}', 0, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        intro_rect.x = 610
        intro_rect.y = y
        screen.blit(string_rendered, intro_rect)
        y += 30
    # почтовый индекс
    if postal_index:
        string_rendered = font.render(f'Почтовый индекс: {postal_index}', 0, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        intro_rect.x = 610
        intro_rect.y = y
        screen.blit(string_rendered, intro_rect)
        y += 30
    if org_info:
        string_rendered = font.render(f'Название организации:', 0, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        intro_rect.x = 610
        intro_rect.y = y
        screen.blit(string_rendered, intro_rect)
        y += 30
        for i in range(0, len(address), 32):
            string_rendered = font.render(f'{org_info[i:i + 32]}', 0, pygame.Color('white'))
            intro_rect = string_rendered.get_rect()
            intro_rect.x = 610
            intro_rect.y = y
            screen.blit(string_rendered, intro_rect)
            y += 30


def get_full_address(address):
    apikey = "40d1649f-0493-4b70-98ba-98533de7710b"
    map_request = f"https://geocode-maps.yandex.ru/1.x/?" \
        f"geocode={address}&" \
        f"apikey={apikey}&" \
        f"format=json"
    response = requests.get(map_request)
    if not response:
        print('Try again...')
        exit(0)
    json = response.json()
    dop = json['response']['GeoObjectCollection']['featureMember'][0]['GeoObject'][
        'metaDataProperty']['GeocoderMetaData']['Address']['Components']
    full = ''
    for i in dop:
        full += i['name'] + ', '
    return full[:-2]


def get_postal_code(address):
    apikey = "40d1649f-0493-4b70-98ba-98533de7710b"
    map_request = f"https://geocode-maps.yandex.ru/1.x/?" \
        f"geocode={address}&" \
        f"apikey={apikey}&" \
        f"format=json"
    response = requests.get(map_request)
    if not response:
        print('Try again...')
        exit(0)
    json = response.json()
    try:
        return json['response']['GeoObjectCollection']['featureMember'][0]['GeoObject'][
            'metaDataProperty']['GeocoderMetaData']['Address']['postal_code']
    except KeyError:
        return False


class Find(QWidget):

    def __init__(self):
        super().__init__()
        self.get_address = False
        self.address = ''
        self.initUI()

    def initUI(self):
        self.n, self.button_ok = QInputDialog.getText(self,
                                                      'Введите адрес',
                                                      'Введите адрес объекта',
                                                      QLineEdit.Normal)


def take_new_place(size, coords1, coords2):
    if size == 17:
        x_sdv = coords1[0] - coords2[0]
        y_sdv = coords1[1] - coords2[1]
        x_sdv *= koef[17]
        y_sdv *= koef[17]
        return x_sdv / 3, y_sdv / 4
    return 0, 0


def lonlat_distance(a, b):
    degree_to_meters_factor = 111 * 1000  # 111 километров в метрах
    a_lon, a_lat = a
    b_lon, b_lat = b
    # Берем среднюю по широте точку и считаем коэффициент для нее.
    radians_lattitude = math.radians((a_lat + b_lat) / 2.)
    lat_lon_factor = math.cos(radians_lattitude)
    # Вычисляем смещения в метрах по вертикали и горизонтали.
    dx = abs(a_lon - b_lon) * degree_to_meters_factor * lat_lon_factor
    dy = abs(a_lat - b_lat) * degree_to_meters_factor
    # Вычисляем расстояние между точками.
    distance = math.sqrt(dx * dx + dy * dy)
    return distance


def get_first_org(coords):
    search_api_server = "https://search-maps.yandex.ru/v1/"
    api_key = "dda3ddba-c9ea-4ead-9010-f43fbc15c6e3"
    search_params = {
        "apikey": api_key,
        "text": get_full_address(coords),
        "lang": "ru_RU",
        "ll": coords,
        "type": "biz",
        "spn": "0.00031799999209092267,0.00031799999209092267",
        "results": 1
    }
    res = requests.get(search_api_server, params=search_params)
    if not res:
        print('Not correct answer')
        print(res)
        exit(0)
    json_res = res.json()
    try:
        return (json_res['features'][0]['properties']['CompanyMetaData']['name'],
                json_res['features'][0]['geometry']['coordinates'])
    except IndexError:
        return (False, False)
