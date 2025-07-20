from pygame import mixer
import pygame


class Sounds:
    def __init__(self):
        mixer.init()
        self.sounds = {
            'green_shoot': pygame.mixer.Sound("assets/green_shoot.wav"),
            'red_shoot': pygame.mixer.Sound("assets/pew.wav"),
        }

        # Extract note segments
        self.segments = [
            pygame.mixer.Sound("assets/pop1.wav"),
            pygame.mixer.Sound("assets/pop2.wav"),
            pygame.mixer.Sound("assets/pop3.wav"),
            pygame.mixer.Sound("assets/pop4.wav"),
            pygame.mixer.Sound("assets/pop5.wav"),
            pygame.mixer.Sound("assets/pop6.wav"),
            pygame.mixer.Sound("assets/pop7.wav"),
            pygame.mixer.Sound("assets/pop8.wav"),
        ]
        self.i = 0

    def playSound(self,key):
        self.sounds[key].play()

    def play(self):
        sound = self.segments[self.i]
        sound.play()
        self.i += 1
        if self.i >= len(self.segments):
            self.i = 0



sounds = Sounds()
