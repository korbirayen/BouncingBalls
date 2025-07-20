import math
import random

import pygame
from pygame import Vector2

from util import utils


class Ball:
    def __init__(self,pos,radius = 10):
        self.color = utils.hueToRGB(hue=random.uniform(0,1))
        self.radius = radius
        self.pos = pos
        self.destroyFlag = False

        angleRad = random.uniform(-2*math.pi,2 * math.pi)
        self.vel = Vector2(math.cos(angleRad),math.sin(angleRad)) * random.uniform(2,2)
        self.canSpawnTime = 0

    def update(self):
        self.vel += Vector2(0,0)
        self.pos += self.vel
        self.canSpawnTime += utils.deltaTime()


    def draw(self):
        pygame.draw.circle(utils.screen, self.color, self.pos,self.radius)
