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
        # VIRAL CONCEPT: "Speed Acceleration Loop"
        # Ball gets 5% faster with each bounce until impossibly fast!
        
        self.balls = []
        self.particles = []
        self.sounds = Sounds()
        self.time_elapsed = 0
        
        # Speed acceleration specific variables
        self.base_ball = Ball(Vector2(utils.width / 2, utils.height / 2), 1.5, (255, 80, 80))
        self.base_ball.circle_body.linearVelocity = (random.uniform(-8, 8), random.uniform(-8, 8))
        self.balls.append(self.base_ball)
        
        # Acceleration tracking
        self.bounce_count = 0
        self.speed_multiplier = 1.0
        self.acceleration_rate = 1.05  # 5% increase per bounce
        self.max_speed = 50.0  # Cap to prevent infinite acceleration
        self.trail_points = []
        self.last_velocity = Vector2(0, 0)
        
    def update(self):
        utils.world.Step(1.0 / 60.0, 6, 2)
        self.time_elapsed += utils.deltaTime()
        
        # Track ball velocity to detect bounces
        ball = self.base_ball
        current_velocity = Vector2(ball.circle_body.linearVelocity[0], ball.circle_body.linearVelocity[1])
        
        # Detect bounce (velocity direction change)
        if len(self.trail_points) > 5:
            # Check for significant velocity change indicating bounce
            velocity_change = abs(current_velocity.length() - self.last_velocity.length())
            direction_change = current_velocity.dot(self.last_velocity) < 0
            
            if velocity_change > 2.0 or direction_change:
                self.bounce_count += 1
                self.speed_multiplier = min(self.acceleration_rate ** self.bounce_count, self.max_speed)
                
                # Apply speed boost
                new_velocity = current_velocity.normalize() * min(current_velocity.length() * self.acceleration_rate, self.max_speed)
                ball.circle_body.linearVelocity = (new_velocity.x, new_velocity.y)
                
                # Visual feedback on bounce
                self.create_bounce_effect(ball.circle_body.position)
                
                # Play accelerating sound
                self.sounds.play()
        
        self.last_velocity = current_velocity
        
        # Add trail point
        pos = Vector2(ball.circle_body.position[0] * utils.PPM, ball.circle_body.position[1] * utils.PPM)
        self.trail_points.append((pos.x, pos.y, time.time()))
        
        # Keep trail manageable
        if len(self.trail_points) > 100:
            self.trail_points.pop(0)
        
        # Update ball color based on speed
        speed = current_velocity.length()
        intensity = min(speed / 20.0, 1.0)
        ball.color = (
            int(255 * intensity),
            int(80 + 175 * (1 - intensity)),
            int(80 + 175 * (1 - intensity))
        )
        
        # Update particles
        for exp in self.particles[:]:
            exp.update()
            if len(exp.particles) == 0:
                self.particles.remove(exp)
    
    def create_bounce_effect(self, position):
        """Create visual effect when ball bounces and accelerates"""
        world_pos = Vector2(position[0] * utils.PPM, position[1] * utils.PPM)
        
        # Create explosion effect
        explosion = Explosion(world_pos, 15, (255, 200, 0), 1.0)
        self.particles.append(explosion)
        
        # Create speed lines
        for i in range(8):
            angle = i * (2 * math.pi / 8)
            speed_line = Explosion(
                world_pos + Vector2(math.cos(angle) * 20, math.sin(angle) * 20),
                3, (255, 255, 255), 0.5
            )
            self.particles.append(speed_line)
    
    def draw(self):
        # Draw speed trail
        self.draw_speed_trail()
        
        # Draw ball
        for ball in self.balls:
            ball.draw()
            
        # Draw particles
        for exp in self.particles:
            exp.draw()
            
        # Draw speed indicator and stats
        self.draw_speed_stats()
    
    def draw_speed_trail(self):
        """Draw the acceleration trail behind the ball"""
        if len(self.trail_points) < 2:
            return
            
        current_time = time.time()
        
        # Draw trail with fading effect
        for i in range(len(self.trail_points) - 1):
            x1, y1, t1 = self.trail_points[i]
            x2, y2, t2 = self.trail_points[i + 1]
            
            # Fade based on age
            age = current_time - t1
            alpha = max(0, 1.0 - age / 2.0)  # Fade over 2 seconds
            
            if alpha > 0:
                # Color based on speed
                speed = self.last_velocity.length()
                intensity = min(speed / 20.0, 1.0)
                
                color = (
                    int(255 * intensity * alpha),
                    int((100 + 155 * (1 - intensity)) * alpha),
                    int((100 + 155 * (1 - intensity)) * alpha)
                )
                
                # Draw trail segment
                if alpha > 0.1:
                    pygame.draw.line(utils.screen, color, (int(x1), int(y1)), (int(x2), int(y2)), 
                                   max(1, int(3 * alpha)))
    
    def draw_speed_stats(self):
        """Draw speed and bounce statistics"""
        # Speed indicator
        speed = self.last_velocity.length()
        speed_text = f"Speed: {speed:.1f}"
        font = utils.font12
        text_surface = font.render(speed_text, True, (255, 255, 255))
        utils.screen.blit(text_surface, (10, 10))
        
        # Bounce counter
        bounce_text = f"Bounces: {self.bounce_count}"
        bounce_surface = font.render(bounce_text, True, (255, 255, 255))
        utils.screen.blit(bounce_surface, (10, 30))
        
        # Speed multiplier
        multiplier_text = f"Speed x{self.speed_multiplier:.2f}"
        multiplier_surface = font.render(multiplier_text, True, (255, 200, 0))
        utils.screen.blit(multiplier_surface, (10, 50))
        
        # Concept title
        title_text = "SPEED ACCELERATION LOOP"
        title_surface = utils.font16.render(title_text, True, (255, 100, 100))
        utils.screen.blit(title_surface, (10, utils.height - 40))
        
        # Description
        description = "Ball gets 5% faster with each bounce!"
        desc_surface = utils.font8.render(description, True, (200, 200, 200))
        utils.screen.blit(desc_surface, (10, utils.height - 20))
