from all_for_project.help_f import *


def end_screen(screen, clock):
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
