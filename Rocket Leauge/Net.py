import math

import pygame
from pygame import Vector2

from util import utils


class Net:
    def __init__(self,team,pos,angle):
        self.pos = pos
        self.team = team
        if team == 'red':
            self.img = pygame.image.load("assets/blueline.png")
        else:
            self.img = pygame.image.load("assets/redline.png")
        self.img = pygame.transform.scale(self.img,(self.img.get_width() * 0.5,self.img.get_height() * 0.5))
        self.movingAngle = angle
        self.angle = 0
    def getRect(self):
        rotated_image, rect = utils.rotate(self.img, self.angle, Vector2(self.pos.x, self.pos.y), Vector2(0, 0))
        return rect

    def update(self):
        center = Vector2(utils.width/2,utils.height/2 - 30)
        rDir = center - self.pos
        self.angle = math.degrees(math.atan2(rDir.y, rDir.x))

        self.movingAngle += 0.5
        # rad = math.radians(self.movingAngle)
        # self.pos = center + Vector2(math.cos(rad),math.sin(rad)) * 230
        # self.pos -= Vector2(self.img.get_width()/2,self.img.get_height()/2)

        center = Vector2(utils.width / 2, utils.height / 2 - 30)
        x = math.cos(math.radians(self.movingAngle))
        y = math.sin(math.radians(self.movingAngle))
        pDir = Vector2(x, y)
        pos = center + pDir * (240)
        self.pos = pos

    def draw(self):
        rotated_image, rect = utils.rotate(self.img, self.angle, Vector2(self.pos.x, self.pos.y), Vector2(0, 0))
        utils.screen.blit(rotated_image, rect.topleft)