from util import Counter
from actuators import Actuators
from sensors import Sensors

class LearningAgent:

    def __init__(self, sensors, actuators, learning_rate, discount_factor, epsilon):
        self.sensors = sensors
        self.actuators = actuators
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.epsilon = epsilon

        self.qvalues = Counter()

    def turnOffLearning(self):
        self.learning_rate = 0
        self.discount_factor = 0

    def getActions(self):
        return []

    def update(self, state, action, nextState, reward):
        pass

    def getState(self):
        pass

    def commit(self, action):
        pass

    def policy(self, state):
        pass
