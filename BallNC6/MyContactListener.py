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
        from Box import Box
        from BallBox import BallBox
        if (isinstance(bodyA.userData,Box) and isinstance(bodyB.userData,BallBox))\
                or (isinstance(bodyA.userData,BallBox) and isinstance(bodyB.userData,Box)):
            self.collisions.append((bodyA, bodyB))
        if (isinstance(bodyA.userData, BallBox) and isinstance(bodyB.userData, BallBox)) \
                or (isinstance(bodyA.userData, BallBox) and isinstance(bodyB.userData, BallBox)):
            self.collisions.append((bodyA, bodyB))

    def EndContact(self, contact):
        pass  # Can be implemented similarly if needed