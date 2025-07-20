from pygame import mixer
import pygame


class Sounds:
    def __init__(self):
        mixer.init()

        # Extract note segments
        self.segments = [
            pygame.mixer.Sound("assets/mariojump.wav"),
        ]

        self.blackHoleSound = pygame.mixer.Sound("assets/levelup.wav")

        self.i = 0

    def play(self):
        for s in self.segments:
            s.stop()
        sound = self.segments[self.i]
        sound.play()
        self.i += 1
        if self.i >= len(self.segments):
            self.i = 0

    def playBlackHoleSound(self):
        self.blackHoleSound.play()


sounds = Sounds()
