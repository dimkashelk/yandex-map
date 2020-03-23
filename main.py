import pygame
from func import *

address = 'Тамбов ул. Мичуринская д. 112В'
address_ll = list(get_coords(address))
size = 10
k = 0.0001
map_file = f'map.png'
pygame.init()
screen = pygame.display.set_mode((600, 450))
save_picture(address_ll, size)
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
                    save_picture(address_ll, size)
            elif event.key == pygame.K_PAGEUP:
                size += 1
                if size == 18:
                    size = 17
                else:
                    save_picture(address_ll, size)
            elif event.key == pygame.K_LEFT:
                address_ll[0] -= k
                if address_ll[1] == -180 - k:
                    address_ll[1] = -180
                else:
                    save_picture(address_ll, size)
            elif event.key == pygame.K_RIGHT:
                address_ll[0] += k
                if address_ll[1] == 180 + k:
                    address_ll[1] = 180
                else:
                    save_picture(address_ll, size)
            elif event.key == pygame.K_UP:
                address_ll[1] += k
                if address_ll[1] == -180 - k:
                    address_ll[1] = -180
                else:
                    save_picture(address_ll, size)
            elif event.key == pygame.K_DOWN:
                address_ll[1] -= k
                if address_ll[1] == 180 + k:
                    address_ll[1] = 180
                else:
                    save_picture(address_ll, size)
    screen.blit(pygame.image.load(map_file), (0, 0))
    pygame.display.flip()
pygame.quit()
