import math
import pygame
from pygame import Vector2
from Box import Box
from util import utils
import colorsys

class OctagonRing:
    def __init__(self, side_length, color=(23, 155, 155)):
        self.boxes = []
        self.initial_positions = []
        self.color = color
        self.center = Vector2(utils.width / 2, utils.height / 2)
        self.angle = 0
        self.num_boxes_per_side = side_length
        self.side_length = side_length
        self.complete = False

        self.time_since_last_color_change = 0  # Timer for color change
        self.color_change_interval = 0.1  # Interval in milliseconds (1 second)
        self.hue = 0
        self.update_color_gradient()

        self.create_octagon()

    def create_octagon(self):
        angle_step = math.pi / 4
        radius = self.side_length/2

        points = []

        for i in range(8):
            angle = angle_step * i
            x = self.center.x + radius * math.cos(angle)
            y = self.center.y + radius * math.sin(angle)
            points.append((x, y))

        for i in range(len(points)):
            start = points[i]
            end = points[(i + 1) % len(points)]
            self.draw_line_with_boxes(start, end)

    def draw_line_with_boxes(self, start, end):
        start = Vector2(start)
        end = Vector2(end)
        delta = end - start
        length = delta.length()
        direction = delta.normalize()

        for i in range(int(length)):
            pos = start + direction * i
            self.boxes.append(Box(pos, self.color))
            self.initial_positions.append(pos)

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
