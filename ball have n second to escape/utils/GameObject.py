import pygame.rect
from pygame.math import Vector2
from utils.util import utils

from enum import Enum


class GameObject:

    def __init__(self, pos, img):
        self.pos = pos
        self.img = img
        self.vel = Vector2(0, 0)

        self.destroyFlag = False
        self.flipX = False

    def update(self):
        self.pos += self.vel

    def draw(self):

        if self.flipX:
            self.img = pygame.transform.flip(self.img, True, False)

        utils.screen.blit(self.img, (self.pos.x , self.pos.y ))

    def getRect(self):
        rect = pygame.rect.Rect(self.pos.x, self.pos.y, self.img.get_width(), self.img.get_height())
        return rect

    def setPos(self, pos):
        self.pos = pos

    def getPos(self):
        return self.pos

    def getCenter(self):
        return Vector2(self.pos.x + self.getRect().w / 2, self.pos.y + self.getRect().h / 2)
