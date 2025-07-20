import math
import random

import pygame
from Box2D import b2PolygonShape
from pygame import Vector2
import Box2D
from util import utils


class Polygon:
    def __init__(self,pos,radius = 1.8):
        self.color = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
        self.color = (231, 111, 81)
        self.radius = radius
        self.isStop = False
        self.destroyFlag = False
        vertices = []
        self.size = 16
        self.rSize = 60
        for i in range(self.size):
            angle = i * (2 * Box2D.b2_pi / self.size)
            x = radius * math.cos(angle)
            y = radius * math.sin(angle)
            vertices.append((x, y))

        self.shape = b2PolygonShape(vertices=vertices)
        self.body = utils.world.CreateDynamicBody(position=utils.from_Pos(pos))
        self.pentagon_fixture = self.body.CreatePolygonFixture(shape=self.shape, density=1, friction=0.0,
                                                              restitution=1.05)
        self.body.userData = self

        # Optionally set an initial velocity
        self.body.linearVelocity = (random.uniform(-10,10), random.uniform(-20,-20))
        # self.body.angularVelocity = 0
        self.angle = 0
        self.bodyPos = self.body.position
        self.body.gravityScale = 0.5
        self.deathTime = 6

    def changeSize(self,size):
        self.rSize = size
        self.size = size
        print(self.size)
        if self.rSize > 16:
            self.size = 16
        if self.rSize < 3:
            self.size = 3
            self.rSize = 3

        angularVelocity = self.body.angularVelocity
        linearVelocity = self.body.linearVelocity
        vertices = []
        for i in range(self.size):
            angle = i * (2 * Box2D.b2_pi / self.size)
            x = self.radius * math.cos(angle)
            y = self.radius * math.sin(angle)
            vertices.append((x, y))

        self.shape = b2PolygonShape(vertices=vertices)
        # self.body = utils.world.CreateDynamicBody(position=self.bodyPos)
        self.pentagon_fixture = self.body.CreatePolygonFixture(shape=self.shape, density=5, friction=0.0,
                                                              restitution=1.0)
        # self.body.userData = self
        # self.body.angle = self.angle
        # self.body.angularVelocity += 1
        # # self.body.linearVelocity = linearVelocity
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
        self.draw_pentagon(self.shape)

        textSize = utils.font32.render(str(self.rSize), True, (0, 0, 0))
        utils.drawText(Vector2(self.getPos().x - textSize.get_width()/2,self.getPos().y - textSize.get_height()/2)
                       ,str(self.rSize),(233,233,233),utils.font32)

    def draw_pentagon(self, shape):

        # Convert Box2D vertices to Pygame coordinates
        vertices = []
        for vertex in shape.vertices:
            rotated_vertex = Box2D.b2Vec2(
                        vertex[0] * math.cos(self.angle) - vertex[1] * math.sin(self.angle),
                        vertex[0] * math.sin(self.angle) + vertex[1] * math.cos(self.angle)
                    )
            vertices.append(utils.to_Pos(self.bodyPos + rotated_vertex))

        # Draw the pentagon
        pygame.draw.polygon(utils.screen,self.color, vertices,2)

    def getPos(self):
        p = utils.to_Pos(self.bodyPos)
        return Vector2(p[0],p[1])