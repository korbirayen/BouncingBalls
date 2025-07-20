from pygame import mixer
import pygame


class Sounds:
    def __init__(self):
        mixer.init()

        # Extract note segments
        self.segments = [
            pygame.mixer.Sound("assets/Pop1.wav"),
            pygame.mixer.Sound("assets/Pop2.wav"),
            pygame.mixer.Sound("assets/Pop3.wav"),
            pygame.mixer.Sound("assets/Pop4.wav"),
            pygame.mixer.Sound("assets/Pop5.wav"),
            pygame.mixer.Sound("assets/Pop6.wav"),
            pygame.mixer.Sound("assets/Pop7.wav"),
            pygame.mixer.Sound("assets/Pop8.wav"),
        ]

        self.blackHoleSound = pygame.mixer.Sound("assets/pop1.wav")

        self.i = 0

    def play(self):
        sound = self.segments[self.i]
        sound.play()
        self.i += 1
        if self.i >= len(self.segments):
            self.i = 0

    def playBlackHoleSound(self):
        self.blackHoleSound.play()


sounds = Sounds()
