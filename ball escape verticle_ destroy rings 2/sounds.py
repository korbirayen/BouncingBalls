from pygame import mixer
import pygame


class Sounds:
    def __init__(self):
        mixer.init()

        self.destroySound = pygame.mixer.Sound("assets/pickupCoin.wav")

        # Extract note segments
        self.segments = [
            pygame.mixer.Sound("assets/gravity fall.wav"),
            pygame.mixer.Sound("assets/gravity fall (1).wav"),
            pygame.mixer.Sound("assets/gravity fall (2).wav"),
            pygame.mixer.Sound("assets/gravity fall (3).wav"),
            pygame.mixer.Sound("assets/gravity fall (4).wav"),
            pygame.mixer.Sound("assets/gravity fall (5).wav"),
            pygame.mixer.Sound("assets/gravity fall (6).wav"),
            pygame.mixer.Sound("assets/gravity fall (7).wav"),
            pygame.mixer.Sound("assets/gravity fall (8).wav"),
            pygame.mixer.Sound("assets/gravity fall (9).wav"),
            pygame.mixer.Sound("assets/gravity fall (10).wav"),
            pygame.mixer.Sound("assets/gravity fall (11).wav"),
            pygame.mixer.Sound("assets/gravity fall (12).wav"),
            pygame.mixer.Sound("assets/gravity fall (13).wav"),
            pygame.mixer.Sound("assets/gravity fall (14).wav"),
            pygame.mixer.Sound("assets/gravity fall (15).wav"),
        ]
        self.i = 0

    def play(self):
        for s in self.segments:
            s.stop()
        sound = self.segments[self.i]
        sound.play()
        self.i += 1
        if self.i >= len(self.segments):
            self.i = 0

    def playDestroySound(self):
        self.destroySound.play()



sounds = Sounds()
