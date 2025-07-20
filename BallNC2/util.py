
import pygame
import math

from Box2D import b2World
from pygame.locals import *

from pygame import Vector2, mixer, time

from MyContactListener import MyContactListener


# a global class
# store global variable, functions

class Utils():

    def __init__(self):

        pygame.init()

        self.width = 600
        self.height = 600

        self.screen = pygame.display.set_mode((self.width, self.height), DOUBLEBUF, 16)
        self.dt = 0
        self.clock = pygame.time.Clock()

        self.currentScreen = None

        self.font8 = pygame.font.Font('assets/robot.ttf', 30)
        self.font12 = pygame.font.Font('assets/pixel.ttf', 12)
        self.font16 = pygame.font.Font('assets/pixel.ttf', 16)

        self.world = b2World(gravity=(0, -20), doSleep=True)
        self.contactListener = MyContactListener()
        self.world.contactListener = self.contactListener

        self.PPM = 10.0  # Pixels per meter

        self.fps = 0
        self.fpsCounter = 0
        self.fpsTimeCount = 0

    def to_Pos(self,pos):
        """Convert from Box2D to Pygame coordinates."""
        return (pos[0] * self.PPM, self.height - (pos[1] * self.PPM))

    def from_Pos(self,pos):
        """Convert from Pygame to Box2D coordinates."""
        return (pos[0] / self.PPM, (self.height - pos[1]) / self.PPM)

    def initDeltaTime(self):  # calculate deltaTime
        t = self.clock.tick(60 * 2)
        self.dt = t / 1000

    def deltaTime(self):
        return self.dt

    def showFps(self):
        self.fpsTimeCount += self.deltaTime()
        self.fpsCounter += 1
        if self.fpsTimeCount > 1:
            self.fpsTimeCount = 0
            self.fps = self.fpsCounter
            self.fpsCounter = 0

        if self.fps >= 50:
            self.drawText(Vector2(0, 0), "fps: " + str(self.fps), (0, 0, 0), self.font16)
        else:
            self.drawText(Vector2(0, 0), "fps: " + str(self.fps), (0, 0, 0), self.font16)

    def drawText(self, pos, text, color, font):  # draw text
        text = font.render(text, True, color)
        self.screen.blit(text, (pos.x, pos.y))

    def distance(self, x1, y1, x2, y2):
        return math.sqrt(math.pow(x2 - x1, 2) + math.pow(y2 - y1, 2) * 1.0)

    def rotate(self, surface, angle, pivot, offset):
        rotated_image = pygame.transform.rotozoom(surface, -angle, 1)
        rotated_offset = offset.rotate(angle)
        rect = rotated_image.get_rect(center=pivot + rotated_offset)
        return rotated_image, rect


utils = Utils()  # util is global object
