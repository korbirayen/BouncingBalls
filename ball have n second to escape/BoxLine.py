import math
import pygame
from pygame import Vector2

from utils.util import utils


class BoxLine:
    def __init__(self, pos, color):
        self.width = 5
        self.height = 0.5
        self.box_body = utils.world.CreateStaticBody(position=(utils.from_Pos((pos.x, pos.y))))
        self.box_shape = self.box_body.CreatePolygonFixture(box=(self.width, self.height), density=1, friction=0.0, restitution=1.0)
        self.color = color
        self.destroyFlag = False
        self.box_body.userData = self
        self.movingAngle = 350
        self.angle = 0  # Initial angle

    def draw(self):
        self.angle += 5

        self.movingAngle += 1
        rad = math.radians(self.movingAngle)
        x = math.cos(rad) * 250
        y = math.sin(rad) * 250
        pos = Vector2(utils.width / 2, utils.height / 2) + Vector2(x, y)
        self.box_body.position = utils.from_Pos(pos)

        # Set the rotation of the box body
        self.box_body.angle = math.radians(self.angle)

        for fixture in self.box_body.fixtures:
            self.draw_polygon(fixture.shape, self.box_body, fixture)

    def draw_polygon(self, polygon, body, fixture):
        vertices = [utils.to_Pos(body.transform * v) for v in polygon.vertices]
        pygame.draw.polygon(utils.screen, self.color, vertices,4)

    def setPos(self, pos):
        position = utils.from_Pos((pos.x, pos.y))
        self.box_body.position = position

    def rotate(self, angle):
        self.angle = angle  # Update the angle