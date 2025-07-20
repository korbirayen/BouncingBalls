import math
import random

import pygame
from pygame import Vector2

from AssetManager import assetsManager
from util import utils


class BlackHole:
    def __init__(self,pos,radius = 55):
        self.color = (255,255,255)
        self.radius = radius
        self.pos = pos

        angleRad = 0
        self.vel = Vector2(math.cos(angleRad),math.sin(angleRad)) * random.uniform(.5,.5)
        self.img = assetsManager.get("football")
        self.img = pygame.transform.scale(self.img,(radius*2.2,radius*2.2))

    def update(self):
        self.vel += Vector2(0,0.12)
        self.pos += self.vel
        self.img = pygame.transform.scale(self.img, (self.radius * 2.2, self.radius * 2.2))

    def draw(self):
        # pygame.draw.circle(utils.screen, self.color, self.pos,self.radius,2)
        utils.screen.blit(self.img,(self.pos.x-self.radius,self.pos.y-self.radius))
