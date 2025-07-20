import numpy as np
from pygame import mixer
import pygame


class Sounds:
    def __init__(self):
        pygame.mixer.init(frequency=44100, size=-16, channels=1, buffer=512)

    def generate_wave(self, frequency, duration, sample_rate=44100, amplitude=0.5):
        t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
        wave = amplitude * np.sin(2 * np.pi * frequency * t)
        wave = (wave * 32767).astype(np.int16)  # Convert to 16-bit PCM format

        # Create a stereo signal by duplicating the mono signal
        stereo_wave = np.zeros((len(wave), 2), dtype=np.int16)
        stereo_wave[:, 0] = wave  # Left channel
        stereo_wave[:, 1] = wave  # Right channel

        return stereo_wave


    def get_note_frequency(self,note_index):
        base_frequencies = [261.63, 293.66, 329.63, 349.23, 392.00, 440.00, 493.88, 523.25]  # C4 to C5

        # Get the octave by integer division by 8 (base_frequencies length)
        octave = note_index // 8
        # Get the note within the octave
        note_in_octave = note_index % 8
        # Calculate the frequency for the note
        frequency = base_frequencies[note_in_octave] * (2 ** octave)
        return frequency

    def play_sound(self,wave_array):
        sound = pygame.sndarray.make_sound(wave_array)
        sound.play()

    def play_at(self,i):
        frequency = self.get_note_frequency(5 + i)
        wave = self.generate_wave(frequency, 0.2)
        self.play_sound(wave)

