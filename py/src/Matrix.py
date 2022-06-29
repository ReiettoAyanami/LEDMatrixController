import pygame
from pygame import Rect
from src.button import Button


class Matrix:


    def __init__(self,pos:tuple = (0,0),buttonSize:tuple = (1,1),rect:pygame.Rect = None, size = 8) -> None:
        self.pos = self.x, self.y = pos
        self.buttonSize = self.buttonW, self.buttonH = buttonSize
        if rect:
            self.pos = self.x, self.y = Rect(rect).topleft
            self.buttonSize = self.buttonW, self.buttonH = Rect(rect).w/size, Rect(rect).h/size


        self.size = size
        
        self.nextFrame = [[Button((self.x + (self.buttonW * i), self.y + (self.buttonH * j), self.buttonW, self.buttonH), color=[0,0,0]) for j in range(self.size)]for i in range(self.size)]
        self.mat = [[Button((self.x + (self.buttonW * i), self.y + (self.buttonH * j), self.buttonW, self.buttonH), color=[0,0,0]) for j in range(self.size)]for i in range(self.size)]
        self.brightness = 255

    def show(self, surface):

        for i in range(len(self.mat)):
            for j in range(len(self.mat[i])):
                self.mat[i][j].show(surface)
                self.mat[i][j].on_event(self.mat[i][j].hover(), lambda: self.mat[i][j].glow(surface, [155,155,155,100]))


    def update(self, mouseEvents, color = [100,100, 100]):

        for i in range(len(self.mat)):
            for j in range(len(self.mat[i])):
                self.mat[i][j].on_event(self.mat[i][j].hover() and mouseEvents['mouse_pressed']['left'],lambda: self.setColorAt(i,j,color))
                
    def setBrightness(self, newBrightness:list[int | float]):

        self.brightness = newBrightness
        
    

    def setColorAt(self,x:int,y:int,color:list[int]):
        
        self.mat[x][y].color = color


    def getMatrixChanges(self):
        
        changed = []

        for i in range(len(self.mat)):
            for j in range(len(self.mat[i])):

                if self.mat[i][j].color != self.nextFrame[i][j].color:
                    self.mat[i][j].color = self.nextFrame[i][j].color
                    changed.append({"idx":((j * self.size )+ i),"color": self.mat[i][j].color})
                    

        return changed

    def setBorderRadius(self, border_radius):
        self.mat[-1][0].set_corners({'topleft':0, 'topright':border_radius, 'bottomleft':0, 'bottomright':0})
        self.mat[0][0].set_corners({'topleft':border_radius, 'topright':0, 'bottomleft':0, 'bottomright':0})
        self.mat[0][-1].set_corners({'topleft':0, 'topright':0, 'bottomleft':border_radius, 'bottomright':0})
        self.mat[-1][-1].set_corners({'topleft':0, 'topright':0, 'bottomleft':0, 'bottomright':border_radius})

