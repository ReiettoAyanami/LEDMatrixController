import sys
from tkinter import messagebox
from src.errors import errors
import serial
from src.DataBuffer import DataBuffer
from threading import Thread
from serial import SerialTimeoutException, SerialException


class SerialData:
    

    """
    Transfers data to the arduino through the COM port using a serial.Serial object.

    Attributes:
        ser: (serial.Serial) transfers data to the arduino.
        comData: (str) data sent to the arduino to ensure stable connection.
        inConnectionStarted: (bool) determines if in connection is started.
        outConnectionStarted: (bool) determines if out connection is started.
        inConnectionStable: (bool) determines if in connection is stable.
        outConnectionStable: (bool) determines if out connection is stable.
        connectionStable: (bool) determines if both in & out connection are stable
        IN_CONNECTION_STARTER: (str) message to the program that data is coming from the arduino.
        inCount: (int) amount of data received from the arduino.
        __inMinData: (int) minimun amount of data to receive for establishing a stable connection.
        OUT_CONNECTION_CONFIRM: (str) message from the arduino to stop data.
        inData: (str) data coming from the arduino.
        dataBuffer: (DataBuffer) buffer of pixel to send to the arduino after the connection is stable.
        windowRunning: (bool) if the pygame window is running.
        executor: (Thread) a thread to continuosly send data to the arduino without interfering with the pygame window.
    
    """


    def __init__(self, ser:serial.Serial, comData = "17\n", inMinData = 50) -> None:
        
        """
        Args:
            ser: object to send / receive data from the arduino.
            comData: string to send to the arduino.
            inMinData: the minimun amount of data to be sure that the connection is stable.
        """


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

        self.windowRunning = False
        self.executor = Thread(target=self.communicate)





    def startConnection(self) -> None:

        """
        Starts the in/out connection with the arduino.

        """

        try:
            self.inData = self.ser.read()
        except SerialException:
            messagebox.showerror("Connection Error", errors["CONNECTION_ERROR"])
            sys.exit()


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


    
    def sendData(self) -> None:
        
        """
        Sends the first element of dataBuffer and then deletes it from the buffer.
        
        """


        if self.dataBuffer.buffer:

            try:
                self.ser.write(self.dataBuffer.toEncodedStringAt(0))
                self.dataBuffer.buffer.pop(0)
            except SerialException:
                messagebox.showerror("Connection Error", errors["CONNECTION_ERROR"])
                self.connectionStable = False
                self.windowRunning = False
                sys.exit()
        
    def communicate(self) -> None:
        """
        Handles connection between arduino and the program.

        """


        while not self.connectionStable:
            self.startConnection()

        while self.connectionStable and self.windowRunning:
            
            self.sendData()



    

