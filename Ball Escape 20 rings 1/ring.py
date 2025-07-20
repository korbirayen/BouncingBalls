import math
import pygame
from pygame import Vector2

from particle import Explosion
from util import utils
import colorsys
import pygame.gfxdraw

import utils
class Ring:
    def __init__(self,id, radius,dir =1, sar = 0):
        self.id = id
        self.boxes = []
        self.dir = dir
        self.initial_positions = []
        self.color = utils.saturationToRGB(sar)
        self.center = Vector2(utils.width / 2, utils.height / 2)
        self.angle = 0
        self.radius = radius
        self.rotation_speed = 1  # Degrees per frame
        self.hole_start_angle = 90
        self.hole_end_angle = 120
        self.destroyFlag = False

        self.size = 100
        self.vertices = []
        for i in range(self.size):
            angle = i * (2 * math.pi / self.size)
            d_angle =  math.degrees(angle)
            if self.hole_start_angle <= d_angle <= self.hole_end_angle:
                continue
            x = radius * math.cos(angle)
            y = radius * math.sin(angle)
            self.vertices.append((self.center.x + x, self.center.y + y))

    def update(self):
        self.angle = (self.angle + self.rotation_speed * self.dir) % 360  # Update angle and wrap around at 360

    def getHole(self):
        hole_start = (self.hole_start_angle + self.angle) % 360
        hole_end = (self.hole_end_angle + self.angle) % 360
        return hole_start, hole_end

    def drawArc(self,surface, x, y, r, th, start, stop, color):
        points_outer = []
        points_inner = []
        n = round(r * abs(stop - start) / 20)
        if n < 2:
            n = 2
        for i in range(n):
            delta = i / (n - 1)
            phi0 = start + (stop - start) * delta
            x0 = round(x + r * math.cos(phi0))
            y0 = round(y + r * math.sin(phi0))
            points_outer.append([x0, y0])
            phi1 = stop + (start - stop) * delta
            x1 = round(x + (r - th) * math.cos(phi1))
            y1 = round(y + (r - th) * math.sin(phi1))
            points_inner.append([x1, y1])
        points = points_outer + points_inner
        pygame.gfxdraw.aapolygon(surface, points, color)
        pygame.gfxdraw.filled_polygon(surface, points, color)

    def draw(self):
        hole_start, hole_end = self.getHole()
        pygame.draw.polygon(utils.screen,self.color,self.vertices,2)


    def spawParticles(self):
        particles = []
        hole_start, hole_end = self.getHole()
        center = Vector2(utils.width/2,utils.height/2)
        for i in range(0,360,5):
            # if i >= hole_start and i <= hole_end:
            x = math.cos(math.radians(i)) * self.radius
            y = math.sin(math.radians(i)) * self.radius
            pos = center + Vector2(x,y)
            exp = Explosion(pos.x,pos.y)
            particles.append(exp)
        return particles