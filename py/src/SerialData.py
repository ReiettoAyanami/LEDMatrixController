import serial
from src.DataBuffer import DataBuffer
from threading import Thread



class SerialData:


    def __init__(self, ser:serial.Serial, comData = "17\n", inMinData = 50) -> None:
        
        self.ser = ser
        self.comData = comData
        

        self.inCount = 0
        self.__inMinData = inMinData
        self.inData = ''
        
        self.IN_CONNECTION_STARTER = b'\x11'
        self.OUT_CONNECTION_CONFIRM = b'\x12'

        self.inConnectionStarted = False
        self.inConnectionStable = False

        self.outConnectionStarted = False
        self.outConnectionStable = False 
        
        self.connectionStable = False

        self.dataBuffer = DataBuffer([])

        self.w_running = False
        self.execute = Thread(target=self.communicate)
        self.isBusy = False




    def startConnection(self):

        self.inData = self.ser.read()


        if self.inData == self.IN_CONNECTION_STARTER:
            self.inConnectionStarted = True 
            self.inCount += 1
        
        if self.inCount >= self.__inMinData:
            self.inConnectionStable = True

        if(self.inConnectionStable):
            
            self.outConnectionStarted = True
            while(not self.outConnectionStable):

                self.ser.write(self.comData.encode())
                
                if self.ser.read() == self.OUT_CONNECTION_CONFIRM:
                    self.outConnectionStable = True


        if(self.outConnectionStable and self.inConnectionStable):
            self.connectionStable = True


    
    def sendData(self):

        if self.dataBuffer.buffer:
            self.ser.write(self.dataBuffer.toEncodedStringAt(0))
            self.dataBuffer.buffer.pop(0)

    
    def communicate(self):

        while not self.connectionStable:
            self.startConnection()

        while self.connectionStable and self.w_running:

            self.sendData()
            


    

