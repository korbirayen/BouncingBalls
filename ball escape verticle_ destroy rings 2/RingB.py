import math
import random

import pygame
from Box2D import b2EdgeShape, Box2D, b2Filter
from pygame import Vector2

from Line import Line
from particle import Explosion
from util import utils


class RingB:
    def __init__(self,id, center, radius,particlesCallback,dir =1, sar = 0,hue = 0,isUp = False ):
        self.color = (255,255,255)
        self.radius = radius
        self.sar = sar
        self.hue = hue
        self.center = center
        self.id = id

        self.rotateDir = dir
        self.size = 90
        self.vertices = []
        self.particlesCallback = particlesCallback

        self.lines = []
        self.isUp = isUp


        for i in range(self.size):
            angle = i * (2 * math.pi / self.size)
            x = radius * 10 * math.cos(angle) + self.center.x
            y = radius * 10 * math.sin(angle) + self.center.y
            self.vertices.append((x, y))

        # self.body = utils.world.CreateStaticBody(position=utils.from_Pos(self.center))
        # self.body.userData = self

        self.create_edge_shape()
        self.destroyFlag = False

        self.color = utils.saturationToRGB(self.sar,self.hue)

    def create_edge_shape(self):
        if self.size == 90:
            for i in range(self.size):
                angle = i * (360 / self.size)
                if not self.isUp:
                    if 40 <= angle <= 130:
                        v1 = self.vertices[i]
                        v2 = self.vertices[(i + 1) % self.size]
                        line = Line(Vector2(v1),Vector2(v2),utils.saturationToRGB(self.sar,self.hue))
                        self.lines.append(line)
                else:
                    if 40 + 180 <= angle <= 130 + 180:
                        v1 = self.vertices[i]
                        v2 = self.vertices[(i + 1) % self.size]
                        line = Line(Vector2(v1),Vector2(v2),utils.saturationToRGB(self.sar,self.hue))
                        self.lines.append(line)

        if self.size  <= 16:
            for i in range(self.size):
                if i == 0:
                    holeSize = self.radius/5
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
        for line in self.lines:
            if line.destroyFlag:
                utils.world.DestroyBody(line.body)
                self.lines.remove(line)
                exp1 = Explosion(line.start_pos.x, line.start_pos.y, self.color)
                exp2 = Explosion(line.end_pos.x, line.end_pos.y, self.color)
                self.particlesCallback(exp1)
                self.particlesCallback(exp2)


    def draw(self):
        for line in self.lines:
            line.draw()

    def spawParticles(self):
        particles = []
        center = Vector2(utils.width/2,utils.height/2)
        if self.size == 90:
            for i in range(0,360,1):
                # if i >= hole_start and i <= hole_end:
                x = math.cos(math.radians(i)) * self.radius * 10
                y = math.sin(math.radians(i)) * self.radius * 10
                pos = center + Vector2(x,y)
                exp = Explosion(pos.x,pos.y,self.color)
                particles.append(exp)
        else:
            for p in self.points:
                pos = p
                exp = Explosion(pos.x, pos.y, self.color)
                particles.append(exp)
        return particles

    def draw_edges(self):
        for fixture in self.body.fixtures:
            v1 = utils.to_Pos(self.body.transform * fixture.shape.vertices[0])
            v2 = utils.to_Pos(self.body.transform * fixture.shape.vertices[1])
            pygame.draw.line(utils.screen, self.color, v1, v2, 4)
        # for p in self.points:
        #     pygame.draw.circle(utils.screen,(233,233,23),p,2)

    def is_point_in_polygon(self,point, vertices):
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