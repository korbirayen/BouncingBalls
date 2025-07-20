import pygame
from pygame import Vector2
from Ball import Ball
from particle import Explosion
from ring import Ring
from sounds import Sounds
from utils.util import utils

class Game:
    def __init__(self):
        self.balls = []
        self.time = 5

        self.rings = [
            Ring(250, 1),
        ]

        initial_ball_color = self.rings[0].color
        self.ball = Ball(Vector2(utils.width / 2, utils.height / 4), 2, self.time)
        self.balls.append(self.ball)
        self.particles = []
        self.collide = False
        self.waitTime = 0
        self.sounds = Sounds()

    def update(self):
        utils.world.Step(1.0 / 60.0, 6, 2)

        if self.ball.destroyFlag:
            self.ball.convertToStatic()
            self.time += 0
            new_ball_color = self.rings[0].color
            self.ball = Ball(Vector2(utils.width / 2, utils.height / 4), 2, self.time)
            self.balls.append(self.ball)
        for ring in self.rings:
            ring.update()
            for ball in self.balls:
                ball.update_color()
        if utils.contactListener.collisions:
            self.sounds.play()
            for bodyA, bodyB, point in utils.contactListener.collisions:
                pos = utils.to_Pos(point)
                self.particles.append(Explosion(pos[0], pos[1], (255, 255, 255)))
                if bodyA.userData == self.ball:
                    if isinstance(bodyB.userData, Ball):
                        bodyB.userData.startShaking()
                if bodyB.userData == self.ball:
                    if isinstance(bodyA.userData, Ball):
                        bodyA.userData.startShaking()
                break
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
