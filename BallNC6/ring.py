import math

import pygame
from pygame import Vector2

from Box import Box
from util import utils
import colorsys


class Ring:
    def __init__(self, radius,cRange,dir, color = (23, 155, 155)):
        self.boxes = []
        self.initial_positions = []
        self.color = color
        self.center = Vector2(utils.width / 2, utils.height / 2)
        self.angle = 0
        self.cRange = cRange
        self.dir = dir
        self.radius = radius
        self.complete = False

        self.time_since_last_color_change = 0  # Timer for color change
        self.color_change_interval = 0.1  # Interval in milliseconds (1 second)
        self.hue = 0
        # self.update_color_gradient()

        for i in range(0, self.cRange):
            rad = math.radians(i)
            pos = self.center + Vector2(math.cos(rad) * radius, math.sin(rad) * radius)
            self.boxes.append(Box(Vector2(pos.x, pos.y), self.color))
            self.initial_positions.append(Vector2(pos.x, pos.y) - self.center)

    def update(self):
        if self.complete:
            for box in self.boxes:
                if box.getPos().y > 800:
                    utils.world.DestroyBody(box.box_body)
                    self.boxes.remove(box)
            return
        self.angle += 0.5 * self.dir # Rotate by 1 degree per update; adjust as needed
        rad_angle = math.radians(self.angle)
        cos_angle = math.cos(rad_angle)
        sin_angle = math.sin(rad_angle)

        for i, initial_pos in enumerate(self.initial_positions):
            rotated_pos = Vector2(
                initial_pos.x * cos_angle - initial_pos.y * sin_angle,
                initial_pos.x * sin_angle + initial_pos.y * cos_angle
            )
            if self.boxes[i].destroyFlag:
                continue
            self.boxes[i].setPos( self.center + rotated_pos)

        for box in self.boxes:
            if box.destroyFlag and box.box_body is not None:
                utils.world.DestroyBody(box.box_body)
                box.box_body = None
        #
        # # Update color every second
        # self.time_since_last_color_change += utils.deltaTime()
        # if self.time_since_last_color_change >= self.color_change_interval:
        #     self.update_color_gradient()
        #     self.time_since_last_color_change = 0

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
        for box in self.boxes:
            if box.destroyFlag:
                continue
            box.draw()

    def getBoxByIndex(self,sBox):
        for i in range(0,len(self.boxes)):
            if self.boxes[i] == sBox:
                return i
        return -1

