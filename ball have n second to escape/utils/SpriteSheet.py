import pygame

from utils.util import utils


class SpriteSheet: # check santa.png

    def __init__(self, texture, rows, cols):
        self.countTime = 0
        self.ffrom = 0
        self.fto = 0
        self.current = 0
        self.time = 0
        self.loop = False

        self.texture = texture
        self.rows = rows
        self.cols = cols

        self.sheet = texture
        self.frames = []

        self.width = self.sheet.get_rect().width
        self.height = self.sheet.get_rect().height

        sizeRow = self.sheet.get_rect().height / rows
        sizeCol = self.sheet.get_rect().width / cols
        for row in range(0, rows):
            for col in range(0, cols):
                img = self.image_at((col * sizeCol, row * sizeRow, sizeCol, sizeRow),(0,0,0))
                self.frames.append(img)

    def image_at(self, rectangle, colorkey=None):
        """Load a specific image from a specific rectangle."""
        # Loads image from x, y, x+offset, y+offset.
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size).convert()
        image.blit(self.sheet, (0, 0), rect)
        if colorkey is not None:
            if colorkey == -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey, pygame.RLEACCEL)
        return image

    def play(self):
        self.countTime += utils.deltaTime()
        if self.countTime >= self.time:
            self.countTime = 0
            self.current += 1
            if self.current > self.fto and self.loop:
                self.current = self.ffrom
            elif self.current > self.fto and not self.loop:
                self.current = self.fto

    def setPlay(self, ffrom, fto, time, loop): # play sheet from to
        self.ffrom = ffrom
        self.fto = fto
        self.time = time
        self.loop = loop
        self.current = ffrom


    def getCurrentFrame(self):
        return self.frames[self.current]


