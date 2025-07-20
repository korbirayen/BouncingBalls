import math

import pygame
from Box2D import b2TestOverlap
from pygame import Vector2

from Ball import Ball
from BallBox import BallBox
from Box import Box
from Polygon import Polygon
from SquareRing import SquareRing
from particle import Explosion
from ring import Ring
from sounds import Sounds
from util import utils


class Game:
    def __init__(self):
        self.balls = []
        # self.balls.append()
        self.balls.append(BallBox(Vector2(utils.width / 2, utils.height / 2 - 199)))
        self.particles = []
        self.boxes = []
        self.ring = SquareRing(utils.width-100,(207, 52, 235))
        # for ring in self.rings:
        #     self.boxes += ring.boxes

        self.collide = False
        self.waitTime = 0
        self.sounds = Sounds()
        self.complete = False


    def update(self):
        self.ring.update()
        for ball in self.balls:
            ball.color = self.ring.color
            if not ball.spawn and ball.deathTime <= 0:
                self.balls.append(BallBox(Vector2(utils.width / 2, utils.height / 2 - 199)))
                ball.spawn = True

        utils.world.Step(1.0 / 60.0, 6, 2)
        if utils.contactListener.collisions:
            for bodyA, bodyB in utils.contactListener.collisions:
                ballBody = bodyA
                if isinstance(bodyB.userData,Ball):
                    ballBody = bodyB
                self.sounds.play()
                break
            utils.contactListener.collisions = []


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

    def check_collision(self,ball, box):
        ballPos = utils.to_Pos(ball.circle_body.position)
        boxPos = utils.to_Pos(box.box_body.position)
        # print(ballPos,boxPos)

        if utils.distance(ballPos[0],ballPos[1],boxPos[0],boxPos[1]) < 67 :
            return True
        return False