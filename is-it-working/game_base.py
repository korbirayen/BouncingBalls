import math

import pygame
from Box2D import b2TestOverlap
from pygame import Vector2

from Ball import Ball
from Box import Box
from particle import Explosion
from ring import Ring
from sounds import Sounds
from util import utils


class Game:
    def __init__(self):
        self.balls = [
            Ball(Vector2(utils.width / 2 + 65, utils.height / 4),Vector2(50,500),
                 radius=3, color=(255, 0, 0)),
            Ball(Vector2(utils.width / 2 - 65, utils.height / 4),Vector2(50,520),
                 radius=3, color=(0, 255, 0)),
            Ball(Vector2(utils.width / 2, utils.height / 4),  Vector2(50,540),
                 radius=3, color=(0, 0, 255)),

        ]
        self.particles = []
        self.rings = [
            Ring(Vector2(utils.width/2,utils.height/2 - 60),220,1),
        ]
        self.collide = False
        self.waitTime = 0
        self.sounds = Sounds()

        self.increaseRadiusTime = 0


    def update(self):
        utils.world.Step(1.5 / 60.0, 6, 2)

        if len(self.balls) == 1:
            self.increaseRadiusTime += utils.deltaTime()
            if self.increaseRadiusTime >= 0.05:
                if self.balls[0].radius < 200/10:
                    self.balls[0].setRadius( self.balls[0].radius * 1.1)


        for ring in self.rings:
            ring.update()
        if utils.contactListener.collisions:
            self.sounds.play()
            for bodyA, bodyB,point in utils.contactListener.collisions:
                utils.contactListener.collisions = []
                pos = utils.to_Pos(point)
                self.particles.append(Explosion(pos[0],pos[1],bodyA.userData.color,bodyB.userData.color))

                bodyA.userData.setRadius(bodyA.userData.radius * 0.92)
                bodyB.userData.setRadius(bodyB.userData.radius * 0.92)

                break

        for ball in self.balls:
            if ball.radius < 0.5:
                utils.world.DestroyBody(ball.circle_body)
                self.balls.remove(ball)

        for exp in self.particles:
            exp.update()
            if len(exp.particles) == 0:
                self.particles.remove(exp)

        # for box in self.boxes:
        #     if box.destroyFlag:
        #         utils.world.DestroyBody(box.box_body)
        #         self.boxes.remove(box)

    def draw(self):
        for ring in self.rings:
            ring.draw()
        for ball in self.balls:
            ball.draw()

        for exp in self.particles:
            exp.draw()

