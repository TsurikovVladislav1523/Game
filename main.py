import random

import pygame
import os
from config import *


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
        self.hp = 5

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
            if pygame.sprite.spritecollideany(self, walls):
                self.rect.x += V / FPS
        elif arg == 2:
            self.tp1 = 0
            if not self.right:
                self.image = pygame.transform.flip(self.image, True, False)
                self.right = True
            self.rect.x += V / FPS
            if pygame.sprite.spritecollideany(self, walls):
                self.rect.x -= V / FPS
        elif arg == 3:
            self.tp1 = 2
            self.rect.y -= V / FPS
            if pygame.sprite.spritecollideany(self, walls):
                self.rect.y += V / FPS
        elif arg == 4:
            self.tp1 = 1
            self.rect.y += V / FPS
            if pygame.sprite.spritecollideany(self, walls):
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
        self.come_to_room = False
        # x0, x1, y0, y1 координаты комнаты, в которой находится зомби
        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
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
        self.rect = self.rect.move(x, y)
        self.x, self.y = x, y

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
        rect_x, rect_y = p.coords()
        self.view += 1
        if self.view % 10 == 0:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]
            self.image = self.image.convert_alpha()
        if not (self.x0 <= rect_x <= self.x1 and self.y0 <= rect_y <= self.y1):
            if self.right:
                self.rect.x += 2
            if not self.right:
                self.rect.x -= 2
                if pygame.sprite.spritecollideany(self, walls):
                    self.image = pygame.transform.flip(self.image, True, False)
                    self.right = True
                    self.rect.x += 2
            if pygame.sprite.spritecollideany(self, walls) and self.right:
                self.image = pygame.transform.flip(self.image, True, False)
                self.right = False
        elif self.x0 <= rect_x <= self.x1 and self.y0 <= rect_y <= self.y1:
            self.come_to_room = True
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
        if not (self.x0 <= rect_x <= self.x1 and self.y0 <= rect_y <= self.y1) and self.come_to_room:
            if self.rect.x != self.x and self.rect.y != self.y:
                if self.rect.x > self.x and self.rect.y > self.y:
                    self.rect.x -= 1
                    self.rect.y -= 1
                elif self.rect.x < self.x and self.rect.y < self.y:
                    self.rect.x += 1
                    self.rect.y += 1
                elif self.rect.x < self.x and self.rect.y > self.y:
                    self.rect.x += 1
                    self.rect.y -= 1
                elif self.rect.x > self.x and self.rect.y < self.y:
                    self.rect.x -= 1
                    self.rect.y += 1
            elif self.rect.y != self.y:
                if self.rect.y < self.y:
                    self.rect.y += 1
                elif self.rect.y > self.y:
                    self.rect.y -= 1
            elif self.rect.x != self.x:
                if self.rect.x < self.x:
                    self.rect.x += 1
                elif self.rect.x > self.x:
                    self.rect.x -= 1


size = width, height = W_WIDTH, W_HEIGHT
screen = pygame.display.set_mode(size)


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
    image = pygame.image.load('data/floor1.png')

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
        for cell_y in range(self.height):
            for cell_x in range(self.width):
                x = self.left + self.cell_size * cell_x
                y = self.top + self.cell_size * cell_y
                if self.board[cell_y][cell_x] == 0:
                    Floor(all_sprite, x, y)
                if self.board[cell_y][cell_x] == 1:
                    Wall(walls, x, y)


clock = pygame.time.Clock()
walls = pygame.sprite.Group()
all_sprite = pygame.sprite.Group()
player = pygame.sprite.Group()
board = Board()
board.render()
p = AnimatedSprite(load_image("walk.png"), load_image("down.png"), load_image("up1.png"), 5, 1, 100, 100)
z1 = AnimatedSpriteZombi(load_image("zombi.png"), 3, 1, 360, 40, all_sprite, 360, 40, 600, 320)
# z2 = AnimatedSpriteZombi(load_image("zombi.png"), 3, 1, 320, 140, all_sprite)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
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
    all_sprite.update()
    player.draw(screen)
    clock.tick(FPS)
    pygame.display.flip()

pygame.quit()
