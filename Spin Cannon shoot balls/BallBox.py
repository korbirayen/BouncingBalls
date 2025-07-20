import math
import random

import pygame
from Box2D import b2PolygonShape, Box2D
from pygame import Vector2
import  copy
from util import utils



class BallBox:
    def __init__(self, pos, side_length= 3,color = (255, 255, 255)):
        self.color = color
        self.side_length = side_length

        vertices = []
        self.size = 8
        for i in range(self.size):
            angle = i * (2 * Box2D.b2_pi / self.size)
            x = side_length * math.cos(angle)
            y = side_length * math.sin(angle)
            vertices.append((x, y))

        self.shape = b2PolygonShape(vertices=vertices)
        self.body = utils.world.CreateDynamicBody(position=utils.from_Pos(pos))
        self.pentagon_fixture = self.body.CreatePolygonFixture(shape=self.shape, density=1, friction=0.0,
                                                              restitution=1.05)

        # self.box_body = utils.world.CreateDynamicBody(position=utils.from_Pos((pos.x, pos.y)))
        # self.box_shape = self.box_body.CreatePolygonFixture(box=(self.side_length, self.side_length),
        #                                                     density=1, friction=0.0, restitution=1.05)
        self.body.linearVelocity = (random.uniform(-30,30), random.uniform(-5, -5))
        self.body.userData = self
        self.deathTime = 6

        self.trail = []  # List to store trail positions
        self.trail_length = 50  # Length of the trail
        self.headColor = (255,255,255)
        self.spawn = False

        self.body.angle = 0
        self.body.fixedRotation = True

        self.angle = 0
        self.bodyPos = self.body.position

    def draw(self):
        if self.deathTime > 0:
            self.deathTime -= utils.deltaTime()
            if self.deathTime <= 0:
                self.convert_to_static()
        if self.deathTime <= 0:
            self.headColor = self.color

        self.update_trail()
        self.draw_trail()
        # for fixture in self.body.fixtures:
        #     self.draw_square(fixture.shape, self.box_body, fixture)
        self.angle = 0
        self.bodyPos = self.body.position
        self.draw_pentagon(self.shape)

        if self.deathTime > 0:
            textSize = utils.font16.render(str(int(self.deathTime)), True, (0, 0, 0))
            utils.drawText(Vector2(self.getPos().x - textSize.get_width() / 2, self.getPos().y - textSize.get_height() / 2)
                           , str(int(self.deathTime)), (255, 255, 255), utils.font16)

    def draw_square(self, polygon, body, fixture):
        vertices = [utils.to_Pos(body.transform * v) for v in polygon.vertices]
        pygame.draw.polygon(utils.screen, (23,23,23), vertices)
        pygame.draw.polygon(utils.screen, self.headColor, vertices,2)

    def getPos(self):
        p = utils.to_Pos(self.body.position)
        return Vector2(p[0], p[1])

    def increase_side_length(self, side_length):
        self.side_length = side_length
        self.box_body.DestroyFixture(self.box_shape)
        self.box_shape = self.box_body.CreatePolygonFixture(box=(self.side_length, self.side_length), density=1, friction=0.0, restitution=1.05)
        # Optionally, update the userData if it depends on side_length
        self.box_body.userData = self


    def convert_to_static(self):
        if self.body is None:
            return

        # Get the current position and angle of the dynamic body
        # position = self.body.position

        angle = self.body.angle

        # Destroy the dynamic body
        utils.world.DestroyBody(self.body)

        # Create a static body with the same shape and position
        self.body = utils.world.CreateStaticBody(position=utils.from_Pos(Vector2(utils.width/2,utils.height/2)), angle=angle)
        self.shape = b2PolygonShape(vertices=self.shape.vertices)
        self.body.CreatePolygonFixture(shape=self.shape, density=1, friction=0.0, restitution=1.05)
        self.body.userData = self


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
        for verticles,color in self.trail:
            for v in verticles:
                pygame.draw.polygon(utils.screen, (23, 23, 23), v)
                pygame.draw.polygon(utils.screen, color, v, 2)

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