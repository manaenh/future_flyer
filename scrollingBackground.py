# import
from cmu_graphics import *
import math
import random
import os, pathlib
from PIL import Image
import time 

# scrolling environment
class Background:
    def __init__(self,speed,rightWall):
        self.rightWall = rightWall
        self.firstLayer = [[rightWall,random.randint(80,150),random.randint(100,200)]]
        self.firstLayerSpeed = speed
        self.secondLayer = [[rightWall+100,random.randint(80,100),random.randint(200,400)]]
        self.secondLayerSpeed = speed * 0.8
        self.thirdLayer = [[rightWall+200,random.randint(80,100),random.randint(200,400)]]
        self.thirdLayerSpeed = speed * 0.5
        self.skyscraper = [[rightWall+300,random.randint(50,80),random.randint(400,520)]]
        self.skyscraperSpeed = speed * 0.7

    def generateFirstLayerBuilding(self):
        lastBuildingIndex = len(self.firstLayer)-1
        lastBuildingPosition = self.firstLayer[lastBuildingIndex][0]+self.firstLayer[lastBuildingIndex][1]
        if  lastBuildingPosition < self.rightWall:
            width = random.randint(100,400)
            space = random.randint(30,260)
            height = random.randint(50,400)
            x = lastBuildingPosition + space
            self.firstLayer += [[x,width,height]]

    
    def generateSecondLayerBuilding(self):
        lastBuildingIndex = len(self.secondLayer)-1
        lastBuildingPosition = self.secondLayer[lastBuildingIndex][0]+self.secondLayer[lastBuildingIndex][1]
        if  lastBuildingPosition < self.rightWall:
            width = random.randint(80,300)
            space = random.randint(10,130)
            height = random.randint(150,550)
            x = lastBuildingPosition + space
            self.secondLayer += [[x,width,height]]
    
    def generateSkyscraper(self):
        lastBuildingIndex = len(self.skyscraper)-1
        lastBuildingPosition = self.skyscraper[lastBuildingIndex][0]+self.skyscraper[lastBuildingIndex][1]
        if  lastBuildingPosition < self.rightWall:
            width = random.randint(50,110)
            space = random.randint(700,1300)
            height = random.randint(400,520)
            x = lastBuildingPosition + space
            self.skyscraper += [[x,width,height]]
    
    def generateThirdLayerBuilding(self):
        lastBuildingIndex = len(self.thirdLayer)-1
        lastBuildingPosition = self.thirdLayer[lastBuildingIndex][0]+self.thirdLayer[lastBuildingIndex][1]
        if  lastBuildingPosition < self.rightWall:
            width = random.randint(80,250)
            space = random.randint(10,130)
            height = random.randint(200,650)
            x = lastBuildingPosition + space
            self.thirdLayer += [[x,width,height]]
    
    def drawBackground(self,ground,screenWidth,screenHeight):
        

        # draw the very back
        colorSky1 = rgb(70,70,70)
        colorSky2 = rgb(30,30,40)
        drawRect(0,0,screenWidth,screenHeight,fill=gradient(colorSky2,colorSky1,start='top'))

        # draw 3rd layer
        color3 = rgb(92,53,106)
        for building3 in self.thirdLayer:
            x3 = building3[0]
            width3 = building3[1]
            height3 = building3[2]
            drawRect(x3,screenHeight,width3,height3,align='left-bottom',fill=color3,opacity=50)
        
        # draw skyscraper
        skyscraperColor = rgb(168,228,226)
        for building in self.skyscraper:
            x = building[0]
            width = building[1]
            height = building[2]
            drawRect(x,screenHeight,width,height,align='left-bottom',fill=skyscraperColor)
            widthSmaller = width*0.8
            cx = (x+(x+width))//2
            smallRectHeight = 20
            drawRect(cx,screenHeight-height,widthSmaller,smallRectHeight,align='bottom',fill=skyscraperColor)
            triangleWidth = widthSmaller * 0.5
            drawRegularPolygon(cx,screenHeight-height-smallRectHeight,triangleWidth,3,fill=skyscraperColor,align='bottom')
            topHeight = 50
            topStart = screenHeight-height-smallRectHeight-triangleWidth
            drawLine(cx,topStart,cx,topStart-topHeight,lineWidth=3,fill=skyscraperColor)

        # draw second layer of building
        color2 = rgb(69,50,116)
        for building2 in self.secondLayer:
            x2 = building2[0]
            width2 = building2[1]
            height2 = building2[2]
            drawRect(x2,screenHeight,width2,height2,align='left-bottom',fill=color2)

        # draw first layer of building
        color1 = rgb(42,28,63)
        for building1 in self.firstLayer:
            x1 = building1[0]
            width1 = building1[1]
            height1 = building1[2]
            drawRect(x1,screenHeight,width1,height1,align='left-bottom',fill=color1)
        # draw ground
        roof = ground - 50
        drawRect(0,roof,screenWidth,screenHeight-roof)
        
        
    
    def buildingMoving(self):
        i = 0
        while i < len(self.firstLayer):
            building = self.firstLayer[i]
            if building[0]+building[1] > 0:
                self.firstLayer[i][0] -= self.firstLayerSpeed
                i += 1
            else:
                self.firstLayer.pop(i)
        
        i = 0 
        while i < len(self.secondLayer):
            building = self.secondLayer[i]
            if building[0]+building[1] > 0:
                self.secondLayer[i][0] -= self.secondLayerSpeed
                i += 1
            else:
                self.secondLayer.pop(i)
        
        i = 0 
        while i < len(self.thirdLayer):
            building = self.thirdLayer[i]
            if building[0]+building[1] > 0:
                self.thirdLayer[i][0] -= self.thirdLayerSpeed
                i += 1
            else:
                self.thirdLayer.pop(i)
        
        i = 0 
        while i < len(self.skyscraper):
            building = self.skyscraper[i]
            if building[0]+building[1] > 0:
                self.skyscraper[i][0] -= self.skyscraperSpeed
                i += 1
            else:
                self.skyscraper.pop(i)


