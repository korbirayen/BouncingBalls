from pygame import mixer
import pygame


class Sounds:
    def __init__(self):
        mixer.init()

        # Extract note segments
        self.segments = [
            pygame.mixer.Sound("assets/gf1.wav"),
            pygame.mixer.Sound("assets/gf2.wav"),
            pygame.mixer.Sound("assets/gf3.wav"),
            pygame.mixer.Sound("assets/gf4.wav"),
            pygame.mixer.Sound("assets/gf5.wav"),
            pygame.mixer.Sound("assets/gf6.wav"),
            pygame.mixer.Sound("assets/gf7.wav"),
            pygame.mixer.Sound("assets/gf8.wav"),
            pygame.mixer.Sound("assets/gf9.wav"),
            pygame.mixer.Sound("assets/gf10.wav"),
            pygame.mixer.Sound("assets/gf11.wav"),
            pygame.mixer.Sound("assets/gf12.wav"),
            pygame.mixer.Sound("assets/gf13.wav"),
            pygame.mixer.Sound("assets/gf14.wav"),
            pygame.mixer.Sound("assets/gf15.wav"),
            pygame.mixer.Sound("assets/gf16.wav"),
            pygame.mixer.Sound("assets/gf17.wav"),
            pygame.mixer.Sound("assets/gf18.wav"),
            pygame.mixer.Sound("assets/gf19.wav"),
            pygame.mixer.Sound("assets/gf20.wav"),
            pygame.mixer.Sound("assets/gf21.wav"),
            pygame.mixer.Sound("assets/gf22.wav"),
            pygame.mixer.Sound("assets/gf23.wav"),
            pygame.mixer.Sound("assets/gf24.wav"),
            pygame.mixer.Sound("assets/gf25.wav"),
            pygame.mixer.Sound("assets/gf26.wav"),
            pygame.mixer.Sound("assets/gf27.wav"),
            pygame.mixer.Sound("assets/gf28.wav"),
            pygame.mixer.Sound("assets/gf29.wav"),
            pygame.mixer.Sound("assets/gf30.wav"),
            pygame.mixer.Sound("assets/gf31.wav"),




        ]
        self.i = 0

    def play(self):
        sound = self.segments[self.i]
        sound.play()
        self.i += 1
        if self.i >= len(self.segments):
            self.i = 0



sounds = Sounds()
