import time
import json
import pygame
from src.errors import errors
from pygame import K_LCTRL, Rect
import pygame_gui
import serial
import sys
from tkinter import messagebox
from src.SerialData import SerialData
from threading import *
from tkinter import colorchooser
from pygame_gui.core import ObjectID
from src.TextMatrix import TextMatrix
import serial.tools.list_ports
from src.ColorData import *



"""
Initializing constants.

"""
config = {}
UIText = {}

with open('configs/config.json', 'r') as j:
    
    config = json.load(j)

with open('configs/lang/' + config['DEFAULT_LANGUAGE'] + '.json', 'r') as j:
    UIText = json.load(j)


MAX_BUFFER_SIZE = config['MAX_BUFFER_SIZE']
ARDUINO_NAME = config['ARDUINO_NAME']


pygame.init()
pygame.font.init()
WINDOW_SIZE = W_WIDTH, W_HEIGHT = config["WINDOW_SIZE"]
window = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption(config['CAPTION'])
w_running = True
manager = pygame_gui.UIManager(WINDOW_SIZE, theme_path=config["THEME_PATH"])
clock = pygame.time.Clock()


#####################################################################################################################
"""
The script right under this comment searches for the arduino by looking at the the COM description.

"""

availableComs = serial.tools.list_ports.comports()
arduinoPort = ''
validFound = False
serialCom = None

"""
Checks if the finding of a port is taking too long, if so it stops all the searching processes
"""
def checkPortFindingTime(startTime:float, secondsOffset:float = 15):
    
    global validFound
    global serialCom
    global w_running

    now = time.time()
    while now <=  startTime + secondsOffset:
        now = time.time()
        if validFound:
            return
    if not validFound:
        for s in serials:
            validFound = True
            s.ser.cancel_read()
            s.ser.cancel_write()
        w_running = False


"""
Checks if a port is the arduino, if so it sets 'arduinoPort' as the checked port, it stops all the other threads if the port is found.
"""
def checkPort(comName:str, sCom:SerialData) -> None:
    global validFound
    global arduinoPort
    global serialCom

    while not sCom.connectionStable and not validFound:
        sCom.startConnection()
        if validFound:
            break
        validFound = sCom.connectionStable
        arduinoPort = comName
    if arduinoPort == comName:
        
        
        serials.remove(sCom)
        for s in serials:
            s.ser.cancel_read()
            s.ser.cancel_write()

        serialCom = sCom


"""
Initializes threads and communications for COM port.
"""

serials = [SerialData(serial.Serial(availableComs[i].name,config["DEFAULT_BAUD_RATE"])) for i in range(len(availableComs))] # SerialData ojects to connect to the arduino
findingProcesses = [Thread(target=checkPort, args = [availableComs[i].name, serials[i]]) for i in range(len(availableComs))] # All the threads needed to find the port (one for every USB device that can receive/send data)

t = time.time()
timeThread = Thread(target=checkPortFindingTime, args=[t, config["MAX_SEARCH_TIME"]]) # Needed to count how long the port finding is taking

for process in findingProcesses:
    process.start()

timeThread.start()

"""
Render Loading Screen.
"""
f = pygame.font.Font("fonts/roboto/Roboto-Bold.ttf",20)
points = ""
dotsCounter = 0

while not validFound:

    window.fill((0,0,0))

    textSurf = f.render(UIText['UI']['LOADING_SCREEN'] + points, True, (255,255,255))
    window.blit(textSurf, (W_WIDTH / 2 - textSurf.get_width() / 2, W_HEIGHT / 2 - textSurf.get_height()/2))

    pygame.display.update()
 
    dotsCounter = dotsCounter + 1 if dotsCounter <= 4000 else 0

    points = ""
    for i in range(int(dotsCounter/1000)):
        points += "."


"""
Shows a message if everything has gone wrong.
"""

if arduinoPort == '' and validFound:
    messagebox.showerror("COM_ERROR", errors['COM_ERROR'])
    pygame.quit()
    sys.exit()
    

"""
Pretty garbage code ngl.
But as long as it works, i mean...
"""


##################################################################################################################





matrixBoard = TextMatrix(rect = (W_WIDTH - W_HEIGHT,0,W_HEIGHT, W_HEIGHT), text=' ')
matrixBoard.setBorderRadius(20)
colorButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(0,0,100,20), text=UIText['UI']['PENCIL_COLOR'], manager=manager, tool_tip_text=UIText['UI_TOOLTIPS']['PENCIL_COLOR']) 
textColorButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(0,20,100,20), text=UIText['UI']['TEXT_COLOR'], manager=manager, tool_tip_text=UIText['UI_TOOLTIPS']['TEXT_COLOR']) 
eraserButton = pygame_gui.elements.UIButton(relative_rect=Rect(0,40,100,20),text=UIText['UI']['ERASER'], manager=manager, tool_tip_text=UIText['UI_TOOLTIPS']['ERASER'])
brightnessSlider = pygame_gui.elements.UIHorizontalSlider(pygame.Rect(100,0,200,20), 50, [0, 255], manager, object_id=ObjectID(class_id='@brightness',object_id='#brightness'))
textChoose =  pygame_gui.elements.UITextEntryLine(pygame.Rect(0,60,150,40),manager)
latestText = pygame_gui.elements.UIDropDownMenu([], UIText['UI']['TEXT_HISTORY'], pygame.Rect(0,100,150,30), manager)
try:
    with open(config["LATEST_TEXT_LIST_PATH"], 'r') as t:
        for line in t.readlines():
            latestText.options_list.append(line.removesuffix("\n"))
except FileNotFoundError:
    open(config["LATEST_TEXT_LIST_PATH"], 'w').close()


"""
TODO

- Fare un sistema decende di GUI -> in pausa
- Animazioni
- Salvare configurazioni
- Essenzialmente basta, penso, spero, dai, speriamo <3

Fatto: 
- Testo
- Porta COM


"""
def colorChooseWindow() -> list:
    c = colorchooser.askcolor(title = "Scegliere il colore: ")
    
    return c[0] if c[0] is not None else [0,0,0]

def main():

    global ser
    global w_running

    if w_running:
        w_running = serialCom.windowRunning = True

    gColor = [255,255,255]
    tColor = [255,255,255]
    mouse_pressed = {'left' : False, 'right':False, 'wheel': False}
    serialCom.executor.start()
    
    while(w_running):
        
        mouse_clicked = {'left' : False, 'right':False, 'wheel': False}
        mouse_moved = False
        mouse_scroll = 0
        
        
        time_delta = clock.tick(60)/1000.0
        mouse_events = {
            'mouse_clicked': mouse_clicked,
            'mouse_pressed': mouse_pressed,
            'mouse_moved': mouse_moved,
            'mouse_scroll': mouse_scroll
        }

        

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                w_running = False
                serialCom.connectionStable = False
                serialCom.windowRunning = False
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.MOUSEMOTION:
                mouse_moved = True

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == pygame.BUTTON_LEFT:
                    mouse_pressed['left'] = True
                    mouse_clicked['left'] = True

                elif event.button == pygame.BUTTON_MIDDLE:
                    mouse_pressed['wheel'] = True
                    mouse_clicked['wheel'] = True

                elif event.button == pygame.BUTTON_RIGHT:
                    mouse_pressed['right'] = True
                    mouse_clicked['right'] = True

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == pygame.BUTTON_LEFT:
                    mouse_pressed['left'] = False
                elif event.button == pygame.BUTTON_MIDDLE:
                    mouse_pressed['wheel'] = False
                elif event.button == pygame.BUTTON_RIGHT:
                    mouse_pressed['right'] = False

            if event.type == pygame.MOUSEWHEEL:
                mouse_scroll = event.y
            

            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == colorButton:
                    gColor = colorChooseWindow()
                if event.ui_element ==  textColorButton:
                    tColor = colorChooseWindow()

                if event.ui_element == eraserButton:
                    gColor = [0,0,0]

            if event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED:
                if event.ui_element == textChoose:
                    
                    if len(event.text):
                        matrixBoard.setText(event.text)
                        
                        """
                        if the length of the options in the latest text is greater than the maximum it will pop the first element in the list
                        and add the latest text selected else it will just add the new element to the option list and write in the file.
                        """


                        if len(latestText.options_list) >= config["MAX_LATEST_LEN"]:
                            latestText.options_list.pop(0)
                            latestText.options_list.append(event.text)
                            with open(config['LATEST_TEXT_LIST_PATH'], 'w') as l:
                                l.writelines([latestText.options_list[i] + "\n" for i in range(len(latestText.options_list))])
                        else:
                            with open(config['LATEST_TEXT_LIST_PATH'], 'a') as l:
                                l.write(event.text +  "\n")

                            latestText.options_list.append(event.text)
                    else:
                        matrixBoard.setText(" ")
            if event.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
                if event.ui_element == latestText:

                    matrixBoard.setText(event.text)
            
           

            manager.process_events(event)




        manager.update(time_delta)
        
        if pygame.key.get_pressed()[K_LCTRL] and mouse_clicked['left'] and matrixBoard.getMousePosition():
            relativePos = matrixBoard.getMousePosition()
            gColor = matrixBoard.bgMat[relativePos[0]][relativePos[1]].color


        if serialCom.connectionStable:
            matrixBoard.bgMouseUpdate(mouse_events, gColor)
            
            

            if len(serialCom.dataBuffer) <  MAX_BUFFER_SIZE:
                matrixBoard.setBrightness(int(brightnessSlider.current_value))
                matrixBoard.displayText(True,.1,tColor)
                changes = matrixBoard.getMatrixChanges()
                serialCom.dataBuffer.addData(changes)
       
            
        
    
        window.fill((0,0,0))
        
        


        matrixBoard.show(window)
        manager.draw_ui(window)

        
        
    
        pygame.display.update()

        
        
    
    



if __name__ == "__main__":
    main()