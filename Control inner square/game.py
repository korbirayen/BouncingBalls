import math
import random
import pygame
from Box2D import b2TestOverlap
from pygame import Vector2
from Ball import Square
from Box import Box
from OuterRing import OuterRing
from OuterSquareRing import OuterSquareRing
from Polygon import Polygon
from WinCircle import WinSquare
from particle import Explosion
from innerring import InnerSquare
from ring2 import Ring2
from sounds import Sounds
from util import utils


class Game:
    def __init__(self):
        self.balls = []
        # self.balls.append()
        self.balls = [
            Square(Vector2(utils.width / 2 - 150, 200), 4, (255, 0, 255), Vector2(5.5, 0)),
            Square(Vector2(utils.width / 2 + 150, 200), 4, (255, 140, 0), Vector2(-5.5, 0)),
        ]
        self.particles = []
        self.boxes = []

        self.inner = InnerSquare(Vector2(utils.width / 2, utils.height / 2), 200)

        self.outer = OuterSquareRing(34, 0)

        self.sounds = Sounds()
        self.winCircle = WinSquare()

        self.innerRect = pygame.Rect(utils.width / 2 - 100, utils.height / 2 - 100, 200, 200)

        # Timer initialization
        self.timer = 60  # 60 seconds countdown
        self.font = pygame.font.Font(None, 70)  # Font for displaying the timer
        self.start_ticks = pygame.time.get_ticks()  # Start the timer

    def update(self):
        if self.winCircle.size >= 200:
            return

        utils.world.Step(1.0 / 60.0, 6, 2)

        self.winCircle.update()
        self.winCircle.collideWith = 0

        collideWithBoth = 0
        for ball in self.balls:
            ball.update()
            if self.innerRect.collidepoint(ball.getPos().x, ball.getPos().y):
                if ball == self.balls[0]:  # red
                    collideWithBoth += 1
                    self.winCircle.collideWith = 1
                if ball == self.balls[1]:
                    collideWithBoth += 1
                    self.winCircle.collideWith = -1

        if collideWithBoth == 2:
            self.winCircle.collideWith = 0

        for exp in self.particles:
            exp.update()
            if len(exp.particles) == 0:
                self.particles.remove(exp)

        # Timer update
        seconds_passed = (pygame.time.get_ticks() - self.start_ticks) / 1000  # Convert milliseconds to seconds
        self.timer = max(60 - int(seconds_passed), 0)  # Count down from 60

    def draw(self):
        outerPos = Vector2(utils.width / 2 - 500 / 2, utils.height / 2 - 500 / 2)
        for ball in self.balls:
            ball.draw(self.outer.surface)

        pygame.draw.rect(self.inner.surface, (0, 0, 0, 255), self.innerRect)

        utils.screen.blit(self.outer.surface, (0, 0))
        utils.screen.blit(self.inner.surface, (0, 0))

        self.outer.draw()
        self.inner.draw()

        self.winCircle.draw()
        for ball in self.balls:
            ball.draw(utils.screen)

        for exp in self.particles:
            exp.draw()

        # Draw the timer on the screen
        timer_text = self.font.render(f"{self.timer}", True, (255, 255, 255))
        utils.screen.blit(timer_text, (273, 630))  # Display in the top-left corner

    def check_collision(self, ball, box):
        ballPos = utils.to_Pos(ball.circle_body.position)
        boxPos = utils.to_Pos(box.box_body.position)

        if utils.distance(ballPos[0], ballPos[1], boxPos[0], boxPos[1]) < 67:
            return True
        return False
