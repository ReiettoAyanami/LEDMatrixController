from src.button import Button
from src.Matrix import Matrix
import pygame
import json

EMOJI_REP = u'\ufffd'

class TextMatrix(Matrix):
    
    """

    A type of Matrix which is used to display text, it can also display images behind said text.

    Attributes:

        pos: (tuple) the top left corner of the matrix.
        buttonSize: (tuple) the size of the buttons.
        size: (int) the size in pixels of the matrix.
        mat: (list[list[Button]]) a list containing buttons that represents every pixel in the physical matrix.
        brightness: (int) the brightness that has to be sent to the physical matrix.
        changed: (list[dict]) the pixel changed from the last frame sent to the arduino.
        font: (dict) a dictionary containing the alphabet + some character like '/', '\\', '?", [...] and also some self-made emojis in the 'emoji'dict.
        emojis: (list[str]) a list of special characters that are not representable with an unicode character.
        text: (str) a parsed string containing only the characters in the set provided in font.
        matrixText: (list[list[int]]) a list representation of the parsed text.
        nextFrame: (list[list[Button]]) a matrix containing the next frame that will be displayed and then swapped if different from the current frame contained in mat.
        bgMat: (list[list[Button]]) a matrix used to represent the background of the image, which will not affect the text.
        scrollCounter:  (int) a variable that increments every frame, once it reaches 1, the scroll variable will get updated
        scroll: (int) represents how much the text has been shifted.

    Usable emoji list:

        *sus*: a face that shows perplexity over something.
        *amogus*: a pixelated version of the amongus character.
        *dead*: a skeleton.
        *cat*: a cat.
        *:)*: the classic smiley face.
        *>:(*: the classic not-so-smiley face.
        *:(*: me writing docs, also some people can recognise this as a sad face.
        *^_^*: very happy face.
        *-_-*: bored face.
        *<3*: a little heart.
        
    """



    def __init__(self,pos:tuple = (0,0),buttonSize:tuple = (1,1),rect:pygame.Rect = None, size:int = 8, text:str = "Hello World!", fontPath:str = "py\\fonts\\MatrixFonts\\8_bit_font.json") -> None:
        super().__init__(pos, buttonSize, rect, size)
        
        """
        Args:

            pos: the top left corner of the matrix.
            buttonSize: the size of the buttons.
            rect: the general dimensions of the matrix, if assigned, pos and buttonSize will be ignored and the respective attributes will be calculated based on the rect's attributes.
            size: the size in pixels of the matrix.
            text: the text that will be rendered on the matrix.
            fontPath: the path where the font for the matrix is stored.
        """


        self.emojis = []
        with open(fontPath, 'r') as j:
            self.font:dict = json.load(j)

        self.text = self.__parseText(text)
        
        self.matrixText = self.__textToMatrix(self.text)
        self.bgMat = [[Button((self.x + (self.buttonW * i), self.y + (self.buttonH * j), self.buttonW, self.buttonH), color=[0,0,0]) for j in range(self.size)]for i in range(self.size)]
        self.scrollCounter = 0
        self.scroll = 0
    
    


    def __parseText(self, txt:str) -> str:

        """
        Parses a given string containing only characters that are in font.

        Args:
            txt: the string that has to be parsed. 

        Returns:
            The text that will contain only the characters in font.
        
        """

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


    
    def __textToMatrix(self, txt:str, letterSpacing:int = 1) -> list[list[int]]:
        
        """
        Transforms a parsed string into text, taking also in account letter spacing.

        Args:
            txt: parsed string.
            letterSpacing: the amount of space from one letter to another.

        Returns:
            A matrix containing 0s and 1s to represent the given string.
            
        """
        

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
    


    def displayText(self,canScroll:bool = True, scrollSpeed:float = .1, newColor:tuple = (255, 255, 255)) -> None:

        """
        Displays the text based on the arguments passed.

        Args:
            canScroll: determines if the text will scroll.
            scrollSpeed: the speed at which the text will scroll.
            newColor: the color which the text will render with.
        
        """
        
        for i in range(len(self.mat)):
            for j in range(len(self.mat[i])):
                
                if self.matrixText[j][(i + self.scroll) % (len(self.matrixText[0] ))]:
                    self.nextFrame[i][j].color = newColor
                else:
                    self.nextFrame[i][j].color = self.bgMat[i][j].color

        if canScroll:
            self.scrollCounter += scrollSpeed

            if self.scrollCounter >= 1:
                self.scroll += 1
                self.scrollCounter = 0


    def bgMouseUpdate(self, mouseEvents:dict, color:list = [100,100, 100]) -> None:


        """
        Updates the background matrix.

        Args:
            mouseEvents: a dictionary containing every mouse event.
            color: the color that the button will be changed to.
        
        """
        for i in range(len(self.mat)):
            for j in range(len(self.mat[i])):
                self.bgMat[i][j].on_event(self.bgMat[i][j].hover() and mouseEvents['mouse_pressed']['left'],lambda: self.setBgColorAt(i,j,color))





    def setBgColorAt(self,x:int,y:int,color:list[int]):
        
        """
        Updates the button color at a given position on the background matrix.

        Args:
            x: the x position on the background matrix.
            y: the y position on the background matrix.
            color: the color that will replace the old one.

        """

        self.bgMat[x][y].color = color