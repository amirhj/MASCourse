import Tkinter as tk
from Tkinter import *
from PIL import ImageTk
from PIL import Image
from environment import Environment
from carscheme import BLOCKSIZE

class GUI:
    def __init__(self, run):
        self.init(run)
        
    def init(self, run):
        self.gui = True
        self.windowSize = (1000, 600)
        self.margin = 10
        
        self.window = tk.Tk()
        self.canvas = tk.Canvas(self.window, width=self.windowSize[0], height=self.windowSize[1])
        self.canvas.pack(side=LEFT)
        
        #self.canvas.bind('<Motion>',self.getXY)
        
        self.env = Environment(self.canvas)
        
        self.drawBg()
        self.drawElements()
        
        self.label = StringVar()
        label = tk.Label(self.window, textvariable=self.label)
        label.place(x=900, y=0)

        self.window.after(0, run)
        self.window.geometry('%dx%d+%d+%d' % (self.windowSize[0],self.windowSize[1], (self.window.winfo_screenwidth()/2)-self.windowSize[0]/2,self.window.winfo_screenheight()/2-self.windowSize[1]/2))

    def run(self):
        self.window.mainloop()
        
    def drawBg(self):
        self.bgImg = ImageTk.PhotoImage(Image.open('images/city.png'))
        self.canvas.create_image(0, 0, anchor=NW, image=self.bgImg)

        self.target = ImageTk.PhotoImage(Image.open('images/target.png'))
        self.canvas.create_image(70, 18, anchor=NW, image=self.target)

        self.obs = [None, None]
        self.obs[0] = ImageTk.PhotoImage(Image.open('images/smallcone.png'))
        self.obs[1] = ImageTk.PhotoImage(Image.open('images/hole.png'))

        c = 0
        for o in self.env.obstacles:
            x = 0
            y = 0
            if self.env.getStreetPos(o[0]) == 'H':
                y = self.env.streetSpecs[o[0]][1][0]
                if o[2] == 1:
                    y = self.env.streetSpecs[o[0]][1][1]
                x = self.env.streetSpecs[o[0]][0][0] + BLOCKSIZE * o[1] - BLOCKSIZE + 2
                if c%2 == 1:
                    x += -1
            else:
                y = self.env.streetSpecs[o[0]][1][0] + BLOCKSIZE * o[1] - BLOCKSIZE + 2
                x = self.env.streetSpecs[o[0]][0][1]
                if o[2] == 1:
                    x = self.env.streetSpecs[o[0]][0][0]
                if c % 2 == 1:
                    y += -1

            self.canvas.create_image(x, y, anchor=NW, image=self.obs[c%2])
            c += 1

        """self.canvas.create_line(13,0,13,600)
        self.canvas.create_line(0,13,1000,13)
        self.canvas.create_line(829,0,829,600)
        self.canvas.create_line(0,567,1000,567)
        
        self.canvas.create_line(0,32,1000,32)
        self.canvas.create_line(0,276,1000,276)
        self.canvas.create_line(0,295,1000,295)
        self.canvas.create_line(0,539,1000,539)
        
        self.canvas.create_line(42,0,42,600)
        self.canvas.create_line(275,0,275,600)
        self.canvas.create_line(304,0,304,600)
        self.canvas.create_line(537,0,537,600)
        self.canvas.create_line(566,0,566,600)
        self.canvas.create_line(800,0,800,600)"""
    
    def drawElements(self):
        pass
    
    def getXY(self,e):
        self.label.set(str(e.x)+', '+str(e.y))
    
    def update(self):
        self.env.mainCar.run()
        self.canvas.update()

    def turnOn(self):
        self.gui = True
        self.env.mainCar.turnOnGUI()
        self.window.deiconify()

    def turnOff(self):
        self.gui = False
        self.env.mainCar.turnOffGUI()
        self.window.withdraw()
