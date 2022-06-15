import imp
import pygame
from pygame import gfxdraw
from src.gui_elements.utils import * 


class Button():
    
    def __init__(self, rect:pygame.Rect or list[int,int,int,int], color:tuple[int,int,int,int] = (100,100,100,255), outline_color:tuple[int,int,int,int] = (255,255,255,255)) -> None:
        self.rect = pygame.Rect(rect)
        self.color = color
        self.outline_color = outline_color
        self.can_be_clicked = True
        

    def show(self, surface:pygame.Surface) -> None:
        # Box per il contorno
        
        gfxdraw.box(surface, self.rect,self.color)

        #Rectangle per il fill
        gfxdraw.rectangle(surface, self.rect, self.outline_color)


    def glow(self, surface, color:tuple or pygame.Color):
        gfxdraw.box(surface, self.rect, color)



    def hover(self) -> bool:
        
        return True if self.rect.collidepoint(pygame.mouse.get_pos()) else False



    def on_event(self, event:bool, func = None):
        
        if event and (func is not None):
            return func()

    