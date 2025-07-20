import math
import random

import pygame
from Box2D import b2TestOverlap
from pygame import Vector2

from Ball import Ball
from BlackHole import BlackHole
from Box import Box
from Polygon import Polygon
from particle import Explosion
from ring import Ring
from ring2 import Ring2
from sounds import Sounds
from util import utils


class Game:
    def __init__(self):
        self.balls = [
            Ball(Vector2(utils.width / 2 - 130, utils.height / 4))
        ]
        self.blackHole = BlackHole(Vector2(utils.width/2,utils.height/3.5))
        # self.balls.append()
        self.particles = []
        self.boxes = []
        self.rings = [
            Ring(utils.width/2 - 50, (123,155,166)),
        ]
        # for ring in self.rings:
        #     self.boxes += ring.boxes

        self.collide = False
        self.waitTime = 0
        self.sounds = Sounds()
        self.complete = False
        self.spawnTimeInterval = 0
        self.spawnTime = 0.5

    def update(self):
        if self.blackHole.radius >= self.rings[0].radius:
            self.blackHole.radius = self.rings[0].radius

        for ring in self.rings:
            ring.update()
            self.blackHoleRingCollision(self.blackHole,ring)
            for ball in self.balls:
                d = utils.distance(ball.pos.x,ball.pos.y,utils.width/2,utils.height/2)
                if d + ball.radius >= ring.radius:
                    # Calculate the normal vector at the collision point
                    circlePos = Vector2(utils.width/2,utils.height/2)
                    normal = ball.pos - circlePos
                    normal = normal.normalize()
                    ball.vel = ball.vel.reflect(normal)

                    # Move the ball out of the collision point to prevent sticking
                    ball.pos = circlePos + normal * (ring.radius - ball.radius)
                    self.sounds.play()
                    if ball.canSpawnTime >= 0.2:
                        ball.canSpawnTime = 0
                        newBall = Ball(Vector2(ball.pos.x - ball.radius,ball.pos.y - ball.radius))
                        self.balls.append(newBall)

        self.blackHole.update()
        for ball in self.balls:
            ball.update()
            if self.check_circle_collision(self.blackHole.pos,self.blackHole.radius,ball.pos,ball.radius):
                ball.destroyFlag = True
                self.blackHole.radius -= self.blackHole.radius/100 * 0
                self.sounds.playBlackHoleSound()

        for ball in self.balls:
            if ball.destroyFlag:
                self.balls.remove(ball)

        for exp in self.particles:
            exp.update()
            if len(exp.particles) == 0:
                self.particles.remove(exp)

    def blackHoleRingCollision(self,ball,ring):
        d = utils.distance(ball.pos.x, ball.pos.y, utils.width / 2, utils.height / 2)
        if d + ball.radius >= ring.radius:
            # Calculate the normal vector at the collision point
            circlePos = Vector2(utils.width / 2, utils.height / 2)
            normal = ball.pos - circlePos
            normal = normal.normalize()
            ball.vel = ball.vel.reflect(normal)
            ball.vel = ball.vel * 1.005
            ball.radius = ball.radius * 1

            # Move the ball out of the collision point to prevent sticking
            ball.pos = circlePos + normal * (ring.radius - ball.radius)

    def check_circle_collision(self,pos1, radius1, pos2, radius2):
        distance = Vector2(pos1).distance_to(pos2)
        return distance <= (radius1 + radius2)

    def draw(self):
        for ring in self.rings:
            ring.draw()
        for ball in self.balls:
            ball.draw()

        self.blackHole.draw()

        utils.drawText(Vector2(220,555),"Emeralds: " + str(len(self.balls)),(255,255,255),utils.font16)

        for exp in self.particles:
            exp.draw()

    def check_collision(self,ball, box):
        ballPos = utils.to_Pos(ball.circle_body.position)
        boxPos = utils.to_Pos(box.box_body.position)
        # print(ballPos,boxPos)

        if utils.distance(ballPos[0],ballPos[1],boxPos[0],boxPos[1]) < 67 :
            return True
        return False