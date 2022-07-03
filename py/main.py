import json
import tkinter
import pygame
from pygame import Rect
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


"""
Initializing constants.

"""
config = {}

with open('py/config.json', 'r') as j:
    
    config = json.load(j)

MAX_BUFFER_SIZE = config['MAX_BUFFER_SIZE']
ARDUINO_NAME = config['ARDUINO_NAME']



pygame.init()
pygame.font.init()
WINDOW_SIZE = W_WIDTH, W_HEIGHT = config["WINDOW_SIZE"]
window = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption(config['CAPTION'])
w_running = True
manager = pygame_gui.UIManager(WINDOW_SIZE, theme_path='py/theme.json')
clock = pygame.time.Clock()




"""
The script right under this comment searches for the arduino by looking at the the COM name.

"""

availableComs = serial.tools.list_ports.comports()
arduinoPort = ''

for com in availableComs:

    if com.description.find(ARDUINO_NAME) > -1:
        arduinoPort = com.name
        

if arduinoPort == '':
    messagebox.showerror("COM Error", "No arduino connected to COM Port.\nIf you are sure your arduino is connected then change the property \"ARDUINO_NAME\" in config.json")
    sys.exit()

ser = serial.Serial(arduinoPort, config["DEFAULT_BAUD_RATE"])
serialCom = SerialData(ser)



matrixBoard = TextMatrix(rect = (W_WIDTH - W_HEIGHT,0,W_HEIGHT, W_HEIGHT), text=' ')
matrixBoard.setBorderRadius(20)
colorButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(0,0,100,20), text="Colore", manager=manager, tool_tip_text="<b>Scelta del colore</b><br>Farà apparire una finestrà che permetterà la scelta del colore con cui disegnare sulla matrice.") 
eraserButton = pygame_gui.elements.UIButton(relative_rect=Rect(0,20,100,20),text="Gomma", manager=manager, tool_tip_text="<b>Gomma</b><br>Permette di far diventare il pennello nero per far spegnere il led.")
brightnessSlider = pygame_gui.elements.UIHorizontalSlider(pygame.Rect(100,0,200,20), 255, [0, 255], manager, object_id=ObjectID(class_id='@brightness',object_id='#brightness'))
textChoose =  pygame_gui.elements.UITextEntryLine(pygame.Rect(0,40,150,40),manager)

latestText = pygame_gui.elements.UIDropDownMenu([], "Latest Text Used", pygame.Rect(0,80,150,30), manager)

with open(config["LATEST_TEXT_LIST_PATH"], 'r') as t:
    for line in t.readlines():
        latestText.options_list.append(line.removesuffix("\n"))
"""
TODO


- Fare un sistema decende di GUI -> in pausa
- Animazioni
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
    w_running = serialCom.windowRunning = True
    gColor = [0,0,0]
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
        matrixBoard.setBrightness(int(brightnessSlider.current_value))
        
        if serialCom.connectionStable:
            matrixBoard.bgMouseUpdate(mouse_events, gColor)
            
            

            if len(serialCom.dataBuffer.buffer) <  MAX_BUFFER_SIZE:
                matrixBoard.displayText(True,.1,(100,0,120))
                changes = matrixBoard.getMatrixChanges()
                serialCom.dataBuffer.addData(changes)

        
    
        window.fill((0,0,0))

        matrixBoard.show(window)
        manager.draw_ui(window)
       
    
        pygame.display.update()

        
        
    
    

    
    



if __name__ == "__main__":
    main()