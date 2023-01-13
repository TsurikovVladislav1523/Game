class AnimatedSpriteZombi(pygame.sprite.Sprite):
    def __init__(self, sheet_w, columns, rows, x, y, group, x0, y0, x1, y1):
        super().__init__(group)
        # x0, x1, y0, y1 координаты комнаты, в которой находится зомби
        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.hp = 4
        self.y1 = y1
        self.frames = []
        self.sheet_w = sheet_w
        self.cut_sheet(sheet_w, columns, rows)
        self.view = 0
        self.right = True
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.image = self.image.convert_alpha()
        self.rect = pygame.Rect(0, 0, 30, 38)
        self.rect = self.rect.move(x, y)

    def cut_sheet(self, sheet, columns, rows):
        self.frames.clear()
        rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                           sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (rect.w * i, rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, rect.size)))

    def update(self):
        if self.hp == 0:
            self.kill()
        # урон от соприкосновения
        if pygame.sprite.collide_mask(self, p):
            p.hp -= 1
        rect_x, rect_y = p.coords()
        self.view += 1
        if self.view % 10 == 0:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]
            self.image = self.image.convert_alpha()
        if not (self.x0 <= rect_x <= self.x1 and self.y0 <= rect_y <= self.y1):
            if self.right:
                self.rect.x += V / FPS
            if not self.right:
                self.rect.x -= V / FPS
                if pygame.sprite.spritecollideany(self, walls):
                    self.image = pygame.transform.flip(self.image, True, False)
                    self.right = True
                    self.rect.x += V / FPS
            if pygame.sprite.spritecollideany(self, walls) and self.right:
                self.image = pygame.transform.flip(self.image, True, False)
                self.right = False
        else:
            if self.rect.x != rect_x and self.rect.y != rect_y:
                if self.rect.x > rect_x and self.rect.y > rect_y:
                    self.rect.x -= 1
                    self.rect.y -= 1
                elif self.rect.x < rect_x and self.rect.y < rect_y:
                    self.rect.x += 1
                    self.rect.y += 1
                elif self.rect.x < rect_x and self.rect.y > rect_y:
                    self.rect.x += 1
                    self.rect.y -= 1
                elif self.rect.x > rect_x and self.rect.y < rect_y:
                    self.rect.x -= 1
                    self.rect.y += 1
            elif self.rect.y != rect_y:
                if self.rect.y < rect_y:
                    self.rect.y += 1
                elif self.rect.y > rect_y:
                    self.rect.y -= 1
            elif self.rect.x != rect_x:
                if self.rect.x < rect_x:
                    self.rect.x += 1
                elif self.rect.x > rect_x:
                    self.rect.x -= 1