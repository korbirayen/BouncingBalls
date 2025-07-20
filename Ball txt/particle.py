import math
import random

import pygame

from util import utils


class Particle:
    def __init__(self, x, y,velX,velY, color):
        self.x = x
        self.y = y
        self.color = color
        self.radius = random.uniform(0.5, 2)
        angle = random.uniform(0,360)
        speed = random.uniform(1,2)
        # self.vel_x = math.cos(math.radians(angle)) * speed
        # self.vel_y = math.sin(math.radians(angle)) * speed
        self.vel_x = velX * speed
        self.vel_y = velY * speed
        self.life = random.randint(100, 500)


    def update(self):
        self.x += self.vel_x
        self.y += self.vel_y
        self.life -= 1

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

class Explosion:
    def __init__(self,x,y,color):
        # Create particles
        self.particles = []
        COLORS = [color]
        for i in range(360):
            t = math.radians(i)  # Convert degrees to radians

            # Heart parametric equation
            posX = 26 * (math.sin(t) ** 3)
            posY = 23 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t)

            # Scale and offset the heart shape to the given (x, y) position
            posX = posX
            posY = -posY
            color = random.choice(COLORS)

            # Create a particle at the heart's position
            velX = posX * 0.1
            velY = posY * 0.1
            particle = Particle(x, y, velX, velY,color)
            self.particles.append(particle)

    def update(self):
        for particle in self.particles:
            particle.update()
        self.particles = [particle for particle in self.particles if particle.life > 0]

    def draw(self,surface):
        for particle in self.particles:
            particle.draw(surface)
