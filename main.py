from func import *
from copy import deepcopy

address = 'Тамбов ул. Мичуринская д. 112В'
full_address = get_full_address(address)
address_ll = list(get_coords(address))
size = 16
k = 0.0001
dop_m = {'map': 'схема', 'sat': 'спутник', 'sat,skl': 'гибрид'}
m = 'map'
map_file = f'map.png'
pt = ''
postal_index = False
pygame.init()
screen = pygame.display.set_mode((1100, 450))
save_picture(address_ll, size, m, pt)
running = True
org_info = False
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
                    save_picture(address_ll, size, m, pt)
            elif event.key == pygame.K_PAGEUP:
                size += 1
                if size == 18:
                    size = 17
                else:
                    save_picture(address_ll, size, m, pt)
            elif event.key == pygame.K_LEFT:
                address_ll[0] -= k
                if address_ll[1] == -180 - k:
                    address_ll[1] = -180
                else:
                    save_picture(address_ll, size, m, pt)
            elif event.key == pygame.K_RIGHT:
                address_ll[0] += k
                if address_ll[1] == 180 + k:
                    address_ll[1] = 180
                else:
                    save_picture(address_ll, size, m, pt)
            elif event.key == pygame.K_UP:
                address_ll[1] += k
                if address_ll[1] == -180 - k:
                    address_ll[1] = -180
                else:
                    save_picture(address_ll, size, m, pt)
            elif event.key == pygame.K_DOWN:
                address_ll[1] -= k
                if address_ll[1] == 180 + k:
                    address_ll[1] = 180
                else:
                    save_picture(address_ll, size, m, pt)
            elif event.key == pygame.K_t or event.key == (pygame.K_t + pygame.KMOD_LSHIFT):
                if m == 'map':
                    m = 'sat'
                elif m == 'sat':
                    m = 'sat,skl'
                elif m == 'sat,skl':
                    m = 'map'
                save_picture(address_ll, size, m, pt)
            elif event.key == pygame.K_f or event.key == (pygame.K_f + pygame.KMOD_LSHIFT):
                pygame.quit()
                app = QApplication(sys.argv)
                ex = Find()
                address = ex.n
                ex.close()
                app.quit()
                ex, app = None, None
                pygame.init()
                screen = pygame.display.set_mode((1100, 450))
                address_ll = list(get_coords(address))
                if pt == '':
                    pt = f'{address_ll[0]},{address_ll[1]}'
                else:
                    pt += f'~{address_ll[0]},{address_ll[1]}'
                save_picture(address_ll, size, m, pt)
                full_address = get_full_address(address)
                postal_index = False
                pt = ''
            elif event.key == pygame.K_q:
                pt = ''
                save_picture(address_ll, size, m, pt)
                full_address = ''
                postal_index = False
                org_info = False
            elif event.key == pygame.K_i:
                if not postal_index:
                    postal_index = get_postal_code(address)
                else:
                    postal_index = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                dop = list(take_new_place(size, [300, 225], list(event.pos)))
                dop_address = deepcopy(address_ll)
                dop_address[0] -= dop[0]
                dop_address[1] += dop[1]
                full_address = get_full_address(','.join(map(str, dop_address)))
                pt = f'{dop_address[0]},{dop_address[1]}'
                if postal_index:
                    postal_index = get_postal_code(full_address)
                save_picture(address_ll, size, m, pt)
            elif event.button == 3:
                if size == 17:
                    dop = list(take_new_place(size, [300, 225], list(event.pos)))
                    dop_address = deepcopy(address_ll)
                    dop_address[0] -= dop[0]
                    dop_address[1] += dop[1]
                    org_name, org_coords = get_first_org(','.join(map(str, dop_address)))
                    org_info = org_name
                    if org_info:
                        pt = f'{org_coords[0]},{org_coords[1]}'
                        save_picture(address_ll, size, m, pt)
    screen.fill((0, 0, 0))
    render(screen, map_file, dop_m[m], full_address, postal_index, org_info)
    pygame.display.flip()
pygame.quit()
