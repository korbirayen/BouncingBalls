import math
import random

import pygame
from Box2D import b2PolygonShape, b2EdgeShape, b2Vec2, Box2D
from pygame import Vector2
from util import utils


def point_in_polygon(point, polygon):
    x, y = point
    inside = False
    for i in range(len(polygon)):
        j = (i + 1) % len(polygon)
        xi, yi = polygon[i]
        xj, yj = polygon[j]
        intersect = ((yi > y) != (yj > y)) and (x < (xj - xi) * (y - yi) / (yj - yi) + xi)
        if intersect:
            inside = not inside
    return inside
class EdgePolygon:
    def __init__(self, pos, side_length=3,size = 3, color=(255, 255, 255)):
        self.color = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
        self.side_length = side_length

        self.size = size
        self.vertices = []
        for i in range(self.size):
            angle = i * (2 * math.pi / self.size)
            x = side_length * math.cos(angle)
            y = side_length * math.sin(angle)
            self.vertices.append((x, y))

        self.body = utils.world.CreateDynamicBody(position=utils.from_Pos(pos))
        self.create_edge_shape()

        self.body.linearVelocity = (random.uniform(-30, 30), random.uniform(-20, -20))
        self.body.userData = self
        self.deathTime = 6

        self.bodyPos = self.body.position
        self.isStatic = False
        self.angle = 1.5707
        self.angle = 0
        self.body.angle = self.angle

    def getVerticles(self):
        vertices = []
        for v in self.vertices:
            vertices.append(utils.to_Pos(v))
        return vertices


    def can_shrink(self, other_polygon):
        offset_x, offset_y = (0.5,0.5)
        for vertex in other_polygon.vertices:
            offset_vertex = (vertex[0] + offset_x, vertex[1] + offset_y)
            if not point_in_polygon(offset_vertex, self.vertices):
                return False
        return True

    def create_edge_shape(self):
        for i in range(self.size):
            v1 = self.vertices[i]
            v2 = self.vertices[(i + 1) % self.size]
            edge = b2EdgeShape(vertices=[v1, v2])
            self.body.CreateEdgeFixture(shape=edge, density=1, friction=0.0, restitution=1.05)

    def draw(self):
        self.bodyPos = self.body.position
        if self.isStatic:
            self.draw_pentagon(self.shape)
            return
        self.draw_edges()

    def getPos(self):
        p = utils.to_Pos(self.body.position)
        return Vector2(p[0], p[1])

    def convert_to_static(self):
        if self.body is None:
            return

        self.isStatic = True
        position = self.body.position
        angle = self.body.angle

        # Store vertices from edge shapes
        if self.size > 16:
            self.size = 16
        self.vertices = []
        for i in range(self.size):
            angle = i * (2 * math.pi / self.size)
            x = self.side_length * math.cos(angle)
            y = self.side_length * math.sin(angle)
            self.vertices.append((x, y))

        # Destroy the dynamic body
        utils.world.DestroyBody(self.body)

        # Create a new static body with a polygon shape
        self.body = utils.world.CreateStaticBody(position=utils.from_Pos(Vector2(utils.width/2,utils.height/2)), angle=angle)
        polygon_shape = b2PolygonShape(vertices=self.vertices)
        self.shape = self.body.CreatePolygonFixture(shape=polygon_shape, density=1, friction=0.0, restitution=1.05)
        self.body.userData = self

    def draw_pentagon(self, shape):

        # Convert Box2D vertices to Pygame coordinates
        vertices = []
        for vertex in self.vertices:
            rotated_vertex = Box2D.b2Vec2(
                vertex[0] * math.cos(self.angle) - vertex[1] * math.sin(self.angle),
                vertex[0] * math.sin(self.angle) + vertex[1] * math.cos(self.angle)
            )
            vertices.append(utils.to_Pos(self.bodyPos + rotated_vertex))

        # Draw the pentagon
        pygame.draw.polygon(utils.screen, self.color, vertices, 6)

    def draw_edges(self):
        for fixture in self.body.fixtures:
            v1 = utils.to_Pos(self.body.transform * fixture.shape.vertices[0])
            v2 = utils.to_Pos(self.body.transform * fixture.shape.vertices[1])
            pygame.draw.line(utils.screen, self.color, v1, v2, 6)

    def change_side_length(self, new_side_length):
        self.side_length = new_side_length
        self.vertices = []
        for i in range(self.size):
            angle = i * (2 * math.pi / self.size)
            x = new_side_length * math.cos(angle)
            y = new_side_length * math.sin(angle)
            self.vertices.append((x, y))

        # Destroy current fixtures
        for fixture in self.body.fixtures:
            self.body.DestroyFixture(fixture)

        # Recreate edge shape
        self.create_edge_shape()