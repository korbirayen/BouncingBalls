import math

import pygame
from Box2D import b2TestOverlap
from pygame import Vector2, Surface

from Ball import Ball
from Bomb import Bomb
from Box import Box
from Net import Net
from Trapezium import Trapezium
from particle import Explosion
from ring import Ring
from sounds import Sounds
from util import utils


class Game:
    def __init__(self):
        self.balls = [
            Ball(Vector2(utils.width / 2, utils.height / 7), 2.5, (0, 255, 0)),
            Ball(Vector2(utils.width / 2 + 80, utils.height / 6),  2.5, (0, 0, 255)),
            Ball(Vector2(utils.width / 2 - 80, utils.height / 6), 2.5, (255, 0, 255)),
            Ball(Vector2(utils.width / 2 - 125, utils.height / 3), 2.5, (125, 0, 255)),
            Ball(Vector2(utils.width / 2 + 125, utils.height / 3), 2.5, (0, 255, 255)),
        ]
        self.particles = []
        self.rings = [
            Ring(250,1),
        ]
        self.collide = False
        self.waitTime = 0
        self.sounds = Sounds()

        self.net = Net(Vector2(255,230))
        self.haveBombBall = None
        self.bomb = Bomb(Vector2(utils.width/2-24,utils.height/2-24))
        self.surface = Surface((utils.width,utils.height),pygame.SRCALPHA)



    def update(self):
        utils.world.Step(1.0 / 60.0, 6, 2)

        if self.haveBombBall is None:
            for ball in self.balls:
                if utils.collide(ball,self.bomb):
                    self.haveBombBall = ball

        self.bomb.update()
        if self.haveBombBall is not None:
            self.bomb.pos = Vector2(self.haveBombBall.getPos().x-self.bomb.getRect().width/2,self.haveBombBall.getPos().y - self.bomb.getRect().height/2)
            if self.bomb.bombTickInterval <= 0:
                self.haveBombBall.destroyFlag = True
                self.haveBombBall = None
                self.bomb.bombTickInterval = self.bomb.bombTick

            for ball in self.balls:
                if ball.destroyFlag:
                    utils.world.DestroyBody(ball.circle_body)
                    self.balls.remove(ball)

                    explosion = Explosion(ball.getPos().x,ball.getPos().y,ball.color)
                    self.particles.append(explosion)

        for ring in self.rings:
            ring.update()
        if utils.contactListener.collisions:
            self.sounds.play()
            for bodyA, bodyB in utils.contactListener.collisions:
                if isinstance(bodyA.userData,Ball) and  isinstance(bodyB.userData,Ball):
                    if bodyA.userData == self.haveBombBall:
                        self.haveBombBall = bodyB.userData
                    elif bodyB.userData == self.haveBombBall:
                        self.haveBombBall = bodyA.userData

            utils.contactListener.collisions = []


        for exp in self.particles:
            exp.update()
            if len(exp.particles) == 0:
                self.particles.remove(exp)

        # for box in self.boxes:
        #     if box.destroyFlag:
        #         utils.world.DestroyBody(box.box_body)
        #         self.boxes.remove(box)

    def draw(self):
        pygame.draw.rect(self.surface,(0,0,0,80),(0,0,utils.width,utils.height))

        for ring in self.rings:
            ring.draw()

        for ball in self.balls:
            ball.draw(self.surface)
            # pygame.draw.rect(utils.screen,(233,23,23),ball.getRect())
        self.bomb.draw(self.surface)

        for exp in self.particles:
            exp.draw(self.surface)

        utils.screen.blit(self.surface,(0,0))



        # pygame.draw.rect(utils.screen, (233, 23, 23), self.bomb.getRect())




