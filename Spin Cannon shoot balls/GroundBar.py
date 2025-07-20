import pygame.draw

from util import utils


class GroundBar:
    def __init__(self,rect,color):
        self.rect = rect
        self.color = color

    def draw(self):
        pygame.draw.rect(utils.screen,self.color,self.rect)

    def getRect(self):
        return self.rect