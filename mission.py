# import
from cmu_graphics import *
import math
import random
import os, pathlib
from PIL import Image
import time 
import ast

class Mission:
    def __init__(self):
        # mission status
        self.missionCompletion = dict()
        self.missions = []
        self.level = 0
        self.requiredStars = 3
        self.currentStars = 0
        self.switchMission = False
        self.noticed = False

        self.index = random.randint(1,4)
        #missions
        self.travel2000 = 'TRAVEL A TOTAL OF 2,000M IN ONE GAME'
        self.reach750NoCoins = 'REACH 750M WITHOUT COLLECTING ANY COINS'
        self.purchase1Item = 'PURCHASE AN ITEM IN THE STORE'  
        self.play3Games = 'PLAY 3 GAMES'
        self.gameCount = False

        self.rubRoof900 = 'RUB YOUR HEAD AGAINST THE ROOF FOR 900M'
        self.rubRoofTime = 0

        self.missionBarX = 1000
        
    def getMission(self):
        self.index = random.randint(1,4)
        if self.index == 1 and self.travel2000 not in self.missionCompletion: 
            return self.travel2000
        elif self.index == 2 and self.reach750NoCoins not in self.missionCompletion: 
            return self.reach750NoCoins
        elif self.index == 3 and self.play3Games not in self.missionCompletion: 
            return self.play3Games
        elif self.index == 4 and self.rubRoof900 not in self.missionCompletion: 
            return self.rubRoof900
    
    def generateMissions(self):
        self.missionCompleted = False
        while len(self.missions) < 1:
            m1 = self.getMission()
            m2 = self.getMission()
            if m1 != m2:
                self.missionCompletion[m1] = False
                self.missionCompletion[m2] = False
                self.missions += [m1,m2]

       # for mission in self.missionCompletion:
       #     if self.missionCompletion[mission] == True:
        #        self.missions.remove(mission)
        
       # while len(self.missions) == 1:
        #    m = self.getMission()
        #    if m not in self.missions:
           #     self.missions += [m]
            
    def drawMissionPause(self):
        if len(self.missions) == 2:
            m1 = self.missions[0]
            m2 = self.missions[1]
            if self.missionCompletion[m1]==True:
                drawLabel(f'{m1}',290,200,align='left',size=16,fill='white')
                drawLabel('[COMPLETED!]',290,220,align='left',size=16,fill='white')
            else:
                drawLabel(f'{m1}',290,200,align='left',size=16,fill='white')
            if self.missionCompletion[m2]==True:
                drawLabel(f'{m2}',290,320,align='left',size=16,fill='white')
                drawLabel('[COMPLETED!]',290,340,align='left',size=16,fill='white')
            else:
                drawLabel(f'{m2}',290,320,align='left',size=16,fill='white')
    
    def drawMissionNotice(self):
        if len(self.missions) == 2:
            m1 = self.missions[0]
            m2 = self.missions[1]
            if self.missionCompletion[m1]==True:
                drawLabel('FIRST MISSION COMPLETED!',200,500,size=20,fill='white')
            if self.missionCompletion[m2]==True:
                drawLabel('SECOND MISSION COMPLETED!',200,540,size=20,fill='white')

    def drawMissionCompleteNotice(self):
        m1 = self.missions[0]
        m2 = self.missions[1]
        if self.missionCompletion[m1]==True and not self.noticed:
            drawLabel(f'{m1} COMPLETED!',self.missionBarX,700,fill='white',size=16,align='left')
        if self.missionCompletion[m2]==True and not self.noticed:
            drawLabel(f'{m2} COMPLETED!',self.missionBarX,700,fill='white',size=16,align='left')
    
    def missionCompleteNoticeAnimation(self,speed):
        if not self.noticed and self.missionBarX > -900:
            self.missionBarX -= speed
        if self.missionBarX > -900:
            self.noticed = True

    
    def drawMissionTransition(self):
        if len(self.missions) == 2:
            m1 = self.missions[0]
            m2 = self.missions[1]
            drawLabel(f'{m1}',200,220,align='left',size=16,fill='white',bold=True)
            drawLabel(f'{m2}',200,350,align='left',size=16,fill='white',bold=True)
        drawLabel(f'{self.level}',700,160,fill='black',size=16,bold=True)
        drawLabel(f'{self.currentStars} / {self.requiredStars}',800,165,fill='black',size=16,bold=True)
    
    def checkMissionCompletion(self,distance,coins,count,flierY,speed):
        for m in self.missions:
            if m == 'TRAVEL A TOTAL OF 2,000M IN ONE GAME':
                if self.travel2000Check(distance) and self.missionCompletion['TRAVEL A TOTAL OF 2,000M IN ONE GAME'] == False:
                    self.missionCompletion['TRAVEL A TOTAL OF 2,000M IN ONE GAME']=True
                    self.switchMission=True
                    self.currentStars += 1
                    self.noticed = False
                    self.missionBarX = 1000
            elif m == 'REACH 750M WITHOUT COLLECTING ANY COINS':
                if self.reach750NoCoinsCheck(distance,coins)and self.missionCompletion['REACH 750M WITHOUT COLLECTING ANY COINS']==False:
                    self.missionCompletion['REACH 750M WITHOUT COLLECTING ANY COINS']=True
                    self.switchMission=True
                    self.currentStars += 1
                    self.noticed = False
                    self.missionBarX = 1000
            elif m == 'PLAY 3 GAMES':
                self.gameCount = True
                if self.play3GamesCheck(count)and self.missionCompletion['PLAY 3 GAMES']==False:
                    self.missionCompletion['PLAY 3 GAMES']=True
                    self.switchMission=True
                    self.currentStars += 1
                    self.noticed = False
                    self.missionBarX = 1000
            elif m == 'RUB YOUR HEAD AGAINST THE ROOF FOR 900M':
                if self.rubRoof900Check(flierY,speed)and self.missionCompletion['RUB YOUR HEAD AGAINST THE ROOF FOR 900M']==False:
                    self.missionCompletion['RUB YOUR HEAD AGAINST THE ROOF FOR 900M']=True
                    self.switchMission=True
                    self.currentStars += 1
                    self.noticed = False
                    self.missionBarX = 1000
    
    def starsCheck(self):
        if self.currentStars >= self.requiredStars:
            self.level += 1
            self.currentStars -= self.requiredStars

    def travel2000Check(self,distance):
        if distance >= 2000:
            return True
    
    def rubRoof900Check(self,flierY,speed):
        if flierY == 30:
            self.rubRoofTime += 1
        distance = (self.rubRoofTime * speed)//10
        if distance >= 900:
            self.rubRoofTime =0
            return True
    def reach750NoCoinsCheck(self,distance,coins):
        if distance >= 750 and coins == 0:
            return True
    
    def play3GamesCheck(self,count):
        if count >= 3:
            self.gameCount = False
            return True