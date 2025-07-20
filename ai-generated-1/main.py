import pygame
from util import utils
from game import Game

utils.currentScreen = Game()

import os, time
# Determine and prepare screenshot directory in this ai-generated-1 project
script_dir = os.path.dirname(os.path.abspath(__file__))
screenshot_dir = os.path.join(script_dir, 'screenshots')
os.makedirs(screenshot_dir, exist_ok=True)
screenshot_timer = 0.0
# Automatically stop after a certain number of screenshots for inspection
max_screenshots = 5
screenshot_count = 0
while True:
    utils.screen.fill((0, 0, 0))
    utils.initDeltaTime()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit(0)

    utils.currentScreen.update()
    utils.currentScreen.draw()
    utils.showFps()
    pygame.display.flip()
