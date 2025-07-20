import math
import pygame
from pygame import Vector2
from Box import Box
from util import utils
import colorsys


class SquareRing:
    def __init__(self, side_length, color=(23, 155, 155)):
        self.boxes = []
        self.initial_positions = []
        self.color = color
        self.center = Vector2(utils.width / 2, utils.height / 2)
        self.angle = 0
        self.num_boxes_per_side = side_length
        self.dir = dir
        self.side_length = side_length
        self.complete = False

        self.time_since_last_color_change = 0  # Timer for color change
        self.color_change_interval = 0.1  # Interval in milliseconds (1 second)
        self.hue = 0
        self.update_color_gradient()

        self.create_square()

    def create_square(self):
        half_side = self.side_length / 2
        spacing = self.side_length / (self.num_boxes_per_side - 1)

        for i in range(self.num_boxes_per_side):
            for j in range(self.num_boxes_per_side):
                if i == 0 or j == 0 or i == self.num_boxes_per_side - 1 or j == self.num_boxes_per_side-1:
                    x = -half_side + i * spacing
                    y = -half_side + j * spacing
                    pos = self.center + Vector2(x, y)
                    self.boxes.append(Box(Vector2(pos.x, pos.y), self.color))
                    self.initial_positions.append(Vector2(x, y))

    def update(self):
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
            if box.destroyFlag:
                continue
            box.draw()

    def getBoxByIndex(self, sBox):
        for i in range(len(self.boxes)):
            if self.boxes[i] == sBox:
                return i
        return -1
