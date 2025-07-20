import math

import pygame
from Box2D import b2TestOverlap
from pygame import Vector2

from Ball import Ball
from Box import Box
from Gem import Gem
from Trapezium import Trapezium
from particle import Explosion
from ring import Ring
from sounds import Sounds, sounds
from util import utils


class Game:
    def __init__(self):
        self.balls = []
        self.balls.append(Ball(Vector2(utils.width/2-23,utils.height/2-200),3,(255,23,23)))
        self.particles = []
        self.rings = [
            Ring(250,1),
        ]
        self.gem = Gem()
        self.collide = False
        self.waitTime = 0
        self.sounds = Sounds()

        self.time = 60
        self.expCount = 0



    def update(self):
        if self.time < 0:
            self.time = 0
            return
        if self.balls[0].currentImge == 6:
            return
        utils.world.Step(1.0 / 60.0, 6, 2)

        for ball in self.balls:
            d = utils.distance(ball.getPos().x,ball.getPos().y,utils.width/2,utils.height/2)
            if d > 250 - ball.radius*10 + 30 :
                self.balls.append(Ball(Vector2(utils.width/2-50,utils.height/2+20),2,(255,23,23)))
                self.balls.append(Ball(Vector2(utils.width/2+50,utils.height/2+20),2,(255,23,23)))
                utils.world.DestroyBody(ball.circle_body)
                self.balls.remove(ball)

                self.sounds.playGoalSound()

        for ring in self.rings:
            ring.update()
        if utils.contactListener.collisions:
            self.sounds.play()
            utils.contactListener.collisions = []
            # for bodyA, bodyB in utils.contactListener.collisions:
            #     utils.contactListener.collisions = []

        self.time -= utils.deltaTime()

        for exp in self.particles:
            exp.update()
            if len(exp.particles) == 0:
                self.particles.remove(exp)

        for ball in self.balls:
            if utils.collide(ball,self.gem):
                self.gem = Gem()
                self.expCount += 1
                if self.expCount >= 6:
                    self.expCount = 0
                    self.balls[0].nextLevel()
                    sounds.playGoalSound()

    def draw(self):
        for ring in self.rings:
            ring.draw()



        for ball in self.balls:
            ball.draw()

        for exp in self.particles:
            exp.draw()


        timeText = str(round(self.time,1)) + "s"
        tw,th = utils.font32.render(timeText,True,(255,255,255)).get_size()
        utils.drawText(Vector2(utils.width/2 - tw/2,655),
                       timeText,(255,255,255),utils.font32
                       )

        self.drawExpBars()

        if self.balls[0].currentImge == 6:
            return
        self.gem.draw()

    def drawExpBars(self):
        x = 150
        y = 50
        w = 50
        for i in range(0,6):
            pygame.draw.rect(utils.screen,(255,255,255),(x,y,w,20),2)
            x += w + 2

        x = 150
        y = 50
        w = 50
        for i in range(0, self.expCount):
            pygame.draw.rect(utils.screen, (23, 255, 23), (x, y, w, 20))
            x += w + 2
