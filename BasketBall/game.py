import pygame
from pygame import Vector2
from Ball import Ball
from Box import Box
from particle import Explosion
from ring import Ring
from sounds import Sounds
from util import utils

class Game:
    def __init__(self):
        self.balls = []
        self.balls.append(Ball(Vector2(utils.width / 2 - 50, utils.height / 4), 1.5, (255, 23, 23)))
        self.particles = []
        self.rings = [Ring(250, 1)]
        self.collide = False
        self.waitTime = 0
        self.sounds = Sounds()

    def update(self):
        utils.world.Step(1.0 / 60.0, 6, 2)

        for ball in self.balls:
            if utils.distance(ball.getPos().x, ball.getPos().y, utils.width / 2, utils.height / 2) > self.rings[0].radius + 48:
                radius = (ball.radius / 100) * 100
                self.balls.append(Ball(Vector2(utils.width / 2 + 60, utils.height / 4), radius, (233, 23, 23)))
                self.balls.append(Ball(Vector2(utils.width / 2 - 60, utils.height / 4), radius, (233, 233, 23)))
                self.balls.remove(ball)
                self.sounds.playGoalSound()

        for ring in self.rings:
            ring.update()
        
        if utils.contactListener.collisions:
            self.sounds.play()
            for bodyA, bodyB in utils.contactListener.collisions:
                if isinstance(bodyA.userData, Ball):
                    bodyA.userData.bounce()
                if isinstance(bodyB.userData, Ball):
                    bodyB.userData.bounce()
            utils.contactListener.collisions = []

        for exp in self.particles:
            exp.update()
            if len(exp.particles) == 0:
                self.particles.remove(exp)

    def draw(self):
        for ring in self.rings:
            ring.draw()
        for ball in self.balls:
            ball.draw()

        for exp in self.particles:
            exp.draw()
