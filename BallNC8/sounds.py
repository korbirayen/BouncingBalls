from pygame import mixer
import pygame


class Sounds:
    def __init__(self):
        mixer.init()

        # Extract note segments
        self.segments = [
            pygame.mixer.Sound("assets/RSS1.wav"),
            pygame.mixer.Sound("assets/RSS2.wav"),
            pygame.mixer.Sound("assets/RSS3.wav"),
            pygame.mixer.Sound("assets/RSS4.wav"),
            pygame.mixer.Sound("assets/RSS5.wav"),
            pygame.mixer.Sound("assets/RSS6.wav"),
            pygame.mixer.Sound("assets/RSS7.wav"),
            pygame.mixer.Sound("assets/RSS8.wav"),
            pygame.mixer.Sound("assets/RSS9.wav"),
            pygame.mixer.Sound("assets/RSS10.wav"),
            pygame.mixer.Sound("assets/RSS11.wav"),
            pygame.mixer.Sound("assets/RSS12.wav"),
            pygame.mixer.Sound("assets/RSS13.wav"),
        ]
        self.i = 0

    def play(self):
        sound = self.segments[self.i]
        sound.play()
        self.i += 1
        if self.i >= len(self.segments):
            self.i = 0



sounds = Sounds()
