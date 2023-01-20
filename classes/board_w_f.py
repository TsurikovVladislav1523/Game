from classes.help_f import *
import random
from classes.furniture import *

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
    def __init__(self, current_level):  # параметры -- количество клеток по ширине и высоте
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

    def render(self, all_sprite, walls, furniture):
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
            Furniture(load_image('chair.png'), load_image('dresser.png'), load_image('table.png'), x, y, furniture)
