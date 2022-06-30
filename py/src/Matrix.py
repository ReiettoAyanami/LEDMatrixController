import pygame
from pygame import Rect
from src.button import Button


class Matrix:

    """
    ### Matrix

    A class used to graphically represent the led matrix connected to the arduino.

    #### Attributes:

    - `pos`: (`tuple`) the top left corner of the matrix.
    - `buttonSize`: (`tuple`) the size of the buttons.
    - `size`: (`int`) the size in pixels of the matrix.
    - `mat`: (`list[list[Button]]`) a list containing buttons that represents every pixel in the physical matrix.
    - `brightness`: (`int`) the brightness that has to be sent to the physical matrix.
    - `changed`: (`list[dict]`) the pixel changed from the last frame sent to the arduino.
    - `nextFrame`: (`list[list[Button]]`) a matrix containing the next frame that will be displayed and then swapped if different from the current frame contained in `mat`.


    #### Args:

    - `pos`: the top left corner of the matrix.
    - `buttonSize`: the size of the buttons.
    - `rect`: the general dimensions of the matrix, if assigned, pos and buttonSize will be ignored and the respective attributes will be calculated based on the rect's attributes.
    - `size`: the size in pixels of the matrix.

    
    """


    def __init__(self,pos:tuple = (0,0),buttonSize:tuple = (1,1),rect:pygame.Rect = None, size:int = 8) -> None:
        self.pos = self.x, self.y = pos
        self.buttonSize = self.buttonW, self.buttonH = buttonSize

        if rect:
            self.pos = self.x, self.y = Rect(rect).topleft
            self.buttonSize = self.buttonW, self.buttonH = Rect(rect).w/size, Rect(rect).h/size

        self.size = size
        self.changed = []
        self.nextFrame = [[Button((self.x + (self.buttonW * i), self.y + (self.buttonH * j), self.buttonW, self.buttonH), color=[0,0,0]) for j in range(self.size)]for i in range(self.size)]
        self.mat = [[Button((self.x + (self.buttonW * i), self.y + (self.buttonH * j), self.buttonW, self.buttonH), color=[0,0,0]) for j in range(self.size)]for i in range(self.size)]
        self.brightness = 255

    def show(self, surface:pygame.Surface) -> None:
        
        """
        Displays the matrix on a given surface.

        #### Args:
        - `surface`: the surface you want the matrix displayed on.
        """

        for i in range(len(self.mat)):
            for j in range(len(self.mat[i])):
                self.mat[i][j].show(surface)
                self.mat[i][j].on_event(self.mat[i][j].hover(), lambda: self.mat[i][j].glow(surface, [155,155,155,100]))


    def mouseUpdate(self, mouseEvents:dict, color:tuple | list = [100,100, 100]) -> None:

        """
        Changes the color of the button you are hovering on when clicked.

        #### Args:
        - `mouseEvents`: a dictionary containing every mouse event.
        - `color`: the color that the button will be changed to.
        
        """

        for i in range(len(self.mat)):
            for j in range(len(self.mat[i])):
                self.mat[i][j].on_event(self.mat[i][j].hover() and mouseEvents['mouse_pressed']['left'],lambda: self.setColorAt(i,j,color))
                
    def setBrightness(self, newBrightness:list[int | float]) -> None:
        """
        Changes the brightness parameter.

        #### Args:
        - `newBrightness`: the new brightness value.
        """


        self.brightness = newBrightness



        
    

    def setColorAt(self,x:int,y:int,color:list[int]):
        
        """
        Updates the button color at a given position.

        #### Args:
        - `x`: the x position on the matrix.
        - `y`: the y position on the matrix.
        - `color`: the color that will replace the old one.

        """


        self.mat[x][y].color = color


    def getMatrixChanges(self) -> list[dict]:
        
        """
        Keeps track of the buttons changed on the matrix and changes them.


        Dict is formatted in this way:
        - {'idx': (`int`), 'color':`list[int]`)}
        """


        self.changed = []

        for i in range(len(self.mat)):
            for j in range(len(self.mat[i])):

                if self.mat[i][j].color != self.nextFrame[i][j].color:
                    self.mat[i][j].color = self.nextFrame[i][j].color
                    self.changed.append({"idx":((j * self.size )+ i),"color": [int(self.mat[i][j].color[k] * self.brightness/255) for k in range(3)]})
                    

        return self.changed

    def setBorderRadius(self, borderRadius:int) -> None:
        
        """
        Sets the matrix's border radii to a given value.

        #### Args:
        - `borderRadius`: the value that the border radii will be set to.
        """

        self.mat[-1][0].set_corners({'topleft':0, 'topright':borderRadius, 'bottomleft':0, 'bottomright':0})
        self.mat[0][0].set_corners({'topleft':borderRadius, 'topright':0, 'bottomleft':0, 'bottomright':0})
        self.mat[0][-1].set_corners({'topleft':0, 'topright':0, 'bottomleft':borderRadius, 'bottomright':0})
        self.mat[-1][-1].set_corners({'topleft':0, 'topright':0, 'bottomleft':0, 'bottomright':borderRadius})

