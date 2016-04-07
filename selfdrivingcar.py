from gui import GUI
from sensors import Sensors
from actuators import Actuators
from learnercar import *
import time
import sys

class SelfDrivingCar:
    def __init__(self):
        self.gui = GUI(self.run)
        self.env = self.gui.env
        self.sensors = Sensors(self.env.mainCar, self.env)
        self.actuators = Actuators(self.env.mainCar)
        self.car = LearnerCar(self.actuators, self.sensors)

        self.guiPerEpisode = int(RESULT_PER_EPISODE)
        if self.guiPerEpisode <= 0:
            self.guiPerEpisode = EPISODES_OF_LEARNING + 1

        self.episodes = 1

        self.gui.run()

    def run(self):
        while self.episodes != EPISODES_OF_LEARNING + EPISODES_OF_TESTING:

            if self.episodes > EPISODES_OF_LEARNING:
                self.car.turnOffLearning()
                print "testing episode", self.episodes - EPISODES_OF_LEARNING, ":"
            else:
                print "learning episode", self.episodes, ":"

            delayTime = 0
            if (self.episodes > EPISODES_OF_LEARNING) or (self.episodes % self.guiPerEpisode == 0):
                self.gui.turnOn()
                delayTime = 0.05
            else:
                self.gui.turnOff()

            self.env.mainCar.putOnSteetEnd(((1,3),(2,3)), 'N')

            clocks = 0
            while clocks < TIME_OUT:
                if self.env.mainCar.queue.isEmpty():
                    state = self.car.getState()
                    action = self.car.policy(state)
                    self.car.commit(action)
                    nextState = self.car.getState()
                    reward = self.car.getReward(state, action, nextState)
                    self.car.update(state, action, nextState, reward)
                    print "    iteration", clocks
                    print "\tstate:", state
                    print "\taction:", action
                    print "\tnextstate:", nextState
                    print "\treward:", reward, "\n"
                    clocks += 1

                if self.car.sensors.isHit():
                    print "Car hit"
                    break

                if self.car.sensors.isInDestination():
                    print "Car reached the goal!"
                    break

                if delayTime > 0:
                    time.sleep(delayTime)

                self.env.checkCollision()
                self.gui.update()

            self.episodes += 1
        self.gui.window.destroy()
        sys.exit()


SelfDrivingCar()