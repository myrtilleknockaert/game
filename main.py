import pygame
import math
from game import Game

pygame.init()

clock = pygame.time.Clock()
fps = 70

# Create the screen
pygame.display.set_caption("Jeu du Pic'asso")
screen = pygame.display.set_mode((1080, 720))

background = pygame.image.load("assets/bg.png")
foreground = pygame.image.load("assets/fg.png")

banner = pygame.image.load("assets/button.png")
banner = pygame.transform.scale(banner, (492, 448))
banner_rect = banner.get_rect()
banner_rect.x = math.ceil(screen.get_width() / 4)
banner_rect.y = math.ceil(screen.get_height() / 6)


game = Game()


running = True
while running:
    screen.blit(background, (0, 0))  # add the background
    screen.blit(foreground, (0, 330))  # add the foreground

    if game.is_playing:
        game.update(screen)
    else:
        screen.blit(banner, banner_rect)

    pygame.display.flip()  # update the screen
    # if the user click on the cross
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            game.pressed[
                event.key
            ] = True  # detect if the user press the space bar to launch projectile

            if event.key == pygame.K_SPACE:
                if game.is_playing:
                    game.player.launch_projectile()
                # else:
                #     game.start()
                #     game.sound_manager.play("click")

        elif event.type == pygame.KEYUP:
            game.pressed[event.key] = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if banner_rect.collidepoint(event.pos):
                game.start()
                game.sound_manager.play("click")

    clock.tick(fps)
