from all_for_project.help_f import *


class Esc(pygame.sprite.Sprite):
    image = load_image('esc.png')

    def __init__(self, quiq):
        super().__init__(quiq)
        self.image = self.image
        self.rect = self.image.get_rect()
        self.rect.center = (1900, 20)
