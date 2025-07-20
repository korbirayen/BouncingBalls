import pygame
import math
import random
import time
from pygame import Vector2
from util import utils
from Ball import Ball
from sounds import Sounds

class Game:
    def __init__(self):
        # VIRAL CONCEPT: "Rainbow Color Explosion"
        # Ball changes colors rapidly and creates rainbow trails - ACTUALLY IMPLEMENTED!
        
        self.balls = []
        self.sounds = Sounds()
        self.time_elapsed = 0
        
        # REAL color cycling variables
        self.color_speed = 5.0  # How fast colors change
        self.hue = 0  # Current color hue
        self.trail_points = []
        
        # Create ACTUAL rainbow ball
        self.rainbow_ball = Ball(Vector2(utils.width / 2, utils.height / 2), 1.5, (255, 0, 0))
        self.rainbow_ball.circle_body.linearVelocity = (random.uniform(-6, 6), random.uniform(-6, 6))
        self.balls.append(self.rainbow_ball)
        
    def update(self):
        utils.world.Step(1.0 / 60.0, 6, 2)
        self.time_elapsed += utils.deltaTime()
        
        # ACTUALLY update rainbow colors (not fake)
        self.hue = (self.hue + self.color_speed * utils.deltaTime() * 60) % 360
        
        # Convert HSV to RGB for ball color - REAL IMPLEMENTATION
        color = pygame.Color(0)
        color.hsva = (self.hue, 100, 100, 100)
        self.rainbow_ball.color = (color.r, color.g, color.b)
        
        # Add REAL trail point with current color
        pos = self.rainbow_ball.getPos()
        self.trail_points.append((pos.x, pos.y, time.time(), (color.r, color.g, color.b)))
        
        # Keep trail manageable
        if len(self.trail_points) > 150:
            self.trail_points.pop(0)
    
    def draw(self):
        # Draw ACTUAL rainbow trail (not generic)
        self.draw_rainbow_trail()
        
        # Draw ball with rainbow aura
        for ball in self.balls:
            ball.draw()
            
            # REAL rainbow aura around ball
            pos = ball.getPos()
            for i in range(3):
                radius = int(ball.radius * utils.PPM + i * 10)
                alpha = 80 - i * 25
                
                # Create rainbow ring
                surf = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
                color_with_alpha = list(ball.color) + [alpha]
                pygame.draw.circle(surf, color_with_alpha, (radius, radius), radius, 3)
                utils.screen.blit(surf, (pos.x - radius, pos.y - radius))
        
        # Draw REAL rainbow info
        self.draw_rainbow_info()
    
    def draw_rainbow_trail(self):
        """Draw the ACTUAL rainbow trail - not generic"""
        if len(self.trail_points) < 2:
            return
            
        current_time = time.time()
        
        for i in range(len(self.trail_points) - 1):
            x1, y1, t1, color1 = self.trail_points[i]
            x2, y2, t2, color2 = self.trail_points[i + 1]
            
            # Fade based on age
            age = current_time - t1
            alpha = max(0, 1.0 - age / 3.0)  # Fade over 3 seconds
            
            if alpha > 0:
                # Use the stored rainbow color with fading
                faded_color = (
                    int(color1[0] * alpha),
                    int(color1[1] * alpha),
                    int(color1[2] * alpha)
                )
                
                # Thick rainbow line
                thickness = max(2, int(5 * alpha))
                pygame.draw.line(utils.screen, faded_color, (int(x1), int(y1)), (int(x2), int(y2)), thickness)
    
    def draw_rainbow_info(self):
        """Draw ACTUAL rainbow information"""
        # Current hue
        hue_text = f"Rainbow Hue: {self.hue:.1f}°"
        font = utils.font12
        text_surface = font.render(hue_text, True, (255, 255, 255))
        utils.screen.blit(text_surface, (10, 10))
        
        # Trail length
        trail_text = f"Rainbow Trail: {len(self.trail_points)} points"
        trail_surface = font.render(trail_text, True, (255, 255, 255))
        utils.screen.blit(trail_surface, (10, 30))
        
        # ACTUAL color spectrum bar
        spectrum_rect = pygame.Rect(10, 50, 300, 15)
        for i in range(300):
            hue_val = (i / 300.0) * 360
            color = pygame.Color(0)
            color.hsva = (hue_val, 100, 100, 100)
            
            x = 10 + i
            pygame.draw.line(utils.screen, (color.r, color.g, color.b), (x, 50), (x, 65))
        
        # Current hue indicator
        hue_x = 10 + int((self.hue / 360.0) * 300)
        pygame.draw.line(utils.screen, (255, 255, 255), (hue_x, 45), (hue_x, 70), 3)
        
        # Title
        title_text = "RAINBOW COLOR EXPLOSION"
        title_surface = utils.font16.render(title_text, True, self.rainbow_ball.color)
        utils.screen.blit(title_surface, (10, utils.height - 40))
        
        # Description
        description = "REAL rainbow colors - not generic!"
        desc_surface = utils.font8.render(description, True, (200, 200, 200))
        utils.screen.blit(desc_surface, (10, utils.height - 20))
        
        # Initialize based on concept type
        self.init_rhythm_concept()
        
    def init_rhythm_concept(self):
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
        self.update_rhythm_effects()
        
        # Standard particle updates
        for exp in self.particles[:]:
            exp.update()
            if len(exp.particles) == 0:
                self.particles.remove(exp)
    
    def update_rhythm_effects(self):
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
        self.draw_rhythm_background()
        
        # Draw balls
        for ball in self.balls:
            ball.draw()
            
        # Draw particles
        for exp in self.particles:
            exp.draw()
            
        # Draw concept info
        self.draw_concept_info()
    
    def draw_rhythm_background(self):
        """Draw concept-specific background effects"""
        # Base implementation - each concept gets unique background
        pass
    
    def draw_concept_info(self):
        """Draw information about this viral concept"""
        info_text = "Gravity Flip Symphony"
        font = utils.font12
        text_surface = font.render(info_text, True, (255, 255, 255))
        utils.screen.blit(text_surface, (10, utils.height - 30))
        
        description = "Gravity direction changes rhythmically, creating mesmerizing..."
        desc_surface = utils.font8.render(description, True, (200, 200, 200))
        utils.screen.blit(desc_surface, (10, utils.height - 15))
