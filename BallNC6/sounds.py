from pygame import mixer
import pygame


class Sounds:
    def __init__(self):
        mixer.init()

        # Extract note segments
        self.segments = [
            pygame.mixer.Sound("assets/SM1.wav"),
            pygame.mixer.Sound("assets/SM2.wav"),
            pygame.mixer.Sound("assets/SM3.wav"),
            pygame.mixer.Sound("assets/SM4.wav"),
            pygame.mixer.Sound("assets/SM5.wav"),
            pygame.mixer.Sound("assets/SM6.wav"),
            pygame.mixer.Sound("assets/SM7.wav"),
            pygame.mixer.Sound("assets/SM8.wav"),
            pygame.mixer.Sound("assets/SM9.wav"),
            pygame.mixer.Sound("assets/SM10.wav"),
            pygame.mixer.Sound("assets/SM11.wav"),
            pygame.mixer.Sound("assets/SM12.wav"),
            pygame.mixer.Sound("assets/SM13.wav"),
            pygame.mixer.Sound("assets/SM14.wav"),
            pygame.mixer.Sound("assets/SM15.wav"),
            pygame.mixer.Sound("assets/SM16.wav"),
            pygame.mixer.Sound("assets/SM17.wav"),
            pygame.mixer.Sound("assets/SM18.wav"),
            pygame.mixer.Sound("assets/SM19.wav"),
            pygame.mixer.Sound("assets/SM20.wav"),
            pygame.mixer.Sound("assets/SM21.wav"),
            pygame.mixer.Sound("assets/SM22.wav"),
            pygame.mixer.Sound("assets/SM23.wav"),
            pygame.mixer.Sound("assets/SM24.wav"),
            pygame.mixer.Sound("assets/SM25.wav"),
            pygame.mixer.Sound("assets/SM26.wav"),
            pygame.mixer.Sound("assets/SM27.wav"),
            pygame.mixer.Sound("assets/SM28.wav"),
            pygame.mixer.Sound("assets/SM29.wav"),
            pygame.mixer.Sound("assets/SM30.wav"),

        ]
        self.i = 0

    def play(self):
        sound = self.segments[self.i]
        sound.play()
        self.i += 1
        if self.i >= len(self.segments):
            self.i = 0



sounds = Sounds()
