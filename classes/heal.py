from classes.help_f import *

class Health(pygame.sprite.Sprite):
    def __init__(self, image, x, health):
        super().__init__(health)
        self.image = image
        self.rect = self.image.get_rect()
        self.image = self.image.convert_alpha()
        self.rect = self.rect.move(x, 5)
