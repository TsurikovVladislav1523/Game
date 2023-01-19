import random

import pygame
import os
import sys
from config import *

pygame.init()
current_level = 'level1'
size = width, height = W_WIDTH, W_HEIGHT
screen = pygame.display.set_mode(size)
smokes = pygame.sprite.Group()
clock = pygame.time.Clock()
walls = pygame.sprite.Group()
gates = pygame.sprite.Group()
all_sprite = pygame.sprite.Group()
cursor1 = pygame.sprite.Group()
health = pygame.sprite.Group()
player = pygame.sprite.Group()
furniture = pygame.sprite.Group()
monsters = pygame.sprite.Group()
blood = pygame.sprite.Group()
boss = pygame.sprite.Group()
quit = pygame.sprite.Group()


def load_image(name, color_key=None):
    fullname = os.path.join(ASSETS_DIR, name)
    image = pygame.image.load(fullname)
    if color_key is not None:
        image = image.convert()
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image


class Gates(pygame.sprite.Sprite):
    open = load_image('opendoor.png')
    close = load_image('closedoor.png')

    def __init__(self):
        super().__init__(gates)
        self.image = self.close
        self.kills = False
        self.rect = self.image.get_rect()
        self.image = self.image.convert_alpha()
        self.rect = self.rect.move(LEVEL_GATES[current_level])

    def update(self):
        self.kills = True
        self.image = self.open


class Smoke(pygame.sprite.Sprite):
    def __init__(self, sheet_w, columns, rows, pos):
        super().__init__(smokes)
        self.frames = []
        self.sheet_d = sheet_w
        self.cut_sheet(sheet_w, columns, rows)
        self.view = 0
        self.tp1 = 0
        self.right = True
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.image = self.image.convert_alpha()
        self.rect = pygame.Rect(0, 0, 30, 38)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.center = (pos[0] - 5, pos[1])
        self.hp = 2

    def cut_sheet(self, sheet, columns, rows):
        self.frames.clear()
        rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                           sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (rect.w * i, rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, rect.size)))

    def update(self, pos):
        self.view += 1
        if self.cur_frame + 1 == len(self.frames):
            self.kill()
            return None
        if self.view % 3 == 0:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]
            self.image = self.image.convert_alpha()
        self.rect.center = (pos[0] - 5, pos[1])


class New_game(pygame.sprite.Sprite):
    image1 = load_image('new.png')
    image_ch = load_image('new_ch.png')

    def __init__(self, new):
        super().__init__(new)
        self.image = self.image1
        self.rect = self.image.get_rect()
        self.image = self.image.convert_alpha()
        self.rect.center = (960, 650)

    def update(self, cur_image):
        self.image = cur_image


class Save_im(pygame.sprite.Sprite):
    image1 = load_image('save.png')
    image_ch = load_image('save_ch.png')

    def __init__(self, save):
        super().__init__(save)
        self.image = self.image1
        self.rect = self.image.get_rect()
        self.rect.center = (960, 300)

    def update(self, cur_image):
        self.image = cur_image


class Save_im_end(pygame.sprite.Sprite):
    image1 = load_image('end_of_game.png')

    def __init__(self, save):
        super().__init__(save)
        self.image = self.image1
        self.rect = self.image.get_rect()
        self.rect.center = (960, 300)

    def update(self, cur_image):
        self.image = cur_image


class Health(pygame.sprite.Sprite):
    def __init__(self, image, x):
        super().__init__(health)
        self.image = image
        self.rect = self.image.get_rect()
        self.image = self.image.convert_alpha()
        self.rect = self.rect.move(x, 5)


class Furniture(pygame.sprite.Sprite):
    def __init__(self, image1, image2, image3, x, y):
        super().__init__(furniture)
        self.image = random.choice([image1, image2, image3])
        self.rect = self.image.get_rect()
        self.hp = 2
        self.image = self.image.convert_alpha()
        self.rect = self.rect.move(x, y)


def start_screen():
    global current_level
    pygame.mixer.music.load('music/menutheme.mp3')
    pygame.mixer.music.play()
    fon = pygame.transform.scale(load_image('logo.png'), (W_WIDTH, W_HEIGHT))
    screen.blit(fon, (0, 0))
    save = pygame.sprite.Group()
    new = pygame.sprite.Group()
    save1 = Save_im(save)
    new1 = New_game(new)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if save1.rect.collidepoint(pygame.mouse.get_pos()):
                    f = open("save.txt", mode="r")
                    current_level = f.read()
                    f.close()
                    return None
                elif new1.rect.collidepoint(pygame.mouse.get_pos()):
                    current_level = 'level1'
                    f = open("input.txt", mode="w")
                    print(f, current_level)
                    f.close()
                    return None
            if save1.rect.collidepoint(pygame.mouse.get_pos()):
                save.update(load_image('save_ch.png'))
            elif new1.rect.collidepoint(pygame.mouse.get_pos()):
                new.update(load_image('new_ch.png'))
            else:
                new.update(load_image('new.png'))
                save.update(load_image('save.png'))

            save.draw(screen)
            new.draw(screen)
            pygame.display.flip()
            clock.tick(FPS)


def end_screen():
    fon = pygame.transform.scale(load_image('end_of_game.png'), (W_WIDTH, W_HEIGHT))
    screen.blit(fon, (0, 0))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == 1025 or event.type == pygame.KEYDOWN:
                return None
        pygame.display.flip()
        clock.tick(FPS)


class Gun():
    def __init__(self):
        self.damage = LEVEL_DAMAGE[current_level]
        self.range = LEVEL_RANGE[current_level]
        self.reload = LEVEL_RELOAD[current_level]
        self.shot_t = 250

    def shot(self):
        smokes.empty()
        Smoke(load_image('smoke1.png'), 12, 1, p.rect.center)
        zomb = pygame.sprite.spritecollideany(cur, monsters)
        if zomb:
            if ((zomb.rect.center[1] - p.rect.center[1]) ** 2 + (
                    zomb.rect.center[0] - p.rect.center[0]) ** 2) ** 0.5 <= self.range and self.shot_t >= self.reload:
                zomb.hp -= self.damage
                cursor1.update(pygame.mouse.get_pos(), change=True)
                self.shot_t = 0
        furn = pygame.sprite.spritecollideany(cur, furniture)
        if furn:
            if ((furn.rect.center[1] - p.rect.center[1]) ** 2 + (
                    furn.rect.center[0] - p.rect.center[0]) ** 2) ** 0.5 <= self.range and self.shot_t >= self.reload:
                furn.hp -= 1
            if furn.hp == 0:
                furn.kill()


class Esc(pygame.sprite.Sprite):
    image = load_image('esc.png')

    def __init__(self, quiq):
        super().__init__(quiq)
        self.image = self.image
        self.rect = self.image.get_rect()
        self.rect.center = (1900, 20)


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sheet_w, sheet_d, sheet_u, columns, rows, x, y):
        super().__init__(player)
        self.frames = []
        self.sheet_d = sheet_d
        self.sheet_w = sheet_w
        self.sheet_u = sheet_u
        self.cut_sheet(sheet_w, columns, rows)
        self.view = 0
        self.tp1 = 0
        self.right = True
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.image = self.image.convert_alpha()
        self.rect = pygame.Rect(0, 0, 30, 38)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.rect.move(x, y)
        self.hp = HP[current_level]

    def cut_sheet(self, sheet, columns, rows):
        self.frames.clear()
        rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                           sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (rect.w * i, rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, rect.size)))

    def update(self, arg, heal=False):
        hp_x = 1072
        if heal:
            if self.hp <= 0:
                end_screen()
                load_level()
                return None
            health.empty()
            for i in range(8):
                hp_x += 40
                if i >= self.hp:
                    Health(load_image('hpmin.png'), hp_x)
                else:
                    Health(load_image('hpplus.png'), hp_x)

        self.tp2 = self.tp1
        self.view += 1
        if self.view % 10 == 0:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]
            self.image = self.image.convert_alpha()
            if not self.right:
                self.image = pygame.transform.flip(self.image, True, False)
        self.mask = pygame.mask.from_surface(self.image)
        if arg == 1:
            self.tp1 = 0
            if self.right:
                self.image = pygame.transform.flip(self.image, True, False)
                self.right = False
            self.rect.x -= V / FPS
            if pygame.sprite.spritecollideany(self, walls) or pygame.sprite.spritecollideany(self, furniture):
                self.rect.x += V / FPS
        elif arg == 2:
            self.tp1 = 0
            if not self.right:
                self.image = pygame.transform.flip(self.image, True, False)
                self.right = True
            self.rect.x += V / FPS
            if pygame.sprite.spritecollideany(self, walls) or pygame.sprite.spritecollideany(self, furniture):
                self.rect.x -= V / FPS
        elif arg == 3:
            self.tp1 = 2
            self.rect.y -= V / FPS
            if pygame.sprite.spritecollideany(self, walls) or pygame.sprite.spritecollideany(self, furniture):
                self.rect.y += V / FPS
        elif arg == 4:
            self.tp1 = 1
            self.rect.y += V / FPS
            if pygame.sprite.spritecollideany(self, walls) or pygame.sprite.spritecollideany(self, furniture):
                self.rect.y -= V / FPS
            if pygame.sprite.spritecollideany(self, gates) and gate.kills:
                print(000)
                start_screen()
        if self.tp2 != self.tp1:
            if self.tp1 == 0:
                self.cut_sheet(self.sheet_w, 5, 1)
                self.cur_frame = 0
                self.image = self.frames[self.cur_frame]
                self.image = self.image.convert_alpha()
            elif self.tp1 == 1:
                self.cut_sheet(self.sheet_d, 5, 1)
                self.cur_frame = 0
                self.image = self.frames[self.cur_frame]
                self.image = self.image.convert_alpha()
            elif self.tp1 == 2:
                self.cut_sheet(self.sheet_u, 5, 1)
                self.cur_frame = 0
                self.image = self.frames[self.cur_frame]
                self.image = self.image.convert_alpha()

    def coords(self):
        return self.rect.left, self.rect.top


class AnimatedSpriteZombi(pygame.sprite.Sprite):
    def __init__(self, sheet_p, sheet_z, sheet_b, group, tp):
        # columns, rows, x, y, x0, y0, x1, y1
        super().__init__(group)
        # x0, x1, y0, y1 координаты комнаты, в которой находится зомби
        self.frames = []
        self.x0 = tp[4]
        self.y0 = tp[5]
        self.x1 = tp[6]
        self.y1 = tp[7]
        if current_level == 'level3':
            self.sheet_z = sheet_z
            self.sheet_p = sheet_p
            self.rect = pygame.Rect(0, 0, 40, 46)
        self.sheet_b = sheet_b
        self.cut_sheet(sheet_b, tp[0], tp[1])
        self.come = False
        self.hp = LEVEL_ZOMBIE_HP[current_level]
        self.view = 0
        self.right = True
        self.down = False
        self.up = False
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.image = self.image.convert_alpha()
        self.rect = pygame.Rect(0, 0, 30, 38)
        self.speedx = 1
        self.speedy = 1
        # для отстлеживания ударов о мебель
        self.count = 0
        self.direction = False
        self.rect = self.rect.move(tp[2], tp[3])

    def cut_sheet(self, sheet, columns, rows):
        self.frames.clear()
        rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                           sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (rect.w * i, rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, rect.size)))

    def update(self):
        if self.hp <= 0:
            self.kill()
        # урон от соприкосновения
        rect_x, rect_y = p.coords()
        if abs(self.rect.x - rect_x) <= 10 and abs(self.rect.y - rect_y) <= 10:
            self.attack(self.right, self.rect, p.rect.centerx - 20, p.rect.centery - 11)
            p.hp -= 1
            p.update(0, heal=True)
        self.view += 1
        if self.view % 10 == 0:
            if current_level == 'level3':
                if self.up and not self.down:
                    self.cut_sheet(self.sheet_z, 3, 1)
                    self.cur_frame = 0
                    self.image = self.frames[self.cur_frame]
                    self.image = self.image.convert_alpha()
                if self.down and not self.up:
                    self.cut_sheet(self.sheet_p, 3, 1)
                    self.cur_frame = 0
                    self.image = self.frames[self.cur_frame]
                    self.image = self.image.convert_alpha()
                if not self.down and not self.up:
                    self.cut_sheet(self.sheet_b, 3, 1)
                    self.cur_frame = 0
                    self.image = self.frames[self.cur_frame]
                    self.image = self.image.convert_alpha()
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]
            self.image = self.image.convert_alpha()
            if not self.right:
                self.image = pygame.transform.flip(self.image, True, False)

        if not (self.x0 <= rect_x <= self.x1 and self.y0 <= rect_y <= self.y1):
            self.rect.x += self.speedx
            self.rect.y += self.speedy
            if pygame.sprite.spritecollideany(self, furniture):
                self.speedx = -self.speedx
                self.count += 1
                if self.right:
                    self.image = pygame.transform.flip(self.image, True, False)
                    self.right = False
                elif not self.right:
                    self.image = pygame.transform.flip(self.image, True, False)
                    self.right = True
                if self.count > 1:
                    self.speedy = -self.speedy
                    self.speedx = -self.speedx
                    if self.right:
                        self.image = pygame.transform.flip(self.image, True, False)
                        self.right = False
                    elif not self.right:
                        self.image = pygame.transform.flip(self.image, True, False)
                        self.right = True
                    self.count = 0
            if self.rect.right >= self.x1:
                if self.right:
                    self.image = pygame.transform.flip(self.image, True, False)
                    self.right = False
                self.speedx -= 2
            if self.rect.left <= self.x0:
                if not self.right:
                    self.image = pygame.transform.flip(self.image, True, False)
                    self.right = True
                self.speedx += 2
            if self.rect.top >= self.y0:
                self.speedy -= 2
            if self.rect.bottom <= self.y1:
                self.speedy += 2
        else:
            self.come = True
            if self.rect.x != rect_x and self.rect.y != rect_y:
                if self.rect.x > rect_x and self.rect.y > rect_y:
                    if self.right:
                        self.image = pygame.transform.flip(self.image, True, False)
                        self.right = False
                    self.rect.x -= 1
                    self.rect.y -= 1
                elif self.rect.x < rect_x and self.rect.y < rect_y:
                    if not self.right:
                        self.image = pygame.transform.flip(self.image, True, False)
                        self.right = True
                    self.rect.x += 1
                    self.rect.y += 1
                elif self.rect.x < rect_x and self.rect.y > rect_y:
                    if not self.right:
                        self.image = pygame.transform.flip(self.image, True, False)
                        self.right = True
                    self.rect.x += 1
                    self.rect.y -= 1
                elif self.rect.x > rect_x and self.rect.y < rect_y:
                    if self.right:
                        self.image = pygame.transform.flip(self.image, True, False)
                        self.right = False
                    self.rect.x -= 1
                    self.rect.y += 1
            elif self.rect.y != rect_y:
                if self.rect.y < rect_y:
                    self.rect.y += 1
                    if current_level == 'level3':
                        self.down, self.up = True, False
                elif self.rect.y > rect_y:
                    self.rect.y -= 1
                    if current_level == 'level3':
                        self.down, self.up = False, True
            elif self.rect.x != rect_x:
                if self.rect.x < rect_x:
                    if not self.right:
                        self.image = pygame.transform.flip(self.image, True, False)
                        self.right = True
                    self.rect.x += 1
                elif self.rect.x > rect_x:
                    if self.right:
                        self.image = pygame.transform.flip(self.image, True, False)
                        self.right = False
                    self.rect.x -= 1
                if current_level == 'level3':
                    self.down, self.up = False, False

    def attack(self, dir, z_rect, p_x, p_y):
        p.hp -= LEVEL_DAMAGE[current_level]
        Blood(blood, dir, z_rect, p_x, p_y)
        blood.draw(screen)


def terminate():
    pygame.quit()
    sys.exit()


class Blood(pygame.sprite.Sprite):
    image = load_image('blood.png', -1)

    def __init__(self, group, dir, z_rect, x, y):
        super().__init__(group)
        self.image = Blood.image
        self.dir = dir
        self.z_rect = z_rect
        self.x = x
        self.y = y
        self.count = 0
        self.image = self.image.convert()
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(self.x, self.y)

    def update(self):
        self.kill()


class Mos(pygame.sprite.Sprite):
    image = load_image('crosshair.png')
    image_red = load_image('crosshair_red.png')
    images = [image, image_red]

    def __init__(self, group, x, y):
        super().__init__(group)
        self.im_n = 0
        self.image = Mos.images[self.im_n]
        self.image = self.image.convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self, pos, change=False):
        gun.shot_t += 1
        if gun.shot_t >= 120:
            self.image = self.images[0]
        if change:
            self.im_n += 1
            self.image = self.images[self.im_n % 2]
        self.rect.center = pos


class Wall(pygame.sprite.Sprite):
    image = load_image('wall1.png')

    def __init__(self, group, x, y):
        super().__init__(group)
        self.image = Wall.image
        self.image = self.image.convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Floor(pygame.sprite.Sprite):
    image = load_image('floor1.png')

    def __init__(self, group, x, y):
        super().__init__(group)
        self.image = self.image.convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Board:
    def __init__(self):  # параметры -- количество клеток по ширине и высоте
        self.width = 48
        self.height = 27
        self.board = LEVELS[current_level]
        self.left = 0  # x верхнего левого угла поля
        self.top = 0  # у левого верхнего угла
        self.cell_size = 40

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self):
        random_floors = []
        for cell_y in range(self.height):
            for cell_x in range(self.width):
                x = self.left + self.cell_size * cell_x
                y = self.top + self.cell_size * cell_y
                if self.board[cell_y][cell_x] == 0:
                    Floor(all_sprite, x, y)
                    random_floors.append((x + 2, y + 2))
                if self.board[cell_y][cell_x] == 1:
                    Wall(walls, x, y)
        for i in range(10):
            x, y = random.choice(random_floors)
            Furniture(load_image('chair.png'), load_image('dresser.png'), load_image('table.png'), x, y)


def load_level():
    smokes.empty()
    walls.empty()
    gates.empty()
    all_sprite.empty()
    cursor1.empty()
    health.empty()
    quit.empty()
    player.empty()
    furniture.empty()
    monsters.empty()
    boss.empty()
    blood.empty()
    global board, gate, gun, cur, p
    board = Board()
    gate = Gates()
    gun = Gun()
    cur = Mos(cursor1, 500, 500)
    board.render()
    q = Esc(quit)
    p = AnimatedSprite(load_image("walk.png"), load_image("down.png"), load_image("up1.png"), 5, 1, 100, 100)
    p.update(0, heal=True)
    for elem in ZOMBIE_COORDS[current_level]:
        if current_level == 'level3':
            z = AnimatedSpriteZombi(load_image("boss_pered.png"), load_image('boss_zad.png'),
                                    load_image('boss_bok.png'), boss, elem)
        else:
            z = AnimatedSpriteZombi('None', 'None', load_image("zombi.png"), monsters, elem)


running = True
start_screen()
pygame.mixer.music.stop()
load_level()
p.update(0, heal=True)
pygame.mouse.set_visible(False)
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 3 and gate.kills and ((gate.rect.center[1] - p.rect.center[1]) ** 2 + (
                    gate.rect.center[0] - p.rect.center[0]) ** 2) ** 0.5 <= 80:
                if int(current_level[-1]) < 3:
                    current_level = current_level[:-1] + str(int(current_level[-1]) + 1)
                load_level()
            if event.button == 1:
                gun.shot()
                if pygame.sprite.spritecollideany(cur, quit):
                    f = open("save.txt", mode="w")
                    f.write(current_level)
                    f.close()
                    terminate()
        if not monsters:
            gates.update()
    pressed_k = pygame.key.get_pressed()
    if pressed_k[pygame.K_a]:
        player.update(1)
    elif pressed_k[pygame.K_d]:
        player.update(2)
    elif pressed_k[pygame.K_w]:
        player.update(3)
    elif pressed_k[pygame.K_s]:
        player.update(4)

    screen.fill(pygame.Color('black'))
    all_sprite.draw(screen)
    walls.draw(screen)
    furniture.draw(screen)
    gates.draw(screen)
    monsters.update()
    boss.update()
    player.draw(screen)
    smokes.update(p.rect.center)
    smokes.draw(screen)
    blood.update()
    monsters.draw(screen)
    boss.draw(screen)
    cursor1.update(pygame.mouse.get_pos())
    cursor1.draw(screen)
    health.draw(screen)
    quit.draw(screen)
    clock.tick(FPS)
    pygame.display.flip()

pygame.quit()
