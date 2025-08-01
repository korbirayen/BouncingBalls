import Box2D
from Box2D import b2ContactListener
from pygame import Vector2

from sounds import sounds


class MyContactListener(b2ContactListener):
    def __init__(self):
        super(MyContactListener, self).__init__()
        self.beginCollisions = []
        self.endCollisions = []

    def BeginContact(self, contact):
       pass

    def EndContact(self, contact):
        fixtureA = contact.fixtureA
        fixtureB = contact.fixtureB
        bodyA = fixtureA.body
        bodyB = fixtureB.body

        manifold = contact.worldManifold
        collision_point = manifold.points[0]

        # Check if one of the fixtures is the circle and the other is the box
        from Box import Box
        from Ball import Ball
        from Line import Line
        if (isinstance(bodyA.userData, Ball) and isinstance(bodyB.userData, Line)) or \
                (isinstance(bodyA.userData, Line) and isinstance(bodyB.userData, Ball)):
            self.beginCollisions.append((bodyA, bodyB, Vector2(collision_point[0], collision_point[1])))

        from StaticBall import StaticBall
        if (isinstance(bodyA.userData, Ball) and isinstance(bodyB.userData, StaticBall)):
            self.beginCollisions.append((bodyA, bodyB, Vector2(collision_point[0], collision_point[1])))