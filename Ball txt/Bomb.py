import math
import pygame
from pygame import Vector2
from sounds import sounds
from util import utils


class Bomb:
    def __init__(self, pos):
        self.pos = pos
        self.img = pygame.image.load("assets/cheese.png")
        self.img = pygame.transform.scale(self.img, (35, 35))

        self.bombTick = 15  # Time until the bomb explodes
        self.bombTickInterval = self.bombTick
        self.flash_interval = 0.1  # Initial flash interval
        self.flash_timer = self.flash_interval  # Timer to control the flashing
        self.visible = True  # To toggle visibility
        
        # Initialize the font for displaying the countdown
        self.font = pygame.font.SysFont(None, 60)  # Set a larger size if desired

    def getRect(self):
        return pygame.Rect(self.pos.x, self.pos.y, self.img.get_width(), self.img.get_height())

    def update(self):
        # Decrease bombTickInterval based on delta time
        self.bombTickInterval -= utils.deltaTime()

        # Calculate the new flash interval dynamically, the lower the bombTickInterval, the faster it flashes
        if self.bombTickInterval > 0:
            # Flash faster as bombTickInterval decreases
            self.flash_interval = max(0.1, self.bombTickInterval / 10)

        # Update the flash timer and toggle visibility when the flash interval is reached
        self.flash_timer -= utils.deltaTime()
        if self.flash_timer <= 0:
            if self.bombTickInterval < 3:
                sounds.playGoalSound()
            self.visible = not self.visible  # Toggle visibility
            self.flash_timer = self.flash_interval  # Reset the flash timer

    def draw(self, surface):
        # Draw the image only if it's currently visible
        if self.bombTickInterval > 3:
            self.visible = True
        if self.visible:
            surface.blit(self.img, self.pos)

        # Display "Bomb Timer:" text followed by the bomb timer at a fixed position on the screen
        bomb_timer_text = f"Cheese Touch: {math.ceil(self.bombTickInterval)}"
        timer_surface = self.font.render(bomb_timer_text, True, (255, 255, 255))  # White text

        # Center the text horizontally and place it at the top of the screen
        timer_pos = (utils.width // 2 - timer_surface.get_width() // 2, 640)
        surface.blit(timer_surface, timer_pos)
