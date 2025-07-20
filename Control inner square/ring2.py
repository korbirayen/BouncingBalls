import math

import pygame
from Box2D import b2CircleShape
from pygame import Vector2

from Box import Box
from util import utils
import colorsys

from Box2D.b2 import (world, polygonShape, circleShape, staticBody, dynamicBody)

class Ring2:
    def __init__(self, radius, color = (23, 155, 155)):
        self.radius = radius
        self.color = color
        pos = Vector2(utils.width/2,utils.height/2)
        self.body = b2CircleShape(pos=utils.from_Pos((pos.x, pos.y)), radius=self.radius)

    def update(self):
        pass

    def update_color_gradient(self):
        # Increment hue and wrap around if it exceeds 1.0
        self.hue = (self.hue + 0.01) % 1.0
        # Convert HSV to RGB
        r, g, b = colorsys.hsv_to_rgb(self.hue, 1, 1)
        # Scale RGB values to 0-255 range
        self.color = (int(r * 255), int(g * 255), int(b * 255))
        for box in self.boxes:
            box.color = self.color

    def draw(self):
        pygame.draw.circle(utils.screen,self.color,(utils.width/2, utils.height/2), self.radius, 1)



