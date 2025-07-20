import math
import random

import pygame.image
from pygame import Vector2

from BallProjectile import BallProjectile
from util import utils


class Cannon:
    def __init__(self,pos,color):
        self.pos = pos
        self.color = color
        self.angle = 0
        self.dir = 1
        self.speed = 0.5
        self.wheelImg = pygame.image.load("assets/wheel.png")
        self.cannonImg = pygame.image.load("assets/red_cannon.png")
        if self.color == 'green':
            self.angle = 0
            self.dir = 1
            self.cannonImg = pygame.image.load("assets/green_cannon.png")
        self.destroyFlag = False
        self.shootDelay = random.uniform(2,2)
        self.shootInterval = 0

        self.movingAngle = 0

    def update(self):
        self.movingAngle += 0.5
        if self.color == 'red':
            center = Vector2(utils.width/2,utils.height/2)
            x = math.cos(math.radians(self.movingAngle))
            y = math.sin(math.radians(self.movingAngle))
            pDir = Vector2(x,y)
            pos = center + pDir * (utils.width/2 - 20)
            self.pos = pos

            rDir = center - self.pos
            self.angle = math.degrees(math.atan2(rDir.y, rDir.x)) + 90


        else:
            if self.angle <= -90 and self.dir == -1:
                self.angle = -90
                self.dir = 1
            if self.angle >= 30 and self.dir == 1:
                self.angle = 30
                self.dir = -1

    def draw(self):
        if self.destroyFlag:
            return
        if self.color == 'red':
            rotated_image, rect = utils.rotate(self.cannonImg, self.angle, Vector2(self.pos.x,self.pos.y), Vector2(0, -20))
            utils.screen.blit(rotated_image, rect.topleft)
        else:
            rotated_image, rect = utils.rotate(self.cannonImg, self.angle, Vector2(self.pos.x + 12, self.pos.y + 10),
                                               Vector2(0, -20))
            utils.screen.blit(rotated_image, rect.topleft)

    def getProjectile(self):
        self.shootInterval += utils.deltaTime()
        if self.shootInterval < self.shootDelay:
            return
        self.shootDelay *= 0.95
        if self.shootDelay < 0.05:
            self.shootDelay = 0.05
        self.shootInterval = 0
        center = Vector2(self.pos.x ,self.pos.y)
        if self.color == 'green':
            center = Vector2(self.pos.x - 12, self.pos.y + 10)
        # Calculate the positionFromAngle based on the cannon's position and angle
        barrel_length = 50  # Adjust this length as needed
        radian_angle = (self.angle-90) * (3.14159265 / 180)  # Convert to radians
        positionFromAngle = Vector2(center.x + barrel_length * math.cos(radian_angle),
                                    center.y + barrel_length * math.sin(radian_angle))

        # Calculate the velocityFromAngle based on the angle
        projectile_speed = 3  # Adjust the speed as needed
        velocityFromAngle = Vector2(projectile_speed * math.cos(radian_angle),
                                    projectile_speed * math.sin(radian_angle))

        color = (255,255,255)
        # if self.color == 'green':
        #     color = (23,233,23)

        projectTile = BallProjectile(positionFromAngle,velocityFromAngle,10,color)
        return projectTile