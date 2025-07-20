import pygame.draw
from pygame import Vector2

from util import utils


class Net:
    def __init__(self,rect,xPercent):
        self.rect = rect
        self.xPercent = xPercent

    def getRect(self):
        return self.rect

    def draw(self):
        text = "x" + str(self.xPercent)
        tw, th = utils.font16.render(text, True, (233, 233, 233)).get_size()
        utils.drawText(Vector2(self.rect.x + ( self.rect.w)/2 - tw / 2, self.rect.y - 30), text, (255, 233, 255), utils.font16)
        pygame.draw.rect(utils.screen,(233,23,23),self.rect)