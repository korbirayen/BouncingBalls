"""
Viral Video Concept Replacer
============================

This script replaces the generic AI-generated video templates with 
truly unique, viral-optimized implementations that actually deliver
what each concept promises.
"""

import os
import shutil
from pathlib import Path

def replace_generic_templates():
    """Replace all generic templates with unique viral implementations"""
    
    base_path = Path(__file__).parent
    
    # Unique viral concepts with actual implementations
    viral_concepts = {
        'ai-generated-3': {
            'title': 'GRAVITY FLIP SYMPHONY',
            'description': 'Gravity changes rhythmically creating mesmerizing dance!',
            'implementation': 'gravity_flip_symphony'
        },
        'ai-generated-4': {
            'title': 'SIZE DOUBLING MADNESS',
            'description': 'Ball doubles every 5 seconds until it fills screen!',
            'implementation': 'size_doubling_madness'
        },
        'ai-generated-5': {
            'title': 'RAINBOW TRAIL PAINTER',
            'description': 'Ball paints entire screen with rainbow trails!',
            'implementation': 'rainbow_trail_painter'
        },
        'ai-generated-6': {
            'title': 'MIRROR BALL UNIVERSE',
            'description': '4 synchronized balls create kaleidoscope patterns!',
            'implementation': 'mirror_ball_universe'
        },
        'ai-generated-11': {
            'title': 'PENDULUM HYPNOSIS',
            'description': 'Perfect pendulum with gradually increasing amplitude!',
            'implementation': 'pendulum_hypnosis'
        },
        'ai-generated-12': {
            'title': 'VORTEX CONSUMPTION',
            'description': 'Spinning center slowly consumes everything!',
            'implementation': 'vortex_consumption'
        }
    }
    
    print("🎥 Starting Viral Video Concept Replacement...")
    print(f"🔧 Replacing {len(viral_concepts)} generic templates with unique implementations")
    
    for folder_name, concept_info in viral_concepts.items():
        folder_path = base_path / folder_name
        
        if folder_path.exists():
            print(f"🎯 Implementing: {concept_info['title']}")
            create_unique_concept(folder_path, concept_info)
        else:
            print(f"❌ Folder not found: {folder_name}")
    
    print("✅ All viral concepts have been upgraded!")
    print("🚀 Ready to create truly engaging viral content!")

def create_unique_concept(folder_path, concept_info):
    """Create a unique implementation for a viral concept"""
    
    # Get the implementation type
    impl_type = concept_info['implementation']
    
    if impl_type == 'gravity_flip_symphony':
        create_gravity_flip_symphony(folder_path, concept_info)
    elif impl_type == 'size_doubling_madness':
        create_size_doubling_madness(folder_path, concept_info)
    elif impl_type == 'rainbow_trail_painter':
        create_rainbow_trail_painter(folder_path, concept_info)
    elif impl_type == 'mirror_ball_universe':
        create_mirror_ball_universe(folder_path, concept_info)
    elif impl_type == 'pendulum_hypnosis':
        create_pendulum_hypnosis(folder_path, concept_info)
    elif impl_type == 'vortex_consumption':
        create_vortex_consumption(folder_path, concept_info)

def create_gravity_flip_symphony(folder_path, concept_info):
    """Create gravity flip symphony implementation"""
    
    game_py_content = f'''import pygame
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
        # VIRAL CONCEPT: "{concept_info['title']}"
        # {concept_info['description']}
        
        self.balls = []
        self.particles = []
        self.sounds = Sounds()
        self.time_elapsed = 0
        
        # Gravity flip variables
        self.gravity_timer = 0
        self.gravity_flip_interval = 2.0  # Flip every 2 seconds
        self.current_gravity = (0, 9.8)
        self.gravity_directions = [
            (0, 9.8),   # Down
            (0, -9.8),  # Up
            (9.8, 0),   # Right
            (-9.8, 0),  # Left
            (6.9, 6.9), # Diagonal down-right
            (-6.9, 6.9), # Diagonal down-left
            (6.9, -6.9), # Diagonal up-right
            (-6.9, -6.9) # Diagonal up-left
        ]
        self.gravity_index = 0
        
        # Create multiple balls for better visual effect
        colors = [(255, 100, 100), (100, 255, 100), (100, 100, 255), 
                 (255, 255, 100), (255, 100, 255), (100, 255, 255)]
        
        for i in range(6):
            x = (i + 1) * utils.width / 7
            y = utils.height / 2 + random.uniform(-50, 50)
            ball = Ball(Vector2(x, y), 1.0 + random.uniform(-0.3, 0.3), colors[i])
            ball.body.linearVelocity = (random.uniform(-3, 3), random.uniform(-3, 3))
            self.balls.append(ball)
        
        # Visual effects
        self.gravity_arrows = []
        self.music_beat_timer = 0
        
    def update(self):
        utils.world.Step(1.0 / 60.0, 6, 2)
        self.time_elapsed += utils.deltaTime()
        self.gravity_timer += utils.deltaTime()
        self.music_beat_timer += utils.deltaTime()
        
        # Flip gravity rhythmically
        if self.gravity_timer >= self.gravity_flip_interval:
            self.flip_gravity()
            self.gravity_timer = 0
        
        # Create musical beat effects
        if self.music_beat_timer >= 0.5:  # Beat every 0.5 seconds
            self.create_beat_effect()
            self.music_beat_timer = 0
        
        # Update particles
        for exp in self.particles[:]:
            exp.update()
            if len(exp.particles) == 0:
                self.particles.remove(exp)
    
    def flip_gravity(self):
        """Flip gravity to next direction"""
        self.gravity_index = (self.gravity_index + 1) % len(self.gravity_directions)
        self.current_gravity = self.gravity_directions[self.gravity_index]
        utils.world.gravity = self.current_gravity
        
        # Visual feedback
        self.create_gravity_flip_effect()
        
        # Play sound
        self.sounds.play_sound("bounce")
    
    def create_gravity_flip_effect(self):
        """Create visual effect when gravity flips"""
        # Gravity arrows around screen edges
        for i in range(8):
            angle = i * (2 * math.pi / 8)
            x = utils.width/2 + math.cos(angle) * (utils.width * 0.4)
            y = utils.height/2 + math.sin(angle) * (utils.height * 0.4)
            
            explosion = Explosion(Vector2(x, y), 15, (255, 255, 0), 1.5)
            self.particles.append(explosion)
    
    def create_beat_effect(self):
        """Create musical beat visual effects"""
        # Pulse effect from center
        center = Vector2(utils.width/2, utils.height/2)
        
        for i in range(12):
            angle = i * (2 * math.pi / 12)
            distance = 100 + (self.music_beat_timer * 50)
            x = center.x + math.cos(angle) * distance
            y = center.y + math.sin(angle) * distance
            
            # Keep within bounds
            if 0 <= x <= utils.width and 0 <= y <= utils.height:
                color = (255, 200, 100)
                explosion = Explosion(Vector2(x, y), 5, color, 1.0)
                self.particles.append(explosion)
    
    def draw(self):
        # Draw gravity indicator background
        self.draw_gravity_background()
        
        # Draw balls
        for ball in self.balls:
            ball.draw()
            
        # Draw particles
        for exp in self.particles:
            exp.draw()
            
        # Draw gravity arrows and info
        self.draw_gravity_info()
    
    def draw_gravity_background(self):
        """Draw background showing gravity direction"""
        # Create gradient based on gravity direction
        gravity_strength = math.sqrt(self.current_gravity[0]**2 + self.current_gravity[1]**2)
        
        if gravity_strength > 0:
            # Normalize gravity vector
            gx = self.current_gravity[0] / gravity_strength
            gy = self.current_gravity[1] / gravity_strength
            
            # Draw gravity field lines
            for i in range(10):
                for j in range(10):
                    x = i * utils.width / 9
                    y = j * utils.height / 9
                    
                    # Arrow showing gravity direction
                    end_x = x + gx * 20
                    end_y = y + gy * 20
                    
                    alpha = int(30 + 25 * math.sin(self.time_elapsed * 2 + i + j))
                    color = (100, 150, 255, alpha)
                    
                    if 0 <= end_x <= utils.width and 0 <= end_y <= utils.height:
                        pygame.draw.line(utils.screen, color[:3], (int(x), int(y)), (int(end_x), int(end_y)), 1)
    
    def draw_gravity_info(self):
        """Draw gravity information and stats"""
        # Gravity direction
        gx, gy = self.current_gravity
        gravity_text = f"Gravity: ({{{gx:.1f}, {gy:.1f}})"
        font = utils.font12
        text_surface = font.render(gravity_text, True, (255, 255, 255))
        utils.screen.blit(text_surface, (10, 10))
        
        # Time until next flip
        time_remaining = self.gravity_flip_interval - self.gravity_timer
        timer_text = f"Next Flip: {{{time_remaining:.1f}}s"
        timer_surface = font.render(timer_text, True, (255, 200, 0))
        utils.screen.blit(timer_surface, (10, 30))
        
        # Flip counter
        flips_text = f"Flips: {{{self.gravity_index}}}"
        flips_surface = font.render(flips_text, True, (100, 255, 100))
        utils.screen.blit(flips_surface, (10, 50))
        
        # Concept title
        title_text = "{concept_info['title']}"
        title_surface = utils.font16.render(title_text, True, (255, 150, 255))
        utils.screen.blit(title_surface, (10, utils.height - 40))
        
        # Description
        description = "{concept_info['description']}"
        desc_surface = utils.font8.render(description, True, (200, 200, 200))
        utils.screen.blit(desc_surface, (10, utils.height - 20))
'''
    
    # Write the new game.py
    game_py_path = folder_path / "game.py"
    with open(game_py_path, 'w', encoding='utf-8') as f:
        f.write(game_py_content)

def create_size_doubling_madness(folder_path, concept_info):
    """Create size doubling madness implementation"""
    
    game_py_content = f'''import pygame
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
        # VIRAL CONCEPT: "{concept_info['title']}"
        # {concept_info['description']}
        
        self.balls = []
        self.particles = []
        self.sounds = Sounds()
        self.time_elapsed = 0
        
        # Size doubling variables
        self.size_timer = 0
        self.doubling_interval = 5.0  # Double every 5 seconds
        self.size_multiplier = 1.0
        self.max_size = 10.0  # Maximum size before reset
        
        # Create main ball
        self.main_ball = Ball(Vector2(utils.width / 2, utils.height / 2), 0.5, (255, 100, 100))
        self.main_ball.body.linearVelocity = (random.uniform(-4, 4), random.uniform(-4, 4))
        self.balls.append(self.main_ball)
        
        # Doubling effects
        self.doubling_count = 0
        self.size_history = [0.5]  # Track size progression
        
    def update(self):
        utils.world.Step(1.0 / 60.0, 6, 2)
        self.time_elapsed += utils.deltaTime()
        self.size_timer += utils.deltaTime()
        
        # Double size every interval
        if self.size_timer >= self.doubling_interval:
            self.double_ball_size()
            self.size_timer = 0
        
        # Update ball color based on size
        if self.balls:
            ball = self.main_ball
            size_ratio = ball.radius / self.max_size
            
            # Color shifts from red to white as it grows
            intensity = min(size_ratio, 1.0)
            ball.color = (
                255,
                int(100 + 155 * intensity),
                int(100 + 155 * intensity)
            )
            
            # Create size particles around large balls
            if ball.radius > 2.0 and random.random() < 0.2:
                self.create_size_particles(ball)
        
        # Update particles
        for exp in self.particles[:]:
            exp.update()
            if len(exp.particles) == 0:
                self.particles.remove(exp)
    
    def double_ball_size(self):
        """Double the ball's size"""
        if not self.balls:
            return
            
        ball = self.main_ball
        
        # Check if ball is too big - reset if so
        if ball.radius >= self.max_size:
            self.reset_ball_size()
            return
        
        # Double the size
        old_radius = ball.radius
        new_radius = min(ball.radius * 2.0, self.max_size)
        
        # Remove old ball body
        self.balls.remove(ball)
        utils.world.DestroyBody(ball.body)
        
        # Create new ball with doubled size
        position = Vector2(ball.body.position[0] * utils.PPM, ball.body.position[1] * utils.PPM)
        velocity = Vector2(ball.body.linearVelocity[0], ball.body.linearVelocity[1])
        
        self.main_ball = Ball(position, new_radius, ball.color)
        self.main_ball.body.linearVelocity = (velocity.x * 0.9, velocity.y * 0.9)  # Slightly slower when bigger
        self.balls.append(self.main_ball)
        
        # Track size progression
        self.size_history.append(new_radius)
        if len(self.size_history) > 10:
            self.size_history.pop(0)
        
        # Visual effects
        self.create_doubling_effect(position, old_radius, new_radius)
        self.doubling_count += 1
        
        # Play sound
        self.sounds.play_sound("bounce")
    
    def reset_ball_size(self):
        """Reset ball to original size when it gets too big"""
        if not self.balls:
            return
            
        ball = self.main_ball
        position = Vector2(ball.body.position[0] * utils.PPM, ball.body.position[1] * utils.PPM)
        
        # Create explosion effect before reset
        explosion = Explosion(position, 50, (255, 255, 255), 2.0)
        self.particles.append(explosion)
        
        # Reset size
        self.balls.remove(ball)
        utils.world.DestroyBody(ball.body)
        
        self.main_ball = Ball(Vector2(utils.width / 2, utils.height / 2), 0.5, (255, 100, 100))
        self.main_ball.body.linearVelocity = (random.uniform(-4, 4), random.uniform(-4, 4))
        self.balls.append(self.main_ball)
        
        # Reset counters
        self.doubling_count = 0
        self.size_history = [0.5]
    
    def create_doubling_effect(self, position, old_radius, new_radius):
        """Create visual effect when ball doubles in size"""
        # Ring expansion effect
        for i in range(16):
            angle = i * (2 * math.pi / 16)
            distance = old_radius + 20
            x = position.x + math.cos(angle) * distance
            y = position.y + math.sin(angle) * distance
            
            explosion = Explosion(Vector2(x, y), 10, (255, 200, 0), 1.5)
            self.particles.append(explosion)
        
        # Size indicator particles
        size_ratio = new_radius / 0.5  # Ratio compared to original
        for i in range(int(size_ratio)):
            angle = random.uniform(0, 2 * math.pi)
            distance = random.uniform(new_radius + 10, new_radius + 30)
            x = position.x + math.cos(angle) * distance
            y = position.y + math.sin(angle) * distance
            
            particle = Explosion(Vector2(x, y), 5, (255, 255, 255), 1.0)
            self.particles.append(particle)
    
    def create_size_particles(self, ball):
        """Create particles around large balls"""
        position = Vector2(ball.body.position[0] * utils.PPM, ball.body.position[1] * utils.PPM)
        
        # Orbiting particles
        angle = random.uniform(0, 2 * math.pi)
        distance = ball.radius + 15
        x = position.x + math.cos(angle) * distance
        y = position.y + math.sin(angle) * distance
        
        color = (255, 150 + int(ball.radius * 20), 150 + int(ball.radius * 20))
        particle = Explosion(Vector2(x, y), 3, color, 0.8)
        self.particles.append(particle)
    
    def draw(self):
        # Draw size progression background
        self.draw_size_background()
        
        # Draw balls
        for ball in self.balls:
            ball.draw()
            
            # Draw size indicator on ball
            if ball.radius > 1.0:
                pos = Vector2(ball.body.position[0] * utils.PPM, ball.body.position[1] * utils.PPM)
                size_text = f"x{{int(ball.radius / 0.5)}}"
                text_surface = utils.font12.render(size_text, True, (255, 255, 255))
                text_rect = text_surface.get_rect(center=(int(pos.x), int(pos.y)))
                utils.screen.blit(text_surface, text_rect)
            
        # Draw particles
        for exp in self.particles:
            exp.draw()
            
        # Draw size stats
        self.draw_size_stats()
    
    def draw_size_background(self):
        """Draw background showing size progression"""
        if not self.balls:
            return
            
        ball = self.main_ball
        size_ratio = ball.radius / self.max_size
        
        # Pulsing background intensity based on size
        intensity = int(30 * size_ratio)
        color = (intensity, intensity // 2, intensity // 2)
        
        # Draw expanding circles
        center = (utils.width // 2, utils.height // 2)
        for i in range(5):
            radius = 50 + i * 40 + ball.radius * 20
            alpha = max(0, intensity - i * 10)
            
            if alpha > 0:
                pygame.draw.circle(utils.screen, color, center, int(radius), 2)
    
    def draw_size_stats(self):
        """Draw size statistics"""
        # Current size
        if self.balls:
            current_size = self.main_ball.radius
            size_text = f"Size: {{current_size:.2f}} (x{{current_size / 0.5:.1f}})"
            font = utils.font12
            text_surface = font.render(size_text, True, (255, 255, 255))
            utils.screen.blit(text_surface, (10, 10))
        
        # Time until next doubling
        time_remaining = self.doubling_interval - self.size_timer
        timer_text = f"Next Double: {{time_remaining:.1f}}s"
        timer_surface = font.render(timer_text, True, (255, 200, 0))
        utils.screen.blit(timer_surface, (10, 30))
        
        # Doubling count
        count_text = f"Doublings: {{self.doubling_count}}"
        count_surface = font.render(count_text, True, (100, 255, 100))
        utils.screen.blit(count_surface, (10, 50))
        
        # Concept title
        title_text = "{concept_info['title']}"
        title_surface = utils.font16.render(title_text, True, (255, 100, 100))
        utils.screen.blit(title_surface, (10, utils.height - 40))
        
        # Description
        description = "{concept_info['description']}"
        desc_surface = utils.font8.render(description, True, (200, 200, 200))
        utils.screen.blit(desc_surface, (10, utils.height - 20))
'''
    
    # Write the new game.py
    game_py_path = folder_path / "game.py"
    with open(game_py_path, 'w', encoding='utf-8') as f:
        f.write(game_py_content)

# Add other implementation functions here...

if __name__ == "__main__":
    replace_generic_templates()
