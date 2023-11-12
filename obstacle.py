from cmu_graphics import *
import random
from PIL import Image
import os, pathlib

# making a new file just for class, learned from Mingjing Zhao

class Obstacle:
    def __init__(self,time,speed):
        self.time = time
        self.speed = speed
        self.distance = 0

        # for hacking nodes
        self.hackingNodes = []
        self.hackingNodesPosition = []
        self.hackingNodesFirst = []
        self.hackingNodeWidth = 3
        # for drones
        self.prepareDrone = False
        self.droneSpeed = speed*1.2
        self.droneCounter = 0
        self.droneY = None
        self.droneY = random.randint(10,400)
        self.droneX = 1000
        self.arrowOpacity = 100
        self.arrow = True
        self.droneStart = False
        self.launchTime = 0
        self.droneIsComing = False
    
    # hacking nodes obstacle
    # backtracking, nodes shouldn't overlap too much
    def isHackingNodesLegal(self,nodeLengths,x,y,ceiling,ground):
        i = 1
        while i < len(nodeLengths):
            xL1,xL2,yL1,yL2 = nodeLengths[i-1][0],nodeLengths[1][0],nodeLengths[i-1][1],nodeLengths[i][1]
            if abs(xL1+xL2) <= 10 or abs(yL1+yL2) <= 10:
                return False
            i += 1
        i = 0
        while i < len(nodeLengths):
            yL = nodeLengths[i][1]
            if y-yL < ceiling or y-yL > ground:
                return False
            i+=1
        return True
    
    def getHackingNodes(self,y,ceiling,ground,rightWall,nodes):
        hackingNode = []
        lastX = firstX = x = rightWall+300
        nodeLengths = []
        for i in range(nodes):
            if nodes == 1:
                xLength = random.randint(90,150)
                yLength = random.randint(10,50)
            else:
                xLength = random.choice([random.randint(-120,-70),random.randint(70,120)])
                yLength = random.choice([random.randint(-40,-20),random.randint(20,40)])
            nodeLengths += [[xLength,yLength]]

        if self.isHackingNodesLegal(nodeLengths,x,y,ceiling,ground):
            for i in range(nodes):
                xLength,yLength = nodeLengths[i][0],nodeLengths[i][1]
                hackingNode += [[x,y,xLength,yLength]]
                x = x+xLength
                if x > lastX:
                    lastX = x
                if x < firstX:
                    firstX = x
                y = y-yLength
            self.hackingNodes += [hackingNode]
            self.hackingNodesPosition += [lastX]
            self.hackingNodesFirst += [firstX]
        else:
            self.getHackingNodes(y,ceiling,ground,rightWall,nodes)
    
    def hackingNodesAnimation(self):
        if self.time % 7 == 0:
            if self.hackingNodeWidth < 5:
                self.hackingNodeWidth  += 1
            elif self.hackingNodeWidth  == 5:
                self.hackingNodeWidth=1
        

    # draw hacking nodes
    def drawHackingNodes(self):
        yellow = rgb(246,215,0)
        lightYellow = rgb(246,238,141)
        lightOrange = rgb(255,172,62)
        yeorange = gradient(lightOrange,yellow)
        light = gradient(lightYellow,yellow)
        for nodes in self.hackingNodes:
            for node in nodes:
                x, y, xL, yL = node[0],node[1],node[2],node[3]
                drawCircle(x,y,6,fill=light)
                drawLine(x,y,x+xL,y-yL,fill=yeorange,lineWidth=self.hackingNodeWidth)
                drawCircle(x+xL,y-yL,6,fill=light)
    
    # hacking nodes moving
    def moveHackingNodes(self):
        self.hackingNodesAnimation()
        self.time += 1
        i = 0
        while i < len(self.hackingNodes):
            nodes = self.hackingNodes[i]
            lastX = self.hackingNodesPosition[i]
            if lastX > 0:
                for node in nodes:
                    node[0] -= self.speed
                self.hackingNodesPosition[i] -= self.speed
                self.hackingNodesFirst[i] -= self.speed
                i += 1
            else:
                self.hackingNodes.pop(i)
                self.hackingNodesPosition.pop(i)
                self.hackingNodesFirst.pop(i)

    # generate new random hacking nodes after certain time            
    def generateNewHackingNodes(self,ground,ceiling,leftWall,rightWall):
        if self.time == 0 or self.time % int(850/self.speed) == 0:
            y = random.randrange(ceiling+20,ground)
            nodes = random.randint(1,3)
            self.getHackingNodes(y,ceiling+10,ground,rightWall,nodes)
        if self.time % 500 == 0:
            self.speed += 1
        self.distance = (self.time*self.speed)//10

    def crashHackingNodes(self,flierX,flierY):
        for i in range(len(self.hackingNodes)):
            nodes = self.hackingNodes[i]
            start = self.hackingNodesFirst[i]
            for node in nodes:
                x1,x2,y1,y2 = node[0],node[0] + node[2],node[1],node[1]-node[3]
                #print(f'x1:{x1},x2:{x2},y1:{y1},y2:{y2},flierX: {flierX},flierY:{flierY}')
                if min(x1,x2) <= flierX <= max(x1,x2):
                    slope = (y2-y1)/(x2-x1)
                    crashingY = y1 + (slope)*(flierX-x1)
                    #print('crashingY:',crashingY,f'slope = {slope},i:{i}')
                    margin = 23
                    if abs(crashingY-flierY) <= margin:
                        return True
##################################################################################################################################
    # for drones!
    def droneAnimation(self):
        if self.droneStart:
            self.droneCounter += 1
        
        if 0 < self.droneCounter < 150:
            if self.arrow:
                self.arrowOpacity = 100
                self.arrow = False
            elif not self.arrow:
                self.arrowOpacity = 0
                self.arrow = True
            
    def crashDrone(self,flierX,flierY):
        if abs(self.droneX-flierX) <= 40 and abs(self.droneY-flierY) <= 40:
            self.droneStart = False
            return True
        
    def drawDrone(self):
        droneMark = Image.open('images/droneLooking.png')
        mark = CMUImage(droneMark.crop((0,0,25,40)))
        arrow = CMUImage(droneMark.crop((25,0,40,40)))
        ready = Image.open('images/readyLaunch.png')
        readyWidth,readyHeight=ready.width,ready.height
        ready = CMUImage(ready)
        drone = Image.open('images/drone1.png')
        droneWidth,droneHeight = drone.width,drone.height
        drone = CMUImage(drone)

        if self.droneCounter < 150:
            drawImage(mark,self.droneX-18,self.droneY,align='right',width=37.5,height=60)
            drawImage(arrow,self.droneX-7,self.droneY,opacity=self.arrowOpacity,align='right',width=22.5,height=60)
        elif 150 <= self.droneCounter < 180:
            drawImage(ready,self.droneX-10,self.droneY,align='right',width=readyHeight*1.3,height=readyHeight*1.5)
        else:
            drawImage(drone,self.droneX,self.droneY,width=droneWidth*1.3,height=droneHeight*1.3)

    def droneMoving(self,flierY,ground,rightWall):
        self.time += 1
        if self.droneStart:
            if self.droneCounter < 150:
                self.droneY = flierY
            elif 150 <= self.droneCounter < 180:
                self.droneIsComing = True
            elif self.droneCounter > 180:
                self.droneIsComing = False
                self.droneX -= self.droneSpeed * 3
        if self.droneX < -10:
            self.droneStart = False
            self.droneY = random.randint(10,ground-10)
            self.droneX = rightWall

    def generateNewDrones(self):
        #print(f'prepare:{self.prepareDrone},drone start: {self.droneStart}')
        if not self.prepareDrone and not self.droneStart:
            self.launchTime = self.time + random.randint(100,1000)
            self.droneCounter = 0
            self.prepareDrone = True
        #print(f'launch time: {self.launchTime},current time: {self.time}')
        if self.time == self.launchTime:
            self.prepareDrone = False
            self.droneStart = True
        if self.time % 500 == 0:
            self.droneSpeed += 1
        
                        

    def drawDistanceStatus(self,x,y,size,align,opacity):
        drawLabel(f'{self.distance} M',x,y,fill='white',bold=True,size=size,font='Courier New',align=align,border='black',borderWidth=1,opacity=opacity)