# -*- coding: utf-8 -*-
"""
Created on Sun Mar 27 12:47:57 2016

@author: amir
"""
from PIL import ImageTk
from PIL import Image
from Tkinter import *
import math
import PIL
from queue import Queue
import copy


def sign(value):
    if value < 0:
        return -1
    return 1


BLOCKSIZE = 20
FIRSTBLOCKINDEX = 1
LASTBLOCKINDEX = 10


class CarScheme:
    def __init__(self, canvas, position, env):
        self.size = (13, int(13 * 263 / 140))
        self.image = PIL.Image.open('images/car.png').resize(self.size, PIL.Image.ANTIALIAS)
        self.fimage = PIL.Image.open('images/car.png').resize(self.size, PIL.Image.ANTIALIAS)
        self.canvas = canvas
        self.position = self.fposition = position
        self.fposition = (position[0], position[1])
        self.imgOnCanvas = None
        self.ofset = (0, -2)
        self.angle = 180
        self.env = env
        self.gui = True
        self.sim = False
        self.hit = False

        self.street = None
        self.posInStreet = 0
        self.direction = None
        self.lane = None
        self.streetBlock = None
        self.guiState = None
        self.queue = Queue()

        self.actions = ['RIGHT', 'LEFT', 'STRAIGHT', 'BRAKE']

    def clone(self):
        car = copy.copy(self)
        car.sim = True
        return car

    def getTkImage(self):
        self.tkImage = ImageTk.PhotoImage(self.image)
        return self.tkImage

    def draw(self):
        if not self.sim:
            if self.imgOnCanvas:
                self.canvas.delete(self.imgOnCanvas)
                del self.tkImage
            self.imgOnCanvas = self.canvas.create_image(self.position[0], self.position[1], anchor=NW,
                                                        image=self.getTkImage())

    def rotate(self, center, init=0):
        oldCenter = self.getCenter()
        radius = math.sqrt((oldCenter[0] - center[0]) ** 2 + (oldCenter[1] - center[1]) ** 2)
        grad = math.pi * self.angle / 180
        newCenter = (center[0] + math.cos(grad) * radius, center[1] + math.sin(grad) * radius * -1)
        self.image = self.fimage.rotate(init, expand=True).rotate(self.angle, expand=True)
        self.position = (newCenter[0] - self.image.size[0] / 2, newCenter[1] - self.image.size[1] / 2)
        if not self.sim:
            self.imgOnCanvas = self.canvas.create_image(self.position[0], self.position[1], anchor=NW,
                                                        image=self.getTkImage())

    def getCenter(self):
        return (self.position[0] + self.image.size[0] / 2, self.position[1] + self.image.size[1] / 2)

    def commit(self, action):
        if action == 'RIGHT':
            pass
        elif action == 'LEFT':
            pass
        elif action == 'STRAIGHT':
            pass
        elif action == 'BRAKE':
            pass

    def turnIntersection(self, direction):
        center = None
        startAngle = None
        endAngle = None
        step = None
        finalStreet = None
        streetBlock = None
        directions = None

        if self.direction == 'N':
            if direction == 'RIGHT':
                center = (self.position[0] + 34, self.position[1] + 14)
                startAngle = 0
                endAngle = -90
                step = -1
                s = self.street
                finalStreet = ((s[0][0], s[0][1] + 1), (s[1][0] - 1, s[1][1] + 1))
                streetBlock = FIRSTBLOCKINDEX
                directions = 'E'
            elif direction == 'LEFT':
                center = (self.position[0] - 39, self.position[1] + 14)
                startAngle = 0
                endAngle = 90
                step = 1
                s = self.street
                finalStreet = ((s[0][0], s[0][1] - 1), s[0])
                streetBlock = LASTBLOCKINDEX
                directions = 'W'
        elif self.direction == 'S':
            if direction == 'RIGHT':
                center = (self.position[0] - 39 + self.image.size[1], self.position[1] + 14)
                startAngle = 0
                endAngle = -90
                step = -1
                s = self.street
                finalStreet = ((s[1][0], s[1][1] - 1), s[1])
                streetBlock = LASTBLOCKINDEX
                directions = 'W'
            elif direction == 'LEFT':
                center = (self.position[0] + 34 + self.image.size[0], self.position[1] + 12)
                startAngle = 0
                endAngle = 90
                step = 1
                s = self.street
                finalStreet = ((s[0][0] + 1, s[0][1] + 1), (s[1][0], s[1][1] + 2))
                streetBlock = FIRSTBLOCKINDEX
                directions = 'E'
        elif self.direction == 'W':
            if direction == 'RIGHT':
                center = (self.position[0] + 14, self.position[1] + 34 - self.image.size[1])
                startAngle = 0
                endAngle = -90
                step = -1
                s = self.street
                finalStreet = ((s[0][0] - 1, s[0][1]), (s[1][0], s[1][1] - 1))
                streetBlock = LASTBLOCKINDEX
                directions = 'N'
            elif direction == 'LEFT':
                center = (self.position[0] - 6, self.position[1] + 39)
                startAngle = 0
                endAngle = 90
                step = 1
                s = self.street
                finalStreet = (s[0], (s[1][0] + 1, s[1][1] - 1))
                streetBlock = FIRSTBLOCKINDEX
                directions = 'S'
        elif self.direction == 'E':
            if direction == 'RIGHT':
                center = (self.position[0] + 14, self.position[1] + 34)
                startAngle = 0
                endAngle = -90
                step = -1
                s = self.street
                finalStreet = (s[1], (s[1][0] + 1, s[1][1]))
                streetBlock = FIRSTBLOCKINDEX
                directions = 'S'
            elif direction == 'LEFT':
                center = (self.position[0] - 34, self.position[1] + 14)
                startAngle = 0
                endAngle = 90
                step = 1
                s = self.street
                finalStreet = ((s[0][0] - 1, s[0][1] + 1), s[1])
                streetBlock = LASTBLOCKINDEX
                directions = 'N'

        self.queue.push(
            {'action': 'rotate', 'step': step, 'center': center, 'startAngle': startAngle, 'endAngle': endAngle,
             'running': False, 'finalStreet': finalStreet, 'streetBlock': streetBlock, 'direction': directions})
        self.fixBlock()

    def moveToStreetEnd(self, street):
        oldpos = self.position
        x = None
        y = None
        xstep = 1
        ystep = 1
        if self.direction in ['N', 'W']:
            y = self.env.streetSpecs[street][1][0]
            x = self.env.streetSpecs[street][0][0]
        elif self.direction in ['S', 'E']:
            y = self.env.streetSpecs[street][1][1]
            x = self.env.streetSpecs[street][0][1]
        if x > oldpos[0]:
            xstep = -1
        if y > oldpos[1]:
            ystep = -1
        self.queue.push({'action': 'move', 'xstep': xstep, 'ystep': ystep, 'finalPos': (x, y), 'running': False})

    def moveToStreetHead(self, street):
        oldpos = self.position
        x = None
        y = None
        xstep = 1
        ystep = 1
        if self.direction in ['N', 'W']:
            y = self.env.streetSpecs[street][1][1]
            x = self.env.streetSpecs[street][0][1]
        elif self.direction in ['S', 'E']:
            y = self.env.streetSpecs[street][1][0]
            x = self.env.streetSpecs[street][0][0]
        if x > oldpos[0]:
            xstep = -1
        if y > oldpos[1]:
            ystep = -1
        self.queue.push({'action': 'move', 'xstep': xstep, 'ystep': ystep, 'finalPos': (x, y), 'running': False})

    def putOnSteetEnd(self, street, direction):
        y = 0
        x = 0

        if direction == 'E':
            y = self.env.streetSpecs[street][1][1]
            x = self.env.streetSpecs[street][0][1]
            self.streetBlock = LASTBLOCKINDEX
        elif direction == 'S':
            y = self.env.streetSpecs[street][1][1]
            x = self.env.streetSpecs[street][0][0]
            self.streetBlock = LASTBLOCKINDEX
        elif direction == 'N':
            y = self.env.streetSpecs[street][1][0]
            x = self.env.streetSpecs[street][0][1]
            self.streetBlock = FIRSTBLOCKINDEX
        elif direction == 'W':
            y = self.env.streetSpecs[street][1][0]
            x = self.env.streetSpecs[street][0][0]
            self.streetBlock = FIRSTBLOCKINDEX
        else:
            raise Exception('Bad direction')

        self.setDirection(direction)
        self.street = street
        self.lane = 'SAME'

        self.position = (x, y)
        self.draw()

    def putOnSteetHead(self, street, direction):
        y = 0
        x = 0

        if direction == 'E':
            y = self.env.streetSpecs[street][1][1]
            x = self.env.streetSpecs[street][0][0]
            self.streetBlock = FIRSTBLOCKINDEX
        elif direction == 'S':
            y = self.env.streetSpecs[street][1][0]
            x = self.env.streetSpecs[street][0][0]
            self.streetBlock = FIRSTBLOCKINDEX
        elif direction == 'N':
            y = self.env.streetSpecs[street][1][1]
            x = self.env.streetSpecs[street][0][1]
            self.streetBlock = LASTBLOCKINDEX
        elif direction == 'W':
            y = self.env.streetSpecs[street][1][0]
            x = self.env.streetSpecs[street][0][1]
            self.streetBlock = LASTBLOCKINDEX
        else:
            raise Exception('Bad direction')

        self.setDirection(direction)
        self.street = street
        self.lane = 'SAME'

        self.position = (x, y)
        self.draw()

    def setDirection(self, directoin):
        self.direction = directoin
        if directoin == 'N':
            self.image = self.fimage.rotate(0)
        elif directoin == 'S':
            self.image = self.fimage.rotate(180)
        elif directoin == 'W':
            self.image = self.fimage.rotate(90)
        else:
            self.image = self.fimage.rotate(-90)

    def turnStreet(self, direction):
        imgcenter = self.getCenter()
        if direction == 'RIGHT':
            if self.direction == 'S':
                center = (imgcenter[0] - 32, imgcenter[1])
                self.queue.push({'action': 'rotate', 'step': -1, 'center': center, 'startAngle': 0, 'endAngle': -45,
                                 'running': False, 'finalStreet': self.street, 'ofset': 180})

                radius = math.sqrt((center[0] - imgcenter[0]) ** 2 + (center[1] - imgcenter[1]) ** 2)
                ofset = radius * math.sin(math.pi / 4)

                newimgcenter = (imgcenter[0] - radius + ofset, imgcenter[1] + ofset)
                newcenter = (newimgcenter[0] + 26, newimgcenter[1] + 26)
                self.queue.push(
                    {'action': 'rotate', 'step': +1, 'center': newcenter, 'startAngle': 135, 'endAngle': 180,
                     'running': False, 'finalStreet': self.street, 'streetBlock': 2})
            elif self.direction == 'N':
                center = (imgcenter[0] + 32, imgcenter[1])
                self.queue.push({'action': 'rotate', 'step': -1, 'center': center, 'startAngle': 180, 'endAngle': 135,
                                 'running': False, 'finalStreet': self.street, 'ofset': 180})

                radius = math.sqrt((center[0] - imgcenter[0]) ** 2 + (center[1] - imgcenter[1]) ** 2)
                ofset = radius * math.sin(math.pi / 4)

                newimgcenter = (imgcenter[0] + radius - ofset, imgcenter[1] - ofset)
                newcenter = (newimgcenter[0] - 26, newimgcenter[1] - 26)
                self.queue.push({'action': 'rotate', 'step': 1, 'center': newcenter, 'startAngle': -45, 'endAngle': 0,
                                 'running': False, 'finalStreet': self.street, 'streetBlock': -2})
            elif self.direction == 'W':
                center = (imgcenter[0], imgcenter[1] - 32)
                self.queue.push({'action': 'rotate', 'step': -1, 'center': center, 'startAngle': 270, 'endAngle': 225,
                                 'running': False, 'finalStreet': self.street, 'ofset': 180})

                radius = math.sqrt((center[0] - imgcenter[0]) ** 2 + (center[1] - imgcenter[1]) ** 2)
                ofset = radius * math.sin(math.pi / 4)

                newimgcenter = (imgcenter[0] - ofset, imgcenter[1] - radius + ofset)
                newcenter = (newimgcenter[0] - 26, newimgcenter[1] + 26)
                self.queue.push({'action': 'rotate', 'step': +1, 'center': newcenter, 'startAngle': 45, 'endAngle': 90,
                                 'running': False, 'finalStreet': self.street, 'streetBlock': 2})
            elif self.direction == 'E':
                center = (imgcenter[0], imgcenter[1] + 32)
                self.queue.push({'action': 'rotate', 'step': -1, 'center': center, 'startAngle': 90, 'endAngle': 45,
                                 'running': False, 'finalStreet': self.street, 'ofset': 180})

                radius = math.sqrt((center[0] - imgcenter[0]) ** 2 + (center[1] - imgcenter[1]) ** 2)
                ofset = radius * math.sin(math.pi / 4)

                newimgcenter = (imgcenter[0] + ofset, imgcenter[1] + radius - ofset)
                newcenter = (newimgcenter[0] + 26, newimgcenter[1] - 26)
                self.queue.push({'action': 'rotate', 'step': 1, 'center': newcenter, 'startAngle': 225, 'endAngle': 270,
                                 'running': False, 'finalStreet': self.street, 'streetBlock': 2})

            if self.lane == 'OPPOSITE':
                self.lane = 'SAME'
            else:
                self.hit = True

        elif direction == 'LEFT':
            if self.direction == 'S':
                center = (imgcenter[0] + 32, imgcenter[1])
                self.queue.push({'action': 'rotate', 'step': 1, 'center': center, 'startAngle': 180, 'endAngle': 225,
                                 'running': False, 'finalStreet': self.street})

                radius = math.sqrt((center[0] - imgcenter[0]) ** 2 + (center[1] - imgcenter[1]) ** 2)
                ofset = radius * math.sin(math.pi / 4)

                newimgcenter = (imgcenter[0] + radius - ofset, imgcenter[1] + ofset)
                newcenter = (newimgcenter[0] - 26, newimgcenter[1] + 26)
                self.queue.push({'action': 'rotate', 'step': -1, 'center': newcenter, 'startAngle': 45, 'endAngle': 0,
                                 'running': False, 'finalStreet': self.street, 'ofset': 180, 'streetBlock': 2})
            elif self.direction == 'N':
                center = (imgcenter[0] - 32, imgcenter[1])
                self.queue.push(
                    {'action': 'rotate', 'step': 1, 'center': center, 'startAngle': 0, 'endAngle': 45, 'running': False,
                     'finalStreet': self.street})

                radius = math.sqrt((center[0] - imgcenter[0]) ** 2 + (center[1] - imgcenter[1]) ** 2)
                ofset = radius * math.sin(math.pi / 4)

                newimgcenter = (imgcenter[0] - radius + ofset, imgcenter[1] - ofset)
                newcenter = (newimgcenter[0] + 26, newimgcenter[1] - 26)
                self.queue.push(
                    {'action': 'rotate', 'step': -1, 'center': newcenter, 'startAngle': -135, 'endAngle': -180,
                     'running': False, 'finalStreet': self.street, 'ofset': 180, 'streetBlock': -2})
            elif self.direction == 'W':
                center = (imgcenter[0], imgcenter[1] + 32)
                self.queue.push({'action': 'rotate', 'step': 1, 'center': center, 'startAngle': 90, 'endAngle': 135,
                                 'running': False, 'finalStreet': self.street})

                radius = math.sqrt((center[0] - imgcenter[0]) ** 2 + (center[1] - imgcenter[1]) ** 2)
                ofset = radius * math.sin(math.pi / 4)

                newimgcenter = (imgcenter[0] - ofset, imgcenter[1] + radius - ofset)
                newcenter = (newimgcenter[0] - 26, newimgcenter[1] - 26)
                self.queue.push(
                    {'action': 'rotate', 'step': -1, 'center': newcenter, 'startAngle': -45, 'endAngle': -90,
                     'running': False, 'finalStreet': self.street, 'ofset': 180, 'streetBlock': -2})
            elif self.direction == 'E':
                center = (imgcenter[0], imgcenter[1] - 32)
                self.queue.push({'action': 'rotate', 'step': 1, 'center': center, 'startAngle': -90, 'endAngle': -45,
                                 'running': False, 'finalStreet': self.street})

                radius = math.sqrt((center[0] - imgcenter[0]) ** 2 + (center[1] - imgcenter[1]) ** 2)
                ofset = radius * math.sin(math.pi / 4)

                newimgcenter = (imgcenter[0] + ofset, imgcenter[1] - radius + ofset)
                newcenter = (newimgcenter[0] + 26, newimgcenter[1] + 26)
                self.queue.push({'action': 'rotate', 'step': -1, 'center': newcenter, 'startAngle': 135, 'endAngle': 90,
                                 'running': False, 'finalStreet': self.street, 'ofset': 180, 'streetBlock': 2})

            if self.lane == 'SAME':
                self.lane = 'OPPOSITE'
            else:
                self.hit = True

        self.fixBlock()

    def moveStraight(self):
        xstep = 0
        ystep = 0
        fp = None
        step = 1
        streetBlock = 0

        if self.direction == 'W':
            xstep = step * -1
            streetBlock -= 1
            fpd = -1 * BLOCKSIZE
            fp = (fpd, 0)
        elif self.direction == 'E':
            xstep = step
            streetBlock += 1
            fpd = BLOCKSIZE
            fp = (fpd, 0)
        elif self.direction == 'N':
            ystep = step * -1
            streetBlock -= 1
            fpd = -1 * BLOCKSIZE
            fp = (0, fpd)
        elif self.direction == 'S':
            ystep = step
            streetBlock += 1
            fpd = BLOCKSIZE
            fp = (0, fpd)

        self.queue.push({'action': 'move', 'ystep': ystep, 'xstep': xstep, 'finalPos': fp, 'running': False,
                         'streetBlock': streetBlock})

    def moveStraightInIntersection(self):
        xstep = 0
        ystep = 0
        fp = None
        step = 1
        streetBlock = 0
        street = None

        if self.direction == 'W':
            xstep = step * -1
            streetBlock = 9
            fpd = -1 * (BLOCKSIZE + 65)
            fp = (fpd, 0)
            street = (1,-1)
        elif self.direction == 'E':
            xstep = step
            streetBlock = -9
            fpd = (BLOCKSIZE + 65)
            fp = (fpd, 0)
            street = (1, 1)
        elif self.direction == 'N':
            ystep = step * -1
            streetBlock = 9
            fpd = -1 * (BLOCKSIZE + 65)
            fp = (0, fpd)
            street = (0, -1)
        elif self.direction == 'S':
            ystep = step
            streetBlock = -9
            fpd = (BLOCKSIZE + 65)
            fp = (0, fpd)
            street = (0, 1)

        self.queue.push({'action': 'move', 'ystep': ystep, 'xstep': xstep, 'finalPos': fp, 'running': False,
                         'streetBlock': streetBlock, 'street': street})

    def fixBlock(self):
        self.queue.push({'action': 'fixblock', 'running': False})

    def run(self):
        if self.queue.size() > 0:
            head = self.queue.head()
            if head['action'] == 'rotate':
                if not head['running']:
                    self.angle = head['startAngle']
                    head['running'] = True
                    if 'streetBlock' in head:
                        self.streetBlock

                ofset = 0
                if 'ofset' in head:
                    ofset = head['ofset']

                if self.angle != head['endAngle']:
                    self.rotate(head['center'], ofset)
                    self.angle += head['step']
                else:
                    self.rotate(head['center'], ofset)
                    self.queue.pop()
                    self.street = head['finalStreet']
                    if 'streetBlock' in head:
                        self.streetBlock += head['streetBlock']
                    if 'direction' in head:
                        self.direction = head['direction']
            elif head['action'] == 'move':
                if not head['running']:
                    self.slack1 = (self.position[0] + head['finalPos'][0], self.position[1] + head['finalPos'][1])
                    head['running'] = True

                nochange = True
                pos = list(self.position)
                x = 0
                y = 0
                if int(self.position[0]) != int(self.slack1[0]):
                    pos[0] += head['xstep']
                    x = head['xstep']
                    nochange = False
                if int(self.position[1]) != int(self.slack1[1]):
                    pos[1] += head['ystep']
                    y = head['ystep']
                    nochange = False
                self.position = tuple(pos)
                if not nochange:
                    if not self.sim:
                        self.canvas.move(self.imgOnCanvas, x, y)
                else:
                    self.queue.pop()
                    if 'streetBlock' in head:
                        self.streetBlock += head['streetBlock']
                    if 'street' in head:
                        s = list(self.street)
                        s = [list(s[0]), list(s[1])]
                        s[0][head['street'][0]] += head['street'][1]
                        s[1][head['street'][0]] += head['street'][1]
                        self.street = tuple([tuple(s[0]), tuple(s[1])])

            elif head['action'] == 'gopoint':
                if not head['running']:
                    self.position = (int(self.position[0]), int(self.position[1]))
                    head['finalPos'] = (int(head['finalPos'][0]), int(head['finalPos'][1]))
                    self.slack1 = 0
                    if head['hold'] != 'x':
                        if head['finalPos'][0] - int(self.position[0]) > 0:
                            self.slack1 = 1
                        elif head['finalPos'][0] - int(self.position[0]) < 0:
                            self.slack1 = -1
                    else:
                        p = list(head['finalPos'])
                        p[0] = self.position[0]
                        head['finalPos'] = tuple(p)
                    self.slack2 = 0
                    if head['hold'] != 'y':
                        if head['finalPos'][1] - int(self.position[1]) > 0:
                            self.slack2 = 1
                        elif head['finalPos'][1] - int(self.position[1]) < 0:
                            self.slack2 = -1
                    else:
                        p = list(head['finalPos'])
                        p[1] = self.position[1]
                        head['finalPos'] = tuple(p)
                    head['running'] = True

                nochange = True
                pos = list(self.position)

                if self.position[0] != head['finalPos'][0]:
                    pos[0] += self.slack1
                    nochange = False
                else:
                    self.slack1 = 0
                if self.position[1] != head['finalPos'][1]:
                    pos[1] += self.slack2
                    nochange = False
                else:
                    self.slack2 = 0

                self.position = tuple(pos)

                if not nochange:
                    if not self.sim:
                        self.canvas.move(self.imgOnCanvas, self.slack1, self.slack2)
                else:
                    self.queue.pop()
            elif head['action'] == 'fixblock':
                fp = None
                step = 1
                hold = None
                if head['running'] == False:
                    if self.direction == 'W':
                        fpd = self.env.streetSpecs[self.street][0][0] + (self.streetBlock - 1) * BLOCKSIZE
                        fp = (fpd, 0)
                        hold = 'y'
                    elif self.direction == 'E':
                        fpd = self.env.streetSpecs[self.street][0][0] + (self.streetBlock) * BLOCKSIZE
                        fp = (fpd, 0)
                        hold = 'y'
                    elif self.direction == 'N':
                        fpd = self.env.streetSpecs[self.street][1][0] + (self.streetBlock - 1) * BLOCKSIZE
                        fp = (0, fpd)
                        hold = 'x'
                    elif self.direction == 'S':
                        fpd = self.env.streetSpecs[self.street][1][0] + (self.streetBlock) * BLOCKSIZE
                        fp = (0, fpd)
                        hold = 'x'

                    self.queue.pop()
                    self.queue.pushTop(
                        {'action': 'gopoint', 'step': step, 'finalPos': fp, 'running': False, 'streetBlock': 0,
                         'hold': hold})
            elif head['action'] == 'brake':
                self.queue.pop()

    def turnOffGUI(self):
        self.gui = False

    def turnOnGUI(self):
        self.gui = True

    def simulate(self):
        while not self.queue.isEmpty():
            if self.checkCollision():
                break
            self.run()

    def brake(self):
        self.queue.push({'action': 'brake', 'running': False})

    def isInIntersection(self):
        if self.direction == 'N':
            if self.streetBlock == FIRSTBLOCKINDEX:
                return True
            return False
        elif self.direction == 'S':
            if self.streetBlock == LASTBLOCKINDEX:
                return True
            return False
        elif self.direction == 'E':
            if self.streetBlock == FIRSTBLOCKINDEX:
                return True
            return False
        elif self.direction == 'W':
            if self.streetBlock == LASTBLOCKINDEX:
                return True
            return False
        return False

    def checkCollision(self):
        """top = self.mainCar.position[1]
        bottom = top + self.mainCar.image.size[1]
        left = self.mainCar.position[0]
        right = left + self.mainCar.image.size[0]"""
        if (self.position[0] < 13) or \
                (self.position[1] < 13) or \
                (self.position[0] > 829) or \
                (self.position[1] > 567):
            self.hit = True
            return True

        if (self.position[1] > 42 and self.mainCar.position[1] < 276) or \
                (self.position[1] > 305 and self.mainCar.position[1] < 539):
            if (self.position[0] > 42 and self.mainCar.position[0] < 275) or \
                    (self.position[0] > 304 and self.mainCar.position[0] < 537) or \
                    (self.position[0] > 566 and self.mainCar.position[0] < 800):
                self.hit = True
                return True

        o = [self.street, self.streetBlock]
        if self.direction == 'W':
            o.append(0)
        elif self.direction == 'E':
            o.append(1)
        elif self.direction == 'S':
            o.append(1)
        elif self.direction == 'N':
            o.append(0)
        if tuple(o) in self.env.obstacles:
            return True

        return False

class CollisionException(Exception):
    def __init__(self, message, errors):
        super(CollisionException, self).__init__(message)
        self.errors = errors
