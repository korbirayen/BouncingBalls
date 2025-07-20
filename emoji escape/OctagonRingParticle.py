import math
import random

import pygame
from pygame import Vector2
from Box import Box
from particle import Particle
from util import utils
import colorsys

class OctagonRingParticle:
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
        self.destroyFlag = False
        # self.update_color_gradient()

        self.create_octagon()
        center = Vector2(utils.width/2,utils.height/2)
        for box in self.boxes:
            # box.convert_to_dynamic()
            # box.box_body.gravityScale = 0

            pos = Vector2(box.x,box.y)
            vel = pos - center
            vel = vel.normalize()
            speed = 2
            vel = Vector2(vel.x * speed,vel.y * speed)
            box.vel_x = vel.x
            box.vel_y = vel.y
            # box.box_body.linearVelocity = (vel.x,vel.y)

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
            self.boxes.append(Particle(pos.x,pos.y, self.color))

    def update(self):
        # Update color every second
        pass

    def draw(self):
        for box in self.boxes:
            box.update()
            box.draw()

