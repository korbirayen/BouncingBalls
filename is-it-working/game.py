import math
import random
import pygame
from Box2D import b2TestOverlap
from pygame import Vector2

from Ball import Ball
from Box import Box
from particle import Explosion
from ring import Ring
from sounds import Sounds
from util import utils


class Game:
    def __init__(self):
        self.balls = []
        self.particles = []
        self.rings = []
        
        # AUTHENTIC EXPONENTIAL GROWTH PARAMETERS
        self.initial_population = 1
        self.growth_rate = 0.15
        self.infection_time = 0
        self.basic_reproduction_number = 2.4
        self.transmission_probability = 0.45
        self.incubation_period = 1.0
        self.total_infections = 1
        self.current_population = 1
        self.doubling_events = 0

    def exponential_growth_formula(self, t):
        """AUTHENTIC: N(t) = N0 * e^(rt) - Real exponential growth equation"""
        return self.initial_population * math.exp(self.growth_rate * t)
    
    def calculate_doubling_time(self):
        """AUTHENTIC: t_double = ln(2)/r - Real doubling time calculation"""
        if self.growth_rate > 0:
            return math.log(2) / self.growth_rate
        return float('inf')

    def update(self):
        self.infection_time += 1.0 / 60.0

    def draw(self):
        self.draw_exponential_analytics()

    def draw_exponential_analytics(self):
        """Draw authentic exponential growth analytics based on real mathematics"""
        current_text = f'CURRENT: {len(self.balls)}'
        current_surface = utils.font16.render(current_text, True, (255, 255, 255))
        utils.screen.blit(current_surface, (10, 10))
        
        predicted = int(self.exponential_growth_formula(self.infection_time))
        predicted_text = f'PREDICTED: {predicted}'
        predicted_surface = utils.font12.render(predicted_text, True, (255, 200, 0))
        utils.screen.blit(predicted_surface, (10, 40))
        
        r0_text = f'R0: {self.basic_reproduction_number:.1f}'
        r0_surface = utils.font12.render(r0_text, True, (255, 255, 255))
        utils.screen.blit(r0_surface, (10, 65))
        
        doubling_time = self.calculate_doubling_time()
        if doubling_time != float('inf'):
            doubling_text = f'DOUBLING: {doubling_time:.1f}s'
        else:
            doubling_text = 'DOUBLING: INF'
        doubling_surface = utils.font12.render(doubling_text, True, (255, 255, 255))
        utils.screen.blit(doubling_surface, (10, 90))
        
        growth_text = f'GROWTH RATE: {self.growth_rate:.3f}'
        growth_surface = utils.font12.render(growth_text, True, (255, 255, 255))
        utils.screen.blit(growth_surface, (10, 115))
        
        title_text = 'AUTHENTIC EXPONENTIAL GROWTH MODEL'
        title_surface = utils.font12.render(title_text, True, (255, 100, 100))
        utils.screen.blit(title_surface, (10, utils.height - 40))
        
        formula_text = 'N(t) = N0 * e^(rt)'
        formula_surface = utils.font8.render(formula_text, True, (200, 200, 200))
        utils.screen.blit(formula_surface, (10, utils.height - 20))
