import math
import pygame
from pygame import Vector2
from CirclePiece import CirclePiece
from util import utils


class Ring:
    def __init__(self, radius=utils.width / 2 - 50, margin=5):
        self.size = 30  # Number of segments
        self.outside_radius = radius
        self.inside_radius = radius - 100
        self.center = Vector2(utils.width / 2, utils.height / 2)
        self.pieces = []

        inside_vertices = []
        outside_vertices = []

        for i in range(self.size):
            angle_deg = 360 / self.size * i
            angle_rad = math.radians(angle_deg)

            # Inside vertices
            x_inside = self.center.x + self.inside_radius * math.cos(angle_rad)
            y_inside = self.center.y + self.inside_radius * math.sin(angle_rad)
            inside_vertices.append(Vector2(x_inside, y_inside))

            # Outside vertices
            x_outside = self.center.x + self.outside_radius * math.cos(angle_rad)
            y_outside = self.center.y + self.outside_radius * math.sin(angle_rad)
            outside_vertices.append(Vector2(x_outside, y_outside))

        # Create CirclePiece for each segment with margin
        id = 0
        hue = 0
        hueStep = 1 / self.size

        for i in range(self.size):
            next_i = (i + 1) % self.size

            # Shrink the edges slightly to create a margin
            inside_v1 = inside_vertices[i] + (self.center - inside_vertices[i]).normalize()
            outside_v1 = outside_vertices[i] + (self.center - outside_vertices[i]).normalize()
            inside_v2 = inside_vertices[next_i] + (self.center - inside_vertices[next_i]).normalize()
            outside_v2 = outside_vertices[next_i] + (self.center - outside_vertices[next_i]).normalize()

            piece = CirclePiece(id,[
                inside_v1,
                outside_v1,
                outside_v2,
                inside_v2
            ], utils.hueToRGB(hue))
            self.pieces.append(piece)
            id += 1
            hue += hueStep

    def update(self):
        for piece in self.pieces:
            piece.update()

    def draw(self):
        for piece in self.pieces:
            piece.draw()
