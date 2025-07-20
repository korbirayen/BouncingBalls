import random

import pygame.image


class AssetsManager:
    def __init__(self):
        self.data = {
            'baseball' : pygame.image.load("assets/emmy.png"),
            'football': pygame.image.load("assets/villy.png"),

        }

    def get(self,key):
        return self.data[key]

    def getRandom(self):
        key = random.choice(list(self.data.keys()))
        return self.data[key]

assetsManager = AssetsManager()