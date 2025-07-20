
import math
import random

import pygame
from Box2D import b2Filter
from pygame import Vector2

from util import utils


class Ball:
    def __init__(self,pos,radius,color,vel = Vector2(-5,-10),gravityScale = 1):
        self.color = color
        self.radius = radius
        self.circle_body = utils.world.CreateDynamicBody(position=(utils.from_Pos((pos.x, pos.y))))
        self.circle_shape = self.circle_body.CreateCircleFixture(radius=self.radius, density=1, friction=0.001, restitution=1.0)
        self.circle_body.linearVelocity = vel
        self.circle_body.userData = self
        self.destroyFlag = False
        self.circle_body.gravityScale = gravityScale

        self.trail = []
        self.trail_length = 50

        self.isPlaySound = False

    def update(self):
        self.trail.append(Vector2(self.getPos()))
        if len(self.trail) > self.trail_length:
            self.trail.pop(0)


    def draw(self):
        if len(self.trail) > 0:
            hue = 0
            hueStep = 0.1 / len(self.trail)
            radius = self.radius
            for i, pos in enumerate(self.trail):
                alpha = int(255 * (i / self.trail_length))
                color = utils.saturationToRGB(hue)
                hue += hueStep
                if hue > 1:
                    hue = 0
                surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
                pygame.draw.circle(surface, (color[0],color[1],color[2],alpha), (radius, radius), radius,4)
                utils.screen.blit(surface, (pos.x - radius, pos.y - radius))
                # pygame.draw.circle(utils.screen, (233,233,233), (pos.x, pos.y), radius,1)
                radius *= 1.05

        for fixture in self.circle_body.fixtures:
            self.draw_circle(fixture.shape, self.circle_body, fixture)

    def draw_circle(self,circle, body, fixture):
        position = utils.to_Pos(body.transform * circle.pos)
        pygame.draw.circle(utils.screen, self.color, [int(x) for x in position], int(circle.radius * utils.PPM))

    def getPos(self):
        p = utils.to_Pos(self.circle_body.position)
        return Vector2(p[0],p[1])

