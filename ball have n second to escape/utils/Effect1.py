import random

import pygame
from pygame import Vector2

from GameObject import GameObject
from SpriteSheet import SpriteSheet
from assets_manager import assetsManager
from util import utils


class Effect1(GameObject):
    def __init__(self,pos):
        super().__init__(pos, None)
        self.sheet = SpriteSheet(assetsManager.get("man_walk"),1,6)
        self.sheet.setPlay(0,5,0.07,True)
        self.img = self.sheet.getCurrentFrame()
        self.destroyFlag = False

    def update(self):
        self.sheet.play()
        self.img = self.sheet.getCurrentFrame()
        if self.sheet.current >= self.sheet.fto:
            self.destroyFlag = True

    def draw(self):
        utils.screen.blit(self.img,self.pos)
