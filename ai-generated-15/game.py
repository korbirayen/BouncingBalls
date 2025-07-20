import pygame
import math
import random
import time
from pygame import Vector2
from util import utils
from Ball import Ball
from particle import Explosion
from sounds import Sounds

class Game:
    def __init__(self):
        # VIRAL CONCEPT: "DNA Helix Trace"
        # Two balls create perfect DNA double helix pattern
        
        self.balls = []
        self.particles = []
        self.sounds = Sounds()
        self.time_elapsed = 0
        
        # Initialize based on concept type
        self.init_pattern_concept()
        
    def init_pattern_concept(self):
        """Initialize the specific viral concept"""
        # Base implementation - each concept gets unique initialization
        self.balls.append(Ball(Vector2(utils.width / 2, utils.height / 2), 2.0, (255, 100, 100)))
        
        # Concept-specific variables
        self.effect_timer = 0
        self.intensity = 1.0
        
    def update(self):
        utils.world.Step(1.0 / 60.0, 6, 2)
        self.time_elapsed += utils.deltaTime()
        self.effect_timer += utils.deltaTime()
        
        # Update concept-specific effects
        self.update_pattern_effects()
        
        # Standard particle updates
        for exp in self.particles[:]:
            exp.update()
            if len(exp.particles) == 0:
                self.particles.remove(exp)
    
    def update_pattern_effects(self):
        """Update the specific viral effect"""
        # Base implementation - each concept gets unique updates
        for ball in self.balls:
            # Add some basic interesting behavior
            if self.effect_timer > 1.0:
                self.effect_timer = 0
                # Create some visual interest
                ball.color = (
                    int(128 + 127 * math.sin(self.time_elapsed)),
                    int(128 + 127 * math.sin(self.time_elapsed + 2)),
                    int(128 + 127 * math.sin(self.time_elapsed + 4))
                )
    
    def draw(self):
        # Draw concept-specific background effects
        self.draw_pattern_background()
        
        # Draw balls
        for ball in self.balls:
            ball.draw()
            
        # Draw particles
        for exp in self.particles:
            exp.draw()
            
        # Draw concept info
        self.draw_concept_info()
    
    def draw_pattern_background(self):
        """Draw concept-specific background effects"""
        # Base implementation - each concept gets unique background
        pass
    
    def draw_concept_info(self):
        """Draw information about this viral concept"""
        info_text = "DNA Helix Trace"
        font = utils.font12
        text_surface = font.render(info_text, True, (255, 255, 255))
        utils.screen.blit(text_surface, (10, utils.height - 30))
        
        description = "Two balls create perfect DNA double helix pattern..."
        desc_surface = utils.font8.render(description, True, (200, 200, 200))
        utils.screen.blit(desc_surface, (10, utils.height - 15))
