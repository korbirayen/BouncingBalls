import math
import random
import pygame
from Box2D import b2Filter
from pygame import Vector2
from util import utils


class Ball:
    def __init__(self, pos, radius, color, vel=Vector2(0, 0)):
        self.color = color
        self.radius = radius
        self.circle_body = utils.world.CreateDynamicBody(position=(utils.from_Pos((pos.x, pos.y))))
        self.circle_shape = self.circle_body.CreateCircleFixture(radius=self.radius, density=1, friction=0.0, restitution=1.0)
        self.circle_body.linearVelocity = vel
        self.circle_body.userData = self
        self.destroyFlag = False
        self.trail = []
        self.trail_length = 0  # Set trail length
        self.isPlaySound = False

        # Setting up collision filtering so balls can collide with each other
        self.circle_shape.filter = b2Filter(categoryBits=0x0002, maskBits=0x0002)

        # Load the image
        self.original_image = pygame.image.load('cat.png').convert_alpha()
        self.image = pygame.transform.scale(self.original_image, (int(self.radius * 2.5 * utils.PPM), int(self.radius * 2.5 * utils.PPM)))

        # Rotation-related attributes
        self.angle = 0
        self.angular_velocity = 0

    def update(self):
        # Update the ball's trail
        self.trail.append(Vector2(self.getPos()))
        if len(self.trail) > self.trail_length:
            self.trail.pop(0)

        # Update the angle based on the ball's velocity
        linear_velocity = self.circle_body.linearVelocity
        self.angular_velocity = (linear_velocity.length / self.radius) * .1  # Adjust the multiplier for desired rotation speed
  # Adjust the multiplier for desired rotation speed
        self.angle = (self.angle + self.angular_velocity) % 360

    def shrink(self):
        """Shrinks the ball's radius by 1% each time it's called."""
        self.radius *= 1 # Reduce the radius by 1%

        # Destroy the current circle shape and create a new one with the updated radius
        self.circle_body.DestroyFixture(self.circle_shape)
        self.circle_shape = self.circle_body.CreateCircleFixture(radius=self.radius, density=1, friction=0.0, restitution=1.0)

        # Resize the image according to the new radius
        self.image = pygame.transform.scale(self.original_image, (int(self.radius * 2.5 * utils.PPM), int(self.radius * 2.5 * utils.PPM)))

    def draw(self):
        # Draw the trail
        if len(self.trail) > 0:
            radius = self.radius
            for pos in self.trail:
                surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
                pygame.draw.circle(surface, (255, 255, 255), (radius, radius), radius, 4)
                utils.screen.blit(surface, (pos.x - radius, pos.y - radius))
                radius *= 1.05

        # Rotate the image based on the current angle
        rotated_image = pygame.transform.rotate(self.image, self.angle)
        rect = rotated_image.get_rect(center=self.getPos())

        # Draw the rotated ball image
        utils.screen.blit(rotated_image, rect.topleft)

    def draw_circle(self, circle, body, fixture):
        # This method is now unnecessary, as we're drawing the image instead of a circle
        pass

    def getPos(self):
        p = utils.to_Pos(self.circle_body.position)
        return Vector2(p[0], p[1])
