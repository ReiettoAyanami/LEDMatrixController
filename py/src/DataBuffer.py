from src.ColorData import *

COLOR_BLACK = [0,0,0]
COLOR_WHITE = [255,255,255]
COLOR_RED = [255,0,0]
COLOR_GREEN = [0,255,0]
COLOR_BLUE = [0,0,255]


class DataBuffer:


    """

    A class which contains a buffer of colors that has to be sent to the Arduino.

    Attributes:
        buffer: (list) the buffer itself

    """

    
    def __init__(self, startBuff:list[ColorData]) -> None:
        
        """
        Args:
            startBuff: a list containg ColorData objects.
        """

        self.__buffer = startBuff
    
    
    def addData(self,newData:list[ColorData]) -> None:
        
        """
        Adds data to the buffer.

        Args:
            newData: a list of ColorData objects.
                
        """

        for d in newData:
            self.__buffer.append(d)

    def clear(self) -> None:

        """
        Clears the buffer.

        """
                
        self.__buffer = []

    def pop(self, idx:int) -> None:

        self.__buffer.pop(idx)


    def __len__(self) -> int:
        return len(self.__buffer)

    def __getitem__(self, key):
        return self.__buffer[key]
    def __setitem__(self, key, newValue):
        self.__buffer[key] = newValue

