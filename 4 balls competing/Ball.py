import random

import pygame
from pygame import Vector2

from util import utils


class Ball:
    def __init__(self,pos,healthBarPos,radius = 2,color = (255,255,255)):
        self.color = color
        self.radius = radius
        self.circle_body = utils.world.CreateDynamicBody(position=(utils.from_Pos((pos.x, pos.y))))
        self.circle_shape = self.circle_body.CreateCircleFixture(radius=self.radius, density=1, friction=0.0, restitution=1)
        self.circle_body.linearVelocity = (random.uniform(-0,0), random.uniform(-0,-0))
        self.circle_body.userData = self

        self.healthBarPos = healthBarPos
        self.health = 100
        self.maxHealth = 100
        self.minHealth = 0
        self.maxRadius = radius
        self.minRadius = 0.5

    def draw(self):
        x = self.healthBarPos.x
        y = self.healthBarPos.y
        for i in range(self.health):
            pygame.draw.rect(utils.screen,self.color,(x,y,2,10))
            x += 5

        for fixture in self.circle_body.fixtures:
            self.draw_circle(fixture.shape, self.circle_body, fixture)

    def draw_circle(self,circle, body, fixture):
        position = utils.to_Pos(body.transform * circle.pos)
        pygame.draw.circle(utils.screen, self.color, [int(x) for x in position], int(circle.radius * utils.PPM))

    def getPos(self):
        p = utils.to_Pos(self.circle_body.position)
        return Vector2(p[0],p[1])

    def setRadius(self, new_radius):
        for fixture in self.circle_body.fixtures:
            self.circle_body.DestroyFixture(fixture)

        self.radius = new_radius
        self.health = int((new_radius - self.minRadius) / (self.maxRadius - self.minRadius) * self.maxHealth)

        self.circle_shape = self.circle_body.CreateCircleFixture(radius=self.radius, density=1, friction=0.0,
                                                                 restitution=1.)