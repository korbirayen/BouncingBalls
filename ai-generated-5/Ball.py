import pygame
import random
from pygame import Vector2
from util import utils

class Ball:
    def __init__(self, pos, radius=2, color=(255, 255, 255), gravityScale=1):
        self.color = color
        self.radius = radius
        self.circle_body = utils.world.CreateDynamicBody(position=utils.from_Pos((pos.x, pos.y)))
        self.circle_shape = self.circle_body.CreateCircleFixture(radius=self.radius, density=1, friction=0.1, restitution=0.8)
        self.circle_body.gravityScale = gravityScale
        self.circle_body.userData = self

    def draw(self):
        position = utils.to_Pos(self.circle_body.position)
        pygame.draw.circle(utils.screen, self.color, [int(x) for x in position], int(self.radius * utils.PPM))

    def getPos(self):
        p = utils.to_Pos(self.circle_body.position)
        return Vector2(p[0], p[1])

    def setRadius(self, new_radius):
        for fixture in self.circle_body.fixtures:
            self.circle_body.DestroyFixture(fixture)
        self.radius = new_radius
        self.circle_shape = self.circle_body.CreateCircleFixture(radius=self.radius, density=1, friction=0.1, restitution=0.8)
