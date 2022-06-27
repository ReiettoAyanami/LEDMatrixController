import sys
from typing import Text
from matplotlib.pyplot import text
import pygame
from pygame import RESIZABLE, Rect, gfxdraw
import pygame_gui
import serial
from src.Matrix import Matrix
from src.LedData import LedData, COLOR_BLACK
from src.SerialData import SerialData
from threading import *
from tkinter import colorchooser
from pygame_gui.core import ObjectID
from src.TextMatrix import TextMatrix

#Pygame Stuff
pygame.init()
pygame.font.init()
WINDOW_SIZE = W_WIDTH, W_HEIGHT = (1280,720)
window = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption('LED MATRIX')
w_running = True
manager = pygame_gui.UIManager(WINDOW_SIZE, theme_path='py/theme.json')
clock = pygame.time.Clock()
gColor = [0,0,0]


#Serial stuff

ser = serial.Serial('com5', 9600)
leds = LedData(64, defaultColor=COLOR_BLACK)
serialCom = SerialData(ser, ledDataSize=64)

#Elements
matrixBoard = TextMatrix(rect = (W_WIDTH - W_HEIGHT,0,W_HEIGHT, W_HEIGHT), text="sus *amogus* sus")
matrixBoard.setBorderRadius(20)
#matrixBoard.placeCharOnMatrix(matrixBoard.matrix_text[0], 0,0,(255,255,255))
colorButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(0,0,100,20), text="Colore", manager=manager, tool_tip_text="<b>Scelta del colore</b><br>Farà apparire una finestrà che permetterà la scelta del colore con cui disegnare sulla matrice.") 
eraserButton = pygame_gui.elements.UIButton(relative_rect=Rect(0,20,100,20),text="Gomma", manager=manager, tool_tip_text="<b>Gomma</b><br>Permette di far diventare il pennello nero per far spegnere il led.")
#selection_l = pygame_gui.elements.UIDropDownMenu(["amongus"],"Brightness", Rect(100,100,100,100),manager)
brightnessSlider = pygame_gui.elements.UIHorizontalSlider(pygame.Rect(100,0,200,20), 255, [0, 255], manager, object_id=ObjectID(class_id='@brightness',object_id='#brightness'))



"""
TODO
- Fare un sistema decende di GUI -> in pausa
- Trasferire solo la parte di matrice che cambia -> Suggested by Massimo Sandretti (https://github.com/MassimoSandre)
- Selezione della porta COM
- Dump di uno sketch fatto apposta su arduino -> se non riesco ad ottimizzare decentemente la connessione
- Animazioni

- Essenzialmente basta, penso, spero, dai, speriamo <3

Fatto: 
- Testo


"""
def sendData(connectionStable):

    while connectionStable and w_running:
        serialCom.sendData(leds)


def colorChooseWindow() -> list:
    c = colorchooser.askcolor(title = "Scegliere il colore: ")
    
    return c[0] if c[0] is not None else [0,0,0]

def main():

    w_running = serialCom.w_running = True
    global leds
    global gColor
    test_x = 0 

    serialCom.execute.start()
    mouse_pressed = {'left' : False, 'right':False, 'wheel': False}

    


    while(w_running):
        
        mouse_clicked = {'left' : False, 'right':False, 'wheel': False}
        mouse_moved = False
        mouse_scroll = 0
        
        time_delta = clock.tick(60)/1000.0
        # unprocessed = unprocessed + (last_frame_time - current_time)
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
                serialCom.w_running = False
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


            

            manager.process_events(event)
        

        manager.update(time_delta)
        matrixBoard.setBrightness(int(brightnessSlider.current_value))
        matrixBoard.bgUpdate(mouse_events, gColor)
        serialCom.ledData = matrixBoard.toLEDData()
        
        

        window.fill((0,0,0))
        

        matrixBoard.show(window, show_text=True, scroll=True, newColor=(255,0,0))
        # tm.show(window)
        # tm.displayText(scrollSpeed=.3, newColor=(255,0,0))
        manager.draw_ui(window)
       
    
        pygame.display.update()


        
    
    

    
    



if __name__ == "__main__":
    main()
    
    


    


# while(True):
    
#     for i in range(64):
        
#         h = maprange((0,63), (0,1), i)


#         r, g, b = hsv_to_rgb((h, 1, .05))

#         ser.write(stringifyLEDData([i, int(r * 255), int(g * 255), int(b * 255)]))
    
    #print(ser.readline().decode('ascii'))

        #print(stringifyLEDData([i, int(r * 255), int(g * 255), int(b * 255)]))

        

    

