import math

import pygame
from Box2D import b2TestOverlap
from pygame import Vector2

from Ball import Ball
from Box import Box
from Net import Net
from Trapezium import Trapezium
from particle import Explosion
from ring import Ring
from sounds import Sounds
from util import utils


class Game:
    def __init__(self):
        self.balls = []
        self.balls.append(Ball(Vector2(utils.width/2+ 150 ,utils.height/2 + 150),2,(255,23,23)))
        self.particles = []
        self.rings = [
            Ring(250,1),
        ]
        self.collide = False
        self.waitTime = 0
        self.sounds = Sounds()

        self.net = Net(Vector2(250,250))




    def update(self):
        utils.world.Step(1.0 / 60.0, 6, 2)

        for ball in self.balls:
            if utils.collide(ball,self.net) :
                self.balls.append(Ball(Vector2(utils.width/2-150,utils.height/2 + 150),2,(255,23,23)))
                self.balls.append(Ball(Vector2(utils.width/2+150,utils.height/2 + 150),2,(255,23,23)))
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

        #     pygame.draw.rect(utils.screen,(233,23,23),ball.getRect())
        # pygame.draw.rect(utils.screen, (233, 23, 23), self.net.getRect())



        self.net.draw()


        for exp in self.particles:
            exp.draw()

