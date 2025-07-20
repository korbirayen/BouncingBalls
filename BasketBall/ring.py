import colorsys
import math

import pygame
from pygame import Vector2

from Box import Box
from util import utils

class Ring:
    def __init__(self, radius, dir):
        self.boxes = []
        self.dir = dir
        self.initial_positions = []
        self.initial_line_positions = []  # To store the relative positions of the lines
        self.color = (255, 255, 255)
        self.center = Vector2(utils.width / 2, utils.height / 2)
        self.angle = 0
        self.hue = 0  # Starting hue value for color gradient
        self.radius = radius
        self.time_since_last_color_change = 0
        self.color_change_interval = 0.1
        self.lines = []  # To store line positions

        for i in range(0, 328):
            rad = math.radians(i)
            pos = self.center + Vector2(math.cos(rad) * radius, math.sin(rad) * radius)
            self.boxes.append(Box(Vector2(pos.x, pos.y), (255, 255, 255)))
            self.initial_positions.append(Vector2(pos.x, pos.y) - self.center)


    def update(self):
        self.angle += .8 * self.dir  # Rotate by 0.5 degrees per update
        rad_angle = math.radians(self.angle)
        cos_angle = math.cos(rad_angle)
        sin_angle = math.sin(rad_angle)

        for i, initial_pos in enumerate(self.initial_positions):
            rotated_pos = Vector2(
                initial_pos.x * cos_angle - initial_pos.y * sin_angle,
                initial_pos.x * sin_angle + initial_pos.y * cos_angle
            )
            self.boxes[i].setPos(self.center + rotated_pos)

        rotated_lines = []
        for initial_start_pos, initial_end_pos in self.initial_line_positions:
            rotated_start_pos = Vector2(
                initial_start_pos.x * cos_angle - initial_start_pos.y * sin_angle,
                initial_start_pos.x * sin_angle + initial_start_pos.y * cos_angle
            )
            rotated_end_pos = Vector2(
                initial_end_pos.x * cos_angle - initial_end_pos.y * sin_angle,
                initial_end_pos.x * sin_angle + initial_end_pos.y * cos_angle
            )
            rotated_lines.append((self.center + rotated_start_pos, self.center + rotated_end_pos))
        self.lines = rotated_lines

        # Update color gradient
        self.update_color_gradient()

    def update_color_gradient(self):
        # Increment hue and wrap around if it exceeds 1.0
        self.hue = (self.hue + 0.001) % 1.0
        # Convert HSV to RGB
        r, g, b = colorsys.hsv_to_rgb(self.hue, 1, 1)
        # Scale RGB values to 0-255 range
        self.color = (int(r * 255), int(g * 255), int(b * 255))
        for box in self.boxes:
            box.color = self.color

    def draw(self):
        for box in self.boxes:
            box.draw()
