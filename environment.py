# -*- coding: utf-8 -*-
"""
Created on Fri Mar 18 16:32:40 2016

@author: amir
"""
from carscheme import CarScheme

class Environment:
    def __init__(self, canvas):
        self.canvas = canvas
        self.mainCar = CarScheme(self.canvas, (330,280), self)
        self.objects = []
        self.intersections = [(0,0),(0,1),(0,2),(0,3),\
                                (1,0),(1,1),(1,2),(1,3),\
                                (2,0),(2,1),(2,2),(2,3)]
                                
        self.streets = [((0,0),(0,1)),((0,1),(0,2)),((0,2),(0,3)),\
                        ((0,0),(1,0)),((0,1),(1,1)),((0,2),(1,2)),((0,3),(1,3)),\
                        ((1,0),(1,1)),((1,1),(1,2)),((1,2),(1,3)),\
                        ((1,0),(2,0)),((1,1),(2,1)),((1,2),(2,2)),((1,3),(2,3)),\
                        ((2,0),(2,1)),((2,1),(2,2)),((2,2),(2,3))]
        
        self.streetSpecs = {
            ((0,0),(0,1)):((54,254),(18,37)),\
            ((0,1),(0,2)):((314,514),(18,37)),\
            ((0,2),(0,3)):((561,761),(18,37)),\
            
            ((0,0),(1,0)):((18,37),(55,253)),\
            ((0,1),(1,1)):((280,299),(55,255)),\
            ((0,2),(1,2)):((542,561),(55,255)),\
            ((0,3),(1,3)):((805,824),(55,255)),\
            
            ((1,0),(1,1)):((54,254),(281,300)),\
            ((1,1),(1,2)):((314,514),(281,300)),\
            ((1,2),(1,3)):((561,761),(281,300)),\
            
            ((1,0),(2,0)):((18,37),(318,518)),\
            ((1,1),(2,1)):((280,299),(318,518)),\
            ((1,2),(2,2)):((542,561),(318,518)),\
            ((1,3),(2,3)):((805,824),(318,518)),\
            
            ((2,0),(2,1)):((54,254),(544,562)),\
            ((2,1),(2,2)):((314,514),(544,562)),\
            ((2,2),(2,3)):((561,761),(544,562)),\
        }

        self.obstacles = [
            (((1, 1), (2, 1)), 5, 0),
            (((1,3),(2,3)), 4, 1),
            (((0,1),(0,2)), 4, 0),
            (((2,0),(2,1)), 5, 0)
        ]
                        
        self.directions = ['N','S','E','W']
        self.lane = ['SAME','OPPOSITE']
        
    def checkCollision(self):
        """top = self.mainCar.position[1]
        bottom = top + self.mainCar.image.size[1]
        left = self.mainCar.position[0]
        right = left + self.mainCar.image.size[0]"""
        if  (self.mainCar.position[0] < 13) or \
            (self.mainCar.position[1] < 13) or \
            (self.mainCar.position[0] > 829) or \
            (self.mainCar.position[1] > 567):
                self.mainCar.hit = True
                return True
        
        if  (self.mainCar.position[1] > 42 and self.mainCar.position[1] < 276) or \
            (self.mainCar.position[1] > 305 and self.mainCar.position[1] < 539):
            if  (self.mainCar.position[0] > 42 and self.mainCar.position[0] < 275) or \
                (self.mainCar.position[0] > 304 and self.mainCar.position[0] < 537) or \
                (self.mainCar.position[0] > 566 and self.mainCar.position[0] < 800):
                self.mainCar.hit = True
                return True

        o = [self.mainCar.street, self.mainCar.streetBlock]
        if self.mainCar.direction == 'W':
            o.append(0)
        elif self.mainCar.direction == 'E':
            o.append(1)
        elif self.mainCar.direction == 'S':
            o.append(1)
        elif self.mainCar.direction == 'N':
            o.append(0)
        if tuple(o) in self.obstacles:
            return True

        return False

    def getStreetPos(self, street):
        if street in [((0,0),(1,0)),((0,1),(1,1)),((0,2),(1,2)),((0,3),(1,3)), ((1,0),(2,0)), ((1,1),(2,1)),((1,2),(2,2)),((1,3),(2,3))]:
            return 'V'
        return 'H'