from cmu_graphics import *
import math
import random
import os, pathlib
from PIL import Image
import time 
import ast


class GameStatus:
    def __init__(self,screenWidth,screenHeight):
        self.screenWidth = screenWidth
        self.screenHeight = screenHeight

        # opacity
        self.opacity = 60
        self.quitOpacity=60
        self.resumeOpacity=60
        self.retryOpacity=60
        self.gameoverOpacity = 0
        self.playAgainOpacity = 60
        self.homeOpacity = 60

        # for transition screen
        self.blackOpacity = 0
        self.transitionScreenOpacity = 0

    # status when playing
    def drawPlayingStatus(self,bestScore):
        # pause
        # I drew this
        pause = Image.open('images/pausedCoin.png')
        pause = CMUImage(pause)
        drawImage(pause,0,0)
        drawLabel(f'BEST: {bestScore} M',18,68,size=10,fill='white',font='Courier New',align='left')  
    
    def drawGameOverStatus(self):
        # game finished
        # I drew this
        gameFinished = Image.open('images/gameFinished.png')
        gameFinished = CMUImage(gameFinished)
        # I drew this
        nextButton = Image.open('images/nextButton.png')
        nextButton = CMUImage(nextButton)
        drawRect(0,0,self.screenWidth,self.screenHeight,fill='black',opacity=40)
        drawImage(gameFinished,0,0,opacity=self.gameoverOpacity) 
        drawImage(nextButton,self.screenWidth-200,self.screenHeight-100,opacity = self.opacity)
    
    def gameOverStatusAnimation(self):
        if self.gameoverOpacity < 100:
            self.gameoverOpacity += 10

    def drawPausedScreen(self):
        # I drew these images
        pause = Image.open('images/pausedScreen.png')
        pause = CMUImage(pause)
        drawImage(pause,0,0)

        quit = Image.open('images/quit.png')
        width,height=quit.width,quit.height
        quit = CMUImage(quit)
        retry = Image.open('images/retry.png')
        retry = CMUImage(retry)
        resume = Image.open('images/resume.png')
        resume = CMUImage(resume)
        x = 250
        drawImage(quit,x,400,width=width*1.4,height=height*1.4,opacity=self.quitOpacity)
        drawImage(retry,x+160,400,width=width*1.4,height=height*1.4,opacity=self.retryOpacity)
        drawImage(resume,x+160*2,400,width=width*1.4,height=height*1.4,opacity=self.resumeOpacity)
    
    def drawTransitionScreen(self,stars):
        drawRect(0,0,self.screenWidth,self.screenHeight,opacity=self.blackOpacity)
        playAgain = Image.open('images/playAgain.png')
        home = Image.open('images/home.png')
        levelFrame = Image.open('images/levelFrame.png')
        levelBar = Image.open('images/levelBar.png')
        levelWidth,levelHeight = levelBar.width,levelBar.height
        playAgain = CMUImage(playAgain)
        home = CMUImage(home)
        levelFrame = CMUImage(levelFrame)
        levelBar = CMUImage(levelBar)
        missions = Image.open('images/pausedScreen.png')
        missionWidth,missionHeight = missions.width,missions.height
        missions = CMUImage(missions.crop((250,100,750,500)))
        if self.transitionScreenOpacity < 100:
            drawImage(missions,150,100,height=missionHeight*0.8,opacity=self.transitionScreenOpacity)
            if stars != 0:
                drawImage(levelBar,670,130,opacity=self.transitionScreenOpacity,width=(levelWidth*1.5)//3*stars,height=levelHeight*1.5)
            drawImage(levelFrame,670,130,opacity=self.transitionScreenOpacity,width=levelWidth*1.5,height=levelHeight*1.5)
            drawImage(home,675,300,opacity=self.transitionScreenOpacity)
            drawImage(playAgain,675,400,opacity=self.transitionScreenOpacity)
        else:
            drawImage(missions,150,100,height=missionHeight*0.8,opacity=100)
            if stars != 0:
                drawImage(levelBar,670,130,opacity=100,width=(levelWidth*1.5)//3*stars,height=levelHeight*1.5)
            drawImage(levelFrame,670,130,opacity=100,width=levelWidth*1.5,height=levelHeight*1.5)
            drawImage(home,675,300,opacity=self.homeOpacity)
            drawImage(playAgain,675,400,opacity=self.playAgainOpacity)


    def fadeToBlackToScreenEffect(self):
        if self.blackOpacity < 80:
            self.blackOpacity += 10
        elif self.transitionScreenOpacity < 100:
            self.transitionScreenOpacity += 10
    
    # reference to CMU 15-112 Fall 2022 notes: "string-12", recommended by Mingjing (Madison) Zhao
    def readFile(self,path):
        with open(path,"rt") as f:
            return f.read()
    
    def writeFile(self,path,contents):
        with open(path, "wt") as f:
            f.write(contents)

    def recordData(self,totalCoins,highestScore):
        data = {'totalCoins':totalCoins,'highestScore':highestScore}
        self.writeFile('record.txt',repr(data))
    
    def getRecords(self):
        records = ast.literal_eval(self.readFile('record.txt'))
        totalCoins = records['totalCoins']
        highestScore = records['highestScore']
        return totalCoins,highestScore
        