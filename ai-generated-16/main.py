import pygame
from util import utils
from game import Game

utils.currentScreen = Game()

while True:
    utils.screen.fill((0, 0, 0), (0, 0, utils.width, utils.height))
    utils.initDeltaTime()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit(0)

    utils.currentScreen.update()
    utils.currentScreen.draw()
    utils.showFps()
    pygame.display.flip()
