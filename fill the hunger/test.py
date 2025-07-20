import math
import random
import pygame
import time
import vlc
from pygame import Vector2, Color, USEREVENT

# Initialize Pygame
pygame.init()

# Screen dimensions
width = 1000
height = 1000

# Initialize clock and screen
clock = pygame.time.Clock()
screen = pygame.display.set_mode((width, height))
screen.fill((0, 0, 0))  # Black background

# Load MP3 file
pygame.mixer.init()


class Ball:
    def __init__(self):
        # Initialize position randomly within the circle's boundary
        angle = random.uniform(0, 2 * math.pi)
        radius = random.uniform(0, width / 2 - 30)  # Ensure the ball doesn't start too close to the edge
        self.position = Vector2(width / 2 + radius * math.cos(angle),
                                height / 2 + radius * math.sin(angle))
        self.color = (0, 0, 0)
        self.gravity = Vector2(0, 0.32)
        self.velocity = Vector2(-9, -9)
        self.prevPos = Vector2(self.position.x, self.position.y)
        self.radius = 30
        self.bounce_count = 0  # Counter for bounces
        self.song = vlc.MediaPlayer('assets/your_song.mp3')
        self.song.set_time(0)  # Start time of the song to play
        self.song_start_time = 0
        self.timer_running = False  # Flag to track if timer is running

        self.particles = []  # List to hold active particles

        self.song.play()
        self.song.audio_set_volume(0)
        time.sleep(0.1)
        self.song_end_time = self.song.get_length()
        self.song.audio_set_volume(50)
        self.song.stop()

    def update(self):
        self.prevPos = Vector2(self.position.x, self.position.y)

        # movement
        self.velocity += self.gravity
        self.position += self.velocity

        dirToCenter = Vector2(self.position.x - width / 2, self.position.y - height / 2)
        if self.isCollide():
            if not self.timer_running:
                pygame.time.set_timer(USEREVENT + 1, 300)  # Set timer for 0.3 seconds
                self.timer_running = True

            # self.song.play()  # Play song
            # self.song_start_time += 300  # Move start time forward for next bounce
            # self.song.set_time(self.song_start_time)
            if not self.song.is_playing():
                self.song.play()
            self.song.audio_set_volume(50)
            if self.song_start_time > self.song_end_time:
                self.song_start_time = 0  # Restart song if end is reached
            self.radius += 1
            self.position = Vector2(self.prevPos.x, self.prevPos.y)

            # Increase velocity magnitude slightly
            self.velocity *= 1.01  # Adjust this factor as needed

            v = math.sqrt(self.velocity.x * self.velocity.x + self.velocity.y * self.velocity.y)
            angleToCollisionPoint = math.atan2(-dirToCenter.y, dirToCenter.x)
            oldAngle = math.atan2(-self.velocity.y, self.velocity.x)
            newAngle = 2 * angleToCollisionPoint - oldAngle
            self.velocity = Vector2(-v * math.cos(newAngle), v * math.sin(newAngle))
            self.bounce_count += 1  # Increment bounce count

            # Create particles
            num_particles = 50
            for _ in range(num_particles):
                angle = random.uniform(0, 2 * math.pi)
                speed = random.uniform(1, 5)
                color = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))
                lifespan = random.randint(20, 40)  # Lifespan of the particle
                particle = Particle(self.position, angle, speed, color, lifespan)
                self.particles.append(particle)

        # Update and remove particles
        for particle in self.particles[:]:  # Iterate over a copy to safely remove from original list
            particle.update()

    def isCollide(self):
        if self.distance(self.position.x, self.position.y, width / 2, height / 2) > width / 2 - self.radius:
            return True
        return False

    def distance(self, x1, y1, x2, y2):
        return math.sqrt(math.pow(x2 - x1, 2) + math.pow(y2 - y1, 2) * 1.0)

    def draw(self):
        pygame.draw.circle(screen, self.color, (int(self.position.x), int(self.position.y)), self.radius)

        # Draw particles
        for particle in self.particles:
            particle.draw()

    def draw_bounce_counter(self):
        # Clear previous counter by filling the background over the previous text
        pygame.draw.rect(screen, (0, 0, 0), (10, 10, 150, 50))

        font = pygame.font.Font(None, 36)
        text = font.render(f"Bounces: {self.bounce_count}", True, (255, 255, 255))
        screen.blit(text, (10, 10))


class Particle:
    def __init__(self, position, angle, speed, color, lifespan):
        self.position = Vector2(position.x, position.y)
        self.velocity = Vector2(speed * math.cos(angle), speed * math.sin(angle))
        self.color = color
        self.alpha = 255
        self.lifespan = lifespan  # Total lifespan of the particle
        self.age = 0  # Current age of the particle

    def update(self):
        self.position += self.velocity
        self.age += 1
        self.alpha = int(255 * (self.age / self.lifespan))  # Fade out gradually

    def draw(self):
        # Ensure alpha is within valid range (0 to 255)
        alpha = max(0, min(255, self.alpha))
        color_with_alpha = (self.color[0], self.color[1], self.color[2], alpha)
        pygame.draw.circle(screen, color_with_alpha, (int(self.position.x), int(self.position.y)), 2)

    def is_dead(self):
        return self.age >= self.lifespan


# Initialize the ball
ball = Ball()
color = Color(211, 12, 211)
h = color.hsla[0]
s = color.hsla[1]
l = color.hsla[2]
colorDir = 1

# Main loop
running = True
while running:
    clock.tick(60)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == USEREVENT + 1:
            # ball.song.stop()  # Stop song after 0.2 seconds

            ball.song.audio_set_volume(0)
            ball.timer_running = False

    # Update ball
    screen.fill((0, 0, 0))
    ball.update()

    # Draw circle background with rotating rainbow colors
    pygame.draw.circle(screen, (255, 0, 0), (width // 2, height // 2), width // 2, 5)
    color.hsla = (h, s, l, 1)
    h += 1 * colorDir
    if h >= 360:
        colorDir = -1
    elif h <= 0:
        colorDir = 1
    pygame.draw.circle(screen, (color.r, color.g, color.b), (int(ball.position.x), int(ball.position.y)),
                       ball.radius + 2)

    # Draw the ball
    ball.draw()

    # Draw bounce counter
    ball.draw_bounce_counter()

    # Refresh the display
    for particle in ball.particles:
        print(particle.is_dead())
        if particle.is_dead():
            ball.particles = []
    pygame.display.flip()

# Stop and quit Pygame mixer
pygame.mixer.stop()
pygame.mixer.quit()

# Quit Pygame
pygame.quit()