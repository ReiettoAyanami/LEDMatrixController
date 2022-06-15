import sys
from matplotlib.pyplot import title
import pygame
from pygame import gfxdraw
from re import ASCII
import time
from matplotlib.colors import hsv_to_rgb
import serial
from src.gui_elements.button import Button
from src.Matrix import Matrix
from src.gui_elements.slider import Slider
from src.LedData import LedData, COLOR_BLACK
from src.SerialData import SerialData
from threading import *
from tkinter import colorchooser
from src.gui_elements.string_button import String_Button
 

#Pygame Stuff
pygame.init()
pygame.font.init()
WINDOW_SIZE = W_WIDTH, W_HEIGHT = (1280,720)
window = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption('LED MATRIX')
#clock = pygame.time.Clock()
w_running = True
#Serial stuff

ser = serial.Serial('COM5', 9600)
serialCom = SerialData(ser)
leds = LedData(64, defaultColor=COLOR_BLACK)
matrixBoard = Matrix(rect = (W_WIDTH - W_HEIGHT,0,W_HEIGHT, W_HEIGHT))
colorButton = String_Button((10,10,500,500),"Colore")
gColor = [0,0,0]

"""
TODO

- Fare un sistema decende di GUI
- Selezione della porta COM
- Dump di uno sketch fatto apposta su arduino
- Animazioni
- Testo
- Essenzialmente basta, penso, spero, dai, speriamo <3


"""



def sendData(connectionStable):

    while connectionStable and w_running:
        #leds.set_at(10, [100,100,0])

        serialCom.sendData(leds)


def colorChooseWindow() -> list:
    c = colorchooser.askcolor(title = "Scegliere il colore: ")
    
    return c[0]

def main():

    global w_running
    global leds
    global gColor

    while(not serialCom.connectionStable):

        serialCom.startConnection()



    
    
    dataThread = Thread(target = sendData, args= [serialCom.connectionStable])
    dataThread.start()
    mouse_pressed = {'left' : False, 'right':False, 'wheel': False}

    
    

    while(serialCom.connectionStable and w_running):
        
        mouse_clicked = {'left' : False, 'right':False, 'wheel': False}
        mouse_moved = False
        mouse_scroll = 0
        

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
        

        gColor =  colorChooseWindow() if mouse_clicked['left'] and colorButton.hover() else gColor
        matrixBoard.update(mouse_events, gColor)

        leds = matrixBoard.toLEDData()
        

        window.fill((0,0,0))
        

        matrixBoard.show(window)
        colorButton.show(window)
        
        

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

        

    

