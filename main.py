import random
from classes.start_screen import *
from classes.zombie_cl import *
from classes.gates import *
from classes.mouse_cl import *
from classes.smoke import *
from classes.heal import *
from classes.board_w_f import *

pygame.init()
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
start_screen(screen, clock)

from classes.start_screen import *


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
        Smoke(load_image('smoke1.png'), 12, 1, p.rect.center, smokes)
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
                    Health(load_image('hpmin.png'), hp_x, health)
                else:
                    Health(load_image('hpplus.png'), hp_x, health)
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
    board = Board(current_level)
    gate = Gates(gates, current_level)
    gun = Gun()
    cur = Mos(cursor1, 500, 500, )
    board.render(all_sprite, walls, furniture)
    q = Esc(quit)
    p = AnimatedSprite(load_image("walk.png"), load_image("down.png"), load_image("up1.png"), 5, 1, 100, 100)
    p.update(0, heal=True)
    for elem in ZOMBIE_COORDS[current_level]:
        if current_level == 'level3':
            z = AnimatedSpriteZombi(load_image("boss_pered.png"), load_image('boss_zad.png'),
                                    load_image('boss_bok.png'), boss, elem, current_level)
        else:
            z = AnimatedSpriteZombi('None', 'None', load_image("zombi.png"), monsters, elem, current_level)


running = True
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
    monsters.update(p, current_level, furniture, screen)
    boss.update(p, current_level, furniture, screen)
    player.draw(screen)
    smokes.update(p.rect.center)
    smokes.draw(screen)
    blood.update()
    monsters.draw(screen)
    boss.draw(screen)
    cursor1.update(pygame.mouse.get_pos(), gun)
    cursor1.draw(screen)
    health.draw(screen)
    quit.draw(screen)
    clock.tick(FPS)
    pygame.display.flip()

pygame.quit()
