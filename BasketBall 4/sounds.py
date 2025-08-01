from pygame import mixer
import pygame


class Sounds:
    def __init__(self):
        mixer.init()

        self.goalSound = pygame.mixer.Sound("assets/slot.wav")

        # Extract note segments
        self.segments = [
            pygame.mixer.Sound("assets/boop.wav"),
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


sounds = Sounds()
