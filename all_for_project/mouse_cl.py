from all_for_project.help_f import *

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

    def update(self, pos, gun, change=False):
        gun.shot_t += 1
        if gun.shot_t >= 120:
            self.image = self.images[0]
        if change:
            self.im_n += 1
            self.image = self.images[self.im_n % 2]
        self.rect.center = pos