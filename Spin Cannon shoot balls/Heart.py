import pygame
from pygame import Vector2

from util import utils


class Heart:
    def __init__(self,pos,color):
        self.pos = pos
        self.color = color
        self.dir = 1
        self.speed = 1
        self.img = pygame.image.load("assets/red_heart.png")
        if self.color == 'green':
            self.img = pygame.image.load("assets/green_heart.png")

        self.maxY = 870
        self.minY = 720
        self.destroyFlag = False

    def update(self):
        self.pos += Vector2(0,self.dir * self.speed)
        if self.pos.y >= self.maxY or self.pos.y <= self.minY:
            self.dir *= -1  # Reverse direction when reaching the limits

    def draw(self):
        if self.destroyFlag:
            return
        utils.screen.blit(self.img,(self.pos.x,self.pos.y))

    def getRect(self):
        return pygame.Rect(self.pos.x, self.pos.y, self.img.get_width(), self.img.get_height())