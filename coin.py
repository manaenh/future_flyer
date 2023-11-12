# import
from cmu_graphics import *
import math
import random
import os, pathlib
from PIL import Image
import time

# coins! my favorite
class Coin:
    def __init__(self,x,radius,speed,time,ground):
        self.x = x
        self.radius = radius
        self.space = 13
        self.coinGroups = []
        self.speed = speed+0.8
        self.time = time
        self.collectedCoins = set()
        self.collectedNumber = 0
        self.ground = ground-20

    # for parabola coin group, generate coin parabolas
    # backtracking to make sure coins do not overlap with obstacles or exceed ceiling
    
    def getParabolaCoins(self,obstaclePos):
        startX = self.x
        startY = random.randint(10,self.ground-40)
        coef = random.uniform(1.5,2.9)
        length = random.randint(5,20)
        coinGroup = []
        if self.isParabolaLegal(startX,startY,length,coef,obstaclePos):
            for i in range(length+1):
                y = coef * (i) * (i-length)+startY
                x = startX + i*(self.radius+self.space)
                coinGroup += [[x,y]]
        else:
            self.getParabolaCoins(obstaclePos) 
        self.coinGroups += [coinGroup]

    def isParabolaLegal(self,startX,startY,length,coef,obstaclePos):
        for i in range(length+1):
            y = coef * (i) * (i-length)+startY
            x = startX + i*(self.radius+self.space)
            if y < 0:
                return False
            for i in range(len(obstaclePos)):
                nodes = obstaclePos[i]
                for node in nodes:
                    x1,x2,y1,y2 = node[0],node[0] + node[2],node[1],node[1]-node[3]
                    #print(f'x1:{x1},x2:{x2},y1:{y1},y2:{y2},flierX: {flierX},flierY:{flierY}')
                    if abs(x1-x) <= 40:
                        slope = (y2-y1)/(x2-x1)
                        crashingY = y1 + (slope)*(x-x1)
                        #print('crashingY:',crashingY,f'slope = {slope},i:{i}')
                        margin = 23
                        if abs(crashingY-y) <= 40:
                            return False
            #for node in obstaclePos:
               # for pos in node:
              #      oX,oY = pos[0],pos[1]
               #     if abs(oX-x) <= 60 and abs(oY-y) <= 60:
               #         print('too close to obstacle! try again')
                #        return False
        return True
            
    # generate coin lines
    def getLineCoinGroup(self):
        startX = self.x
        startY = random.randint(10,self.ground-20)
        coinGroup = []
        nums = random.randint(3,8)
        for num in range(nums):
            coinGroup += [[startX+num*(self.radius+self.space),startY]]
        self.coinGroups += [coinGroup]
    
    # draw coin lines
    def drawLineCoinGroup(self):
        yellow = rgb(246,215,0)
        for coinGroup in self.coinGroups:
            for position in coinGroup:
                x = position[0]
                y = position[1]
                drawCircle(x,y,self.radius,fill=yellow)

    # collect coin in coin lines
    def collectCoinsInLine(self,flierX,flierY):
        collected = False
        for i in range(len(self.coinGroups)):
            coinGroup = self.coinGroups[i]
            j = 0
            while j < len(coinGroup):
                position = coinGroup[j]
                x,y = position[0],position[1]
                if abs(flierX-x)<=20+self.radius and abs(flierY-y)<=20+self.radius:
                    collected = True
                    self.coinGroups[i].pop(j)
                    self.collectedNumber += 1
                else:
                    j += 1
        return collected

    # coin lines are moving
    def coinLinesMoving(self):
        self.time += 1
        i = 0
        while i < len(self.coinGroups):
            coinGroup = self.coinGroups[i]
            lastCoinIndex = len(coinGroup)-1
            if coinGroup != []:
                lastX = self.coinGroups[i][lastCoinIndex-1][0]
            if coinGroup == []:
                self.coinGroups.pop(i)
            elif lastX > 0 - self.radius:
                for j in range(len(coinGroup)):
                    self.coinGroups[i][j][0] -= self.speed
                i += 1
            else:
                self.coinGroups.pop(i)

    # general
    def generateNewCoinGroup(self,ground,ceiling,leftWall,rightWall,obstaclePos):
        if self.time == 0 or self.time % int(800/self.speed) == 0:
            index = random.randint(0,1)
            if index == 0:
                self.getLineCoinGroup()
            elif index == 1:
                self.getParabolaCoins(obstaclePos)
        if self.time % 500 == 0:
            self.speed += 1
        
    def __hash__(self):
        return hash(str(self))
    
    def drawCollectedCoinsNumber(self,x,y,size,opacity):
        color1 = rgb(249,239,29)
        drawLabel(f'{self.collectedNumber}',x,y,fill=color1,bold=True,size=size,opacity=opacity)
    
    # magnet power up
    def magnetPowerUp(self,flierX,flierY,level):
        speed = level * 10
        magnetStrength = level * 100
        self.time += 1            
        i = 0
        while i < len(self.coinGroups):
            coinGroup = self.coinGroups[i]
            lastCoinIndex = len(coinGroup)-1
            if coinGroup != []:
                lastX = self.coinGroups[i][lastCoinIndex-1][0]
            
            if coinGroup == []:
                self.coinGroups.pop(i)
            elif lastX > 0 - self.radius:
                for j in range(len(coinGroup)):
                    x = self.coinGroups[i][j][0]
                    y = self.coinGroups[i][j][1]
                    if abs(flierX-x)<=magnetStrength and abs(flierY-y)<=magnetStrength:
                        if x < flierX:
                            self.coinGroups[i][j][0] += speed
                        else:
                            self.coinGroups[i][j][0] -= speed
                        if y < flierY:
                            self.coinGroups[i][j][1] += speed
                        else:
                            self.coinGroups[i][j][1] -= speed
                    else:
                        self.coinGroups[i][j][0] -= self.speed
                i += 1
            else:
                self.coinGroups.pop(i)