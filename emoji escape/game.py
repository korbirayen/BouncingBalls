import math
import random
import pygame
from pygame import Vector2

from Ball import Ball
from Trapezium import Trapezium
from sounds import Sounds
from util import utils

class Game:
    def __init__(self):
        # Load individual images from the assets folder
        self.images = [
            pygame.image.load("assets/moo2.png").convert_alpha(),
            # Add more images if needed
        ]
        
        self.radius = 2
        # The first ball will have an initial velocity of (0, 0)
        self.balls = [
            Ball(Vector2(utils.width / 2 - 60, -50), random.choice(self.images), self.radius, initial=True)
        ]
        self.particles = []
        self.boxes = []
        self.shapes = [
            Trapezium([
                (-200, 205),
                (8, 0),
                (-200, 200),
                (8, 2)
            ], Vector2(utils.width / 2 - 135, 700)),
            Trapezium([
                (200, 205),
                (-8, 0),
                (200, 200),
                (-8, 2)
            ], Vector2(utils.width / 2 + 135, 700))
        ]

        self.collide = False
        self.waitTime = 0
        self.sounds = Sounds()
        self.complete = False
        self.count = 0
        self.despawn_counter = 0  # Counter for despawned balls

        # Load the stationary image from assets
        self.stationary_image = pygame.image.load("assets/moo1.png").convert_alpha()
        self.stationary_image_position = (utils.width / 2 - self.stationary_image.get_width() / 2, 650)

        # Font for displaying ball count and despawn counter
        self.font = pygame.font.Font(None, 50)

    def update(self):
        for ball in self.balls:
            if ball.getPos().y > utils.height + 50:
                ball.destroyFlag = True
                # Spawn two new balls when one falls off the screen
                self.balls.append(Ball(Vector2(utils.width / 2 - 60, -50), random.choice(self.images), self.radius))
                self.balls.append(Ball(Vector2(utils.width / 2 + 62, -50), random.choice(self.images), self.radius))
                self.balls.append(Ball(Vector2(utils.width / 2, -50), random.choice(self.images), self.radius))

                # Play the escape sound when new balls are spawned
                self.sounds.play_escape_sound()

        for ball in self.balls:
            if ball.destroyFlag:
                utils.world.DestroyBody(ball.circle_body)
                self.balls.remove(ball)
                self.despawn_counter += 1  # Increment the despawn counter

        utils.world.Step(1.0 / 60.0, 6, 2)
        if utils.contactListener.collisions:
            self.sounds.play()
            utils.contactListener.collisions = []

        for exp in self.particles:
            if exp.boxes[0].x < -200 or exp.boxes[0].y < -200 or exp.boxes[0].x > \
                    utils.width + 200 or exp.boxes[0].y > utils.height + 200:
                self.particles.remove(exp)

    def draw(self):
        # Draw the stationary image on the screen
        utils.screen.blit(self.stationary_image, self.stationary_image_position)

        # Draw shapes and balls
        for shape in self.shapes:
            shape.draw()
        for ball in self.balls:
            ball.draw()

        for exp in self.particles:
            exp.draw()

        # Draw the ball counter on the screen showing the actual number of balls
        ball_count = len(self.balls)
        ball_count_text = self.font.render(f"Milk: {ball_count}", True, (255, 255, 255))
        utils.screen.blit(ball_count_text, (252.5, 750))
