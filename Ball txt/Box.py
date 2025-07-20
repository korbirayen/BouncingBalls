
import pygame
from pygame import Vector2

from util import utils


class Box:
    def __init__(self,pos,color):
        self.width = 0.2
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
        pygame.draw.polygon(utils.screen, self.color, vertices)

    def setPos(self,pos):
        position = utils.from_Pos((pos.x, pos.y))
        self.box_body.position = position
