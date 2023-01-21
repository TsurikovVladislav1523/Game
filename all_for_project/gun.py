from all_for_project.help_f import *
from all_for_project.smoke import *


class Gun():
    def __init__(self, current_level):
        self.damage = LEVEL_DAMAGE_P[current_level]
        self.range = LEVEL_RANGE[current_level]
        self.reload = LEVEL_RELOAD[current_level]
        self.shot_t = 250

    def shot(self, smokes, p, cur, monsters, furniture, cursor1, boss):
        smokes.empty()
        Smoke(load_image('smoke1.png'), 12, 1, p.rect.center, smokes)
        zomb = pygame.sprite.spritecollideany(cur, monsters)
        if zomb:
            if ((zomb.rect.center[1] - p.rect.center[1]) ** 2 + (
                    zomb.rect.center[0] - p.rect.center[0]) ** 2) ** 0.5 <= self.range and self.shot_t >= self.reload:
                zomb.hp -= self.damage
                cursor1.update(pygame.mouse.get_pos(), self, change=True)
                self.shot_t = 0
        zomb = pygame.sprite.spritecollideany(cur, boss)
        if zomb:
            if ((zomb.rect.center[1] - p.rect.center[1]) ** 2 + (
                    zomb.rect.center[0] - p.rect.center[0]) ** 2) ** 0.5 <= self.range and self.shot_t >= self.reload:
                zomb.hp -= self.damage
                cursor1.update(pygame.mouse.get_pos(), self, change=True)
                self.shot_t = 0
        furn = pygame.sprite.spritecollideany(cur, furniture)
        if furn:
            if ((furn.rect.center[1] - p.rect.center[1]) ** 2 + (
                    furn.rect.center[0] - p.rect.center[0]) ** 2) ** 0.5 <= self.range and self.shot_t >= self.reload:
                furn.hp -= 1
            if furn.hp == 0:
                furn.kill()
