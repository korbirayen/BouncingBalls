import math

import pygame
from pygame import Vector2

from Box import Box
from Trapezium import Trapezium
from util import utils


class Net:
    def __init__(self, pos):
        self.pos = pos
        self.original_img = pygame.image.load("assets/basket.png")
        self.img = pygame.transform.scale(self.original_img, (90, 80))
        self.angle = 900

        self.boxes = []
        x = pos.x - 5
        y = pos.y + 5
        for i in range(50):
            box = Box(Vector2(x, y), (0, 0, 0))
            self.boxes.append(box)
            x += 0.7
            y += 1.5
        x = pos.x + self.img.get_width()
        y = pos.y + 5
        for i in range(50):
            box = Box(Vector2(x, y), (0, 0, 0))
            self.boxes.append(box)
            x -= 0.7
            y += 1.5

        self.box_positions = [box.getPos() - Vector2(self.pos.x + self.img.get_width()/2,self.pos.y + self.img.get_height()/2) for box in self.boxes]

    def getRect(self):
        return pygame.Rect(self.pos.x + 30, self.pos.y + 20, self.img.get_width() - 60, self.img.get_height() - 60)

    def draw(self):
        self.rotate(1)
        center = self.pos + Vector2(self.img.get_width() / 2, self.img.get_height() / 2)
        for i, box_pos in enumerate(self.box_positions):
            rotated_pos = self.rotate_point(box_pos, self.angle) + center
            self.boxes[i].setPos(rotated_pos)
            self.boxes[i].draw()

        rotated_img = pygame.transform.rotate(self.img, self.angle)
        rect = rotated_img.get_rect(center=self.img.get_rect(topleft=self.pos).center)
        utils.screen.blit(rotated_img, rect.topleft)

    def rotate(self, angle):
        self.angle += angle

    def rotate_point(self, point, angle):
        rad_angle = -angle * (3.14159 / 180)  # convert to radians and negate for counter-clockwise rotation
        rotated_x = point.x * math.cos(rad_angle) - point.y * math.sin(rad_angle)
        rotated_y = point.x * math.sin(rad_angle) + point.y * math.cos(rad_angle)
        return Vector2(rotated_x, rotated_y)
