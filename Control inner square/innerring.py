import math
import pygame
from pygame import Vector2

from Box import Box
from util import utils
import colorsys


class InnerSquare:
    def __init__(self, pos, size):
        self.boxes = []
        self.pos = pos
        self.size = size
        self.half_size = size / 2
        self.complete = False

        self.time_since_last_color_change = 0  # Timer for color change
        self.color_change_interval = 0.1  # Interval in milliseconds
        self.hue = 0
        self.color = (255, 255, 255)
        self.destroyFlag = False
        self.surface = pygame.Surface((utils.width, utils.height), pygame.SRCALPHA)

    def update(self):
        pass

    def getSize(self):
        return self.size

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
        top_left = (self.pos.x - self.half_size, self.pos.y - self.half_size)
        pygame.draw.rect(utils.screen, self.color, (*top_left, self.size, self.size), 2)

    def getBoxByIndex(self, sBox):
        for i in range(len(self.boxes)):
            if self.boxes[i] == sBox:
                return i
        return -1

    def destroy(self):
        for box in self.boxes:
            utils.world.DestroyBody(box.box_body)
        self.boxes = []

    def is_point_inside(self, point):
        # Check if the point is inside the square
        left = self.pos.x - self.half_size
        right = self.pos.x + self.half_size
        top = self.pos.y - self.half_size
        bottom = self.pos.y + self.half_size

        return left <= point.x <= right and top <= point.y <= bottom
