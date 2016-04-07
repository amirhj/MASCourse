from learnignagent import LearningAgent

EPISODES_OF_LEARNING = 10
EPISODES_OF_TESTING = 10
RESULT_PER_EPISODE = 1
LEARNING_RATE = 0.9
DISCOUNT_FACTOR = 0.8
TIME_OUT = 100


class LearnerCar(LearningAgent):

    def __init__(self, actuators, sensors):
        LearningAgent.__init__(self, sensors, actuators, LEARNING_RATE, DISCOUNT_FACTOR)

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
        pass

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

        # YOUR CODE HERE
        return None

    def getReward(self, state, action, nextState):
        """
        This function calculates reward according to current state, action taken in current state and next state.
        Return value must be a number.
        """

        # YOUR CODE HERE
        return None

