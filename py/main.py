from pickletools import pyfloat
import pydoc
import pygame
from pygame import Rect
import pygame_gui
import serial
import sys
from src.SerialData import SerialData
from threading import *
from tkinter import colorchooser
from pygame_gui.core import ObjectID
from src.TextMatrix import TextMatrix



MAX_BUFFER_SIZE = 64



pygame.init()
pygame.font.init()
WINDOW_SIZE = W_WIDTH, W_HEIGHT = (1280,720)
window = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption('LED MATRIX')
w_running = True
manager = pygame_gui.UIManager(WINDOW_SIZE, theme_path='py/theme.json')
clock = pygame.time.Clock()

ser = serial.Serial('com5', 9600)
serialCom = SerialData(ser)


matrixBoard = TextMatrix(rect = (W_WIDTH - W_HEIGHT,0,W_HEIGHT, W_HEIGHT), text='Buone Vacanze *amogus* ')
matrixBoard.setBorderRadius(20)
colorButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(0,0,100,20), text="Colore", manager=manager, tool_tip_text="<b>Scelta del colore</b><br>Farà apparire una finestrà che permetterà la scelta del colore con cui disegnare sulla matrice.") 
eraserButton = pygame_gui.elements.UIButton(relative_rect=Rect(0,20,100,20),text="Gomma", manager=manager, tool_tip_text="<b>Gomma</b><br>Permette di far diventare il pennello nero per far spegnere il led.")
brightnessSlider = pygame_gui.elements.UIHorizontalSlider(pygame.Rect(100,0,200,20), 255, [0, 255], manager, object_id=ObjectID(class_id='@brightness',object_id='#brightness'))



"""
TODO


- Fare un sistema decende di GUI -> in pausa
- Animazioni
- Selezione della porta COM
- Essenzialmente basta, penso, spero, dai, speriamo <3

Fatto: 
- Testo


"""
def colorChooseWindow() -> list:
    c = colorchooser.askcolor(title = "Scegliere il colore: ")
    
    return c[0] if c[0] is not None else [0,0,0]

def main():

    w_running = serialCom.windowRunning = True
    gColor = [0,0,0]
    serialCom.execute.start()
    mouse_pressed = {'left' : False, 'right':False, 'wheel': False}

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


            

            manager.process_events(event)

        

        manager.update(time_delta)
        matrixBoard.setBrightness(int(brightnessSlider.current_value))
        
        if serialCom.inConnectionStable:
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
    
    


    


# while(True):
    
#     for i in range(64):
        
#         h = maprange((0,63), (0,1), i)


#         r, g, b = hsv_to_rgb((h, 1, .05))

#         ser.write(stringifyLEDData([i, int(r * 255), int(g * 255), int(b * 255)]))
    
    #print(ser.readline().decode('ascii'))

        #print(stringifyLEDData([i, int(r * 255), int(g * 255), int(b * 255)]))

        

    

