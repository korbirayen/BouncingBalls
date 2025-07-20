import math
import random

import pygame
from Box2D import b2TestOverlap
from pygame import Vector2

from Ball import Ball
from Box import Box
from CirclePiece import CirclePiece
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
        # To access the polygon name for any size
        # Example: polygon with 3 sides

        for i in range(1):
            ball = Ball("assets/3.png",Vector2(utils.width/2 + 10 ,utils.height/2 - 80 ),2.0,(255,255,255))
            self.balls.append(ball)

        self.size = 3
        self.ring = Ring()


    def update(self):
        if self.i >= 360:
            i = 360
        utils.world.Step(1.0 / 60.0, 6, 2)

        for exp in self.particles:
            exp.update()
            if len(exp.particles) == 0:
                self.particles.remove(exp)

        self.ring.update()

        for ball in self.balls:
            if ball.getPos().y > utils.height:
                utils.world.DestroyBody(ball.circle_body)
                self.balls.remove(ball)

        if utils.contactListener.endCollisions:
            for bodyA,bodyB,point in utils.contactListener.endCollisions:
                body = bodyA
                if isinstance(bodyB.userData,CirclePiece):
                    body = bodyB

                piece = body.userData
                self.sounds.play_at(piece.id)
                piece.startMovingBack()
                # piece.body.linearVelocity = (0,0)

            utils.contactListener.endCollisions = []


    def draw(self):

        self.ring.draw()
        for ball in self.balls:
            ball.draw()


        for exp in self.particles:
            exp.draw()
        #


