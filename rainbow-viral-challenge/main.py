import pygame

from util import utils
from viral_game import ViralGame

utils.currentScreen = ViralGame()

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
