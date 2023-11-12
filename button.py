# import
from cmu_graphics import *
import math
import random
import os, pathlib
from PIL import Image
import time 
import ast
        

class Button:
    def __init__(self,screenWidth,screenHeight):
        self.screenWidth= screenWidth
        self.screenHeight = screenHeight
    def pressedNext(self,mouseX,mouseY):
        x1 = self.screenWidth-200
        y1 = self.screenHeight-100
        x2 = x1+100
        y2 = y1+60
        if x1 < mouseX < x2 and y1 < mouseY < y2:
            return True
    
    def pressedPause(self,mouseX,mouseY):
        x1 = self.screenWidth-77
        y1 = 18
        x2 = x1 + 37
        y2 = y1 + 37
        if x1 < mouseX < x2 and y1 < mouseY < y2:
            return True
    
    def pressedQuit(self,mouseX,mouseY):
        x1 = 250
        y1 = 400
        x2 = x1 + 154
        y2 = y1+70
        if x1 < mouseX < x2 and y1 < mouseY < y2:
            return True
    
    def pressedRetry(self,mouseX,mouseY):
        x1 = 410
        y1 = 400
        x2 = x1 + 154
        y2 = y1 + 70
        if x1 < mouseX < x2 and y1 < mouseY < y2:
            return True
    
    def pressedResume(self,mouseX,mouseY):
        x1 = 570
        y1 = 400
        x2 = x1 + 154
        y2 = y1 + 70
        if x1 < mouseX < x2 and y1 < mouseY < y2:
            return True
    
    def pressedPlayAgain(self,mouseX,mouseY):
        x1 = 675
        y1 = 400
        x2 = x1 + 110
        y2 = y1 + 50
        if x1 < mouseX < x2 and y1 < mouseY < y2:
            return True
        
    def pressedHome(self,mouseX,mouseY):
        x1 = 675
        y1 = 300
        x2 = x1 + 110
        y2 = y1 + 50
        if x1 < mouseX < x2 and y1 < mouseY < y2:
            return True
    
    def pressedSetting(self,mouseX,mouseY):
        x1 = 940
        x2 = x1 + 60
        y1 = 0
        y2 = y1 + 60
        if x1 < mouseX < x2 and y1 < mouseY < y2:
            return True
    
    def pressedStore(self,mouseX,mouseY):
        x1 = 880
        x2 = x1 + 60
        y1 = 0
        y2 = y1 + 60
        if x1 < mouseX < x2 and y1 < mouseY < y2:
            return True

    
    