import math
import random

import pygame
from pygame import Vector2

from util import utils


class Ball:
    def __init__(self, pos, radius=64/10, color=(255, 255, 255), vel=Vector2(0, 0)):
        self.color = color
        self.radius = radius
        self.circle_body = utils.world.CreateDynamicBody(position=(utils.from_Pos((pos.x, pos.y))))
        self.circle_shape = self.circle_body.CreateCircleFixture(radius=self.radius, density=1, friction=0.0, restitution=1.0)
        self.circle_body.linearVelocity = vel
        self.circle_body.userData = self
        self.circle_body.angularVelocity = 1
        
        # List of images to choose from
        self.images = [
            pygame.image.load("assets/crunch2.png"),
            pygame.image.load("assets/crunch2.png"),
            pygame.image.load("assets/crunch3.png"),
            pygame.image.load("assets/crunch4.png"),
            pygame.image.load("assets/crunch5.png"),
            pygame.image.load("assets/crunch6.png")
        ]
        
        # Randomly pick one of the images
        self.image = random.choice(self.images)
    
    def draw(self):
        velocity = self.circle_body.linearVelocity
        speed = velocity.length
        maxSpeed = 45
        if speed > maxSpeed:
            scale = maxSpeed / speed
            self.circle_body.linearVelocity = (velocity.x * scale, velocity.y * scale)
        
        # Rotate and draw the selected image
        rotated_img = pygame.transform.rotate(self.image, -self.circle_body.angle * (180 / math.pi))
        rect = rotated_img.get_rect(center=self.getPos())
        utils.screen.blit(rotated_img, rect.topleft)

    def getPos(self):
        p = utils.to_Pos(self.circle_body.position)
        return Vector2(p[0], p[1])
