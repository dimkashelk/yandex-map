import requests
import sys
import pygame
from PyQt5.QtWidgets import *


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


def render(screen, map_f, m):
    screen.blit(pygame.image.load(map_f), (0, 0))
    font = pygame.font.Font(None, 38)
    text = m
    string_rendered = font.render(f'Текущий тип карты: {text}', 0, pygame.Color('white'))
    intro_rect = string_rendered.get_rect()
    intro_rect.x = 610
    intro_rect.y = 10
    screen.blit(string_rendered, intro_rect)
    string_rendered = font.render(f'Для смены нажмите T', 0, pygame.Color('white'))
    intro_rect = string_rendered.get_rect()
    intro_rect.x = 610
    intro_rect.y = 40
    screen.blit(string_rendered, intro_rect)
    string_rendered = font.render(f'Для поиска нажмите F', 0, pygame.Color('white'))
    intro_rect = string_rendered.get_rect()
    intro_rect.x = 610
    intro_rect.y = 70
    screen.blit(string_rendered, intro_rect)
    # Сброс поискового результата
    string_rendered = font.render(f'Сброс поискового результата (Q)', 0, pygame.Color('white'))
    intro_rect = string_rendered.get_rect()
    intro_rect.x = 610
    intro_rect.y = 100
    screen.blit(string_rendered, intro_rect)


class Find(QWidget):

    def __init__(self):
        super().__init__()
        self.get_address = False
        self.address = ''
        self.initUI()

    def initUI(self):
        self.n, self.button_ok = QInputDialog.getText(self,
                                                      'Введите полный адрес',
                                                      'Введите полный адрес объекта',
                                                      QLineEdit.Normal)
