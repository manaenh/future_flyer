# I drew all the pictures except for the flier
# All sounds are from Jetpack Joyride game

# import
from cmu_graphics import *
import math
import random
import os, pathlib
from obstacle import *
from flier import *
from coin import *
from scrollingBackground import *
from powerup import *
from gameStatus import *
from startStatus import *
from button import *
from mission import *
from sounds import *
from PIL import Image
import time 
import ast

# general onAppStart
def onAppStart(app):
    # record
    app.recordStatus = GameStatus(app.width,app.height)
    app.totalCoins,app.bestScore = app.recordStatus.getRecords()
    app.missions = Mission()
    app.buttonPressed = False
    app.gameCount = 0

    # sounds
    app.sound = Sounds()

    app.button = Button(app.width,app.height)


    start_restart(app)

# inital screen ###############################################
def start_restart(app):
    app.instructionOpacity = 100
    app.fade = True
    app.status = StartStatus(0,app.width,app.height)
    app.stepsPerSecond = 100
    


def start_redrawAll(app):
    # start background
    app.status.drawStartBackground()
    # game title and coins and records
    
    app.status.drawThings(app.totalCoins)
    # instruction
    app.status.drawInstructions()

    if app.status.settingOn:
        app.status.drawSetting()
    elif app.status.storeOn:
        app.status.drawStore()
    

def start_onStep(app):
    app.status.fadingEffect()    
    if app.status.transition == True:
        app.status.startSwitchToMain()
    if app.status.y < -app.height-400:
        start_restart(app)
        main_restart(app)
        setActiveScreen('main')

def start_onKeyPress(app,key):
    if key == 'space' and not app.status.settingOn and not app.status.storeOn:
        app.status.transition = True
        app.sound.button.play()

def start_onMouseMove(app,mouseX,mouseY):
    if app.button.pressedSetting(mouseX,mouseY): app.status.settingOpacity = 100
    else: app.status.settingOpacity = 60
    if app.button.pressedStore(mouseX,mouseY): app.status.storeOpacity = 100
    else: app.status.storeOpacity = 60

def start_onMousePress(app,mouseX,mouseY):
    if app.button.pressedSetting(mouseX,mouseY):
        app.status.settingOn = not app.status.settingOn
        app.status.storeOn = False
    elif app.button.pressedStore(mouseX,mouseY):
        app.status.storeOn = not app.status.storeOn
        app.status.settingOn = False

# main game loop ###############################################

def main_restart(app):
    # set up screen
    app.ground = app.height - 100
    app.ceiling = 4
    app.rightWall = app.width
    app.leftWall = 0

    #status
    app.paused = False
    app.gameOver = False
    app.speed = 3
    app.stepsPerSecond = 80
    app.gameStatus = GameStatus(app.width,app.height)
    app.difficultyLevel = 1
    app.time = 0
    app.transitionScreen = False
    
    if app.missions.gameCount:
        app.gameCount += 1

    # load hacking nodes
    app.hackingNodes = Obstacle(0,app.speed)

    # load drones
    app.drone = []
    for i in range(app.difficultyLevel):
        app.drone += [Obstacle(0,app.speed)]

    #set up player
    app.flier = Flier(350,app.ceiling, False,app.ground-60)
    app.flier.flierOnGround()

    #load coins!
    app.coins = Coin(app.rightWall,9,app.speed,0,app.ground)

    #load power ups!
    app.powerUp = Powerup(0,app.speed,app.rightWall)

    #load background
    app.scrollBackground = Background(app.speed,app.rightWall)

    # load mission
    app.missions = Mission()
    app.missions.generateMissions()

    


# shown on screen
def main_redrawAll(app):
    #draw scrolling environment
    app.scrollBackground.drawBackground(app.ground,app.width,app.height)

    # draw hacking nodes
    app.hackingNodes.drawHackingNodes()

    #draw coins
    app.coins.drawLineCoinGroup()
    #draw number of coins gained,distance
    # draw status and fire
    if not app.gameOver:
        app.coins.drawCollectedCoinsNumber(50,23,16,100)
        app.hackingNodes.drawDistanceStatus(18,48,20,'left',100)
        app.gameStatus.drawPlayingStatus(app.bestScore)
        app.flier.drawFire() 
        app.missions.drawMissionNotice()
    elif app.gameOver and app.paused and not app.transitionScreen:
        app.gameStatus.drawGameOverStatus()
        color1 = rgb(249,239,29)
        app.coins.drawCollectedCoinsNumber(app.width//2+100,app.height//2+80,50,app.gameStatus.gameoverOpacity)
        app.hackingNodes.drawDistanceStatus(app.width//2,220,60,'center',app.gameStatus.gameoverOpacity)
        drawLabel(f'{app.totalCoins}',app.width-200,35,align='right',fill=color1,size=16,bold=True,opacity=app.gameStatus.gameoverOpacity)
    
    for drone in app.drone:
        if drone.droneStart and not app.gameOver:
            drone.drawDrone()

    #draw flier (running/flying)
    if (app.flier.y < app.flier.ground or app.flier.isFlying) and not app.gameOver:
        app.flier.drawFlierFlying()
    elif not app.gameOver:
        app.flier.drawRunningFlier()
    else:
        app.flier.drawDyingFlier(app.width,app.height)

    # draw power up
    app.powerUp.drawPowerUps()
    
    #pause
    if app.paused and not app.gameOver:
        drawRect(0,0,app.width,app.height,opacity=40)
        app.gameStatus.drawPausedScreen()
        app.missions.drawMissionPause()
    
    # transition page
    if app.transitionScreen:
        app.gameStatus.drawTransitionScreen(app.missions.currentStars)
        app.missions.drawMissionTransition()
    
# controls
def main_onKeyHold(app,keys):
    if 'space' in keys:
        app.flier.isFlying = True

def main_onKeyPress(app,key):
    if key == 'space' and app.gameOver and app.paused:
        app.buttonPressed = True
        main_restart(app)

def main_onKeyRelease(app,key):

    # flier falling
    app.flier.isFlying = False
    if key == 'space' and app.gameOver and app.paused:  
        app.buttonPressed = False


def main_onMousePress(app,mouseX,mouseY):
    if not app.gameOver:
        if app.button.pressedPause(mouseX,mouseY):
            app.paused = True
            app.sound.button.play(restart=True)
        if app.button.pressedQuit(mouseX,mouseY): 
            app.sound.button.play(restart=True)
            setActiveScreen('start')
        elif app.button.pressedRetry(mouseX,mouseY):
            app.sound.button.play(restart=True)
            main_restart(app)
        elif app.button.pressedResume(mouseX,mouseY):
            app.sound.button.play(restart=True)
            app.paused = False
    if app.gameOver and not app.transitionScreen:
        if app.button.pressedNext(mouseX,mouseY):
            app.sound.button.play(restart=True)
            app.gameStatus.opacity = 50
            app.transitionScreen = True
        if app.missions.switchMission:
            app.missions.generateMissions()
            app.missions.starsCheck()
    if app.gameOver and app.transitionScreen:
        if app.button.pressedPlayAgain(mouseX,mouseY):
            app.sound.button.play(restart=True)
            main_restart(app)
        elif app.button.pressedHome(mouseX,mouseY):
            app.sound.button.play(restart=True)
            setActiveScreen('start')


def main_onMouseMove(app,mouseX,mouseY):
    if app.gameOver and not app.transitionScreen:
        if app.button.pressedNext(mouseX,mouseY): app.gameStatus.opacity = 100
        else: app.gameStatus.opacity = 60
    if not app.gameOver:
        if app.button.pressedQuit(mouseX,mouseY): app.gameStatus.quitOpacity = 100
        else: app.gameStatus.quitOpacity = 60
        if app.button.pressedRetry(mouseX,mouseY): app.gameStatus.retryOpacity = 100
        else: app.gameStatus.retryOpacity = 60
        if app.button.pressedResume(mouseX,mouseY): app.gameStatus.resumeOpacity = 100
        else: app.gameStatus.resumeOpacity = 60
    if app.gameOver and app.transitionScreen:
        if app.button.pressedPlayAgain(mouseX,mouseY): app.gameStatus.playAgainOpacity = 100
        else: app.gameStatus.playAgainOpacity = 60
        if app.button.pressedHome(mouseX,mouseY): app.gameStatus.homeOpacity=100
        else:app.gameStatus.homeOpacity = 60 
        
    

# moving stuff
def main_onStep(app):
    # sound
    if app.flier.y >= app.flier.ground and not app.gameOver and not app.paused:
        app.sound.running.play(loop=True)
    else:
        app.sound.running.pause()
    
    if app.flier.isFlying and not app.gameOver and not app.paused :
        app.sound.flyEnd.play(restart=True)
    else:
        app.sound.flyEnd.pause
    
    if not app.gameOver and not app.paused:
        # general
        app.time += 1
        # hacking nodes
        app.hackingNodes.generateNewHackingNodes(app.ground,app.ceiling,app.leftWall,app.rightWall)
        app.hackingNodes.moveHackingNodes()

        #flier move
        app.flier.runningCounter() 
           
        if app.flier.isFlying:
            app.flier.appliedForce()
        else:
            app.flier.gravity()
        if app.hackingNodes.crashHackingNodes(app.flier.x,app.flier.y):
            app.sound.dying.play()
            app.gameOver = True
        
        for drone in app.drone: 
            if drone.crashDrone(app.flier.x,app.flier.y):
                app.sound.dying.play()
                app.gameOver = True
                break
          
        #jetpack physics
        app.flier.determineFireStrength()
        
        #power up moving
        if app.powerUp.powerUpOnScreen:
            app.sound.powerupComing.play()
        if app.powerUp.collidePowerUps(app.flier.x,app.flier.y):
            app.sound.powerupComing.pause
            app.sound.getsPowerup.play()
    
        powerup = app.powerUp.generatePowerUps()
        app.powerUp.powerUpBoxMoving()
        app.powerUp.time+=1
        app.powerUp.fadingEffect()

        # coins move
        # whether has magnet power ups or not
        if powerup == 'magnet':
            app.coins.magnetPowerUp(app.flier.x,app.flier.y,1)
        else:
            app.coins.coinLinesMoving()
        
        app.coins.generateNewCoinGroup(app.ground,app.ceiling,app.leftWall,app.rightWall,app.hackingNodes.hackingNodes)
        if app.coins.collectCoinsInLine(app.flier.x,app.flier.y):
            app.sound.coins.play()
        else:
            app.sound.coins.pause

        # building backgrounds
        app.scrollBackground.generateFirstLayerBuilding()
        app.scrollBackground.generateSecondLayerBuilding()
        app.scrollBackground.generateThirdLayerBuilding()
        app.scrollBackground.generateSkyscraper()
        app.scrollBackground.buildingMoving()

        # drones
        if app.time % 1000 == 0: 
            app.difficultyLevel += 1

        for drone in app.drone:
            drone.droneAnimation()
            drone.droneMoving(app.flier.y,app.ground,app.rightWall)
            drone.generateNewDrones()

        # check missions
        app.missions.checkMissionCompletion(app.hackingNodes.distance,app.coins.collectedNumber,app.gameCount,app.flier.y,app.hackingNodes.speed)
 
    if app.gameOver and not app.paused:
        app.hackingNodes.moveHackingNodes()
        app.scrollBackground.buildingMoving()
        app.coins.coinLinesMoving()
        app.flier.flierDeadCount()
        app.powerUp.powerUpBoxMoving()
        if app.hackingNodes.distance > app.bestScore:
            app.bestScore = app.hackingNodes.distance
        if app.flier.flierDeadFalling():
            app.paused = True
            app.totalCoins += app.coins.collectedNumber
            app.gameStatus.recordData(app.totalCoins,app.bestScore)
    if app.gameOver and app.paused:
        app.gameStatus.gameOverStatusAnimation()
    if app.transitionScreen:
        app.gameStatus.fadeToBlackToScreenEffect()  
            



def main():
    runAppWithScreens(width=1000,height=600,initialScreen='start')

main()