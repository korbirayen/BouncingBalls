import math
import random

import pygame
from Box2D import b2Filter, b2PolygonShape
from pygame import Vector2

from util import utils


class Square:
    def __init__(self, pos, size, color, vel=Vector2(random.uniform(-10, 10),-20)):
        self.color = color
        self.size = size
        self.half_size = size / 2
        self.square_body = utils.world.CreateDynamicBody(position=utils.from_Pos((pos.x, pos.y)))
        vertices = [(-self.half_size, -self.half_size), (self.half_size, -self.half_size),
                    (self.half_size, self.half_size), (-self.half_size, self.half_size)]
        self.square_shape = self.square_body.CreatePolygonFixture(vertices=vertices, density=1, friction=0.0, restitution=1.01)
        self.square_body.linearVelocity = vel
        self.square_body.userData = self
        self.destroyFlag = False
        self.square_body.angularVelocity = 1

        self.trail = []
        self.trail_length = 50

        self.isPlaySound = False

    def update(self):
        self.trail.append(Vector2(self.getPos()))
        if len(self.trail) > self.trail_length:
            self.trail.pop(0)

    def draw(self, drawSurface):
        for fixture in self.square_body.fixtures:
            self.draw_square(fixture.shape, self.square_body, fixture, drawSurface)

    def draw_square(self, polygon, body, fixture, surface):
        vertices = [(utils.to_Pos(body.transform * v)) for v in polygon.vertices]
        pygame.draw.polygon(surface, (0, 0, 0), [[int(v[0]), int(v[1])] for v in vertices])
        pygame.draw.polygon(surface, self.color, [[int(v[0]), int(v[1])] for v in vertices], 2)



    def getPos(self):
        p = utils.to_Pos(self.square_body.position)
        return Vector2(p[0], p[1])
