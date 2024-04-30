#python program to find shortest path from one block to another with hueristic algorithm 

#importing modules

import os
import sys
import math
import pygame
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

sc = pygame.display.set_mode((700,700))

#class 
class cells:
    def __init__(self,a,b):
        self.i = a
        self.j = b
        self.f = 0
        self.g = 0
        self.h = 0
        self.value = 1
        self.obs = False
        self.closed = False
        self.previous = None
        self.neighbours = []
    #show cells
    def show(self,color,st):
        if self.closed == False:
            pygame.draw.rect(sc,color,(self.i*w,self.j*h,w,h),st)
            pygame.display.update()
    #find neighbours
    def my_neighboures(self, grid):
        i = self.i
        j = self.j
        
        if i < row-1 and grid[i+1][j].obs == False:
            self.neighbours.append(grid[i+1][j])
        if i > 0 and grid[i-1][j].obs == False:
            self.neighbours.append(grid[i-1][j])
        if j < col-1 and grid[i][j+1].obs == False:
            self.neighbours.append(grid[i][j+1])
        if j > 0 and grid[i][j-1].obs == False:
            self.neighbours.append(grid[i][j-1])
            
#globaly used variables
           
row = 25
col = 25
openSet = []
closedSet = []
w = 700/row
h = 700/col
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
white = (255,255,255)
success = (22,129,14)
spot = (252,219,7)


#1d array
table = [0 for i in range(row)]

# 2d array 
for i in range(row):
    table[i] = [0 for j in range(col)]
    
for i in range(row):
    for j in range(col):
        table[i][j] = cells(i,j)
        table[i][j].show(white,1)
        
start = table[2][2]
end = table[22][22]

#creating boundries
for i in range(row):
    #print(i)
    table[i][0].obs = True
    table[i][0].show(white,0)
    table[0][col-1-i].obs = True
    table[0][col-1-i].show(white,0)
    table[i][col-1].obs = True
    table[i][col-1].show(white,0)
    table[row-1][col-1-i].obs = True
    table[row-1][col-1-i].show(white,0)


def onsubmit():
    global start,end
    st = startbox.get().split(',')
    ed = endbox.get().split(',')
    start = table[int(st[0])][int(st[1])]
    end = table[int(ed[0])][int(ed[1])]
    start.show(spot,0)
    end.show(spot,0)
    openSet.append(start)
    window.quit()
    window.destroy()
 
window = Tk()
labala = Label(window, text='Starting Value (x,y)')
startbox = Entry(window)
labalb = Label(window, text='Ending Value (x,y)')
endbox = Entry(window)
var = IntVar()
showpath = ttk.Checkbutton(window,text='Show Path', onvalue=1,offvalue=0,variable=var)
submit = Button(window,text='Submit',command=onsubmit)

labala.grid(row=0,column=0,pady=3)
startbox.grid(row=0,column=1,pady=3)
labalb.grid(row=1,column=0,pady=3)
endbox.grid(row=1,column=1,pady=3)
showpath.grid(row=2,column=1,pady=3)
submit.grid(row=3,column=1,pady=3)

window.update()
mainloop()
pygame.init()

def onmousepress(x):
    w = x[0]
    h = x[1]
    x1 = w // ( 700 // row)
    x2 = h // ( 700 // col)
    access = table[x1][x2]
    if access != start and access != end:
        if access.closed == False:
            access.obs = True
            access.show(white,0)
    
    
    
loop = True
while loop:
    ev = pygame.event.get()
    for event in ev:
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                loop = False
                break
        if pygame.mouse.get_pressed()[0]:
            try:
                pos = pygame.mouse.get_pos()
                onmousepress(pos)
            except AttributeError:
                pass


#
for i in range(row):
    for j in range(col):
        table[i][j].my_neighboures(table)
        
        
def heuristic(c,e):
    d = math.sqrt((c.i-e.i)**2 + (c.j-e.j)**2)
    return d
    
    
def main():
    start.show(spot,0)
    end.show(spot,0)
    if len(openSet) > 0:
        lowerIndex = 0
        for i in range(len(openSet)):
            if openSet[i].f < openSet[lowerIndex].f:
                lowerIndex = i
        
        current = openSet[lowerIndex]
        if current == end:
            start.show(spot,0)
            tempF = int(current.f)
            print('Done ', tempF)
            for i in range(tempF):
                current.closed = False
                current.show(success,0)
                current = current.previous
            end.show(spot,0)
            pygame.display.update()
            Tk().wm_withdraw()
            result = messagebox.askokcancel('Path Found ',('Run Again ??'))
            if result:
                os.execl(sys.executable,sys.executable, *sys.argv)
            else:
                ag = True
                while ag:
                    ev = pygame.event.get()
                    for event in ev:
                        if event.type == pygame.QUIT:
                            ag = False
                            break
            pygame.quit()
        
        openSet.pop(lowerIndex)
        closedSet.append(current)
        
        neighbourss = current.neighbours
        
        for i in range(len(neighbourss)):
            nc = neighbourss[i]
            if nc not in closedSet:
                tempG = current.g + current.value
                if nc in openSet:
                    if nc.g > tempG:
                        nc.g = tempG
                else:
                    nc.g = tempG
                    openSet.append(nc)
                    
                nc.h = heuristic(nc,end)
                nc.f = nc.g + nc.h
            if nc.previous == None:
                nc.previous = current
                
    if var.get():        
        for i in range(len(openSet)):
            openSet[i].show(green,0)
        for i in range(len(closedSet)):
            if closedSet[i] != start and closedSet[i] != end:
                closedSet[i].show(red,0)
    current.closed = True   

while True:
    ev = pygame.event.poll()
    if ev.type == pygame.QUIT:
        pygame.quit()
    pygame.display.update()
    main()
        
          
                
    