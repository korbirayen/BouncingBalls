import math

from pygame import Vector2

from Country import Country
from Line import Line
from util import utils


class Star:
    def __init__(self,imgs):
        self.lines = []
        self.countries = []
        self.center = Vector2(utils.width/2,utils.height/2)
        self.createRing(50)
        self.createRing(100)
        self.createRing(150)
        self.createRing(200)
        self.createStars(imgs)

    def createRing(self,radius):
        size = 8
        vertices = []
        for i in range(size):
            angle = i * (2 * math.pi / size)
            x = radius * math.cos(angle)
            y = radius * math.sin(angle)
            vertices.append(self.center + Vector2(x, y))
        for i in range(len(vertices)):
            nextI = (i+1)% len(vertices)
            line = Line(vertices[i],vertices[nextI])
            self.lines.append(line)

    def draw(self):
        for line in self.lines:
            if line.destroyFlag:
                utils.world.DestroyBody(line.body)
                self.lines.remove(line)

        for line in self.lines:
            line.draw()

        for country in self.countries:
            country.draw()

    def createStars(self,imgs):
        size = 8
        radius = 200
        vertices = []
        cI = 0
        for i in range(size):
            angle = i * (2 * math.pi / size)
            x = radius * math.cos(angle)
            y = radius * math.sin(angle)
            vertices.append(self.center + Vector2(x, y))

            nextI = (i + 1) % (size + 1)
            angleNexti = nextI * (2*math.pi / size)

            middleAngle = (angleNexti + angle)/2
            middleX = radius * math.cos(middleAngle) * 1.5
            middleY = radius * math.sin(middleAngle) * 1.5
            vertices.append(self.center + Vector2(middleX, middleY))

            cX = radius * math.cos(middleAngle) * 1.15
            cY = radius * math.sin(middleAngle) * 1.15
            self.countries.append(Country(self.center + Vector2(cX,cY),imgs[cI]))
            cI += 1
            print("u")


        for i in range(len(vertices)):
            nextI = (i+1)% len(vertices)
            line = Line(vertices[i],vertices[nextI])
            self.lines.append(line)