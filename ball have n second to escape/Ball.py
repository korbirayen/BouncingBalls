import random
import pygame
from Box2D import b2_staticBody
from pygame import Vector2
from utils.util import utils
import colorsys

import pygame
import colorsys

import pygame
import colorsys

class Trail:
    def __init__(self, max_length=50):
        self.max_length = max_length
        self.positions = []
        self.hue = 0

    def update(self, position):
        # Add the current position with the current color hue
        self.positions.append((position, self.hue))
        # Remove old positions from the trail
        while len(self.positions) > self.max_length:
            self.positions.pop(0)
        # Increment the hue for the next frame
        self.hue = (self.hue + 0.02) % 1.0

    def draw(self, screen, radius):
        for i, (position, hue) in enumerate(self.positions):
            color = colorsys.hsv_to_rgb(hue, 1, 1)
            color = (int(color[0] * 255), int(color[1] * 255), int(color[2] * 255))
            alpha = max(0, 255 - i * 255 // len(self.positions))  # Fade effect
            pygame.draw.circle(screen, color + (alpha,), (int(position.x), int(position.y)), radius + 18)



class Ball:
    def __init__(self, pos, radius, time):
        self.radius = radius
        self.color = (155, 155, 155)  # Initialize with a default color
        self.circle_body = utils.world.CreateDynamicBody(position=(utils.from_Pos((pos.x, pos.y))))
        self.circle_shape = self.circle_body.CreateCircleFixture(radius=self.radius, density=1, friction=0.0, restitution=1.00)
        self.circle_body.linearVelocity = (.9, 0)
        self.circle_body.userData = self
        self.time = time
        self.destroyFlag = False
        self.isStatic = False
        self.shaking = False
        self.shake_magnitude = 0
        self.shake_duration = 0.5
        self.shake_time_remaining = 0
        self.hue = 0
        self.color_change_interval = 0
        self.time_since_last_color_change = 0
        self.trail = Trail()  # Add a trail instance

    def update_color(self):
        self.hue = (self.hue + 0.001) % 1.0
        r, g, b = colorsys.hsv_to_rgb(self.hue, 1, 1)
        self.color = (int(r * 255), int(g * 255), int(b * 255))

    def draw(self):
        draw_pos = self.getPos()
        self.trail.update(draw_pos)  # Update the trail with the current position

        if self.shaking:
            self.shake_time_remaining -= utils.deltaTime()
            if self.shake_time_remaining <= 0:
                self.shaking = False
            else:
                offset = Vector2(random.uniform(-self.shake_magnitude, self.shake_magnitude),
                                 random.uniform(-self.shake_magnitude, self.shake_magnitude))
                draw_pos = self.getPos() + offset
        else:
            draw_pos = self.getPos()

        self.trail.draw(utils.screen, self.radius)  # Draw the trail with the ball's radius

        if not self.destroyFlag:
            self.time -= utils.deltaTime()
            if self.time < 0:
                self.time = 0
                self.destroyFlag = True
            self.time_since_last_color_change += utils.deltaTime()
            if self.time_since_last_color_change >= self.color_change_interval:
                self.update_color()
                self.time_since_last_color_change = 1   
            for fixture in self.circle_body.fixtures:
                self.draw_circle(fixture.shape, self.circle_body, fixture, draw_pos)
            time = round(self.time)
            tw, th = utils.font16.render(str(time), (255, 255, 255), True).get_size()
            utils.drawText(Vector2(draw_pos.x - tw / 2, draw_pos.y - th / 2), str(time), (255, 255, 255), utils.font16)
        else:
            for fixture in self.circle_body.fixtures:
                self.draw_circle_border(fixture.shape, self.circle_body, fixture, draw_pos)

    def draw_circle(self, circle, body, fixture, draw_pos):
        position = utils.to_Pos(body.transform * circle.pos)
        position += (draw_pos - self.getPos())
        pygame.draw.circle(utils.screen, self.color, [int(x) for x in position], int(circle.radius * utils.PPM))
        pygame.draw.circle(utils.screen, (0, 0, 0), [int(x) for x in position], int(circle.radius + 1.2 * utils.PPM))

    def draw_circle_border(self, circle, body, fixture, draw_pos):
        position = utils.to_Pos(body.transform * circle.pos)
        position += (draw_pos - self.getPos())
        pygame.draw.circle(utils.screen, self.color, [int(x) for x in position], int(circle.radius * utils.PPM), 5)

    def getPos(self):
        p = utils.to_Pos(self.circle_body.position)
        return Vector2(p[0], p[1])

    def convertToStatic(self):
        self.circle_body.type = b2_staticBody
        self.circle_body.awake = True
        self.isStatic = True

    def startShaking(self, magnitude=1, duration=0.5):
        self.shaking = True
        self.shake_magnitude = magnitude
        self.shake_duration = duration
        self.shake_time_remaining = duration