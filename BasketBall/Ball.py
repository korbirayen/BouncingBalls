import math
import random
import pygame
from pygame import Vector2
from util import utils

class Ball:
    def __init__(self, pos, radius=64/10, color=(255, 255, 255)):
        self.color = color
        self.radius = radius
        self.circle_body = utils.world.CreateDynamicBody(position=(utils.from_Pos((pos.x, pos.y))))
        self.circle_shape = self.circle_body.CreateCircleFixture(radius=self.radius, density=1, friction=0.0, restitution=1)
        self.circle_body.linearVelocity = (random.uniform(0, 0), random.uniform(-0, 0))
        self.circle_body.userData = self
        self.bounce_count = 0
        self.img = pygame.image.load("assets/bean.png")  # Start with kernel.png
        self.circle_body.angularVelocity = 1

    def draw(self):
        rotated_img = pygame.transform.rotate(self.img, -self.circle_body.angle * (180 / math.pi))  # Convert radians to degrees and rotate
        rect = rotated_img.get_rect(center=self.getPos())
        utils.screen.blit(rotated_img, rect.topleft)

    def draw_circle(self, circle, body, fixture):
        position = utils.to_Pos(body.transform * circle.pos)
        pygame.draw.circle(utils.screen, self.color, [int(x) for x in position], int(circle.radius * utils.PPM))

    def getPos(self):
        p = utils.to_Pos(self.circle_body.position)
        return Vector2(p[0], p[1])

    def bounce(self):
        self.bounce_count += 1
        if self.bounce_count >= 8:
            self.img = pygame.image.load("assets/bean.png")  # Change to popcorn.png after 5 bounces
