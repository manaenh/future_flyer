# import
from cmu_graphics import *
import math
import random
import os, pathlib
from PIL import Image
import time 
import ast

class Sounds:
    def __init__(self):
        self.button = self.loadSound('sounds/button_1.mp3')
        self.changeScreen = self.loadSound('sounds/changeScreen.mp3')
        self.droneComing =self.loadSound('sounds/dromeComing.mp3')
        self.dying =self.loadSound('sounds/dying.mp3')
        self.fly = self.loadSound('sound/flyAll.mp3')
        self.flyStart =self.loadSound('sounds/flyStart.mp3')
        self.flyMid =self.loadSound('sounds/flyMid.mp3')
        self.flyEnd =self.loadSound('sounds/flyEnd.mp3')
        self.coins =self.loadSound('sounds/gainCoins.mp3')
        self.getsPowerup =self.loadSound('sounds/getsPowerup.mp3')
        self.powerupComing =self.loadSound('sounds/powerupComing.mp3')
        self.running = self.loadSound('sounds/running.mp3')  
    
    # reference to 15112 lecture demo
    def loadSound(self,relativePath):
        absolutePath = os.path.abspath(relativePath)
        url = pathlib.Path(absolutePath).as_uri()
        return Sound(url)