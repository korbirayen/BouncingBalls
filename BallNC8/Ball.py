import random

import pygame
from pygame import Vector2

from util import utils


class Ball:
    def __init__(self,pos,radius = 0.8):
        self.color = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
        self.radius = radius
        self.circle_body = utils.world.CreateDynamicBody(position=utils.from_Pos((pos.x, pos.y)))
        self.circle_shape = self.circle_body.CreateCircleFixture(radius=self.radius, density=1, friction=0.0,
                                                                 restitution=1.)
        self.circle_body.linearVelocity = (random.uniform(-1,1), random.uniform(-0,-0))
        self.circle_body.userData = self

    def draw(self):
        for fixture in self.circle_body.fixtures:
            self.draw_circle(fixture.shape, self.circle_body, fixture)

    def draw_circle(self,circle, body, fixture):
        position = utils.to_Pos(body.transform * circle.pos)
        pygame.draw.circle(utils.screen, self.color, [int(x) for x in position], int(circle.radius * utils.PPM))

    def getPos(self):
        p = utils.to_Pos(self.circle_body.position)
        return Vector2(p[0],p[1])

    def increase_radius(self, radius):
        self.radius = radius
        self.circle_body.DestroyFixture(self.circle_shape)
        self.circle_shape = self.circle_body.CreateCircleFixture(radius=self.radius, density=1, friction=0.0, restitution=1.05)
        # Optionally, update the userData if it depends on radius
        self.circle_body.userData = self

    def convert_to_static(self):
        # Save the current position and properties
        position = self.circle_body.position
        fixtures = [(f.shape.radius, f.density, f.friction, f.restitution) for f in self.circle_body.fixtures]

        # Destroy the dynamic body
        utils.world.DestroyBody(self.circle_body)

        # Create a static body at the same position
        self.circle_body = utils.world.CreateStaticBody(position=position)

        # Recreate the fixtures with the same properties
        for radius, density, friction, restitution in fixtures:
            self.circle_body.CreateCircleFixture(radius=radius, density=density, friction=friction,
                                                 restitution=restitution)
        # Update userData
        self.circle_body.userData = self