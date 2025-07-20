import colorsys
import math

import pygame
from pygame import Vector2

from Box import Box
from util import utils


class Ring:
    def __init__(self, radius,dir):
        self.boxes = []
        self.dir = dir
        self.initial_positions = []
        self.initial_line_positions = []  # To store the relative positions of the lines
        self.color = (247, 126, 86)
        self.center = Vector2(utils.width / 2, utils.height / 2)
        self.angle = 0
        self.hue = 0
        self.radius = radius
        # self.update_color_gradient()
        self.time_since_last_color_change = 0
        self.color_change_interval = 0.1
        self.lines = []  # To store line positions

        for i in range(0, 360):
            rad = math.radians(i)
            pos = self.center + Vector2(math.cos(rad) * radius, math.sin(rad) * radius)
            self.boxes.append(Box(Vector2(pos.x, pos.y), (0,125,0)))
            self.initial_positions.append(Vector2(pos.x, pos.y) - self.center)


    def update(self):
        self.angle += 1 * self.dir # Rotate by 1 degree per update; adjust as needed
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
            box.draw()
        for start_pos, end_pos in self.lines:
            pygame.draw.line(utils.screen, (255,255,255), start_pos, end_pos,3)