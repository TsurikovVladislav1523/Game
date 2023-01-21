import random
from all_for_project.start_screen import *
from all_for_project.zombie_cl import *
from all_for_project.gates import *
from all_for_project.mouse_cl import *
from all_for_project.smoke import *
from all_for_project.heal import *
from all_for_project.board_w_f import *
from all_for_project.end_screen import *
from all_for_project.gun import *
from all_for_project.esc import *
from all_for_project.load_level import *
from all_for_project.pers import *

pygame.init()
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
quits = pygame.sprite.Group()
start_screen(screen, clock)

from all_for_project.start_screen import *

running = True
pygame.mixer.music.stop()
load_level(smokes, walls, gates, all_sprite, cursor1, health, player, furniture, monsters, boss, current_level, quits,
           clock)

from all_for_project.load_level import *

p.update(0, smokes, walls, gates, all_sprite, cursor1, health, player, furniture, monsters, boss,
         current_level,
         quits, clock, heal=False)
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
                load_level(smokes, walls, gates, all_sprite, cursor1, health, player, furniture, monsters, boss,
                           current_level,
                           quits,
                           clock)

                from all_for_project.load_level import *
            if event.button == 1:
                gun.shot(smokes, p, cur, monsters, furniture, cursor1, boss)
                if pygame.sprite.spritecollideany(cur, quits):
                    f = open("save.txt", mode="w")
                    f.write(current_level)
                    f.close()
                    terminate()
        if not monsters:
            gates.update()
    pressed_k = pygame.key.get_pressed()
    if pressed_k[pygame.K_a]:
        player.update(1, smokes, walls, gates, all_sprite, cursor1, health, player, furniture, monsters, boss,
                      current_level,
                      quits, clock)
    elif pressed_k[pygame.K_d]:
        player.update(2, smokes, walls, gates, all_sprite, cursor1, health, player, furniture, monsters, boss,
                      current_level,
                      quits, clock)
    elif pressed_k[pygame.K_w]:
        player.update(3, smokes, walls, gates, all_sprite, cursor1, health, player, furniture, monsters, boss,
                      current_level,
                      quits, clock)
    elif pressed_k[pygame.K_s]:
        player.update(4, smokes, walls, gates, all_sprite, cursor1, health, player, furniture, monsters, boss,
                      current_level,
                      quits, clock)

    screen.fill(pygame.Color('black'))
    all_sprite.draw(screen)
    walls.draw(screen)
    furniture.draw(screen)
    gates.draw(screen)
    monsters.update(p, current_level, furniture, screen, clock, health, walls, smokes, gates, all_sprite, cursor1,
                    player, monsters, boss, quits)
    boss.update(p, current_level, furniture, screen, clock, health, walls, smokes, gates, all_sprite, cursor1, player,
                monsters, boss, quits)
    player.draw(screen)
    if p.restart:
        p.restart = False
        load_level(smokes, walls, gates, all_sprite, cursor1, health, player, furniture, monsters, boss, current_level,
                   quits, clock)

        from all_for_project.load_level import *
    smokes.update(p.rect.center)
    smokes.draw(screen)
    blood.update()
    monsters.draw(screen)
    boss.draw(screen)
    cursor1.update(pygame.mouse.get_pos(), gun)
    cursor1.draw(screen)
    health.draw(screen)
    quits.draw(screen)
    clock.tick(FPS)
    pygame.display.flip()

pygame.quit()
