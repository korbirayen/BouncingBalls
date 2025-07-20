from Box2D import b2ContactListener

class MyContactListener(b2ContactListener):
    def __init__(self):
        super(MyContactListener, self).__init__()
        self.collisions = []
        self.endCollisions = []

    def BeginContact(self, contact):
        bodyA = contact.fixtureA.body
        bodyB = contact.fixtureB.body
        
        if hasattr(bodyA, 'userData') and hasattr(bodyB, 'userData'):
            if bodyA.userData and bodyB.userData:
                worldManifold = contact.worldManifold
                point = worldManifold.points[0] if len(worldManifold.points) > 0 else (0, 0)
                self.collisions.append((bodyA, bodyB, point))

    def EndContact(self, contact):
        bodyA = contact.fixtureA.body
        bodyB = contact.fixtureB.body
        
        if hasattr(bodyA, 'userData') and hasattr(bodyB, 'userData'):
            if bodyA.userData and bodyB.userData:
                worldManifold = contact.worldManifold
                point = worldManifold.points[0] if len(worldManifold.points) > 0 else (0, 0)
                self.endCollisions.append((bodyA, bodyB, point))
