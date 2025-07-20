import math
import random

import pygame
from pygame import Vector2

from util import utils


class Ball:
    def __init__(self,pos,radius = 13):
        self.color = utils.hueToRGB(hue=random.uniform(0,1))
        self.radius = radius
        self.pos = pos
        self.destroyFlag = False

        angleRad = random.uniform(-2*math.pi,2 * math.pi)
        self.vel = Vector2(0,random.uniform(2,5))
        self.canSpawnTime = 0
        self.img = pygame.image.load("assets/mushroom.png")
        self.img = pygame.transform.scale(self.img, (radius * 2, radius * 2))
        self.angle = 0

    def update(self):
        self.angle += 1
        self.vel += Vector2(0,0.0981)
        self.pos += self.vel
        self.canSpawnTime += utils.deltaTime()


    def draw(self):
        # pygame.draw.circle(utils.screen, self.color, self.pos,self.radius)
        rotate_img = pygame.transform.rotate(self.img,self.angle)
        utils.screen.blit(rotate_img, (self.pos.x-self.radius,self.pos.y - self.radius))
