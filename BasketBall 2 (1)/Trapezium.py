import math
import random

import pygame
from Box2D import b2PolygonShape
from pygame import Vector2
import Box2D
from util import utils


class Trapezium:
    def __init__(self, points,pos):
        if len(points) != 4:
            raise ValueError("Four points are required to define a trapezium")

        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.color = (0,0,0)
        self.isStop = False
        self.destroyFlag = False
        # self.vertices = [utils.from_Pos(point) for point in points]
        self.vertices = points

        self.shape = b2PolygonShape(vertices=self.vertices)
        self.body = utils.world.CreateStaticBody(
            position=utils.from_Pos(pos))  # Position the body at the first point
        self.trapezium_fixture = self.body.CreatePolygonFixture(shape=self.shape, density=1, friction=0.0,
                                                                restitution=1.0)
        self.body.userData = self

        # Optionally set an initial velocity
        self.body.linearVelocity = (random.uniform(-10, 10), random.uniform(-20, -20))
        self.angle = 0
        self.bodyPos = self.body.position
        self.body.gravityScale = 0.5
        self.deathTime = 6

    def stop(self):
        self.isStop = True
        self.body.linearVelocity = (0, 0)
        self.body.angularVelocity = 0
        self.body.gravityScale = 0

    def draw(self):
        if self.isStop:
            self.stop()
        self.angle = 0
        self.bodyPos = self.body.position
        self.draw_trapezium(self.shape)

    def draw_trapezium(self, shape):
        # Convert Box2D vertices to Pygame coordinates
        vertices = []
        for vertex in shape.vertices:
            rotated_vertex = Box2D.b2Vec2(
                vertex[0] * math.cos(self.angle) - vertex[1] * math.sin(self.angle),
                vertex[0] * math.sin(self.angle) + vertex[1] * math.cos(self.angle)
            )
            vertices.append(utils.to_Pos(self.bodyPos + rotated_vertex))

        # Draw the trapezium
        pygame.draw.polygon(utils.screen, self.color, vertices)

    def getPos(self):
        p = utils.to_Pos(self.bodyPos)
        return Vector2(p[0], p[1])


# # Example usage:
# points = [
#     Vector2(100, 100),
#     Vector2(200, 100),
#     Vector2(250, 200),
#     Vector2(50, 200)
# ]
# trapezium = Trapezium(points)
# trapezium.draw()
