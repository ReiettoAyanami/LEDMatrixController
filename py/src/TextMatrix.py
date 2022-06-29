from src.button import Button
from src.Matrix import Matrix
import pygame

import json

EMOJI_REP = u'\ufffd'

class TextMatrix(Matrix):

    def __init__(self,pos:tuple = (0,0),buttonSize:tuple = (1,1),rect:pygame.Rect = None, size = 8, text:str = "Hello World!", font_path:str = "py\\fonts\\MatrixFonts\\8_bit_font.json") -> None:
        super().__init__(pos, buttonSize, rect, size)
        
        self.emojis = []

        


        with open(font_path, 'r') as j:
            self.font:dict = json.load(j)
        self.text = self.__parseText(text)
        
        self.matrix_text = self.__textToMatrix(self.text)
        self.bgMat = [[Button((self.x + (self.buttonW * i), self.y + (self.buttonH * j), self.buttonW, self.buttonH), color=[0,0,0]) for j in range(self.size)]for i in range(self.size)]
        self.scroll_counter = 0
        self.scroll = 0
    
    def show(self,surface:pygame.Surface):

        super().show(surface)


    def __parseText(self, txt:str) -> str:
        txt = txt.upper()
        allowed = self.font.keys()
        emoji_allowed = list(self.font['emojis'].keys())
        
        ntxt = ''

        for i in range(len(emoji_allowed)):
            
            if txt.find(emoji_allowed[i]) >= 0:
                for j in range(txt.count(emoji_allowed[i])):
                    self.emojis.append(emoji_allowed[i])
                    
                txt = txt.replace(emoji_allowed[i], EMOJI_REP)



        for i in range(min(64, len(txt))):
            if txt[i] in allowed or txt[i] == EMOJI_REP:
                ntxt += txt[i]

        
        return ntxt


    
    def __textToMatrix(self, txt:str, letter_spacing:int = 1) -> list:

        matrix_text = [[0 for _ in range( len(txt) * len(self.font['A']) + (len(self.emojis) * len(self.font['emojis']["*SUS*"])) +  (letter_spacing * len(txt)))] for _ in range(len(self.font['A']))]
        emojiCounter = 0
        
        for k in range(len(txt)):
            
            if txt[k] != EMOJI_REP:
                matChar = self.font[txt[k]]
            else:
                print(self.emojis, emojiCounter)
                matChar = self.font['emojis'][self.emojis[emojiCounter]]


            for i in range(len(matChar)):
                for j in range(len(matChar[i])):
                    
                    x = j
                    y =  (k * len(matChar) + i) + (letter_spacing * k)
                    
                    
                    matrix_text[x][y] = matChar[i][j]


                    

            if txt[k] == EMOJI_REP:
                
                emojiCounter += 1 
                
                        

                
        return matrix_text
    


    def displayText(self,scroll:bool = True, scrollSpeed:float = .1, newColor:tuple = (255, 255, 255)):
        
        
        for i in range(len(self.mat)):
            for j in range(len(self.mat[i])):
                
                if self.matrix_text[j][(i + self.scroll) % (len(self.matrix_text[0] ))]:
                    self.nextFrame[i][j].color = newColor
                else:
                    self.nextFrame[i][j].color = self.bgMat[i][j].color

        if scroll:
            self.scroll_counter += scrollSpeed

            if self.scroll_counter >= 1:
                self.scroll += 1
                self.scroll_counter = 0

    def bgUpdate(self, mouseEvents, color = [100,100, 100]):

        for i in range(len(self.mat)):
            for j in range(len(self.mat[i])):
                self.bgMat[i][j].on_event(self.bgMat[i][j].hover() and mouseEvents['mouse_pressed']['left'],lambda: self.setBgColorAt(i,j,color))





    def setBgColorAt(self,x:int,y:int,color:list[int]):
        
        self.bgMat[x][y].color = color