import pygame
from Box2D import b2World, b2BodyDef, b2EdgeShape, b2_staticBody

from util import utils


class Line:
    def __init__(self, start_pos, end_pos,color = (23,255,255)):
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.color = color
        # Convert Pygame coordinates to Box2D coordinates
        box2d_start = utils.from_Pos(self.start_pos)
        box2d_end = utils.from_Pos(self.end_pos)

        # Define the static body
        body_def = b2BodyDef()
        body_def.position = (0, 0)  # Position is relative, lines have absolute positions
        body_def.type = b2_staticBody

        # Create the body
        self.body = utils.world.CreateBody(body_def)
        self.body.userData = self

        # Define the edge shape
        edge_shape = b2EdgeShape(vertices=[box2d_start, box2d_end])

        # Create the fixture
        self.body.CreateFixture(shape=edge_shape)
        self.destroyFlag = False


    def draw(self):
        pygame_start_pos = utils.to_Pos(self.body.fixtures[0].shape.vertices[0])
        pygame_end_pos = utils.to_Pos(self.body.fixtures[0].shape.vertices[1])
        pygame.draw.line(utils.screen, self.color, pygame_start_pos, pygame_end_pos,3)
