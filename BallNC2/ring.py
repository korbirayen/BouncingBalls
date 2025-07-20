import colorsys
import math

import pygame
from pygame import Vector2

from Box import Box
from util import utils


class Ring:
    def __init__(self, radius):
        self.boxes = []
        self.initial_positions = []
        self.color = (255, 255, 155)
        self.center = Vector2(utils.width / 2, utils.height / 2)
        self.angle = 0
        self.hue = 0
        self.update_color_gradient()
        self.time_since_last_color_change = 0
        self.color_change_interval = 0.1

        for i in range(0, 335):
            rad = math.radians(i)
            pos = self.center + Vector2(math.cos(rad) * radius, math.sin(rad) * radius)
            self.boxes.append(Box(Vector2(pos.x, pos.y), self.color))
            self.initial_positions.append(Vector2(pos.x, pos.y) - self.center)

    def update(self):
        self.angle += -.77  # Rotate by 1 degree per update; adjust as needed
        rad_angle = math.radians(self.angle)
        cos_angle = math.cos(rad_angle)
        sin_angle = math.sin(rad_angle)

        for i, initial_pos in enumerate(self.initial_positions):
            rotated_pos = Vector2(
                initial_pos.x * cos_angle - initial_pos.y * sin_angle,
                initial_pos.x * sin_angle + initial_pos.y * cos_angle
            )
            self.boxes[i].setPos( self.center + rotated_pos)

        #
        # Update color every second
        self.time_since_last_color_change += utils.deltaTime()
        if self.time_since_last_color_change >= self.color_change_interval:
            self.update_color_gradient()
            self.time_since_last_color_change = 0

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
            box.draw()




class Ring2:
    def __init__(self, radius):
        self.boxes2 = []
        self.initial_positions2 = []
        self.color = (23, 155, 155)
        self.center2 = Vector2(utils.width / 2, utils.height / 2)
        self.angle2 = 5
        self.hue2 = 0
        self.update_color_gradient2()
        self.time_since_last_color_change2 = 0
        self.color_change_interval2 = 0.05

        for i in range(0, 365):
            rad = math.radians(i)
            pos = self.center2 + Vector2(math.cos(rad) * radius, math.sin(rad) * radius)
            self.boxes.append(Box(Vector2(pos.x, pos.y), self.color))
            self.initial_positions.append(Vector2(pos.x, pos.y) - self.center2)

    def update2(self):
        self.angle2 += 2.7 # Rotate by 1 degree per update; adjust as needed
        rad_angle = math.radians(self.angle2)
        cos_angle = math.cos(rad_angle)
        sin_angle = math.sin(rad_angle)

        for i, initial_pos in enumerate(self.initial_positions2):
            rotated_pos = Vector2(
                initial_pos.x * cos_angle - initial_pos.y * sin_angle,
                initial_pos.x * sin_angle + initial_pos.y * cos_angle
            )
            self.boxes2[i].setPos( self.center2 + rotated_pos)

        #
        # Update color every second
        self.time_since_last_color_change2 += utils.deltaTime()
        if self.time_since_last_color_change2 >= self.color_change_interval2:
            self.update_color_gradient2()
            self.time_since_last_color_change2 = 0

    def update_color_gradient2(self):
        # Increment hue and wrap around if it exceeds 1.0
        self.hue2 = (self.hue2 + 0.01) % 1.0
        # Convert HSV to RGB
        r, g, b = colorsys.hsv_to_rgb(self.hue2, 1, 1)
        # Scale RGB values to 0-255 range
        self.color2 = (int(r * 255), int(g * 255), int(b * 255))
        for box in self.boxes2:
            box.color = self.color2

    def draw2(self):
        for box in self.boxes2:
            box.draw2()