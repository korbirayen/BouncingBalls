import math
import random

import pygame
from pygame import Vector2

from util import utils


class Ball:
    def __init__(self,pos,radius = 64/10,color = (255,255,255),vel = Vector2(-5,35)):
        self.color = color
        self.radius = radius
        self.circle_body = utils.world.CreateDynamicBody(position=(utils.from_Pos((pos.x, pos.y))))
        self.circle_shape = self.circle_body.CreateCircleFixture(radius=self.radius, density=1, friction=0.0, restitution=1.0)
        self.circle_body.linearVelocity = vel
        self.circle_body.userData = self
        self.img = pygame.image.load("assets/golfball.png")
        self.circle_body.angularVelocity = 1

    def draw(self):
        velocity = self.circle_body.linearVelocity
        speed = velocity.length
        maxSpeed = 45
        if speed > maxSpeed:
            scale = maxSpeed / speed
            self.circle_body.linearVelocity = (velocity.x * scale, velocity.y * scale)

        # for fixture in self.circle_body.fixtures:
        #     self.draw_circle(fixture.shape, self.circle_body, fixture)
        # img,rect = utils.rotate(self.img,self.circle_body.angle,(0,0),Vector2(0,0))
        # rotated_img = pygame.transform.rotate(self.img, -self.circle_body.angle * (
        #             180 / math.pi))  # Convert radians to degrees and rotate
        # rect = rotated_img.get_rect(center=self.getPos())
        # utils.screen.blit(img,(self.getPos().x - 24,self.getPos().y-24))
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