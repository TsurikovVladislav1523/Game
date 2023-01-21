from all_for_project.help_f import *


class Smoke(pygame.sprite.Sprite):
    def __init__(self, sheet_w, columns, rows, pos, smokes):
        super().__init__(smokes)
        self.frames = []
        self.sheet_d = sheet_w
        self.cut_sheet(sheet_w, columns, rows)
        self.view = 0
        self.tp1 = 0
        self.right = True
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.image = self.image.convert_alpha()
        self.rect = pygame.Rect(0, 0, 30, 38)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.center = (pos[0] - 5, pos[1])

    def cut_sheet(self, sheet, columns, rows):
        self.frames.clear()
        rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                           sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (rect.w * i, rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, rect.size)))

    def update(self, pos):
        self.view += 1
        if self.cur_frame + 1 == len(self.frames):
            self.kill()
            return None
        if self.view % 3 == 0:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]
            self.image = self.image.convert_alpha()
        self.rect.center = (pos[0] - 5, pos[1])
