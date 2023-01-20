import random
from classes.help_f import *

class Furniture(pygame.sprite.Sprite):
    def __init__(self, image1, image2, image3, x, y, furniture):
        super().__init__(furniture)
        self.image = random.choice([image1, image2, image3])
        self.rect = self.image.get_rect()
        self.hp = 2
        self.image = self.image.convert_alpha()
        self.rect = self.rect.move(x, y)
