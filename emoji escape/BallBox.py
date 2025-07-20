import colorsys
import math
import random

import pygame
from Box2D import b2PolygonShape, Box2D
from pygame import Vector2
import  copy
from util import utils

class BallBox:
    def __init__(self, pos, side_length= 20,color = (255, 255, 255)):
        self.color = color
        self.color = (231, 111, 81)

        self.side_length = side_length

        vertices = []
        self.size = 3
        for i in range(self.size):
            angle = i * (2 * Box2D.b2_pi / self.size)
            x = side_length * math.cos(angle)
            y = side_length * math.sin(angle)
            vertices.append((x, y))

        self.shape = b2PolygonShape(vertices=vertices)
        self.body = utils.world.CreateDynamicBody(position=utils.from_Pos(pos))
        self.pentagon_fixture = self.body.CreatePolygonFixture(shape=self.shape, density=1, friction=0.5,
                                                              restitution=1.0)

        # self.box_body = utils.world.CreateDynamicBody(position=utils.from_Pos((pos.x, pos.y)))
        # self.box_shape = self.box_body.CreatePolygonFixture(box=(self.side_length, self.side_length),
        #                                                     density=1, friction=0.0, restitution=1.05)
        self.body.linearVelocity = (random.uniform(-5,5), random.uniform(-5, -5))
        self.body.userData = self
        self.deathTime = 6

        self.trail = []  # List to store trail positions
        self.trail_length = 15  # Length of the trail
        self.headColor = (255,23,23)
        self.spawn = False

        self.body.angle = 0
        # self.body.fixedRotation = True

        self.angle = 0
        self.bodyPos = self.body.position

        self.time_since_last_color_change = 0  # Timer for color change
        self.color_change_interval = 0.001  # Interval in milliseconds (1 second)
        self.hue = 0
        self.update_color_gradient()

    def draw(self):
        # Update color every second
        self.time_since_last_color_change += utils.deltaTime()
        if self.time_since_last_color_change >= self.color_change_interval:
            self.update_color_gradient()
            self.time_since_last_color_change = 0

        self.update_trail()
        self.draw_trail()
        # for fixture in self.body.fixtures:
        #     self.draw_square(fixture.shape, self.box_body, fixture)
        self.bodyPos = self.body.position
        # self.draw_pentagon(self.shape)


    def draw_square(self, polygon, body, fixture):
        vertices = [utils.to_Pos(body.transform * v) for v in polygon.vertices]
        pygame.draw.polygon(utils.screen, (23,23,23), vertices)
        pygame.draw.polygon(utils.screen, self.headColor, vertices,2)

    def getPos(self):
        p = utils.to_Pos(self.body.position)
        return Vector2(p[0], p[1])

    def increase_side_length(self, side_length):
        self.side_length = side_length

        # Destroy the existing fixture
        self.body.DestroyFixture(self.pentagon_fixture)

        # Calculate the new vertices based on the new side length
        self.size = 3
        vertices = []
        for i in range(self.size):
            angle = i * (2 * Box2D.b2_pi / self.size)
            x = side_length * math.cos(angle)
            y = side_length * math.sin(angle)
            vertices.append((x, y))

        # Create the new shape and fixture
        self.shape = b2PolygonShape(vertices=vertices)
        self.pentagon_fixture = self.body.CreatePolygonFixture(shape=self.shape, density=1, friction=0.5,
                                                                restitution=1.0)

        # Update the userData if it depends on side_length
        self.body.userData = self

    def convert_to_static(self):
        if self.body is None:
            return

        # Get the current position and angle of the dynamic body
        position = self.body.position
        angle = self.body.angle

        # Destroy the dynamic body
        utils.world.DestroyBody(self.body)

        # Create a static body with the same shape and position
        self.body = utils.world.CreateStaticBody(position=position, angle=angle)
        self.shape = b2PolygonShape(vertices=self.shape.vertices)
        self.body.CreatePolygonFixture(shape=self.shape, density=1, friction=0.0, restitution=1.05)
        self.body.userData = self

    def update_color_gradient(self):
        # Increment hue and wrap around if it exceeds 1.0
        self.hue = (self.hue + 0.01) % 1.0
        # Convert HSV to RGB
        r, g, b = colorsys.hsv_to_rgb(self.hue, 1, 1)
        # Scale RGB values to 0-255 range
        self.color = (int(r * 255), int(g * 255), int(b * 255))

    def update_trail(self):
        verticles = []
        for fixture in self.body.fixtures:
            v = [utils.to_Pos(self.body.transform * v) for v in fixture.shape.vertices]
        verticles.append(v)

        self.trail.append((verticles,self.color))
        # Limit the length of the trail
        if len(self.trail) > self.trail_length:
            self.trail.pop(0)

    def draw_trail(self):
        i = 0
        for verticles,color in self.trail:
            if i == len(self.trail)-1:
                for v in verticles:
                    pygame.draw.polygon(utils.screen, (255,255,255), v)
                    pygame.draw.polygon(utils.screen, (23,23,23), v, 5)
            else:
                for v in verticles:
                    # pygame.draw.polygon(utils.screen, (255,23,255), v)
                    pygame.draw.polygon(utils.screen, color, v)
            i += 1

    def draw_pentagon(self, shape):

        # Convert Box2D vertices to Pygame coordinates
        vertices = []
        for vertex in shape.vertices:
            rotated_vertex = Box2D.b2Vec2(
                vertex[0] * math.cos(self.angle) - vertex[1] * math.sin(self.angle),
                vertex[0] * math.sin(self.angle) + vertex[1] * math.cos(self.angle)
            )
            vertices.append(utils.to_Pos(self.bodyPos + rotated_vertex))

        # Draw the pentagon
        pygame.draw.polygon(utils.screen, self.color, vertices, 2)