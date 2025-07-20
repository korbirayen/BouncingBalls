import pygame
import math
from Box2D import b2World
from pygame.locals import *
from pygame import Vector2
from MyContactListener import MyContactListener

class Utils():
    def __init__(self):
        pygame.init()
        self.width = 600
        self.height = 600
        self.screen = pygame.display.set_mode((self.width, self.height), DOUBLEBUF, 16)
        self.dt = 0
        self.clock = pygame.time.Clock()
        self.currentScreen = None
        
        try:
            self.font8 = pygame.font.Font('assets/pixel.ttf', 8)
            self.font12 = pygame.font.Font('assets/pixel.ttf', 12)
            self.font16 = pygame.font.Font('assets/pixel.ttf', 16)
        except:
            self.font8 = pygame.font.Font(None, 8)
            self.font12 = pygame.font.Font(None, 12)
            self.font16 = pygame.font.Font(None, 16)

        self.world = b2World(gravity=(0, -20), doSleep=True)
        self.contactListener = MyContactListener()
        self.world.contactListener = self.contactListener
        self.PPM = 10.0
        self.fps = 0
        self.fpsCounter = 0
        self.fpsTimeCount = 0
        self.time = 0

    def to_Pos(self, pos):
        return (pos[0] * self.PPM, self.height - (pos[1] * self.PPM))

    def from_Pos(self, pos):
        return (pos[0] / self.PPM, (self.height - pos[1]) / self.PPM)

    def initDeltaTime(self):
        t = self.clock.tick(60)
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
        text = self.font16.render(f"fps: {self.fps}", True, (255, 255, 255))
        self.screen.blit(text, (0, 0))

    def drawText(self, pos, text, color, font):
        text = font.render(text, True, color)
        self.screen.blit(text, (pos.x, pos.y))

    def distance(self, x1, y1, x2, y2):
        return math.sqrt(math.pow(x2 - x1, 2) + math.pow(y2 - y1, 2))

utils = Utils()
