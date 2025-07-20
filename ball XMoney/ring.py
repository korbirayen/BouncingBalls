import math
import pygame
from pygame import Vector2
from Line import Line
from Net import Net
from util import utils


class Ring:
    def __init__(self, size=3):
        self.size = size  # Number of sides (3 for triangle, 4 for square, etc.)
        self.center = Vector2(utils.width / 2, utils.height / 2)

        marginY = 200
        marginX = 50
        self.width  = (utils.width - marginX - marginX)
        self.lines = [

            Line(Vector2(marginX,marginY),Vector2(utils.width-marginX,marginY),(255,255,255)),
            Line(Vector2(marginX, utils.height - marginY), Vector2(utils.width - marginX, utils.height - marginY), (255, 255, 255)),
            Line(Vector2(marginX, marginY), Vector2(marginX, utils.height - marginY), (255, 255, 255)),
            Line(Vector2(utils.width - marginX, marginY), Vector2(utils.width - marginX, utils.height - marginY), (255, 255, 255)),
        ]

        self.nets = []
        slides = 8
        percents = [50,1.8,0.5,0.2,0.2,0.5,1.8,50]

        x = marginX
        slideHeight = 50
        width = (utils.width - marginX - marginX) / slides
        for i in range(slides):
            line = Line(Vector2(x, utils.height - marginY), Vector2(x, utils.height - marginY - slideHeight), (255, 255, 255))
            self.lines.append(line)
            self.nets.append(Net(pygame.Rect(x,utils.height - marginY - 5,width,5),percents[i]))
            x += width



    def getWidth(self):
        return self.width

    def update(self):
        pass

    def destroy(self):
        for line in self.lines:
            utils.world.DestroyBody(line.body)

    def draw(self):
        for line in self.lines:
            line.draw()

        for net in self.nets:
            net.draw()
