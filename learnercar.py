from learnignagent import LearningAgent
import util
import random

EPISODES_OF_LEARNING = 10
EPISODES_OF_TESTING = 10
RESULT_PER_EPISODE = 1
TIME_OUT = 100

# *** Learning Parameters ****
LEARNING_RATE = 0.9
DISCOUNT_FACTOR = 0.8
EPSILON = 0.9


class LearnerCar(LearningAgent):

    def __init__(self, actuators, sensors):
        LearningAgent.__init__(self, sensors, actuators, LEARNING_RATE, DISCOUNT_FACTOR, EPSILON)

        """
        Put your code here if you want to do something before start of learning.
        """
        # YOUR CODE HERE

    def getActions(self):
        """
        Return an array of actions you choose for learning. Every action is a string.
        """

        # YOUR CODE HERE
        return []

    def update(self, state, action, nextState, reward):
        """
        This function updates Q-Values ny given parameters.
        """
        nextQ = []
        for a in self.getActions():
            nextQ.append(self.qvalues[(nextState, a)])
        sample = reward + self.discount_factor * max(nextQ)
        self.qvalues[(state, action)] = self.qvalues[(state, action)]*(1-self.learning_rate) + self.learning_rate*sample

    def getState(self):
        """
        This function return current state of agent. A state must be a tuple of parameters.
        Parameters must be strings or digits or tuples. A state must describes the state of agent efficiently.
        Use must use self.sensors to get values of sensors.
        Sensors show location and moving direction of car, which lane it is,
        is there obstacle or intersection in front and is current location the destination or not.
        """

        # YOUR CODE HERE
        return None

    def commit(self, action):
        """
        Every action commits its task here. Use self.actuators to make car do something.
        """

        # YOUR CODE HERE
        pass

    def policy(self, state):
        """
        Given state what is the proper action according to Q-values. Use self.qvalues to access them.
        This function should return proper action. Type of actions is string.
        """
        nextQ = util.Counter()
        for a in self.getActions():
            nextQ[a] = self.qvalues[(state, a)]
        if util.flipCoin(self.epsilon):
            return nextQ.argMax()
        else:
            del nextQ[nextQ.argMax()]
            return random.choice(nextQ.keys())

    def getReward(self, state, action, nextState):
        """
        This function calculates reward according to current state, action taken in current state and next state.
        Return value must be a number.
        """

        # YOUR CODE HERE
        return None

    def episodTerminationEvent(self):
        """
        This method is called after termination of each episode of learning.
        If you want to do something do it here or let it empty.
        """

        # YOUR CODE HERE
        pass

    def learningTerminationEvent(self):
        """
        This method is called after termination of learning.
        If you want to do something do it here or let it empty.
        """

        # YOUR CODE HERE
        pass
