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
        from Box import Box
        from Ball import Ball
        # if (isinstance(bodyA.userData,Box) and isinstance(bodyB.userData,Ball)) or\
        #     (isinstance(bodyA.userData, Ball) and isinstance(bodyB.userData, Box))  :
        #     self.collisions.append((bodyA, bodyB))

        if (isinstance(bodyA.userData, Ball) and isinstance(bodyB.userData, Ball)) :
            # Get the collision position
            world_manifold = contact.worldManifold
            collision_points = world_manifold.points

            # You can process the collision points as needed
            for point in collision_points:
                print(f"Collision point: {point}")
                # For example, you can add the collision points to the collisions list
                self.collisions.append((bodyA, bodyB, point))


    def EndContact(self, contact):
        pass  # Can be implemented similarly if needed