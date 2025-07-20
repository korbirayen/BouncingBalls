import math
import random

import pygame
from Box2D import b2Filter
from pygame import Vector2

from util import utils, BALL, PIECE


class Ball:
    def __init__(self,imgStr,pos,radius = 64/10,color = (255,255,255),vel = Vector2(random.uniform(0,0),0)):
        self.color = color
        self.radius = radius
        self.circle_body = utils.world.CreateDynamicBody(position=(utils.from_Pos((pos.x, pos.y))))
        self.circle_shape = self.circle_body.CreateCircleFixture(radius=self.radius, density=0.5, friction=0.0, restitution=1,
                                                                 filter=b2Filter(categoryBits=BALL, maskBits=PIECE))
        self.circle_body.linearVelocity = vel
        self.circle_body.userData = self

        self.circle_body.angularVelocity = 1
        self.circle_body.linearVelocity = (0,0)
        self.velocity = Vector2(0,0)

        self.setMinSpeed = False
        self.minSpeedTime = 0

    def draw(self):
        text = "Time: " + str(round(self.minSpeedTime,1))
        tw, th = utils.font24.render(text, True, (233, 233, 233)).get_size()
        utils.drawText(Vector2(utils.width / 2 - tw / 2, 600), text, (0, 0, 0), utils.font24)

        velocity = self.circle_body.linearVelocity
        speed = velocity.length
        self.circle_body.linearVelocity *= 1.0035
        self.minSpeedTime += utils.deltaTime()
        if self.minSpeedTime > 40:
            self.setMinSpeed = True

        if self.setMinSpeed: # after 45 second , min speed is 45
            minSpeed = 45
            if speed < minSpeed:
                scale = minSpeed / speed
                self.circle_body.linearVelocity = (velocity.x * scale, velocity.y * scale)

        pygame.draw.circle(utils.screen,self.color,self.getPos(),self.radius * 10)

    def draw_circle(self,circle, body, fixture):
        position = utils.to_Pos(body.transform * circle.pos)
        pygame.draw.circle(utils.screen, self.color, [int(x) for x in position], int(circle.radius * utils.PPM))

    def getPos(self):
        p = utils.to_Pos(self.circle_body.position)
        return Vector2(p[0],p[1])

    def getRect(self):
        return pygame.Rect(self.getPos().x - self.radius*10,self.getPos().y - self.radius*10,self.radius*10 * 2,self.radius*10 * 2)

    def change_radius(self, new_radius):
        # Remove the existing circle fixture
        self.circle_body.DestroyFixture(self.circle_shape)
        # Update the radius
        self.radius = new_radius

        # Create a new circle fixture with the updated radius
        self.circle_shape = self.circle_body.CreateCircleFixture(radius=self.radius, density=1, friction=0.0,
                                                                 restitution=1.0)
        # Scale the image to the new size
        self.img = pygame.transform.scale(self.oImg, (int(self.radius * 10 * 2), int(self.radius * 10 * 2)))