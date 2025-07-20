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
        self.vel = Vector2(math.cos(angleRad),math.sin(angleRad)) * random.uniform(5,5)
        self.oImage = pygame.image.load("assets/mario.png")
        # self.pos.x -= self.img.get_width()/2
        # self.pos.y -= self.img.get_height()/2

        self.original_pos = self.pos.copy()  # Save the original position
        self.shake_magnitude = 2  # The magnitude of the shake
        self.shakeTime = 0.5

    def update(self):
        self.img = pygame.transform.scale(self.oImage,(self.radius * 2,self.radius * 2))

        if self.shakeTime > 0:
            self.shakeTime -= utils.deltaTime()
            self.pos = self.original_pos + Vector2(random.uniform(-self.shake_magnitude, self.shake_magnitude),
                                               random.uniform(-self.shake_magnitude, self.shake_magnitude))

    def draw(self):
        utils.screen.blit(self.img,(self.pos.x - self.radius,self.pos.y - self.radius))