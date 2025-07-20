import pygame
import random
import math
from util import utils

class Particle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.vx = random.uniform(-5, 5)
        self.vy = random.uniform(-5, 5)
        self.life = 255
        self.color = color
        
    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.2  # gravity
        self.life -= 3
        
    def draw(self):
        if self.life > 0:
            alpha = max(0, self.life)
            color = (*self.color[:3], alpha)
            try:
                pygame.draw.circle(utils.screen, self.color[:3], (int(self.x), int(self.y)), 2)
            except:
                pass

class Explosion:
    def __init__(self, x, y, color1=(255, 255, 255), color2=(255, 255, 255)):
        self.particles = []
        for i in range(10):
            color = color1 if i % 2 == 0 else color2
            self.particles.append(Particle(x, y, color))
    
    def update(self):
        for particle in self.particles[:]:
            particle.update()
            if particle.life <= 0:
                self.particles.remove(particle)
    
    def draw(self):
        for particle in self.particles:
            particle.draw()
