import pygame.draw
from pygame import Vector2

from util import utils


class BallProjectile:
    def __init__(self,pos,vel,radius,color):
        self.pos = pos
        self.radius = radius
        self.color = color
        self.vel = vel
        self.destroyFlag = False

        self.trail = []  # List to store previous positions
        self.trail_length = 20  # Number of previous positions to store


    def update(self):
        self.pos += self.vel

        if self.pos.x < -200 or self.pos.x > utils.width + 200 or self.pos.y < -200 or self.pos.y > utils.height + 200:
            self.destroyFlag = True

        self.trail.append(Vector2(self.pos))
        # Limit the trail length
        if len(self.trail) > self.trail_length:
            self.trail.pop(0)

    def draw(self):
        if self.destroyFlag:
            return
        # Draw the trail
        trailColor = self.color
        for i, trail_pos in enumerate(self.trail):
            # Create a surface with per-pixel alpha
            alpha = int(255 * (i / len(self.trail)))
            if alpha < 0:
                alpha = 0
            if alpha > 255:
                alpha = 255
            trail_surface = pygame.Surface((self.radius, self.radius), pygame.SRCALPHA)
            trail_color = (trailColor[0], trailColor[1],trailColor[2], alpha)
            # Draw the circle onto the trail surface
            pygame.draw.circle(trail_surface, trail_color, (self.radius // 2, self.radius // 2), self.radius // 2)
            # Blit the trail surface onto the main screen
            utils.screen.blit(trail_surface, (trail_pos.x - self.radius // 2, trail_pos.y - self.radius // 2))

        # Draw the ball

        pygame.draw.circle(utils.screen,self.color,self.pos,self.radius)

    def getRect(self):
        return pygame.Rect(self.pos.x-self.radius,self.pos.y - self.radius,self.radius*2,self.radius*2)