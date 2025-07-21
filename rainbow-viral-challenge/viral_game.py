import math
import random
import pygame
from pygame import Vector2

from Ball import Ball
from ring import Ring
from particle import Explosion
from sounds import Sounds
from util import utils


class ViralGame:
    def __init__(self):
        print("Creating RAINBOW VIRAL CHALLENGE...")
        
        # VIRAL VIDEO CONCEPT: Rainbow Ball Multiplication Challenge
        # GOAL: Fill all rings with multiplying rainbow balls before time runs out
        
                viral_text = 'VIRAL PHYSICS | RAINBOW MULTIPLICATION | CHAIN REACTIONS'
        viral_surface = utils.font8.render(viral_text, True, (150, 255, 150))
        utils.screen.blit(viral_surface, (10, bottom_y + 20))tarting with one rainbow ball
        start_color = (255, 0, 0)  # Start with red
        
        self.balls = [
            Ball(Vector2(utils.width / 2, utils.height - 100), Vector2(0, -300),
                 radius=4.0, color=start_color),
        ]
        
        # VIRAL VIDEO PARAMETERS
        self.time_limit = 120.0  # 2 minutes for maximum suspense
        self.current_time = 0
        self.balls_created = 1
        self.rings_filled = 0
        self.chain_reactions = 0
        self.max_multiplier = 0
        
        # VIRAL MECHANICS
        self.multiplication_chance = 0.85  # High chance for viral effect
        self.rainbow_speed = 0.03  # Color cycling speed
        self.explosion_power = 25  # Particle count for explosions
        
        self.particles = []
        
        # CHALLENGE RINGS - Strategic placement for viral suspense
        self.rings = [
            Ring(Vector2(utils.width/5, utils.height/3), 100, 1),      # Top left
            Ring(Vector2(4*utils.width/5, utils.height/3), 90, 1),     # Top right
            Ring(Vector2(utils.width/2, utils.height/2), 120, 1),      # Center
            Ring(Vector2(utils.width/4, 3*utils.height/4), 80, 1),     # Bottom left
            Ring(Vector2(3*utils.width/4, 3*utils.height/4), 85, 1),   # Bottom right
        ]
        
        # Ring tracking for viral challenge
        for i, ring in enumerate(self.rings):
            ring.target_balls = 25 + (i * 5)  # Increasing difficulty
            ring.is_filled = False
            ring.fill_percentage = 0.0
            ring.rainbow_phase = random.random()
            ring.id = i + 1
        
        self.sounds = Sounds()
        self.global_rainbow_phase = 0

        # Initialize ball properties
        for ball in self.balls:
            ball.rainbow_phase = 0
            ball.generation = 0
            ball.multiplier_power = 1.0

    def get_rainbow_color(self, phase):
        """Generate smooth rainbow colors for viral visual appeal"""
        # Enhanced rainbow with more vibrant colors
        colors = [
            (255, 0, 0),     # Red
            (255, 64, 0),    # Red-Orange
            (255, 128, 0),   # Orange
            (255, 192, 0),   # Yellow-Orange
            (255, 255, 0),   # Yellow
            (128, 255, 0),   # Yellow-Green
            (0, 255, 0),     # Green
            (0, 255, 128),   # Green-Cyan
            (0, 255, 255),   # Cyan
            (0, 128, 255),   # Cyan-Blue
            (0, 0, 255),     # Blue
            (128, 0, 255),   # Blue-Purple
            (255, 0, 255),   # Purple
            (255, 0, 128),   # Purple-Pink
        ]
        
        # Smooth interpolation between colors
        scaled_phase = phase * len(colors)
        index = int(scaled_phase) % len(colors)
        next_index = (index + 1) % len(colors)
        t = scaled_phase - int(scaled_phase)
        
        current = colors[index]
        next_color = colors[next_index]
        
        r = int(current[0] * (1-t) + next_color[0] * t)
        g = int(current[1] * (1-t) + next_color[1] * t)
        b = int(current[2] * (1-t) + next_color[2] * t)
        
        return (r, g, b)

    def calculate_ring_fill_percentage(self, ring):
        """Calculate ring fill percentage - creates viral suspense"""
        balls_in_ring = 0
        ring_center = ring.center
        
        for ball in self.balls:
            ball_pos = ball.getPos()
            distance = (ball_pos - ring_center).length()
            if distance < ring.radius:
                balls_in_ring += 1
        
        ring.fill_percentage = min(100.0, (balls_in_ring / ring.target_balls) * 100)
        
        # VIRAL MOMENT: Ring completion explosion
        if ring.fill_percentage >= 100.0 and not ring.is_filled:
            ring.is_filled = True
            self.rings_filled += 1
            self.create_viral_explosion(ring)
            print(f"RING {ring.id} COMPLETED! ({self.rings_filled}/{len(self.rings)})")

    def create_viral_explosion(self, ring):
        """MASSIVE viral explosion when ring is completed"""
        center = ring.center
        
        # Create massive particle explosion
        for i in range(self.explosion_power * 2):
            angle = (2 * math.pi * i) / (self.explosion_power * 2)
            distance = random.uniform(ring.radius * 0.8, ring.radius * 2.0)
            
            x = center.x + distance * math.cos(angle)
            y = center.y + distance * math.sin(angle)
            
            # Rainbow explosion colors
            rainbow_color = self.get_rainbow_color(random.random())
            white_flash = (255, 255, 255)
            
            self.particles.append(Explosion(x, y, rainbow_color, white_flash))
        
        # Chain reaction chance - viral surprise element
        if random.random() < 0.3:  # 30% chance
            self.trigger_chain_reaction(ring)

    def trigger_chain_reaction(self, source_ring):
        """Surprise chain reactions - unexpected viral moments"""
        self.chain_reactions += 1
        print(f"CHAIN REACTION #{self.chain_reactions}!")
        
        # Find nearby rings for chain effect
        for ring in self.rings:
            if ring != source_ring and not ring.is_filled:
                distance = (ring.center - source_ring.center).length()
                if distance < 200:  # Close enough for chain reaction
                    
                    # Create lightning effect between rings
                    steps = 15
                    for i in range(steps):
                        t = i / steps
                        chain_x = source_ring.center.x * (1-t) + ring.center.x * t
                        chain_y = source_ring.center.y * (1-t) + ring.center.y * t
                        
                        lightning_color = self.get_rainbow_color(t)
                        self.particles.append(Explosion(chain_x, chain_y, lightning_color, (255, 255, 255)))
                    
                    # Spawn bonus balls near target ring
                    self.spawn_bonus_balls(ring, 8)
                    break

    def spawn_bonus_balls(self, target_ring, count):
        """Spawn bonus balls with special properties"""
        for i in range(count):
            angle = (2 * math.pi * i) / count + random.uniform(-0.3, 0.3)
            distance = random.uniform(40, 70)
            
            x = target_ring.center.x + distance * math.cos(angle)
            y = target_ring.center.y + distance * math.sin(angle)
            
            # Keep within bounds
            x = max(30, min(utils.width - 30, x))
            y = max(30, min(utils.height - 30, y))
            
            # Special rainbow color
            bonus_color = self.get_rainbow_color(random.random())
            
            # Random velocity for chaotic effect
            velocity = Vector2(
                random.uniform(-300, 300),
                random.uniform(-200, 200)
            )
            
            bonus_ball = Ball(Vector2(x, y), velocity, 
                            radius=random.uniform(3.0, 5.0), 
                            color=bonus_color)
            
            # Special properties for bonus balls
            bonus_ball.rainbow_phase = random.random()
            bonus_ball.generation = 999  # Special marker
            bonus_ball.multiplier_power = 2.0  # Double power!
            
            self.balls.append(bonus_ball)
            self.balls_created += 1

    def viral_multiplication(self, ball, collision_point):
        """VIRAL ball multiplication with rainbow effects"""
        if len(self.balls) >= 250:  # Performance limit
            return
        
        # High multiplication chance for viral effect
        if random.random() < self.multiplication_chance:
            
            # More offspring for viral appeal
            offspring_count = random.randint(2, 5)
            if ball.generation == 999:  # Bonus balls multiply more
                offspring_count = random.randint(4, 7)
            
            multiplier = min(offspring_count, 6)
            self.max_multiplier = max(self.max_multiplier, multiplier)
            
            for i in range(offspring_count):
                angle = (2 * math.pi * i) / offspring_count + random.uniform(-0.4, 0.4)
                distance = random.uniform(30, 55)
                
                new_x = collision_point[0] + distance * math.cos(angle)
                new_y = collision_point[1] + distance * math.sin(angle)
                
                # Keep balls on screen
                new_x = max(25, min(utils.width - 25, new_x))
                new_y = max(25, min(utils.height - 25, new_y))
                
                # Progressive rainbow colors
                color_offset = (i * 0.25) % 1.0
                new_rainbow_phase = (ball.rainbow_phase + color_offset) % 1.0
                new_color = self.get_rainbow_color(new_rainbow_phase)
                
                # Chaotic velocities for viral effect
                velocity = Vector2(
                    random.uniform(-280, 280),
                    random.uniform(-220, 220)
                )
                
                new_ball = Ball(Vector2(new_x, new_y), velocity, 
                              radius=random.uniform(2.5, 4.0), 
                              color=new_color)
                
                new_ball.rainbow_phase = new_rainbow_phase
                new_ball.generation = ball.generation + 1
                new_ball.multiplier_power = ball.multiplier_power * 0.9  # Slight decay
                
                self.balls.append(new_ball)
                self.balls_created += 1
            
            # Viral explosion effect
            explosion_color1 = self.get_rainbow_color(ball.rainbow_phase)
            explosion_color2 = self.get_rainbow_color((ball.rainbow_phase + 0.5) % 1.0)
            
            for j in range(self.explosion_power):
                angle = (2 * math.pi * j) / self.explosion_power
                exp_distance = random.uniform(15, 35)
                exp_x = collision_point[0] + exp_distance * math.cos(angle)
                exp_y = collision_point[1] + exp_distance * math.sin(angle)
                
                self.particles.append(Explosion(exp_x, exp_y, explosion_color1, explosion_color2))
            
            self.sounds.play()

    def update(self):
        utils.world.Step(1.5 / 60.0, 6, 2)
        
        # Update timer - creates viral suspense
        self.current_time += 1.0 / 60.0
        time_remaining = max(0, self.time_limit - self.current_time)
        
        # Update global rainbow effect
        self.global_rainbow_phase += self.rainbow_speed
        if self.global_rainbow_phase > 1.0:
            self.global_rainbow_phase -= 1.0
        
        # Update all balls with rainbow colors
        for ball in self.balls:
            ball.rainbow_phase += self.rainbow_speed * (0.5 + random.uniform(-0.1, 0.1))
            if ball.rainbow_phase > 1.0:
                ball.rainbow_phase -= 1.0
            
            # Apply rainbow color
            ball.color = self.get_rainbow_color(ball.rainbow_phase)

        # Update ring fill tracking
        for ring in self.rings:
            self.calculate_ring_fill_percentage(ring)
            
            # Rainbow effect for rings close to completion
            if ring.fill_percentage > 75:
                ring.rainbow_phase += 0.08
                if ring.rainbow_phase > 1.0:
                    ring.rainbow_phase -= 1.0

        # Ball-ring viral interactions
        for ball in self.balls:
            ball_pos = ball.getPos()
            
            for ring in self.rings:
                distance = (ball_pos - ring.center).length()
                
                # Inside ring - chance for viral multiplication
                if distance < ring.radius:
                    if random.random() < 0.025:  # 2.5% chance per frame
                        self.viral_multiplication(ball, (ring.center.x, ring.center.y))

        # Ball collision viral multiplication
        if utils.contactListener.collisions:
            for bodyA, bodyB, point in utils.contactListener.collisions:
                utils.contactListener.collisions = []
                pos = utils.to_Pos(point)
                
                if (hasattr(bodyA.userData, 'radius') and hasattr(bodyB.userData, 'radius')):
                    ballA = bodyA.userData
                    ballB = bodyB.userData
                    
                    # Both balls can trigger multiplication
                    self.viral_multiplication(ballA, pos)
                    
                    # Rainbow collision explosion
                    color1 = self.get_rainbow_color(ballA.rainbow_phase)
                    color2 = self.get_rainbow_color(ballB.rainbow_phase) if hasattr(ballB, 'rainbow_phase') else (255, 255, 255)
                    self.particles.append(Explosion(pos[0], pos[1], color1, color2))
                    self.sounds.play()
                break

        # Remove balls that fall off screen
        balls_to_remove = []
        for ball in self.balls:
            if ball.radius < 1.0 or ball.getPos().y > utils.height + 150:
                balls_to_remove.append(ball)
                
        for ball in balls_to_remove:
            if ball in self.balls:
                utils.world.DestroyBody(ball.circle_body)
                self.balls.remove(ball)

        # Update particles
        for exp in self.particles:
            exp.update()
            if len(exp.particles) == 0:
                self.particles.remove(exp)

        # Victory condition - continuous celebration
        if self.rings_filled >= len(self.rings):
            if random.random() < 0.15:  # 15% chance per frame for celebration
                center_x = utils.width / 2
                center_y = utils.height / 2
                victory_color = self.get_rainbow_color(random.random())
                
                for i in range(5):
                    spread_x = center_x + random.uniform(-100, 100)
                    spread_y = center_y + random.uniform(-100, 100)
                    self.particles.append(Explosion(spread_x, spread_y, victory_color, (255, 255, 255)))

    def draw(self):
        # Draw rings with viral rainbow effects
        for ring in self.rings:
            if ring.is_filled:
                # Golden completed ring
                ring.color = (255, 215, 0)
            elif ring.fill_percentage > 75:
                # Rainbow ring when almost full - builds suspense
                ring.color = self.get_rainbow_color(ring.rainbow_phase)
            elif ring.fill_percentage > 50:
                # Yellow warning ring
                ring.color = (255, 255, 0)
            elif ring.fill_percentage > 25:
                # Orange progress ring
                ring.color = (255, 165, 0)
            else:
                # Gray empty ring
                ring.color = (128, 128, 128)
            
            ring.draw()
            
        # Draw all rainbow balls
        for ball in self.balls:
            ball.draw()

        # Draw viral particle explosions
        for exp in self.particles:
            exp.draw()
            
        self.draw_viral_stats()

    def draw_viral_stats(self):
        """Draw viral video statistics and progress"""
        
        # TIME REMAINING - Creates urgency
        time_remaining = max(0, self.time_limit - self.current_time)
        minutes = int(time_remaining // 60)
        seconds = int(time_remaining % 60)
        
        if time_remaining < 30:
            time_color = (255, 50, 50)  # Red urgency
        elif time_remaining < 60:
            time_color = (255, 200, 0)  # Yellow warning
        else:
            time_color = (255, 255, 255)  # White normal
            
        time_text = f'TIME: {minutes}:{seconds:02d}'
        time_surface = utils.font16.render(time_text, True, time_color)
        utils.screen.blit(time_surface, (utils.width - 140, 10))
        
        # BALL COUNT - Satisfying growing numbers
        balls_text = f'BALLS: {len(self.balls)}'
        balls_surface = utils.font16.render(balls_text, True, (255, 255, 255))
        utils.screen.blit(balls_surface, (10, 10))
        
        # TOTAL CREATED
        created_text = f'CREATED: {self.balls_created}'
        created_surface = utils.font12.render(created_text, True, (0, 255, 0))
        utils.screen.blit(created_surface, (10, 40))
        
        # RINGS PROGRESS - Main challenge
        rings_text = f'RINGS: {self.rings_filled}/{len(self.rings)}'
        if self.rings_filled == len(self.rings):
            rings_color = self.get_rainbow_color(self.global_rainbow_phase)
        else:
            rings_color = (255, 200, 0)
            
        rings_surface = utils.font16.render(rings_text, True, rings_color)
        utils.screen.blit(rings_surface, (10, 70))
        
        # INDIVIDUAL RING PROGRESS
        y_start = 105
        for i, ring in enumerate(self.rings):
            progress_text = f'Ring {ring.id}: {ring.fill_percentage:.0f}%'
            
            if ring.is_filled:
                progress_color = (0, 255, 0)
            elif ring.fill_percentage > 75:
                progress_color = self.get_rainbow_color(ring.rainbow_phase)
            elif ring.fill_percentage > 50:
                progress_color = (255, 255, 0)
            elif ring.fill_percentage > 25:
                progress_color = (255, 165, 0)
            else:
                progress_color = (150, 150, 150)
                
            progress_surface = utils.font8.render(progress_text, True, progress_color)
            utils.screen.blit(progress_surface, (10, y_start + i * 15))
        
        # VIRAL STATISTICS
        if self.chain_reactions > 0:
            chain_text = f'CHAIN REACTIONS: {self.chain_reactions}'
            chain_surface = utils.font12.render(chain_text, True, (255, 100, 255))
            utils.screen.blit(chain_surface, (10, y_start + 85))
        
        if self.max_multiplier > 0:
            mult_text = f'MAX MULTIPLIER: x{self.max_multiplier}'
            mult_surface = utils.font8.render(mult_text, True, (200, 100, 200))
            utils.screen.blit(mult_surface, (10, y_start + 105))
        
        # MAIN STATUS - Center drama
        if self.rings_filled >= len(self.rings):
            status_text = 'VIRAL CHALLENGE COMPLETE!'
            status_color = self.get_rainbow_color(random.random())
        elif time_remaining <= 0:
            status_text = 'TIME UP!'
            status_color = (255, 50, 50)
        elif self.rings_filled > len(self.rings) // 2:
            status_text = 'ALMOST VIRAL!'
            status_color = (255, 200, 0)
        else:
            status_text = 'FILL ALL RINGS!'
            status_color = (255, 255, 255)
            
        status_surface = utils.font16.render(status_text, True, status_color)
        text_rect = status_surface.get_rect(center=(utils.width//2, 60))
        utils.screen.blit(status_surface, text_rect)
        
        # BOTTOM VIRAL BRANDING
        bottom_y = utils.height - 50
        
        title_text = 'RAINBOW VIRAL CHALLENGE'
        title_color = self.get_rainbow_color(self.global_rainbow_phase)
        title_surface = utils.font12.render(title_text, True, title_color)
        utils.screen.blit(title_surface, (10, bottom_y))
        
        viral_text = 'VIRAL PHYSICS | RAINBOW MULTIPLICATION | CHAIN REACTIONS'
        viral_surface = utils.font8.render(viral_text, True, (150, 255, 150))
        utils.screen.blit(viral_surface, (10, bottom_y + 20))
