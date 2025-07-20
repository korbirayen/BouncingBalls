import math

import pygame
from pygame import Vector2, Surface

from Box import Box
from util import utils
import colorsys


class OuterRing:
    def __init__(self, pos,surface):
        self.boxes = []
        self.pos = pos
        self.complete = False

        self.time_since_last_color_change = 0  # Timer for color change
        self.color_change_interval = 0.1  # Interval in milliseconds (1 second)
        self.hue = 0
        self.destroyFlag = False
        self.surface = surface
        self.radius = 500


    def update(self):
        pass

    def getRadius(self):
        return self.surface.get_width()

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
        utils.screen.blit(self.surface,(self.pos.x,self.pos.y))
        # pygame.draw.circle(utils.screen, self.color, Vector2(utils.width/2,utils.height/2), self.radius,2)

    def getBoxByIndex(self,sBox):
        for i in range(0,len(self.boxes)):
            if self.boxes[i] == sBox:
                return i
        return -1

    def destroy(self):
        for box in self.boxes:
            utils.world.DestroyBody(box.box_body)
        self.boxes = []