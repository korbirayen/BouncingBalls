import math
import pygame
from Box2D import b2TestOverlap
from pygame import Vector2

from Ball import Ball
from Box import Box
from Car import Car
from CarRing import CarRing
from Net import Net
from Trapezium import Trapezium
from particle import Explosion
from ring import Ring
from sounds import Sounds
from util import utils


class Game:
    def __init__(self):
        self.balls = []
        self.balls.append(Ball(Vector2(utils.width / 2, utils.height / 2 - 100), 2, (255, 23, 23)))

        self.cars = [
            Car('red', Vector2(utils.width / 2 + 100, utils.height / 7), 3.5),
            Car('blue', Vector2(utils.width / 2 - 100, utils.height / 7), 3.5),
        ]

        self.particles = []
        self.rings = [
            Ring(250, 1),
            CarRing(250, 1)
        ]
        self.collide = False
        self.waitTime = 0
        self.sounds = Sounds()

        self.redNet = Net('red', Vector2(0, 1), 330 + (360 - 330) / 2)
        self.blueNet = Net('blue', Vector2(0, 1), ((180 - 30) + (180)) / 2)

        self.teamRedScore = 0
        self.teamBlueScore = 0

        # Timer variables
        self.start_time = pygame.time.get_ticks()
        self.time_limit = 45000  # 30 seconds in milliseconds
        self.time_remaining = self.time_limit

    def update(self):
        utils.world.Step(1.0 / 60.0, 6, 2)

        # Update the timer
        elapsed_time = pygame.time.get_ticks() - self.start_time
        self.time_remaining = max(self.time_limit - elapsed_time, 0)

        for ball in self.balls:
            if utils.collide(self.redNet, ball):
                d = utils.distance(ball.getPos().x, ball.getPos().y, utils.width / 2, utils.height / 2)
                if d > 250 - ball.radius * 10 + 30:
                    self.balls.append(Ball(Vector2(utils.width / 2, utils.height / 2 - 100), 2, (255, 23, 23)))
                    utils.world.DestroyBody(ball.circle_body)
                    self.balls.remove(ball)
                    self.sounds.playGoalSound()
                    self.teamBlueScore += 1

            if utils.collide(self.blueNet, ball):
                d = utils.distance(ball.getPos().x, ball.getPos().y, utils.width / 2, utils.height / 2)
                if d > 250 - ball.radius * 10 + 30:
                    self.balls.append(Ball(Vector2(utils.width / 2, utils.height / 2 - 100), 2, (255, 23, 23)))
                    utils.world.DestroyBody(ball.circle_body)
                    self.balls.remove(ball)
                    self.sounds.playGoalSound()
                    self.teamRedScore += 1

        self.redNet.update()
        self.blueNet.update()

        for ring in self.rings:
            ring.update()

        for exp in self.particles:
            exp.update()
            if len(exp.particles) == 0:
                self.particles.remove(exp)

    def draw(self):
        for ring in self.rings:
            ring.draw()

        for ball in self.balls:
            ball.draw()

        for car in self.cars:
            car.draw()

        text = "USA: " + str(self.teamRedScore)
        utils.drawText(Vector2(80, 535), text, (0, 0, 255), utils.font24)
        text = "CA: " + str(self.teamBlueScore)
        tw = utils.font24.render(text, True, (255, 255, 255)).get_width()
        utils.drawText(Vector2(370, 535), text, (255, 0, 0), utils.font24)

        # Draw the countdown timer
        time_text = f" {math.ceil(self.time_remaining / 1000)}"
        utils.drawText(Vector2(215, 515), time_text, (255, 255, 255), utils.font16)

        self.redNet.draw()
        self.blueNet.draw()

        for exp in self.particles:
            exp.draw()
