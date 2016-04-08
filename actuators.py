class Actuators:
    def __init__(self, carscheme):
        self.car = carscheme

    def moveStraight(self):
        if self.car.isInIntersection():
            self.car.moveStraightInIntersection()
        else:
            self.car.moveStraight()
        if self.car.sim:
            self.car.simulate()

    def turnLeft(self):
        if self.car.isInIntersection():
            self.car.turnIntersection('LEFT')
        else:
            self.car.turnStreet('LEFT')
        if self.car.sim:
            self.car.simulate()

    def turnRight(self):
        if self.car.isInIntersection():
            self.car.turnIntersection('RIGHT')
        else:
            self.car.turnStreet('RIGHT')
        if self.car.sim:
            self.car.simulate()

    def c(self):
        self.car.brake()
        if self.car.sim:
            self.car.simulate()
