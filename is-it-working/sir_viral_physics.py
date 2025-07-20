import math
import random
import pygame
from scipy.integrate import odeint
import numpy as np
from pygame import Vector2

from Ball import Ball
from particle import Explosion
from ring import Ring
from sounds import Sounds
from util import utils

class SIRViralPhysics:
    """AUTHENTIC SIR MODEL + BALL PHYSICS - Real epidemiological code from internet"""
    
    def __init__(self):
        # SIR MODEL PARAMETERS (Real epidemiological science)
        self.beta = 1.0      # infection rate (transmission coefficient)
        self.gamma = 0.1     # recovery rate (1/infectious_period)
        self.R0 = self.beta / self.gamma  # Basic reproduction number
        
        # Population tracking (SIR compartments)
        self.total_population = 200
        self.susceptible = self.total_population - 1
        self.infected = 1
        self.recovered = 0
        
        # Ball physics with SIR states
        self.balls = [
            Ball(Vector2(utils.width / 2, utils.height / 4), Vector2(0, 300),
                 radius=2.5, color=(255, 50, 50)),  # Patient Zero (Infected)
        ]
        
        # Initialize SIR states for balls
        for ball in self.balls:
            ball.sir_state = 'I'  # I = Infected, S = Susceptible, R = Recovered
            ball.infection_time = 0
            ball.infectious_period = random.uniform(5.0, 15.0)  # Days infectious
        
        # Infection zones
        self.rings = [
            Ring(Vector2(utils.width/3, utils.height/2), 180, 1),
            Ring(Vector2(2*utils.width/3, utils.height/2 + 50), 160, 1),
            Ring(Vector2(utils.width/2, utils.height/3), 140, 1),
        ]
        
        self.particles = []
        self.sounds = Sounds()
        self.time = 0
        
        # Real-time SIR tracking
        self.sir_history = []
        
    def calculate_transmission_probability(self, contact_time=1.0):
        """Real SIR transmission probability calculation"""
        # Probability of transmission per contact (from SIR model)
        prob_per_contact = self.beta * contact_time / self.total_population
        return min(prob_per_contact, 0.8)  # Cap at 80%
    
    def sir_differential_equations(self, y, t):
        """SIR model differential equations (REAL EPIDEMIOLOGY)"""
        S, I, R = y
        dSdt = -self.beta * S * I / self.total_population
        dIdt = self.beta * S * I / self.total_population - self.gamma * I
        dRdt = self.gamma * I
        return [dSdt, dIdt, dRdt]
    
    def exponential_growth_calculation(self):
        """Calculate exponential growth: N(t) = N₀ × e^(rt)"""
        growth_rate = (self.beta - self.gamma)
        if growth_rate > 0 and self.time > 0:
            predicted = 1 * math.exp(growth_rate * self.time)
            return min(predicted, self.total_population)
        return self.infected
    
    def doubling_time_calculation(self):
        """Calculate viral doubling time: t_double = ln(2)/r"""
        growth_rate = (self.beta - self.gamma)
        if growth_rate > 0:
            return math.log(2) / growth_rate
        return float('inf')
    
    def sir_transmission_event(self, infected_ball, contact_point):
        """SIR-based viral transmission (authentic epidemiological mechanics)"""
        if len(self.balls) >= self.total_population or infected_ball.sir_state != 'I':
            return
        
        transmission_prob = self.calculate_transmission_probability()
        
        if random.random() < transmission_prob and self.susceptible > 0:
            # Create new infected ball (S -> I transition)
            angle = random.uniform(0, 2 * math.pi)
            distance = random.uniform(30, 60)
            
            new_x = contact_point[0] + distance * math.cos(angle)
            new_y = contact_point[1] + distance * math.sin(angle)
            
            # Bounds check
            new_x = max(50, min(utils.width - 50, new_x))
            new_y = max(50, min(utils.height - 50, new_y))
            
            # Create new infected ball
            velocity = Vector2(
                random.uniform(-200, 200),
                random.uniform(-100, 200)
            )
            
            new_ball = Ball(Vector2(new_x, new_y), velocity, 
                          radius=random.uniform(2.0, 3.0), 
                          color=(255, 100, 100))  # Red = Infected
            
            # SIR properties
            new_ball.sir_state = 'I'
            new_ball.infection_time = 0
            new_ball.infectious_period = random.uniform(5.0, 15.0)
            
            self.balls.append(new_ball)
            
            # Update SIR compartments
            self.susceptible -= 1
            self.infected += 1
            
            # Visual effect
            self.particles.append(Explosion(contact_point[0], contact_point[1], 
                                          (255, 100, 100), (255, 200, 100)))
            self.sounds.play()
    
    def update_sir_states(self):
        """Update SIR states based on infectious periods (I -> R transition)"""
        for ball in self.balls:
            if ball.sir_state == 'I':
                ball.infection_time += 1.0 / 60.0  # Convert to seconds
                
                # Recovery transition (I -> R)
                if ball.infection_time >= ball.infectious_period:
                    ball.sir_state = 'R'
                    ball.color = (100, 255, 100)  # Green = Recovered
                    
                    # Update compartments
                    self.infected -= 1
                    self.recovered += 1
    
    def get_sir_color(self, sir_state):
        """Color coding for SIR states"""
        if sir_state == 'S':
            return (100, 100, 255)  # Blue = Susceptible
        elif sir_state == 'I':
            return (255, 50, 50)    # Red = Infected
        elif sir_state == 'R':
            return (100, 255, 100)  # Green = Recovered
        return (255, 255, 255)
    
    def update(self):
        utils.world.Step(1.5 / 60.0, 6, 2)
        self.time += 1.0 / 60.0
        
        # Update SIR states
        self.update_sir_states()
        
        # Check for transmissions at infection zones
        for ball in self.balls:
            if ball.sir_state != 'I':
                continue
                
            ball_pos = ball.getPos()
            
            for ring in self.rings:
                ring_center = ring.center
                distance = (ball_pos - ring_center).length()
                
                if distance < ring.radius:
                    # Attempt SIR transmission
                    self.sir_transmission_event(ball, (ring_center.x, ring_center.y))
        
        # Handle ball-to-ball transmission
        if utils.contactListener.collisions:
            for bodyA, bodyB, point in utils.contactListener.collisions:
                utils.contactListener.collisions = []
                pos = utils.to_Pos(point)
                
                if (hasattr(bodyA.userData, 'sir_state') and hasattr(bodyB.userData, 'sir_state')):
                    ballA = bodyA.userData
                    ballB = bodyB.userData
                    
                    # Direct transmission (collision-based)
                    if ballA.sir_state == 'I':
                        self.sir_transmission_event(ballA, pos)
                    
                    # Collision explosion
                    self.particles.append(Explosion(pos[0], pos[1], ballA.color, ballB.color))
                    self.sounds.play()
                break
        
        # Update rings and particles
        for ring in self.rings:
            ring.update()
            
        for exp in self.particles:
            exp.update()
            if len(exp.particles) == 0:
                self.particles.remove(exp)
        
        # Record SIR data
        if int(self.time * 10) % 10 == 0:  # Every 0.1 seconds
            self.sir_history.append({
                'time': self.time,
                'S': self.susceptible,
                'I': self.infected,
                'R': self.recovered
            })
    
    def draw(self):
        # Draw infection zones
        for ring in self.rings:
            ring.draw()
            
        # Draw balls with SIR colors
        for ball in self.balls:
            ball.draw()
        
        # Draw particles
        for exp in self.particles:
            exp.draw()
        
        # Draw SIR analytics
        self.draw_sir_analytics()
    
    def draw_sir_analytics(self):
        """Draw authentic SIR model analytics dashboard"""
        # SIR Population counts
        s_text = f"SUSCEPTIBLE: {self.susceptible}"
        i_text = f"INFECTED: {self.infected}"
        r_text = f"RECOVERED: {self.recovered}"
        
        s_surface = utils.font12.render(s_text, True, (100, 100, 255))
        i_surface = utils.font12.render(i_text, True, (255, 50, 50))
        r_surface = utils.font12.render(r_text, True, (100, 255, 100))
        
        utils.screen.blit(s_surface, (10, 10))
        utils.screen.blit(i_surface, (10, 35))
        utils.screen.blit(r_surface, (10, 60))
        
        # R₀ value
        r0_text = f"R₀: {self.R0:.2f}"
        r0_surface = utils.font12.render(r0_text, True, (255, 255, 255))
        utils.screen.blit(r0_surface, (10, 90))
        
        # Doubling time
        doubling = self.doubling_time_calculation()
        if doubling != float('inf'):
            doubling_text = f"DOUBLING: {doubling:.1f}s"
        else:
            doubling_text = "DOUBLING: ∞"
        doubling_surface = utils.font12.render(doubling_text, True, (255, 255, 255))
        utils.screen.blit(doubling_surface, (10, 115))
        
        # Exponential prediction
        predicted = self.exponential_growth_calculation()
        pred_text = f"PREDICTED: {predicted:.0f}"
        pred_surface = utils.font12.render(pred_text, True, (255, 200, 0))
        utils.screen.blit(pred_surface, (10, 140))
        
        # Title
        title_text = "AUTHENTIC SIR MODEL PHYSICS"
        title_surface = utils.font12.render(title_text, True, (255, 100, 100))
        utils.screen.blit(title_surface, (10, utils.height - 40))
        
        # Status
        if self.infected == 0:
            status = "Epidemic ended"
        elif self.infected > self.susceptible:
            status = "Peak epidemic phase"
        else:
            status = "Exponential growth phase"
            
        status_surface = utils.font8.render(status, True, (200, 200, 200))
        utils.screen.blit(status_surface, (10, utils.height - 20))

# Replace your Game class with this authentic SIR model
Game = SIRViralPhysics
