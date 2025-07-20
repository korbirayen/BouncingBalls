import math
import random

import pygame
from pygame import Vector2

from util import utils


class BlackHole:
    def __init__(self,pos,radius = 20):
        self.color = (255,255,255)
        self.radius = radius
        self.pos = pos

        angleRad = 0
        self.vel = Vector2(math.cos(angleRad),math.sin(angleRad)) * random.uniform(.1,-.1)
        print(self.vel)

    def update(self):
        self.vel += Vector2(0,0.0981)
        self.pos += self.vel

    def draw(self):
        pygame.draw.circle(utils.screen, self.color, self.pos,self.radius,2)
