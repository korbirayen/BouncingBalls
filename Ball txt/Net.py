import math

import pygame
from pygame import Vector2

from util import utils


class Net:
    def __init__(self,pos):
        self.pos = pos
        self.img = pygame.image.load("assets/goal.png")
        self.img = pygame.transform.scale(self.img,(120,120))
        self.angle = 330 + (360 - 330)/2

    def getRect(self):
        return pygame.Rect(self.pos.x +40,self.pos.y + 20 ,self.img.get_width() - 40,self.img.get_height() - 60 )

    def update(self):
        self.angle += 1
        rad = math.radians(self.angle)
        self.pos = Vector2(utils.width/2,utils.height/2) + Vector2(math.cos(rad),math.sin(rad)) * 250
        self.pos -= Vector2(self.img.get_width()/2,self.img.get_height()/2)

    def draw(self):
        utils.screen.blit(self.img,self.pos)