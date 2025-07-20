import random

import pygame
from pygame import Vector2
import  copy
from util import utils

class BallBox:
    def __init__(self, pos, side_length= 2,color = (255, 255, 255)):
        self.color = color
        self.side_length = side_length
        self.box_body = utils.world.CreateDynamicBody(position=utils.from_Pos((pos.x, pos.y)))
        self.box_shape = self.box_body.CreatePolygonFixture(box=(self.side_length, self.side_length),
                                                            density=1, friction=0.0, restitution=1)
        self.box_body.linearVelocity = (random.uniform(-10, 10), random.uniform(-0, -0))
        self.box_body.userData = self
        self.box_body.angle = 0
        self.deathTime = 5

        self.trail = []  # List to store trail positions
        self.trail_length = 50  # Length of the trail
        self.headColor = color
        self.spawn = False

        self.box_body.angle = 0
        self.box_body.fixedRotation = True


    def draw(self):
        if self.deathTime > 0:
            self.deathTime -= utils.deltaTime()
            if self.deathTime <= 0:
                self.convert_to_static()
        if self.deathTime <= 0:
            self.headColor = self.color

        self.update_trail()
        self.draw_trail()
        for fixture in self.box_body.fixtures:
            self.draw_square(fixture.shape, self.box_body, fixture)

        if self.deathTime > 0:
            textSize = utils.font16.render(str(int(self.deathTime)), True, (0, 0, 0))
            utils.drawText(Vector2(self.getPos().x - textSize.get_width() / 2, self.getPos().y - textSize.get_height() / 2)
                           , str(int(self.deathTime)), (255, 255, 255), utils.font16)

    def draw_square(self, polygon, body, fixture):
        vertices = [utils.to_Pos(body.transform * v) for v in polygon.vertices]
        pygame.draw.polygon(utils.screen, (0,0,0), vertices)
        pygame.draw.polygon(utils.screen, self.headColor, vertices,4)

    def getPos(self):
        p = utils.to_Pos(self.box_body.position)
        return Vector2(p[0], p[1])

    def increase_side_length(self, side_length):
        self.side_length = side_length
        self.box_body.DestroyFixture(self.box_shape)
        self.box_shape = self.box_body.CreatePolygonFixture(box=(self.side_length, self.side_length), density=1, friction=0.0, restitution=1.05)
        # Optionally, update the userData if it depends on side_length
        self.box_body.userData = self

    def convert_to_static(self):
        if self.box_body is None:
            return

        # Get current properties
        pos = self.box_body.position
        angle = self.box_body.angle

        # Destroy the dynamic body
        utils.world.DestroyBody(self.box_body)
        # Create a new static body
        self.box_body = utils.world.CreateStaticBody(position=pos, angle=angle)
        self.box_shape = self.box_body.CreatePolygonFixture(box=(self.side_length, self.side_length), density=1,
                                                            friction=0.0, restitution=1.05)
        self.box_body.userData = self

    def update_trail(self):
        verticles = []
        for fixture in self.box_body.fixtures:
            v = [utils.to_Pos(self.box_body.transform * v) for v in fixture.shape.vertices]
        verticles.append(v)

        self.trail.append((verticles,self.color))

        # Limit the length of the trail
        if len(self.trail) > self.trail_length:
            self.trail.pop(0)

    def draw_trail(self):
        for verticles,color in self.trail:
            for v in verticles:
                pygame.draw.polygon(utils.screen, (0, 0, 0), v)
                pygame.draw.polygon(utils.screen, color, v, 2)