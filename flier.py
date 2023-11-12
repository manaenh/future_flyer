from cmu_graphics import *
import math
import random
import os, pathlib
from PIL import Image
import time

# player character
class Flier:
    def __init__(self,x,y,isFlying,ground):
        self.x = x
        # used lecture kirb 
        self.y = y
        self.dy = 0
        self.ddy = 0.5
        self.isFlying = isFlying
        self.flierRunning= []
        self.framesCounter = 0
        self.ground = ground
        self.flierRunningFramesCounter = 0

        # jetpack fire!
        self.fireCounter = 0
        self.fireOpacity1 = 0
        self.fireOpacity2 = 0
        self.noFire = True
        self.force = False

        # when dead and fall, the times it bump back up
        self.fallingCount = 0
        self.justDied = False
        self.deadCounter = 0
        self.deadYellowOpacity = 60
        self.bumpAngle = 0
        self.bump = False
        self.crash = False
    
    # flier flying look
    def drawFlierFlying(self):
        # I photoshopped the image generated from MidJourney, https://www.midjourney.com/app/
        flier = Image.open('images/flierFlying02.png')
        flier = CMUImage(flier)
        drawImage(flier,self.x,self.y,align='center')

    
    # flier on ground running movement
    def flierOnGround(self):
        # I photoshop all the motions using an image generated from MidJourney, https://www.midjourney.com/app/
        flier = Image.open('images/flier04.png')
        for i in range(4):
            frame = CMUImage(flier.crop((60*i,35,60+60*i,100)))
            self.flierRunning.append(frame)

    def drawRunningFlier(self):
        
        flierRunning = self.flierRunning[self.framesCounter]
        drawImage(flierRunning,self.x,self.y,align='center')
    
    def runningCounter(self):
        
        self.flierRunningFramesCounter += 1
        if self.flierRunningFramesCounter % 4 == 0:
            self.framesCounter = (1+self.framesCounter)%len(self.flierRunning)


    # flier gravity and force
    def gravity(self): 
        self.force = False
        self.ddy=0.25
        if self.y+self.dy < 30:
            self.y = 30
            self.dy = 0
        if self.y + self.dy < self.ground:
            # reference to 15-112 lecture
            self.y += self.dy
            self.dy += self.ddy
        else:
            self.y = self.ground
            self.dy = 0
            self.ddy = 0.25

    def appliedForce(self):
        self.force = True
        self.ddy = 0.5
        if self.y+self.dy > self.ground+5:
            self.y = self.ground
            self.dy = 0
        if self.y + self.dy > 30:
            self.y += self.dy
            self.dy += -self.ddy
        else:
            self.y = 30

    # when flier is dead
    def flierDeadFalling(self):
        if not self.crash:
            self.dy = -5
            self.crash=True
        self.y += self.dy
        self.dy += self.ddy
        if self.y >= self.ground:
            self.dy = -0.65*abs(self.dy)
            self.fallingCount += 1
        #print(f'y:{self.y},dy:{self.dy},count:{self.fallingCount}')
        if self.fallingCount >= 6:
            return True
    
    def flierDeadCount(self):
        self.deadCounter += 1
        if self.deadCounter < 15:
            self.justDied = True
            if self.deadYellowOpacity > 0:
                self.deadYellowOpacity-=5
        else:
            self.justDied = False
        
        if self.bump and self.fallingCount < 4:
            self.bumpAngle+=3
        elif self.bump and self.fallingCount < 6:
            self.bumpAngle=20
    
    # draw when flier is dead

    def drawDyingFlier(self,screenWidth,screenHeight):
        justDead = Image.open('images/justDied.png')
        justDead = CMUImage(justDead)
        skull1 = Image.open('images/skull1.png')
        skull2 = Image.open('images/skull2.png')
        skull1 = CMUImage(skull1)
        skull2 = CMUImage(skull2)
        bump = Image.open('images/diedBump.png')
        almostDead = Image.open('images/diedOnGround.png')
        bump = CMUImage(bump)
        almostDead = CMUImage(almostDead)
        dead = Image.open('images/completelyDead.png')
        dead = CMUImage(dead)

        if self.justDied:
            drawRect(0,0,screenWidth,screenHeight,fill='yellow',opacity=self.deadYellowOpacity)
        if self.y < self.ground and not self.bump:
            if self.deadCounter < 10:
                drawImage(justDead,self.x,self.y)
            elif self.deadCounter < 20:
                drawImage(skull1,self.x,self.y,rotateAngle=-20)
            elif self.deadCounter < 30:
                drawImage(skull2,self.x,self.y,rotateAngle=-20)
            elif self.deadCounter < 40:
                drawImage(skull1,self.x,self.y,rotateAngle=-20)
            elif self.deadCounter < 50:
                drawImage(skull2,self.x,self.y,rotateAngle=-20)

        else:
            self.bump = True

        if self.bump:
            if self.fallingCount < 5:
                drawImage(bump,self.x,self.y,rotateAngle=self.bumpAngle)
            elif self.fallingCount < 6:
                drawImage(almostDead,self.x,self.y)
            else:
                drawImage(dead,self.x,self.y)


    
    # physics of fire
    def determineFireStrength(self):
        if self.force:
            self.fireCounter += 1
        else:
            self.fireCounter = 0
        
        if 0<self.fireCounter < 10:
            self.fireOpacity1 = 100
        elif 10 <= self.fireCounter and 0 < self.fireOpacity1 <= 100 and 0 <=self.fireOpacity2 < 100:
            self.fireOpacity1 -= 20
            self.fireOpacity2 += 20
        elif self.fireCounter == 0 and self.fireOpacity2 > 0:
            self.fireOpacity2 -= 20
            self.fireOpacity1 = 0
        elif self.fireCounter == 0 and self.fireOpacity1 > 0:
            self.fireOpacity1 -= 20
        #print('fire count',self.fireCounter,'1',self.fireOpacity1,'2',self.fireOpacity2)

    def drawFire(self):
        fire1 = Image.open('images/startFire.png')
        fireWidth1,fireHeight1 = fire1.width,fire1.height
        fire2 = Image.open('images/laterFire.png')
        fire1 = CMUImage(fire1)
        fire2 = CMUImage(fire2)

        if 0 < self.fireCounter < 10:
            index = 9-self.fireCounter
            if abs(self.y-self.ground) < fireHeight1:
                drawImage(fire1,self.x,self.y+15,align='top',width=fireWidth1-index,height=abs(self.y-self.ground)+1)
            else:
                drawImage(fire1,self.x,self.y+15,align='top',width=fireWidth1-index,height=fireHeight1-index*2)
        else:
            if abs(self.y-self.ground) < fireHeight1:
                drawImage(fire1,self.x,self.y+15,align='top',opacity=self.fireOpacity1,height=abs(self.y-self.ground)+1)
                drawImage(fire2,self.x,self.y+15,align='top',opacity=self.fireOpacity2,height=abs(self.y-self.ground)+1,width=fireWidth1*0.8)
            else:
                drawImage(fire1,self.x,self.y+15,align='top',opacity=self.fireOpacity1)
                drawImage(fire2,self.x,self.y+15,align='top',opacity=self.fireOpacity2,width=fireWidth1*0.8)


