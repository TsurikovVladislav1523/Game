import pygame
import sys
import os
from config import *
size = width, height = W_WIDTH, W_HEIGHT
size = width, height = W_WIDTH, W_HEIGHT
screen = pygame.display.set_mode(size)

def terminate():
    pygame.quit()
    sys.exit()


def load_image(name, color_key=None):
    fullname = os.path.join(ASSETS_DIR, name)
    image = pygame.image.load(fullname)
    if color_key is not None:
        image = image.convert()
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image
