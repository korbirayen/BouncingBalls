import random

import pygame

from util import utils


class Particle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.radius = random.uniform(0.5, 2)
        self.vel_x = random.uniform(-2, 2)
        self.vel_y = random.uniform(-2, 2)
        self.life = random.randint(5, 40)

    def update(self):
        self.x += self.vel_x
        self.y += self.vel_y
        self.life -= 1

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

class Explosion:
    def __init__(self,x,y):
        # Create particles
        self.particles = []
        COLORS = [(255,255,255)]
        for _ in range(10):
            color = random.choice(COLORS)
            particle = Particle(x,y, color)
            self.particles.append(particle)

    def update(self):
        for particle in self.particles:
            particle.update()
        self.particles = [particle for particle in self.particles if particle.life > 0]

    def draw(self):
        for particle in self.particles:
            particle.draw(utils.screen)
