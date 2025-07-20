import math
import random

import pygame
from Box2D import b2TestOverlap
from pygame import Vector2

from Ball import Ball
from Line import Line
from RingB import RingB
from particle import Explosion
from sounds import Sounds, sounds
from util import utils


class Game:
    def __init__(self):
        self.balls = []
        # self.balls.append()
        self.balls = [
            Ball(Vector2(utils.width / 2 + 50, 50), 1.2, (23, 255, 255),gravityScale=1),
            Ball(Vector2(utils.width / 2 - 50, 50), 1.2, (255, 255, 23), gravityScale=1),
        ]
        self.walls = [
            Line(Vector2(0,0),Vector2(utils.width,0)),
            Line(Vector2(0, 0), Vector2(0, utils.height)),
            Line(Vector2(utils.width, 0), Vector2(utils.width, utils.height)),
        ]

        self.particles = []
        self.boxes = []

        self.rings = [

        ]
        center = Vector2(utils.width / 2, 50)
        hue = 0
        hueStep = 1/8
        for i in range(8):
            ring = RingB(0, center, 50,self.particles.append, 2, sar=1, hue=hue)
            self.rings.append(ring)
            center.y += 40
            hue += hueStep

        center = Vector2(utils.width / 2, utils.height - 50)
        hue = 0
        hueStep = 1 / 8
        for i in range(8):
            ring = RingB(0, center, 50, self.particles.append, 2, sar=1, hue=hue,isUp=True)
            self.rings.append(ring)
            center.y -= 40
            hue += hueStep


        self.collide = False
        self.waitTime = 0
        self.sounds = Sounds()
        self.complete = False
        self.spawnTimeInterval = 0
        self.spawnTime = 0.5


    def update(self):
        for ball in self.balls:
            if ball.getPos().y >= utils.height - 30:
                return

        utils.world.Step(1.0 / 60.0, 6, 2)
        utils.time += utils.deltaTime()
        if utils.contactListener:
            for bodyA,bodyB in utils.contactListener.collisions:
                body = bodyA
                if isinstance(bodyB.userData,Line):
                    body = bodyB

                body.userData.destroyFlag = True

            utils.contactListener.collisions = []

        for ring in self.rings:
            ring.update()

            # d = utils.distance(self.ball.getPos().x,self.ball.getPos().y,utils.width/2,utils.height/2)
            # if d >= ring.radius*10 :
            #     ring.destroyFlag = True
            #     utils.world.DestroyBody(ring.body)


        for ball in self.balls:
            ball.update()
            # if len(self.rings) > 0:
            #     if not self.rings[0].is_point_in_polygon(ball.getPos(),self.rings[0].points):
            #         self.rings[0].destroyFlag = True
            #         utils.world.DestroyBody(self.rings[0].body)

        for ring in self.rings:
            if ring.destroyFlag:
                self.particles += ring.spawParticles()
                self.rings.remove(ring)
                self.sounds.playDestroySound()



        for exp in self.particles:
            exp.update()
            if len(exp.particles) == 0:
                self.particles.remove(exp)


    def nearestRing(self,ball):
        nearest = self.rings[0]
        minDst = 9999999999999
        for ring in self.rings:
            d =  utils.distance(ring.p_center.x,ring.p_center.y,ball.getPos().x,ball.getPos().y)
            if d <= minDst :
                minDst = d
                nearest = ring
        return nearest

    def draw(self):
        self.drawFinishLine()
        for ring in self.rings:
            ring.draw()

        for wall in self.walls:
            wall.draw()

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

    def drawFinishLine(self):
        # finish line
        width = utils.width/15
        x = 0
        y = utils.height - width * 2
        for row in range(2):
            for col in range(15):
                if row == 0:
                    color = (255,255,255)
                    if col %2 == 0:
                        color = (23,23,23)
                else:
                    color = (23, 23, 23)
                    if col % 2 == 0:
                        color = (255, 255, 255)
                pygame.draw.rect(utils.screen,color,(x + col * width,y + row * width,width,width))