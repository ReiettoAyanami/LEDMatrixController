COLOR_BLACK = [0,0,0]
COLOR_WHITE = [255,255,255]
COLOR_RED = [255,0,0]
COLOR_GREEN = [0,255,0]
COLOR_BLUE = [0,0,255]


class DataBuffer:


    def __init__(self, startBuff:list[dict]) -> None:
        

        self.buffer = []
        for d in startBuff:
            self.buffer.append([d['idx'], d['color'][0], d['color'][1], d['color'][2]])
    
    
    def addData(self,newData:list[dict]):
            for d in newData:
                self.buffer.append([d['idx'], d['color'][0], d['color'][1], d['color'][2]])


    def clear(self):
        self.buffer = []

    def toEncodedStringAt(self,idx:int) -> str:
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



