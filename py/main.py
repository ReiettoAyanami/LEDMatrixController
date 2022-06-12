from ast import arg
from random import randint, random

import pygame
from re import ASCII
import time
from matplotlib.colors import hsv_to_rgb
import serial
from src.gui_elements.slider import Slider
from src.LedData import LedData
from src.SerialData import SerialData
from threading import *

#Pygame Stuff
pygame.init()
pygame.font.init()
WINDOW_SIZE = W_WIDTH, W_HEIGHT = (1000,1000)
window = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption('LED MATRIX')
#clock = pygame.time.Clock()

#Serial stuff
ser = serial.Serial('COM5', 9600)
sd = SerialData(ser)
ld = LedData(64, defaultColor=[0,0,255])

s = Slider((100,100, 100, 10))

def dataLoop():
    sd.sendData(ld)

def main():

    

    while(not sd.connectionStable):

        sd.startConnection()


    dataThread = Thread(target=dataLoop)
    

    w_running = True
    mouse_pressed = {'left' : False, 'right':False, 'wheel': False}

    
    dataThread.start()
    dataThread.join()

    while(w_running):
        
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
            

        window.fill((0,0,0))


        s.show(window)
        s.update(mouse_events)
        ld.fill([int(s.get_value() * 255), int(s.get_value() * 255), int(s.get_value() * 255)])
        dataThread.run()
        
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

        

    

