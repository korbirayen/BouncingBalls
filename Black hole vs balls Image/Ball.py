import math
import random

import pygame
from pygame import Vector2

from AssetManager import assetsManager
from util import utils


class Ball:
    def __init__(self,pos,radius = 20):
        self.color = utils.hueToRGB(hue=random.uniform(1,1))
        self.radius = radius
        self.pos = pos
        self.destroyFlag = False

        angleRad = random.uniform(2*math.pi,2 * math.pi)
        self.vel = Vector2(math.cos(angleRad),math.sin(angleRad)) * random.uniform(-3.6,-3.6)
        self.canSpawnTime = 0

        self.img = assetsManager.get("baseball")
        self.img = pygame.transform.scale(self.img, (radius*2, radius*2))

    def update(self):
        self.vel += Vector2(0,0.00981)
        self.pos += self.vel
        self.canSpawnTime += utils.deltaTime()


    def draw(self):
        # pygame.draw.circle(utils.screen, self.color, self.pos,self.radius)
        utils.screen.blit(self.img, (self.pos.x - self.radius, self.pos.y - self.radius))