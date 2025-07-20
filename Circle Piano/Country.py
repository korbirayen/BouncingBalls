import random

import pygame
from pygame import Vector2

from util import utils


class Country:
    def __init__(self,pos,img):
        self.pos = Vector2(pos[0],pos[1])
        self.img = pygame.image.load(img)
        self.img = pygame.transform.scale(self.img,(48,48))
        self.pos.x -= self.img.get_width()/2
        self.pos.y -= self.img.get_height()/2


    def draw(self):
        utils.screen.blit(self.img,self.pos)

    def getRect(self):
        return pygame.Rect(self.pos.x , self.pos.y, self.img.get_width(), self.img.get_height() )