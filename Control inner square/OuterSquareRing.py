import math
import random

import pygame
from Box2D import b2EdgeShape, Box2D, b2Filter
from pygame import Vector2

from particle import Explosion
from util import utils


class OuterSquareRing:
    def __init__(self, radius, dir=1, sar=0, hue=0):
        self.color = (255, 255, 255)
        self.radius = radius
        self.sar = sar
        self.hue = hue
        self.center = Vector2(utils.width / 2, utils.height / 2)

        self.rotateDir = dir
        self.size = 4
        self.vertices = []
        for i in range(self.size):
            angle = i * (2 * math.pi / self.size)
            x = radius * math.cos(angle)
            y = radius * math.sin(angle)
            self.vertices.append((x, y))

        pos = Vector2(utils.width / 2, utils.height / 2)
        self.body = utils.world.CreateStaticBody(position=utils.from_Pos(pos))
        self.body.userData = self

        self.create_edge_shape()
        self.destroyFlag = False

        self.color = (255,255,255)
        self.surface = pygame.Surface((utils.width,utils.height),pygame.SRCALPHA)
        self.body.angle = math.radians(45)

        self.points = []
        for i in range(self.size):
            angle = i * (2 * math.pi / self.size)
            x = self.center.x + radius * 10 * math.cos(angle)
            y = self.center.y + radius * 10 * math.sin(angle)
            self.points.append(Vector2(x, y))

    def create_edge_shape(self):
        if self.size == 90:
            for i in range(self.size):
                angle = i * (360 / self.size)
                if (0 <= angle <= 320):
                    v1 = self.vertices[i]
                    v2 = self.vertices[(i + 1) % self.size]
                    edge = b2EdgeShape(vertices=[v1, v2])
                    self.body.CreateEdgeFixture(shape=edge, density=1, friction=0.0, restitution=1.0)
        if self.size <= 16:
            for i in range(self.size):
                # if i == 0:
                #     holeSize = self.radius/5
                #     v1 = Vector2(self.vertices[i])
                #     v2 = Vector2(self.vertices[(i + 1) % self.size])
                #     length = (v2 - v1).length()
                #     dir = (v2 - v1).normalize()
                #     mV1 = v1 + dir * (length / 2 - holeSize)
                #     mV2 = v1 + dir * (length / 2 + holeSize)
                #
                #     edge = b2EdgeShape(vertices=[v1, mV1])
                #     self.body.CreateEdgeFixture(shape=edge, density=1, friction=0.0, restitution=1.0)
                #
                #     edge = b2EdgeShape(vertices=[mV2, v2])
                #     self.body.CreateEdgeFixture(shape=edge, density=1, friction=0.0, restitution=1.0)
                # else:
                v1 = self.vertices[i]
                v2 = self.vertices[(i + 1) % self.size]
                edge = b2EdgeShape(vertices=[v1, v2])
                self.body.CreateEdgeFixture(shape=edge, density=1, friction=0.0, restitution=1.0)

    def update(self):
        self.body.angle = -360 + (math.sin(utils.time * self.rotateDir / 1) + 0.5) * 1
        self.points = []
        for fixture in self.body.fixtures:
            v1 = utils.to_Pos(self.body.transform * fixture.shape.vertices[0])
            v2 = utils.to_Pos(self.body.transform * fixture.shape.vertices[1])
            self.points.append(Vector2(v1[0], v1[1]))
            self.points.append(Vector2(v2[0], v2[1]))

    def draw(self):
        self.draw_edges()

    def draw_edges(self):
        for fixture in self.body.fixtures:
            v1 = utils.to_Pos(self.body.transform * fixture.shape.vertices[0])
            v2 = utils.to_Pos(self.body.transform * fixture.shape.vertices[1])
            pygame.draw.line(utils.screen, self.color, v1, v2, 2)
        # for p in self.points:
        #     pygame.draw.circle(utils.screen,(233,233,23),p,2)

    def is_point_in_polygon(self, point, vertices):
        # Ray-casting algorithm to check if the point is inside the polygon
        num_vertices = len(vertices)
        j = num_vertices - 1  # The last vertex is the previous one to the first
        inside = False
        for i in range(num_vertices):
            xi, yi = vertices[i]
            xj, yj = vertices[j]
            if ((yi > point.y) != (yj > point.y)) and \
                    (point.x < (xj - xi) * (point.y - yi) / (yj - yi) + xi):
                inside = not inside
            j = i
        return inside