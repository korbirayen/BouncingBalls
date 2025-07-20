import random

import pygame
from Box2D import b2Filter
from pygame import Vector2

from util import utils


class Box:
    def __init__(self,pos,color):
        self.width = 0.1
        self.box_body = utils.world.CreateStaticBody(position=(utils.from_Pos((pos.x, pos.y))))
        self.box_shape = self.box_body.CreatePolygonFixture(box=(self.width,self.width), density=1, friction=0.0, restitution=1.0)
        self.color = color
        self.destroyFlag = False
        self.box_body.userData = self

    def draw(self):
        for fixture in self.box_body.fixtures:
            self.draw_polygon(fixture.shape, self.box_body, fixture)
    def draw_polygon(self,polygon, body, fixture):
        vertices = [utils.to_Pos(body.transform * v) for v in polygon.vertices]
        # print("box",vertices)
        pygame.draw.polygon(utils.screen, self.color, vertices)

    def setPos(self,pos):
        position = utils.from_Pos((pos.x, pos.y))
        self.box_body.position = position

    def getPos(self):
        p = utils.to_Pos(self.box_body.position)
        return Vector2(p[0], p[1])

    def convert_to_dynamic(self):
        # Get current properties
        if self.box_body is None:
            return
        pos = self.box_body.position
        angle = self.box_body.angle
        # Destroy static body
        utils.world.DestroyBody(self.box_body)

        # Create new dynamic body
        self.box_body = utils.world.CreateDynamicBody(position=pos)
        self.box_shape = self.box_body.CreatePolygonFixture(box=(self.width, self.width), density=1, friction=0.0, restitution=1.0)
        self.box_body.userData = self

        # Apply random initial velocity
        initial_velocity = (random.uniform(-10, 10), random.uniform(10, 20))
        self.box_body.linearVelocity = initial_velocity

        collision_filter = b2Filter()
        collision_filter.categoryBits = 0x0002  # Unique category for dynamic box
        collision_filter.maskBits = 0x0000  # Do not collide with any other categories

        self.box_shape.filterData = collision_filter