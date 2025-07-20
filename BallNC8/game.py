import math

import pygame
from Box2D import b2TestOverlap
from pygame import Vector2

from Ball import Ball
from Box import Box
from Polygon import Polygon
from particle import Explosion
from ring import Ring
from sounds import Sounds
from util import utils


class Game:
    def __init__(self):
        self.balls = []
        self.ball = Ball(Vector2(utils.width / 2 + 50, utils.height / 2 - 50), 1.4)
        self.balls.append(self.ball)


        self.particles = []
        self.boxes = []
        self.rings = [
            Ring(utils.width/2 - 50 * .7   ,300,-2,(207, 52, 235)),
            Ring(utils.width/2 - 50 *  2.1  ,300,2,(207, 52, 235)),
            Ring(utils.width/2 - 50 * 3.5   ,300,-2,(207, 52, 235)),
        ]
        # for ring in self.rings:
        #     self.boxes += ring.boxes

        self.collide = False
        self.waitTime = 0
        self.sounds = Sounds()
        self.complete = False
        self.bounceCount = 0


    def update(self):
        utils.world.Step(1.0 / 60.0, 6, 2)
        if utils.contactListener.collisions:
            for bodyA, bodyB in utils.contactListener.collisions:
                # ballBody = bodyA
                # if isinstance(bodyB.userData,Ball):
                #     ballBody = bodyB
                # nextRadius = ballBody.userData.radius/100 * 100
                # ballBody.userData.increase_radius(nextRadius)
                self.sounds.play()
                self.bounceCount += 1
                if self.bounceCount >= 15:
                    self.ball.convert_to_static()
                    self.bounceCount = 0
                    self.ball = Ball(Vector2(utils.width / 2 - 50, utils.height / 2 - 50), 1.4)
                    self.balls.append(self.ball)
                break
            utils.contactListener.collisions = []

        for ring in self.rings:
            ring.update()
            if ring.complete:
                continue
            if utils.distance(self.ball.getPos().x,self.ball.getPos().y,utils.width/2,utils.height/2) > utils.width:
                for box in ring.boxes:
                   box.convert_to_dynamic()
                ring.complete = True


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


    def draw(self):
        textWidth = utils.font24.render("Bounces: " + str(round(self.bounceCount)),(255,255,255),True).get_width()
        utils.drawText(Vector2(utils.width/2-textWidth/2,10),"Bounces: " + str(round(self.bounceCount)),(255,255,255),utils.font24)
        for ring in self.rings:
            ring.draw()

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