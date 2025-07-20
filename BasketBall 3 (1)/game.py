import math
import pygame
from Box2D import b2TestOverlap
from pygame import Vector2

from Ball import Ball
from Box import Box
from Net import Net
from Trapezium import Trapezium
from particle import Explosion
from ring import Ring
from sounds import Sounds
from util import utils


class Game:
    def __init__(self):
        self.balls = []
        self.balls.append(Ball(Vector2(utils.width / 2 - 20, utils.height / 4), 2, (0, 173, 239)))
        self.particles = []
        self.rings = [
            Ring(250, -1),
        ]
        self.collide = False
        self.waitTime = 0
        self.sounds = Sounds()

        self.net = Net(Vector2(255, 230))

        # Circle parameters
        self.circle_center = Vector2(utils.width / 2, utils.height / 2)
        self.circle_radius = 250
        self.loading_bar_width = 350  # Width of the loading bar
        self.loading_bar_height = 20  # Height of the loading bar
        self.max_balls = 150  # Number of balls needed to fill the bar

        # Counter for balls going through the ring
        self.counter = 0.00  # Start the counter at $1.00

        # Countdown timer
        self.start_time = pygame.time.get_ticks()  # Start time for the countdown
        self.countdown = 60  # Countdown starts from 60 seconds

    def update(self):
        utils.world.Step(1.0 / 60.0, 6, 2)

        # Update the countdown timer
        elapsed_time = (pygame.time.get_ticks() - self.start_time) / 1000  # Time in seconds
        self.countdown = max(60 - int(elapsed_time), 0)  # Countdown from 60 seconds, ensuring it doesn't go below 0

        for ball in self.balls:
            d = utils.distance(ball.getPos().x, ball.getPos().y, utils.width / 2, utils.height / 2)
            if d > 250 - ball.radius * 10 + 30:
                self.balls.append(Ball(Vector2(utils.width / 2 - 78, utils.height / 5), 2, (255, 23, 23)))
                self.balls.append(Ball(Vector2(utils.width / 2 + 82, utils.height / 5), 2, (255, 23, 23)))
                utils.world.DestroyBody(ball.circle_body)
                self.balls.remove(ball)

                self.sounds.playGoalSound()

                # Increment the counter by 1.00
                self.counter += 1.00

        self.net.update()

        for ring in self.rings:
            ring.update()
        if utils.contactListener.collisions:
            self.sounds.play()
            utils.contactListener.collisions = []

        for exp in self.particles:
            exp.update()
            if len(exp.particles) == 0:
                self.particles.remove(exp)

    def count_balls_in_circle(self):
        count = 0
        for ball in self.balls:
            pos = ball.getPos()
            distance = utils.distance(pos.x, pos.y, self.circle_center.x, self.circle_center.y)
            if distance <= self.circle_radius - ball.radius * 10:
                count += 1
        return count

    def draw_loading_bar(self):
        count = self.count_balls_in_circle()
        fill_ratio = min(count / self.max_balls, 1.0)  # Ensure ratio doesn't exceed 1

        # Position of the loading bar on the screen
        bar_x = (utils.width - self.loading_bar_width) / 2
        bar_y = utils.height - 670  # Position it near the bottom of the screen

        # Draw the border of the loading bar
        pygame.draw.rect(utils.screen, (255, 255, 255), (bar_x, bar_y, self.loading_bar_width, self.loading_bar_height), 2)

        # Draw the filled portion of the loading bar
        filled_width = self.loading_bar_width * fill_ratio
        pygame.draw.rect(utils.screen, (255, 255, 0), (bar_x, bar_y, filled_width, self.loading_bar_height))

    def draw_countdown(self):
        font = pygame.font.Font(None, 70)  # Choose the font and size
        countdown_text = font.render(f"{self.countdown}", True, (255, 255, 255))
        utils.screen.blit(countdown_text, (273, 640))  # Position the countdown at the top left

    def draw(self):
        for ring in self.rings:
            ring.draw()

        for ball in self.balls:
            ball.draw()

        self.net.draw()

        for exp in self.particles:
            exp.draw()

        # Draw the countdown timer
        self.draw_countdown()

        # Draw the loading bar
        self.draw_loading_bar()
