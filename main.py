import sys
import pygame
from func import *

response = None
address = 'Тамбов ул. Мичуринская д. 112В'
size = 0.001
map_request = f"http://static-maps.yandex.ru/1.x/?ll={','.join(map(str, get_coords(address)))}&spn={size},{size}&l=map"
response = requests.get(map_request)

if not response:
    print("Ошибка выполнения запроса:")
    print(map_request)
    print("Http статус:", response.status_code, "(", response.reason, ")")
    sys.exit(1)

map_file = f"{address}.png"
with open(map_file, "wb") as file:
    file.write(response.content)
pygame.init()
screen = pygame.display.set_mode((600, 450))
screen.blit(pygame.image.load(map_file), (0, 0))
pygame.display.flip()
while pygame.event.wait().type != pygame.QUIT:
    pass
pygame.quit()
