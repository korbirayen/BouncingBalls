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
        from Polygon import Polygon
        from OuterSquareRing import OuterSquareRing
        from Ball import Square
        if (isinstance(bodyA.userData,OuterSquareRing) and isinstance(bodyB.userData,Square))\
                or (isinstance(bodyA.userData,Square) and isinstance(bodyB.userData,Square)):
            self.collisions.append((bodyA, bodyB))
            sounds.play()

    def EndContact(self, contact):
        pass  # Can be implemented similarly if needed