import pygame.draw
from pygame import Vector2

from util import utils


class Block:
    def __init__(self,rect,color,live):
        self.rect = rect
        self.color = color
        self.live = live
        self.destroyFlag = False

    def draw(self):
        pygame.draw.rect(utils.screen,self.color,self.rect,2)
        text_width,text_height = utils.font16.render(str(self.live),(255,0,255),True).get_size()
        utils.drawText(
            Vector2(self.rect.x + self.rect.w/2 - text_width/2,self.rect.y + self.rect.h/2 - text_width/2)
            ,str(self.live),(255,255,255),utils.font16)

    def getRect(self):
        return self.rect