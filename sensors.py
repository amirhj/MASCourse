class Sensors:
    def __init__(self, carscheme, env):
        self.car = carscheme
        self.env = env

    def getLane(self):
        return self.car.lane

    def getLocation(self):
        return self.car.street

    def isThereObstacle(self):
        o = [self.car.street]
        if self.car.direction == 'W':
            o.append(self.car.streetBlock - 2)
            o.append(0)
        elif self.car.direction == 'E':
            o.append(self.car.streetBlock + 2)
            o.append(1)
        elif self.car.direction == 'S':
            o.append(self.car.streetBlock + 2)
            o.append(1)
        elif self.car.direction == 'N':
            o.append(self.car.streetBlock - 2)
            o.append(0)
        if tuple(o) in self.env.obstacles:
            return True
        return False

    def isInIntersection(self):
        return self.car.isInIntersection()

    def isHit(self):
        return self.car.hit

    def getMoveingDirection(self):
        return self.car.direction

    def isInDestination(self):
        if self.car.street == ((0, 0), (0, 1)) and self.car.streetBlock == 1:
            return True
        return False