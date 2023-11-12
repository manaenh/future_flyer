# import
from cmu_graphics import *
import math
import random
import os, pathlib
from PIL import Image
import time 
import ast

class StartStatus:
    def __init__(self,y,screenWidth,screenHeight):
        self.y=y
        self.screenWidth = screenWidth
        self.screenHeight = screenHeight
        self.transition = False
        self.opacity = 100
        self.fade = False

        #opacity
        self.backgroundOpacity = 80
        self.settingOpacity = 60
        self.storeOpacity = 60

        #status
        self.settingOn = False
        self.storeOn = False

    def drawStartBackground(self):
        # background color
        colorSky1 = rgb(70,70,70)
        colorSky2 = rgb(30,30,40)
        drawRect(0,0,self.screenWidth,self.screenHeight*2,fill=gradient(colorSky2,colorSky1,start='top'))
        # draw start screen
        skyBackground = Image.open('images/startBackground.png')
        skyBackground = CMUImage(skyBackground)
        drawImage(skyBackground,0,self.y,opacity=100)
        # ground
        drawRect(0,self.y+self.screenHeight*2+300,self.screenWidth,150)
    
    def drawThings(self,totalCoins):

        #color1 = rgb(249,239,29)
        #color2 = rgb(69,190,201)
        choices = Image.open('images/topThree.png')
        setting = CMUImage(choices.crop((940,0,1000,60)))
        store = CMUImage(choices.crop((880,0,940,60)))
        choices = CMUImage(choices.crop((0,0,880,60)))
        drawImage(choices,0,self.y)
        drawImage(store,880,self.y,opacity=self.storeOpacity)
        drawImage(setting,940,self.y,opacity=self.settingOpacity)

        gameTitle = Image.open('images/futureFlier.png')
        width,height=gameTitle.width,gameTitle.height
        gameTitle = CMUImage(gameTitle)
        drawImage(gameTitle,self.screenWidth//2-360,self.y+120,align='center',opacity=self.backgroundOpacity,width=width//2,height=height//2)
        
        # draw record
        color1 = rgb(249,239,29)
        drawLabel(f'{totalCoins}',self.screenWidth-200,self.y+35,size=16,bold=True,align='right',fill=color1)

    def drawSetting(self):
        settingScreen = Image.open('images/settingScreen.png')
        settingScreen = CMUImage(settingScreen)
        drawRect(0,0,self.screenWidth,self.screenHeight,opacity=50)
        drawImage(settingScreen,0,self.y+60)


    
    def drawStore(self):
        drawRect(0,0,self.screenWidth,self.screenHeight,opacity=50)
        drawLabel('TO BE ANNOUNCED!',self.screenWidth//2,self.screenHeight//2,fill='white',size=40)

    def drawInstructions(self):
        drawLabel('PRESS SPACE TO PLAY!',self.screenWidth//2+330,self.y+self.screenHeight-370,font='Arial',size=20,bold=True,fill='white',opacity=self.opacity)

    def fadingEffect(self):
        if self.opacity > 0 and self.fade:
            self.opacity -= 10
        elif self.opacity == 0 and self.fade:
            self.fade = False
        elif self.opacity < 100 and not self.fade:
            self.opacity += 10
        elif self.opacity == 100 and not self.fade:
            self.fade = True
    def startSwitchToMain(self):
        self.y -= 30
