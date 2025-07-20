from pygame import mixer
import pygame


class Sounds:
    def __init__(self):
        mixer.init()

        self.destroySound = pygame.mixer.Sound("assets/sadcat.wav")

        # Extract note segments
        self.segments = [
            pygame.mixer.Sound("assets/clav1.wav"),
            pygame.mixer.Sound("assets/clav2.wav"),
            pygame.mixer.Sound("assets/clav3.wav"),
            pygame.mixer.Sound("assets/clav4.wav"),
            pygame.mixer.Sound("assets/clav5.wav"),
            pygame.mixer.Sound("assets/clav6.wav"),
            pygame.mixer.Sound("assets/clav7.wav"),
            pygame.mixer.Sound("assets/clav8.wav"),
            pygame.mixer.Sound("assets/clav9.wav"),
            pygame.mixer.Sound("assets/clav10.wav"),
            pygame.mixer.Sound("assets/clav11.wav"),
            pygame.mixer.Sound("assets/clav12.wav"),
            pygame.mixer.Sound("assets/clav13.wav"),
            pygame.mixer.Sound("assets/clav12.wav"),
            pygame.mixer.Sound("assets/clav11.wav"),
            pygame.mixer.Sound("assets/clav10.wav"),
            pygame.mixer.Sound("assets/clav9.wav"),
            pygame.mixer.Sound("assets/clav8.wav"),
            pygame.mixer.Sound("assets/clav7.wav"),
            pygame.mixer.Sound("assets/clav6.wav"),
            pygame.mixer.Sound("assets/clav5.wav"),
            pygame.mixer.Sound("assets/clav4.wav"),
            pygame.mixer.Sound("assets/clav3.wav"),
            pygame.mixer.Sound("assets/clav2.wav"),
    





   
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
