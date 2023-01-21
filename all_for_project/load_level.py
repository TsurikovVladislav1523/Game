from all_for_project.help_f import *
from all_for_project.zombie_cl import *
from all_for_project.board_w_f import *
from all_for_project.gates import *
from all_for_project.esc import *
from all_for_project.gates import *
from all_for_project.gates import *
from all_for_project.mouse_cl import *
from all_for_project.pers import *


def load_level(smokes, walls, gates, all_sprite, cursor1, health, player, furniture, monsters, boss, current_level,
               quits, clock):
    smokes.empty()
    walls.empty()
    gates.empty()
    all_sprite.empty()
    cursor1.empty()
    health.empty()
    quits.empty()
    player.empty()
    furniture.empty()
    monsters.empty()
    boss.empty()
    blood.empty()
    global board, gate, gun, cur, p
    board = Board(current_level)
    gate = Gates(gates, current_level)
    cur = Mos(cursor1, 500, 500, )
    board.render(all_sprite, walls, furniture)
    q = Esc(quits)
    p = Pers(load_image("walk.png"), load_image("down.png"), load_image("up1.png"), 5, 1, 100, 100, player,
             current_level)
    p.update(0, smokes, walls, gates, all_sprite, cursor1, health, player, furniture, monsters, boss,
             current_level,
             quits, clock, heal=True)
    gun = Gun(current_level)
    for elem in ZOMBIE_COORDS[current_level]:
        if current_level == 'level3':
            z = AnimatedSpriteZombi(load_image("boss_pered.png"), load_image('boss_zad.png'),
                                    load_image('boss_bok.png'), boss, elem, current_level)
        else:
            z = AnimatedSpriteZombi('None', 'None', load_image("zombi.png"), monsters, elem, current_level)
