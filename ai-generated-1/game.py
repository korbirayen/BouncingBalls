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
        # VIRAL CONCEPT: "Every Bounce Makes Ball BIGGER!" 
        # CLONING 22M VIEW VIDEO: Ball grows each bounce until MASSIVE!
        
        self.balls = []
        self.particles = []
        self.sounds = Sounds()
        self.time_elapsed = 0
        
        # Size growth variables (THE CORE VIRAL MECHANIC)
        # Start ball in center of screen in world coordinates - make it bigger so it's visible!
        center_x = utils.width / 2
        center_y = utils.height / 2
        self.growth_ball = Ball(Vector2(center_x, center_y), 3.0, (255, 100, 100))  # Start at 3.0 radius = 30 pixels
        self.growth_ball.circle_body.linearVelocity = (random.uniform(-8, 8), random.uniform(-8, 8))
        self.balls.append(self.growth_ball)
        
        # Growth tracking
        self.bounce_count = 0
        self.growth_per_bounce = 1.15  # 15% bigger each bounce (VIRAL ESCALATION)
        self.max_size = 15.0  # Maximum before explosion (150 pixels radius)
        self.last_bounce_time = 0
        self.bounce_cooldown = 0.5  # Prevent rapid bounces
        
        # Visual effects for viral appeal
        self.size_history = [3.0]  # Track size progression starting from 3.0
        self.explosion_particles = []

        # Create static boundaries so the ball bounces inside the screen
        # Convert screen dimensions to Box2D world units
        world_width = utils.width / utils.PPM
        world_height = utils.height / utils.PPM
        
        # Create walls as static bodies
        walls = utils.world.CreateStaticBody()
        # Bottom wall
        walls.CreateEdgeFixture(vertices=[(0, 0), (world_width, 0)], friction=0.1, restitution=0.9)
        # Top wall  
        walls.CreateEdgeFixture(vertices=[(0, world_height), (world_width, world_height)], friction=0.1, restitution=0.9)
        # Left wall
        walls.CreateEdgeFixture(vertices=[(0, 0), (0, world_height)], friction=0.1, restitution=0.9)
        # Right wall
        walls.CreateEdgeFixture(vertices=[(world_width, 0), (world_width, world_height)], friction=0.1, restitution=0.9)
        
    def update(self):
        utils.world.Step(1.0 / 60.0, 6, 2)
        self.time_elapsed += utils.deltaTime()
        
        # THE VIRAL MECHANIC: Detect bounces and make ball BIGGER!
        ball = self.growth_ball
        current_velocity = Vector2(ball.circle_body.linearVelocity[0], ball.circle_body.linearVelocity[1])
        
        # Detect bounce by checking if ball hits walls or changes direction significantly
        pos = ball.getPos()
        radius_pixels = ball.radius * utils.PPM
        
        # Check wall collisions (BOUNCE DETECTION)
        hit_wall = (
            pos.x - radius_pixels <= 0 or pos.x + radius_pixels >= utils.width or
            pos.y - radius_pixels <= 0 or pos.y + radius_pixels >= utils.height
        )
        
        # Only grow if enough time passed since last bounce (prevent spam)
        current_time = time.time()
        if hit_wall and (current_time - self.last_bounce_time) > self.bounce_cooldown:
            self.grow_ball()
            self.last_bounce_time = current_time
        
        # Update ball color based on size (VISUAL ESCALATION)
        size_ratio = ball.radius / self.max_size
        intensity = min(size_ratio, 1.0)
        ball.color = (
            int(255 * (0.5 + 0.5 * intensity)),  # Red increases
            int(100 * (1 - intensity * 0.8)),    # Green decreases  
            int(100 * (1 - intensity * 0.8))     # Blue decreases
        )
        
        # Check for EXPLOSION (CLIMAX MOMENT)
        if ball.radius >= self.max_size:
            self.create_massive_explosion()
        
        # Update particles
        for exp in self.particles[:]:
            exp.update()
            if len(exp.particles) == 0:
                self.particles.remove(exp)
    
    def grow_ball(self):
        """THE CORE VIRAL MECHANIC: Make ball bigger each bounce!"""
        ball = self.growth_ball
        
        # Calculate new size
        old_radius = ball.radius
        new_radius = min(old_radius * self.growth_per_bounce, self.max_size)
        
        # Actually resize the ball (Box2D doesn't allow dynamic resizing, so recreate)
        old_pos = ball.getPos()
        old_velocity = Vector2(ball.circle_body.linearVelocity[0], ball.circle_body.linearVelocity[1])
        old_color = ball.color
        
        # Remove old ball
        self.balls.remove(ball)
        utils.world.DestroyBody(ball.circle_body)
        
        # Create new bigger ball
        self.growth_ball = Ball(old_pos, new_radius, old_color)
        self.growth_ball.circle_body.linearVelocity = (old_velocity.x * 0.95, old_velocity.y * 0.95)  # Slightly slower when bigger
        self.balls.append(self.growth_ball)
        
        # Track growth for display
        self.bounce_count += 1
        self.size_history.append(new_radius)
        if len(self.size_history) > 20:  # Keep history manageable
            self.size_history.pop(0)
        
        # VIRAL VISUAL FEEDBACK (simplified - no particles for now)
        # self.create_growth_effect(old_pos, old_radius, new_radius)
        
        # Sound feedback (gets higher pitch as ball grows)
        self.sounds.play()
        
        print(f"BOUNCE {self.bounce_count}! Size: {old_radius:.2f} → {new_radius:.2f}")
    
    def create_growth_effect(self, position, old_radius, new_radius):
        """Create satisfying visual effect when ball grows"""
        # Ring expansion effect (SATISFYING VISUAL)
        for i in range(12):
            angle = i * (2 * math.pi / 12)
            distance = (old_radius + new_radius) * utils.PPM * 0.5
            
            effect_pos = position + Vector2(
                math.cos(angle) * distance,
                math.sin(angle) * distance
            )
            
            # Growth particles
            growth_particle = Explosion(effect_pos, 8, (255, 200, 0), 1.2)
            self.particles.append(growth_particle)
        
        # Center burst effect
        center_burst = Explosion(position, 15, (255, 255, 255), 1.5)
        self.particles.append(center_burst)
    
    def create_massive_explosion(self):
        """CLIMAX: Massive explosion when ball reaches max size!"""
        ball = self.growth_ball
        pos = ball.getPos()
        
        # Remove the ball
        self.balls.remove(ball)
        utils.world.DestroyBody(ball.circle_body)
        
        # MASSIVE EXPLOSION EFFECT (simplified - no particles for now)
        # for ring in range(5):
        #     # particle effects disabled for now
        
        # Print the climax moment before resetting
        print(f"💥 MASSIVE EXPLOSION! Ball reached maximum size after {self.bounce_count} bounces!")
        # Reset for another cycle (ENDLESS LOOP)
        self.reset_ball()
    
    def reset_ball(self):
        """Reset for another viral cycle"""
        # Create new small ball in center
        center_x = utils.width / 2
        center_y = utils.height / 2
        self.growth_ball = Ball(Vector2(center_x, center_y), 3.0, (255, 100, 100))  # Start at 3.0 radius
        self.growth_ball.circle_body.linearVelocity = (random.uniform(-8, 8), random.uniform(-8, 8))
        self.balls.append(self.growth_ball)
        
        # Reset counters
        self.bounce_count = 0
        self.size_history = [3.0]
    
    def draw(self):
        # Draw size progression background
        self.draw_size_background()
        
        # Draw the growing ball
        for ball in self.balls:
            ball.draw()
            
            # Draw size indicator on ball (VIRAL VISUAL)
            pos = ball.getPos()
            size_text = f"x{ball.radius / 3.0:.1f}"  # Show growth multiplier from starting size 3.0
            font = utils.font12
            text_surface = font.render(size_text, True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(int(pos.x), int(pos.y)))
            utils.screen.blit(text_surface, text_rect)
            
        # Draw growth particles (disabled for now)
        # for exp in self.particles:
        #     exp.draw()
            
        # Draw viral stats
        self.draw_viral_stats()
    
    def draw_size_background(self):
        """Draw background showing growth progression"""
        if not self.balls:
            return
            
        ball = self.growth_ball
        size_ratio = ball.radius / self.max_size
        
        # Pulsing background that intensifies with size
        pulse = math.sin(self.time_elapsed * 5) * 0.3 + 0.7
        intensity = int(40 * size_ratio * pulse)
        
        # Draw expanding rings showing growth potential
        center = (utils.width // 2, utils.height // 2)
        for i in range(5):
            ring_radius = int(50 + i * 40 + ball.radius * utils.PPM * 0.5)
            alpha = max(0, intensity - i * 8)
            
            if alpha > 0 and ring_radius < utils.width:
                color = (alpha, alpha // 2, alpha // 2)
                pygame.draw.circle(utils.screen, color, center, ring_radius, 2)
    
    def draw_viral_stats(self):
        """Draw the viral statistics that make people watch"""
        font = utils.font12
        
        # Current size (THE MAIN METRIC)
        if self.balls:
            current_size = self.growth_ball.radius
            size_multiplier = current_size / 3.0  # Compare to starting size 3.0
            size_text = f"SIZE: {size_multiplier:.1f}x BIGGER!"
            size_surface = font.render(size_text, True, (255, 255, 0))
            utils.screen.blit(size_surface, (10, 10))
        
        # Bounce counter (PROGRESS INDICATOR)
        bounce_text = f"BOUNCES: {self.bounce_count}"
        bounce_surface = font.render(bounce_text, True, (255, 255, 255))
        utils.screen.blit(bounce_surface, (10, 30))
        
        # Progress to explosion (TENSION BUILDING)
        if self.balls:
            progress = (self.growth_ball.radius / self.max_size) * 100
            progress_text = f"EXPLOSION: {progress:.0f}%"
            color = (255, int(255 * (1 - progress/100)), 0)  # Red as it approaches
            progress_surface = font.render(progress_text, True, color)
            utils.screen.blit(progress_surface, (10, 50))
        
        # Size history graph (VISUAL PROGRESS)
        self.draw_size_graph()
        
        # Viral title
        title_text = "EVERY BOUNCE = BIGGER BALL!"
        title_surface = utils.font16.render(title_text, True, (255, 100, 100))
        utils.screen.blit(title_surface, (10, utils.height - 40))
        
        # Viral description  
        description = "Will it explode? 22M people watched to find out!"
        desc_surface = utils.font8.render(description, True, (200, 200, 200))
        utils.screen.blit(desc_surface, (10, utils.height - 20))
    
    def draw_size_graph(self):
        """Draw mini graph showing size progression (VISUAL SATISFACTION)"""
        if len(self.size_history) < 2:
            return
            
        # Graph area
        graph_x = 10
        graph_y = 80
        graph_width = 200
        graph_height = 40
        
        # Background
        pygame.draw.rect(utils.screen, (30, 30, 30), (graph_x, graph_y, graph_width, graph_height))
        
        # Plot size progression
        max_size_in_history = max(self.size_history)
        for i in range(len(self.size_history) - 1):
            x1 = graph_x + (i / len(self.size_history)) * graph_width
            x2 = graph_x + ((i + 1) / len(self.size_history)) * graph_width
            
            y1 = graph_y + graph_height - (self.size_history[i] / max_size_in_history) * graph_height
            y2 = graph_y + graph_height - (self.size_history[i + 1] / max_size_in_history) * graph_height
            
            # Line color based on size
            intensity = self.size_history[i + 1] / self.max_size
            color = (int(255 * intensity), int(200 * (1 - intensity)), 0)
            
            pygame.draw.line(utils.screen, color, (int(x1), int(y1)), (int(x2), int(y2)), 2)
        
        # Graph label
        label_surface = utils.font8.render("Size Growth", True, (200, 200, 200))
        utils.screen.blit(label_surface, (graph_x, graph_y - 15))
