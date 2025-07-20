import random

import pygame
from pygame import Vector2

from util import utils


class Ball:
    def __init__(self,pos,radius ,color):
        self.color = color
        self.radius = radius
        self.circle_body = utils.world.CreateDynamicBody(position=utils.from_Pos((pos.x, pos.y)))
        self.circle_shape = self.circle_body.CreateCircleFixture(radius=self.radius, density=1, friction=0.0,
                                                                 restitution=1.0)
        self.circle_body.linearVelocity = (random.uniform(-5,5), random.uniform(-5,-5))
        self.circle_body.userData = self
        self.destroyFlag = False

        self.increaseRadiusDelay = 0

    def update(self):
        self.increaseRadiusDelay += utils.deltaTime()
        if self.increaseRadiusDelay > 0.1:
            self.increaseRadiusDelay = 0
            self.set_radius(self.radius*1.01)

    def draw(self):
        for fixture in self.circle_body.fixtures:
            self.draw_circle(fixture.shape, self.circle_body, fixture)

    def draw_circle(self,circle, body, fixture):
        position = utils.to_Pos(body.transform * circle.pos)
        pygame.draw.circle(utils.screen, self.color, [int(x) for x in position], int(circle.radius * utils.PPM))

    def getPos(self):
        p = utils.to_Pos(self.circle_body.position)
        return Vector2(p[0],p[1])

    def set_radius(self, radius):
        self.radius = radius
        self.circle_body.DestroyFixture(self.circle_shape)
        self.circle_shape = self.circle_body.CreateCircleFixture(radius=self.radius, density=1, friction=0.0, restitution=1.00)
        # Optionally, update the userData if it depends on radius
        self.circle_body.userData = self

    def getRect(self):
        return pygame.Rect(self.getPos().x - self.radius*10,self.getPos().y - self.radius*10,self.radius*10*2,self.radius*10*2)