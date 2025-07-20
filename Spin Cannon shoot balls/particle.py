import math
import random

import pygame

from util import utils


class Particle:
    def __init__(self, x, y, vel_x,vel_y,radius,color,life):
        self.x = x
        self.y = y
        self.vel_x = vel_x
        self.vel_y = vel_y
        self.radius = radius
        self.color = color
        self.life = life
        # self.color = color
        # self.radius = random.uniform(2,5)
        # self.vel_x = random.uniform(-2, 2)
        # self.vel_y = random.uniform(-2, 2)
        # self.life = random.randint(5, 40)

    def update(self):
        self.x += self.vel_x
        self.y += self.vel_y
        self.life -= utils.deltaTime()

    def draw(self):
        pygame.draw.circle(utils.screen, self.color, (int(self.x), int(self.y)), self.radius)


class Explosion:
    def __init__(self,x,y,color):
        # Create particles
        self.particles = []
        COLORS = [color]
        self.destroyFlag = False
        for _ in range(10):
            color = random.choice(COLORS)
            particle = Particle(x,y,random.uniform(-2, 2),random.uniform(-2, 2),random.uniform(2,5), color,random.uniform(0.1, 0.3))
            self.particles.append(particle)

    def update(self):
        for particle in self.particles:
            particle.update()
        self.particles = [particle for particle in self.particles if particle.life > 0]
        if len(self.particles) <= 0:
            self.destroyFlag = True

    def draw(self):
        for particle in self.particles:
            particle.draw()




class HeartExplosion:
    def __init__(self,x,y,color):
        # Create particles
        self.particles = []
        COLORS = [color]
        self.destroyFlag = False

        i = 0
        while i <= 6.28:
            color = random.choice(COLORS)
            t = random.uniform(0, 2 * math.pi)
            velX = 1 * math.pow(math.cos(i), 3)
            velY = 1 * math.pow(math.sin(i), 3)
            particle = Particle(x,y,velX,velY,random.uniform(2,5), color,random.uniform(0.5, 1.0))
            self.particles.append(particle)
            i += 0.2

        # for _ in range(10):
        #     color = random.choice(COLORS)
        #     t = random.uniform(0, 2 * math.pi)
        #     velX = 16 * (math.sin(t) ** 3)
        #     velY = 13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t)
        #     particle = Particle(x,y,velX,velY,random.uniform(2,5), color,random.randint(5, 40))
        #     self.particles.append(particle)

    def update(self):
        for particle in self.particles:
            particle.update()
        self.particles = [particle for particle in self.particles if particle.life > 0]
        if len(self.particles) <= 0:
            self.destroyFlag = True

    def draw(self):
        for particle in self.particles:
            particle.draw()

