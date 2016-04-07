# -*- coding: utf-8 -*-
"""
Created on Mon Mar 21 13:56:10 2016

@author: amir
"""

class Queue:
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return len(self.items) == 0

    def push(self, item):
        self.items.insert(0,item)
    
    def pushTop(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop()

    def size(self):
        return len(self.items)
    
    def head(self):
        return self.items[-1]