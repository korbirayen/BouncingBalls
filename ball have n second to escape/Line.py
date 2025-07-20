import math

import pygame
from Box2D import b2World, b2BodyDef, b2EdgeShape, b2_staticBody
from pygame import Vector2

from utils.util import utils


class Line:
    def __init__(self, start_pos, end_pos):
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.lives = 3

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

        self.movingAngle = 0

    def get_color(self):
        """Return color based on remaining lives."""
        if self.lives == 3:
            return (255, 255, 255)  # Green for 3 lives
        elif self.lives == 2:
            return (123, 23, 23)  # Yellow for 2 lives
        elif self.lives == 1:
            return (255, 0, 0)  # Red for 1 life
        else:
            return (255, 255, 255)  # Default to white if lives are invalid

    def draw(self):

        if self.lives <= 0:
            self.destroyFlag = True


        pygame_start_pos = utils.to_Pos(self.body.fixtures[0].shape.vertices[0])
        pygame_end_pos = utils.to_Pos(self.body.fixtures[0].shape.vertices[1])
        pygame.draw.line(utils.screen, (233,23,23), pygame_start_pos, pygame_end_pos,6)
