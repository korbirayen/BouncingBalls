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
        # VIRAL CONCEPT: "Infinite Ball Split"
        # Every collision splits ball into 2 smaller ones - exponential growth!
        
        self.balls = []
        self.particles = []
        self.sounds = Sounds()
        self.time_elapsed = 0
        
        # Split system variables
        self.split_count = 0
        self.min_ball_size = 0.3  # Minimum size before no more splits
        self.max_balls = 150  # Prevent infinite splitting
        self.split_cooldown = {}  # Prevent rapid splitting
        
        # Create initial ball
        initial_ball = Ball(Vector2(utils.width / 2, utils.height / 2), 2.0, (255, 100, 255))
        initial_ball.circle_body.linearVelocity = (random.uniform(-5, 5), random.uniform(-5, 5))
        initial_ball.generation = 0  # Track split generation
        self.balls.append(initial_ball)
        
        # Track collisions for splitting
        self.collision_detection_timer = 0
        
    def update(self):
        utils.world.Step(1.0 / 60.0, 6, 2)
        self.time_elapsed += utils.deltaTime()
        self.collision_detection_timer += utils.deltaTime()
        
        # Check for collisions and split balls
        if self.collision_detection_timer > 0.1:  # Check every 0.1 seconds
            self.check_for_splits()
            self.collision_detection_timer = 0
        
        # Update split cooldowns
        current_time = time.time()
        for ball_id in list(self.split_cooldown.keys()):
            if current_time - self.split_cooldown[ball_id] > 1.0:
                del self.split_cooldown[ball_id]
        
        # Update ball colors based on generation
        for ball in self.balls:
            generation = getattr(ball, 'generation', 0)
            # Color shifts with each generation
            hue = (generation * 60) % 360
            color = pygame.Color(0)
            color.hsva = (hue, 80, 100, 100)
            ball.color = (color.r, color.g, color.b)
        
        # Update particles
        for exp in self.particles[:]:
            exp.update()
            if len(exp.particles) == 0:
                self.particles.remove(exp)
    
    def check_for_splits(self):
        """Check for balls that should split due to collisions"""
        if len(self.balls) >= self.max_balls:
            return
            
        balls_to_split = []
        
        for i, ball in enumerate(self.balls):
            # Check if ball is moving fast enough and not in cooldown
            velocity = Vector2(ball.circle_body.linearVelocity[0], ball.circle_body.linearVelocity[1])
            ball_id = id(ball)
            
            # Split conditions
            should_split = (
                velocity.length() > 3.0 and  # Moving fast enough
                ball.radius > self.min_ball_size and  # Big enough to split
                ball_id not in self.split_cooldown and  # Not in cooldown
                random.random() < 0.15  # 15% chance per check
            )
            
            if should_split:
                balls_to_split.append(ball)
                self.split_cooldown[ball_id] = time.time()
        
        # Perform splits
        for ball in balls_to_split:
            self.split_ball(ball)
    
    def split_ball(self, original_ball):
        """Split a ball into two smaller balls"""
        if len(self.balls) >= self.max_balls:
            return
            
        # Remove original ball
        self.balls.remove(original_ball)
        utils.world.DestroyBody(original_ball.circle_body)
        
        # Calculate new properties
        new_radius = original_ball.radius * 0.8  # Smaller than original
        original_velocity = Vector2(original_ball.circle_body.linearVelocity[0], original_ball.circle_body.linearVelocity[1])
        position = Vector2(original_ball.circle_body.position[0] * utils.PPM, original_ball.circle_body.position[1] * utils.PPM)
        generation = getattr(original_ball, 'generation', 0) + 1
        
        # Create two new balls moving in different directions
        for i in range(2):
            # Calculate split direction
            angle = random.uniform(0, 2 * math.pi)
            offset = Vector2(math.cos(angle) * 20, math.sin(angle) * 20)
            new_position = position + offset
            
            # Keep in bounds
            new_position.x = max(new_radius, min(utils.width - new_radius, new_position.x))
            new_position.y = max(new_radius, min(utils.height - new_radius, new_position.y))
            
            # Create new ball
            new_ball = Ball(new_position, new_radius, original_ball.color)
            new_ball.generation = generation
            
            # Set velocity (split in different directions)
            split_angle = angle + (i * math.pi + random.uniform(-0.5, 0.5))
            speed = original_velocity.length() * random.uniform(0.8, 1.2)
            new_velocity = Vector2(math.cos(split_angle) * speed, math.sin(split_angle) * speed)
            new_ball.circle_body.linearVelocity = (new_velocity.x, new_velocity.y)
            
            self.balls.append(new_ball)
        
        # Create split effect
        self.create_split_effect(position, generation)
        self.split_count += 1
        
        # Play sound
        self.sounds.play()
    
    def create_split_effect(self, position, generation):
        """Create visual effect when ball splits"""
        # Main explosion
        explosion = Explosion(position, 20, (255, 200, 100), 1.5)
        self.particles.append(explosion)
        
        # Generation-based color particles
        hue = (generation * 60) % 360
        color = pygame.Color(0)
        color.hsva = (hue, 100, 100, 100)
        
        # Split particles
        for i in range(12):
            angle = i * (2 * math.pi / 12)
            particle_pos = position + Vector2(math.cos(angle) * 15, math.sin(angle) * 15)
            particle_explosion = Explosion(particle_pos, 5, (color.r, color.g, color.b), 1.0)
            self.particles.append(particle_explosion)
    
    def draw(self):
        # Draw generation indicators
        self.draw_generation_background()
        
        # Draw balls
        for ball in self.balls:
            ball.draw()
            
            # Draw generation number on ball
            if hasattr(ball, 'generation') and ball.generation > 0:
                pos = Vector2(ball.circle_body.position[0] * utils.PPM, ball.circle_body.position[1] * utils.PPM)
                text = str(ball.generation)
                text_surface = utils.font8.render(text, True, (255, 255, 255))
                text_rect = text_surface.get_rect(center=(int(pos.x), int(pos.y)))
                utils.screen.blit(text_surface, text_rect)
            
        # Draw particles
        for exp in self.particles:
            exp.draw()
            
        # Draw stats
        self.draw_split_stats()
    
    def draw_generation_background(self):
        """Draw background effects based on current generations"""
        if not self.balls:
            return
            
        max_generation = max(getattr(ball, 'generation', 0) for ball in self.balls)
        
        # Draw generation waves
        for gen in range(max_generation + 1):
            hue = (gen * 60) % 360
            color = pygame.Color(0)
            color.hsva = (hue, 30, 20, 100)
            
            radius = 50 + gen * 30
            center = (utils.width // 2, utils.height // 2)
            
            # Pulsing effect
            pulse = math.sin(self.time_elapsed * 2 + gen * 0.5) * 0.2 + 1.0
            current_radius = int(radius * pulse)
            
            if current_radius > 0:
                pygame.draw.circle(utils.screen, (color.r, color.g, color.b), center, current_radius, 1)
    
    def draw_split_stats(self):
        """Draw split statistics"""
        # Ball count
        count_text = f"Balls: {len(self.balls)}"
        font = utils.font12
        text_surface = font.render(count_text, True, (255, 255, 255))
        utils.screen.blit(text_surface, (10, 10))
        
        # Split count
        splits_text = f"Splits: {self.split_count}"
        splits_surface = font.render(splits_text, True, (255, 255, 255))
        utils.screen.blit(splits_surface, (10, 30))
        
        # Max generation
        if self.balls:
            max_gen = max(getattr(ball, 'generation', 0) for ball in self.balls)
            gen_text = f"Max Generation: {max_gen}"
            gen_surface = font.render(gen_text, True, (255, 200, 0))
            utils.screen.blit(gen_surface, (10, 50))
        
        # Concept title
        title_text = "INFINITE BALL SPLIT"
        title_surface = utils.font16.render(title_text, True, (255, 100, 255))
        utils.screen.blit(title_surface, (10, utils.height - 40))
        
        # Description
        description = "Every collision splits ball into 2 smaller ones!"
        desc_surface = utils.font8.render(description, True, (200, 200, 200))
        utils.screen.blit(desc_surface, (10, utils.height - 20))
        
        description = "Each collision creates colorful particle explosions that spa..."
        desc_surface = utils.font8.render(description, True, (200, 200, 200))
        utils.screen.blit(desc_surface, (10, utils.height - 15))
