from email.policy import default
from typing import List


class LedData:

    def __init__(self, size:int =  1, data:list[int] = None, defaultColor = [0,0,0]) -> None:
        if size != None and size >= 1:
            self.__data = [[i,defaultColor[0],defaultColor[1],defaultColor[2]] for i in range(int(size))] if data is None else data
        else:
            raise ValueError("No valid argument for size or data.")


    def fill(self,new_color:list[int]) -> None:
        self.__data = [[i, new_color[0], new_color[1], new_color[2]]for i in range(len(self.__data))]

    @property
    def data(self) -> list:
        return self.__data

    @data.setter
    def data(self, new_val):
        self.__data = new_val

    def __setitem__(self, idx, new_val):
        self.__data[idx] = new_val

    def __getitem__(self, idx) -> list:
        return self.__data[idx]

    def __len__(self) -> int:
        return len(self.__data)
    

    
    
    