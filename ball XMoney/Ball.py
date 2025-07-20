import math
import random

import pygame
from pygame import Vector2

from util import utils


class Ball:
    def __init__(self, imgStr, pos, radius=64/10, color=(255, 255, 255), vel=None):
        self.color = color
        self.radius = radius
        # Set a random horizontal velocity between -4 and 4, and vertical velocity to 0
        if vel is None:
            vel = Vector2(random.uniform(-3, 3), 0)
        self.circle_body = utils.world.CreateDynamicBody(position=(utils.from_Pos((pos.x, pos.y))))
        self.circle_shape = self.circle_body.CreateCircleFixture(radius=self.radius, density=1, friction=0.0, restitution=random.uniform(0.1, 0.4))
        self.circle_body.linearVelocity = vel
        self.circle_body.userData = self
        self.oImg = pygame.image.load(imgStr)
        self.img = pygame.transform.scale(self.oImg, (radius * 10 * 2, radius * 10 * 2))

        self.circle_body.angularVelocity = 1

    def draw(self):
        velocity = self.circle_body.linearVelocity
        speed = velocity.length
        maxSpeed = 45
        if speed > maxSpeed:
            scale = maxSpeed / speed
            self.circle_body.linearVelocity = (velocity.x * scale, velocity.y * scale)

        pygame.draw.circle(utils.screen, self.color, self.getPos(), int(self.radius * utils.PPM))

    def draw_circle(self, circle, body, fixture):
        position = utils.to_Pos(body.transform * circle.pos)
        pygame.draw.circle(utils.screen, self.color, [int(x) for x in position], int(circle.radius * utils.PPM))

    def getPos(self):
        p = utils.to_Pos(self.circle_body.position)
        return Vector2(p[0], p[1])

    def getRect(self):
        return pygame.Rect(self.getPos().x - self.radius * 10, self.getPos().y - self.radius * 10, self.radius * 10 * 2, self.radius * 10 * 2)

    def change_radius(self, new_radius):
        # Remove the existing circle fixture
        self.circle_body.DestroyFixture(self.circle_shape)
        # Update the radius
        self.radius = new_radius

        # Create a new circle fixture with the updated radius
        self.circle_shape = self.circle_body.CreateCircleFixture(radius=self.radius, density=1, friction=0.0, restitution=1.0)
        # Scale the image to the new size
        self.img = pygame.transform.scale(self.oImg, (int(self.radius * 10 * 2), int(self.radius * 10 * 2)))
