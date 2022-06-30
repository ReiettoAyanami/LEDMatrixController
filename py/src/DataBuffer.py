COLOR_BLACK = [0,0,0]
COLOR_WHITE = [255,255,255]
COLOR_RED = [255,0,0]
COLOR_GREEN = [0,255,0]
COLOR_BLUE = [0,0,255]


class DataBuffer:


    """
    ### DataBuffer

    A class which contains a buffer of colors that has to be sent to the Arduino.

    #### Attributes:
    - `buffer`: (`list`) the buffer itself

    #### Args:
    - `startBuff`: a list containg dictionaries containing an 'idx' and a 'color' property.


    """

    
    def __init__(self, startBuff:list[dict]) -> None:
        
        self.buffer = []
        for d in startBuff:
            self.buffer.append([d['idx'], d['color'][0], d['color'][1], d['color'][2]])
    
    
    def addData(self,newData:list[dict]) -> None:
        
        """
        Adds data to the buffer.

        #### Args:
        - `newData`: a list of dictionaries formatted exactly like the buffer for initialize the class.
                
        """

        for d in newData:
            self.buffer.append([d['idx'], d['color'][0], d['color'][1], d['color'][2]])

    def clear(self):

        """
        Clears the buffer.

        """
                
        self.buffer = []

    def toEncodedStringAt(self,idx:int) -> str:

        """
        Encodes a buffer's element at a given index in the following format:

        '.iiirrrgggbbb\\n'

        . -> start reading data;
        iii -> index: 001;
        rrr -> red color: 020;
        ggg -> green color: 100;
        bbb -> blue color: 069;
        \\n -> stop reading data.

        #### Args:
        - `idx` : the index of the element you want to encode.

        """


        s = "."

        for i in range(len(self.buffer[idx])):

            d =  self.buffer[idx][i]
            ed = 0

            if d > 0:
                while int(d / (10 ** ed)) > 0:
                    ed +=1
            else:
                ed = 1
                
            z = 3 - ed
            
            

            for _ in range(z):
                s += '0'
            s+= str(self.buffer[idx][i])
        s += "\n"
        
        return s.encode()



