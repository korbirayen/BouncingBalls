from pygame import mixer
import pygame


class Sounds:
    def __init__(self):
        mixer.init()

        self.goalSound = pygame.mixer.Sound("assets/click.wav")

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
        sound = self.segments[self.i]
        sound.play(maxtime=200)
        self.i += 1
        if self.i >= len(self.segments):
            self.i = 0

    def playGoalSound(self):
        for sound in self.segments:
            sound.stop()
        pygame.mixer.Sound.stop(self.goalSound)
        pygame.mixer.Sound.play(self.goalSound)
        # self.goalSound.stop()
        # self.goalSound.play()


sounds = Sounds()
