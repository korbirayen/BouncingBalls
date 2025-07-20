import math
import random

import pygame
from pygame import Vector2

from util import utils


class Gem:
    def __init__(self):
        self.radius = random.uniform(1, 170)
        angle = random.uniform(0, 360)
        self.pos = Vector2(
            utils.width / 2 + self.radius * math.cos(math.radians(angle)),
            utils.height / 2 + self.radius * math.sin(math.radians(angle))
        )
        self.img = pygame.image.load("assets/gem.png")
        self.img = pygame.transform.scale(self.img,(35,35))

    def getRect(self):
        return pygame.Rect(self.pos.x ,self.pos.y,self.img.get_width() ,self.img.get_height())

    def update(self):
        pass
    def draw(self):
        utils.screen.blit(self.img,self.pos)