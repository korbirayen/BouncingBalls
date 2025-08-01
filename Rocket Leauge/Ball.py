import math
import random

import pygame
from Box2D import b2Filter
from pygame import Vector2

from util import utils, CATEGORY_BALL, CATEGORY_CAR, CATEGORY_BALL_BOX


class Ball:
    def __init__(self,pos,radius = 64/10,color = (255,255,255),vel = Vector2(0,-5)):
        self.color = color
        self.radius = radius
        self.circle_body = utils.world.CreateDynamicBody(position=(utils.from_Pos((pos.x, pos.y))))
        self.circle_shape = self.circle_body.CreateCircleFixture(radius=self.radius, density=1, friction=0.0, restitution=.99,
                                                                 filter=b2Filter(categoryBits=CATEGORY_BALL, maskBits=(CATEGORY_CAR | CATEGORY_BALL_BOX)))
        self.circle_body.linearVelocity = vel
        self.circle_body.userData = self
        self.oImg = pygame.image.load("assets/cue.png")
        self.img = pygame.transform.scale(self.oImg,(self.radius*10*2,self.radius*10*2))
        self.circle_body.angularVelocity = 1
        # self.circle_body.gravityScale = 2
        self.circle_body.linearVelocity = (random.uniform(-0, 0), random.uniform(-0, -10))

    def draw(self):
        rotated_img = pygame.transform.rotate(self.img, -self.circle_body.angle * (
                    180 / math.pi))  # Convert radians to degrees and rotate
        rect = rotated_img.get_rect(center=self.getPos())
        utils.screen.blit(rotated_img, rect.topleft)

    def draw_circle(self,circle, body, fixture):
        position = utils.to_Pos(body.transform * circle.pos)
        pygame.draw.circle(utils.screen, self.color, [int(x) for x in position], int(circle.radius * utils.PPM))

    def getPos(self):
        p = utils.to_Pos(self.circle_body.position)
        return Vector2(p[0],p[1])

    def getRect(self):
        return pygame.Rect(self.getPos().x - self.radius*10,self.getPos().y - self.radius*10,self.radius*10 * 2,self.radius*10 * 2)