from classes.help_f import *


class Gates(pygame.sprite.Sprite):
    open = load_image('opendoor.png')
    close = load_image('closedoor.png')

    def __init__(self, gates, current_level):
        super().__init__(gates)
        self.image = self.close
        self.kills = False
        self.rect = self.image.get_rect()
        self.image = self.image.convert_alpha()
        self.rect = self.rect.move(LEVEL_GATES[current_level])

    def update(self):
        self.kills = True
        self.image = self.open
