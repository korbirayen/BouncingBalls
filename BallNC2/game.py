import pygame
from pygame import Vector2
from Ball import Ball
from ring import Ring
from sounds import Sounds
from util import utils

class Game:
    def __init__(self):
        self.balls = []
        self.balls.append(Ball(Vector2(utils.width / 2 - 150, utils.height / 4), 1.5, 'china.png', team='biden'))
        self.balls.append(Ball(Vector2(utils.width / 2 + 150, utils.height / 4), 1.5, 'usa.png', team='trump'))
        self.particles = []
        self.ring = Ring(250)
        self.ring2 = Ring(250)
        self.collide = False
        self.waitTime = 0
        self.sounds = Sounds()

        # Initialize counters for each team
        self.biden_counter = 0  # Counter for Biden team
        self.trump_counter = 0  # Counter for Trump team

    def update(self):
        utils.world.Step(1.0 / 60.0, 6, 2)

        balls_to_remove = []  # To collect balls that need to be removed

        for ball in self.balls:
            # Check if ball is within screen bounds
            if 0 <= ball.getPos().x <= utils.width and 0 <= ball.getPos().y <= utils.height:
                # Ball is within bounds, no action needed
                pass
            else:
                # Ball has escaped, replace with two new balls
                radius = (ball.radius / 100) * 100
                if ball.team == 'biden':
                    self.biden_counter += 1  # Increment Biden's counter
                    new_ball1 = Ball(Vector2(utils.width / 2 - 50, utils.height / 4), radius, ball.image_path, team='biden')
                    new_ball2 = Ball(Vector2(utils.width / 2 - 100, utils.height / 4), radius, ball.image_path, team='biden')
                elif ball.team == 'trump':
                    self.trump_counter += 1  # Increment Trump's counter
                    new_ball1 = Ball(Vector2(utils.width / 2 + 50, utils.height / 4), radius, ball.image_path, team='trump')
                    new_ball2 = Ball(Vector2(utils.width / 2 + 100, utils.height / 4), radius, ball.image_path, team='trump')

                self.balls.append(new_ball1)
                self.balls.append(new_ball2)
                balls_to_remove.append(ball)

        # Remove the balls that have escaped
        for ball in balls_to_remove:
            self.balls.remove(ball)

        # Update the rings
        self.ring.update()
        if utils.contactListener.collisions:
            self.sounds.play()
            utils.contactListener.collisions = []

        self.ring2.update()
        if utils.contactListener.collisions:
            self.sounds.play()
            utils.contactListener.collisions = []

        # Update and remove particles
        for exp in self.particles:
            exp.update()
            if len(exp.particles) == 0:
                self.particles.remove(exp)

    def draw(self):
        self.ring.draw()
        for ball in self.balls:
            ball.draw()

        for exp in self.particles:
            exp.draw()

        # Draw counters
        utils.drawText(Vector2(350, 565), f"Lois: {self.biden_counter}", (0, 0, 0), utils.font8)
        utils.drawText(Vector2(150, 565), f"Stewie: {self.trump_counter}", (0, 0, 0), utils.font8)

    def get_biden_counter(self):
        return self.biden_counter

    def get_trump_counter(self):
        return self.trump_counter
