import requests
import sys


def save_picture(addr, s):
    map_request = f"http://static-maps.yandex.ru/1.x/?" \
        f"ll={','.join(map(str, get_coords(addr)))}&" \
        f"l=map&" \
        f"z={s}"
    response = requests.get(map_request)
    if not response:
        print("Ошибка выполнения запроса:")
        print(map_request)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        sys.exit(1)
    map_f = f"{addr}.png"
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
