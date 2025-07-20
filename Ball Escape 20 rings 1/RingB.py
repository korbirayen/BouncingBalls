import math
import random

import pygame
from Box2D import b2EdgeShape, Box2D, b2Filter
from pygame import Vector2

from particle import Explosion
from util import utils


class RingB:
    def __init__(self, id, radius,dir =-1, sar = 5):
        self.color = (255,255,255)
        self.radius = radius
        self.id = id
        self.sar = sar

        self.rotateDir = dir
        self.size = 90
        self.vertices = []
        for i in range(self.size):
            angle = i * (2 * math.pi / self.size)
            x = radius * math.cos(angle)
            y = radius * math.sin(angle)
            self.vertices.append((x, y))

        pos = Vector2(utils.width/2,utils.height/2)
        self.body = utils.world.CreateStaticBody(position=utils.from_Pos(pos))
        self.body.userData = self

        self.create_edge_shape()
        self.hue = random.uniform(0.5,2)
        self.destroyFlag = False

        self.hue = (self.sar + utils.deltaTime() / 50) % 1
        self.color = utils.saturationToRGB(self.hue)


    def create_edge_shape(self):
        if self.size == 90:
            for i in range(self.size):
                angle = i * (360 / self.size)
                if (0 <= angle <= 315) :
                    v1 = self.vertices[i]
                    v2 = self.vertices[(i + 1) % self.size]
                    edge = b2EdgeShape(vertices=[v1, v2])
                    self.body.CreateEdgeFixture(shape=edge, density=1, friction=0.0, restitution=1.0)
        if self.size == 3 or self.size == 4 :
            for i in range(self.size):
                if i == 0:
                    holeSize = 8
                    v1 = Vector2(self.vertices[i])
                    v2 = Vector2(self.vertices[(i + 1) % self.size])
                    length = (v2 - v1).length()
                    dir = (v2 - v1).normalize()
                    mV1 = v1 + dir * (length / 2 - holeSize)
                    mV2 = v1 + dir * (length / 2 + holeSize)

                    edge = b2EdgeShape(vertices=[v1, mV1])
                    self.body.CreateEdgeFixture(shape=edge, density=1, friction=0.0, restitution=1.0)

                    edge = b2EdgeShape(vertices=[mV2, v2])
                    self.body.CreateEdgeFixture(shape=edge, density=1, friction=0.0, restitution=1.0)
                else:
                    v1 = self.vertices[i]
                    v2 = self.vertices[(i + 1) % self.size]
                    edge = b2EdgeShape(vertices=[v1, v2])
                    self.body.CreateEdgeFixture(shape=edge, density=1, friction=0.0, restitution=1.0)


    def update(self):
        # Increment the hue value; use modulus to keep it in the range [0, 1]
        self.hue = (self.hue + 0) % 1  # Adjust the 0.001 value to control the speed of hue change

        # Interpolate the color from white to yellow based on the hue
        red_value = 255
        green_value = 200
        blue_value = int(255 * (1 - self.hue))  # Decrease blue as hue increases

        # Set the color with full red and green, and decreasing blue
        self.color = (red_value, green_value, blue_value)

        # Update the rotation
        self.body.angle += self.rotateDir * utils.deltaTime()



    def draw(self):
        self.draw_edges()

    def spawParticles(self):
        particles = []
        center = Vector2(utils.width/2,utils.height/2)
        for i in range(0,360,2):
            # if i >= hole_start and i <= hole_end:
            x = math.cos(math.radians(i)) * self.radius * 10
            y = math.sin(math.radians(i)) * self.radius * 10
            pos = center + Vector2(x,y)
            exp = Explosion(pos.x,pos.y,self.color)
            particles.append(exp)
        return particles

    def draw_edges(self):
        for fixture in self.body.fixtures:
            v1 = utils.to_Pos(self.body.transform * fixture.shape.vertices[0])
            v2 = utils.to_Pos(self.body.transform * fixture.shape.vertices[1])
            pygame.draw.line(utils.screen, self.color, v1, v2, 5)

