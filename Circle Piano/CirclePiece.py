import pygame
from Box2D import b2World, b2BodyDef, b2PolygonShape, b2_dynamicBody, b2Filter
from pygame import Vector2

from util import utils, PIECE, BALL

class CirclePiece:
    def __init__(self,id, points, color):
        # Store the polygon points and color
        self.id = id
        self.points = points
        self.color = color
        self.lives = 3

        # Convert Pygame coordinates to Box2D coordinates
        box2d_points = [utils.from_Pos(point) for point in self.points]

        # Define the dynamic body
        body_def = b2BodyDef()
        body_def.type = b2_dynamicBody
        body_def.position = (0, 0)
        body_def.gravityScale = 0  # No gravity effect

        # Create the body
        self.body = utils.world.CreateBody(body_def)
        self.body.userData = self

        # Define the polygon shape
        polygon_shape = b2PolygonShape(vertices=box2d_points)

        # Create the fixture with density, friction, and restitution
        self.body.CreateFixture(shape=polygon_shape, density=1.1, friction=0, restitution=1.0,
                                filter=b2Filter(categoryBits=PIECE, maskBits=BALL))

        self.destroyFlag = False
        self.body.angle = 0
        self.body.fixedRotation = True
        self.startPosition = Vector2(0, 0)
        self.movingBack = False
        self.time = 0

    def startMovingBack(self):
        self.movingBack = True
        self.time = 1


    def update(self):
        if self.movingBack:
            self.time -= utils.deltaTime()
            if self.time > 0:
                return
            # Get the current position
            current_position = Vector2(self.body.position[0],self.body.position[1])

            # Calculate the difference between the current position and the start position
            position_diff = self.startPosition - current_position
            # Move towards the starting position
            if position_diff.length() > 0.1:  # Small threshold to stop
                move_step = position_diff.normalize() * 1  # Move a small step
                self.body.position += (move_step.x, move_step.y)  # Update Box2D body position

            # Check if we have reached the start position
            if position_diff.length() <= 0.1:
                self.movingBack = False  # Stop moving back when we reach the target
                self.body.linearVelocity = (0, 0)

    def draw(self):
        # Get the transformed vertices from the body to draw the polygon
        transformed_points = [utils.to_Pos(self.body.GetWorldPoint(vertex)) for vertex in self.body.fixtures[0].shape.vertices]
        pygame.draw.polygon(utils.screen, self.color, transformed_points)
        pygame.draw.polygon(utils.screen, (23, 23, 23), transformed_points, 4)
