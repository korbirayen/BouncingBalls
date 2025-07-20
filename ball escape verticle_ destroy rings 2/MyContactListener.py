import Box2D
from Box2D import b2ContactListener

from sounds import sounds


class MyContactListener(b2ContactListener):
    def __init__(self):
        super(MyContactListener, self).__init__()
        self.collisions = []

    def BeginContact(self, contact):
        fixtureA = contact.fixtureA
        fixtureB = contact.fixtureB
        bodyA = fixtureA.body
        bodyB = fixtureB.body

        # Check if one of the fixtures is the circle and the other is the box
        from Ball import Ball
        from RingB import RingB
        if (isinstance(bodyA.userData,RingB) and isinstance(bodyB.userData,Ball))\
                or (isinstance(bodyA.userData,Ball) and isinstance(bodyB.userData,RingB)):
            self.collisions.append((bodyA, bodyB))
            sounds.play()

        from Line import Line
        if (isinstance(bodyA.userData,Line) and isinstance(bodyB.userData,Ball))\
                or (isinstance(bodyA.userData,Ball) and isinstance(bodyB.userData,Line)):
            self.collisions.append((bodyA, bodyB))
            sounds.play()

    def EndContact(self, contact):
        pass  # Can be implemented similarly if needed