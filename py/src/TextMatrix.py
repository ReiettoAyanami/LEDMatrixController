from src.button import Button
from src.Matrix import Matrix
import pygame

import json

EMOJI_REP = u'\ufffd'

class TextMatrix(Matrix):




    def __init__(self,pos:tuple = (0,0),buttonSize:tuple = (1,1),rect:pygame.Rect = None, size = 8, text:str = "Hello World!", fontPath:str = "py\\fonts\\MatrixFonts\\8_bit_font.json") -> None:
        super().__init__(pos, buttonSize, rect, size)
        self.emojis = []
        with open(fontPath, 'r') as j:
            self.font:dict = json.load(j)
        self.text = self.__parseText(text)
        
        self.matrixText = self.__textToMatrix(self.text)
        self.bgMat = [[Button((self.x + (self.buttonW * i), self.y + (self.buttonH * j), self.buttonW, self.buttonH), color=[0,0,0]) for j in range(self.size)]for i in range(self.size)]
        self.scrollCounter = 0
        self.scroll = 0
    
    def show(self,surface:pygame.Surface):
        super().show(surface)


    def __parseText(self, txt:str) -> str:
        txt = txt.upper()
        allowed = self.font.keys()
        emojiAllowed = list(self.font['emojis'].keys())
        
        ntxt = ''

        for i in range(len(emojiAllowed)):
            
            if txt.find(emojiAllowed[i]) >= 0:
                for j in range(txt.count(emojiAllowed[i])):
                    self.emojis.append(emojiAllowed[i])
                    
                txt = txt.replace(emojiAllowed[i], EMOJI_REP)



        for i in range(min(64, len(txt))):
            if txt[i] in allowed or txt[i] == EMOJI_REP:
                ntxt += txt[i]

        
        return ntxt


    
    def __textToMatrix(self, txt:str, letterSpacing:int = 1) -> list:

        matrixText = [[0 for _ in range( len(txt) * len(self.font['A']) + (len(self.emojis) * len(self.font['emojis']["*SUS*"])) +  (letterSpacing * len(txt)))] for _ in range(len(self.font['A']))]
        emojiCounter = 0
        
        for k in range(len(txt)):
            
            if txt[k] != EMOJI_REP:
                matChar = self.font[txt[k]]
            else:
                matChar = self.font['emojis'][self.emojis[emojiCounter]]


            for i in range(len(matChar)):
                for j in range(len(matChar[i])):
                    
                    x = j
                    y =  (k * len(matChar) + i) + (letterSpacing * k)
                    
                    
                    matrixText[x][y] = matChar[i][j]


                    

            if txt[k] == EMOJI_REP:
                
                emojiCounter += 1 
                
                        

                
        return matrixText
    


    def displayText(self,scroll:bool = True, scrollSpeed:float = .1, newColor:tuple = (255, 255, 255)):
        
        
        for i in range(len(self.mat)):
            for j in range(len(self.mat[i])):
                
                if self.matrixText[j][(i + self.scroll) % (len(self.matrixText[0] ))]:
                    self.nextFrame[i][j].color = newColor
                else:
                    self.nextFrame[i][j].color = self.bgMat[i][j].color

        if scroll:
            self.scrollCounter += scrollSpeed

            if self.scrollCounter >= 1:
                self.scroll += 1
                self.scrollCounter = 0

    def bgMouseUpdate(self, mouseEvents, color = [100,100, 100]):

        for i in range(len(self.mat)):
            for j in range(len(self.mat[i])):
                self.bgMat[i][j].on_event(self.bgMat[i][j].hover() and mouseEvents['mouse_pressed']['left'],lambda: self.setBgColorAt(i,j,color))





    def setBgColorAt(self,x:int,y:int,color:list[int]):
        
        self.bgMat[x][y].color = color