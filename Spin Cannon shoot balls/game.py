import math
import random

import pygame
from Box2D import b2TestOverlap
from pygame import Vector2

from Ball import Ball
from BallBox import BallBox
from Block import Block
from Box import Box
from Cannon import Cannon
from EdgePolygon import EdgePolygon
from GroundBar import GroundBar
from Heart import Heart
from Polygon import Polygon
from SeparateBox import SeparateBox
from particle import Explosion, HeartExplosion
from ring import Ring
from sounds import Sounds, sounds
from util import utils


class Game:
    def __init__(self):
        self.balls = [
            Ball(Vector2(utils.width/2,300),1,utils.hueToRGB(random.uniform(0,1))),
        ]
        # self.balls.append()
        self.particles = []
        self.rings = [
            Ring(Vector2(utils.width/2, utils.height/2), utils.width/2-100, 360, 0, (255, 255, 255)),
        ]

        self.ballProjectiles = []

        self.redCannon = Cannon(Vector2(50,660),'red')

        self.spawnTime = 1
        self.spawnInterval = 0


    def update(self):

        if len(self.balls) > 0:
            self.spawnInterval += utils.deltaTime()
            if self.spawnInterval >= self.spawnTime:
                self.spawnInterval = 0
                self.spawnTime *= 1.
                self.balls.append(Ball(Vector2(utils.width / 2, 300), 1, utils.hueToRGB(random.uniform(0, 1))))

        for ball in self.balls:
            ball.update()
            for p in self.ballProjectiles:
                if p.pos.x < -100 or p.pos.y < -100 or p.pos.x > utils.width + 100 or p.pos.y > utils.height + 100:
                    p.destroyFlag = True
                if utils.collide(p.getRect(),ball.getRect()):
                    sounds.playSound("green_shoot")
                    ball.destroyFlag = True
                    p.destroyFlag = True
                    self.particles.append(HeartExplosion(ball.getPos().x,ball.getPos().y,ball.color))


        self.redCannon.update()
        for p in self.ballProjectiles:
            p.update()

        redP = self.redCannon.getProjectile()
        if redP:
            self.ballProjectiles.append(redP)
            sounds.playSound("red_shoot")

        # remove block and ballProjectile
        for ball in self.ballProjectiles:
            if ball.destroyFlag:
                self.ballProjectiles.remove(ball)

        # remove balls
        for ball in self.balls:
            if ball.destroyFlag:
                utils.world.DestroyBody(ball.circle_body)
                self.balls.remove(ball)

        for ring in self.rings:
            ring.update()

        utils.world.Step(1.0 / 60.0, 6, 2)
        if utils.contactListener.collisions:
            for bodyA, bodyB in utils.contactListener.collisions:
                sounds.play()
                utils.contactListener.collisions = []
                break

        for particle in self.particles:
            particle.update()
        for particle in self.particles:
            if particle.destroyFlag:
                self.particles.remove(particle)

    def draw(self):
        pygame.draw.circle(utils.screen,(255,255,255),Vector2(utils.width/2,utils.height/2),utils.width/2-50,3)
        self.redCannon.draw()


        for ring in self.rings:
            ring.draw()
        for ball in self.balls:
            ball.draw()

        for p in self.ballProjectiles:
            p.draw()

        for exp in self.particles:
            exp.draw()
