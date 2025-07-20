import pygame

from util import utils


class Net:
    def __init__(self,pos):
        self.pos = pos
        self.img = pygame.image.load("assets/home.png")
        self.img = pygame.transform.scale(self.img,(70,70))

    def getRect(self):
        return pygame.Rect(self.pos.x +20,self.pos.y + 20 ,self.img.get_width() - 40,self.img.get_height() - 60 )

    def draw(self):
        utils.screen.blit(self.img,self.pos)