import math
import random

import pygame
from pygame import Vector2

from util import utils


import math
import random

import pygame
from pygame import Vector2

from util import utils
from Box2D import b2Filter



class Ball:
    def __init__(self, pos, img, radius=64/10, initial=False):
        self.radius = radius
        self.circle_body = utils.world.CreateDynamicBody(position=(utils.from_Pos((pos.x, pos.y))))
        
        # Create a collision filter that makes balls not collide with each other
        self.filter = b2Filter(categoryBits=0x0002, maskBits=0xFFFF ^ 0x0002)
        
        self.circle_shape = self.circle_body.CreateCircleFixture(
            radius=self.radius,
            density=1,
            friction=0.0,
            restitution=0.9,
            filter=self.filter  # Assign the filter here
        )
        
        # Set velocity for the first ball (initial=True) to (0, 0), otherwise random horizontal velocity
        if initial:
            self.circle_body.linearVelocity = Vector2(0, 0)
        else:
            self.circle_body.linearVelocity = Vector2(random.uniform(-11, 11), -0)
        
        self.circle_body.userData = self
        self.oImg = img
        self.img = pygame.transform.scale(self.oImg, (self.radius * 24, self.radius * 24))
        self.circle_body.angularVelocity = 1
        self.destroyFlag = False



    def draw(self):
        velocity = self.circle_body.linearVelocity
        speed = velocity.length
        maxSpeed = 45
        if speed > maxSpeed:
            scale = maxSpeed / speed
            self.circle_body.linearVelocity = (velocity.x * scale, velocity.y * scale)

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
