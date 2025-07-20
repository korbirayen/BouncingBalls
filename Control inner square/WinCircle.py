import colorsys
import random

import pygame
from pygame import Vector2

from util import utils


class WinSquare:
    def __init__(self):
        self.color = (0, 0, 0)
        self.size = 0
        self.collideWith = 0
        self.value = 0

    def update(self):
        if self.collideWith == 1:
            self.value += utils.deltaTime() * 40
        elif self.collideWith == -1:
            self.value -= utils.deltaTime() * 40

        if self.value > 0:
            self.color = (255, 0, 255)
            self.size = abs(self.value) * 2  # Size is twice the radius for a square
        elif self.value < 0:
            self.color = (255, 140, 0)
            self.size = abs(self.value) * 2

    def draw(self):
        # Calculate the top-left corner based on size and center position
        top_left_x = (utils.width / 2) - (self.size / 2)
        top_left_y = (utils.height / 2) - (self.size / 2)
        pygame.draw.rect(utils.screen, self.color, (top_left_x, top_left_y, self.size, self.size))
