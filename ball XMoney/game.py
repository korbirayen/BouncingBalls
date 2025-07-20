import math
import random

import pygame
from Box2D import b2TestOverlap
from pygame import Vector2

from Ball import Ball
from Box import Box
from Line import Line
from Star import Star
from StaticBall import StaticBall
from particle import Explosion
from ring import Ring
from sounds import Sounds
from util import utils


class Game:
    def __init__(self):
        self.balls = []
        self.particles = []
        self.sounds = Sounds()
        self.i = 0
        self.ring = Ring()

        for i in range(1):
            ball = Ball("assets/3.png", Vector2(utils.width / 2, 220), 1.0, utils.hueToRGB(random.uniform(0, 1)))
            self.balls.append(ball)

        self.ball = self.balls[0]

        self.createStaticBalls()

        self.money = 100

        # Countdown timer
        self.timer_start = 60  # Start from 60 seconds
        self.time_left = self.timer_start
        self.last_update_time = pygame.time.get_ticks()  # Get the initial time

    def createStaticBalls(self):
        rows = 8
        width = self.ring.getWidth()
        spacing = 50
        startX = 50
        startY = 200
        for row in range(rows):
            balls_in_row = row + 1
            x_offset = (width // 2) - (balls_in_row * spacing // 2)
            y = spacing + row * spacing
            for col in range(balls_in_row):
                x = x_offset + col * spacing
                ball = StaticBall("assets/3.png", Vector2(25 + startX + x, 0 + startY + y), 0.7, (255, 233, 233))
                self.balls.append(ball)

        utils.world.DestroyBody(self.balls[1].circle_body)
        self.balls.remove(self.balls[1])

    def update(self):
        # Update the countdown timer
        current_time = pygame.time.get_ticks()
        if current_time - self.last_update_time >= 1000:  # 1 second has passed
            self.time_left -= 1
            self.last_update_time = current_time

        if self.time_left <= 0:
            self.time_left = 0  # Prevent the timer from going below 0

        if self.i >= 360:
            i = 360
        utils.world.Step(1.0 / 60.0, 6, 2)

        for exp in self.particles:
            exp.update()
            if len(exp.particles) == 0:
                self.particles.remove(exp)

        for ball in self.balls:
            if ball.getPos().y > utils.height:
                utils.world.DestroyBody(ball.circle_body)
                self.balls.remove(ball)

        if utils.contactListener.beginCollisions:
            self.sounds.play()
            utils.contactListener.beginCollisions = []

        for net in self.ring.nets:
            if utils.collide(net, self.ball):
                self.money *= net.xPercent
                utils.world.DestroyBody(self.ball.circle_body)
                ball = Ball("assets/3.png", Vector2(utils.width / 2, 220), 1.0, utils.hueToRGB(random.uniform(0, 1)))
                self.balls.append(ball)
                self.ball = ball

    def draw(self):
        self.ring.draw()

        for ball in self.balls:
            ball.draw()

        for exp in self.particles:
            exp.draw()

        # Draw the money display
        text = "" + str(round(self.money, 2)) + "$"
        tw, th = utils.font24.render(text, True, (233, 233, 233)).get_size()
        utils.drawText(Vector2(350, 710), text, (255, 233, 255), utils.font24)

        # Draw the countdown timer
        timer_text = f"{self.time_left}"
        timer_tw, timer_th = utils.font24.render(timer_text, True, (233, 233, 233)).get_size()
        utils.drawText(Vector2(150, 710), timer_text, (255, 255, 255), utils.font24)
