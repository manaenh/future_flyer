# import
from cmu_graphics import *
import math
import random
import os, pathlib
from PIL import Image
import time 

# power ups!
class Powerup:
    def __init__(self,time,speed,rightWall):
        self.time = time
        self.x = rightWall
        self.y = 200
        self.size = 40
        self.gotPowerUp = False
        self.speed = speed + 0.5
        self.powerUpOnScreen = False
        self.rightWall = rightWall
        self.initialTime = None
        self.powerUpCounter = 0
        self.opacity = 100
        self.fade = False

    # draw power up   
    def drawPowerUps(self):

        #magnet
        if self.powerUpOnScreen and not self.gotPowerUp:
            magnet = Image.open('images/magnet.png')
            magnet = CMUImage(magnet)
            drawImage(magnet,self.x,self.y,opacity=self.opacity)
            #drawRect(self.x,self.y,self.size,self.size,align='center')
    
    def collidePowerUps(self,flierX,flierY):
        if abs(flierX-self.x) <= 20+self.size/2 and abs(flierY-self.y)<=20+self.size/2:
            self.gotPowerUp = True
            self.powerUpOnScreen = False
            self.x = self.rightWall
            return True
            
    
    # power up box moving
    def powerUpBoxMoving(self):
        if self.powerUpOnScreen:
            self.x -= self.speed
        if self.x <= 0 - self.size:
            self.powerUpOnScreen = False
            self.x = self.rightWall


    # generate a power up over some time
    def generatePowerUps(self):
        if self.time == 0 or self.time % 1000 == 0:
            # print(f'time:{self.time},pX:{self.x},pY:{self.y}')
            self.powerUpOnScreen = True
            self.speed += 0.5
        if self.gotPowerUp:
            self.powerUpCounter += 1
            if self.powerUpCounter >= 600:
                self.gotPowerUp = False
            return 'magnet'
        else:
            self.powerUpCounter = 0
    
    # fading effect
    def fadingEffect(self):
        if self.opacity > 0 and self.fade:
            self.opacity  -= 10
        elif self.opacity  == 0 and self.fade:
            self.fade = False
        elif self.opacity < 100 and not self.fade:
            self.opacity  += 10
        elif self.opacity == 100 and not self.fade:
            self.fade = True
