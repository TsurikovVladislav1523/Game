import random

import pygame
import os
import sys
from config import *

current_level = '1'


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
        self.hp = 5
        self.image = self.image.convert_alpha()
        self.rect = self.rect.move(x, y)


class Gun():
    def __init__(self):
        self.damage = LEVEL_DAMAGE[current_level]
        self.range = LEVEL_RANGE[current_level]
        self.reload = LEVEL_RELOAD[current_level]
        self.shot_t = 0

    def shot(self):
        self.shot_t = 0
        zomb = pygame.sprite.spritecollideany(cur, monsters)
        if zomb:
            if ((zomb.rect.center[1] - p.rect.center[1]) ** 2 + (
                    zomb.rect.center[0] - p.rect.center[0]) ** 2) ** 0.5 <= self.range:
                zomb.hp -= self.damage
                cursor1.update(pygame.mouse.get_pos(), change=True)


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

    def update(self, arg):
        hp_x = 1072
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
    def __init__(self, sheet_w, columns, rows, x, y, group, x0, y0, x1, y1):
        super().__init__(group)
        # x0, x1, y0, y1 координаты комнаты, в которой находится зомби
        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.hp = 4
        self.y1 = y1
        self.frames = []
        self.sheet_w = sheet_w
        self.cut_sheet(sheet_w, columns, rows)
        self.view = 0
        self.right = True
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.image = self.image.convert_alpha()
        self.rect = pygame.Rect(0, 0, 30, 38)
        self.speedx = 1
        self.speedy = 1
        self.rect = self.rect.move(x, y)

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
        if self.hp == 0:
            self.kill()
        # урон от соприкосновения
        if pygame.sprite.collide_mask(self, p):
            p.hp -= 1
        rect_x, rect_y = p.coords()
        self.view += 1
        if self.view % 10 == 0:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]
            self.image = self.image.convert_alpha()
        if not (self.x0 <= rect_x <= self.x1 and self.y0 <= rect_y <= self.y1):
            self.rect.x += self.speedx
            self.rect.y += self.speedy
            if self.rect.right >= self.x1:
                self.speedx -= 2
            if self.rect.left <= self.x0:
                self.speedx += 2
            if self.rect.top >= self.y0:
                self.speedy -= 2
            if self.rect.bottom <= self.y1:
                self.speedy += 2
            #     if pygame.sprite.spritecollideany(self, walls):
            #         self.image = pygame.transform.flip(self.image, True, False)
            #         self.rect.x -= 1
            #         self.rect.y -= 1
            # if self.right:
            #     self.rect.x += V / FPS
            # if not self.right:
            #     self.rect.x -= V / FPS
            #     if pygame.sprite.spritecollideany(self, walls):
            #         self.image = pygame.transform.flip(self.image, True, False)
            #         self.right = True
            #         self.rect.x += V / FPS
            # if pygame.sprite.spritecollideany(self, walls) and self.right:
            #     self.image = pygame.transform.flip(self.image, True, False)
            #     self.right = False
        else:
            if self.rect.x != rect_x and self.rect.y != rect_y:
                if self.rect.x > rect_x and self.rect.y > rect_y:
                    self.rect.x -= 1
                    self.rect.y -= 1
                elif self.rect.x < rect_x and self.rect.y < rect_y:
                    self.rect.x += 1
                    self.rect.y += 1
                elif self.rect.x < rect_x and self.rect.y > rect_y:
                    self.rect.x += 1
                    self.rect.y -= 1
                elif self.rect.x > rect_x and self.rect.y < rect_y:
                    self.rect.x -= 1
                    self.rect.y += 1
            elif self.rect.y != rect_y:
                if self.rect.y < rect_y:
                    self.rect.y += 1
                elif self.rect.y > rect_y:
                    self.rect.y -= 1
            elif self.rect.x != rect_x:
                if self.rect.x < rect_x:
                    self.rect.x += 1
                elif self.rect.x > rect_x:
                    self.rect.x -= 1


def terminate():
    pygame.quit()
    sys.exit()


# def start_screen():
#     fon = pygame.transform.scale(load_image('logo.png'), (W_WIDTH, W_HEIGHT))
#     screen.blit(fon, (0, 0))
#
#     while True:
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 terminate()
#             if event.type == 768 or \
#                     event.type == 1025:
#                 return None
#             pygame.display.flip()
#             clock.tick(FPS)


size = width, height = W_WIDTH, W_HEIGHT
screen = pygame.display.set_mode(size)

pygame.mouse.set_visible(False)


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


class Mos(pygame.sprite.Sprite):
    image = pygame.image.load('data/сrosshair.png')
    image_red = pygame.image.load('data/crosshair_red.png')
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
        if gun.shot_t >=120:
            self.image = self.images[0]
        if change:
            self.im_n += 1
            print(self.im_n % 2)
            self.image = self.images[self.im_n % 2]
        self.rect.center = pos


class Wall(pygame.sprite.Sprite):
    image = pygame.image.load('data/wall1.png')

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
        self.board = level1
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


clock = pygame.time.Clock()
walls = pygame.sprite.Group()
all_sprite = pygame.sprite.Group()
cursor1 = pygame.sprite.Group()
health = pygame.sprite.Group()
player = pygame.sprite.Group()
furniture = pygame.sprite.Group()
monsters = pygame.sprite.Group()
board = Board()
gun = Gun()
cur = Mos(cursor1, 500, 500)
board.render()
p = AnimatedSprite(load_image("walk.png"), load_image("down.png"), load_image("up1.png"), 5, 1, 100, 100)
z1 = AnimatedSpriteZombi(load_image("zombi.png"), 3, 1, 320, 40, monsters, 240, 40, 880, 400)
# z2 = AnimatedSpriteZombi(load_image("zombi.png"), 3, 1, 320, 140, all_sprite)

running = True
# start_screen()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                gun.shot()
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
    monsters.update()
    player.draw(screen)
    monsters.draw(screen)
    cursor1.update(pygame.mouse.get_pos())
    cursor1.draw(screen)
    health.draw(screen)
    clock.tick(FPS)
    pygame.display.flip()

pygame.quit()
