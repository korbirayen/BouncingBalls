from pygame import mixer
import pygame


class Sounds:
    def __init__(self):
        mixer.init()

        # Extract note segments
        self.segments = [
            pygame.mixer.Sound("assets/chicken.wav"),
        ]
        self.i = 0

    def play(self):
        sound = self.segments[self.i]
        sound.play()
        self.i += 1
        if self.i >= len(self.segments):
            self.i = 0



sounds = Sounds()


