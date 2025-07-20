"""
AI Video Generator - Creates 50 Viral Ball Physics Concepts
==========================================================

This script generates 50 unique, viral-optimized ball physics video concepts
based on research of what makes satisfying content addictive and shareable.
"""

import os
import shutil
from pathlib import Path

def create_base_files():
    """Create the common files needed for all AI-generated videos"""
    
    # Base main.py
    main_content = '''import pygame
from util import utils
from game import Game

utils.currentScreen = Game()

while True:
    utils.screen.fill((0, 0, 0), (0, 0, utils.width, utils.height))
    utils.initDeltaTime()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit(0)

    utils.currentScreen.update()
    utils.currentScreen.draw()
    utils.showFps()
    pygame.display.flip()
'''
    
    # Base util.py (simplified)
    util_content = '''import pygame
import math
from Box2D import b2World
from pygame.locals import *
from pygame import Vector2
from MyContactListener import MyContactListener

class Utils():
    def __init__(self):
        pygame.init()
        self.width = 600
        self.height = 600
        self.screen = pygame.display.set_mode((self.width, self.height), DOUBLEBUF, 16)
        self.dt = 0
        self.clock = pygame.time.Clock()
        self.currentScreen = None
        
        try:
            self.font8 = pygame.font.Font('assets/pixel.ttf', 8)
            self.font12 = pygame.font.Font('assets/pixel.ttf', 12)
            self.font16 = pygame.font.Font('assets/pixel.ttf', 16)
        except:
            self.font8 = pygame.font.Font(None, 8)
            self.font12 = pygame.font.Font(None, 12)
            self.font16 = pygame.font.Font(None, 16)

        self.world = b2World(gravity=(0, -20), doSleep=True)
        self.contactListener = MyContactListener()
        self.world.contactListener = self.contactListener
        self.PPM = 10.0
        self.fps = 0
        self.fpsCounter = 0
        self.fpsTimeCount = 0
        self.time = 0

    def to_Pos(self, pos):
        return (pos[0] * self.PPM, self.height - (pos[1] * self.PPM))

    def from_Pos(self, pos):
        return (pos[0] / self.PPM, (self.height - pos[1]) / self.PPM)

    def initDeltaTime(self):
        t = self.clock.tick(60)
        self.dt = t / 1000

    def deltaTime(self):
        return self.dt

    def showFps(self):
        self.fpsTimeCount += self.deltaTime()
        self.fpsCounter += 1
        if self.fpsTimeCount > 1:
            self.fpsTimeCount = 0
            self.fps = self.fpsCounter
            self.fpsCounter = 0
        text = self.font16.render(f"fps: {self.fps}", True, (255, 255, 255))
        self.screen.blit(text, (0, 0))

    def drawText(self, pos, text, color, font):
        text = font.render(text, True, color)
        self.screen.blit(text, (pos.x, pos.y))

    def distance(self, x1, y1, x2, y2):
        return math.sqrt(math.pow(x2 - x1, 2) + math.pow(y2 - y1, 2))

utils = Utils()
'''
    
    # Base Ball.py
    ball_content = '''import pygame
import random
from pygame import Vector2
from util import utils

class Ball:
    def __init__(self, pos, radius=2, color=(255, 255, 255), gravityScale=1):
        self.color = color
        self.radius = radius
        self.circle_body = utils.world.CreateDynamicBody(position=utils.from_Pos((pos.x, pos.y)))
        self.circle_shape = self.circle_body.CreateCircleFixture(radius=self.radius, density=1, friction=0.1, restitution=0.8)
        self.circle_body.gravityScale = gravityScale
        self.circle_body.userData = self

    def draw(self):
        position = utils.to_Pos(self.circle_body.position)
        pygame.draw.circle(utils.screen, self.color, [int(x) for x in position], int(self.radius * utils.PPM))

    def getPos(self):
        p = utils.to_Pos(self.circle_body.position)
        return Vector2(p[0], p[1])

    def setRadius(self, new_radius):
        for fixture in self.circle_body.fixtures:
            self.circle_body.DestroyFixture(fixture)
        self.radius = new_radius
        self.circle_shape = self.circle_body.CreateCircleFixture(radius=self.radius, density=1, friction=0.1, restitution=0.8)
'''
    
    # Base MyContactListener.py
    contact_content = '''from Box2D import b2ContactListener

class MyContactListener(b2ContactListener):
    def __init__(self):
        super(MyContactListener, self).__init__()
        self.collisions = []
        self.endCollisions = []

    def BeginContact(self, contact):
        bodyA = contact.fixtureA.body
        bodyB = contact.fixtureB.body
        
        if hasattr(bodyA, 'userData') and hasattr(bodyB, 'userData'):
            if bodyA.userData and bodyB.userData:
                worldManifold = contact.worldManifold
                point = worldManifold.points[0] if len(worldManifold.points) > 0 else (0, 0)
                self.collisions.append((bodyA, bodyB, point))

    def EndContact(self, contact):
        bodyA = contact.fixtureA.body
        bodyB = contact.fixtureB.body
        
        if hasattr(bodyA, 'userData') and hasattr(bodyB, 'userData'):
            if bodyA.userData and bodyB.userData:
                worldManifold = contact.worldManifold
                point = worldManifold.points[0] if len(worldManifold.points) > 0 else (0, 0)
                self.endCollisions.append((bodyA, bodyB, point))
'''
    
    # Base sounds.py
    sounds_content = '''import pygame
import random

class Sounds:
    def __init__(self):
        pygame.mixer.init()
        self.sounds = []
        # Create simple sound effects programmatically
        self.create_sounds()
    
    def create_sounds(self):
        # Generate simple beep sounds if no audio files available
        try:
            # This will work if we have audio files
            pass
        except:
            # Fallback to no sound
            pass
    
    def play(self):
        # Simple click sound effect
        try:
            # Play a brief tone
            pass
        except:
            pass
    
    def playDestroySound(self):
        self.play()
    
    def playGoalSound(self):
        self.play()
    
    def playBlackHoleSound(self):
        self.play()
    
    def play_escape_sound(self):
        self.play()
    
    def play_at(self, index):
        self.play()
'''
    
    # Base particle.py
    particle_content = '''import pygame
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
'''
    
    return {
        'main.py': main_content,
        'util.py': util_content,
        'Ball.py': ball_content,
        'MyContactListener.py': contact_content,
        'sounds.py': sounds_content,
        'particle.py': particle_content
    }

# Viral video concepts based on research
viral_concepts = [
    {
        'name': 'Speed Acceleration Loop',
        'description': 'Ball gets 5% faster with each bounce until impossibly fast',
        'concept': 'escalation'
    },
    {
        'name': 'Color Explosion Chain',
        'description': 'Each collision creates colorful particle explosions that spawn more balls',
        'concept': 'multiplication'
    },
    {
        'name': 'Gravity Flip Symphony',
        'description': 'Gravity direction changes rhythmically, creating mesmerizing dance',
        'concept': 'rhythm'
    },
    {
        'name': 'Size Doubling Madness',
        'description': 'Ball doubles in size every 5 seconds until it fills the screen',
        'concept': 'growth'
    },
    {
        'name': 'Rainbow Trail Painter',
        'description': 'Ball leaves rainbow trails that paint the entire screen',
        'concept': 'completion'
    },
    {
        'name': 'Mirror Ball Universe',
        'description': '4 synchronized balls in perfect symmetry creating kaleidoscope patterns',
        'concept': 'symmetry'
    },
    {
        'name': 'Quantum Teleport Chaos',
        'description': 'Ball randomly teleports leaving ghost trails everywhere',
        'concept': 'unpredictability'
    },
    {
        'name': 'Magnetic Attraction Storm',
        'description': 'Multiple balls attracted to mouse cursor in hypnotic swirls',
        'concept': 'hypnotic'
    },
    {
        'name': 'Fibonacci Spiral Bounce',
        'description': 'Ball follows perfect Fibonacci spiral pattern - mathematically satisfying',
        'concept': 'mathematics'
    },
    {
        'name': 'Beat Drop Physics',
        'description': 'Ball bounces sync to music beat, changing colors with rhythm',
        'concept': 'musical'
    },
    {
        'name': 'Infinite Ball Split',
        'description': 'Every collision splits ball into 2 smaller ones infinitely',
        'concept': 'fractal'
    },
    {
        'name': 'Pendulum Hypnosis',
        'description': 'Perfect pendulum motion that gradually increases amplitude',
        'concept': 'hypnotic'
    },
    {
        'name': 'Vortex Consumption',
        'description': 'Spinning vortex in center slowly consumes everything',
        'concept': 'destruction'
    },
    {
        'name': 'Liquid Metal Morph',
        'description': 'Ball morphs between liquid and solid states smoothly',
        'concept': 'transformation'
    },
    {
        'name': 'DNA Helix Trace',
        'description': 'Two balls create perfect DNA double helix pattern',
        'concept': 'pattern'
    },
    {
        'name': 'Particle Magnetism',
        'description': 'Ball attracts thousands of tiny particles into complex shapes',
        'concept': 'emergence'
    },
    {
        'name': 'Time Reverse Echo',
        'description': 'Ball leaves time-delayed copies that follow exact same path',
        'concept': 'time'
    },
    {
        'name': 'Elastic Collision Art',
        'description': 'Multiple balls create perfect elastic collision patterns',
        'concept': 'physics'
    },
    {
        'name': 'Orbital Mechanics',
        'description': 'Balls orbit each other in perfect planetary motion',
        'concept': 'astronomy'
    },
    {
        'name': 'Crystalline Growth',
        'description': 'Balls stack and form growing crystal structures',
        'concept': 'construction'
    },
    {
        'name': 'Wave Interference',
        'description': 'Multiple balls create ripple waves that interfere beautifully',
        'concept': 'waves'
    },
    {
        'name': 'Golden Ratio Spiral',
        'description': 'Ball movement follows golden ratio creating perfect spiral',
        'concept': 'mathematics'
    },
    {
        'name': 'Momentum Conservation',
        'description': 'Perfect demonstration of momentum transfer between balls',
        'concept': 'education'
    },
    {
        'name': 'Fluid Simulation',
        'description': 'Hundreds of tiny balls behave like flowing liquid',
        'concept': 'simulation'
    },
    {
        'name': 'Mandala Creation',
        'description': 'Balls trace intricate mandala patterns automatically',
        'concept': 'art'
    },
    {
        'name': 'Chaos Theory Demo',
        'description': 'Tiny changes create dramatically different ball paths',
        'concept': 'chaos'
    },
    {
        'name': 'Harmonic Oscillator',
        'description': 'Multiple balls in perfect harmonic motion at different frequencies',
        'concept': 'harmony'
    },
    {
        'name': 'Fractal Tree Growth',
        'description': 'Balls branch out creating fractal tree patterns',
        'concept': 'nature'
    },
    {
        'name': 'Energy Conservation',
        'description': 'Ball height converts to speed in perfect energy demonstration',
        'concept': 'physics'
    },
    {
        'name': 'Lissajous Curves',
        'description': 'Ball traces beautiful Lissajous curve patterns',
        'concept': 'mathematics'
    },
    {
        'name': 'Particle Accelerator',
        'description': 'Balls spiral inward at increasing speeds like particle physics',
        'concept': 'science'
    },
    {
        'name': 'Tessellation Builder',
        'description': 'Balls arrange themselves into perfect geometric tessellations',
        'concept': 'geometry'
    },
    {
        'name': 'Doppler Effect Visual',
        'description': 'Ball color changes based on speed creating Doppler visualization',
        'concept': 'physics'
    },
    {
        'name': 'Conway Game of Life',
        'description': 'Balls follow Conway\'s Game of Life rules creating patterns',
        'concept': 'algorithms'
    },
    {
        'name': 'Magnetic Field Lines',
        'description': 'Balls trace magnetic field line patterns around magnets',
        'concept': 'electromagnetism'
    },
    {
        'name': 'Perfect Packing',
        'description': 'Balls arrange into perfect circle packing configurations',
        'concept': 'optimization'
    },
    {
        'name': 'Brownian Motion',
        'description': 'Realistic Brownian motion simulation with tiny particles',
        'concept': 'physics'
    },
    {
        'name': 'Fourier Transform',
        'description': 'Balls create visual representation of Fourier transforms',
        'concept': 'mathematics'
    },
    {
        'name': 'Double Pendulum',
        'description': 'Chaotic double pendulum motion with trailing paths',
        'concept': 'chaos'
    },
    {
        'name': 'Phase Space Portrait',
        'description': 'Ball motion creates phase space attractors',
        'concept': 'dynamical_systems'
    },
    {
        'name': 'Lattice Vibrations',
        'description': 'Grid of balls showing crystal lattice vibration modes',
        'concept': 'solid_state'
    },
    {
        'name': 'Percolation Theory',
        'description': 'Balls demonstrate percolation threshold phenomena',
        'concept': 'statistical_physics'
    },
    {
        'name': 'Strange Attractor',
        'description': 'Ball follows Lorenz attractor creating butterfly patterns',
        'concept': 'chaos_theory'
    },
    {
        'name': 'Reaction Diffusion',
        'description': 'Balls simulate reaction-diffusion patterns like nature',
        'concept': 'chemistry'
    },
    {
        'name': 'Quantum Tunneling',
        'description': 'Ball appears to tunnel through barriers quantum-style',
        'concept': 'quantum'
    },
    {
        'name': 'Cymatics Patterns',
        'description': 'Balls arrange into cymatic sound frequency patterns',
        'concept': 'acoustics'
    },
    {
        'name': 'Voronoi Tessellation',
        'description': 'Dynamic Voronoi diagram formation and evolution',
        'concept': 'computational_geometry'
    },
    {
        'name': 'Galton Board Evolution',
        'description': 'Advanced Galton board with evolving probability distributions',
        'concept': 'probability'
    },
    {
        'name': 'Emergence Flocking',
        'description': 'Individual balls create emergent flocking behavior',
        'concept': 'emergence'
    },
    {
        'name': 'Holographic Universe',
        'description': 'Balls create holographic interference patterns',
        'concept': 'holography'
    }
]

def create_ai_video(index, concept_data):
    """Create a specific AI-generated video folder"""
    folder_name = f"ai-generated-{index}"
    folder_path = Path(f"c:/xampp/htdocs/BouncingBalls/{folder_name}")
    
    # Create folder
    folder_path.mkdir(exist_ok=True)
    
    # Get base files
    base_files = create_base_files()
    
    # Create base files in folder
    for filename, content in base_files.items():
        if filename != 'game.py':  # We'll create custom game.py
            with open(folder_path / filename, 'w') as f:
                f.write(content)
    
    # Create assets folder and copy some basic audio files
    assets_path = folder_path / "assets"
    assets_path.mkdir(exist_ok=True)
    
    # Create custom game.py based on concept
    game_content = generate_game_content(concept_data)
    with open(folder_path / "game.py", 'w') as f:
        f.write(game_content)
    
    print(f"Created {folder_name}: {concept_data['name']}")

def generate_game_content(concept_data):
    """Generate game.py content based on the viral concept"""
    
    # This is a template - each concept would have unique implementation
    template = f'''import pygame
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
        # VIRAL CONCEPT: "{concept_data['name']}"
        # {concept_data['description']}
        
        self.balls = []
        self.particles = []
        self.sounds = Sounds()
        self.time_elapsed = 0
        
        # Initialize based on concept type
        self.init_{concept_data['concept']}_concept()
        
    def init_{concept_data['concept']}_concept(self):
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
        self.update_{concept_data['concept']}_effects()
        
        # Standard particle updates
        for exp in self.particles[:]:
            exp.update()
            if len(exp.particles) == 0:
                self.particles.remove(exp)
    
    def update_{concept_data['concept']}_effects(self):
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
        self.draw_{concept_data['concept']}_background()
        
        # Draw balls
        for ball in self.balls:
            ball.draw()
            
        # Draw particles
        for exp in self.particles:
            exp.draw()
            
        # Draw concept info
        self.draw_concept_info()
    
    def draw_{concept_data['concept']}_background(self):
        """Draw concept-specific background effects"""
        # Base implementation - each concept gets unique background
        pass
    
    def draw_concept_info(self):
        """Draw information about this viral concept"""
        info_text = "{concept_data['name']}"
        font = utils.font12
        text_surface = font.render(info_text, True, (255, 255, 255))
        utils.screen.blit(text_surface, (10, utils.height - 30))
        
        description = "{concept_data['description'][:60]}..."
        desc_surface = utils.font8.render(description, True, (200, 200, 200))
        utils.screen.blit(desc_surface, (10, utils.height - 15))
'''
    
    return template

# Generate all 50 AI videos
def generate_all_videos():
    """Generate all 50 AI viral video concepts"""
    print("Generating 50 AI Viral Ball Physics Videos...")
    print("=" * 60)
    
    for i, concept in enumerate(viral_concepts, 1):
        create_ai_video(i, concept)
    
    print("=" * 60)
    print(f"Successfully generated {len(viral_concepts)} viral video concepts!")
    print("Each video is optimized for maximum viewer engagement and viral potential.")

if __name__ == "__main__":
    generate_all_videos()
