import pygame
from func import *


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


address = 'Тамбов ул. Мичуринская д. 112В'
address_ll = list(get_coords(address))
size = 10
k = 0.0001
dop_m = {'map': 'схема', 'sat': 'спутник', 'sat,skl': 'гибрид'}
m = 'map'
map_file = f'map.png'
pygame.init()
screen = pygame.display.set_mode((1000, 450))
save_picture(address_ll, size, m)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_PAGEDOWN:
                size -= 1
                if size == -1:
                    size = 0
                else:
                    save_picture(address_ll, size, m)
            elif event.key == pygame.K_PAGEUP:
                size += 1
                if size == 18:
                    size = 17
                else:
                    save_picture(address_ll, size, m)
            elif event.key == pygame.K_LEFT:
                address_ll[0] -= k
                if address_ll[1] == -180 - k:
                    address_ll[1] = -180
                else:
                    save_picture(address_ll, size, m)
            elif event.key == pygame.K_RIGHT:
                address_ll[0] += k
                if address_ll[1] == 180 + k:
                    address_ll[1] = 180
                else:
                    save_picture(address_ll, size, m)
            elif event.key == pygame.K_UP:
                address_ll[1] += k
                if address_ll[1] == -180 - k:
                    address_ll[1] = -180
                else:
                    save_picture(address_ll, size, m)
            elif event.key == pygame.K_DOWN:
                address_ll[1] -= k
                if address_ll[1] == 180 + k:
                    address_ll[1] = 180
                else:
                    save_picture(address_ll, size, m)
            elif event.key == pygame.K_t or event.key == (pygame.K_t + pygame.KMOD_LSHIFT):
                if m == 'map':
                    m = 'sat'
                elif m == 'sat':
                    m = 'sat,skl'
                elif m == 'sat,skl':
                    m = 'map'
                save_picture(address_ll, size, m)
    screen.fill((0, 0, 0))
    render(screen, map_file, dop_m[m])
    pygame.display.flip()
pygame.quit()
