import random
import pygame
from pygame import Vector2
from util import utils

class Ball:
    def __init__(self, pos, radius, image_path, team='biden', rotation_speed=1.0):
        self.team = team  # Store the team name
        self.image_path = image_path
        self.original_image = pygame.image.load(image_path)
        self.original_image = pygame.transform.scale(self.original_image, (int(radius * 2.5 * utils.PPM), int(radius * 2.5 * utils.PPM)))
        self.image = self.original_image
        self.radius = radius
        self.rotation_speed = rotation_speed
        self.angle = 0  # Initial rotation angle
        self.circle_body = utils.world.CreateDynamicBody(position=(utils.from_Pos((pos.x, pos.y))))
        self.circle_shape = self.circle_body.CreateCircleFixture(radius=self.radius, density=1, friction=0.0, restitution=1)
        self.circle_body.linearVelocity = (random.uniform(-0, 0), random.uniform(0, 0))  # Random velocity
        self.circle_body.userData = self

    def update(self):
        # Update the angle for rotation
        self.angle = (self.angle + self.rotation_speed) % 360
        # Rotate the image
        self.image = pygame.transform.rotate(self.original_image, self.angle)

    def draw(self):
        self.update()  # Update rotation before drawing
        for fixture in self.circle_body.fixtures:
            self.draw_circle(fixture.shape, self.circle_body, fixture)

    def draw_circle(self, circle, body, fixture):
        position = utils.to_Pos(body.transform * circle.pos)
        pos = [int(x) for x in position]
        rect = self.image.get_rect(center=pos)
        utils.screen.blit(self.image, rect.topleft)

    def getPos(self):
        p = utils.to_Pos(self.circle_body.position)
        return Vector2(p[0], p[1])
