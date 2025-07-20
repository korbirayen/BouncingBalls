import pygame
from pygame import Vector2
from Ball import Ball
from RingB import RingB
from util import utils
from sounds import Sounds

class Game:
    def __init__(self):
        pygame.init()
        self.balls = []
        self.spawn_new_ball()
        self.particles = []
        self.rings = []
        self.initialize_rings()
        self.sounds = Sounds()
        
        self.ball_timer = 0
        self.freeze_time = 7000  # 5000 milliseconds = 5 seconds

    def spawn_new_ball(self):
        """Spawns a new ball at the center."""
        new_ball = Ball(Vector2(utils.width / 2 + 15, utils.height / 2 - 65), 1.2, (255, 255, 255))
        self.balls.append(new_ball)
        self.current_ball = new_ball
        self.ball_timer = pygame.time.get_ticks()

    def initialize_rings(self):
        radius = 8
        base_speed = 2  # Base speed for the first ring
        sar = 0.1
        for i in range(13):
            dir = base_speed * (1 + (0.05 * i))  # Increase speed by 0.1% for each subsequent ring
            ring = RingB(i + 1, radius, dir, sar)
            radius += 1.5
            sar += 1 / 20
            self.rings.append(ring)


    def update(self):
        utils.world.Step(1.0 / 60.0, 6, 2)

        current_time = pygame.time.get_ticks()

        # Handle collisions between balls
        self.handle_ball_collisions()

        # Handle collisions with rings
        if utils.contactListener:
            for bodyA, bodyB in utils.contactListener.collisions:
                self.sounds.play()
                if isinstance(bodyA.userData, Ball) and isinstance(bodyB.userData, RingB):
                    bodyA.userData.shrink()  # Shrink the ball if it collided with a ring
                    bodyA.userData.color = bodyB.userData.color  # Change ball color to match the ring
                elif isinstance(bodyB.userData, Ball) and isinstance(bodyA.userData, RingB):
                    bodyB.userData.shrink()  # Shrink the ball if it collided with a ring
                    bodyB.userData.color = bodyA.userData.color  # Change ball color to match the ring
                break
            utils.contactListener.collisions = []

        # Update rings and handle destruction
        for ring in self.rings:
            ring.update()
            if ring.destroyFlag:
                continue
            for ball in self.balls:
                d = utils.distance(ball.getPos().x, ball.getPos().y, utils.width / 2, utils.height / 2)
                if d >= ring.radius * 10:
                    ring.destroyFlag = True
                    utils.world.DestroyBody(ring.body)

        # Update the current ball
        if self.current_ball:
            self.current_ball.update()

            # Check if 5 seconds have passed
            if current_time - self.ball_timer >= self.freeze_time:
                self.freeze_ball(self.current_ball)
                self.spawn_new_ball()

        # Handle ring destruction and particle spawning
        for ring in self.rings:
            if ring.destroyFlag:
                self.particles += ring.spawParticles()
                self.rings.remove(ring)
                self.sounds.playDestroySound()

        # Update particles
        for exp in self.particles:
            exp.update()
            if len(exp.particles) == 0:
                self.particles.remove(exp)

    def freeze_ball(self, ball):
        """Freezes the given ball by stopping its movement."""
        ball.circle_body.linearVelocity = (0, 0)
        ball.circle_body.angularVelocity = 0
        ball.circle_body.active = False

    def handle_ball_collisions(self):
        """Handle collisions between balls."""
        for i, ball_a in enumerate(self.balls):
            for ball_b in self.balls[i + 1:]:
                if self.check_collision(ball_a, ball_b):
                    self.resolve_collision(ball_a, ball_b)

    def check_collision(self, ball_a, ball_b):
        """Check if two balls are colliding."""
        pos_a = utils.to_Pos(ball_a.circle_body.position)
        pos_b = utils.to_Pos(ball_b.circle_body.position)
        distance = utils.distance(pos_a[0], pos_a[1], pos_b[0], pos_b[1])
        return distance <= (ball_a.radius + ball_b.radius) * utils.PPM

    def resolve_collision(self, ball_a, ball_b):
        """Resolve a collision between two balls using elastic collision physics."""
        if not ball_a.circle_body.active:
            moving_ball, frozen_ball = ball_b, ball_a
        elif not ball_b.circle_body.active:
            moving_ball, frozen_ball = ball_a, ball_b
        else:
            self.standard_collision(ball_a, ball_b)
            return

        # Play sound for collision with frozen ball
        self.sounds.play()

        pos_moving = Vector2(moving_ball.circle_body.position.x, moving_ball.circle_body.position.y)
        pos_frozen = Vector2(frozen_ball.circle_body.position.x, frozen_ball.circle_body.position.y)
        normal = (pos_moving - pos_frozen).normalize()

        velocity = Vector2(moving_ball.circle_body.linearVelocity.x, moving_ball.circle_body.linearVelocity.y)
        reflected_velocity = velocity - 2 * velocity.dot(normal) * normal

        moving_ball.circle_body.linearVelocity = reflected_velocity


    def standard_collision(self, ball_a, ball_b):
        pos_a = Vector2(ball_a.circle_body.position.x, ball_a.circle_body.position.y)
        pos_b = Vector2(ball_b.circle_body.position.x, ball_b.circle_body.position.y)

        normal = (pos_a - pos_b).normalize()
        relative_velocity = Vector2(ball_a.circle_body.linearVelocity.x, ball_a.circle_body.linearVelocity.y) - Vector2(ball_b.circle_body.linearVelocity.x, ball_b.circle_body.linearVelocity.y)
        velocity_along_normal = relative_velocity.dot(normal)

        if velocity_along_normal > 0:
            return

        restitution = 1.0
        impulse_scalar = -(1 + restitution) * velocity_along_normal
        impulse_scalar /= (1 / ball_a.radius + 1 / ball_b.radius)

        impulse = impulse_scalar * normal
        ball_a.circle_body.linearVelocity += (impulse / ball_a.radius)
        ball_b.circle_body.linearVelocity -= (impulse / ball_b.radius)

    def draw(self):
        for ring in self.rings:
            ring.draw()

        for ball in self.balls:
            ball.draw()

        for exp in self.particles:
            exp.draw()

        # Calculate the remaining time until the ball freezes
        current_time = pygame.time.get_ticks()
        time_left = max(0, (self.freeze_time - (current_time - self.ball_timer)) / 1000)  # Convert to seconds

        # Display the countdown timer
        countdown_font = pygame.font.Font(None, 70)
        countdown_text = countdown_font.render(f"{time_left:.2f}", True, (255, 255, 255))
        utils.screen.blit(countdown_text, (250, 635))