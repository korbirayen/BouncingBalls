from pygame import mixer
import pygame


class Sounds:
    def __init__(self):
        mixer.init()

        self.goalSound = pygame.mixer.Sound("assets/bg.wav")
        self.carVCarSound = pygame.mixer.Sound("assets/pop1.wav")
        self.carVBallSound = pygame.mixer.Sound("assets/pop2.wav")

        # Extract note segments
        self.segments = [
            pygame.mixer.Sound("assets/pop3.wav"),
   
        ]
        self.i = 0

    def play(self):
        sound = self.segments[self.i]
        sound.play()
        self.i += 1
        if self.i >= len(self.segments):
            self.i = 0

    def playGoalSound(self):
        for sound in self.segments:
            sound.stop()
        self.goalSound.play()

    def playCarVCarSound(self):
        for sound in self.segments:
            sound.stop()
        self.carVCarSound.play()

    def playCarVBallSound(self):
        for sound in self.segments:
            sound.stop()
        self.carVBallSound.play()


sounds = Sounds()
