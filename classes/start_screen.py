from classes.help_f import *

f = open("save.txt", mode="r")
current_level = f.read()
f.close()


class New_game(pygame.sprite.Sprite):
    image1 = load_image('new.png')
    image_ch = load_image('new_ch.png')

    def __init__(self, new):
        super().__init__(new)
        self.image = self.image1
        self.rect = self.image.get_rect()
        self.image = self.image.convert_alpha()
        self.rect.center = (960, 650)

    def update(self, cur_image):
        self.image = cur_image


class Save_im(pygame.sprite.Sprite):
    image1 = load_image('save.png')
    image_ch = load_image('save_ch.png')

    def __init__(self, save):
        super().__init__(save)
        self.image = self.image1
        self.rect = self.image.get_rect()
        self.rect.center = (960, 300)

    def update(self, cur_image):
        self.image = cur_image

    def __init__(self, save):
        super().__init__(save)
        self.image = self.image1
        self.rect = self.image.get_rect()
        self.rect.center = (960, 300)

    def update(self, cur_image):
        self.image = cur_image


def start_screen(screen, clock):
    global current_level
    pygame.mixer.music.load('music/menutheme.mp3')
    pygame.mixer.music.play()
    fon = pygame.transform.scale(load_image('logo.png'), (W_WIDTH, W_HEIGHT))
    screen.blit(fon, (0, 0))
    save = pygame.sprite.Group()
    new = pygame.sprite.Group()
    save1 = Save_im(save)
    new1 = New_game(new)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if save1.rect.collidepoint(pygame.mouse.get_pos()):
                    f = open("save.txt", mode="r")
                    current_level = f.read()
                    f.close()
                    return None
                elif new1.rect.collidepoint(pygame.mouse.get_pos()):
                    current_level = 'level1'
                    f = open("save.txt", mode="w")
                    print(f, current_level)
                    f.close()
                    return None
            if save1.rect.collidepoint(pygame.mouse.get_pos()):
                save.update(load_image('save_ch.png'))
            elif new1.rect.collidepoint(pygame.mouse.get_pos()):
                new.update(load_image('new_ch.png'))
            else:
                new.update(load_image('new.png'))
                save.update(load_image('save.png'))

            save.draw(screen)
            new.draw(screen)
            pygame.display.flip()
            clock.tick(FPS)
