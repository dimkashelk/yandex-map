import sys
import pygame
from func import *


address = 'Тамбов ул. Мичуринская д. 112В'
size = 10
map_file = f'{address}.png'
pygame.init()
screen = pygame.display.set_mode((600, 450))
save_picture(address, size)
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
                    print('Please wait...')
                    save_picture(address, size)
            elif event.key == pygame.K_PAGEUP:
                size += 1
                if size == 18:
                    size = 17
                else:
                    print('Please wait...')
                    save_picture(address, size)
    screen.blit(pygame.image.load(map_file), (0, 0))
    pygame.display.flip()
pygame.quit()
