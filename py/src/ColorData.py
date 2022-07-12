
class ColorData:
    
    """
    An object used to describe what data needs to be sent to the arduino.

    Attributes:
        idx: (int) the index of the pixel that needs to be lit up.
        color: (tuple[int]) the color that the pixel at the given index will assume.

    """


    def __init__(self, idx:int = 0, color:tuple[int] = (0,0,0)) -> None:

        """
        Inits the class.

        Args:

        idx: the index of the pixel that needs to be lit up.
        color: the color that the pixel at the given index will assume.

        """

        self.__idx = idx
        self.__color = color


    def toEncodedString(self) -> str:

        """
        Transforms this object's attributes into an encoded string that will be parsed and interpreted by the arduino.

        Args:
            idx : the index of the element you want to encode.

        Returns:
            A string which is formatted like this:
            
            - .iiirrrgggbbb\\n -> the format.
            - . -> start reading data;
            - iii -> index: 001;
            - rrr -> red color: 020;
            - ggg -> green color: 100;
            - bbb -> blue color: 069;
            - \\n -> stop reading data.


        """


        
        attr = [self.__idx] + [self.__color[i] for i in range(len(self.__color))]
        data = '.'

        
        for i in range(len(attr)):
            
            current = str(attr[i])

            if len(current) < 3:
                
                
                zeros = ''
                for i in range(3 - len(current)):
                    zeros += '0'

                current = zeros + current
                data += current
            else:
                data += current

        data += '\n'
        return data.encode()

    @property
    def idx(self) -> int:
        return self.__idx

    @idx.setter
    def idx(self, new_idx:int = 0) -> None:
        self.__idx = new_idx
    
    @property
    def color(self) -> tuple:
        return self.__color

    @color.setter
    def color(self, new_color:tuple[int] = (0,0,0)) -> None:
        self.__color = new_color
