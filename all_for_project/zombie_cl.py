from all_for_project.help_f import *

blood = pygame.sprite.Group()


class Blood(pygame.sprite.Sprite):
    def __init__(self, group, dir, z_rect, x, y, image):
        super().__init__(group)
        self.image = image
        self.dir = dir
        self.z_rect = z_rect
        self.x = x
        self.y = y
        self.count = 0
        self.image = self.image.convert()
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(self.x, self.y)

    def update(self):
        self.kill()


class AnimatedSpriteZombi(pygame.sprite.Sprite):
    def __init__(self, sheet_p, sheet_z, sheet_b, group, tp, current_level):
        # columns, rows, x, y, x0, y0, x1, y1
        super().__init__(group)
        # x0, x1, y0, y1 координаты комнаты, в которой находится зомби
        self.frames = []
        self.x0 = tp[4]
        self.y0 = tp[5]
        self.x1 = tp[6]
        self.y1 = tp[7]
        if current_level == 'level3':
            self.sheet_z = sheet_z
            self.sheet_p = sheet_p
            self.rect = pygame.Rect(0, 0, 40, 46)
        self.sheet_b = sheet_b
        self.cut_sheet(sheet_b, tp[0], tp[1])
        self.come = False
        self.hp = LEVEL_ZOMBIE_HP[current_level]
        self.view = 0
        self.right = True
        self.down = False
        self.up = False
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.image = self.image.convert_alpha()
        self.rect = pygame.Rect(0, 0, 30, 38)
        self.speedx = 1
        self.speedy = 1
        # для отстлеживания ударов о мебель
        self.count = 0
        self.direction = False
        self.rect = self.rect.move(tp[2], tp[3])

    def cut_sheet(self, sheet, columns, rows):
        self.frames.clear()
        rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                           sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (rect.w * i, rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, rect.size)))

    def update(self, p, current_level, furniture, screen, clock, health, walls, smokes, gates, all_sprite, cursor1,
               player, monsters, boss, quits):
        if self.hp <= 0:
            self.kill()
        # урон от соприкосновения
        rect_x, rect_y = p.coords()
        if abs(self.rect.x - rect_x) <= 10 and abs(self.rect.y - rect_y) <= 10:
            self.attack(self.right, self.rect, p.rect.centerx - 20, p.rect.centery - 11, p, current_level, screen)
            p.hp -= 1
            p.update(0, smokes, walls, gates, all_sprite, cursor1, health, player, furniture, monsters, boss,
                     current_level,
                     quits, clock, heal=True)
        self.view += 1
        if self.view % 10 == 0:
            if current_level == 'level3':
                if self.up and not self.down:
                    self.cut_sheet(self.sheet_z, 3, 1)
                    self.cur_frame = 0
                    self.image = self.frames[self.cur_frame]
                    self.image = self.image.convert_alpha()
                if self.down and not self.up:
                    self.cut_sheet(self.sheet_p, 3, 1)
                    self.cur_frame = 0
                    self.image = self.frames[self.cur_frame]
                    self.image = self.image.convert_alpha()
                if not self.down and not self.up:
                    self.cut_sheet(self.sheet_b, 3, 1)
                    self.cur_frame = 0
                    self.image = self.frames[self.cur_frame]
                    self.image = self.image.convert_alpha()
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]
            self.image = self.image.convert_alpha()
            if not self.right:
                self.image = pygame.transform.flip(self.image, True, False)

        if not (self.x0 <= rect_x <= self.x1 and self.y0 <= rect_y <= self.y1):
            self.rect.x += self.speedx
            self.rect.y += self.speedy
            if pygame.sprite.spritecollideany(self, furniture):
                self.speedx = -self.speedx
                self.count += 1
                if self.right:
                    self.image = pygame.transform.flip(self.image, True, False)
                    self.right = False
                elif not self.right:
                    self.image = pygame.transform.flip(self.image, True, False)
                    self.right = True
                if self.count > 1:
                    self.speedy = -self.speedy
                    self.speedx = -self.speedx
                    if self.right:
                        self.image = pygame.transform.flip(self.image, True, False)
                        self.right = False
                    elif not self.right:
                        self.image = pygame.transform.flip(self.image, True, False)
                        self.right = True
                    self.count = 0
            if self.rect.right >= self.x1:
                if self.right:
                    self.image = pygame.transform.flip(self.image, True, False)
                    self.right = False
                self.speedx -= 2
            if self.rect.left <= self.x0:
                if not self.right:
                    self.image = pygame.transform.flip(self.image, True, False)
                    self.right = True
                self.speedx += 2
            if self.rect.top >= self.y0:
                self.speedy -= 2
            if self.rect.bottom <= self.y1:
                self.speedy += 2
        else:
            self.come = True
            if self.rect.x != rect_x and self.rect.y != rect_y:
                if self.rect.x > rect_x and self.rect.y > rect_y:
                    if self.right:
                        self.image = pygame.transform.flip(self.image, True, False)
                        self.right = False
                    self.rect.x -= 1
                    self.rect.y -= 1
                elif self.rect.x < rect_x and self.rect.y < rect_y:
                    if not self.right:
                        self.image = pygame.transform.flip(self.image, True, False)
                        self.right = True
                    self.rect.x += 1
                    self.rect.y += 1
                elif self.rect.x < rect_x and self.rect.y > rect_y:
                    if not self.right:
                        self.image = pygame.transform.flip(self.image, True, False)
                        self.right = True
                    self.rect.x += 1
                    self.rect.y -= 1
                elif self.rect.x > rect_x and self.rect.y < rect_y:
                    if self.right:
                        self.image = pygame.transform.flip(self.image, True, False)
                        self.right = False
                    self.rect.x -= 1
                    self.rect.y += 1
            elif self.rect.y != rect_y:
                if self.rect.y < rect_y:
                    self.rect.y += 1
                    if current_level == 'level3':
                        self.down, self.up = True, False
                elif self.rect.y > rect_y:
                    self.rect.y -= 1
                    if current_level == 'level3':
                        self.down, self.up = False, True
            elif self.rect.x != rect_x:
                if self.rect.x < rect_x:
                    if not self.right:
                        self.image = pygame.transform.flip(self.image, True, False)
                        self.right = True
                    self.rect.x += 1
                elif self.rect.x > rect_x:
                    if self.right:
                        self.image = pygame.transform.flip(self.image, True, False)
                        self.right = False
                    self.rect.x -= 1
                if current_level == 'level3':
                    self.down, self.up = False, False

    def attack(self, dir, z_rect, p_x, p_y, p, current_level, screen):
        p.hp -= LEVEL_DAMAGE[current_level]
        Blood(blood, dir, z_rect, p_x, p_y, load_image('blood.png', -1))
        blood.draw(screen)
